# ship-check.data.md — reference tables for `.claude/commands/ship-check.md`

Read by the `/ship-check` command (checks 1 and 4). Kept in a sibling file so `ship-check.md` stays under 200 lines (H6, §5.2). Do not duplicate these tables back into `ship-check.md` — this file is the one boss for them.

## Scrub regex table (§5.3.4)

`<APPROVED_ORG>` is a placeholder — resolve it at run time from the repo's `.ship-check/config.yml` key `approved_org`. Do not hardcode an org name here; config.yml owns that value (D-14, one boss).

| Pattern | Regex | Example match |
|---------|-------|---------------|
| Personal GitHub org/user (any but the approved org) | `github\.com/(?!<APPROVED_ORG>)[a-zA-Z0-9-]+/` | `github.com/someuser/example-repo` |
| HubSpot portal ID (in `hubspot/` or `skills/*/`) | `\b\d{7,8}\b` | `21445566` |
| Slack channel ID | `\bC[0-9A-Z]{8,10}\b` | `C08ABCDE12` |
| UUID (e.g. Notion page IDs) | `\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b` | `f47ac10b-58cc-4372-a567-0e02b2c3d479` |
| Local absolute path | `/Users/[^/\s]+/` or `C:\\Users\\` | `/Users/example/Desktop/...` |
| Stale brand names | `\b(ClearCalcs)\b` | `ClearCalcs` |
| Live customer/deal names | every line in `.ship-check/live-names.txt` (repo-owned do-not-ship list) | any line in that file |

## Blocker-keyword table (§5.3.1)

A review comment is a blocker if it is part of a `CHANGES_REQUESTED` review, OR its body matches (case-insensitive) any of:

| Keyword / pattern |
|--------------------|
| `blocker` |
| `request changes` |
| `must fix` |
| `before merge` |
| `do not merge` |
| 🚫 |
| `Round N` (a numbered directive, e.g. "Round 2") |
