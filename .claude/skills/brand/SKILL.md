---
name: brand
description: Run when the user wants to set up their brand, add their brand to the project, provides a website URL / brand guidelines / positioning doc for onboarding, OR says "add this to my brand context" (a product, image, doc, logo, font, or fact to fold into an existing brand). Works from a website URL, brand documents, or a manual description. Builds the brand's operating system under brands/[brand-name]/intelligence/: strategy, counter-positioning, colour palette + typography + logo read off the live site, brand voice, a portable context capsule, and a full product catalog index — plus incrementally adds new products/assets/facts to an existing brand at any time. Everything downstream (static ads) is personalised to the brand from the start. Multiple brands can be set up and run side-by-side.
group: Core
summary: Point it at a URL, get a brand brain. Run this first. Also folds new products, images, docs and facts into an existing brand at any time
version: 1.0.0
outputs: []
requires: []
---

# Brand Setup & Brand Operating System

`/brand` builds and maintains a brand's **operating system** — the shared brain
every other skill reads so anything generated is on-brand. It runs in two modes:

- **Full setup** — a new brand from a website URL, brand documents, or a manual
  description. Produces the complete `intelligence/` folder below.
- **Incremental add** — "add this to my brand context": fold a new product,
  image, document, logo, font, or fact into an **existing** brand without
  redoing setup. See **Incremental mode** near the end.

Detect the mode first: if the user names an existing brand under `brands/`, or
says "add this to my brand context / catalog", route to **Incremental mode**.
Otherwise run **Full setup**.

---

## Output — the brand folder

A brand has two compartments and `/brand` creates both (Step 2). Everything
`/brand` itself writes lands in `intelligence/`:

```
brands/[brand-name]/intelligence/
  visual-guidelines.md     ← visual identity + PROMPT MODIFIER  (brand-detection marker)
  brand-strategy.md        ← personality/values, audience, competitive landscape
  counter-positioning.md   ← counter-position + value proposition package
  brand-voice.md           ← how the brand writes (copy layer)
  brand-context.md         ← one-page portable capsule (paste into any AI tool)
  avatars.md               ← the 3–5 named people the brand sells to (Step 6e)
  offers.md                ← the closed list of offers any page may use (Step 6e)
  setup.json               ← brand type + the image tool this brand generates with (Step 0b)
  learnings.md             ← rules and defaults earned from reviews (written by /paper-ads, not here)
  color-palette.json       ← structured colour tokens (accent / neutral · name·hex·use)
  typography.json          ← typefaces (role·family·source·weights) + design-system pointer
  products.json            ← product CATALOG index { brand, updated, products:[…] }
  product-images/          ← FLAT product images: [slug]-01.jpg, [slug]-02.jpg …
  logos/                   ← logo files (.svg,.png) — scraped from the site, manual drop-in as fallback
  fonts/                   ← font files — auto-downloaded (open-license) + added manually
  context-uploads/         ← RAW archive of every "add this to my brand context" drop ([YYYY-MM-DD]-[slug].ext)
```

> **`avatars.md` and `offers.md` are load-bearing downstream.** `/ad-angles`
> writes every angle and headline for the avatars in `avatars.md`, in their own
> pain words, and takes every offer from `offers.md` — it is forbidden from
> inventing an offer. Formats: `references/avatars.md`, `references/offers.md`.

> **`context-uploads/` is the raw-input trail, not a derived doc.** Every time the
> user drops more context into an existing brand, the material is archived here
> verbatim (a dated copy) *and* its substance is folded into the derived docs
> above. It is distinct from `brand-context.md` — that is the one-page capsule
> *generated from* the brand; this is the pile of source material the brand was
> *built from*. See **Incremental mode**.

> **`visual-guidelines.md` is the brand-detection marker.** Its presence at
> `intelligence/visual-guidelines.md` is what every downstream
> skill (`/paper-ads`, …) uses to recognise a
> real brand. **Always write it.** Product images are always **flat** in
> `product-images/` (`[slug]-01.jpg`) — files that share leading filename tokens
> group as one product; never use per-product subfolders.

### The `generation/` compartment

`/brand` also creates the brand's second compartment, `generation/` — where every
*other* skill writes. `/brand` never puts files in it; it creates the empty
folders so a brand's shape is complete from day one:

