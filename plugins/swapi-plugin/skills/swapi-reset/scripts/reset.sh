#!/usr/bin/env bash
# Archives the current pipeline run's artifacts under state/archive/<timestamp>/
# and removes them from the top level of state/, so the next swapi-fetch starts
# clean. state/history.log is never archived or touched - it is the permanent
# ledger across every run and reset.
set -euo pipefail

STATE_DIR="state"
ARTIFACTS=(01-raw.json 02-transformed.json 02-transformed.enriched.json 03-report.html pipeline-state.json)

FOUND=0
for f in "${ARTIFACTS[@]}"; do
  if [ -f "$STATE_DIR/$f" ]; then
    FOUND=1
    break
  fi
done

if [ "$FOUND" -eq 0 ]; then
  echo "nothing to reset - no run artifacts found in $STATE_DIR/"
  exit 0
fi

ARCHIVE_DIR="$STATE_DIR/archive/$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$ARCHIVE_DIR"

for f in "${ARTIFACTS[@]}"; do
  if [ -f "$STATE_DIR/$f" ]; then
    mv "$STATE_DIR/$f" "$ARCHIVE_DIR/$f"
  fi
done

echo "archived to $ARCHIVE_DIR"
