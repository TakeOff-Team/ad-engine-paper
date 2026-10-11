# Tools

The skills use the best tool available for each job, and never stop because a
nice-to-have is missing. Only Paper is required. Everything else has a fallback.

**Keep the tool check small.** An everyday person should see two tools, not
seven. `/brand` mentions only these, at the start of a brand's setup:

| Shown | Why | If it is missing |
|---|---|---|
| **Paper Desktop**, connected to Claude | Builds every ad as editable layers, and makes the photos with its built-in image generation | Required. Setup carries on; the build stops and says how to connect it |
| **Firecrawl** (optional) | Reads the brand's website cleanly | Claude's built-in web fetch. JS-heavy sites may come back thin |

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

- **Paper:** list files. If Paper is connected but no file is open, don't warn:
  create the brand's file (`create_file`, named `ad-engine · {Brand}`), open it
  (`open_file`), record its id as `paper_file_id`, and say "I opened a Paper file
  for {Brand}." If Paper isn't connected at all, give the person the two steps
  in plain words (open Paper Desktop, turn on its Claude connection) and keep
  going with everything that doesn't need it.
- **Firecrawl, Perplexity, Claude in Chrome:** a tool counts as connected
  if **either** route has it:
  1. **Directly:** the tool appears in this session's tool list.
  2. **Through Composio:** many people connect apps through Composio instead. If
     any Composio tool is in this session (names containing `COMPOSIO`), run
     `COMPOSIO_SEARCH_TOOLS` with one query per app ("scrape a web page with
     firecrawl"). It's free, and its connection status
     says which toolkits have an active connection.
  Never report a tool as missing until both routes are checked. When a tool is
  connected only through Composio, use it through Composio
  (`COMPOSIO_MULTI_EXECUTE_TOOL`) for the whole run. Do not call a paid tool
  just to check it.
- **Higgsfield** (only after a switch): a balance call. **fal** (only after a switch): `FAL_KEY` is present in `.env`.

## How to tell the person

Once, during `/brand`, in two or three friendly sentences. No table, no ✅ ⚠️ ❌,
no "missing", "not connected" or "no key". Lead with what's ready, then name any
optional extra as something they *could* add later, with what it would get them.
For example:

> "You're all set: Paper is open and ready, and it'll make the photos too.
> Firecrawl isn't connected, which is fine. It's an optional extra that reads
> your site a bit more cleanly, if you ever want it."

Never mention Perplexity, Claude in Chrome, Higgsfield or fal here, except the
one line that they can switch photos to Higgsfield or fal whenever they like.
Connect lines are given only if the person asks how to add an extra. Then carry on. Never block on an optional tool, never ask twice, and
never pretend a fallback was the best tool. If a result came from a fallback,
say so where it matters ("colours read from the HTML, not the live page: check
them").

## Connect lines

```bash
claude mcp add --transport http -s user firecrawl https://mcp.firecrawl.dev/YOUR_FIRECRAWL_KEY/v2/mcp
```

Higgsfield, Perplexity and Claude in Chrome connect through Claude's own
connector settings. Paper connects through Paper Desktop (see its docs). Restart
Claude after adding any of them.
