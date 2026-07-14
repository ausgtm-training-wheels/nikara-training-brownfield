# Contributing to nikara-training-brownfield

This repo trains the **brief → verify → decide** loop. Before you touch
anything, read `CLAUDE.md` (the seven invariants) and run `/ship-check`
before every PR. The long-form reasoning behind every rule below lives in
`SETUP.md` (the course's spec of record) — this file pins the tables you
need day to day; it does not restate the reasoning.

## The seven habits (H1-H7)

| ID | Habit | Real-PR symptom |
|----|-------|-----------------|
| **H1** | **Merged past the blocker.** Treats "Request changes" as advisory. | Merged with Round 1 and Round 2 reviewer blockers still open. |
| **H2** | **Answer the easy half.** Ships the reference file, skips the mechanism. | Delivered a reference doc but never folded the mechanism into the phases where it was requested. |
| **H3** | **Improve here, break there — silently.** Adds a new phase while deleting the old one, without saying so. | Added a phase, silently removed Phase 0 and transcript discipline. |
| **H4** | **Two sources of truth, no boss.** Same fact stated two ways in two places, no reconciliation. | A skill said "MCP or CLI"; permissions frontmatter required both. |
| **H5** | **My sandbox, shipped as everyone's library.** Personal identifiers cross the sandbox/library boundary. | Personal GitHub org, portal ID, channel ID, UUID, live customer name — all hardcoded in a shared plugin. |
| **H6** | **Write-to-the-trigger prose bloat.** Descriptions and files balloon past their contract. | A 180-word skill description; a single skill file at 704 lines against a 500-line ceiling. |
| **H7** | **Claimed, not verified.** The artifact asserts a behaviour that was never once exercised. Everything is verified by *reading*; nothing by *running*. | The PR rewrote the skill to be "read-only" and to have "dropped the Enrichment and Write-back tabs" — but the bundled export script the rep actually shares was never touched, and still renders both. Two runtime APIs the whole hand-off depends on were never called; a CRM field documented as writable was never written to. |

## How the tools map to the habits

| Habit | Caught by | How |
|-------|-----------|-----|
| H1 | `/ship-check` blocker ledger | Every review comment enumerated, addressed-or-not. Cannot merge past. |
| H2 | Good-brief template; `/ship-check`'s "hard half" check | The brief names the hard half; the report shows whether it was closed. |
| H3 | `/ship-check` diff-against-main | Every removal named. Every invariant listed pre-change and verified post-change. |
| H4 | `/ship-check` one-boss check | Every duplicated fact surfaced; every permission cross-referenced. |
| H5 | `/ship-check` scrub | Every personal identifier flagged. |
| H6 | `/ship-check` gates; `skill-lint` line-count and word-count | Enforced by the linter, not by prose. |
| H7 | `/ship-check` §5.3.7 (claim vs implementation); W06-01 | Every behavioural claim traced to the artifact that implements it. Nothing is "done" because it reads done. |

## Before you open a PR

1. Run `make test` locally (network-free). It must exit 0.
2. Run `/ship-check`. Address every `BLOCKERS OPEN` item — do not merge past
   an open blocker (H1).
3. If you touch a skill's `permissions.yml`, cite every permission in the
   matching `SKILL.md` body (H4).
