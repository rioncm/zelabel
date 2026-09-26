---
name: mission-control
description: Plan, resume, maintain, and archive development missions using .mission records and Mission Status v1. Use for Mission Control planning, mission progress or decision updates, "Mission accomplished", archival, and resumption from accomplished history.
---

# Mission Control

Use Mission Control to connect development outcomes, accepted evidence, decisions, and durable knowledge. Preserve its vocabulary: Mission, Objective, Milestone, Work Package, Agent Run, Artifact, Evidence, Human Decision Point, Agent Decision, Context, and Knowledge.

## Select The Work

Start with the user's requested operation and the repository's current mission records. A progress question, terminology explanation, or skill review does not itself call for a new mission, a rewritten plan, or archival.

Read only the references needed for the operation:

| Operation | Reference |
| --- | --- |
| Write a substantial plan or explain terminology | [Mission language](references/mission-language.md) |
| Create or reorganize `.mission/` | [Folder layout](references/mission-folder-layout.md) |
| Interpret, create, migrate, or update status; resume a mission; reconcile Human Decision Points or multiple status writers | [Status management](references/mission-status-management.md) |
| Make or record a significant choice under delegated broad authority | [Agent Decision](references/agent-decision.md) |
| Audit completion, archive, correct history, or resume from an accomplished mission | Read [Mission Accomplished](references/mission-accomplished.md) completely; use its archival procedure only when archiving |

For repository work, read local instructions and `.mission/README.md` first, then the relevant Objective, Work Package, decisions, and Evidence. Use `status.json` to locate current work; verify its claims against those durable records and current repository facts.

## Plan Or Refine A Mission

1. State the Mission's outcome and why it matters.
2. Define Objectives as measurable outcomes. Keep them independent where practical; put implementation steps in Work Packages.
3. Establish Milestones as proven capabilities, with expected Evidence. Include dates only when they are real constraints.
4. Shape Work Packages with purpose, context, artifacts, validation, dependencies, and relevant Agent Run notes. Include ownership only when useful.
5. Separate required missing context from optional background. Reference authorized credential retrieval procedures rather than copying secret values into mission files.
6. Classify decisions using the authority rules below. Make human questions concrete, with the impact and timing of each choice.
7. Define what Evidence will make each outcome trustworthy and what reusable Knowledge should survive it.
8. For repo-local mission planning, create `.mission/` if absent; otherwise update the existing structure. Keep the Mission in its README, Objectives and Work Packages under `objectives/`, and mission-wide Evidence, Knowledge, decisions, and Context in the folders defined by the layout reference.
9. Create or reconcile `status.json` using Mission Status v1 after updating the durable records. Keep optional presentation settings, including `short_name`, in `settings.json`.

Adapt the plan to the request. A substantial plan normally covers Mission Intent, Objectives, Milestones, Work Packages, Context Needed, Human Decision Points, delegated Agent Decision Authority, Execution Sequence, and Knowledge To Capture. Omit empty sections and avoid repeating the same plan in several files; link to the authoritative record.

Use Discover, Define, Prepare, Execute, Validate, Learn, Evolve, and Accomplish to describe the lifecycle. Accomplish requires the authority and evidence gates below; it is not an automatic final step of every work package.

## Resume Or Maintain A Mission

1. Follow the current Objective and relevant Work Package from the mission README and status. Reconcile stale summaries with accepted decisions, Evidence, and current files before choosing the next action.
2. Continue the authorized work from its existing success criteria. Do not restart planning or reopen settled decisions merely because a new agent run began.
3. Keep implementation progress and validation results in the relevant Work Package, Agent Run notes, and Evidence. Update mission status only for a material mission-level change, following the status reference.
4. Update affected documentation and retained Knowledge when the work changes what future agents need to know. Distinguish planned, implemented, validated, deployed, and accepted outcomes.

If the active surface is `awaiting_definition`, use retained Context, Knowledge, and accomplished history to establish the next mission contract with the user. An already supplied brief can provide that definition; do not invent objectives from an opportunity list or reactivate an archived Objective.

## Decision Authority

Classify the choice before choosing a record:

- **Routine, low-impact implementation choice within the request:** proceed without a durable decision record or a new approval step.
- **Significant choice within explicitly delegated broad decision-making authority:** decide and promptly record it under `.mission/agent-decisions/` using the Agent Decision reference. Record implementation state separately; a decision does not prove delivery.
- **Choice that still requires human judgment or authority:** create a Human Decision Point under `.mission/decision-points/`, with an explicit lifecycle status. Examples include unresolved product intent, scope changes, risk acceptance, and external actions outside existing authorization.

Use authority already provided by the user's instructions or accepted mission contract. Do not ask again for an action already authorized within that scope. An Agent Decision record never supplies or expands authority. Broad delegation does not override human-reserved choices or authorize unrelated external actions.

Only Human Decision Point files with `status: open` belong in `status.json.open_decision_points`. Preserve resolved, deferred, and superseded decisions as history. Keep Agent Decisions out of the human Decision Queue.

## Mission Accomplished

Run the archival transition when the user explicitly declares the Mission accomplished or asks for archival, or when the active mission contract explicitly authorizes automatic archival after named completion evidence is present. Apparent completion, paused work, or a request to tidy `.mission/` does not supply that authority.

Treat completion as an evidence gate. If the audit finds a meaningful contradiction with the accepted mission contract, complete the unaffected audit and documentation work, then report the discrepancy and request human judgment before archiving.

Follow the ordered procedure in [Mission Accomplished](references/mission-accomplished.md): audit, synchronize learning and documentation, select a unique archive identity, protect unrelated work and secrets, copy and verify the complete mission record, and only then retire its active files. Keep implementation artifacts outside `.mission/` in place. Archival does not itself authorize commits, tags, pushes, branch deletion, or publication.

After verification, leave the active surface `awaiting_definition`, retain cross-mission Context and Knowledge, and index the accomplished history. Do not invent the next Mission. Correct history through dated notes rather than silently rewriting archived facts.

## Quality Bar

Make the next authorized action clear: what outcome matters, what Evidence supports it, which human judgment is still needed, and what Knowledge should remain. Keep status a current navigation snapshot rather than evidence, history, a heartbeat, or a coordination lock. Use mission terminology without obscuring concrete technical meaning or the user's chosen language.
