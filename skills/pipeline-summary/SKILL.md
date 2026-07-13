---
name: pipeline-summary
description: Rolls up an entire HubSpot pipeline into a stage-by-stage summary — deal count, total value, and owner load per stage — so a manager can spot a bottleneck at a glance. Reads only; writes nothing.
---

# pipeline-summary

A read-only HubSpot GTM skill. Given a pipeline name, it produces a
stage-by-stage roll-up: how many deals sit in each stage, their combined
value, and which owners carry the heaviest load — the report a sales
manager wants before a pipeline review meeting.

This skill never writes to HubSpot. Every permission it declares is a read
scope (see `permissions.yml` and the citations below).

## Phase 0: Read the brief

Read the user's request in full before touching HubSpot. Identify which
pipeline they mean, and whether they want the whole pipeline or a filtered
slice (e.g. "just this quarter's deals"). Do not call any tool until the
request is understood. This phase is never skipped, even for a routine
weekly request.

## Phase 1: Resolve the pipeline definition

Uses `crm.pipelines.read` — this permission is needed here because Phase 1
fetches the pipeline's stage list and stage order. Without it, the skill
has no frame to roll deals up into.

If the pipeline name is ambiguous, list the candidates and ask which one
rather than guessing.

## Phase 2: Pull every open deal in the pipeline

Uses `crm.objects.deals.read` — this permission is needed here because
Phase 2 reads every deal currently assigned to the resolved pipeline,
including its stage, amount, and owner ID.

Apply any filter the user named in Phase 0 (date range, deal type) before
grouping.

## Phase 3: Resolve owners for load reporting

Uses `crm.objects.owners.read` — this permission is needed here because
Phase 3 turns each deal's raw owner ID into a human-readable owner name so
the load-per-stage table is legible to the reader, not a list of IDs.

## Phase 4: Assemble the summary

Group the deals from Phase 2 by stage, using the stage order from Phase 1:

- Stage name, deal count, combined value
- Owner load: how many open deals each owner (resolved in Phase 3) carries
  in this pipeline, sorted highest to lowest
- One line flagging the stage with the largest deal count relative to the
  others, if the imbalance is clear from the data

Present the roll-up as a plain-text table. Do not fabricate a bottleneck
call if the distribution looks even — say "no stage stands out" instead.

## What this skill does not do

- It does not write, update, or delete any HubSpot record.
- It does not send email, Slack messages, or any outbound communication.
- It does not assume a single default pipeline — if the user does not name
  one and more than one pipeline exists, it asks in Phase 0 rather than
  picking one silently.
