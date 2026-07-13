---
description: Run all six /ship-check gates against the current branch's PR and print the fixed report + verdict (SETUP.md §5.1).
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*), Bash(git diff:*), Bash(git rev-parse:*), Bash(git branch:*), Bash(make lint:*), Bash(make review:*), Bash(bash -c:*), Read, Grep, Glob
---

# /ship-check

Nikara runs this before every merge from Week 2 on and reads this report, not diffs. Never skip a section, never soften a failing check, never print CLEAN unless every check actually passed.

## 0. Detect state

Run `gh pr view --json number,title,url,body,comments,reviews,headRefName`. If this fails (no `gh`, not authenticated, no PR open for this branch, no network), stop immediately, print:

```
# /ship-check report — TOOL FAILURE
<the gh error>
```

then run `bash -c 'exit 3'` and print `Exit: 3 (TOOL FAILURE)` as the last line. Do not run any of the six checks.

Otherwise capture the PR JSON, `git rev-parse --short HEAD`, the branch name, and `Ran at: <UTC timestamp now>`. The scrub-regex and blocker-keyword tables live in `.claude/commands/ship-check.data.md` — read it if present rather than inlining the tables here.

## Run the six checks, in order

Each check produces one `## N. <name>` section below. An empty check (nothing found) still prints its header, with body `No issues found` — never omit a section.

### 1. Blocker ledger

From `comments`/`reviews`: a comment is a blocker if it belongs to a `CHANGES_REQUESTED` review, or its body matches a keyword from ship-check.data.md's blocker-keyword table. For each blocker, search `gh pr diff` and the changed files for a matching hunk or a `[ship-check:addressed:<id>]` marker in the PR body to fill `Addressed?`. No evidence → `NO`, and the check fails. Emit exactly:

```
### Blocker ledger
Reviewer blockers found: N (open: K, addressed: N-K)

| # | Author | Blocker | Addressed? | Evidence |
|---|--------|---------|------------|----------|
| 1 | @author | "first 100 chars" | NO | — |

**Unresolved blockers must be addressed before merge:**
- #1 — @author — "..."
```

### 2. Diff against main

From `gh pr diff` and `git diff main...HEAD --name-status`, one row per file: `File | Status | Intended? | Summary`. `Intended?` is `YES` if covered by the PR body's stated scope, else `UNINTENDED`. Separately call out any `D` status or any hunk removing ≥5 non-blank lines, regardless of intended status. Emit exactly:

```
### Diff against main
Files changed: N (added: A, modified: M, deleted: D)

| File | Status | Intended? | Summary |
|------|--------|-----------|---------|

**Callouts:**
- <file>: N lines removed. Deleted content: <what>. Was this intentional?
```

### 3. One boss

Across every changed file, extract candidate facts (frontmatter values, headings, table rows, permission declarations, tool names, HubSpot property names, phase numbers) and find duplicates by exact-string and structured semantic match (e.g. a permission declared in `permissions.yml` and restated in `SKILL.md` prose). Inconsistent duplicates fail the check. Emit exactly:

```
### One boss
Duplicated facts found: N (consistent: K, conflicting: N-K)

| # | Fact | Location A | Location B | Consistent? |
|---|------|-----------|-----------|-------------|

**Conflicts must be resolved before merge:**
- #1 — pick the boss and remove the duplicate.
```

### 4. Scrub

Run every regex in ship-check.data.md's scrub table across every text file in the diff, resolving `<APPROVED_ORG>` from `.ship-check/config.yml`'s `approved_org` and the do-not-ship list from `.ship-check/live-names.txt`. Every hit fails unless the file's top line reads `<!-- ship-check:scrub:exempt reason=... -->`. Emit exactly:

```
### Scrub
Hits: N

| # | Pattern | File:Line | Match | Exempt? |
|---|---------|-----------|-------|---------|

**Every hit must be removed or exempted with reason before merge.**
```

### 5. Least privilege

For each skill in the diff with a permissions declaration (`permissions.yml` or SKILL.md frontmatter), list every declared permission/tool and search the SKILL.md body for a citation (a paragraph, list item, or code fence explaining why and where it's used). No citation → fails. Emit exactly:

```
### Least privilege
Skill: <name>

| Permission | Cited in SKILL.md? | Where | Notes |
|-----------|---------------------|-------|-------|

**Uncited permissions must be removed or justified before merge.**
```

### 6. Gates

Run `make lint` and `make review`. Capture stdout/stderr; either non-zero fails the check. Translate common failure lines into one plain-English sentence each (line-count over ceiling, description over word ceiling, missing citation, phase gap) — Nikara reads the translation, not the raw output. Emit exactly:

```
### Gates
make lint: PASS|FAIL (exit N)
  <raw finding line, if any>

make review: PASS|FAIL (exit N)

**Translation:**
- <plain-English sentence per raw finding>
```

## Assemble the report

Print, in this exact order, never omitting a section:

```
# /ship-check report — <PR title> (#<PR number>)
Ran at: <UTC timestamp>
Branch: <branch> → main
Commit: <short SHA>

## 1. Blocker ledger
<§1 output>

## 2. Diff against main
<§2 output>

## 3. One boss
<§3 output>

## 4. Scrub
<§4 output>

## 5. Least privilege
<§5 output>

## 6. Gates
<§6 output>

## Verdict
<verdict block>
```

## Verdict + exit

- All six checks passed → `**Verdict: CLEAN** — every check passed. Safe to merge.`
- Any of checks 1–5 has an unresolved item, or gates failed → `**Verdict: BLOCKERS OPEN** — the following must be resolved before merge:` + a numbered list pulled from every failing check.
- A check produced findings needing judgement (e.g. a duplicate fact that might be intentional) and nothing else failed → `**Verdict: NEEDS HUMAN DECISION** — the following need coach input:` + the ambiguous findings.

Map the verdict to an exit code — CLEAN: 0, BLOCKERS OPEN: 1, NEEDS HUMAN DECISION: 2 — then, as the final tool call, run `bash -c 'exit N'` and print `Exit: N (<VERDICT>)` as the report's very last line. A CLEAN verdict must never be printed while any check actually failed.

## CHANGELOG

A new check is a new or extended numbered section above, never a rewrite (§5.5, SHIP-05).

- **v1 (baseline):** checks 1–6 as specified in this file — blocker ledger, diff against main, one boss, scrub, least privilege, gates.
- **Week 3:** enriches §5 (least privilege) with a full input/output/side-effect table per permission — not a new section.
- **Week 4:** extends §4 (scrub)'s regex list in ship-check.data.md with any literal the plugin promotes to a shared invariant.
- **Week 5:** enriches §3 (one boss) into "one boss + convergence" — does every phase's stated output feed the next phase's stated input?
- **Week 6:** Nikara designs and adds one new check herself.
- **Week 7:** adds the ownership-map check at spec level (used with `/workflows`, not on every PR).
