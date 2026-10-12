---
name: competitor-ads-intel
description: "Finds the brand's top competitors, confirms them with the person, finds each one's Meta Ad Library page, pulls every image ad they are running with Apify, and lays them out in Paper: one page per competitor, every ad numbered, longest-running first. The person looks and says the numbers they like; those become the references /paper-ads remakes. Run after /paper-ads-prep and before /paper-ads."
group: Ads
summary: Finds your competitors, pulls every image ad they run into Paper, one page each, so you can pick the ones worth remaking
version: 1.0.0
outputs: [competitor-ads]
requires: [Paper, Apify]
optional: [Firecrawl or a browser for finding each competitor's Facebook page, Perplexity for finding competitors]
---

# Competitor ads intel: see what's working, pick what to remake

> **Where brands live.** A brand's folder is `04-Brand/clients/<brand>/` when the
> project has a `04-Brand/clients/` folder, otherwise `brands/<brand>/`. Every
> `brands/<brand>/` path in this file means that folder. Read
> `.claude/skills/paper-ads-prep/references/system.md` once per session: it holds the
> rules every skill in this system follows, including who this is for.

The person should never have to hunt through the Meta Ad Library by hand. This
skill finds the competitors, pulls their ads, and puts them all on the Paper
canvas where they can see everything at once. **It never picks for them.**
Choosing which ads are worth copying takes human taste; the skill's job is to
make that choice easy.

A pull lives at `brands/<brand>/generation/competitor-ads/<YYYY-MM-DD>/`.
Create it before use.

## 1. Find the top competitors

Read `intelligence/brand-strategy.md` (Competitive landscape),
`counter-positioning.md` and `products.json`, plus anything the project's own
files say about competitors. Then search the web (Perplexity if connected,
otherwise built-in search) for brands selling the same thing to the same
people. Prefer brands that actually advertise on Facebook and Instagram:
direct-to-consumer brands and challengers over giant retailers whose ads are
mostly catalog or video.

Pick the **top 3 to 5**. For each, one line on why it's a competitor.

## 2. Confirm them with the person

This is the one question this skill asks. Plain and short:

> "Here's who I think your top competitors are:
> 1. **Liquid I.V.**: the biggest name in electrolyte mixes
> 2. **Ultima Replenisher**: same zero-sugar pitch, aimed at daily use
> 3. ...
>
> Are these right? Anyone to drop, or anyone I'm missing? A brand you admire
> outside your category works too, if you like their ads."

Take their answer as final. Add anyone they name, drop anyone they reject.
Don't ask again.

## 3. Find each competitor's Facebook page

The Ad Library is organised by Facebook page, so each competitor needs its
**page link** (`https://www.facebook.com/liquidiv`). Never search the Ad
Library by brand name: a name search returns any ad that mentions the name.

In order, stop at the first that works:
1. **The competitor's own website:** read the footer and header for the
   Facebook link (Firecrawl if connected, otherwise web fetch).
2. **A web search** for `<brand> site:facebook.com`.
3. **The Ad Library in a browser,** if one is connected: search the brand and
   copy the page link from the advertiser card.

If one can't be found, say so in one line and carry on with the rest; the
person can paste the link if they have it. Write the list to
`<batch>/competitors.json`:

```json
[{"name": "Liquid I.V.", "page_url": "https://www.facebook.com/liquidiv"}]
```

## 4. Pull their image ads with Apify

Check Apify is connected, directly or through Composio
(`.claude/skills/paper-ads-prep/references/tools.md`). Use the actor
**`automation-lab/facebook-ads-library`** with:

```json
{"pageUrls": ["<each page_url>"], "country": "ALL", "activeStatus": "active",
 "mediaType": "image_and_meme", "maxAds": 100}
```

**State the cost first.** It is $0.005 to start plus about $0.0005 per ad, so
five competitors at up to 100 ads each is about a quarter. Under a dollar: say
the number and go. Over a dollar: ask. Read the actual charge off the run
afterwards and say it.

Run it, wait for it to finish (poll the run; it takes a minute or two), and note
the run's **dataset id**. Don't page the ads through the chat: the script below
reads them straight from Apify.

**No Apify at all:** say once, kindly, what it would add (every ad on one page
instead of scrolling), with the connect line from `tools.md`. Then give them
the Ad Library links you found in step 3 so they can browse and screenshot the
ones they like by hand.

## 5. Download, clean and sort

From the project root:

```bash
python3 .claude/skills/competitor-ads-intel/fetch-competitor-ads.py --dataset <datasetId> --competitors <batch>/competitors.json --out <batch>
```

It keeps active image ads only (no catalog or video ads), downloads each image
straight away (Meta's image links expire), drops near-duplicates, and sorts
**longest-running first**, because a brand that keeps paying for an ad is
telling you it works. Each competitor gets a folder of `01.jpg`, `02.jpg`, ...
and an `index.json`; the batch gets a `summary.json` with each competitor's Ad
Library link. If a competitor comes back with few or no image ads (some brands
run mostly video), say so in plain words.

**Up to 50 ads per competitor, then ask.** The script keeps at most 50 unique
ads each, which is about what one page can show at a glance. If it says a
competitor reached the limit with more not shown, ask before going over, and
lay out nothing for them until they answer:

> "Ultima is running more than 50 image ads, about 48 more I haven't shown.
> Want all of them on their page, or are 50 plenty?"

On a yes, rerun for just that competitor with a higher limit, `--only <slug>
--max 150`, which costs nothing extra. If the script also says Apify returned
100 or more ads, they may be running even more than the pull caught: offer a
bigger pull (`maxAds` up to 500), with its cost first.

## 6. Lay them out in Paper, one page per competitor

Open the brand's Paper file (`paper_file_id` in `intelligence/setup.json`;
with none yet, create `ad-engine · {Brand}`, open it and record the id, without
asking). Then:

```bash
node .claude/skills/competitor-ads-intel/layout-competitor-pages.js --file <paper_file_id> --batch <batch>
```

Each competitor gets its own Paper page, "Competitor · Liquid I.V.", with every
image ad numbered, how long it has been running under it, and their Ad Library
link at the top. Take a screenshot of one page to check it rendered.

## 7. Let them pick

Tell them where to look and how to answer, in one short message:

> "Your competitors' ads are in Paper now, one page each, longest-running first.
> Flip through them and tell me the ones you like, like 'Liquid I.V. 3 and 7,
> Ultima 12'. Pick 2 or 3 with a clear idea: a bold claim, a before-and-after,
> a big number. Those are the ones I'll remake for your brand."

When they answer, copy each pick into
`generation/paper-ads/ad-references/` as `<competitor-slug>-<NN>.jpg`, confirm
the list back in one line, and hand off:

> "Got them. Run `/paper-ads` and I'll remake those for your brand."

If they select ads in Paper instead of saying numbers, read the selection and
match it to the numbers on the page.

## Rules

- Never pick the ads for them, and never rank them as "best". Longest-running
  is a fact, not a verdict.
- Nothing is spent without saying the cost first.
- These ads are references for format and idea only. `/paper-ads` rewrites
  every word for the person's brand and never copies another brand's name,
  product, claims or exact lines.
