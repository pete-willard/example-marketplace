# SWAPI.info endpoints

Base URL: `https://swapi.info/api` - no auth, no documented rate limit, no pagination.

Each endpoint returns a **flat JSON array** of every record in that collection - unlike the old `swapi.dev`, there is no `{count, next, previous, results}` wrapper. What you fetch is everything there is.

| Resource | Endpoint | Approx. count | Notable fields |
|---|---|---|---|
| people | `/api/people` | 83 | height, mass, hair_color, skin_color, eye_color, birth_year, gender, homeworld (URL), films/species/vehicles/starships (URL arrays) |
| planets | `/api/planets` | 60 | rotation_period, orbital_period, diameter, climate, gravity, terrain, surface_water, population |
| starships | `/api/starships` | 36 | name, model, manufacturer, cost_in_credits, length, crew, passengers, cargo_capacity, hyperdrive_rating |
| vehicles | `/api/vehicles` | 39 | name, model, manufacturer, cost_in_credits, length, crew, passengers |
| species | `/api/species` | 37 | classification, designation, average_height, language |
| films | `/api/films` | 6 | title, episode_id, director, release_date |

A single record (e.g. `/api/people/1`) returns the same shape as one array element, plus `created`, `edited`, and `url`.

## Sortable vs. filterable fields, per resource

`swapi-transform` uses this table to tell the user what's actually available before asking them to pick - don't offer a field that isn't real, and don't offer a field as "sortable" if it isn't reliably numeric (see quirks below).

| Resource | Sortable (numeric, use `scripts/sort.py`) | Filterable (text, use `scripts/filter.py`'s `eq`/`contains`, or numeric ops for the sortable fields above) |
|---|---|---|
| people | `height`, `mass` | `hair_color`, `skin_color`, `eye_color`, `gender`, `birth_year`, `name` |
| planets | `rotation_period`, `orbital_period`, `diameter`, `surface_water`, `population` | `climate`, `terrain`, `gravity`, `name` |
| starships | `cost_in_credits`, `length`, `crew`, `passengers`, `cargo_capacity`, `hyperdrive_rating` | `name`, `model`, `manufacturer` |
| vehicles | `cost_in_credits`, `length`, `crew`, `passengers` | `name`, `model`, `manufacturer` |
| species | `average_height` | `classification`, `designation`, `language`, `name` |
| films | `episode_id` | `title`, `director`, `release_date` |

`birth_year` (people) and `release_date` (films) look sortable but aren't listed as such on purpose: `birth_year` values look like `"19BBY"`/`"600BBY"` and `release_date` is an ISO date string - `scripts/sort.py`'s numeric coercion can't parse either, so they'd silently fall into the "non-numeric, sorts last" bucket. Filter on them with `eq`/`contains` instead.

## Known data quirks (verified against the live API, not assumed)

Numeric-looking fields are strings, and not all of them are numeric:

- Fields like `mass` are frequently the literal string `"unknown"` - e.g. most political/Jedi characters in `people` have `mass: "unknown"` (Tarkin, Mon Mothma, Grievous, and 20+ others).
- At least one record uses a thousands separator: Jabba Desilijic Tiure has `mass: "1,358"`. A naive `parseInt`/numeric sort will silently misorder this (`parseInt("1,358")` stops at the comma and reads `1`) or produce `NaN`.
- Relationship fields (`homeworld`, `films`, `species`, `vehicles`, `starships`) are **URLs, not names** - rendering them directly in a report shows a raw link instead of e.g. "Tatooine".

Treat this file as the source of truth for `swapi-transform`'s sort/filter logic over assumptions about "clean" numeric data - `scripts/sort.py` and `scripts/filter.py` in that skill both handle the comma and `"unknown"` cases explicitly, on purpose.
