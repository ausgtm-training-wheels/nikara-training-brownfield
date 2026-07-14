# CLAUDE.md — nikara-training-brownfield invariants

This repo is a teaching artifact. Every contributor — including Claude — must
hold these seven invariants. `/ship-check` and `make lint` / `make review`
enforce them mechanically; this file is the human-readable source.

## The seven invariants

1. **Length ceiling.** Every skill's `SKILL.md` must be under 500 lines.
   Every skill description must be under 60 words.

2. **Permission citation.** Every permission declared in a skill's
   `permissions.yml` must be cited in that same skill's `SKILL.md` body —
   a line explaining why the permission is needed and where it is used.

3. **No personal identifiers.** No file in this repo may contain a personal
   GitHub org, a personal portal ID, a personal Slack channel ID, a personal
   UUID, or a `/Users/<name>/` path. This repo is portable — anyone can fork
   it and it must still work.

4. **Phase 0 is mandatory.** Every skill declares phases numbered 0..N with
   no gaps. Phase 0 is "read the transcript / read the brief". Phase 0 is
   not optional and must not be removed by any later change.

5. **One boss per fact.** Every changed fact is owned by exactly one file.
   If the same fact must appear in two places, the top of the file that is
   NOT the source of truth carries a comment naming the one boss file.

6. **Claims must be true of the code.** Every behavioural claim in a
   `SKILL.md` — what the skill renders, reads, writes, or says it never
   does — must be true of the artifact that implements it. If the SKILL.md
   describes runtime behaviour, the bundled script or asset must agree.
   Rewriting a description without changing the code it describes is a
   broken invariant, not a docs change.

7. **Permissions obey this file, not just the prose.** A permission must be
   allowed here, not merely cited in the SKILL.md. Bare interpreters and
   shell wildcards (`Bash(python3 *)` and similar) are forbidden: ship a
   `bin/` wrapper and declare that instead. A citation justifies why you
   want a permission, not that you may have it.

These are exactly what `tools/skill-lint` and `tools/skill-review` check
(see `Makefile`), and exactly what the planted PRs in this repo violate.
