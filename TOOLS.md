# Tools

The skills use the best tool available for each job, and never stop because a
nice-to-have is missing. Only Paper is required. Everything else has a fallback,
and the person is told once, in plain words, what they are missing and what it
would get them.

`/brand` checks every tool below at the start of a brand's setup, prints one
table, and records the result in `intelligence/setup.json` under `tools`. Later
skills read that record instead of asking again, and re-check only a tool they
are about to use.

| Job | Best tool | If it is missing | What the person loses |
|---|---|---|---|
| Building the ads | **Paper Desktop**, connected to Claude | Nothing. The build stops and says how to connect it | Everything. Required |
| Making the photograph | **Paper's own image generation**, **Higgsfield**, or **fal**: chosen per brand | Formats with no photo still build. A brand with no image tool gets type, proof and real-photo ads only | Generated scenes and product shots |
| Reading the brand's site | **Firecrawl** (clean page content, screenshots, branding) | Claude's built-in web fetch, then pasted text | Some pages render poorly without it; JS-heavy sites may come back thin |
| Exact colours, fonts and logo | **Claude in Chrome** (reads the live page) | Parse the page's HTML and CSS, then ask for a screenshot of the palette | Exactness. Colours and fonts are best-guess and flagged for checking |
| Research (reviews, competitors, the customer's words) | **Perplexity** (sourced answers, deep research) | Claude's built-in web search, several targeted queries, sources cited | Speed and breadth. The research is still done, just with more queries |
| Competitor ads at scale | **Apify** (Meta Ad Library scraper) | A browser connector, screenshots per advertiser, then the manual Ad Library route | Volume. Dozens of ads instead of hundreds |

## How to check, without spending

- **Paper:** list files, or open the brand's file.
- **Higgsfield:** a balance call.
- **fal:** `FAL_KEY` is present in `.env`.
- **Paper image generation:** Paper is connected and the person says which plan they are on (Free: limited; Pro: 100x more per week).
- **Firecrawl, Perplexity, Apify, Claude in Chrome:** the tool appears in this session's tool list. Do not call a paid tool just to check it.

## How to tell the person

Once, during `/brand`, as a short table: what is connected, what is not, what
each missing one would add, and the one line to connect it. Then carry on with
the fallbacks. Never block on an optional tool, never ask twice, and never
pretend a fallback was the best tool. If a result came from a fallback, say so
where it matters ("colours read from the HTML, not the live page: check them").

## Connect lines

```bash
claude mcp add --transport http -s user firecrawl https://mcp.firecrawl.dev/YOUR_FIRECRAWL_KEY/v2/mcp
claude mcp add --transport http -s user apify https://mcp.apify.com
```

Higgsfield, Perplexity and Claude in Chrome connect through Claude's own
connector settings. Paper connects through Paper Desktop (see its docs). Restart
Claude after adding any of them.