```
brands/[brand-name]/generation/
  ad-scout/             ← /ad-scout (optional): category ad pulls + findings
  ad-angles/                 ← /ad-angles: angles, copy and Meta ad text per campaign
  paper-ads/        ← /paper-ads: the built ads, per campaign and concept
    ad-references/              ← drop winning-ad format refs here
```

The `*-references/` and `*-uploads/` folders are **inboxes** — a human drops files
there for a skill to read, so they exist from the start and assets can be staged
before any skill has run. Every other folder is an **outbox**: the skill creates
`[output-name]/` inside its category at generation time.

There is no canonical list — every skill declares its own `outputs:` and
`inboxes:` in its `SKILL.md` frontmatter, and `brand.py` derives the scaffold
from whatever skills are installed. Add a skill folder and its folders scaffold;
remove one and nothing else breaks. `python3 .claude/skills/brand/brand.py
--validate` checks every declaration.

**Format references** — read each as you build the matching file; they hold the
exact structure:

- `references/brand-strategy.md` — structure of `brand-strategy.md`
- `references/counter-positioning.md` — the counter-positioning framework (Step 4)
- `references/color-palette.md` — structure of `color-palette.json`
- `references/typography.md` — structure of `typography.json`
- `references/brand-voice.md` — structure of `brand-voice.md`
- `references/brand-context.md` — structure of the portable capsule
- `references/setup.md` — structure of `setup.json`, and the wording of the image-tool question

---

## Step 0 — Determine intake mode

**Asking this question is your entire first response**, unless the person has
already answered it in their request ("intake mode: both", a URL plus a folder
of documents, "here are my brand docs"). Then say which mode you understood in
one line and move on; do not ask again. Otherwise output the four options
below exactly as listed — no preamble, no lead-in, no narrating that you are
about to ask. Then stop and wait for the reply: do not scaffold folders, fetch
the site, or research anything until the user has picked an intake mode.

> "How would you like to set up your brand? I can work from:
> 1. **A website URL** — I'll read that exact site, then research around it
> 2. **Brand documents** — paste or share your brand guidelines, style guide, positioning doc, deck, or any written materials
> 3. **Both** — a URL plus supporting documents for the most complete picture
> 4. **Neither yet** — tell me about the brand and I'll build it from what you share
>
> Which works best for you?"

Adapt the research stages below to the answer. All modes produce the same
`intelligence/` output — they just draw from different sources.

---

## Step 0b — Two setup questions (brand type and image tool)

Ask these together, in your **second** response, right after the person answers
the intake question and before the research starts. Read `references/setup.md`
for the exact wording, then write the answers to
`./brands/[brand-name]/intelligence/setup.json` once the brand folder exists
(Step 2).

