# Agent Documentation

This folder contains detailed documentation that Claude can reference for specific tasks.

## How to Use

When asking Claude to work on a specific area, reference the relevant doc:
- "Read agent-docs/api-patterns.md before implementing the new endpoint"
- "Follow the conventions in agent-docs/python3-migration.md"

## Suggested Documents

Consider creating docs for:
- **toggl-api.md** - Toggl API documentation, rate limits, authentication
- **python3-migration.md** - Migration checklist, compatibility notes
- **csv-format.md** - Expected CSV output format, column definitions
- **time-rounding.md** - Business rules for time rounding and alignment
- **container-setup.md** - Containerfile details, Python 2.7 dependency pins, SELinux notes

## Tips

- Keep each doc focused on one topic
- Include concrete examples, not just abstract rules
- Update docs when patterns change
- Reference these docs in CLAUDE.md when relevant
