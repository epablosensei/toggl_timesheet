# CLAUDE.md

## Project Overview

CLI tool to export Toggl time entries to CSV timesheets. Fetches time tracking data from the Toggl API and generates formatted CSV reports organized by client and project.

**Tech Stack:** Python 3
**Dependencies:** requests, dataset, SQLAlchemy, python-dateutil

## Commands

### Running the Tool
- `python timesheet.py` - Generate timesheet CSV for last month
- `python timesheet.py -s 2024-01-01 -e 2024-01-31` - Custom date range
- `python timesheet.py -p` - Generate per-project CSVs
- `python timesheet.py -f` - Export all entries to full.csv
- `python timesheet.py -m` - Export daily totals per user to monthly CSV
- `python timesheet.py -h` - Show help

### Development Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Quick Commands
- `pip install -r requirements.txt` - Install dependencies
- `source venv/bin/activate` - Activate virtual environment
- `deactivate` - Deactivate virtual environment

### Dangerous Commands (DO NOT run without explicit permission)
- `python timesheet.py` - Calls Toggl API (uses API quota)
- Any modifications to `config.py` - Contains API credentials

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     toggl_timesheet                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    ┌──────────────────┐                                         │
│    │   timesheet.py   │  CLI Entry Point                        │
│    │   (main)         │  - Parse args, orchestrate flow         │
│    └────────┬─────────┘                                         │
│             │                                                    │
│    ┌────────┴─────────┐                                         │
│    ▼                  ▼                                         │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │  togglapi/   │  │  toggltime/  │                             │
│  │  api.py      │  │  toggltime.py│                             │
│  │              │  │  timelib.py  │                             │
│  │              │  │              │                             │
│  │ - ReportAPI  │  │ - Toggletime │                             │
│  └──────┬───────┘  │ - Time utils │                             │
│         │          └──────┬───────┘                             │
│         │                 │                                      │
│         ▼                 ▼                                      │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐           │
│  │ Toggl API   │   │  SQLite DB  │   │  CSV Files  │           │
│  │ (external)  │   │  (data/*.db)│   │ (data/*.csv)│           │
│  └─────────────┘   └─────────────┘   └─────────────┘           │
│                                                                  │
│  Config: config.py (API token, workspace ID, timezone)          │
└─────────────────────────────────────────────────────────────────┘
```

### Key Modules

- **timesheet.py** - Main CLI, argument parsing, CSV generation
- **togglapi/api.py** - `ReportAPI` (detailed reports via Toggl Reports API v2)
- **toggltime/toggltime.py** - `Toggletime` class for time entry manipulation
- **toggltime/timelib.py** - Date/time utility functions
- **config.py** - User configuration (API token, workspace ID, timezone)

## Conventions

### Code Style
- Python 3 only — no Python 2 compatibility
- Follow existing patterns in codebase

### Commit Messages
Use Conventional Commits format:
- `feat:` new features
- `fix:` bug fixes
- `chore:` maintenance tasks
- `docs:` documentation changes
- `refactor:` code refactoring

## Protected Files

**DO NOT modify without explicit permission:**
- `config.py` - Contains API credentials
- `data/` directory - Output files, user data

## Notes

- Virtual environment: `venv/` (activate with `source venv/bin/activate`)
- `ALIGN_TIME` and `ROUNDUP` are independent settings with different effects — see `agent-docs/time-rounding.md` for full details. When set to the same value, `ROUNDUP` is a no-op. Current use case: `ALIGN_TIME=15`, `ROUNDUP=0`.
