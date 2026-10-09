---
name: ad-angles
description: "The thinking before the building. Turns the brand's avatars, their own words, the offers and the chosen reference formats into a campaign: four to five angles, two variants each, the on-image copy for every variant slot by slot, a claims ledger that traces every number, and the Meta ad text (primary texts, headlines, descriptions, button) per angle. Run after /brand and before /paper-ads. Also rewrites specific variants from a review note."
group: Ads
summary: Angles, on-image copy and Meta ad text in the customer's own words, every claim traced. Run before building
version: 1.0.0
outputs: [ad-angles]
requires: []
optional: [generation/ad-scout findings for category patterns, intelligence/learnings.md from earlier reviews]
---

# Ad copy: think like the reader, say their pain better than they can

> All copywriting is thinking like the other person and expressing their pains
> better than they can, so well and so articulately that they assume you have the
> answer.

Everything below is that sentence made mechanical. The reader never sees a
"concept". They see eight words in a feed and decide in under a second whether
those words are about them. This pass exists so every variant's words are about
them, and so nothing is built in Paper until the words are right.

Read `references/copy-digest.md` once before writing (awareness stages,
headline formulas and why they fail, pain quantification, the So-What chain,
testimonials, CTAs, AI tells).

Create this skill's declared output folder before use. A campaign lives at
`brands/<brand>/generation/ad-angles/<campaign>/` (lowercase, hyphens, for example
`autumn-launch`).

## Inputs (read all, in this order)

| File | What you take from it |
|---|---|
| `intelligence/avatars.md` | **The bank. Read it first.** The named people, their verbatim pain words, wants, objections with rebuttals, emotional driver. The headline's words come from here. A pain marked as inferred is a hypothesis, and gets at most one variant |
| `intelligence/offers.md` | The closed list of offers, by ID, with stacking rules and the avatar-to-offer heuristic. No offer exists outside this file |
| `intelligence/products.json` | Real names, prices, and each product's `claims`. With `offers.md`, the only source of numbers |
| `intelligence/brand-voice.md` | How the brand writes, and its compliance rules, which are hard constraints |
| `intelligence/counter-positioning.md` | What the brand stands against: the source of contrarian and enemy angles |
| `intelligence/learnings.md` (if present) | Rules never to break, Defaults to follow, and which angles were validated or killed and why. **Check every reference you assign against the Rules**: a format that needs a dark ground, a generated person or a dashboard is unusable for a brand whose Rules forbid them, however good the format |
| `intelligence/setup.json` | `advertiser` and `landing_url`: whose account runs the ads and where they send people. The ad text's display link and URL come from here, never from the website's own CTA |
| `generation/ad-scout/*/findings.md` (if present) | What the category runs and leans on, and any offer gap. Shape only; never a line |
| `generation/paper-ads/ad-references/` | The formats available. **Look at every reference** and list its text primitives (headline, rating line, three callouts, testimonial card, badge, legal). The copy has to fill those slots, so the slots have to be known first |

If `avatars.md` carries no real customer quotes, say so at the top of `copy.md`
and flag every headline `derived, not customer language`. Never present invented
phrasing as the customer's.

**If the customer language is thin** (few real quotes in `avatars.md`), do one
round of research before proposing angles: reviews, Reddit and forum threads,
comments on the brand's and competitors' posts. Use Perplexity if it is
connected, otherwise Claude's built-in web search with several narrow queries.
Quote what you find verbatim with its source, and say which tool you used.

## Step 1. Angles, then variants

A campaign is **angles times variants**, not a pile of ads.

- An **angle** is one hypothesis about why this person buys: avatar, the pain or
  desire, the awareness stage, and an angle type (contrarian, mechanism,
  transformation, enemy, specificity, social proof). Name it, and write one line
  on why it should work.
