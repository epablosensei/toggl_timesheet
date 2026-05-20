# Sprint Backlog

## Current Sprint
Started: 2026-01-21
Goal: Full Python 3 Migration (clean port — no Python 2 compatibility maintained)

## In Progress
- **[TASK-002]** Fix all Python 2 syntax across all files

## Backlog (Prioritized)

### Python 3 Migration
- [ ] **[TASK-002]** Fix all Python 2 syntax across all files
  - Print statements → `print()` in timesheet.py, togglapi/api.py, toggltime/timelib.py
  - `except X, e:` → `except X as e:` in timesheet.py
  - `e.message` → `str(e)` in timesheet.py
  - `from urllib import urlencode` → `from urllib.parse import urlencode` in togglapi/api.py

- [ ] **[TASK-003]** Update requirements.txt for Python 3
  - Update dataset, SQLAlchemy, alembic to current versions
  - Remove `six` (Python 2/3 bridge, not needed in Python 3)
  - Verify all dependencies install and work under Python 3

- [ ] **[TASK-004]** Verify Toggl API compatibility
  - Confirm Reports API v2 (`api.track.toggl.com/reports/api/v2`) still responds
  - TogglAPI class uses deprecated v8 (`www.toggl.com/api/v8`) — assess if used and whether to update to v9 or remove
  - Update API endpoints if needed

### Code Quality
- [ ] **[TASK-005]** Add proper error handling for API failures
- [ ] **[TASK-006]** Add unit tests for core functionality
- [ ] **[TASK-007]** Add type hints (after Python 3 migration)

### Features
- [ ] **[TASK-008]** Review and integrate `--full` aggregation fix
  - Branch: kat/full-aggregation
  - Notes: Aggregates entries by day (GROUP BY user, start with MIN/MAX/SUM) instead of listing each entry individually; currently used in production by Kat; conflicts with upstream approach — decision needed

- [ ] **[TASK-009]** Consider adding XLS export option
  - Branch exists: feature/xls_print

## Completed
- [x] **[CHORE-001]** Add Claude Code configuration
  - Completed: 2026-01-21
  - Branch: claudify-repo

- [x] **[TASK-001]** Complete roundup function implementation
  - Completed: 2026-05-20
  - Branch: feature/python3-migration

## Blocked
<!-- Tasks waiting on external dependencies -->
