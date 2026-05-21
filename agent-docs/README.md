# Agent Documentation

This folder contains detailed documentation that Claude can reference for specific tasks.

## How to Use

When asking Claude to work on a specific area, reference the relevant doc:
- "Read agent-docs/api-patterns.md before implementing the new endpoint"
- "Follow the conventions in agent-docs/python3-migration.md"

## Documents

- **[toggl-api.md](toggl-api.md)** - Toggl API authentication, endpoints, pagination, rate limits
- **[python3-migration.md](python3-migration.md)** - What changed in the Python 3 migration, known issues
- **[csv-format.md](csv-format.md)** - CSV output format, column definitions, filename conventions
- **[time-rounding.md](time-rounding.md)** - Business rules for ALIGN_TIME and ROUNDUP settings

## Tips

- Keep each doc focused on one topic
- Include concrete examples, not just abstract rules
- Update docs when patterns change
- Reference these docs in CLAUDE.md when relevant
