# Ad Engine: Paper

Four skills that build on-brand static ads in Paper: `/brand` (once per brand), `/ad-scout` (optional references), `/ad-angles` (angles, copy, Meta ad text), `/paper-ads` (the build, measured before delivery).

The system's rules, tools and conventions live with the skills so they travel together:

- `.claude/skills/brand/references/system.md`: how the system thinks and its guardrails. Read it once per session.
- `.claude/skills/brand/references/tools.md`: the best tool for each job, the fallback when it's missing, and the connect lines.
- `.claude/skills/brand/references/conventions.md`: folder layout, naming and ids.

Brands live in `brands/<brand>/`, created by `/brand`. (In a project that already keeps clients in `04-Brand/clients/`, they go there instead.)

Chat is plain language. No step codes, no schema names, no file names unless the person needs to open one. Every step closes with a short summary plus what the person does next.