1. **What does the brand sell?** Do not ask this when the site answers it. A
   store selling masks is a product brand; a course is a service brand. Say
   what you concluded in one line ("Physical product, so the photos will show
   it and I'll need a size reference") and let the person correct it. Ask only
   when the site is genuinely ambiguous. This decides whether a base photo
   shows the product (with a size reference) or a scene with no product in it.
2. **Which image tool do you want to use for the photography?** Higgsfield or
   fal.
3. **Is this your brand, a client's, or one you're practising on?** A client
   brand means every unverified offer, every named person and every competitor
   mention waits for sign-off. A practice brand means those get flagged and the
   build goes on. Record it as `relationship`.
4. **Whose ad account runs these, and where do they send people?** The
   advertiser (the brand itself, or an affiliate or agency running on its
   behalf) and the exact landing link, including any affiliate or tracking
   parameters. Every piece of ad text points at that link. Never assume the
   website's own URL. Explain the trade in plain words (the reference file has the wording):
   what each costs, what each needs set up, and that only the photograph ever
   costs anything, because every word on the ad is an editable layer in Paper.
   If they have neither, recommend one and say why. If they have both, let them
   pick and say it can be changed later by editing one line.

Also say, once, that the ads are built in **Paper**, so Paper Desktop needs to
be installed and connected before the build step. Do not make it a question.

Do not ask anything else here. Everything else is found on the site or asked at
the step that needs it. Write `brand_type`, `image_tool`, `relationship`,
`advertiser` and `landing_url` to `setup.json`.

**A decision made once is not reopened.** If you told the person how a case
will be handled ("I'll only use offers that are live on the site"), do not ask
them to decide it again later. Apply it.

---

## Step 1 — Research the brand

**The URL the user gave you _is_ the brand.** It is the anchor and the source of
truth — not the brand's *name*, which may belong to several unrelated companies.
Load that exact URL first, establish from the site itself who this company is,
and only then reach for external search to fill gaps. Work through all applicable
stages before writing.

### Stage A — Document intake (if documents / pasted content provided)

Read everything the user shares first. Extract: voice & positioning, personality
& values, audience signals (psychographics, beliefs, brands they love),
competitive cues, founding story / methodology, and the specific outcome the
customer gets. Note anything ambiguous so you can fill it via web research or by
asking.

### Stage B — Live site audit (if URL provided)

Fetch the exact URL the user gave and read it before any external search. Crawl
the site's *own* pages for the substance — `/about`, product pages, stockists,
the footer — rather than reaching for the open web.

- **Identity — do this first:** what this company actually *is*: category, what
  it sells, who runs it, where it operates, which markets. The footer is usually
  the most reliable read — legal entity name, registered address, company or
  registration number, contact details. Write this down. It is what makes every
  later search unambiguous, and what you check external sources against.
- **Language and voice:** hero headline, About page, 3–4 product descriptions —
  the 5 adjectives that most precisely describe how this brand sounds. Be
  specific, not "clean" or "premium". (Feeds `brand-voice.md`.)
- **Photography on site:** lighting quality (hard/soft, natural/studio), colour
  grade (warm/cool/matte/contrast), typical composition and subject.
- **Type in use:** headline weight/style; body treatment (leading, caps, tracking).
- **Colour in use:** which colour leads, which is accent, backgrounds, CTA colour.
- **Layout feel:** airy vs. dense; grid vs. organic.
- **Packaging:** shape, material, finish, label placement, distinctive details.
- **Audience & positioning:** who it's clearly for, what it claims to do
  differently, what it stands against, the outcome it promises, competitors
  named or implied.

### Stage C — Web research (supplements the site; never overrides it)

External search fills gaps the site left. It never establishes who the brand is —
Stage B already did that.

**Brand names collide.** A bare-name search returns whichever company SEO
favours, and that is frequently not the user's. Before searching, build a
disambiguator out of the Stage B identity — the domain, the category, the home
market, the legal entity — and carry it in every query:

- ✅ `site:blueelephant.co about` · `blueelephant.co eyewear Seoul`
- ❌ `"Blue Elephant" founding story` — returns a Thai restaurant group on a
  different domain: an unrelated company that merely shares the name

**Verify before you use.** A result counts only if it is demonstrably the same
entity — served from the brand's own domain, or matching the identity you pinned
in Stage B (same category, market, or legal entity). If a source can't be tied
back to that, discard it. Never blend two same-named companies into one brand.
When the site and a search result disagree, the site wins.

Then search — disambiguated — for what the site didn't answer:

- founding story, mission — personality, values, the counter-position
- `[brand] vs [competitor]`, `best [category] brands` — the competitive landscape
- reviews, Reddit / Substack / Amazon — customer language, pain points, what they tried before
- font / typeface names, hex codes, brand colours — though the live DOM read in
  Steps 2 and 2b is far stronger evidence; use search only to *name* what the
  read already found
- design system, brand guidelines, style guide, press kit — also try the brand's
  own `/design`, `/brand`, `/guidelines`, `/styleguide`, `/press` paths
- design agency, rebrand — often unlocks precise language about the identity
- **Meta Ad Library** — the creative formats, messaging angles, and visual treatment they run now

Skip this stage if the brand has no public presence beyond its own site — note
the gap instead. A thin brand that is correct beats a rich brand built on the
wrong company.

### Stage D — Market context

Identify 2–3 direct competitors and 1–2 indirect ones (different category, same
job-to-be-done). For each, note one specific visual or positioning choice that
sets this brand apart. If no competitors are established yet, ask: "Which brands
do you admire or position against?"

---

## Step 2 — Scaffold folders, write brand-strategy.md + color-palette.json

Create both compartments first — one command, from the project root:
```bash
python3 .claude/skills/brand/brand.py --scaffold "[brand-name]"
```

This creates `brands/[brand-name]/intelligence/` (`product-images/`, `logos/`,
`fonts/`, `context-uploads/`), plus the full
`generation/` tree every other skill writes to. It is idempotent and never
touches existing files, so rerun it freely: on a brand mid-setup, or to backfill one
created before a new skill existed. It is the only
`brand.py` command that runs from the project root; every later step in this
skill runs from inside `intelligence/`.

Read `references/brand-strategy.md`, then write
`./brands/[brand-name]/intelligence/brand-strategy.md` — three sections
(Personality & Values, Target Audience, Competitive Landscape). Where information
is genuinely missing, note the gap rather than guessing.

Then read `references/color-palette.md` and write
`./brands/[brand-name]/intelligence/color-palette.json`. Two buckets — `accent`
(genuinely coloured colours) and `neutral` (blacks/whites/grays/surfaces, ordered
dark→light); keep `primary`, `secondary`, `background` as empty arrays for
compatibility. Uppercase 6-digit hex. Source the colours in priority order:

1. **Live computed styles (preferred — a real read).** If a Chrome browser is
   connected, with the homepage loaded run the entire body of
   `.claude/skills/brand/extract-site-colors.js` via `javascript_tool` on that
   tab. It returns `{ suggested, ranked, signals }` read from the rendered DOM.
   Use `suggested` as the spine; fold each colour into `accent` or `neutral`.
2. **Stated brand guidelines / docs.** If the user shared colour values, those
   are authoritative.
3. **WebFetch fallback (no browser).** Parse the homepage HTML/CSS for `#hex` and
   `rgb()` values, frequency-rank them, cross-reference the logo / `og:image`.

**Screenshot fallback** — if the automated read fails and no docs were shared,
ask: *"I couldn't read the colours off your site automatically. Drop a screenshot
of your palette — a swatch sheet, a brand-guideline colour page, or just your
homepage — and I'll read the exact hexes from it."* Read it with the Read tool
and pull the hexes. Always produce a complete best-effort palette — flag any
colour you're unsure about.

---

## Step 2b — Typography & design system

Right after colour, capture the brand's **fonts** and any published **design
system**. Read `references/typography.md`, then write
`./brands/[brand-name]/intelligence/typography.json`. Source in priority order:

1. **Live computed fonts (preferred).** With a Chrome browser on the homepage,
   run the entire body of `.claude/skills/brand/extract-site-fonts.js` via
   `javascript_tool`. It returns `{ suggested, ranked, signals, loaded, links }`
   — `suggested` is the role→family map; `loaded`/`links` set each font's
   `source` and `weights`.
2. **Stated guidelines / a found design-system page** — authoritative; record it
   under `design_system`.
3. **WebFetch fallback** — parse the homepage for `@font-face` names, Google
   Fonts `<link href="fonts.googleapis.com/css2?family=…">`, Adobe
   `use.typekit.net` / `fonts.adobe.com` kits.

**WhatFont / screenshot fallback** — if the read fails: *"I couldn't read your
fonts automatically. Install the free WhatFont Chrome extension, click your
headline and body text on your live site, and tell me the names — or send a
screenshot of your type page."*

Always include the verbatim `note` verification caveat in `typography.json` (fonts
are inferred — a model can misread them). Then collect the actual font files for
open-license faces:

```bash
cd ./brands/[brand-name]/intelligence && python3 ../../../.claude/skills/brand/brand.py --fetch-fonts "Inter,Playfair Display"
```

Only `google-fonts` families resolve; licensed/foundry faces (Adobe, Monotype,
self-hosted) must be dropped into `fonts/` by hand — list them in
`typography.json` and tell the user in the Step 8 report.

**Always describe the typography, even when the name or the file is missing.**
Whether or not you can pin the exact family or download it, write a short visual
description of each role's type into `typography.json` (the `description` field —
see `references/typography.md`) and into the **Typography** section of
`visual-guidelines.md`. Cover: category (serif / sans / slab / mono / display),
stroke contrast (high vs. monoline), weight and width, and any distinctive
letterforms or treatment (all-caps, tight tracking, humanist vs. geometric). When
a face can't be identified (read failed, no docs, user didn't confirm) or can't be
downloaded (a licensed/foundry face), set `family` to the best guess or
`"unknown"` — but never leave the type undescribed. Downstream image and ad skills
fall back to this written description to keep type on-brand when the actual font
name and file aren't available.

