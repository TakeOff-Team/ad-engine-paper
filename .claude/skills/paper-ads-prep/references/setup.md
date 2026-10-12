# setup.json: format reference

> **What this is.** The small file `/paper-ads-prep` writes to `intelligence/setup.json`.
> Nothing in it is asked: `/paper-ads-prep` works it out and says what it concluded.
> `/paper-ads` reads it before it does anything that costs money or needs a
> product photo.

```json
{
  "brand_type": "product",
  "image_tool": "paper",
  "paper_file_id": null,
  "tools": {"paper": true, "firecrawl": false},
  "chosen": "2026-10-11"
}
```

| Field | Values | Read by |
|---|---|---|
| `brand_type` | `product` (a physical thing with a pack shot) or `service` (services, courses, software, anything without one). Worked out from the site | `/paper-ads`: product photos need a packshot and a size reference; a service brand's photo is a scene, a setting or a moment, never a product |
| `image_tool` | `paper` (the default for every brand), or `higgsfield` / `fal` only when the person asks to switch | `/paper-ads`: which tool makes the photo |
| `image_model` | optional, only after a switch. Higgsfield: `nano_banana_pro` (default) or `gpt_image_2`. On fal the script fixes the model | `/paper-ads` |
| `paper_file_id` | filled in the first time the brand's Paper file is created | `/paper-ads` |
| `tools` | what the tool check found, direct or through Composio | every skill, so nothing is checked twice |
| `chosen` | the date | nobody; it is there so a stale choice is visible |

Older brands may also carry `relationship`, `advertiser` or `landing_url`. They
are ignored now.

## Switching the image tool (only when the person asks)

Every brand starts on Paper's own image generation, and nobody is asked about
it: Paper is already required, so there is nothing else to sign up for. The tool
check tells the person once that they can switch. Only when they ask, explain
the trade in plain words, then change `image_tool` (and `image_model` if needed)
and say which line changed.

> "Only the photo behind the ad ever costs anything. Every word is an editable
> layer in Paper, so copy and layout changes are free whichever tool makes the
> photo.
>
> **Paper (what you're on now).** Nothing extra to set up, and it has the top
> models built in. The free plan allows only a handful of images; Paper Pro ($20
> a month) gives about a hundred times more per week. If you're building more
> than a few ads a week, you'll want Pro.
>
> **Higgsfield.** Good if you already pay for it. It connects through Claude with
> no keys to paste, and your plan's credits cover the photos. It's a
> subscription, and a big batch can run a plan dry.
>
> **fal.** Pay only for what you make, about ten cents a photo, no subscription.
> You create an account, add a few dollars and paste a key into one file. I'll
> walk you through it."

When switching to Higgsfield, check the balance; to fal, check `FAL_KEY` in
`.env`. Prices drift: if the person asks for exact numbers, check the tool's
current pricing rather than quoting this file.
