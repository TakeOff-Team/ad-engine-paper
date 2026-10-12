# Ad Engine: Paper, system rules

Read once per session by `/paper-ads-prep`, `/competitor-ads-intel` and `/paper-ads`.

Drop in ads you like and get them remade for your brand: on-brand, grounded in the brand's real facts and offers, built in Paper so every word stays editable. `/paper-ads-prep` gets the brand ready once; `/competitor-ads-intel` puts every image ad the brand's competitors run onto the Paper canvas so the person can pick; `/paper-ads` remakes each reference ad as a text-free photo plus independently editable text and UI, in 4:5 and 9:16, one row per reference on the canvas.

It is not much of a codebase on purpose. The skills are the product; the brand's own files are the substrate they read.

## Modularity

**Each skill describes itself. Nothing outside a skill keeps a list of skills.**

- Every skill's `SKILL.md` frontmatter declares its `outputs:` and `inboxes:` (folders under `brands/<brand>/generation/`), `requires:` (hard needs), `optional:` (soft needs it degrades without), and a `version:`. Scaffolding, validation and the docs tables all derive from these declarations.
- **Skills create their own folders on first use** (`mkdir -p` for each declared path). `/paper-ads-prep`'s scaffold is a convenience, not a prerequisite.
- Everything reads the brand intelligence `/paper-ads-prep` writes. The shapes of the `intelligence/` files are the system's internal API; change them only deliberately.
- `python3 .claude/skills/paper-ads-prep/brand.py --validate` checks every declaration; `--docs` regenerates the skill tables between markers in `README.md` and this file.

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

- **Remake what already works.** The person brings ads they like; picking them takes human taste, so the system never picks for them. Each remake keeps the reference's format and its idea, and rewrites every word for the brand from its real facts. We are not an ad agency: no angle strategy, no media plan, no research the person didn't ask for.
- **Simple on purpose.** Three skills, run in order. Every extra question or step has to earn its place for someone who has barely used AI.
- **The image model never draws a word.** It makes a text-free photograph. Everything a customer reads is an editable layer in Paper.
- **Paper is the deliverable.** Not a mirror of a render. If Paper is not connected, the build stops and says so.
- **Never show a subpar ad.** `preflight.js` measures every artboard straight out of Paper (overlaps, clipped text, dead crops, type under the floor, safe zones, the 9:16 rail, empty bands) and the build is not finished until it reports zero failures. Eyes are for what it cannot measure: a cut-off head, a figure that blends in, a line that reads wrong.
- **The brand learns.** Feedback becomes `intelligence/learnings.md`: Rules that are never broken, Defaults that are strong preferences.
- Claude does the judgment (copy, layout, art direction). Scripts do the mechanical work and checks. Don't script the judgment.

## Repository map

- `.claude/skills/paper-ads-prep/`: gets the brand ready. **Run this first.** It takes stock of what the project already knows, checks the ad-critical inputs, fills gaps from the site and the web, and asks only for what's missing. Photos default to Paper. It scaffolds every folder.
- `.claude/skills/competitor-ads-intel/`: finds the top competitors, confirms them, pulls their image ads with Apify, and lays them out in Paper, one page per competitor.
- `.claude/skills/paper-ads/`: drop in ads you like and it remakes them, in Paper, and `preflight.js`, the measuring script. Conventions for all skills in `.claude/skills/paper-ads-prep/references/conventions.md`.

<!-- skills-table:start -->
| | |
|---|---|
| **`/paper-ads-prep`** | Gets your brand ready for /paper-ads: checks what it already knows, fills the gaps, asks only for what's missing. Run this first |
| **`/competitor-ads-intel`** | Finds your competitors, pulls every image ad they run into Paper, one page each, so you can pick the ones worth remaking |
| **`/paper-ads`** | Drop in ads you like; it remakes each one for your brand in Paper, every word editable, in 4:5 and 9:16, measured before delivery |
<!-- skills-table:end -->

- The brand folder (`04-Brand/clients/[brand]/` in a vault that has one, otherwise `brands/[brand]/`): the context substrate: `intelligence/` (identity, strategy, customers, commercial files, setup, learnings) and `generation/` (versioned outputs). Created by `/paper-ads-prep`, never by hand. See `brands/README.md`.

## Generation

The brand's **prompt modifier** (`visual-guidelines.md`) opens every image prompt and is what makes a plate look like the brand rather than like stock AI. The image tool is the brand's choice, recorded in `intelligence/setup.json`: Paper's own image generation, Higgsfield through its connector, or fal through `FAL_KEY`. All three cost money, credits or plan usage. The build states the exact cost and gets explicit approval before any paid call. A format with no photograph in it generates nothing and costs nothing.

## Tools

Best tool first, fallback always, the person told once and kindly. Tools can be connected directly or through Composio; check both before calling anything missing. The cheap way to check each tool, the Composio check and the connect lines are in `.claude/skills/paper-ads-prep/references/tools.md`. Only Paper is required.

## Guardrails (non-negotiable)

1. **Nothing is spent without an explicit yes.** Show the cost before the first paid call, for fal dollars, Higgsfield credits and Paper generations alike, and for Apify pulls (say the number; ask when it's over a dollar). 
2. Offers come from `intelligence/offers.md` by ID; claims must be supportable by `brands/[brand]/intelligence/` content. Compliance rules in `brand-voice.md` are hard constraints, and no style or conversion rule may harden a health claim past what `intelligence/` supports. Truth outranks voice, which outranks everything else.
3. A reference ad contributes its format and its idea. Every word is rewritten for the brand; never another brand's name, product, claims, people, likeness or distinctive lines.
4. No em dashes in any line a customer reads.
5. No fabricated people, quotes, reviews, screenshots or dashboards. Proof is real or it is absent.
6. **No claim of a check that did not run.** "Nothing failed" and "fonts rendered" are quotes of a measurement or they are not said.
7. **Nothing written to the brand's files without saying so.** Offers, copy and specs change only on the person's word, and a request to "try another version" is answered with a proposal, not a build.


## Starting state

- **First move: `/paper-ads-prep <url>`.**
- **Then `/competitor-ads-intel`:** their competitors' ads land in Paper; the person says the numbers they like. (Already have ads they love? They can paste them in and skip this.)
- **Then `/paper-ads`.** Every new batch after that is `/competitor-ads-intel` (or ads they found) and `/paper-ads`.
- Chat is plain language, written for someone who has barely used AI (see **Who this is for**). No step codes, no schema names, no file names unless the person needs to open one. Explain any term of art the first time it appears (a reference is an ad you want remade; a plate is the photo with no words on it). Every step closes with a short summary plus what the person does next.
