---
name: swapi-report
description: Render a previously transformed SWAPI.info dataset (state/02-transformed.json) into a self-contained HTML report using a matching template. Use when the user wants a formatted report, table, or page from Star Wars data that has already been fetched and transformed.
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/skills/swapi-report/scripts/render.py:*) Bash(xdg-open state/03-report.html:*) Read Write Agent
---

## What this skill does

Reads `state/02-transformed.json` and `state/pipeline-state.json`, picks the right HTML template for the entity type, and fills it in. No network calls of its own beyond the optional lookup in Step 2 - if the data isn't already right, send the user back to `swapi-transform`.

## Step 1: pick the template

Read `entity_type` from `state/pipeline-state.json`, then load **only** the matching template - this is a branch, not a menu to browse:

- `people` -> [templates/people-report.html](templates/people-report.html)
- `planets` -> [templates/planets-report.html](templates/planets-report.html)
- `starships` -> [templates/starships-report.html](templates/starships-report.html)
- anything else (`vehicles`, `species`, `films`) -> [templates/generic-report.html](templates/generic-report.html)

Don't read the other three templates - they don't apply to this run and would only spend context for nothing.

## Step 2: pick which columns to show (people / planets / starships only)

These three templates support a dynamic column set instead of a fixed one - the report should only show columns relevant to what was actually asked for, not every field the template happens to know about.

1. Read `operation` and `params` from `state/pipeline-state.json`. Both `sort` and `filter` record the field that was queried as `params.field` - that's always included.
2. Default columns = `name` + `params.field` (skip the duplicate if `params.field` is already `name`, e.g. a `filter name eq ...` run).
3. If `params.display_fields` is present (a list `swapi-transform` records when the user explicitly named extra columns to display, beyond what they sorted/filtered on), append those too, deduped, preserving order.
4. Don't ask the user for extra columns here - only show more than the default when `display_fields` already says so. "Only when explicitly asked for" means honor it if it's already recorded, not prompt for it every render.

This produces an ordered list like `name,length` or `name,length,crew` - pass it to `render.py` as `--columns` in Step 4. `generic-report.html` has no columns to pick (it's a name+url list, not a table) - skip this step entirely when that's the chosen template.

## Step 3: resolve homeworld names (people only, optional)

`homeworld` in the raw data is a URL (e.g. `https://swapi.info/api/planets/1`), not a name, and the people template has a `{{homeworld_name}}` column. If `entity_type` is `people`, resolve it before rendering:

1. Collect the **distinct** `homeworld` URLs across the rows (there are far fewer unique planets than people - dedupe first, don't fetch once per row).
2. For each distinct URL, delegate the lookup to a lightweight subagent: call the Agent tool with `model: "haiku"` and a prompt like "Fetch `<url>` and return only the planet's `name` field, nothing else." This is a purely mechanical fetch-and-extract with no ambiguity or multi-step reasoning, so it doesn't need this skill's main model - a small/fast model is the right tool for the job, and it's cheap to fan out one call per distinct planet in parallel.
3. Merge the results back into the rows in memory as `homeworld_name`, keyed by the original `homeworld` URL, before calling `render.py`.

Skip this step entirely for any other `entity_type` - the other templates have no `{{homeworld_name}}` token.

## Step 4: render

Run:

```
${CLAUDE_PLUGIN_ROOT}/skills/swapi-report/scripts/render.py <chosen-template-path> state/02-transformed.json state/03-report.html --columns <columns-from-step-2>
```

Omit `--columns` entirely when the chosen template is `generic-report.html` (it has no header marker, so `render.py` would just warn and ignore it anyway).

(`CLAUDE_PLUGIN_ROOT` resolves to this plugin's install directory - the script always runs from there, regardless of the current project's working directory.) `render.py` does plain `{{field}}` token substitution, once per row, inside the template's `<!-- ROW_START --> ... <!-- ROW_END -->` block, HTML-escaping every value. It does not evaluate anything from the data, so odd values like `"unknown"` mass just render as literal text instead of breaking the page. With `--columns`, it also regenerates the header row and the per-row cells from that exact list, overriding the template's static header - that's what keeps the report limited to the columns Step 2 picked instead of the template's full fixed set. If you resolved `homeworld_name` in Step 3, write the enriched rows to a temporary JSON file first and pass that to `render.py` instead of `state/02-transformed.json` directly.

## Step 5: finish

Update `state/pipeline-state.json` with `{"step": "report", "output": "state/03-report.html"}` and append a line to `state/history.log`. Tell the user the report's path, then ask - don't just do it - "Would you like me to open it in your browser?" Only run `xdg-open state/03-report.html` if they say yes.
