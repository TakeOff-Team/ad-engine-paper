#!/usr/bin/env python3
"""
competitor-ads-intel / fetch-competitor-ads.py

Turns one or more Apify runs of `automation-lab/facebook-ads-library` into a
clean, numbered set of competitor image ads on disk, ready to lay out in Paper.

  python3 .claude/skills/competitor-ads-intel/fetch-competitor-ads.py \
      --dataset <datasetId> [--dataset <datasetId> ...] \
      --competitors <batch>/competitors.json \
      --out <batch> [--max 50] [--only <slug,slug>]

competitors.json (written by Claude before the pull):
  [{"name": "Liquid I.V.", "page_url": "https://www.facebook.com/liquidiv"}, ...]

What it does, per competitor:
  - keeps ads that are active, have an image, and are not catalog (DPA) or video ads
  - downloads the first image of each ad straight away (Meta's image links expire)
  - drops near-duplicates (the same creative run many times), keeping the longest-running
  - sorts longest-running first: a brand that keeps paying for an ad is telling you it works
  - saves 01.jpg, 02.jpg ... into <batch>/<competitor-slug>/ with an index.json

Writes <batch>/summary.json with each competitor's page id, Ad Library link and counts.
The dataset is read from Apify's API directly, so nothing bulky passes through the chat.
APIFY_TOKEN is used if set; run datasets are usually readable without it.
"""
import argparse, datetime, io, json, os, re, sys, urllib.parse, urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Error: Pillow is not installed. Run: pip install pillow")

FIELDS = "adArchiveId,adLibraryUrl,pageId,pageName,pageUrl,isActive,startDate,displayFormat,imageUrls,bodyText,title"
SKIP_FORMATS = {"DPA", "VIDEO"}
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "competitor"


def norm_page(u):
    if not u:
        return ""
    p = urllib.parse.urlparse(u.strip().lower())
    path = p.path.rstrip("/")
    if path.startswith("/pg/"):
        path = path[3:]
    q = urllib.parse.parse_qs(p.query)
    if "id" in q and path.endswith("profile.php"):
        return "id:" + q["id"][0]
    return path


def fetch_dataset(ds):
    items, offset = [], 0
    token = os.environ.get("APIFY_TOKEN")
    while True:
        url = f"https://api.apify.com/v2/datasets/{ds}/items?clean=true&format=json&limit=1000&offset={offset}&fields={FIELDS}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"} if token else {})
        try:
            page = json.load(urllib.request.urlopen(req, timeout=120))
        except Exception as e:
            sys.exit(f"Error: could not read Apify dataset {ds} ({e}). If it needs a token, set APIFY_TOKEN.")
        items += page
        if len(page) < 1000:
            return items
        offset += 1000


def ahash(img):
    g = img.convert("L").resize((16, 16))
    px = list(g.tobytes())
    avg = sum(px) / len(px)
    return sum(1 << i for i, v in enumerate(px) if v > avg)