---

## Step 2c — Logo

Collect the brand's logo into `./brands/[brand-name]/intelligence/logos/`.
Source in priority order:

1. **HTTP fetch (preferred — no browser needed).** Run:
   ```bash
   cd ./brands/[brand-name]/intelligence && python3 ../../../.claude/skills/brand/brand.py --fetch-logo https://brand.com
   ```
   Tries schema.org JSON-LD `Organization.logo`, then a header/nav `<img>`, then
   the largest declared favicon — in that order — and downloads what it finds as
   `logo.[ext]` (+ `logo-icon.[ext]` if a distinct favicon was also found
   alongside a stronger primary logo). Never overwrites a file already in
   `logos/`.
2. **Live browser read (when the HTTP fetch finds nothing — a JS-rendered
   header, an inline SVG logo, or a bot-blocked site).** With a Chrome browser
   on the homepage, run the entire body of
   `.claude/skills/brand/extract-site-logo.js` via `javascript_tool`. It returns
   `suggested: { type, value, source }`:
   - `type: 'svg'` — `value` is already markup; write it directly to
     `logos/logo.svg` with the Write tool.
   - `type: 'image'` — `value` is an absolute URL; download it with
     `brand.py --logo-url "[value]"`.
   If `suggested` picked the wrong element, check `candidates` for the right one.
