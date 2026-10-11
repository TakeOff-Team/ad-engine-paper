# Tools

The skills use the best tool available for each job, and never stop because a
nice-to-have is missing. Only Paper is required. Everything else has a fallback.

**Keep the tool check small.** An everyday person should see three tools, not
seven. `/brand` shows only these, at the start of a brand's setup:

| Shown | Why | If it is missing |
|---|---|---|
| **Paper Desktop**, connected to Claude | Builds every ad as editable layers, and makes the photos with its built-in image generation | Required. Setup carries on; the build stops and says how to connect it |
| **Firecrawl** (optional) | Reads the brand's website cleanly | Claude's built-in web fetch. JS-heavy sites may come back thin |
| **Apify** (optional) | Pulls competitor ads from the Meta Ad Library for `/ad-scout` | A browser connector screenshots the Ad Library, then the manual route. Dozens of ads instead of hundreds |

Then one sentence: "Photos are made with Paper's built-in image generation. If
you'd ever rather use Higgsfield or fal, just say so."

**Used quietly, never shown.** These make the output better when they happen to
be connected, but listing them overwhelms people, so the skills check them
silently, use them when present, and fall back without comment:

| Job | Used when present | Fallback |
|---|---|---|
| Exact colours, fonts and logo | **Claude in Chrome** (reads the live page) | Parse the page's HTML and CSS; flag colours and fonts for checking |
| Research (reviews, competitors, the customer's words) | **Perplexity** (sourced answers, deep research) | Claude's built-in web search, several targeted queries, sources cited |

**Only on request.** **Higgsfield** and **fal** are alternative image tools. They
are not checked or mentioned beyond the one sentence above. When the person asks
to switch, follow the switching section of `setup.md`.

Record every check in `intelligence/setup.json` under `tools`. Later skills read
that record instead of asking again, and re-check only a tool they are about to
use.

## How to check, without spending

- **Paper:** list files, or open the brand's file.
- **Firecrawl, Apify, Perplexity, Claude in Chrome:** the tool appears in this session's tool list. Do not call a paid tool just to check it.
- **Higgsfield** (only after a switch): a balance call. **fal** (only after a switch): `FAL_KEY` is present in `.env`.

## How to tell the person

Once, during `/brand`: three lines for Paper, Firecrawl and Apify (connected or
not, what a missing one would add, the line to connect it), then the image-tool
sentence. Then carry on. Never block on an optional tool, never ask twice, and
never pretend a fallback was the best tool. If a result came from a fallback,
say so where it matters ("colours read from the HTML, not the live page: check
them").

## Connect lines

```bash
claude mcp add --transport http -s user firecrawl https://mcp.firecrawl.dev/YOUR_FIRECRAWL_KEY/v2/mcp
claude mcp add --transport http -s user apify https://mcp.apify.com
```

Higgsfield, Perplexity and Claude in Chrome connect through Claude's own
connector settings. Paper connects through Paper Desktop (see its docs). Restart
Claude after adding any of them.
