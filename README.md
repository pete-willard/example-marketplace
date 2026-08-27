# Example Marketplace

An example [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) for QA skills.

## Plugins

- **swapi-plugin** — runs the SWAPI.info Star Wars API demo pipeline end to end: fetch a resource collection, sort/filter it, and render it as a self-contained HTML report. Bundles five skills (`swapi`, `swapi-fetch`, `swapi-transform`, `swapi-report`, `swapi-reset`) that read/write pipeline state under `state/` in the current project, plus a `sw-statistician` subagent for data analysis and rankings.

  `swapi-reset` is marked `user-invocable: false` — it has no slash command of its own. It only runs when Claude decides a reset is needed, or via `sw-statistician`, which preloads it as its sanctioned way to clear pipeline state.

## How to install

From inside Claude Code:

```bash
/plugin marketplace add pete-willard/example-marketplace && /plugin install swapi-plugin@example-marketplace
```

Or from a shell:

```bash
claude plugin marketplace add pete-willard/example-marketplace && claude plugin install swapi-plugin@example-marketplace
```

Add `-y` to the `install` command if running non-interactively (no TTY) to skip the confirmation prompt.

## Usage

Run the full pipeline:

```bash
/swapi-plugin:swapi
```

Or delegate an analysis question directly to the statistician subagent:

```
@swapi-plugin:sw-statistician what are the 5 heaviest starships?
```