3. **Manual fallback.** If both automated reads come up empty, ask: *"I
   couldn't find your logo automatically. Could you drop the logo file (.svg or
   .png) into `brands/[brand-name]/intelligence/logos/`?"*

A favicon-only result is a square mark, not the full wordmark — note this in
the Step 8 report so the user knows to drop in a better file if they have one.

---

## Step 3 — Counter-positioning (sub-skill)

After `brand-strategy.md` and **before** product collection, run the
counter-positioning framework. Read `references/counter-positioning.md` in full
and follow it exactly — a seven-phase process ending in the Phase 7 package
written to `./brands/[brand-name]/intelligence/counter-positioning.md`. Honour
its behavioural rules (always name what the brand stands against; never accept a
value proposition without a "without" clause). Briefly summarise the recommended
counter-position and value proposition in chat, then continue.

---

## Step 4 — Write visual-guidelines.md (the brand-detection marker)

Write `./brands/[brand-name]/intelligence/visual-guidelines.md` — the file the
app and every image skill read. Ground it in the **exact** hexes from
`color-palette.json` and font names from `typography.json` (not eyeballed
values). Use this structure:

```
# [Brand Name] — Visual Guidelines

## Brand identity
**Name:** [as styled]
**Tagline:** [if any]
**Design agency:** [if known]
**Positioning:** [one sentence — who it's for, what it does, how it sounds]
**Voice:** [5 precise adjectives]
**What sets it apart:** [one sentence per closest competitor]

## Colour palette
- **Primary:** [name] — #XXXXXX
- **Secondary:** [name] — #XXXXXX
- **Accent:** [name] — #XXXXXX
- **Background:** [description] — #XXXXXX (list all backgrounds the brand uses)
- **CTA / button:** [fill #XXXXXX] / [text #XXXXXX] — [shape, radius, weight]
(Hexes must match color-palette.json exactly.)

## Typography
- **Headline:** [typeface] — [weight range]
- **Body / UI:** [typeface] — [style]
- **Treatment:** [all-caps, tracking, leading — distinctive choices]
(Names must match typography.json exactly.)

## Photography style
- **Lighting:** [hard/soft, natural/studio, direction]
- **Colour grade:** [temperature, saturation, contrast, film quality — be specific]
- **Composition:** [framing, subject placement, negative space]
- **What appears in frame:** [subjects, body language, props, styling]
- **Surfaces and backgrounds:** [materials, textures, settings]
- **Overall mood:** [5 adjectives]

## Packaging & product
- **Physical form:** [shape, material, finish]
- **Label and logo placement:** [where branding sits]
- **Distinctive visual features:** [what makes it recognisable]
- **Product system:** [how the range is unified visually]

## Ad formats & creative style
- **Formats:** [feed, Stories, editorial, OOH, …]
- **Text on image:** [how copy is used — typeface, colour, placement, scale]
- **Photo vs illustration:** [what kind]
- **UGC:** [whether creator content appears in paid, and how it's treated]
- **Pricing and offers:** [how price/shipping/discounts are presented — or not]

## Prompt modifier
[One paragraph, 50–75 words, written to OPEN any image-generation prompt. Lock in:
exact hex values, precise lighting direction, colour grade, surfaces/backgrounds,
mood in 3 adjectives, any hard visual rules. This is the single most-used output —
the image model reads it first, so make it specific enough to constrain, not just
describe.]
```

