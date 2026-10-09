# Plates through Paper's own image generation

Used when `intelligence/setup.json` says `image_tool: paper`. Paper has the top
image models built in and generates straight into the canvas, so the person
needs no second tool.

**Read Paper's own guide first, every session:** `get_guide` with topic
`image-generation`. It holds the current syntax (generation is requested with
`paper-gen://` image URLs inside `write_html`, `update_styles` or
`create_artboard`), the models on offer and how to pass reference images. Paper
changes faster than this file. If the guide and this file disagree, the guide
wins.

## What is verified (2026-10-09, Dream Recovery test)

- **It takes reference images.** Pass the packshot as `reference_nodes` and the
  model keeps the real product: logo, label, tag and strap all survived. So
  product plates work through Paper, not just scenes.
- **The call:** `write_html` with `targetNodeId` (the frame) and `mode:
  "insert-children"`, holding `<img src="paper-gen://{model}?prompt=...&reference_nodes={id}">`.
  The packshot goes in first as an `<img src="paper-asset:///abs/path">` and its
  node id is the reference.
- **Models and cost** (usage units per image): `google-nano-banana-2-1` 1, the
  default for scenes and for product with a reference; `openai-gpt-image-edit-2-5`
  2, when a reference needs transparency or more precision; `nano-banana-pro` /
  `nano-banana-pro-edit` 4, for 2K output when it matters.
- **No 4:5.** Nano Banana 2.1 offers 3:4 and 9:16; request 3:4 and let
  `save-plate.py` crop. With a reference image, the output follows the
  reference's ratio instead, so use a reference cropped to 3:4, or crop after.
- **Ten images per call at most**, and a call that would exceed the weekly
  allowance is declined whole. Generate a block's plates in calls of ten or
  fewer.
- **It returns at once and fills later.** Poll the node until
  `imageGeneration.status` is `ready` (about a minute for two), then pull the
  file with `get_fill_image`.

## The steps

1. **Say the count first.** Paper does not charge per image, but generations
   count against the person's weekly limit (Free: limited; Pro: about 100x
   more). State how many plates the block needs. A yes is still required,
   because a used-up weekly limit stops the rest of the campaign.
2. **Generate into a scratch frame, not the finished ad.** Create a frame at the
   plate's exact size beside the artboard, and request the generation as its
   background, with the same prompt rules as any plate: brand prompt modifier
   first, the image zone and clear space described, and the closing line
   "Absolutely no typography anywhere except the printed product packaging."
3. **Pass the references** (packshot, size reference) in whatever way the guide
   describes. **If Paper's generation cannot take reference images**, it cannot
   be trusted with a real product: use it only for plates with no product in
   them (scenes, settings, textures), and say that product plates need
   Higgsfield or fal.
4. **Wait for it.** Poll the frame's node info until the generation status is
   ready. An error is a failed try.
5. **Pull it out and file it.** Download the result with the fill-image tool,
   then run `save-plate.py` on the downloaded file. It crops to ratio, resizes to
   delivery size and desaturates by 10%, same as every plate. Then
   `product-bbox.py`.
6. **Approve, then place.** The person approves the plate exactly as with any
   other tool. The approved file is placed as the image zone's background in the
   real artboard and the scratch frame is deleted.

The 9:16 is derived from the approved 4:5 with `extend-plate.py`, and the fill
is a Paper generation on the canvas it writes, same rules.

Record `image_tool: paper`, the model named in the guide, and tries per plate in
`spec.json`.
