# Ad Engine: Paper

Two skills that remake ads you like for your brand, built in Paper: `/brand` (once per brand) and `/paper-ads` (drop in reference ads; it remakes each one, every word editable, measured before delivery).

The system's rules, tools and conventions live with the skills so they travel together:

- `.claude/skills/brand/references/system.md`: who this is for, how the system thinks, and its guardrails. Read it once per session.
- `.claude/skills/brand/references/tools.md`: the tools, how to check them (directly or through Composio), and the fallbacks.
- `.claude/skills/brand/references/conventions.md`: folder layout, naming and ids.

Brands live in `brands/<brand>/`, created by `/brand`. (In a project that already keeps clients in `04-Brand/clients/`, they go there instead.)

Assume the person has barely used AI. Plain language, one ask at a time, fix what you can instead of flagging it, and close every step with what happens next.
