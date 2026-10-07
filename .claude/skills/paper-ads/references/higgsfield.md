# Plates through Higgsfield

Used when `intelligence/setup.json` says `image_tool: higgsfield`. Claude calls
the Higgsfield connector directly; there is no script for the generation itself.
`save-plate.py` files the result.

The model ids below (`nano_banana_pro`, `gpt_image_2`) are Higgsfield **model
ids**, not separate tools or servers.

## Which model

| Model | Use it for | Ratios |
|---|---|---|
| `nano_banana_pro` (default) | Product plates with a packshot and a scale reference; scenes | 4:5 and 9:16 natively |
| `gpt_image_2`, quality high | **Required** for people prominent in frame, and **required** after the first model misses twice on a plate | 9:16 natively, **no 4:5**: request 3:4 and let `save-plate.py` crop |

When requesting 3:4 for a 4:5 plate, tell the model to keep the product and the
required clear space inside the central band, because about 6% of the height is
cropped away.

`setup.json` `image_model` overrides the default for the brand.

## The call, in order

1. **Upload the references.** A local file (packshot, scale reference, format
   reference) goes through the connector's media upload; a public URL through
   its import-by-URL tool. Keep the returned media ids.
2. **Quote first.** Call the image generation tool with the full request and
   `get_cost: true`. Its arguments are nested under a `params` object, and
   `get_cost` goes **inside** `params`. Passed at the top level it is ignored and
   a real job is submitted and charged. The quote returns credits and submits
   nothing.
3. **Show the cost and get a yes.** Total credits for every plate in the batch,
   the balance, and the maximum with one retry per plate.
4. **Generate.** Same request without `get_cost`: model, prompt, `aspect_ratio`,
   `resolution: "2k"`, and the reference media ids in the role the model
   declares (`image_references` for `nano_banana_pro`, `image` for
   `gpt_image_2`). Check the tool's own schema for the exact field shape; it
   changes more often than this file does.
5. **Wait** for the job, then read the result URL.
6. **Check what served.** Read the model name back off the finished job. The
   service has substituted a faster model for the one requested before (Dream
   Recovery: fourteen of fourteen jobs). Record `model_requested` and
   `model_served` in `spec.json`, never report the requested model as the one
   that ran, and **stop before the next paid call to tell the person**: what
   was served, what it costs, and the choice between continuing on it,
   switching, or stopping. Not in the final report. Before the next credit.
7. **File it:**
   ```bash
   python3 .claude/skills/paper-ads/save-plate.py <concept-folder> --variant feed_4x5 --source "<result url>"
   ```
   It downloads, crops to ratio if needed, resizes to delivery size (1080 wide), desaturates by 10%, and writes
   `[name]-feed_4x5-plate_v1.png`.

Batches: submit all plates in one batch call where the connector offers one, and
wait on them together.

## Deriving the 9:16 from the approved 4:5

`extend-plate.py` has written `<name>-fullscreen_9x16-canvas_vN.png` (the 4:5
placed on a flat ground inside a 1080×1920 frame) and the matching mask. The
model's job is to continue the photograph into the flat areas and change
nothing inside the pasted photo.

1. Upload the canvas as a media file.
2. Quote, then call `generate_image` with `nano_banana_pro`, the canvas as the
   image reference, `aspect_ratio: "9:16"`, and a prompt of this shape: the
   brand's prompt modifier, then "Extend this photograph to fill the whole
   frame. Everything inside the existing photograph stays exactly as it is:
   same product, same hands, same lighting, same crop. The flat areas become a
   seamless continuation of the background. No new objects, no text."
3. If the connector offers `outpaint_image`, that is the alternative: upload the
   canvas, quote with `get_cost`, run at 9:16. It takes no prompt, so use it
   when the background is simple and the model edit when it is not.
4. File the result with `save-plate.py --variant fullscreen_9x16`. The product
   box for the 9:16 is already in `spec.json` from `extend-plate.py`; check the
   result against it by eye at 100%: the product must not have moved.

A fresh 9:16 generation is the fallback, not the default.

## Things that go wrong

- **Listing recent generations returns the whole account,** prompts included,
  across every brand. Ask for the smallest page that covers this batch and match
  by prompt and time. Do not paste the list.
- **A plate with letters in it** is a reject, however small the letters. The
  prompt already forbids them; a second failure means the reference image itself
  carries text the model is copying. Drop the format reference from the call
  (`reference_image_for_generation: false` in `spec.json`) and describe the
  composition in words instead.
- **No reference at all** (a service brand's proxy scene): skip the upload step
  and generate from the prompt alone.
