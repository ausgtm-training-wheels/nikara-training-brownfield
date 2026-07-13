---
name: deal-intel
description: Summarizes an open HubSpot deal's stage, owner, recent activity, and blocking risk factors so a rep can walk into a call prepared. Reads deal, contact, and pipeline records; writes nothing.
---

# deal-intel

A read-only HubSpot GTM skill. Given a deal name or ID, it produces a short
brief a rep can read in under a minute before a call: current stage, who
owns it, what happened recently, and what risks might stall it.

This skill never writes to HubSpot. Every permission it declares is a read
scope (see `permissions.yml` and the citations below).

## Phase 1: Look up the deal record

Uses `crm.objects.deals.read` — this permission is needed here because
Phase 1 fetches the deal's current stage, amount, close date, and owner
from the CRM. Without it, the skill cannot identify which deal it is
briefing on.

Resolve the deal from the user's input (name match if not given an exact
ID). If more than one deal matches, list the candidates and ask which one,
rather than guessing.

## Phase 2: Pull associated contacts

Uses `crm.objects.contacts.read` — this permission is needed here because
Phase 2 reads every contact associated with the deal to report who the
buying-committee members are and when each was last contacted.

For each associated contact, note their role on the deal (if set) and the
timestamp of their most recent logged activity.

## Phase 3: Place the deal in its pipeline

Uses `crm.pipelines.read` — this permission is needed here because Phase 3
reads the pipeline and stage definitions so the brief can say how far along
the deal is relative to the full pipeline, not just its raw stage name.

Compare the deal's current stage against the pipeline's stage order. Note
how long the deal has sat in its current stage compared to the pipeline's
typical time-in-stage, if that data is available on the stage record.

## Phase 4: Assemble the brief

Combine Phases 1-3 into a short brief:

- Deal name, stage, amount, close date, owner
- Buying-committee contacts and last-touch recency
- Stage position and time-in-stage flag if the deal looks stalled
- One line naming the single biggest risk to close, if one is evident from
  the data gathered (e.g. no contact touched in the last two weeks)

Present the brief as plain text. Do not fabricate a risk if none is evident
from the data — say "no obvious risk from CRM data" instead.

## Phase 8: Surface renewal risk signals

Uses `crm.objects.deals.read` — this permission is needed here because
Phase 8 compares the deal's close date against today to flag deals that are
overdue for a decision, surfacing renewal or stall risk beyond what
Phase 4's brief already covers.

For deals past their close date with no stage change in 30+ days, append a
one-line flag: "overdue — no stage movement in over 30 days." This flag
supplements the biggest-risk line from Phase 4; it does not replace it.

## What this skill does not do

- It does not write, update, or delete any HubSpot record.
- It does not send email, Slack messages, or any outbound communication.
- It does not guess a portal ID, contact, or deal that was not resolved in
  Phase 1 or Phase 2 — ambiguity is surfaced to the user, not silently
  picked for them.