The **prompt modifier** is the most important line in the whole run — draft it
last, after all research, and make it exact.

---

## Step 5 — Write brand-voice.md

Read `references/brand-voice.md`, then write
`./brands/[brand-name]/intelligence/brand-voice.md` — how the brand *writes*,
the copy counterpart to the prompt modifier. Ground every rule in real copy from
the site, product pages, and ad captions (quote it). This is what `/ad-angles`
reads for headlines and ad copy. For
a brand with little copy, note the gap and build from the founder's own words.

---

## Step 6 — Product catalog

The catalog (`products.json` + flat `product-images/`) is the brand's product
index — the source of truth every product-facing skill reads.

### 6a — Choose products

**If a URL was provided**, ask:

> "Which products would you like in your catalog? Paste the direct product page
> URL for each — this grabs exactly the products you choose, with all their
> images. Or say 'best-sellers' and I'll grab the top sellers automatically."

Wait for explicit URLs or explicit "best-sellers" — don't guess or auto-scrape.
A spoken answer ("the performance sleep mask") is explicit enough: match it to
the product on the site, say which one you matched in one line, and continue.
Voice-to-text garbles names; confirm, don't block.

**If no URL**, tell the user the folder is ready and to drop images into
`intelligence/product-images/` named `[slug]-01.jpg`, `[slug]-02.jpg` (lowercase,
hyphens); then run the reindex in 6c.

### 6b — Download

Run the scraper from inside `intelligence/` so images and `products.json` land
correctly. **Preferred — exact product URLs:**
```bash
cd ./brands/[brand-name]/intelligence && python3 ../../../.claude/skills/brand/brand.py --scrape https://brand.com --product-urls "https://brand.com/products/one,https://brand.com/products/two"
```
**Best-sellers:**
```bash
cd ./brands/[brand-name]/intelligence && python3 ../../../.claude/skills/brand/brand.py --scrape https://brand.com
```

This writes flat images `product-images/[slug]-01.jpg …` and a catalog
`products.json`. On Shopify it also captures price, category, and description per
product for free.

**If the scraper is blocked or saves 0 images** (Akamai/Cloudflare, e.g. Nike, or
non-Shopify): the HTML is walled but the image CDN usually isn't.
1. **Browser gallery route (strongest)** — if a Chrome browser is connected: for
   each product URL, `navigate` to it, wait ~3s, run the entire body of
   `.claude/skills/brand/extract-product-gallery.js` via `javascript_tool` (returns
   `{ name, count, image_urls }`). Append `{ name, product_url, image_urls }` for
   each to `products-to-ingest.json` in `intelligence/`.
2. **WebFetch route** — WebFetch each product page, extract name + all image URLs,
   write the same `products-to-ingest.json`.
3. Download via the open CDN, then delete the temp file:
   ```bash
   cd ./brands/[brand-name]/intelligence && python3 ../../../.claude/skills/brand/brand.py --ingest-file products-to-ingest.json
   ```

Don't loop on a wall that won't budge — escalate to the next tier, then manual.

### 6c — Reindex from disk (manual drops)

After the user drops images in by hand — or to reconcile the catalog with what's
actually on disk — rebuild `products.json` (preserving any enrichment already
recorded):
```bash
cd ./brands/[brand-name]/intelligence && python3 ../../../.claude/skills/brand/brand.py --index
```

### 6d — Enrich the catalog

For each product, fill the catalog's `category`, `description`, and `claims`
(short factual selling points used to ground ad copy) by reading its product page
where available. Write them into the matching `products.json` entry. These survive
future re-scrapes and `--index` runs.

Present the result:
```
Catalog: [N] products, [M] images.
  • camp-shirt        — 4 images
  • slim-chino-black  — 6 images
  …
```

### 6e — Avatars and offers

The two files everything commercial reads. They come last in the research chain
because both depend on the catalog: offers need real prices and SKUs, avatars
need to know what's actually sold.

