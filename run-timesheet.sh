#!/bin/bash
# Usage: ./run-timesheet.sh [timesheet.py args...]
# Examples:
#   ./run-timesheet.sh -h
#   ./run-timesheet.sh -s 2024-01-01 -e 2024-01-31 -p

set -e

RUNTIME=$(command -v podman || command -v docker)
if [ -z "$RUNTIME" ]; then
    echo "Error: neither podman nor docker found in PATH" >&2
    exit 1
fi

IMAGE="toggl-timesheet"

# Build image if it doesn't exist
if ! "$RUNTIME" image exists "$IMAGE" 2>/dev/null; then
    echo "Image '$IMAGE' not found, building..."
    "$RUNTIME" build -t "$IMAGE" .
fi

# Determine host data directory
# Priority: TOGGL_DATA_DIR env var > config.py DATA_DIR > default 'data'
if [ -n "$TOGGL_DATA_DIR" ]; then
    DATA_DIR="$TOGGL_DATA_DIR"
elif [ -f config.py ]; then
    DATA_DIR=$(python3 -c "
import re
for line in open('config.py'):
    m = re.match(r\"DATA_DIR\s*=\s*['\x22](.+?)['\x22]\", line)
    if m: print(m.group(1)); break
else: print('data')
" 2>/dev/null || echo "data")
else
    DATA_DIR="data"
fi

mkdir -p "$DATA_DIR"

# Mount host DATA_DIR to same path inside container (:z for SELinux)
MOUNTS="-v ./$DATA_DIR:/app/$DATA_DIR:z"

if [ -f config.py ]; then
    MOUNTS="$MOUNTS -v ./config.py:/app/config.py:ro,z"
fi

exec $RUNTIME run --rm -e TOGGL_DATA_DIR="$DATA_DIR" $MOUNTS "$IMAGE" "$@"
