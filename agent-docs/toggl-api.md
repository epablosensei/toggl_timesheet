# Toggl API

## Authentication

HTTP Basic Auth with the API token as the username and the literal string `api_token` as the password. No OAuth required.

```python
from requests.auth import HTTPBasicAuth
auth = HTTPBasicAuth(api_token, 'api_token')
```

The token is set in `config.py` as `API_TOKEN`.

## Endpoints in use

The tool uses **Reports API v2** exclusively.

Base URL: `https://api.track.toggl.com/reports/api/v2`

| Endpoint | Method | Used for |
|---|---|---|
| `/details` | GET | Fetching all time entries for a date range |

Parameters sent with every request:
- `workspace_id` — required, set in `config.py`
- `since` / `until` — date range (ISO format)
- `user_agent` — hardcoded as `toggl_timesheet`
- `rounding` — passed as `off` by default
- `per_page` — number of entries per page (default 50)

## Pagination

The API returns paginated results. The response includes `total_count` and `per_page`. The client fetches page 1, calculates how many pages exist, then fetches the remaining pages sequentially.

```python
last_page = (total_count // per_page) + 1  # if remainder exists
```

All pages are concatenated into a single list before processing.

## Rate limits and errors

| HTTP status | Meaning | Tool behaviour |
|---|---|---|
| 401 | Bad API token | Prints specific message, exits |
| 429 | Rate limit hit | Prints specific message, exits |
| other 4xx/5xx | API error | Prints generic message with status, exits |
| timeout | No response in 30s | Prints timeout message, exits |

## API version notes

- **v2** (current): confirmed working, used by `ReportAPI` in `togglapi/api.py`
- **v3**: Toggl has indicated this is coming but it is not yet fully documented — tracked as TASK-010
- **v8** (time entries API): was used by the old `TogglAPI` class which has been removed; v8 is being deprecated by Toggl
