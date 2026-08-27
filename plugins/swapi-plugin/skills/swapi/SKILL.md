---
name: swapi
description: Run the full Star Wars API demo pipeline end to end - fetch a SWAPI.info resource, transform it, and render an HTML report. Use when the user wants to run, demo, or restart the whole SWAPI pipeline rather than a single step.
---

Run these three skills in order. Each one reads the previous one's output from `state/` and writes its own - don't skip steps or reorder them:

1. `swapi-fetch` - ask what to fetch, hit swapi.info, write `state/01-raw.json`.
2. `swapi-transform` - read `state/01-raw.json`, ask what operation to apply, write `state/02-transformed.json`.
3. `swapi-report` - read `state/02-transformed.json`, render the HTML report, write `state/03-report.html`.

If `state/pipeline-state.json` already shows a completed step from a previous run, ask the user whether to resume from the next step or start over. If they choose to start over, run `swapi-reset` first (it archives the previous run's artifacts under `state/archive/`, it does not delete them) before invoking `swapi-fetch`.