- A **variant** keeps the angle and changes **exactly one** thing: the headline,
  or the reference format. Two variants that differ on two axes teach nothing.
  A format test keeps the same set of copy slots (if v1 carries a CTA and a
  guarantee, v2's format must too, or the test is also a copy test). Pick the
  second reference accordingly.

Defaults: **four to five angles, two variants each.** `learnings.md` Defaults
override. Ids are `a1-v1`, `a1-v2`, `a2-v1`. Angles are numbered in the order
they appear in `angles.md`, and stay in that order.

**When the person asks for more angles, push back once before agreeing.** Say
the three costs in one line each: more angles lean on the same few photos and
proof points, so the extra ones get thinner; two angles end up testing the same
thing with different words; and a review of forty artboards gets skimmed. Offer
the alternative: a second campaign after the first one has verdicts, seeded by
what won. If they still want more, build it, and apply the approval gate to the
added angles exactly as to the first five.

- Start from angles `learnings.md` marks validated; add at most two new
  hypotheses; never re-run a killed angle without a new reason.
- First campaign for a brand: all angles are fresh. Spread them across at least
  two avatars and across awareness stages, with at least one angle at each end
  (unaware or problem-aware, and product-aware or most-aware) unless the traffic
  is known to be cold, in which case a product-aware headline must also
  introduce the product.
- **One wildcard.** One variant in the campaign deliberately breaks a Default: a
  format, a register, or an angle the brand has never run. It may never break a
  Rule. Label it. A kept wildcard is the only way the system learns its defaults
  have drifted.
- **Assign each variant a reference format** from `ad-references/`. Match the
  format to the argument: a proof angle wants a format with a rating or a
  testimonial card; an offer angle wants a format with a price or badge; a pain
  angle wants a headline-led format. An angle that needs proof the brand does not
  have is dropped, not faked.
- Not enough references for the campaign: say how many more would help and what
  kind, and offer `/ad-scout`.

Write `angles.md`: per angle, the id, name, why it works, avatar, stage, type,
status (`proposed`), and the variant plan (`v1: headline A on ref-03 · v2:
headline B on ref-03`, or `v1 on ref-03 · v2 on ref-07`).

**Show the angle plan and get a yes before writing copy.** Five lines, plain
language. This is the cheapest moment to change direction. The gate applies
every time angles are added, including "come up with five more": the new five
are shown as a plan first, not written straight into copy.

## Step 2. The method, per variant

**1. Stand where they stand.** One line: who is reading this, at what moment, in
what mood. A person, not a persona label.

**2. Their pain, in their words.** Quote the pain words from `avatars.md` closest
to this angle, verbatim. For a most-aware or offer angle, take the objection
instead: the headline answers the doubt they actually raised.

**3. Their pain, said better than they can.** Run the So-What chain from the
feature down to the thing they feel or lose. Quantify it when `products.json` or
`offers.md` allows; make it a scene when they do not. This line is the seed of
the headline, not the offer.

**4. Pick the awareness stage.** It decides which headline formula is eligible
(digest, Awareness).

**5. Write the on-image copy, slot by slot, for the assigned format.**
- **Headline plus two alternates**, three to nine words, each from a different
  formula at the chosen stage. The first is the pick.
- **Subhead**, one line: the product named and the outcome, in plain words.
- **Every other primitive the format has**, in the reference's order: rating
  line, callouts, card text, badge, price, button, legal. Each one real.
- **CTA** describes the benefit, two to five words, **and passes the stranger
  test on its own**: someone who has never seen the site must know what
  happens when they tap. The site's own jargon ("Build my AI Operating System")
  is a brand phrase, not a CTA, however often the site uses it. Plain beats
  clever here. If `offers.md` carries a jargon CTA, propose plain wording in the
  angle plan and let the person choose.
- **A 9:16 cut.** The tall frame holds less. Mark which lines survive in 9:16:
  the hook, the offer and one proof point. Cut supporting copy before shrinking
  type.

**6. The three cold-reader questions.** For someone who has never heard of the
brand: what is this, who is it for, why care now. The ad as a whole answers the
first and at least one of the others. Usually the subhead carries "what is
this". Skipping it is allowed on purpose (warm traffic, the product is visibly
the thing being sold, a pure brand line) and the reason is written down. A
forgotten skip is the bug.

**7. No em dashes. Ever.** Not in a headline, subhead, button, card, caption or
ad text. Use a period, a comma, a colon or a new line. Ranges keep their dash
("3–5", "Jan–Aug"). Hyphens inside words are fine.

**8a. Named people.** A real customer, member or case study named in copy
needs the brand's permission to appear in paid ads. If `intelligence/` does not
record that permission for the name, ask once, in the angle plan, before the
name is used. Hold the name back until the answer; never ship it on a guess.

