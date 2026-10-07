#!/usr/bin/env python3
"""
extend-plate.py — build the 9:16 plate from the approved 4:5 plate, by geometry first.

Usage (from project root):
  python3 .claude/skills/paper-ads/extend-plate.py <concept-folder> [--plate path] [--bbox x0,y0,x1,y1] [--anchor 0.55]

Takes the approved 4:5 plate and its product box (from spec.json, written by
product-bbox.py, or passed with --bbox), scales and places the 4:5 inside a
1080×1920 canvas so the product box lands inside the 9:16 product stage
(x120–810, y430–1350) and clear of the platform rail (x840–1080, y560–1500), and
writes two files next to spec.json:

  <name>-fullscreen_9x16-canvas_vN.png   the 4:5 pasted on a flat ground sampled from its edges
  <name>-fullscreen_9x16-mask_vN.png     white where the model may paint, black where it must not

Then the image model fills the empty areas (references/higgsfield.md, "Deriving
the 9:16"), the result is filed with save-plate.py, and the product box for the
9:16 is already known: it is written to spec.json here, so preflight.js can check
text against it. --anchor sets where the product's vertical centre sits in the
stage, 0.5 = middle. Free, no network.
"""
import json, sys
from pathlib import Path
from PIL import Image

W, H = 1080, 1920
STAGE = (120, 430, 810, 1350)
RAIL = (840, 560, 1080, 1500)


def _arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def _latest(out: Path, stem: str):
    c = sorted(out.glob(f"{stem}_v*.png"), key=lambda p: int(p.stem.rsplit("_v", 1)[1]))
    return c[-1] if c else None


def _next(out: Path, stem: str) -> Path:
    n = 1
    while (out / f"{stem}_v{n}.png").exists():
        n += 1
    return out / f"{stem}_v{n}.png"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    out = Path(sys.argv[1]); spec = json.loads((out / "spec.json").read_text()); name = spec.get("output_name", out.name)
    v45 = spec.get("variants", {}).get("feed_4x5", {})
    plate = Path(_arg("--plate")) if _arg("--plate") else _latest(out, f"{name}-feed_4x5-plate")
    if not plate or not plate.exists():
        sys.exit("Error: no approved 4:5 plate found. Pass --plate.")
    bbox = [int(x) for x in _arg("--bbox").split(",")] if _arg("--bbox") else v45.get("product_bbox")
    if not bbox:
        sys.exit("Error: no product box for the 4:5. Run product-bbox.py on feed_4x5 first, or pass --bbox.")
    src = Image.open(plate).convert("RGB"); sw, sh = src.size
    bx0, by0, bx1, by1 = bbox; bw, bh = bx1 - bx0, by1 - by0
    anchor = float(_arg("--anchor", 0.55))

    # scale so the product fits the stage with a margin, never upscaling past 1:1
    sx0, sy0, sx1, sy1 = STAGE; stage_w, stage_h = sx1 - sx0, sy1 - sy0
    margin = 0.9
    scale = min(1.0, stage_w * margin / bw, stage_h * margin / bh, W / sw)
    nw, nh = round(sw * scale), round(sh * scale)
    scaled = src.resize((nw, nh), Image.Resampling.LANCZOS)
    pbx0, pby0, pbx1, pby1 = (round(v * scale) for v in bbox)
    pbw, pbh = pbx1 - pbx0, pby1 - pby0
    # place: product centred horizontally in the stage, vertical centre at `anchor` of the stage
    target_cx = (sx0 + sx1) / 2
    target_cy = sy0 + stage_h * anchor
    ox = round(target_cx - (pbx0 + pbw / 2)); oy = round(target_cy - (pby0 + pbh / 2))
    # keep the pasted photo inside the canvas horizontally when it is as wide as the canvas
    if nw >= W: ox = 0
    ox = max(min(ox, W - nw), 0) if nw <= W else ox
    oy = max(min(oy, H - nh), 0) if nh <= H else oy
    final_bbox = [pbx0 + ox, pby0 + oy, pbx1 + ox, pby1 + oy]

    # flat ground sampled from the photo's edge pixels, so the fill has a plausible colour to continue
    edge = [src.getpixel((x, y)) for x in (0, sw - 1) for y in range(0, sh, max(1, sh // 60))] + \
           [src.getpixel((x, y)) for y in (0, sh - 1) for x in range(0, sw, max(1, sw // 60))]
    ground = tuple(sum(p[i] for p in edge) // len(edge) for i in range(3))
    canvas = Image.new("RGB", (W, H), ground); canvas.paste(scaled, (ox, oy))
    mask = Image.new("L", (W, H), 255); mask.paste(0, (ox, oy, ox + nw, oy + nh))
    cpath = _next(out, f"{name}-fullscreen_9x16-canvas"); mpath = cpath.with_name(cpath.name.replace("-canvas_", "-mask_"))
    canvas.save(cpath); mask.save(mpath)

    v916 = spec.setdefault("variants", {}).setdefault("fullscreen_9x16", {})
    v916.update({"aspect_ratio": "9:16", "derived_from": plate.name, "canvas": cpath.name, "mask": mpath.name,
                 "photo_box": [ox, oy, ox + nw, oy + nh], "product_bbox": final_bbox, "product_bbox_source": "extend-plate", "scale": round(scale, 4)})
    (out / "spec.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")

    inside = final_bbox[0] >= sx0 and final_bbox[1] >= sy0 and final_bbox[2] <= sx1 and final_bbox[3] <= sy1
    in_rail = final_bbox[2] > RAIL[0] and final_bbox[3] > RAIL[1] and final_bbox[1] < RAIL[3]
    print(f"  ✓ {cpath.name}  (4:5 scaled {scale:.3f}, placed at x{ox}, y{oy})")
    print(f"  ✓ {mpath.name}  (white = area the model fills)")
    print(f"  product box in 9:16: x{final_bbox[0]}–{final_bbox[2]}, y{final_bbox[1]}–{final_bbox[3]}  stage: {'inside' if inside else 'OUTSIDE'}  rail: {'clear' if not in_rail else 'ENTERED'}")
    if not inside or in_rail:
        sys.exit("  ! geometry failed: the product does not fit the stage at this anchor. Try --anchor or a tighter --bbox.")


if __name__ == "__main__":
    main()
