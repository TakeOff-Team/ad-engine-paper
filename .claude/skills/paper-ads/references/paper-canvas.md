# The Paper canvas

How the ads are arranged in Paper, how they are named, and the quirks worth
knowing before the first artboard.

## One file per brand, one row per reference

Each brand has one Paper file. If `paper_file_id` is empty, create one
(`create_file`, named `ad-engine · {Brand}`), open it (`open_file`), and record its
id as `paper_file_id` in `intelligence/setup.json`; never ask the person to make
or open a file. Reuse it after that. Every session opens the file before doing
anything else.

Each batch is a block on the canvas, with a plain text label above it (the
date). Inside the block, one row per reference:

```
[2026-10-11]

[ref · r1] [r1 · 4x5][r1 · 9x16]
[ref · r2] [r2 · 4x5][r2 · 9x16]   [r2-v2 · 4x5][r2-v2 · 9x16]
[ref · r3] [r3 · 4x5][r3 · 9x16]
```

- **A row is one reference** and the ad remade from it. Rows run top to bottom
  in reference order.
- **The reference** sits at the left edge as a small locked image artboard named
  `ref · r1`, so the person can compare the original with the remake. It is
  never shipped.
- **An ad is a pair:** the 4:5 artboard, then the 9:16 artboard, side by side.
  Extra versions, only when asked (`r2-v2`), follow in the same row.

Spacing: 80px between the two ratios of one ad, 240px between versions, 480px
between rows, 960px between batches. Consistent gaps are what make the canvas
readable at a glance; do not eyeball them.

## Naming

- Ad artboards: `r1 · 4x5` and `r1 · 9x16`; extra versions `r1-v2 · 4x5`.
- Reference: `ref · r1`. Batch label: the date.
- Layers inside an ad, by role: `plate`, `headline`, `subhead`, `cta`, `rating`,
  `badge-1`, `card-1`, `legal`, and so on. Role names are what make a later
  one-layer edit possible.
- A held ad keeps its name and gains a suffix in brackets: `r3 · 9x16 (HELD:
  strap in the rail)`. The preflight lists it as HELD with the reason and never
  counts it as a pass.
- A transparent cutout (a person or product with the background removed) is
  named `cutout-…` so the preflight knows its box is bigger than the figure.
- A revised ad replaces its artboard in place. Do not pile up `r1 (2)`.

## Order of work on the canvas

1. Open the brand file (create it on the first run and record the id).
2. Create or reuse the brand's design tokens: the palette from
   `color-palette.json`, the type roles from `typography.json`.
3. Lay out the batch label and the references first, so the structure is
   visible before anything is built.
4. Build wireframes into their slots (SKILL step 4).
5. Place approved plates and finish each ad (SKILL step 7).
6. Screenshot the full canvas for the delivery report.

## Font preflight (do this before the first wireframe)

Paper draws from fonts installed on the machine and from Google Fonts. A font
file sitting in `intelligence/fonts/` is invisible to Paper until it is
installed.

1. For each family in `typography.json`, ask Paper whether it has it.
2. Then prove it, both halves: write one throwaway text layer in that family,
   **read its computed style back** (the family Paper actually resolved), and
   screenshot it. The font lookup tool can refuse right after a file is opened;
   the throwaway layer is the proof that counts. Some Paper versions accept a family
   name and silently draw the system font instead. If the computed family or the
   screenshot shows a fallback, the face is not available, whatever the lookup
   said.
3. Missing and open-licence: install the file from `intelligence/fonts/` into
   the user's font folder, then tell the person to restart Paper (it does not
   rescan). Missing and licensed: ask before installing.
4. Still unavailable: use the stand-in `typography.json` names. Only if that is
   missing too, the closest face Paper has. Either way say so in one line,
   update `typography.json` with what was used, and treat the embedded-font SVG
   from `compose-text.py` as the exact visual.

Delete the throwaway layer.

## Cropping a photo

A photo is the `backgroundImage` of its frame, with `backgroundSize: cover`.
The crop is `backgroundPosition` (for example `50% 30%` to show more of the
top). **`objectPosition` does nothing on a frame.** Paper stores it and ignores
it, which is how a whole run shipped with every head cut off while the style
said otherwise. The preflight fails any photo frame that carries
`objectPosition`.

Before setting a crop, read the file's real orientation. A photo with EXIF
rotation reports its width and height swapped in a quick listing, and crop maths
done on the wrong numbers lands the subject in the wrong place. Open the image
and look. After placing, screenshot the frame at scale 1 and confirm the head,
hands and product are inside the frame with room to spare.

## Writing, reading, exporting

- **One write at a time.** Parallel `replace` writes have returned success and
  changed nothing. After a disconnect, read back every write that was in flight
  before trusting it.
- **Screenshots lag one write behind.** Make a cheap read (basic info) first,
  then screenshot, or you review the state before your edit.
- **Export at scale 1, six artboards per call at most.** Larger batches have
  dropped files without an error, and Paper's default scale has flipped to 2x
  mid-run. Check every exported file is 1080 wide; resize a 2160-wide file
  before filing it.

## Quirks that cost time

- Inline styles only: no stylesheets, no classes, no scripts, no tables, no
  margins. Use flex or absolute positioning.
- Local images are referenced as `paper-asset:///absolute/path`.
- `create_artboard` ignores `left` and `top`; position the artboard with
  `update_styles` after creating it. `right` is ignored on nodes; compute
  `left`. A cloned button can lose `display: flex`; re-apply it and check.
- Hard-stop gradients and `background-size` patterns can be stripped. For a grid,
  dots or any pattern, render a PNG and use it as an image.
- An export fired straight after writing can return the bare artboard. Wait a
  moment and retry up to three times; check the file is not implausibly small.
- Exports land in the user's Downloads folder under the artboard name. Move them
  into the concept folder and rename them (SKILL step 9).
- Text layers size to their content. A long headline that wraps to an extra
  line pushes everything under it; the preflight catches the overlap, but check
  the wrap yourself on any headline over about 24 characters at 96px.
- If Paper reports a usage limit, stop cleanly, say what is built and what is
  not, and pick up from the next artboard when it clears. Never rebuild finished
  artboards.
