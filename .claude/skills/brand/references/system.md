# Ad Engine: Paper, system rules

Read once per session by `/brand`, `/ad-scout`, `/ad-angles` and `/paper-ads`.

On-brand static ads, grounded in the brand's full business context and in its customers' own words, built in Paper so every line stays editable. `/brand` builds the brand's operating system; `/ad-scout` (optional) finds reference formats; `/ad-angles` turns customer language into angles, copy and Meta ad text; `/paper-ads` builds each ad as a text-free photographic plate plus independently editable text and UI, in 4:5 and 9:16, arranged on the canvas by angle.

It is not much of a codebase on purpose. The skills are the product; the brand's own files are the substrate they read.

## Modularity

**Each skill describes itself. Nothing outside a skill keeps a list of skills.**

- Every skill's `SKILL.md` frontmatter declares its `outputs:` and `inboxes:` (folders under `brands/<brand>/generation/`), `requires:` (hard needs), `optional:` (soft needs it degrades without), and a `version:`. Scaffolding, validation and the docs tables all derive from these declarations.
- **Skills create their own folders on first use** (`mkdir -p` for each declared path). `/brand`'s scaffold is a convenience, not a prerequisite.
- Everything reads the brand intelligence `/brand` writes. The shapes of the `intelligence/` files are the system's internal API; change them only deliberately.
- `python3 .claude/skills/brand/brand.py --validate` checks every declaration; `--docs` regenerates the skill tables between markers in `README.md` and this file.

## How this system thinks

- **Angles, not ads.** A campaign is four to five hypotheses about why a specific person buys, each tested with two variants that differ on exactly one thing. The canvas, the files and the review are all organised by angle.
- **Their words, not ours.** Copy is arranged from the customer's own phrases in `avatars.md`. A pain several customers named outranks one the founder guessed.
- **The image model never draws a word.** It makes a text-free photograph. Everything a customer reads is an editable layer in Paper.
- **Paper is the deliverable.** Not a mirror of a render. If Paper is not connected, the build stops and says so.
- **Never show a subpar ad.** `preflight.js` measures every artboard straight out of Paper (overlaps, clipped text, dead crops, type under the floor, safe zones, the 9:16 rail, empty bands) and the build is not finished until it reports zero failures. Eyes are for what it cannot measure: a cut-off head, a figure that blends in, a line that reads wrong.
- **The brand learns.** Verdicts become `intelligence/learnings.md`: Rules that are never broken, Defaults that are strong preferences, angles marked validated or killed.
- Claude does the judgment (angles, copy, layout, art direction). Scripts do the mechanical work and checks. Don't script the judgment.

## Repository map

- `.claude/skills/brand/`: point it at a URL, get a brand brain. **Run this first.** It also asks the four setup questions (what you sell, image tool, whose ad account and link, own brand or client or practice) and scaffolds every folder.
- `.claude/skills/ad-scout/`: optional reference finding. Always asks before pulling.
- `.claude/skills/ad-angles/`: angles, on-image copy, claims ledger, Meta ad text.
- `.claude/skills/paper-ads/`: the build, in Paper, and `preflight.js`, the measuring script. Conventions for all skills in `.claude/skills/brand/references/conventions.md`.

<!-- skills-table:start -->
| | |
|---|---|
| **`/brand`** | Point it at a URL, get a brand brain. Run this first. Also folds new products, images, docs and facts into an existing brand at any time |
| **Ads** | `/ad-angles` · `/ad-scout` · `/paper-ads` |
| ↳ `/ad-angles` | Angles, on-image copy and Meta ad text in the customer's own words, every claim traced. Run before building |
| ↳ `/ad-scout` | Optional. Pulls the ads running in your category and files the ones you pick as references |
| ↳ `/paper-ads` | Builds every ad in Paper as an editable layout over a text-free photo, in 4:5 and 9:16, arranged by angle, measured before delivery |
<!-- skills-table:end -->

- The brand folder (`04-Brand/clients/[brand]/` in a vault that has one, otherwise `brands/[brand]/`): the context substrate: `intelligence/` (identity, strategy, customers, commercial files, setup, learnings) and `generation/` (versioned outputs). Created by `/brand`, never by hand. See `brands/README.md`.

## Generation

The brand's **prompt modifier** (`visual-guidelines.md`) opens every image prompt and is what makes a plate look like the brand rather than like stock AI. The image tool is the brand's choice, recorded in `intelligence/setup.json`: Paper's own image generation, Higgsfield through its connector, or fal through `FAL_KEY`. All three cost money, credits or plan usage. The build states the exact cost and gets explicit approval before any paid call. A format with no photograph in it generates nothing and costs nothing.

## Tools

Best tool first, fallback always, the person told once. The full table, the cheap way to check each tool, and the connect lines are in `.claude/skills/brand/references/tools.md`. Only Paper is required.

## Guardrails (non-negotiable)

1. **Nothing is spent without an explicit yes.** Show the cost before the first paid call, for fal dollars, Higgsfield credits and Paper generations alike, and for Apify pulls over a dollar.
2. Offers come from `intelligence/offers.md` by ID; claims must be supportable by `brands/[brand]/intelligence/` content. Compliance rules in `brand-voice.md` are hard constraints, and no style or conversion rule may harden a health claim past what `intelligence/` supports. Truth outranks voice, which outranks everything else.
3. Reference ads and competitor ads contribute format and structure only, never another brand's copy, product or likeness.
4. No em dashes in any line a customer reads.
5. No fabricated people, quotes, reviews, screenshots or dashboards. Proof is real or it is absent.
6. **No claim of a check that did not run.** "Nothing failed" and "fonts rendered" are quotes of a measurement or they are not said.
7. **Nothing written to the brand's files without saying so.** Offers, copy, angles and specs change only on the person's word, and a request to "try a variant" is answered with a proposal, not a build.


## Starting state

- **First move: `/brand <url>`.**
- **Then references:** drop them in, or `/ad-scout`.
- **Then `/ad-angles`, then `/paper-ads`.**
- Chat is plain language. No step codes, no schema names, no file names unless the person needs to open one. Explain any term of art the first time it appears (an angle is one reason a specific person buys; a variant changes one thing; a plate is the photo with no words on it). Every step closes with a short summary plus what the person does next.
