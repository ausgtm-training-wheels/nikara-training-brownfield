#!/usr/bin/env python3
"""Render the pipeline-summary export dashboard as a self-contained HTML file.

The dashboard has two tabs:
  - Summary: the read-only stage-by-stage roll-up (deal count, value, owner load).
  - Write-back: a form the manager uses to queue stage corrections back to HubSpot.

SKILL.md documents both tabs. If SKILL.md's description of what this script
renders and this file ever disagree, /ship-check's claim-vs-implementation
check (§5.3.7) should catch it — this file is the boss for what actually renders.
"""

import html
import json
import sys


def render_summary_tab(stages):
    rows = "".join(
        "<tr><td>{name}</td><td>{count}</td><td>{value}</td><td>{owner}</td></tr>".format(
            name=html.escape(s["name"]),
            count=s["count"],
            value=html.escape(s["value"]),
            owner=html.escape(s["top_owner"]),
        )
        for s in stages
    )
    return (
        '<section id="summary" class="tab">'
        "<h2>Pipeline summary</h2>"
        "<table><thead><tr><th>Stage</th><th>Deals</th>"
        "<th>Value</th><th>Top owner</th></tr></thead>"
        "<tbody>{rows}</tbody></table>"
        "</section>"
    ).format(rows=rows)


def render_writeback_tab(stages):
    # Write-back tab: renders a stage-change form the manager submits to push
    # corrections back into HubSpot. This is the tab a "read-only" claim must drop.
    options = "".join(
        '<option value="{name}">{name}</option>'.format(name=html.escape(s["name"]))
        for s in stages
    )
    return (
        '<section id="writeback" class="tab">'
        "<h2>Write-back</h2>"
        '<form method="post" action="/hubspot/deals/stage">'
        '<label>Deal ID <input name="deal_id"></label>'
        '<label>Move to stage <select name="stage">{options}</select></label>'
        '<button type="submit">Push change to HubSpot</button>'
        "</form>"
        "</section>"
    ).format(options=options)


def render_dashboard(stages):
    tabs = [
        ("Summary", render_summary_tab(stages)),
        ("Write-back", render_writeback_tab(stages)),
    ]
    nav = "".join(
        '<a href="#{anchor}">{label}</a>'.format(anchor=label.lower().replace("-", ""), label=label)
        for label, _ in tabs
    )
    body = "".join(section for _, section in tabs)
    return "<!doctype html><html><body><nav>{nav}</nav>{body}</body></html>".format(
        nav=nav, body=body
    )


def main(argv):
    # Input: a JSON file of stages on argv[1], or a tiny built-in sample.
    if len(argv) > 1:
        with open(argv[1], encoding="utf-8") as fh:
            stages = json.load(fh)
    else:
        stages = [
            {"name": "Discovery", "count": 12, "value": "$240k", "top_owner": "Rep A"},
            {"name": "Proposal", "count": 5, "value": "$310k", "top_owner": "Rep B"},
        ]
    sys.stdout.write(render_dashboard(stages))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
