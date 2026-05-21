# Time Rounding and Alignment

The tool has two independent settings for controlling how time entries are adjusted before being written to CSV.

## ALIGN_TIME

Snaps both the **start and stop times** of each entry to clean minute boundaries. The billed duration is then recalculated from those snapped times.

Valid values: `0` (off), `1` (hourly), `15` (15-minute intervals), `30` (30-minute intervals)

### Start time rules (ALIGN_TIME=15)

| Actual minute | Snaps to |
|---|---|
| :00 – :10 | :00 |
| :11 – :20 | :15 |
| :21 – :40 | :30 |
| :41 – :50 | :45 |
| :51 – :59 | :00 next hour |

### Stop time rules (ALIGN_TIME=15)

| Actual minute | Snaps to |
|---|---|
| :00 (exactly) | :00 (unchanged) |
| :01 – :15 | :15 |
| :16 – :30 | :30 |
| :31 – :45 | :45 |
| :46 – :59 | :00 next hour |

Stop time always moves **forward** (never back). Start time can move either direction.

### Effect on duration

Because both start and stop land on boundary times, the resulting duration is always a multiple of the interval. With ALIGN_TIME=15, duration is always a multiple of 15 minutes.

## ROUNDUP

Leaves the **start time unchanged** and rounds the duration up to the next interval, extending the stop time forward to cover it.

Valid values: `0` (off), `1`, `15`, `30`

Example with ROUNDUP=15, ALIGN_TIME=0:

| Original | Duration | After roundup | New stop |
|---|---|---|---|
| 09:00 – 09:07 | 7 min | 15 min | 09:15 |
| 09:00 – 09:15 | 15 min | 15 min (unchanged) | 09:15 |
| 09:00 – 09:16 | 16 min | 30 min | 09:30 |

## Using both together

When ALIGN_TIME and ROUNDUP are set to the **same value**, ROUNDUP is always a no-op. Alignment already guarantees the duration is a multiple of the interval, so there is nothing for ROUNDUP to round up.

**Current setup (ALIGN_TIME=15, ROUNDUP=0):** entries snap to 15-minute boundaries, duration follows. This is the correct setting for booking in 15-minute increments.

ROUNDUP is available as an option if you ever want to keep original clock times in the CSV but still enforce minimum billing intervals — but that is not the current use case.

## Processing order

For each entry, the tool always runs alignment first, then roundup:

```
align_start_stop()  →  roundup()  →  write to DB
```

## History

`roundup()` was unimplemented (a stub) in the original Python 2 code. It was fully implemented in the Python 3 migration using `math.ceil` (always rounds up, never down). The original stub had a comment suggesting nearest-interval rounding (`round()`), but ceiling rounding was chosen as it avoids ever billing zero for a non-zero entry.
