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

# Set up mounts (:z needed for SELinux on Fedora/RHEL)
MOUNTS="-v ./data:/app/data:z"

if [ -f config.py ]; then
    MOUNTS="$MOUNTS -v ./config.py:/app/config.py:ro,z"
fi

# Create data directory if it doesn't exist
mkdir -p data

exec $RUNTIME run --rm $MOUNTS "$IMAGE" "$@"
