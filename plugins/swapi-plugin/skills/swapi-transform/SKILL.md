---
name: swapi-transform
description: Sort, filter, or trim a previously-fetched SWAPI.info dataset (state/01-raw.json) into a smaller, ordered result set. Use when the user wants to sort, rank, filter, or take the top/bottom N rows of Star Wars data that has already been fetched.
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/skills/swapi-transform/scripts/sort.py:*) Bash(${CLAUDE_PLUGIN_ROOT}/skills/swapi-transform/scripts/filter.py:*) Read Write
---

## What this skill does

Takes the raw JSON at `state/01-raw.json` (written by `swapi-fetch`) and produces a smaller, ordered `state/02-transformed.json`. It makes no network calls - if `state/01-raw.json` doesn't exist, tell the user to run `swapi-fetch` first instead of guessing at data.

## Step 1: hard-stop checkpoint - ask before doing anything else

This is a required interactive checkpoint, not a formality: **always** stop here and ask the user, even if their original request already seemed to state a count or field (e.g. "give me the 5 heaviest" still gets asked). Do not infer, assume, or default these values yourself. End your turn on the question and wait for a reply before touching Step 2.

1. Read `entity_type` from `state/pipeline-state.json`.
2. Look up that resource's row in the "Sortable vs. filterable fields" table in `swapi-fetch`'s [references/endpoints.md](../swapi-fetch/references/endpoints.md), and present the real sortable and filterable field names to the user as a short menu - don't invent or guess field names, and don't offer every field in the raw JSON, only the ones that table lists.
3. Ask exactly two questions:
   - How many results do you want in the end?
   - Which field, and which sort direction (ascending/descending) or filter condition, should be used?

Only proceed to Step 2 once the user has answered both. Don't add a third question about report columns - `swapi-report` defaults the final report to just the name and the field used here. Only if the user volunteers, unprompted, that they also want other fields *shown* in the report (not sorted/filtered on - e.g. "sort by length but also show me the crew count"), note those extra field names for Step 3.

## Step 2: branch to the matching reference and script

This dataset has real junk values - `"unknown"` and comma-thousands like `"1,358"` (see `swapi-fetch`'s [references/endpoints.md](../swapi-fetch/references/endpoints.md)). Don't hand-roll a comparison yourself; load **one** of the following branches, whichever matches the request, and use its script:

- **Sorting or ranking** ("top N", "bottom N", "heaviest", "tallest", "by X ascending/descending") -> read [references/sort.md](references/sort.md), then run `${CLAUDE_PLUGIN_ROOT}/skills/swapi-transform/scripts/sort.py`.
- **Filtering by a condition** ("only where mass > 1000", "climate contains desert", exact match on a field) -> read [references/filter.md](references/filter.md), then run `${CLAUDE_PLUGIN_ROOT}/skills/swapi-transform/scripts/filter.py`.

Only read the reference file for the branch you are actually taking - the other one is irrelevant to this request and would just spend context for nothing. Both scripts are called via `${CLAUDE_PLUGIN_ROOT}`, which resolves to this plugin's install directory regardless of the current project's working directory.

## Step 3: save state

Write the script's stdout to `state/02-transformed.json`. Update `state/pipeline-state.json` with an added `"operation"` and `"params"` describing what was done, and append a line to `state/history.log`. If the user named extra display-only fields in Step 1, add them as `"params.display_fields": [...]` (a plain list of field names) so `swapi-report` can pick them up later without needing this conversation's context - otherwise omit the key entirely, don't write it as an empty list. Tell the user how many rows survived and that `swapi-report` is the next step.
