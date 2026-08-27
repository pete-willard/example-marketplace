---
name: swapi-reset
description: Archive and clear the SWAPI pipeline's current run artifacts (state/01-raw.json, state/02-transformed*.json, state/03-report.html, state/pipeline-state.json) so the next swapi-fetch starts clean. Use when the user wants to reset, clear, start over, or wipe the previous SWAPI pipeline run before running it again.
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/skills/swapi-reset/scripts/reset.sh:*) Read Write
user-invocable: false
---

## What this skill does

Moves the current run's artifacts into a timestamped `state/archive/<timestamp>/` folder and removes them from the top level of `state/`, so `swapi-fetch` doesn't see a stale `pipeline-state.json` or `01-raw.json` from a previous run. It never deletes anything - only moves. `state/history.log` is never touched: it's the permanent ledger across every run and every reset, by design.

## Steps

1. Run `${CLAUDE_PLUGIN_ROOT}/skills/swapi-reset/scripts/reset.sh` (`CLAUDE_PLUGIN_ROOT` resolves to this plugin's install directory - the script always runs from there, regardless of the current project's working directory).
2. If it prints "nothing to reset", tell the user the pipeline is already clean - there's nothing more to do.
3. If it prints an archive path, append a line to `state/history.log`, e.g. `2026-08-16T22:40:00Z reset -> archived previous run to state/archive/20260816T224000Z/`.
4. Tell the user the pipeline is clear and ready for a fresh `swapi-fetch`.

## Notes

- This is a deliberate, single-purpose skill - it only resets, it doesn't fetch/transform/report anything itself.
- `user-invocable: false` means this skill has no `/swapi-plugin:swapi-reset` slash command - it only runs when Claude (or an agent that preloads it, like `sw-statistician`) decides a reset is needed.
- Old archives under `state/archive/` are never cleaned up automatically. If the user wants to actually discard an old archive, that's a separate, explicit request - don't do it as a side effect of running this skill.
