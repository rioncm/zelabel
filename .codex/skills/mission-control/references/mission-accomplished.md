# Mission Accomplished Transition

Use this ordered procedure for archival after the authority gate in
[`SKILL.md`](../SKILL.md) passes. Completion review may use the audit without
initiating archival. For historical reading or corrections, use the guidance
at the end of this reference. Treat archival as a reversible preservation
operation on mission records inside `.mission/`; keep implementation artifacts
elsewhere in the repository in place.

## 1. Audit Completion

Read current repository files rather than relying on chat memory:

- active `.mission/README.md` and `status.json`;
- every objective README and work package;
- open Human Decision Points, Agent Decisions, expected artifacts, expected evidence, context, knowledge, and relevant debug notes;
- project, operator, deployment, runbook, repo-map, and user documentation relevant to the mission.

Confirm every required objective is complete; documented artifacts exist;
required validation and evidence support the outcome; Human Decision Points
have explicit non-open lifecycle states; Agent Decision implementation states
are truthful; and documentation matches delivery. Required operational or
deployment work must be complete unless the accepted mission contract
explicitly leaves it outside the completion gate. Label such external actions
with their owner and remaining work. Parse `status.json` and reconcile it with
durable records.

Distinguish implementation complete, validated, deployed, and operationally
accepted. If a meaningful contradiction remains, finish unaffected audit and
documentation work, present the discrepancy, and request human judgment before
writing the archive. Do not waive required evidence by relabeling missing work
as an opportunity or external action.

## 2. Learn And Synchronize

Make the mission record understandable without its originating conversation. Record:

- mission intent and final outcome;
- each objective and its accepted evidence;
- delivered artifacts at their current repository paths;
- resolved Human Decision Points, Agent Decisions, and superseded approaches;
- validation results, deployment state, limitations, and external actions;
- reusable knowledge and operating instructions;
- deliberately out-of-scope follow-on opportunities.

Synchronize root project documentation, `.codex/CONTEXT.md`, repo maps, runbooks, and user documentation where current evidence makes them stale. Remove disproven labels such as active, pending, missing, or not implemented.

Classify knowledge before archival:

- archive mission-specific knowledge with the mission;
- promote stable project-wide knowledge into active project documentation or retained `.mission/context/` and `.mission/knowledge/`;
- record possibilities in a next-mission brief without making commitments.

## 3. Select The Archive Identity

Inspect `.mission/accomplished/` and use its documented convention. For sequential names, choose the next unused identity; do not fill a gap if that could obscure history. If no convention exists, establish a deterministic sortable convention and explain it in `.mission/accomplished/README.md`.

Never overwrite, merge into, or reuse an existing archive directory. Maintain the accomplished index with the archive identity and title, completion date, concise outcome, artifact and evidence links, operational state or limitations, and relationship to later missions when known.

## 4. Protect Secrets And Integrity

Inspect `git status` before editing and preserve unrelated user changes. Scan mission content for credentials, tokens, private keys, connection strings, personal data, and other unsafe durable material. Exclude or redact secrets and record only the authorized retrieval location or process.

Record a current commit identifier when it improves traceability, but state that it does not capture uncommitted work. Do not commit, tag, push, delete branches, or publish unless the user explicitly authorizes it.

## 5. Stage, Verify, Then Retire

Perform these steps in order:

1. Create the unique archive directory.
2. Copy the complete mission-specific operating record into the archive's documented layout, including the context and knowledge needed to understand it independently. Retain reusable copies on the active surface. Do not recursively copy `.mission/accomplished/` into the new archive or introduce an extra nested snapshot layer unless the repository convention requires one.
3. Finalize the copied README and status so they identify the mission as accomplished, give the completion date, and link final evidence and implementation artifacts. Keep archived status within the v1 schema with `mission_state: "complete"`; put archival metadata in the README or index. Rebase moved record links and status paths to their archived destinations so they do not resolve to a later mission's active files. Preserve the source facts and treat these finalization edits as intentional differences from the active record.
4. Verify expected files, objective counts, evidence, links, JSON validity, secret handling, and standalone readability.
5. Compare the staged archive with active source material, account for intentional finalization edits, link updates, and secret redactions, and resolve every unexplained omission or difference.
6. Only after the comparison passes, remove or replace archived mission-specific files on the active surface.

Never begin with destructive cleanup. Preserve important debug records as historical context, not current guidance. Never archive only README and status while leaving the mission's evidence, Human Decision Points, or Agent Decisions behind. Preserve facts as known at completion; make later corrections through dated notes.

## 6. Prepare For Mission Definition

Leave:

- `.mission/README.md` stating the previous mission is accomplished and the next mission awaits definition;
- valid `.mission/status.json` with no current objective;
- existing `.mission/settings.json`, when present;
- `.mission/accomplished/README.md` and every archive;
- retained cross-mission context and knowledge;
- optionally, `.mission/context/next-mission-brief.md` with stable capabilities, current state, constraints, opportunities, and definition questions.

Use Mission Status version 1:

```json
{
  "schema_version": "1",
  "mission_state": "awaiting_definition",
  "mission_health": "normal",
  "current_objective": null,
  "current_focus": null,
  "recommended_next_action": null,
  "open_decision_points": [],
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_by": "<identity>"
}
```

Do not invent objectives or convert opportunities into commitments. Invite a human-and-agent definition conversation about intent, desired outcome, constraints, and acceptable evidence.

## 7. Validate And Report

Before declaring the transition complete, confirm:

- the archive path is unique, complete, indexed, and link-valid;
- archive and active JSON parse and describe consistent states;
- project and mission documentation agree;
- no archived objective appears active;
- durable cross-mission knowledge remains discoverable;
- no secret entered durable history;
- the active surface is ready for definition;
- repository diffs contain only intended transition changes.

Report the archive path, documentation synchronized, knowledge promoted, future opportunities, operational or deployment state, validation performed, and the new mission state. Do not say "Mission accomplished" while required archival or documentation work remains.

## Reading Or Correcting Accomplished History

Read the accomplished index, selected archive, and retained project context to
answer historical questions or prepare the next definition. Treat archived
status as a completion snapshot, not current authority or an active work claim.
Verify facts that may have changed against the live repository before using
them for new work.

For a correction, preserve the original facts as recorded and add a dated note
describing the correction or supersession, supporting evidence, and related
mission. Do not rerun the archival transition, reuse its identity, or restore
its Objectives to active status merely to read or correct it.
