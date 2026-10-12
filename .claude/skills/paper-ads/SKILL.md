---
name: paper-ads
description: "Remake ads you like for your brand, fully editable in Paper. Drop in one or more reference ads (screenshots are fine); for each one it keeps what makes the ad work (the format and the hook), rewrites every word for the brand from its real facts and offers, wireframes it in Paper, generates only the text-free photo (Paper's own image generation by default, or Higgsfield or fal if the brand switched), places every word as an editable layer, in 4:5 and 9:16, and measures it with a preflight script before anything is called done. Then takes feedback in plain words."
image_model: Paper image generation (default), Higgsfield Nano Banana Pro, or fal GPT Image 2.5 Sunburst
group: Ads
summary: Drop in ads you like; it remakes each one for your brand in Paper, every word editable, in 4:5 and 9:16, measured before delivery
version: 4.0.0
outputs: [paper-ads]
inboxes:
  paper-ads/ad-references: Ad references
requires: [Paper]
optional: [Higgsfield connector or FAL_KEY only if the brand switched image tools, intelligence/fonts/*.ttf for the brand's real typefaces]
---

# Remake ads you like, built in Paper

> **Where brands live.** A brand's folder is `04-Brand/clients/<brand>/` when the
> project has a `04-Brand/clients/` folder, otherwise `brands/<brand>/`. Every
> `brands/<brand>/` path in this file means that folder. Read
> `.claude/skills/paper-ads-prep/references/system.md` once per session: it holds the
> rules every skill in this system follows.


The person brings ads they like. This skill remakes each one for their brand:
same format, same idea, their product, their words, their look. One finished
ad per reference, in both sizes, every word editable.

An ad here is two independent parts: a **text-free photographic plate** and an
**editable layout** on top of it. The image model never draws a word. Every
headline, badge, rating, button and legal line is its own layer in Paper, so a
copy change, a new variant or a translation costs nothing. Only a new photograph
costs money.

Paper is not optional. The Paper file is the deliverable; the flat PNGs are
exports of it. If Paper is connected but no file is open, create or open the brand's file
yourself (see `references/paper-canvas.md`) and carry on. If the Paper connector
is not reachable at all, stop and say so in one friendly line (*"Open Paper
Desktop, then say go"*). Do not fall back to
a flat render and call it done.

**Nothing is called finished until `preflight.js` says so.** The script reads
every artboard straight out of Paper and fails the ones with overlaps, clipped
text, dead crops, type under the floor, text outside the safe zones, and a
button in the platform rail. Your eyes are for what the script cannot see: a
head cut off, a figure that blends into the ground, a line that reads wrong.

Create this skill's declared inbox and output folders before use.

## Non-negotiables

- Every ad is delivered as two independently composed variants: **4:5**
  (1080×1350) and **9:16** (1080×1920). Never crop one finished design into the
  other.
- All claims, offers and product facts come from `brands/<brand>/intelligence/`.
  Offers come from `offers.md` by ID. Nothing is inferred from a reference ad.
- **Keep the reference's idea, rewrite every word.** A reference works because
  of its format *and* its hook ("We got caught: someone on our team posted our
  best deal"). Keep both: the same layout and the same idea, retold for this
  brand in its own voice. Never use the other brand's name, product, claims,
  people or likeness, and never copy its distinctive lines word for word.
- Before any paid call, state the exact plates, the call count, the cost, and
  the maximum cost including one quality retry per failed plate. Get an explicit
  yes. This holds for Higgsfield credits exactly as it does for fal dollars.
- Each failed plate may use one pre-authorised retry. If that fails too, show the
  better source and ask before spending again.
- Never generate to improve a layout. Layout iteration is free and happens in
  Paper.
- **A plate is never patched, tiled, feathered, extended or boxed, in Paper or
  in a script.** The only way a plate grows is a model re-render or a model
  outpaint, quoted and approved like any other plate.
- **Every plate the person will see copy on is approved by the person first,
  retries included.** A retry does not inherit the approval of the plate it
  replaces.
- **If the model that served is not the model requested, stop before the next
  paid call and say so.** The person decides whether to keep paying for the
  substitute, switch models, or stop.
- **A judgement is a measurement or it is not reported.** "About 20px" from a
  downscaled screenshot is not a measurement. Product position comes from
  `product-bbox.py`; text position comes from `preflight.js`.
- No em dashes in any line a customer reads.
- **Never write to `offers.md` or any `spec.json` beyond the ad you are
  building, and never add an ad, a version or a file the person did not ask
  for, without saying so in the same message.** A note like "try a couple of
  versions" is a request to propose, not to build.
- **Never say "nothing failed" or "fonts rendered correctly" unless you are
  quoting a measurement.** Paste the preflight summary line. If a check was not
  run, say it was not run.

## 0. Read the setup

Read `intelligence/setup.json` (written by `/paper-ads-prep`): `brand_type`
(`product` or `service`), `image_tool` (`paper` by default; `higgsfield` or
`fal` only if the person switched), `image_model`, and `paper_file_id` if one
exists. No file: work out `brand_type` from the brand files, use Paper for
photos, and write it. Then read `intelligence/learnings.md` if it exists; its
Rules are hard constraints and its Defaults are strong preferences. Read
`intelligence/preflight.json` if it exists; it holds the brand's own type
minimums and empty-band limits, and the preflight script enforces them. Read
`brand-voice.md`, `avatars.md`, `counter-positioning.md`, `offers.md` and
`products.json`: they are where every word and every fact comes from.

Check the tools the run needs, kindly and without warning language:
- **Paper:** open `paper_file_id`; with no file yet, create the brand's file
  and open it, without asking. No connection at all: stop, in one friendly line.
- **Paper image generation** (the default): nothing to check beyond Paper itself.
  Mention the plan's weekly limit once if the batch is large.
- **Higgsfield** (only if switched): one balance call. State the credits available.
- **fal** (only if switched): `FAL_KEY` present in `.env`.

## 1. Gather the references

The references are the ads the person wants remade: files in
`generation/paper-ads/ad-references/`, or images pasted into the chat (save
those into that folder first). Each reference becomes one ad, numbered in
order: `r1`, `r2`, `r3`. Extra versions of one, only when asked, are `r1-v2`,
`r1-v3`.

**References from `/competitor-ads-intel`:** when the person picked ads from
the competitor pages in Paper, those picks are already in `ad-references/`
(named `<competitor>-<NN>.jpg`). Remake exactly those.

**No references yet:** don't go looking for ads yourself. Picking ads worth
copying takes the person's taste. Say, warmly:

> "First let's find some ads worth remaking. Run `/competitor-ads-intel` and
> I'll put every image ad your competitors are running into Paper so you can
> pick. Or, if you've already seen ads you love from any brand, paste
> screenshots in here."

**Batch size.** Build up to five references at a time (ten artboards). With
more, build the first five, take the person's notes, then do the next five.

Each ad lives in its own folder: `generation/paper-ads/<YYYY-MM-DD>/<id>/`
(for example `2026-10-11/r2/`). All scripts take that folder as their argument.

## 1b. Write the words

For each reference, work out in one line **why it works**: the format (a
notes screenshot, a before-and-after, a big stat, a review card) and the hook
(the idea that stops the scroll). Then write this brand's version of every line
on it:

- Same idea, same structure, same rough length per line. If the reference says
  "We got caught", this brand's ad gets caught too, in its own words.
- In the brand's voice from `brand-voice.md`, aimed at the avatar in
  `avatars.md` the reference's idea fits best, using that person's own pain
  words where a line calls for them. Name the avatar in `spec.json`.
- Every fact, number, price and claim from `products.json` or `offers.md`.
  Nothing invented, nothing borrowed from the reference. If the reference
  leans on a fact this brand doesn't have (a review count, a discount), use a
  true one it does have, or drop that line and say so.
- If the reference's idea can't be told truthfully for this brand, say so and
  suggest a close one that can.

Record the words in the ad's `spec.json`. Show them with the wireframes in step
4, so the person can change any line before anything is spent.

## 2. Read the reference and choose a route

Inspect the reference and record its format-defining primitives: image
treatment, search modules, ratings, testimonial cards, comparison states, labels,
badges, rules, buttons and proof. Every primitive is `photographic`, `editable`,
or an intentional documented omission. Do not replace a recognisable format
device with generic copy.

Pick one of three routes:

- **layout-first** for three or more text groups, offers, comparisons,
  statistics, annotated images or precise editorial hierarchy. Build the complete
  editable wireframe first; photography only fills named image zones. Decide
  before generation whether each image zone is a deliberate panel or a seamless
  bleed, and keep that treatment through the run.
- **plate-first** only for a simple image-led composition with one short
  headline and generous, unambiguous copy space.
- **layout-only** when the reference itself has no photograph in it, or when the
  photograph is one the brand already owns: pure type on a brand ground, a
  testimonial card, a comparison table, a notes screenshot, a real screenshot, a
  real photo of the founder. Nothing is generated and nothing is spent. **Real
  photos are not desaturated.** They are the brand's, and they stay as shot.

**The reference decides the route, not the brand type.** A service, course or
software brand has no pack shot, but if the reference is built on a photograph
and the brand owns none that fits, generate a base photo for it: the customer's
world, the moment the problem bites, the outcome, a setting, a texture. It is
never a product shot and needs no size reference. Only skip the photograph when
the reference has none.

**Check the reference against the Rules before building.** A reference whose
format needs something `learnings.md` forbids (a dark ground for a brand that
never runs dark, a generated face for a brand that never shows one) is the wrong
reference for this brand. Say so kindly and suggest swapping it.

## 3. Specify the system

Write `spec.json` in the ad's folder before generating. It contains the ad id,
the reference, why it works, the product inputs, the words from step 1b, both
delivery variants, image zones, the plate prompt,
format primitives, route, and the photos used with their crop values.

**Product plates** need two references:

1. an isolated, exact packshot for shape, finish and label; and
2. the same product held in a hand or shown against or on a body, for scale.

Record these as `product_images` and `product_scale_reference`. The format
reference may be the scale reference only if it visibly shows the exact product.
Otherwise use a brand-owned scale asset or ask for one. Never substitute another
SKU or a generic hand reference.

**Plates with no product in them** (a service brand's proxy scene, a setting, a
texture) leave both fields out. The plate prompt then describes the scene from
`visual-guidelines.md` and the customer's world, never a real person's likeness
and never a generated screen or dashboard.

**Real photos.** One photo per ad, unless the person approved the reuse.
Read each file's real orientation (EXIF rotation changes the width and height
that a quick listing reports) before any crop maths. Record the file, the crop
and the reason in `spec.json`.

For any visual role repeated at least twice (labels, callouts, statistics,
cards, search rows, comparison cells, offers or CTAs) add a `repeated_systems`
entry. Define the shared type, container, padding, stroke, radius, fill,
baseline or alignment edge, and the permitted reference-derived variations.
Connector systems also define the common rule, endpoint and anchor treatment.
Composition may be asymmetric; repeated components may not vary arbitrarily.

For annotation formats, also record the annotation subject, supported labels and
the visual anchor for each label. Labels must answer the same product question;
do not mix ingredients with founder facts, serving counts, offers or unrelated
claims.

## 4. Build the wireframe in Paper, before photography

Read `references/paper-canvas.md` first. It holds the canvas layout (one row
per reference), the artboard naming, the font preflight, how a photo is cropped in Paper, and the
Paper quirks that cost time.

Make one wireframe artboard per ratio using the real copy and component systems,
placed in its reference's row. It must work with images hidden: hierarchy, lanes, UI,
proof and CTA remain clear and editable. Build one correct repeated component and
duplicate it; vary content and placement, not type, padding, box size or line
style unless the reference specifically calls for it.

Review repeated components side by side. Equal roles share their declared system
and align to intentional lanes or anchors, not convenient empty pixels. For
leader lines, use short, non-crossing routes to distinct anchors. Keep labels,
leaders and containers clear of faces, product labels and critical copy.

**Run the preflight on the wireframes** (step 8 explains the command). It
catches zone, overlap and type-size problems before a photo exists, when they
are cheapest to fix. Then screenshot each wireframe at scale 1 and save it in
the ad's folder as `<id>-wireframe-<ratio>.png`. A run with no wireframe
screenshots on disk skipped this step.

Wireframe the whole batch before the cost gate, then show the wireframes and
each ad's words together with one cost number. The person can change any line
or swap a reference before a cent is spent.

## 5. Generate only the photography

Skip this section for the layout-only route.

State the cost and get a yes (Non-negotiables). Then, once per ratio per ad:

**Generate the 4:5 first, approve it, then derive the 9:16 from it.** Fresh
9:16 generations fail far more often than 4:5 ones (Dream Recovery: 4:5 passed
first time five of five, 9:16 one of four, and every retry credit went to 9:16).
So the 9:16 is built by geometry, not by prompt:

1. `product-bbox.py <ad-folder> --variant feed_4x5` records where the
   product sits in the approved 4:5 (auto on a plain ground, `--bbox` on a scene).
2. `extend-plate.py <ad-folder>` scales and places that 4:5 inside a
   1080×1920 canvas so the product lands inside the product stage and clear of
   the rail, and writes the canvas, a mask, and the 9:16 product box into
   `spec.json`. The geometry is checked before any credit is spent.
3. The model fills only the empty areas (`references/higgsfield.md`, "Deriving
   the 9:16"), quoted and approved like any plate. Feed and Stories then show
   the same approved photograph.

Only when the 4:5 composition cannot be extended (a tight crop with no room, a
scene whose edges are not continuable) is a 9:16 generated fresh, with the
product's position stated as pixel bounds in the prompt, and `product-bbox.py`
run on the result before copy goes on.

- **`image_tool: higgsfield`**: follow `references/higgsfield.md`. Claude calls
  the Higgsfield connector with the packshot, the scale reference and (when used)
  the format reference as image references, then files the result with
  `save-plate.py`, which crops to ratio where needed, resizes to delivery size
  and applies the house desaturation. After two misses on a plate, or whenever a
  person is prominent in frame, the model switches as the reference says; that
  is a rule, not a suggestion.
- **`image_tool: paper`**: follow `references/paper-images.md`. Paper
  generates the plate inside the artboard's image zone, so there is no file to
  upload; the result is downloaded with Paper's fill-image tool, desaturated and
  filed with `save-plate.py`, then placed back as the zone's background like any
  plate. Its usage counts against the person's weekly Paper limit; say how many
  generations the block needs before starting.
- **`image_tool: fal`**: run `generate-blank-ad.py <ad-folder> --variant
  feed_4x5`; for the 9:16, run `extend-plate.py` and pass the canvas as the
  edit source so the model fills the empty areas.

Either way the prompt opens with the brand's prompt modifier from
`visual-guidelines.md`, names the exact image zone, crop, product and scale
references and required clear space, and asks for no ad copy, UI, rules, dots,
labels or placeholder text. Printed packaging is the only permitted text. End
every prompt with: "Absolutely no typography anywhere except the printed product
packaging."

If the reference includes a person, preserve composition, pose, crop and
lighting, but prompt a different face, hair and styling. Check `learnings.md`
first: a brand that never shows a generated person gets a scene instead.

Every **generated** plate is desaturated by 10% before review and delivery,
consistently across the whole plate. Both scripts do this. Real photos are left
alone.

## 6. Source QA and approval gate

Inspect each generated plate before any overlay work. Reject a plate that has
invented letters, an incorrect, mirrored, rotated or cropped pack, a wrong label
orientation, implausible physical scale, or a lookalike of the reference subject.
Compare pack scale to the hand or body reference, not just to empty space.

Measure visible bounds, not frame bounds. Reconcile text and image zones against
the actual plate. A failed crop or insufficient copy space uses the one permitted
retry, not shrunken type or a Paper patch.

Show the selected 4:5 and 9:16 plates with their product bounds (from
`product-bbox.py`, never estimated by eye) and safe-zone results. Do not place
copy on a plate until the person approves it, and that includes every retry. Show
all plates of the batch together and take one approval, noting
any they reject. A held plate is reported the moment it is held, with the
measured reason, not in the final report.

### Delivery safety

Full detail in `references/mobile-delivery.md`.

- 4:5 critical-content zone: x54 to 1026, y54 to 1296.
- 9:16 critical-content zone: x90 to 990, y250 to 1570.
- In 9:16, reserve x840 to 1080, y560 to 1500 for platform controls. Keep the
  product, wordmark, CTA, proof and required labels out of it. The product or
  use moment belongs in x120 to 810, y430 to 1350.
- Minimum type at 1080px wide: headline 88px; statistic 96px; CTA or price 34px;
  subhead or proof 30px; label 28px; legal 20px. These are floors. The brand's
  own minimums in `preflight.json` sit above them and win.
- The band below the live zone is not a void. The photo, the figure, the ground
  or the wordmark reaches the edge; a flat empty strip under a type-led ad is a
  failure the preflight reports.

Never fix a 9:16 safe-zone failure by tiling, extending, offsetting or boxing a
finished plate in Paper. Re-render the source with approval; Paper may only crop
inside an already seamless approved image zone.

## 7. Compose the editable ad in Paper

Place each approved plate or real photo into its wireframe's image zone, as the
frame's background image beneath everything. **Crop with `backgroundPosition`.**
Paper keeps `objectPosition` on a frame but ignores it, so a crop written that
way never happens; the preflight fails any photo frame that carries it.

The wireframe becomes the ad: every text, UI, proof, rule, button and legal
element stays its own named layer. Name layers by role (`headline`, `subhead`,
`cta`, `rating`, `legal`, `badge-1`) so a later revise can change one layer's
text instead of rebuilding the artboard, and so the preflight knows which floor
applies to which line.

Write one visual group per call and **one write at a time**. Parallel replace
writes have returned success and changed nothing. After any disconnect, read
back every write that was in flight before trusting it. Screenshots can lag one
write behind; take a cheap read first, then the screenshot.

Fonts: follow the preflight in `references/paper-canvas.md` and prove the face
by computed style and screenshot before the first wireframe. If Paper cannot
draw the brand face, the order is fixed: first the stand-in `typography.json`
names, then, only if that is unavailable too, the closest face Paper has, and
in both cases the person is told in one line and `typography.json` is updated
to say what was used. Never a third font nobody chose. Run `compose-text.py` on
the ad to produce the embedded-font SVG as the exact visual reference
whenever the brand face itself did not render; when it did, the script is
optional.

## 8. Final preflight: the script, then your eyes

Run the preflight on every artboard of the batch, from the project root:

```bash
node .claude/skills/paper-ads/preflight.js --file <paper_file_id> --only r1,r2 --campaign brands/<brand>/generation/paper-ads/<YYYY-MM-DD> --config brands/<brand>/intelligence/preflight.json --out brands/<brand>/generation/paper-ads/<YYYY-MM-DD>/preflight.json
```

`--campaign` lets it read each variant's product box from `spec.json`, so text
sitting on the product and a product entering the 9:16 rail are measured even
though the product is baked into the plate. Run `product-bbox.py` on every
plate first; a ground plate with no product box is reported as a warning.

It reads positions, sizes, text and computed styles straight from Paper and
prints PASS, WARN or FAIL per artboard with the reason. Zero FAILs is the bar.
Every WARN is either fixed or answered in one line in the delivery note. Then
look, at scale 1, never smaller, for the things it cannot measure:

- a head, hands or product cut by the frame edge, or sitting too close to it;
- a cutout that blends into the ground instead of standing off it;
- repeated components that read as one deliberate system;
- the image treatment intentionally seamless or intentionally panelled;
- the 9:16 read at phone scale with the UI chrome imagined on top;
- every fact and claim on the artboard traceable to `products.json` or `offers.md`;
- the format's own primitives present and editable;
- no em dash anywhere;
- the pair in its reference's row, 4:5 then 9:16, named per the canvas spec;
- no two ads in the batch read as the same ad (same packshot, same ground, same
  stack); if two references would come out alike, vary the photo on one;
- a notes, chat or phone format carries no device chrome (status bar, clock,
  battery) that would make a written note read as a real screenshot.

Correct any failure in Paper, re-run the script, and only then call the block
done. **Never present an ad that fails.** Hold it back and say which one and
why. Paste the script's summary line in the delivery note.

## 9. Deliver

Export each artboard from Paper at **scale 1**, no more than six artboards per
export call, and verify every file is 1080 wide before moving on; Paper's default
scale has changed mid-run and produced 2160-wide files. Move the files out of
Downloads into the ad's folder as `<id>-<ratio>.png`.

Then report, short and plain:

- where the ads are in Paper (one row per reference);
- per ad: which reference it remade and the one line on why that reference works;
- the preflight summary line, and any WARN you left, with why;
- what was spent, against what was quoted;
- anything held back, and any font stand-in.

Close with what they can do next: click any word in Paper and change it for
free, or just tell you what they like and don't, in plain words. Voice-to-text
is perfect.

## 10. Feedback, and what the brand learns

The person reacts in their own words: "love r2", "r1's headline is too long",
"r3 is too dark", "make another version of r2 with a different headline".
Handle it without making them use any special phrasing:

- **A words note:** rewrite the line (same rules as step 1b) and update that one
  layer in Paper. Free.
- **A layout note:** fix it in Paper. Free. A note that applies to every ad
  ("make the buttons bigger") is applied to every ad.
- **A photo note:** only this costs money. Quote it and get a yes first.
- **"Another version":** propose what would change in one line, and build it as
  `r2-v2` only on a yes.
- **Love it:** mark it `approved` in its `spec.json`.
- **Don't like it, with a reason:** fix it or drop it, and **remember the
  reason** in `intelligence/learnings.md` so the next batch doesn't repeat it.
  An objective problem (wrong pack, an unsupported claim) goes under
  `## Rules`, permanent; a matter of taste ("too dark") under `## Defaults`.
  Quote their words and date the line. Tell them in one line: "Got it, I'll
  remember that for next time."
- **A Default with a number in it becomes a check.** "Subheads at least 42px"
  goes into `intelligence/preflight.json` as `"min_px": {"subhead": 42}`; "no
  empty band under 9:16 ads" lowers `"max_empty_bottom"`. The next run fails on
  it instead of hoping.

This skill reads `learnings.md` and `preflight.json` at the start of every run.
Those two files are how the second batch is better than the first.
