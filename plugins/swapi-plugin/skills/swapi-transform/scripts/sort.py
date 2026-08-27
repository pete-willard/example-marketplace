#!/usr/bin/env python3
"""Sort a JSON array (from stdin) by a field. Non-numeric values sort last."""
import json
import sys


def numeric_key(value):
    if not isinstance(value, str):
        return None
    cleaned = value.replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


def main():
    if len(sys.argv) < 3:
        print("usage: sort.py <field> <asc|desc> [limit]", file=sys.stderr)
        sys.exit(1)

    field = sys.argv[1]
    direction = sys.argv[2]
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else None

    if direction not in ("asc", "desc"):
        print("error: direction must be 'asc' or 'desc'", file=sys.stderr)
        sys.exit(1)

    records = json.load(sys.stdin)

    rankable = [r for r in records if numeric_key(r.get(field)) is not None]
    unrankable = [r for r in records if numeric_key(r.get(field)) is None]

    rankable.sort(key=lambda r: numeric_key(r.get(field)), reverse=(direction == "desc"))

    result = rankable + unrankable
    if limit is not None:
        result = result[:limit]

    json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
