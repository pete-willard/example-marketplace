# Sorting SWAPI data

`scripts/sort.py` reads a JSON array from stdin and writes a JSON array to stdout.

```
${CLAUDE_PLUGIN_ROOT}/skills/swapi-transform/scripts/sort.py <field> <asc|desc> [limit] < state/01-raw.json > state/02-transformed.json
```

(`CLAUDE_PLUGIN_ROOT` resolves to this plugin's install directory - the script always runs from there, regardless of the current project's working directory.)

Behavior:

- Values are coerced with a numeric-aware comparator: commas are stripped, then the result is parsed as a float.
- Records where the field is `"unknown"`, missing, or otherwise non-numeric always sort to the **end**, regardless of `asc`/`desc` - they are excluded from the ranking rather than silently treated as `0`.
- `limit` (optional) trims to the first N rows after sorting. This is how "top 5" / "give me N rows" requests are satisfied - `swapi.info` itself has no row-limit query parameter, so the trimming has to happen here, client-side.

Example:

```
${CLAUDE_PLUGIN_ROOT}/skills/swapi-transform/scripts/sort.py mass desc 5 < state/01-raw.json > state/02-transformed.json
```

Returns the 5 people with the highest known `mass` - Jabba Desilijic Tiure's `"1,358"` correctly outranks every three-digit mass, and the 20+ people with `mass: "unknown"` are excluded rather than sorted to the top or bottom arbitrarily.
