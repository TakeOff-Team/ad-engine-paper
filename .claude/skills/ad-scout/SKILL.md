---
name: ad-scout
description: "Optional. Finds reference ads when the person has none, or wants more: pulls what the brand's competitors and category are running on Meta right now, shows them as a numbered sheet, and files the ones the person picks into the reference inbox for /paper-ads. Always asks first, because someone who already has references they love does not need it."
group: Ads
summary: Optional. Pulls the ads running in your category and files the ones you pick as references
version: 1.0.0
outputs: [ad-scout]
requires: []
optional: [Apify connector for pulling ads at scale, a browser connector as the fallback]
---

# Ad research: find the references, when there are none

The build skill recreates a winning ad format with the brand's own product and
words. That needs formats to model. Some people arrive with a folder of ads they
love. Others have nothing. This skill is for the second group, and for anyone
who wants to see the category before choosing.

It produces **evidence and options, never decisions.** The person picks.

Create this skill's declared output folder before use. A pull lives at
`brands/<brand>/generation/ad-scout/<YYYY-MM-DD>/`.

## Ask first. This is the whole point of the skill being optional

Before pulling anything, ask one question, in plain words:

> "Do you already have ads you'd like to model? If you do, drop them into the
> references folder and we can skip this. If you don't, or you want to see what's
> working in your category first, I can pull what your competitors are running
> right now. It costs a few cents and takes a couple of minutes."

- **They have references:** confirm they are in
  `generation/paper-ads/ad-references/`, say how many are there, and stop.
  Pulling competitor ads on top of references the person already loves is
  wasted time.
- **They have none, or want both:** continue.

## Who to pull

Competitor names come from `intelligence/brand-strategy.md` (Competitive
landscape). If it names fewer than two, pull the category keyword first, list the
five advertisers that appear most, and ask which are real competitors.

Two rules that prevent bad data:

1. The brand's **own** ad presence is read from its Page transparency line in the
   Ad Library, never from a keyword search on the brand name, which matches ad
   copy and returns noise.
2. Named competitors are pulled by **Facebook page URL**, never by searching
   their name.

## Pull

**With the Apify connector (preferred):** the Meta Ad Library scraper, about
60 to 100 active ads per named advertiser, plus one category keyword run of 100.

State the cost before the run: roughly a tenth of a cent per ad, so three
competitors and a category run is about a quarter. Under a dollar: say the
number and go. Over a dollar: ask.

After the run, read the actual charge off the run and write it in `findings.md`; the estimate and the chat and the file must say the same number.

Download every creative into `ads/{advertiser}/` straight away (the image links
expire) and keep `ads.json` with the advertiser, start date, copy, landing page
and platform mix.

**Without Apify:** load each advertiser's Ad Library page in a browser connector,
screenshot the grid and one or two ad details per advertiser. Say in the findings
that the sample is thin.

**Neither available:** say so once, with what Apify would add (hundreds of ads
instead of a few screenshots) and its connect line from `TOOLS.md`, then and give the person the manual route in one line:
open the Meta Ad Library, search the competitor's page, screenshot the ads they
like, drop them into the references folder.

## Show it

```bash
python3 .claude/skills/paper-ads/contact-sheet.py brands/[brand]/generation/ad-scout/[date]/ads
```

That writes one numbered sheet of every creative and an `index.md` mapping
numbers to files. Show the sheet. Statics only matter here; skip video frames.

## Read the evidence

Write `findings.md` with what the ads show, each claim pointing at numbered
examples:

- product-forward or lifestyle; text on the image or caption only;
- which formats dominate, and which nobody runs (white space);
- what the copy leans on: guarantees, prices, reviews, ingredients, founders;
- an **offer gap**, if the category leads with a guarantee or a discount the
  brand does not have in `offers.md`. One line for the person; `/ad-angles` reads
  it and never invents the missing offer;
- three to five format directions worth modelling, by number.

A category with no designed statics is white space to test into, not a
prohibition. When two styles both survive, recommend testing both rather than
picking.

## Let them pick, then file the picks

Ask: *"Which of these would you like to model? Give me the numbers. Five to ten
is plenty."* Recommend a spread across your format directions, and say why in a
line each.

Copy the picked files into `generation/paper-ads/ad-references/`, renamed
`ref-01-{advertiser}-{format}.png` and so on. Record in `findings.md` which were
picked.

**A reference contributes format and structure only.** Never another brand's
copy, product, or likeness. Say this once when filing them.

## Hand off

Three lines: how many ads were pulled from whom and what it cost, the two or
three things the category leans on, how many references are now in the inbox.
Then the next step: `/ad-angles`.

Refresh monthly at most. This is a baseline, not a live feed.