def days_running(start, today):
    try:
        return (today - datetime.date.fromisoformat(start[:10])).days
    except Exception:
        return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", action="append", required=True)
    ap.add_argument("--competitors", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max", type=int, default=50, help="most ads to keep per competitor (ask the person before going higher)")
    ap.add_argument("--only", default="", help="comma-separated competitor slugs to (re)process; others keep their existing folders")
    a = ap.parse_args()

    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    comps = json.load(open(a.competitors))
    for c in comps:
        c["slug"] = c.get("slug") or slug(c["name"])
        c["_key"] = norm_page(c.get("page_url", ""))

    rows = []
    for ds in a.dataset:
        rows += fetch_dataset(ds)
    today = datetime.date.today()

    # match each ad to a competitor by its Facebook page
    by_comp = {c["slug"]: [] for c in comps}
    unmatched = 0
    for r in rows:
        key = norm_page(r.get("pageUrl", ""))
        hit = next((c for c in comps if c["_key"] and (c["_key"] == key or c.get("page_id") == r.get("pageId"))), None)
        if not hit:
            name = (r.get("pageName") or "").lower()
            hit = next((c for c in comps if c["name"].lower() in name or name in c["name"].lower()), None) if name else None
        if not hit:
            unmatched += 1
            continue
        hit.setdefault("page_id", r.get("pageId"))
        hit.setdefault("page_name", r.get("pageName"))
        by_comp[hit["slug"]].append(r)

    summary = {"pulled": today.isoformat(), "datasets": a.dataset, "ads_returned": len(rows), "unmatched": unmatched, "competitors": []}
    only = {x.strip() for x in a.only.split(",") if x.strip()}
    old = {}
    if only and (out / "summary.json").exists():
        old = {x["slug"]: x for x in json.load(open(out / "summary.json")).get("competitors", [])}
    for c in comps:
        if only and c["slug"] not in only and c["slug"] in old:
            summary["competitors"].append(old[c["slug"]])
            continue
        ads = [r for r in by_comp[c["slug"]]
               if r.get("isActive", True) and r.get("imageUrls") and (r.get("displayFormat") or "").upper() not in SKIP_FORMATS]
        ads.sort(key=lambda r: days_running(r.get("startDate", ""), today), reverse=True)
        folder = out / c["slug"]
        folder.mkdir(exist_ok=True)
        for old_f in folder.glob("*.jpg"):
            old_f.unlink()
        kept, hashes, failed, used = [], [], 0, 0
        for r in ads:
            if len(kept) >= a.max:
                break
            used += 1
            img = None
            # Some regional CDN hosts (e.g. scontent.fosu2-2.fna.fbcdn.net) resolve IPv6-only;
            # the signed path also works on the generic scontent.xx.fbcdn.net host.
            src = r["imageUrls"][0]
            for u in (src, re.sub(r"//scontent[^/]*\.fbcdn\.net/", "//scontent.xx.fbcdn.net/", src)):
                try:
                    data = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
                    img = Image.open(io.BytesIO(data))
                    img.load()
                    break
                except Exception:
                    img = None
            if img is None:
                failed += 1
                continue
            if min(img.size) < 200:
                continue
            h = ahash(img)
            if any(bin(h ^ x).count("1") <= 12 for x in hashes):
                continue  # near-duplicate of a longer-running ad already kept
            hashes.append(h)
            n = len(kept) + 1
            f = folder / f"{n:02d}.jpg"
            img.convert("RGB").save(f, "JPEG", quality=90)
            kept.append({"n": n, "file": str(f), "days_running": days_running(r.get("startDate", ""), today),
                         "start": r.get("startDate"), "format": r.get("displayFormat"), "ad_id": r.get("adArchiveId"),
                         "ad_library_url": r.get("adLibraryUrl"), "width": img.width, "height": img.height,
                         "headline": (r.get("title") or "")[:120], "text": (r.get("bodyText") or "")[:200]})
        json.dump(kept, open(folder / "index.json", "w"), indent=2)
        pid = c.get("page_id")
        summary["competitors"].append({
            "name": c["name"], "slug": c["slug"], "page_url": c.get("page_url"), "page_id": pid,
            "ad_library": f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&media_type=image_and_meme&view_all_page_id={pid}" if pid else None,
            "image_ads_found": len(ads), "kept": len(kept), "download_failed": failed, "folder": str(folder),
            "hit_cap": len(kept) >= a.max and used < len(ads), "not_yet_checked": len(ads) - used,
            "pull_maybe_capped": len(by_comp[c["slug"]]) >= 100})
    json.dump(summary, open(out / "summary.json", "w"), indent=2)

    print(f"{len(rows)} ads returned, {unmatched} not from these competitors")
    for c in summary["competitors"]:
        print(f"  {c['name']}: {c['kept']} unique image ads kept (of {c['image_ads_found']} active image ads)" + (f", {c['download_failed']} images failed" if c["download_failed"] else "")
              + (f"  ** reached the {a.max} limit, {c['not_yet_checked']} more not shown: ask before raising --max" if c.get("hit_cap") else "")
              + ("  ** Apify returned 100+ ads, so they may run even more: a bigger pull costs more" if c.get("pull_maybe_capped") else ""))
    print(f"summary: {out / 'summary.json'}")


if __name__ == "__main__":
    main()
