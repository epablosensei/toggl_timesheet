# Sprint Backlog

## Current Sprint
Started: 2026-01-21
Goal: Full Python 3 Migration (clean port — no Python 2 compatibility maintained)

## Backlog (Prioritized)

### Type correctness
- [ ] **[TASK-011]** Fix type errors revealed by mypy
  - [ ] Guard `e.response` before accessing `.status_code` in HTTPError handler
  - [ ] Cast `ROUNDUP` / `ALIGN_TIME` CLI args to `int` (config expects `int`, getopt gives `str`)
  - [ ] Fix `get_detailed_report` signature to accept `datetime | str` (callers pass datetime)
  - [ ] Fix `print_csv` + `year_month_only` to accept `date | datetime` (called with `start.date()`)
  - [ ] Add `data_list` type annotation in `api.py`

### API
- [ ] **[TASK-010]** Migrate to Reports API v3 when available
  - Currently using Reports API v2 (`api.track.toggl.com/reports/api/v2`) — confirmed working
  - Toggl docs state v3 is coming but not yet fully documented
  - Toggl API v8 (used by old TogglAPI class) is being deprecated — already removed

## Completed

- [x] **[CHORE-001]** Add Claude Code configuration
  - Completed: 2026-01-21
  - Branch: claudify-repo

- [x] **[TASK-001]** Complete roundup function implementation
  - Completed: 2026-05-20
  - Branch: feature/python3-migration

- [x] **[TASK-002]** Fix all Python 2 syntax across all files
  - Completed: 2026-05-20
  - Branch: feature/python3-migration

- [x] **[TASK-003]** Update requirements.txt for Python 3
  - Completed: 2026-05-20
  - Branch: feature/python3-migration
  - Dropped all pinned transitive deps and `six`; only direct deps listed; verified end-to-end against live API

- [x] **[TASK-004]** Verify Toggl API compatibility
  - Completed: 2026-05-20
  - Branch: feature/python3-migration
  - Reports API v2 confirmed working (tested all three modes against live API)
  - TogglAPI class (v8) removed — was dead code; v8 is also being deprecated by Toggl
  - No endpoint changes needed; ReportAPI was already on the correct host
  - Fixed `db.query()` calls broken by dataset 2.0 API change (dict arg → kwargs)

- [x] **[TASK-008]** Integrate `-f` aggregation fix
  - Completed: 2026-05-20
  - Branch: feature/python3-migration
  - `-f` now outputs one row per day (MIN start, MAX stop, SUM duration) instead of one row per entry
  - Ported from kat/full-aggregation; `-p` per-user behaviour intentionally kept as-is

- [x] **[TASK-005]** Add proper error handling for API failures
  - Completed: 2026-05-20
  - Branch: feature/python3-migration
  - Added timeout and raise_for_status() to ReportAPI._query()
  - Specific messages for 401 (bad token) and 429 (rate limit)
  - Fixed broken DB rename logic; removed dead sys.exc_info() call

- [x] **[TASK-007]** Add type hints across all modules
  - Completed: 2026-05-20
  - Branch: feature/python3-migration

- [x] **[CHORE-002]** Repo audit and cleanup
  - Completed: 2026-05-20
  - Branch: feature/python3-migration
  - Removed: LICENSE.txt (duplicate), .idea/ (stale PyCharm config), Python 2 .pyc files
  - Updated: .gitignore (added __pycache__/, venv/, venv-py3/), README.md (Python 3 install instructions)

## Blocked
<!-- Tasks waiting on external dependencies -->
