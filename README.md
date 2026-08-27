# Example Marketplace

An example [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) for QA skills.

## Plugins

- **swapi-plugin** — runs the SWAPI.info Star Wars API demo pipeline end to end: fetch a resource collection, sort/filter it, and render it as a self-contained HTML report. Bundles five skills (`swapi`, `swapi-fetch`, `swapi-transform`, `swapi-report`, `swapi-reset`) that read/write pipeline state under `state/` in the current project.

## Usage

```bash
/plugin marketplace add pete-willard/example-marketplace
/plugin install swapi-plugin@example-marketplace
```

Then run:

```bash
/swapi-plugin:swapi
```
