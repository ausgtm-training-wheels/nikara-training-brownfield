---
name: fellow
description: Drafts a one-page account research brief for an upcoming call by pulling recent HubSpot activity and public company signals into a single read-only summary. Integrates with HubSpot via MCP or CLI.
---

# fellow

A read-only research-assistant skill. Given a company or contact name, it
produces a one-page brief combining recent HubSpot activity with public
signals (funding news, headcount changes, recent hires) so a rep walks into
a call with context beyond the CRM record.

This skill integrates with HubSpot via **MCP or CLI** — pick whichever
integration is available in the environment; `fellow` only needs one path
to reach HubSpot data.

## Phase 0: Read the brief

Read the user's request in full before touching HubSpot or any public data
source. Identify the company or contact the request is about, and confirm
whether the ask is a full brief or a narrower fact. Do not call any tool
until the request is understood.

## Phase 1: Pull recent HubSpot activity

Uses `mcp.hubspot.read` — this permission is needed here because Phase 1
fetches the account's or contact's recent HubSpot activity (notes, emails,
meetings logged).

Uses `cli.hubspot-cli.exec` — this permission is needed here because Phase 1
fetches the same recent HubSpot activity.

## Phase 2: Pull public signals

Search for recent public signals about the company: funding rounds,
headcount changes, and recent leadership hires. Cite the source for each
signal found; omit any signal that cannot be sourced.

## Phase 3: Assemble the brief

Combine Phases 1-2 into a one-page brief:

- Recent HubSpot activity summary
- Public signals found, each with its source
- One line noting anything that looks like a good conversation opener

Present the brief as plain text. Do not fabricate a signal that was not
found in Phase 2 — say "no notable public signal found" instead.

## What this skill does not do

- It does not write, update, or delete any HubSpot record.
- It does not send email, Slack messages, or any outbound communication.
- It does not guess a company or contact that was not confirmed in Phase 0.
