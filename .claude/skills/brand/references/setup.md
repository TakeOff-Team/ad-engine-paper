# setup.json: format reference

> **What this is.** The small file `/brand` writes to `intelligence/setup.json`
> from the setup questions in Step 0b. Every downstream skill reads it before it
> does anything that costs money or needs a product photo.

```json
{
  "brand_type": "product",
  "image_tool": "paper",
  "image_model": "nano_banana_pro",
  "relationship": "own",
  "advertiser": "The brand itself",
  "landing_url": "https://your-brand.com/?utm_source=meta",
  "paper_file_id": null,
  "chosen": "2026-10-03"
}
```

| Field | Values | Read by |
|---|---|---|
| `brand_type` | `product` (a physical thing with a pack shot) or `service` (services, courses, software, anything without one) | `/paper-ads`: product plates need a packshot and a size reference; service brands have no pack shot, so a base photo (when the reference calls for one) is a scene, a setting or a moment, never a product, and needs no size reference |
| `image_tool` | `paper` (the default for every brand), or `higgsfield` / `fal` only when the person asks to switch | `/paper-ads`: which path makes the photographic plate |
| `image_model` | optional override. Valid Higgsfield ids: `nano_banana_pro` (default, 4:5 native) or `gpt_image_2` (no 4:5, cropped from 3:4). On fal the script fixes the model; leave it out | `/paper-ads` |
| `relationship` | `own`, `client` or `practice`. A client brand holds every unverified offer, named person and competitor mention for sign-off; a practice brand flags them and continues | `/ad-angles`, `/paper-ads` |
| `advertiser` | who runs the ads: the brand, or the person as an affiliate or agency | `/ad-angles` |
| `landing_url` | the exact link every ad sends people to, affiliate or tracking parameters included | `/ad-angles` (display link and URL in the ad text) |
| `paper_file_id` | filled in by `/paper-ads` the first time it creates the brand's Paper file | `/paper-ads` |
| `chosen` | the date | nobody; it is there so a stale choice is visible |

Changing tools later is editing one line. Say so when you write the file.

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

## Advertiser and link, in plain words

> "Whose ad account will these run from, and what link should every
> ad send people to? If you run them as an affiliate or an agency, give me the
> exact link with your tracking on it."

## Brand type, in plain words

> "And what does the brand sell: a physical product I can photograph, or a
> service, course or software with no pack shot?"

A brand that sells both is `product` if most ads will show the product, and the
person can say otherwise per campaign.
