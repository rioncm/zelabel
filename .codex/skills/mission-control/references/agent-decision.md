# Agent Decision: <short, specific title>

<!--
Use this record only for a significant decision made by an agent during a
Mission. A decision is significant when it changes system behavior, structure,
data, security, operations, or the direction of later work.

Keep the record brief and factual. Prefer plain terms. Do not use this template
for routine coding choices or for a question that still requires human judgment;
record the latter as a Human Decision Point.
-->

- **Date:** YYYY-MM-DD
- **Decision maker:** <agent identity>
- **Mission or objective:** <name or link>
- **Authority source:** <user instruction or mission contract granting broad decision-making authority>
- **Authority scope:** <the delegated boundary that contained this choice>

## Human/Agent Boundary

Use this template only when all of the following are true:

- a human or accepted mission contract explicitly granted broad decision-making authority;
- the choice is inside that delegated scope;
- the choice is significant enough to affect later work, behavior, structure, data, security, or operations; and
- the choice does not require a separate human approval, risk acceptance, scope expansion, credential grant, or external authorization.

Routine implementation choices within the user's request need neither this
record nor a Human Decision Point. For a significant choice that still needs
human judgment or authorization, create a Human Decision Point and pause only
the dependent action. Use authority already granted; do not request it again.

An Agent Decision record documents existing authority; it does not supply,
expand, or retrospectively imply authority. Recommendations that have not been
selected under delegated authority are not Agent Decisions. Once the agent
selects an option, create the record promptly even when implementation will
follow.

Store completed records under `.mission/agent-decisions/` with a sortable name
such as `01-storage-layout.md`. Agent Decisions are settled records, not open
questions, and must never appear in `status.json.open_decision_points`.

## Purpose

<What needed to be decided, and why did it matter?>

## Options Considered

- **<Option>:** <brief benefit or drawback>
- **<Option>:** <brief benefit or drawback>

## Decision Made

<State exactly what the agent chose.>

## Implementation State

<State whether implementation is planned, in progress, implemented, validated,
or superseded. Link evidence when available; do not imply completion from the
decision alone.>

## Rationale

<Explain briefly why this option best fit the accepted mission intent, constraints, and available evidence.>

## Impact

<Note the important result, tradeoff, or follow-up. Remove this section if there is no meaningful impact beyond the decision itself.>

## Related Files and Lines

- `<path>:<line>` — <how this file reflects or supports the decision>
- `<path>:<line>` — <how this file reflects or supports the decision>

If a later decision replaces this one, preserve this record and add a dated
supersession note linking to the newer Human Decision Point or Agent Decision.
