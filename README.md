# Ad Engine: Paper

Point Claude at your brand's website and get a brand brain. Tell it who your customers are in their own words. Then get a campaign of static ads built in Paper: four to five angles, two variants each, in 4:5 feed and 9:16 full-screen, with the Meta ad text written for every angle. Every word on every ad is an editable layer. Only the photograph behind it costs anything, and nothing is spent without your yes.

<!-- skills-count:start -->
Four skills. One brand context every one of them reads.
<!-- skills-count:end -->

> Looking at this folder and it seems near-empty? The skills live in `.claude/`, a hidden folder. It's there. Press `Cmd+Shift+.` in Finder to see it, or just open a Claude session here and everything works.

## What you need

| | Why | Cost |
|---|---|---|
| **Claude Code** or **Claude Cowork**, opened in this folder | Runs the skills and the scripts | Your Claude plan |
| **Paper Desktop**, connected to Claude | The ads are built there, as editable layers. Not optional | Free tier works |
| One image tool: **Paper's own image generation**, **Higgsfield**, or a **fal.ai** key | Makes the photograph behind each ad. Asked once per brand, with the trade-offs explained | Included in Paper (Pro for real volume), Higgsfield credits, or about ten cents a photo on fal |
| **Python 3** | Runs the small scripts | Free |
| Recommended: **Claude in Chrome** | Lets `/brand` read colours, fonts and your logo straight off your site | Free |
| Optional: the **Apify** connector | Lets `/ad-scout` pull the ads your competitors are running | A few cents per pull |
| Optional: **Firecrawl** | Cleaner reads of your website | Free tier works |
| Optional: **Perplexity** | Faster, sourced research on reviews and competitors | Your Perplexity plan |

Only Paper is required. Every other tool has a fallback, and `/brand` tells you once what you have, what you're missing, and what each one would add. Details in [TOOLS.md](TOOLS.md).

## Start here

Clone this repo, open Claude Code in the folder, make sure Paper Desktop is open with a file open, and paste this:

```
Set me up: create a Python venv in this folder and install requirements.txt into it, check that Paper is connected, then run /brand for https://your-brand.com and take me through it. Explain each step in plain language. I'll answer with voice-to-text.
```

Replace the URL with your brand's website. That is the whole setup. The venv keeps this project's Python packages in their own folder, so nothing else on your machine changes.

If you would rather type it yourself:

```bash
git clone https://github.com/TakeOff-Team/ad-engine-paper.git
cd ad-engine-paper
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # only if you chose fal
```

Then, in Claude Code from this folder:

```
/brand https://your-brand.com
```

That builds your brand's operating system under `brands/[brand-name]/`: strategy, positioning, voice, colour, typography, product catalog, the named people you sell to in their own words, and your offers. It asks four setup questions on the way: what you sell, which image tool, whose ad account, and whether this is your brand, a client's, or practice.

Then give it formats to model. Drop ads you like into `brands/[brand-name]/generation/paper-ads/ad-references/`. No references? Run:

```
/ad-scout
```

It asks first, then pulls what your category is running so you can pick. Then:

```
/ad-angles
/paper-ads
```

## The skills

<!-- skills-table:start -->
| | |
|---|---|
| **`/brand`** | Point it at a URL, get a brand brain. Run this first. Also folds new products, images, docs and facts into an existing brand at any time |
| **Ads** | `/ad-angles` · `/ad-scout` · `/paper-ads` |
| ↳ `/ad-angles` | Angles, on-image copy and Meta ad text in the customer's own words, every claim traced. Run before building |
| ↳ `/ad-scout` | Optional. Pulls the ads running in your category and files the ones you pick as references |
| ↳ `/paper-ads` | Builds every ad in Paper as an editable layout over a text-free photo, in 4:5 and 9:16, arranged by angle, measured before delivery |
<!-- skills-table:end -->

## How a campaign gets made

1. **Angles first.** An angle is one reason a specific person buys. `/ad-angles` proposes four to five, each with two variants that change exactly one thing, and you approve the plan before a word is written.
2. **Copy in their words.** Headlines come from your customers' own phrases. Every number traces to your product catalog or your offers list. Offers are never invented, and a testimonial that claims a result is held to the same rules as your own copy.
3. **Wireframe in Paper.** Each ad is laid out with the real copy, in both ratios, before any image exists.
4. **Generate only the photography.** One text-free photo per ad, approved by you before copy goes on it. The tall version is derived from the approved feed photo by geometry, so the product lands in the safe zone and both ratios show the same shot. Formats with no photo in them cost nothing.
5. **Editable ads, arranged by angle.** One row per angle on the Paper canvas, each variant as a 4:5 and 9:16 pair, the Meta ad text at the end of the row.
6. **Measured, not eyeballed.** A script reads every artboard straight out of Paper and fails any ad with text over the product, clipped lines, type too small for a phone, or a button in the Stories rail. Nothing is called done until it passes.
7. **Tell it what you think.** `keep a1-v2`. `kill a3-v1: too dark`. Keeps make an angle stronger next time. Kills become rules the brand never breaks again.

Copy and layout changes are free. Only a new photograph costs money.

## If something goes wrong

| What you see | What it means | Fix |
|---|---|---|
| Claude says it does not know `/brand` | Claude was not opened in this folder | Open a new Claude session with this folder selected |
| "Open Paper Desktop with a file open" | Paper is closed, or no file is open, or Paper is not connected to Claude | Open Paper with any file, connect it in Claude's connector settings, start a new session |
| The build stops and asks about a model substitution | Higgsfield served a cheaper model than the one requested | Say whether to continue on it, switch, or stop. It will not spend again until you answer |
| A photo keeps failing in 9:16 | The product lands in the Stories button rail | The build derives the tall version from the approved feed photo instead of generating it fresh; if it still fails, it asks before re-rendering |
| An ad is listed as held | It failed a measured check and was kept off the delivery on purpose | Fix it in Paper (free) or kill it. It will never be presented as finished |
| The brand font looks wrong in Paper | Paper could not find the font on your machine | Install the font file from `brands/[brand]/intelligence/fonts/`, restart Paper, say "go" |
| Onboarding asks about customers and references | That is the context the ads are built from | Talk, voice-to-text is best. Messy is fine |
| A script says "FAL_KEY not found" | You chose fal and the key is not in `.env` | Copy `.env.example` to `.env` and paste your key |

## Layout

| Path | What it is |
|---|---|
| `CLAUDE.md` | How the system works and the rules it follows |
| `.claude/skills/` | The skills. Each one is a self-contained folder with its scripts |
| `brands/[brand]/` | Created by `/brand`: `intelligence/` (what the brand is) and `generation/` (what you make). Don't build it by hand |

## What it will never do

Invent an offer, a price or a guarantee. Generate a person and attach a name and a quote. Render a dashboard or screenshot that does not exist. Lift a competitor's line. Spend a credit without a yes. Call an ad finished that it did not measure.
