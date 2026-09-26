# Mission Status Management

Use this reference whenever creating, interpreting, migrating, or updating `.mission/status.json`; resuming a mission; changing Decision Point lifecycle; or considering multiple status writers.

## Version 1 Contract

Use this shape for every new or migrated mission:

```json
{
  "schema_version": "1",
  "mission_state": "defined",
  "mission_health": "unknown",
  "current_objective": null,
  "current_focus": null,
  "recommended_next_action": null,
  "open_decision_points": [],
  "updated_at": null,
  "updated_by": null
}
```

Keep every key present. `schema_version` is the string `"1"`; state and health
use the enums below; `open_decision_points` is always an array of path strings.
The remaining fields accept strings or `null` when no truthful value is known.

## Semantics

- Use `mission_state`: `defined`, `active`, `waiting`, `validating`, `complete`, or `awaiting_definition`.
- Use `mission_health`: `unknown`, `normal`, `attention`, or `blocked`.
- Keep lifecycle and health separate. Waiting can be healthy; active can need attention.
- Point `current_objective` to a repository-relative directory such as `.mission/objectives/01-foundation` or use `null`.
- Keep `current_focus` to one immediate outcome and `recommended_next_action` to one concrete resumption step.
- Keep `open_decision_points` equal to all and only durable Human Decision Point files in the active `.mission/decision-points/` whose lifecycle status is `open`. Use repository-relative paths without duplicates. Exclude accomplished history and Agent Decisions.
- Use an ISO 8601 timestamp for `updated_at` and an attributable human, agent, or system identity for `updated_by`.

Derive human attention when health is `attention` or `blocked`, or when open decisions exist. Do not persist `attention_required`.

Publish live agent activity as Agent Run events or notes. Do not persist `active_agent_runs`; status is not a heartbeat, lease, or process registry.

## Update Protocol

Update status only for a material mission-level change:

1. Read the current file immediately before editing.
2. Read the current Objective, when present, and supporting Decision Point, Evidence, or mission contract.
3. Update the durable records first, then change only fields supported by that context.
4. Update `updated_at` and `updated_by` in the same write.
5. Use atomic replacement when available; it prevents partial files, not competing writers from overwriting one another.
6. Re-read the file, validate JSON and enums, and verify referenced paths.

Keep routine implementation activity in Work Packages, Agent Run records, and Evidence. Avoid status churn.

## Evidence Rules

Treat every snapshot value as a claim, not proof:

- Support `mission_health: normal` with recent Evidence appropriate to the current Objective.
- Pair `mission_health: blocked` with a documented constraint or open Decision Point.
- Use `mission_state: validating` while checking claimed outcomes against success criteria.
- Write `mission_state: complete` only when accepted Evidence satisfies the active mission contract.
- Do not infer archival authority from `complete`; follow `mission-accomplished.md`.

## Decision Point Lifecycle

Use one canonical lifecycle state in YAML frontmatter for each Human Decision Point file under `.mission/decision-points/`:

- `open`: human judgment is required now.
- `resolved`: outcome and rationale are recorded.
- `deferred`: no current judgment is required; record the reconsideration trigger.
- `superseded`: another named decision or contract replaced the question.

```markdown
---
status: resolved
resolved_at: 2026-07-17
resolved_by: user
---

# Decision Point: Authentication Contract
```

When a decision changes state, update the durable file first, reconcile `open_decision_points` in the same controlled change, and update health or next action only when materially affected. Never treat folder presence as open status.

Agent Decisions use the separate `.mission/agent-decisions/` record defined by
`agent-decision.md`. They document significant choices already made under
delegated authority, have no open lifecycle, do not derive human attention, and
must not be copied into the Decision Queue. If an apparent Agent Decision still
needs approval, reclassify it as a Human Decision Point before acting.

## Migration

Readers may accept older minimal and `pilot-1` files temporarily. Writers emit version 1.

For `pilot-1`:

1. Set `schema_version` to `"1"`.
2. Remove `attention_required` and derive attention from health and open decisions.
3. Remove `active_agent_runs` and publish run activity through events or Agent Run notes.
4. Reconcile open decisions against explicit file lifecycle.
5. Add missing required keys using the types above: derive state from the mission contract, use `unknown` for unestablished health, reconcile the decision array, and use `null` for unknown nullable fields.
6. Validate JSON, enums, attribution, and referenced paths.

For a legacy three-field placeholder, preserve truthful values and add the
remaining version 1 keys under the same rules. Do not invent prior attribution;
attribute the migration write itself with its actual identity and timestamp.
An inspection alone does not require migration.

## Multi-Agent Boundary

Use one status writer at a time. Let other agents publish Agent Run records, Evidence, Decision requests, and status recommendations for the writer to reconcile.

`updated_at` is not concurrency control. Never use status as a lease, mutex,
heartbeat, or work claim. If concurrent writes are necessary, that requires a
separately designed coordination mechanism with revisions and conditional
updates; do not introduce one as part of routine mission maintenance.

## Operating Mode Boundary

Mission Status answers what is true now. Operating Mode answers what behavior is permitted next. Do not embed autonomous continuation authority in `status.json`.
