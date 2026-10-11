# Ad Engine: Paper

Find an ad you love. Get it remade for your brand.

Point Claude at your website once and it learns your brand: colours, fonts, logo, products, voice and real offers. Then drop in ads you like, from any brand, and it remakes each one for you: same format, same idea, your product, your words, your look. Built in Paper, so every word is an editable layer. Only the photo behind it costs anything, and nothing is spent without your yes.

<!-- skills-count:start -->
Two skills. One brand context both of them read.
<!-- skills-count:end -->

> Looking at this folder and it seems near-empty? The skills live in `.claude/`, a hidden folder. It's there. Press `Cmd+Shift+.` in Finder to see it, or just open a Claude session here and everything works.

## What you need

| | Why | Cost |
|---|---|---|
| **Claude Code** or **Claude Cowork** | Runs the skills | Your Claude plan |
| **Paper Desktop**, connected to Claude | The ads are built there as editable layers, and it makes the photos with its built-in image generation | Free tier to try it; Pro for real volume |
| **Python 3** | Runs the small scripts | Free |
| Optional: **Firecrawl** | Reads your website more cleanly | Free tier works |

That's the whole list. Already pay for **Higgsfield** or **fal**? Say so any time and the photos switch over. Connected through Composio? That works too.

## Start here

Open Claude Code in your project, open Paper Desktop, and paste this:

```
Install the ad skills from https://github.com/TakeOff-Team/ad-engine-paper into this project and onboard my brand: https://your-brand.com

1. Clone the repo into a temporary folder and copy its skill folders into this project's .claude/skills folder. If a skill with the same name is already there, ask me before replacing it.
2. Set up a Python venv in this project and install the repo's requirements.txt into it.
3. Check that Paper is connected and open a Paper file for my brand. If Paper isn't connected, tell me in plain steps how to connect it.
4. Don't make me restart. Open .claude/skills/brand/SKILL.md and follow it for my brand, starting with the tool check.

Explain each step in plain language. I'll answer with voice-to-text.
```

Replace the URL with your website. Already have your business described in this project? It reads that first and won't ask you what you already told it.

Starting from a fresh folder instead? Clone this repo, open Claude Code inside it, and paste the same prompt.

## Then make ads

1. **Find two or three ads you love.** From any brand, any industry. Screenshots are fine. The easiest place is the [Meta Ad Library](https://www.facebook.com/ads/library): search a brand you admire and look for ads that have been running for months, because brands keep paying for the ones that work. Pinterest and ads that stopped your own scroll work too.
2. **Drop them in** `brands/[your-brand]/generation/paper-ads/ad-references/`, or just paste them into the chat.
3. **Run:**

```
/paper-ads
```

For each ad, it works out why it works (the format and the hook), rewrites every line for your brand from your real products and offers, and shows you the layouts and the words before spending anything. Say yes, and it makes one photo per ad, builds it in Paper in 4:5 feed and 9:16 stories, and measures every ad before calling it done.

4. **Tell it what you think,** in plain words. "Love the second one." "The first headline is too long." "Too dark." Copy and layout changes are free. If you don't like something, it remembers why, so the next batch doesn't repeat it.

Next time, it's just steps 1 to 4. Your brand is already set up.

## The skills

<!-- skills-table:start -->
| | |
|---|---|
| **`/brand`** | Point it at a URL, get a brand brain. Run this first. Also folds new products, images, docs and facts into an existing brand at any time |
| **`/paper-ads`** | Drop in ads you like; it remakes each one for your brand in Paper, every word editable, in 4:5 and 9:16, measured before delivery |
<!-- skills-table:end -->

## If something goes wrong

| What you see | What it means | Fix |
|---|---|---|
| Claude says it does not know `/paper-ads` | Claude was not opened in the folder the skills are in | Open a new Claude session in that folder |
| Claude asks you to connect Paper | Paper Desktop is closed, or not connected to Claude | Open Paper Desktop, turn on its Claude connection, say "go" |
| The build stops and asks about a model substitution | Higgsfield served a cheaper model than the one requested | Say whether to continue on it, switch, or stop. It will not spend again until you answer |
| An ad is listed as held | It failed a measured check and was kept back on purpose | Fix it in Paper (free) or drop it. It will never be presented as finished |
| The brand font looks wrong in Paper | Paper could not find the font on your machine | Install the font file from `brands/[brand]/intelligence/fonts/`, restart Paper, say "go" |
| A script says "FAL_KEY not found" | You switched photos to fal and the key is not in `.env` | Copy `.env.example` to `.env` and paste your key |

## Layout

| Path | What it is |
|---|---|
| `CLAUDE.md` | Where the system's rules, tools and conventions live |
| `.claude/skills/` | The skills. Each one is a self-contained folder with its scripts |
| `brands/[brand]/` | Created by `/brand`: `intelligence/` (what the brand is) and `generation/` (what you make). Don't build it by hand |

## What it will never do

Invent an offer, a price or a guarantee. Copy another brand's name, product, claims or exact lines. Generate a person and attach a name and a quote. Render a dashboard or screenshot that does not exist. Spend a credit without a yes. Call an ad finished that it did not measure.