Read `references/avatars.md`, then write
`./brands/[brand-name]/intelligence/avatars.md` — three to five named people,
each with a concrete vignette, **verbatim pain words**, wants, objections with
their rebuttals, an emotional driver, and the page point of view that suits them.
Draw the language from reviews, ad-library comments, and the brand's own segment
copy. Avatars are distinct on *why they buy*, never on demographics alone.

**Ask for the customer's own words before you write the avatars.** One message,
plain language:

> "Two things that make the ads far better. First: what are the five to ten
> things your customers complain about or want most, in the words they actually
> use? Talk it out, voice-to-text is perfect, messy is fine. Second: if you have
> call transcripts, a review export, support tickets or DMs, drop them in and
> I'll pull the exact phrases."

Archive anything they drop under `context-uploads/` (Incremental mode, Step A)
and mine it: quote lines verbatim, note where each came from, and count how many
different people said the same thing. A pain three customers named outranks one
the founder guessed. In `avatars.md`, tag each pain word with its source
(`review`, `call`, `founder`, `inferred`), and where the founder's list and the
mined language overlap, say so: that overlap is the strongest angle the brand
has. If they have nothing to share, write from the public reviews, and mark the
gap rather than presenting a guess as a finding.

Then read `references/offers.md` and write
`./brands/[brand-name]/intelligence/offers.md` — the closed list of offers any
page may use, with IDs (`O1`, `O2`, …), stacking rules, and a selection heuristic
mapping the avatar names above to a primary offer. Source every price, code, term
and guarantee from the catalog, the live storefront, or the user directly.