**8b. Quotes are claims too.** A testimonial that states an outcome ("my
recovery scores went up") is a health or results claim and obeys
`brand-voice.md` compliance exactly as the brand's own words would. A quote
that names a competitor, or a press mention ("GQ tested it"), is a flag that
needs the person's yes before it is built; on a client brand it is held until
then, on a practice brand it is flagged in the angle plan and may proceed.

**8c. No two angles may look like the same ad.** If two angles would share the
same packshot, the same ground and the same stack, change the photo or the
format on one of them before writing copy. Two lookalike ads muddy both tests.

**8. Claims ledger.** Every digit, percentage, timeframe, name and quote in the
copy maps to its source: a `products.json` claim, an `offers.md` ID, or a quoted
line in `avatars.md`. **No ledger entry, no claim.** A number that cannot be
traced is rewritten into something that can, or removed. Compliance rules in
`brand-voice.md` outrank everything, and no rule of style or conversion may
harden a health claim past what `intelligence/` supports.

**9. The cold read.** Write one line per variant: `Cold read: "what a stranger
would say this is selling, after two seconds"`. Vague is a flag: add the missing
context, or write the reason it is fine. Every pronoun needs a referent inside
the ad. Then read the headline aloud as the reader. Is it about me, or about
them? Would I say it to a friend about my own problem? Would a competitor's name
fit in it unchanged? Does it pass the AI-tells list?

## Step 3. Meta ad text, per angle

Meta takes several options each for primary text, headline and description and
mixes them per viewer, so every headline has to read correctly beside every
primary text. That is why this is written per angle, not per image.

For each angle:
- **Three to five primary texts**, in three shapes: one that lands in **40
  characters**, one at about **125** (the feed's "see more" line), one longer
  story or proof version.
- **Three to five headlines**, **40 characters max**, the strongest under **27**.
- **One or two descriptions**, **25 characters**. Support only.
- **One button** from Meta's fixed list, plus one alternate.
- **Display link** and the UTM template
  `utm_source=meta&utm_medium=paid&utm_campaign={campaign}&utm_content={angle}-{variant}`.

The display link and destination come from `setup.json` (`landing_url`, which
may be an affiliate or tracking link, never the raw site URL by assumption).
Write the character count beside every line. Run the pairing check: read each
headline against each primary text and fix any pair that repeats or contradicts.
Every line obeys the claims ledger and the em-dash rule.

## Campaign-level rules

- **Offers by ID only.** One primary offer per ad. Respect the stacking rules.
- **A risk reversal leads when the brand has one.** If research shows the
  category leads with a guarantee and `offers.md` has none, write one line at the
  top of `copy.md` for the person, and then write nothing that implies one.
- **Never lift a competitor's line, and never reuse a reference ad's copy.** A
  reference gives the shape; the words come from this brand's customers.
- **Never reword the brand's own homepage headline and call it an angle.** It can
  be an alternate, labelled `house line`.
- **Voice:** the brand's tone from `brand-voice.md`, the reader's vocabulary from
  `avatars.md`. When they conflict, the reader wins.

## Output, in `generation/ad-angles/<campaign>/`

`angles.md`, then `copy.md`:

```
# Copy: {brand} · {campaign} · {date}

Offer gap: {one line, or "none found"}
Customer language: {N quoted lines from avatars.md} | derived: none on file
Stage spread: unaware {n} · problem {n} · solution {n} · product {n} · most-aware {n}

## Angle a1 · {angle name} · {avatar} · {stage}

### a1-v1 · {reference file} · tests: {headline | format}
Reader:       {a person at a moment}
Their words:  "{quote}" (avatars.md, {avatar})
Said better:  {the articulated pain}
Headline:     {pick}          [{formula}]
  alt:        {…}             [{formula}]
  alt:        {…}             [{formula}]
Subhead:      {…}
Slots:        {every other primitive of the format, in order, verbatim}
CTA:          {…}
Offer:        {O-id, or none}
9:16 keeps:   {which lines survive in the tall frame}
Cold read:    "{…}"   {Context: where it is carried, or why it is skipped}
Claims:       "{claim}" → {source} · "{claim}" → {source}   {or: none}
```

Then `ad-unit.md` (one paste-ready block per angle, with character counts) and
`ad-unit.json` (`{angle_id: {primary_texts, headlines, descriptions, cta,
cta_alt, display_link, url}}`), which `/paper-ads` places on the canvas
as an editable text card at the end of each angle's row.

## Rewrite mode

Given variant ids and a note ("shorter", "more specific", "wrong stage"), rewrite
only those blocks, append `(rev N: {note})` to the block header, and keep the
ledger current. `/paper-ads` then updates the one layer in Paper.

## Hand off

Print, in plain language: the angles in one line each, the stage spread, any
offer gap, how many variants were written, any `derived` flags, and any claim
that had to be softened because it could not be traced (name it; the person may
have the source). Then the next step: `/paper-ads {campaign}`.
