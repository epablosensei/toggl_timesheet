# Python 3 Migration Notes

Migration completed May 2026 on branch `feature/python3-migration`. The codebase is now Python 3 only — no Python 2 compatibility is maintained.

## What changed

### Syntax
- `print` statements → `print()` functions
- `u''` unicode string prefixes removed (all strings are unicode in Python 3)
- `%`-format and `.format()` strings → f-strings throughout
- `class Foo(object):` → `class Foo:`

### Dependencies
- `requirements.txt` stripped back to direct dependencies only (`requests`, `dataset`, `python-dateutil`)
- Removed `six` (Python 2/3 compatibility shim — no longer needed)
- Removed all pinned transitive dependencies
- `virtualenv` → standard `python3 -m venv`

### API
- `urllib` → `requests` (was already partially migrated; completed)
- `TogglAPI` class (used Toggl v8 API) removed — it was dead code and v8 is being deprecated by Toggl
- `ReportAPI` kept and fixed — was already using the correct v2 endpoint
- Fixed `db.query()` calls broken by `dataset` 2.0 API change (positional dict arg → keyword args)

### Bug fixes made during migration
- `self.worksheet_id` typo fixed to `self.workspace_id` in `api.py` — workspace fallback was silently broken
- `print(self.stop)` debug statement removed from `align_stop()` in `toggltime.py` — was spamming output for entries ending :45–:59

### New functionality
- `roundup()` method implemented properly — was an unimplemented stub in Python 2 (see `agent-docs/time-rounding.md`)
- `-f` (full mode) now aggregates by day — was outputting one row per entry previously
- Proper error handling added to API calls: timeouts, 401, 429, generic HTTP errors
- Type hints added across all modules; mypy and pyright clean

## What was NOT changed

- `ALIGN_TIME` logic in `align_start()` and `align_stop()` — identical to Python 2
- CSV output format and column structure
- Reports API v2 endpoints — confirmed working, no changes needed
- Overall architecture and flow

## Known remaining issues

- **CHORE-004:** `dataset` has no type stubs — Pylance flags all `db.query()` row access. Options: write a stub, switch to a typed ORM, or suppress per-file. Currently suppressed via `.vscode/settings.json` (`typeCheckingMode: basic`).
- **TASK-010:** Toggl Reports API v3 is coming but not yet documented. Currently on v2 which is confirmed working.
