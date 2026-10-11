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

## Who this is for

Assume the person has **low technical skill and has barely used AI.** Many have
never opened a terminal. Everything the skills say and do is built so this
person never feels lost or scared off:

- **Fix it, don't flag it.** If something can be sorted without the person, sort
  it and say what you did in one line. Paper is open but no file is? Create the
  brand's file and open it. A tool is connected through Composio rather than
  directly? Use it that way. Only ask when the person genuinely has to act.
- **No warning signs, no red crosses, no error language.** Never show ⚠️ or ❌,
  "missing", "failed", "not connected" or "no key". Say what is ready, then what
  could be added later as an optional extra.
- **No tables of tools, no jargon.** One or two short sentences beat a table.
  Never name a tool the person doesn't need.
- **One ask at a time,** with the exact words or the exact click they need.
- **Encouraging and forward-facing.** Every message ends with what happens next.

## How this system thinks

- **Angles, not ads.** A campaign is four to five hypotheses about why a specific person buys, each tested with two variants that differ on exactly one thing. The canvas, the files and the review are all organised by angle.
- **Their words, not ours.** Copy is arranged from the customer's own phrases in `avatars.md`. A pain several customers named outranks one the founder guessed.
- **The image model never draws a word.** It makes a text-free photograph. Everything a customer reads is an editable layer in Paper.
- **Paper is the deliverable.** Not a mirror of a render. If Paper is not connected, the build stops and says so.
- **Never show a subpar ad.** `preflight.js` measures every artboard straight out of Paper (overlaps, clipped text, dead crops, type under the floor, safe zones, the 9:16 rail, empty bands) and the build is not finished until it reports zero failures. Eyes are for what it cannot measure: a cut-off head, a figure that blends in, a line that reads wrong.
- **The brand learns.** Verdicts become `intelligence/learnings.md`: Rules that are never broken, Defaults that are strong preferences, angles marked validated or killed.
- Claude does the judgment (angles, copy, layout, art direction). Scripts do the mechanical work and checks. Don't script the judgment.

## Repository map

- `.claude/skills/brand/`: point it at a URL, get a brand brain. **Run this first.** It also runs a short tool check (Paper, Firecrawl, Apify) and asks the setup questions (what you sell, whose ad account and link, own brand or client or practice). Photos default to Paper. It scaffolds every folder.
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

Best tool first, fallback always, the person told once and kindly. Tools can be connected directly or through Composio; check both before calling anything missing. The cheap way to check each tool, the Composio check and the connect lines are in `.claude/skills/brand/references/tools.md`. Only Paper is required.

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
- Chat is plain language, written for someone who has barely used AI (see **Who this is for**). No step codes, no schema names, no file names unless the person needs to open one. Explain any term of art the first time it appears (an angle is one reason a specific person buys; a variant changes one thing; a plate is the photo with no words on it). Every step closes with a short summary plus what the person does next.
