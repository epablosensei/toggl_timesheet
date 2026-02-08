# Sprint Backlog

## Current Sprint
Started: 2026-01-21
Goal: Python 3 Migration Planning

## In Progress
<!-- Tasks currently being worked on -->

## Backlog (Prioritized)

### Python 3 Migration
- [ ] **[TASK-001]** Complete roundup function implementation
  - File: toggltime/toggltime.py:180
  - Notes: TODO comment exists, function is incomplete

- [ ] **[TASK-002]** Audit Python 2/3 compatibility issues
  - Check print statements (need parentheses)
  - Check urllib imports (urllib vs urllib.parse)
  - Check string handling (unicode)

- [ ] **[TASK-003]** Add `from __future__ import` statements
  - print_function, division, unicode_literals

- [ ] **[TASK-004]** Update requirements.txt for Python 3
  - Verify all dependencies support Python 3

### Code Quality
- [ ] **[TASK-005]** Add proper error handling for API failures
- [ ] **[TASK-006]** Add unit tests for core functionality
- [ ] **[TASK-007]** Add type hints (after Python 3 migration)

### Features
- [ ] **[TASK-008]** Consider adding XLS export option
  - Branch exists: feature/xls_print

## Completed
<!-- Completed tasks with dates -->
- [x] **[TASK-009]** Containerize for Podman/Docker (Python 2.7)
  - Completed: 2026-02-08
  - Branch: feature/podman-container
  - Containerfile (python:2.7-slim), requirements-container.txt, run-timesheet.sh
  - Environment variable support in config.py-example
  - SELinux-compatible volume mounts (:z flag)

- [x] **[CHORE-001]** Add Claude Code configuration
  - Completed: 2026-01-21
  - Branch: claudify-repo

## Blocked
<!-- Tasks waiting on external dependencies -->
