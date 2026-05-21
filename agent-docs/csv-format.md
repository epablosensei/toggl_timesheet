# CSV Output Format

The tool writes CSV files to the `data/` directory. The mode flag determines how entries are grouped and how files are named.

## Delimiter and quoting

All CSVs use `;` as the delimiter and `QUOTE_NONNUMERIC` quoting (all non-numeric fields are quoted).

## Output modes

### Default mode (no flag)

One CSV per client. Entries are aggregated by day — multiple entries on the same day for the same client are collapsed into one row (MIN start_time, MAX stop_time, SUM duration_dec).

**Filename:** `YYYY-MM-<client>.csv`
**Example:** `2026-04-Acme.csv`

**Header rows:**
```
"Client: ";  "<client name>"
"Period: ";  "<start> - <stop>"
""
"consultant"; "start date"; "start time"; "stop date"; "stop time"; "time (h)"; "duration_dec"
```

**Data rows:** one per day per client
```
"<user>"; "<YYYY-MM-DD>"; "<HH:MM:SS>"; ""; "<HH:MM:SS>"; ""; <decimal hours>
```

Note: stop date and `time (h)` columns are always empty (`""`).

---

### Per-project mode (`-p`)

One CSV per client/project/user combination.

**Filename:** `YYYY-MM-<client>-<project>-<username>.csv`
**Example:** `2026-04-Acme-Website-jane_smith.csv`

Username is lowercased with spaces replaced by underscores.

**Header rows:**
```
"Client:";  "<client>"
"Project:"; "<project>"
"Period:";  "<start> - <stop>"
"User:";    "<user>"
""
(blank row)
"consultant"; "start date"; "start time"; "stop date"; "stop time"; "time (h)"; "duration_dec"
```

**Data rows:** aggregated by day (same structure as default mode).

---

### Full mode (`-f`)

Single CSV with all entries across all clients and users. Aggregated by user and day.

**Filename:** `YYYY-MM-full.csv`
**Example:** `2026-04-full.csv`

**Header row (no metadata rows):**
```
"consultant"; "start date"; "start time"; "stop date"; "stop time"; "time (h)"; "duration_dec"
```

**Data rows:** one per user per day, all clients combined.

---

## Column definitions

| Column | Source | Notes |
|---|---|---|
| `consultant` | `user` field from Toggl | Consultant name as entered in Toggl |
| `start date` | `start` field | Date only, `YYYY-MM-DD` |
| `start time` | `start_time` field | `HH:MM:SS`, after alignment |
| `stop date` | — | Always empty |
| `stop time` | `stop_time` field | `HH:MM:SS`, after alignment |
| `time (h)` | — | Always empty |
| `duration_dec` | calculated | Decimal hours, e.g. `0.5` = 30 minutes |

## Data directory

Output files go to `config.DATA_DIR` (default: `data/`). An SQLite database (`YYYY-MM.db`) is also written there as an intermediate step — the previous run's database is rotated to `.db.old` before each run.
