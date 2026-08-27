#!/usr/bin/env python3
"""Filter a JSON array (from stdin) by a field/op/value condition."""
import json
import sys

OPS = {"eq", "contains", "gt", "gte", "lt", "lte"}


def numeric(value):
    if not isinstance(value, str):
        return None
    cleaned = value.replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


def matches(record, field, op, value):
    raw = record.get(field)

    if op == "eq":
        return isinstance(raw, str) and raw.lower() == value.lower()
    if op == "contains":
        return isinstance(raw, str) and value.lower() in raw.lower()

    left = numeric(raw)
    right = numeric(value)
    if left is None or right is None:
        return False
    if op == "gt":
        return left > right
    if op == "gte":
        return left >= right
    if op == "lt":
        return left < right
    if op == "lte":
        return left <= right
    return False


def main():
    if len(sys.argv) != 4:
        print("usage: filter.py <field> <eq|contains|gt|gte|lt|lte> <value>", file=sys.stderr)
        sys.exit(1)

    field, op, value = sys.argv[1], sys.argv[2], sys.argv[3]
    if op not in OPS:
        print(f"error: unknown op '{op}' (expected one of {sorted(OPS)})", file=sys.stderr)
        sys.exit(1)

    records = json.load(sys.stdin)
    result = [r for r in records if matches(r, field, op, value)]
    json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
