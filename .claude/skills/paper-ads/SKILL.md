---
name: paper-ads
description: "Build the ads in Paper: for every angle and variant from /ad-angles, wireframe the reference format with the real copy, generate only the text-free photographic plate (Higgsfield or fal, whichever the brand chose), then place fully editable text and UI on it, in 4:5 and 9:16, laid out on the Paper canvas by angle, and measured by a preflight script before anything is called done. Also runs on a single reference with no campaign."
image_model: Higgsfield Nano Banana Pro, or fal GPT Image 2.5 Sunburst
group: Ads
summary: Builds every ad in Paper as an editable layout over a text-free photo, in 4:5 and 9:16, arranged by angle, measured before delivery
version: 3.1.0
outputs: [paper-ads]
inboxes:
  paper-ads/ad-references: Ad references
requires: [Paper]
optional: [Higgsfield connector or FAL_KEY for photographic plates, intelligence/fonts/*.ttf for the brand's real typefaces]
---

# Static ads, built in Paper

An ad here is two independent parts: a **text-free photographic plate** and an
**editable layout** on top of it. The image model never draws a word. Every
headline, badge, rating, button and legal line is its own layer in Paper, so a
copy change, a new variant or a translation costs nothing. Only a new photograph
costs money.

Paper is not optional. The Paper file is the deliverable; the flat PNGs are
exports of it. If the Paper connector is not reachable, stop and say so in one
line (*"Open Paper Desktop with a file open, then say go"*). Do not fall back to
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
- Reference ads contribute format and structure only: never another brand's
  copy, product, or likeness.
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
- **Never write to `offers.md`, `copy.md`, `angles.md` or any `spec.json` beyond
  the concept you are building, and never add a concept, a variant or a file
  the person did not ask for, without saying so in the same message.** A note
  like "try a couple of variants" is a request to propose, not to build.
- **Never say "nothing failed" or "fonts rendered correctly" unless you are
  quoting a measurement.** Paste the preflight summary line. If a check was not
  run, say it was not run.

## 0. Read the setup

Read `intelligence/setup.json` (written by `/brand`): `brand_type`
(`product` or `service`), `image_tool` (`paper`, `higgsfield` or `fal`), `image_model`,
`advertiser` and `landing_url`, and `paper_file_id` if one exists. Missing file:
ask the setup questions from `/brand` Step 0b and write it. Then read
`intelligence/learnings.md` if it exists; its Rules are hard constraints and its
Defaults are strong preferences. Read `intelligence/preflight.json` if it
exists; it holds the brand's own type minimums and empty-band limits, and the
preflight script enforces them.

Check the tools the run needs, and say what is missing in plain words:
- **Paper:** list files or open `paper_file_id`. No connection: stop.
- **Paper image generation** (if chosen): nothing to check beyond Paper itself.
  Mention the plan's weekly limit once if the batch is large.
- **Higgsfield** (if chosen): one balance call. State the credits available.
- **fal** (if chosen): `FAL_KEY` present in `.env`.

## 1. Decide what is being built

**Campaign mode (the default).** `/ad-angles` has written
`generation/ad-angles/<campaign>/` with `angles.md`, `copy.md` and `ad-unit.json`.
Every variant in `copy.md` names its angle, its reference format, and its copy,
slot by slot. Build exactly those. Do not rewrite the copy here; a copy problem
goes back through `/ad-angles --rewrite`.

**Single mode.** The person dropped one reference and wants one ad, no campaign.
Write the copy yourself by the `/ad-angles` method (their pain in their words
from `avatars.md`, an offer by ID, a claims ledger), record it in the concept's
`spec.json`, and treat it as angle `a1`, variant `v1`.

No references in `ad-references/` and no campaign: say so and offer the two ways
forward. *"Drop in a few ads you'd like to model, or run /ad-scout and I'll pull
what's running in your category."*

Each concept lives in its own folder:
`generation/paper-ads/<campaign>/<angle>-<variant>/` (for example
`autumn-launch/a2-v1/`). All scripts take that folder as their argument.

**Batch size.** A campaign of five angles by two variants is twenty artboards,
and that is the most one review pass can hold. If the campaign is bigger, build
and present it in blocks of two or three angles, run the preflight on each
block, and get the person's notes on a block before building the next. Do not
build forty artboards and then review them at a third of their size.

## 2. Read the reference and choose a route

Inspect the concept's reference and record its format-defining primitives: image
treatment, search modules, ratings, testimonial cards, comparison states, labels,
badges, rules, buttons and proof. Every primitive is `photographic`, `editable`,
or an intentional documented omission. Do not replace a recognisable format
device with generic campaign copy.

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
reference for this brand. Say so and pick another; `/ad-angles` should have
caught it, and the build must not let it through.

## 3. Specify the system

Write `spec.json` in the concept folder before generating. It contains the
angle and variant ids, the reference and product inputs, the supported copy
(copied from `copy.md`), both delivery variants, image zones, the plate prompt,
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
`visual-guidelines.md` and the avatar's world, never a real person's likeness
and never a generated screen or dashboard.

**Real photos.** One photo per angle, unless the person approved the reuse.
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

Read `references/paper-canvas.md` first. It holds the by-angle canvas layout, the
artboard naming, the font preflight, how a photo is cropped in Paper, and the
Paper quirks that cost time.

Make one wireframe artboard per ratio using the real copy and component systems,
placed in its angle's row. It must work with images hidden: hierarchy, lanes, UI,
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
the concept folder as `<id>-wireframe-<ratio>.png`. A run with no wireframe
screenshots on disk skipped this step.

When a campaign has several concepts, wireframe the block before the cost gate,
so the person approves one number for the block and sees the layouts first.

## 5. Generate only the photography

Skip this section for the layout-only route.

State the cost and get a yes (Non-negotiables). Then, once per ratio per concept:

**Generate the 4:5 first, approve it, then derive the 9:16 from it.** Fresh
9:16 generations fail far more often than 4:5 ones (Dream Recovery: 4:5 passed
first time five of five, 9:16 one of four, and every retry credit went to 9:16).
So the 9:16 is built by geometry, not by prompt:

1. `product-bbox.py <concept-folder> --variant feed_4x5` records where the
   product sits in the approved 4:5 (auto on a plain ground, `--bbox` on a scene).
2. `extend-plate.py <concept-folder>` scales and places that 4:5 inside a
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
- **`image_tool: fal`**: run `generate-blank-ad.py <concept-folder> --variant
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
copy on a plate until the person approves it, and that includes every retry. In
a campaign, show all plates of the block together and take one approval, noting
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
the concept to produce the embedded-font SVG as the exact visual reference
whenever the brand face itself did not render; when it did, the script is
optional.

## 8. Final preflight: the script, then your eyes

Run the preflight on every artboard of the block, from the project root:

```bash
node .claude/skills/paper-ads/preflight.js --file <paper_file_id> --only a1-v1,a1-v2 --campaign brands/<brand>/generation/paper-ads/<campaign> --config brands/<brand>/intelligence/preflight.json --out brands/<brand>/generation/paper-ads/<campaign>/preflight.json
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
- every claim on the artboard present in the concept's claims ledger;
- the format's own primitives present and editable;
- no em dash anywhere;
- the pair in its angle's row, 4:5 then 9:16, named per the canvas spec;
- no two concepts in the campaign read as the same ad (same packshot, same
  ground, same stack). Two angles that look alike muddy both tests; change the
  photo or the format on one of them;
- a notes, chat or phone format carries no device chrome (status bar, clock,
  battery) that would make a written note read as a real screenshot.

Correct any failure in Paper, re-run the script, and only then call the block
complete. **Never present an ad that fails.** Hold it back and say which one and
why. Paste the script's summary line in the delivery note.

## 9. Deliver

Export each artboard from Paper at **scale 1**, no more than six artboards per
export call, and verify every file is 1080 wide before moving on; Paper's default
scale has changed mid-run and produced 2160-wide files. Move the files out of
Downloads into the concept folder as `<angle>-<variant>-<ratio>.png`.

Then report, in plain language:

- the Paper file and how the canvas is organised (one row per angle);
- per angle: the variants built, the reference each one modelled, what the
  variant tests;
- the preflight summary line, and the WARNs you chose to leave, with why;
- where the Meta ad text for each angle is (`ad-unit.md`, and the text card at
  the end of each row in Paper);
- what was spent, against what was quoted;
- which fonts Paper drew and how that was proven, any fallback, intentional
  format omissions and any ratio-specific simplification;
- anything held back.

Close with the two things the person can do next: edit anything in Paper for
free, or tell you the verdicts.

## 10. Verdicts, and what the brand learns

The person reviews in Paper and answers in a sentence. Accept any of: `keep
a1-v2`, `kill a3-v1: too dark`, `change a2-v1: shorter headline`, or a note about
the whole batch.

- **Keep:** mark the concept `approved` in its `spec.json` and set its angle to
  `validated` in the campaign's `angles.md`. A validated angle gets more variants
  next campaign.
- **Change:** a copy note goes to `/ad-angles --rewrite` and the one layer is
  updated in Paper. A layout note is fixed in Paper. A note that applies to every
  ad ("subheads bigger") is applied to every ad, then written as a Default. Only
  a note about the photograph itself costs a plate, and that goes through the
  cost gate. A note asking for more variants is answered with a proposal, and the
  new variant is built only on a yes; it goes into the row before the Meta ad
  text card, and the card moves right.
- **Kill:** every variant of an angle killed means the angle is `killed`, with
  the reason. Generalise the reason and file it in `intelligence/learnings.md`:
  an objective defect (wrong pack, an unsupported claim, a compliance problem)
  under `## Rules`, permanent; a matter of taste under `## Defaults`, a strong
  preference a later batch may still test against. Quote the person's words and
  date the line. Confirm a new Default in one line before writing it.
- **A Default with a number in it becomes a check.** "Subheads at least 42px"
  goes into `intelligence/preflight.json` as `"min_px": {"subhead": 42}`; "no
  empty band under 9:16 ads" lowers `"max_empty_bottom"`. The next run fails on
  it instead of hoping.
- A kill with no reason is recorded, not turned into a rule. Ask once.
- Learnings carried over from another system's verdicts (a previous tool, an
  older folder) are shown to the person as one block, with a count, and
  confirmed before they bind. Until then they are marked `proposed`.

`/ad-angles` and this skill both read `learnings.md` and `preflight.json` at the
start of every run. Those two files are how the second batch is better than
the first.
