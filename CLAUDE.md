# Ad Engine: Paper

Three skills, run in order, that remake proven ads for your brand in Paper: `/paper-ads-prep` (once per brand: checks what it knows, fills gaps, asks only for what's missing), `/competitor-ads-intel` (pulls competitors' image ads into Paper, one page each, for the person to pick from) and `/paper-ads` (remakes the picks, every word editable, measured before delivery).

The system's rules, tools and conventions live with the skills so they travel together:

- `.claude/skills/paper-ads-prep/references/system.md`: who this is for, how the system thinks, and its guardrails. Read it once per session.
- `.claude/skills/paper-ads-prep/references/tools.md`: the tools, how to check them (directly or through Composio), and the fallbacks.
- `.claude/skills/paper-ads-prep/references/conventions.md`: folder layout, naming and ids.

Brands live in `brands/<brand>/`, created by `/paper-ads-prep`. (In a project that already keeps clients in `04-Brand/clients/`, they go there instead.)

Assume the person has barely used AI. Plain language, one ask at a time, fix what you can instead of flagging it, and close every step with what happens next.
