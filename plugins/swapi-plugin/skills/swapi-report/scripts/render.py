#!/usr/bin/env python3
"""Fill an HTML template's row block with rows from a JSON array.

Usage: render.py <template.html> <data.json> <output.html> [--columns field1,field2,...]

Template contract: everything between the literal markers
<!-- ROW_START --> and <!-- ROW_END --> is treated as one row's HTML,
repeated once per record, with {{field}} tokens replaced by that
record's value (HTML-escaped). Everything outside the markers is
copied through unchanged. {{row_count}} outside the row block is
replaced with the total number of rows rendered.

Optional --columns: a comma-separated list of field names. When given,
the table header and row cells are generated from exactly this column
list instead of the template's static ones - this is how a report shows
only the columns relevant to what was actually sorted/filtered, instead
of a fixed set baked into the template. This requires the template to
mark its header row with <!-- HEADER_START --> ... <!-- HEADER_END -->
(the three table templates - people/planets/starships - have this;
generic-report.html is a name+url list, not a table, and has no marker,
so --columns is ignored for it with a warning).
"""
import html
import json
import re
import sys

ROW_RE = re.compile(r"<!-- ROW_START -->(.*?)<!-- ROW_END -->", re.DOTALL)
HEADER_RE = re.compile(r"<!-- HEADER_START -->(.*?)<!-- HEADER_END -->", re.DOTALL)
TOKEN_RE = re.compile(r"\{\{(\w+)\}\}")

# Only the fields that need units or a non-obvious label spelled out -
# everything else falls back to title-casing the field name.
LABEL_OVERRIDES = {
    "height": "Height (cm)",
    "mass": "Mass (kg)",
    "diameter": "Diameter (km)",
    "length": "Length (m)",
    "surface_water": "Surface Water (%)",
    "rotation_period": "Rotation Period (hrs)",
    "orbital_period": "Orbital Period (days)",
    "cost_in_credits": "Cost (credits)",
    "homeworld_name": "Homeworld",
}


def label_for(field):
    return LABEL_OVERRIDES.get(field, field.replace("_", " ").title())


def render_row(row_template, record):
    def replace(match):
        value = record.get(match.group(1), "")
        return html.escape(str(value))
    return TOKEN_RE.sub(replace, row_template)


def parse_args(argv):
    columns = None
    positional = []
    i = 0
    while i < len(argv):
        if argv[i] == "--columns":
            i += 1
            if i >= len(argv):
                print("error: --columns requires a value", file=sys.stderr)
                sys.exit(1)
            columns = [c.strip() for c in argv[i].split(",") if c.strip()]
        else:
            positional.append(argv[i])
        i += 1
    if len(positional) != 3:
        print("usage: render.py <template.html> <data.json> <output.html> [--columns field1,field2,...]", file=sys.stderr)
        sys.exit(1)
    return positional[0], positional[1], positional[2], columns


def main():
    template_path, data_path, output_path, columns = parse_args(sys.argv[1:])

    with open(template_path, encoding="utf-8") as f:
        template = f.read()
    with open(data_path, encoding="utf-8") as f:
        records = json.load(f)

    row_match = ROW_RE.search(template)
    if not row_match:
        print("error: template has no <!-- ROW_START --> ... <!-- ROW_END --> block", file=sys.stderr)
        sys.exit(1)

    header_match = HEADER_RE.search(template)
    dynamic = bool(columns and header_match)

    if columns and not header_match:
        print(f"warning: --columns given but {template_path} has no <!-- HEADER_START --> marker; ignoring --columns", file=sys.stderr)

    if dynamic:
        header_html = "<tr>" + "".join(f"<th>{html.escape(label_for(c))}</th>" for c in columns) + "</tr>"
        row_template = "<tr>" + "".join(f"<td>{{{{{c}}}}}</td>" for c in columns) + "</tr>"
        template = template[:header_match.start()] + header_html + template[header_match.end():]
        # Header replacement shifts offsets, so re-find the row block before using it.
        row_match = ROW_RE.search(template)
    else:
        row_template = row_match.group(1)

    rows_html = "\n".join(render_row(row_template, r) for r in records)

    output = template[: row_match.start()] + rows_html + template[row_match.end():]
    output = output.replace("{{row_count}}", str(len(records)))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"wrote {len(records)} rows to {output_path}")


if __name__ == "__main__":
    main()
