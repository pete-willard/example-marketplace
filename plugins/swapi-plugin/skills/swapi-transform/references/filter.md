# Filtering SWAPI data

`scripts/filter.py` reads a JSON array from stdin and writes a JSON array to stdout.

```
${CLAUDE_PLUGIN_ROOT}/skills/swapi-transform/scripts/filter.py <field> <op> <value> < state/01-raw.json > state/02-transformed.json
```

(`CLAUDE_PLUGIN_ROOT` resolves to this plugin's install directory - the script always runs from there, regardless of the current project's working directory.)

Supported `<op>` values:

- `eq` - case-insensitive exact string match.
- `contains` - case-insensitive substring match.
- `gt`, `gte`, `lt`, `lte` - numeric comparison. Values are comma-stripped and parsed as floats, same as `sort.py`; records where the field can't be parsed as a number (e.g. `"unknown"`) are dropped rather than raising an error or defaulting to `0`.

Example:

```
${CLAUDE_PLUGIN_ROOT}/skills/swapi-transform/scripts/filter.py climate contains desert < state/01-raw.json > state/02-transformed.json
${CLAUDE_PLUGIN_ROOT}/skills/swapi-transform/scripts/filter.py mass gt 1000 < state/01-raw.json > state/02-transformed.json
```

The second example returns only Jabba Desilijic Tiure - every `mass: "unknown"` record is dropped, not treated as failing (or passing) the comparison silently.
