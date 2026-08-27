#!/usr/bin/env bash
# Fetches a single SWAPI.info collection and prints it to stdout as JSON.
# Usage: fetch.sh <people|planets|starships|vehicles|species|films>
set -euo pipefail

RESOURCE="${1:?usage: fetch.sh <people|planets|starships|vehicles|species|films>}"
BASE_URL="https://swapi.info/api"

case "$RESOURCE" in
  people|planets|starships|vehicles|species|films) ;;
  *)
    echo "error: unknown resource '$RESOURCE' (expected people|planets|starships|vehicles|species|films)" >&2
    exit 1
    ;;
esac

curl -sS --fail-with-body "$BASE_URL/$RESOURCE"