**The default CTA must pass the stranger test.** Someone who has never seen the
site has to know what happens when they tap. Write it in plain words ("Start the
course", "See the course", "Join the course") and record the site's own phrase
beside it as an alternate. A brand phrase ("Build my AI Operating System") is
positioning, not a button.

**Named people need permission on record.** For every customer, member or case
study the research names as proof, record whether the brand has permission to
use the name in paid ads, or `permission: unknown`. `/ad-angles` holds back any
name marked unknown until the person answers.

**Never invent an offer, a price, a code, or a guarantee.** Where the research is
ambiguous — a bundle exists but its price isn't visible, a guarantee is implied
but never stated — ask the user rather than filling the gap. Everything
downstream treats this file as a promise the brand will honour. A brand with one
product and free shipping has a two-offer library, and that is a complete answer.

---

## Step 7 — Write brand-context.md (portable capsule)

Read `references/brand-context.md`, then write the one-page
`./brands/[brand-name]/intelligence/brand-context.md` — a self-contained ~1-page
export distilling strategy, positioning, voice, palette, type, the prompt
modifier (verbatim), and a compact product list. It's designed to paste into any
external AI tool for instant on-brand output. Regenerate it whenever the brand
context changes.

---

## Step 8 — Report back

Give the user:

1. **Brand name** and intake mode used
2. **Positioning** — the recommended counter-position + value proposition
3. **Colour palette** — the accent/neutral colours read into `color-palette.json`;
   note it's a best-effort first pass to edit, and flag any uncertain colour
4. **Typography** — heading + body fonts, their source, which open-license fonts
   were auto-downloaded, which licensed faces the user must drop in, and any
   design system found. Say in one line that the build step proves the fonts in
   Paper before the first ad, so there is nothing for them to verify now.
5. **Logo** — whether it was found automatically (and from where — JSON-LD,
   header, or favicon-only) or still needs a manual drop into `logos/`
6. **Catalog** — number of products and images indexed (or note manual)
7. **Avatars and offers** — how many of each, named; flag any offer field you had
   to ask about or leave open, and any avatar resting on inference rather than
   real customer language
8. **Setup** — the brand type, the image tool, the advertiser and the landing
   link on file, in one line
9. **Carried-over learnings** — if you seeded `learnings.md` from the person's
   earlier verdicts (an older tool's rules file, a notes doc), list them as one
   block with a count and ask for one yes before they bind. Until then they are
   marked `proposed`.

Keep it to two or three sentences plus a short list — what now exists, then what
the user does next:

- **References.** Look first, then ask. If the person pointed you at a folder
  of their own material, check it for reference ads before asking anything, and
  say what you found (*"I found six ads in your references folder. Want me to
  use those, add more, or pull what your category is running?"*). Only when
  nothing is on hand ask plainly: *"Do you already have ads you'd like to
  model? Drop them into `generation/paper-ads/ad-references/`. If you don't,
  run `/ad-scout` and I'll pull what's running in your category so you can
  pick."* Never run the research unasked; someone with references they love
  does not need it.
- **`/ad-angles`** — turns the avatars, offers and references into four to five
  angles with two variants each, the copy for every one, and the Meta ad text.
- **`/paper-ads`** — builds them in Paper, laid out by angle, in 4:5 and
  9:16, with every word editable.
- Add more products, images or facts any time with "add this to my brand
  context".
- Verify the fonts, and drop a logo into `logos/` if one is still missing.

---

## Incremental mode — "add this to my brand context"

When the user wants to fold something into an **existing** brand (they name a
brand under `brands/`, or say "add this to my brand context / catalog"), do NOT
rerun full setup. Confirm which brand if ambiguous, then work in this order:
**archive the raw drop → refine the affected doc(s) → regenerate the capsule.**

### Step A — Archive the raw context first

Before you change anything, preserve exactly what the user gave you in
`intelligence/context-uploads/`, so the brand keeps a trail of everything it was
built from. This runs *alongside* the refinement below — it never replaces it.

- **A dropped file** (guidelines PDF, positioning deck, style guide, brand
  document, screenshot, line sheet — anything with no dedicated home of its own).
  From the brand's `intelligence/`:
  ```bash
  cd ./brands/[brand-name]/intelligence && python3 ../../../.claude/skills/brand/brand.py --save-context "[path-to-file]" --move
  ```
  Use `--move` for a throwaway chat upload under `uploads/` (its permanent home
  is now `context-uploads/`); drop `--move` to copy a file the user keeps
  elsewhere. Comma-separate several paths; add `--as "[name]"` to name them.
- **A pasted fact or a verbal correction** (no source file). Write it straight to
  `context-uploads/[YYYY-MM-DD]-[slug].md` with the Write tool — a short note
  capturing what the user said, dated, in their words.
- **A product, logo, or font already lands in its own dedicated home**
  (`product-images/`, `logos/`, `fonts/`) — that folder *is* its archive, so do
  **not** also duplicate the asset into `context-uploads/`. A *document about*
  products (a catalogue PDF, a line sheet) is context — archive that.

### Step B — Refine the affected doc(s)

Then act only on the new item and update the file(s) it belongs to:

- **A product (URL):** run `brand.py --scrape [site] --product-urls "[url]"` from
  the brand's `intelligence/` — it appends to the flat `product-images/` and
  merges into `products.json` without touching existing products. Then enrich the
  new entry (6d).
- **A product (dropped images):** confirm they're named `[slug]-01.jpg …`, then
  `brand.py --index` to fold them into the catalog; enrich the entry.
- **A product (image URLs from a walled site):** use the ingest path (6b).
- **A logo:** if the user drops a file, confirm it's in `logos/`. If they ask
  you to pull it from the site instead, run `brand.py --fetch-logo [url]`
  (browser + manual fallback as in Step 2c) and report what was saved.
- **A font file:** confirm it's in `fonts/`; for a named Google font,
  `brand.py --fetch-fonts "[Family]"`; update `typography.json` if it's a new
  brand face.
- **A brand fact / document / correction:** update the specific file it belongs
  to — `brand-strategy.md`, `counter-positioning.md`, `visual-guidelines.md`,
  `brand-voice.md`, `color-palette.json`, or `typography.json` — and nothing else.

### Step C — Regenerate the capsule

**After any incremental change, regenerate `brand-context.md`** so the portable
capsule stays current, then give a one-line summary of what changed — including
where the raw drop was archived. Never overwrite unrelated files.

---

## Notes

- Slug the brand folder name: lowercase, hyphens, no spaces (`satisfy-running`,
  `glossier`). Use the name as it appears on the site/docs.
- Follow redirects to the final URL; if a page fails, note it and continue.
- Hexes and font names matter — don't approximate; if you can't find exact values,
  say so rather than guess.
- The **prompt modifier** (visual-guidelines.md) and **brand-voice.md** are the two
  highest-leverage outputs — one governs every image, the other every line of copy.
- Keep every `.md` clean: tidy headings, one idea per block, proper spacing.
- Product images are always **flat** in `product-images/` (`[slug]-01.jpg`) — never
  per-product subfolders, or the catalog won't group them.
