---
name: swapi-fetch
description: Fetch a single resource collection (people, planets, starships, vehicles, species, or films) from swapi.info, the public Star Wars API, and save the raw JSON as the source of truth for the SWAPI demo pipeline. Use when the user wants to pull, download, or refresh Star Wars data before sorting/filtering/reporting on it.
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/skills/swapi-fetch/scripts/fetch.sh:*) Read Write
---

## What this skill does

Fetches exactly one SWAPI.info resource collection, verbatim, and writes it to disk. It does not sort, filter, or reshape the data - that is `swapi-transform`'s job. This skill's only job is getting an honest copy of the source of truth onto disk.

## Steps

1. Ask the user which resource to fetch: `people`, `planets`, `starships`, `vehicles`, `species`, or `films`. See [references/endpoints.md](references/endpoints.md) for what each collection contains and known data quirks - read it before you reason about the data, don't guess.
2. Run `${CLAUDE_PLUGIN_ROOT}/skills/swapi-fetch/scripts/fetch.sh <resource>` (`CLAUDE_PLUGIN_ROOT` resolves to this plugin's install directory - the script always runs from there, regardless of the current project's working directory). This is the only network call this skill makes, and it only ever talks to `https://swapi.info`.
3. Save the script's stdout verbatim to `state/01-raw.json` in the project root (create the `state/` directory if it doesn't exist yet).
4. Write/update `state/pipeline-state.json`:
   ```json
   {
     "step": "fetch",
     "entity_type": "<resource>",
     "fetched_at": "<ISO timestamp>",
     "count": <number of records>,
     "source": "https://swapi.info/api/<resource>"
   }
   ```
5. Append one line to `state/history.log`, e.g. `2026-08-16T12:00:00Z fetch people -> state/01-raw.json (83 items)`.
6. Tell the user how many records were fetched and that `swapi-transform` is the next step.

## Notes

- `swapi.info` returns the full collection as a flat JSON array - there is no pagination and no server-side filtering or `?limit=` support. If the user asks for "the first 5 rows" or "top 10", that is `swapi-transform`'s job, not this skill's: fetch everything, trim later.
- Fetch exactly one resource per run. If the user wants both `people` and `planets`, run this skill twice and ask before overwriting an existing `state/01-raw.json`.
