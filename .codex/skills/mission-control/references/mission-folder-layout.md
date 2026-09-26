# Mission Folder Layout

Use this reference when creating or reorganizing `.mission` in a repository.

## Design Intent

The `.mission` folder is the mission operating layer for a repo. It should be easy for a human to scan and easy for an agent to traverse without special tooling.

The core rule is:

- Objectives define measurable outcomes; Work Packages contain the implementation work.
- Objective folders contain the files and folders needed for agentic development of that objective.
- Mission-wide evidence and knowledge live at the `.mission` root.
- Sortable names make navigation and intended sequence clear; explicit dependencies determine execution order.

## Default Layout

```text
.mission/
  README.md
  settings.json  # optional
  status.json
  accomplished/
    README.md
    mission.01/
      README.md
      status.json
      objectives/
      evidence/
      knowledge/
      decision-points/
      agent-decisions/
      context/
  objectives/
    01-foundation/
      README.md
      work/
        01-app-layout.md
        02-data-model.md
  evidence/
    01-foundation/
  knowledge/
    architecture.md
    runbook.md
  decision-points/
    01-auth-strategy.md
  agent-decisions/
    01-storage-layout.md
  context/
    repo-map.md
    environment.md
```

The tree illustrates the available locations, not a requirement to create
empty records or placeholder archives. Preserve an existing repository's
consistent naming and add folders as their records are needed.

## Root Files

### README.md

Describe the overall mission of the repo:

- Mission intent
- Current objectives
- Mission health or current focus
- How to navigate `.mission`
- Links to key evidence, knowledge, and decision points

### status.json

Use the complete Mission Status v1 shape in
[status management](mission-status-management.md). That reference defines the
fields, types, semantics, migration, and update protocol. Keep status a current
read model; do not add agent heartbeats, work claims, or duplicate attention flags.

### settings.json

Use this optional file for stable presentation metadata that is neither mission state nor evidence:

```json
{
  "schema_version": "1",
  "short_name": "BirdSong"
}
```

Keep `short_name` concise and recognizable in navigation. Preserve the first H1 in `.mission/README.md` as the complete mission title.

## Objectives

Use `.mission/objectives/<nn-slug>/` for each Objective and its Work Packages.

Name objective folders with two-digit order prefixes:

- `01-foundation`
- `02-authentication`
- `03-agent-runs`

Each objective should include:

```text
01-foundation/
  README.md
  work/
    01-app-layout.md
    02-navigation.md
```

The objective `README.md` should include:

- Objective intent
- Success criteria
- Milestones
- Dependencies
- Expected artifacts
- Expected evidence
- Open decision points

Each `work/*.md` file should include:

- Purpose
- Context needed
- Work steps
- Expected artifacts
- Evidence required
- Dependencies
- Decision points
- Agent run notes

## Evidence

Use `.mission/evidence/` for proof that work completed correctly. Group evidence by objective, agent run, or date depending on what will be easiest to retrieve.

Examples:

- Test output
- Screenshots
- Deployment notes
- Benchmark results
- Review notes
- Commit references

## Knowledge

Use `.mission/knowledge/` for durable documentation needed by future work.

Examples:

- Architecture notes
- Runbooks
- System diagrams
- Learned patterns
- Settled decisions
- Glossaries

## Decision Points

Use `.mission/decision-points/` for durable Human Decision Points. Give each
file an explicit YAML frontmatter `status` of `open`, `resolved`, `deferred`, or
`superseded`. Only `open` decisions require current human attention; preserve
the others in place as mission history. Objective READMEs and Work Packages can
link to these records. A question needing current human judgment belongs in a
durable file here so it can be represented in `status.json.open_decision_points`.

## Agent Decisions

Use `.mission/agent-decisions/` for significant choices made by an agent under
explicit broad decision-making authority. Read and use
`agent-decision.md` for each record. These are settled rationale and provenance,
not questions awaiting judgment: do not assign them Human Decision Point
lifecycle states and never include them in `status.json.open_decision_points`.

Create the record when the choice is made and distinguish the settled decision
from its implementation state. A decision does not prove implementation,
validation, deployment, or acceptance.

Record the source and scope of delegated authority. If the needed choice exceeds
that authority or requires human approval, create a Human Decision Point instead.
Do not record routine implementation choices merely to create an exhaustive log.

## Context

Use `.mission/context/` for mission-wide context that many objectives need:

- Repo map
- Environment setup
- Coding standards
- Constraints
- External systems
- Glossary

## Accomplished Missions

Use `.mission/accomplished/` for complete, readable records of accomplished missions. Maintain `.mission/accomplished/README.md` as the history index. For each archive, include its identifier and title, completion date, concise outcome, key artifact and evidence links, operational state or limitations, and relationship to later missions when known.

Follow the repository's existing archive naming convention. If it uses sequential identities such as `mission.01`, choose the next unused sequence. If no convention exists, establish and document a deterministic sortable convention. Never overwrite, merge into, or silently reuse an archive path.

Archive mission operating records from `.mission/`, including objectives, work packages, evidence, Human Decision Points, Agent Decisions, knowledge, context, debug notes, and final status. Keep implementation artifacts outside `.mission/` in place and link them from the archive. Treat accomplished history as immutable: add clearly dated correction or supersession notes instead of silently rewriting historical facts.

Read [Mission Accomplished](mission-accomplished.md) before creating, correcting,
or resuming from an archive. Reading history does not itself trigger archival.

## Awaiting-Definition Surface

After verifying an archive, keep the active layer small:

```text
.mission/
  README.md
  status.json
  settings.json            # retain if present
  accomplished/
    README.md
    mission.01/
  context/
    next-mission-brief.md  # optional
  knowledge/               # retained cross-mission knowledge only
```

State in `.mission/README.md` that the previous mission is accomplished and the
next mission awaits definition. Use the awaiting-definition status example in
[Mission Accomplished](mission-accomplished.md), with truthful attribution and
`null` focus and next action unless a definition conversation has established them.

Retain project-wide architecture, operational rules, constraints, and other cross-mission knowledge in active project documentation, `.mission/context/`, or `.mission/knowledge/`. Put noncommittal future possibilities in optional `.mission/context/next-mission-brief.md`. Do not create new objectives until a human-and-agent definition conversation establishes the next mission contract.

## Suggestions

- Keep objective folders small enough that an agent can read the objective README and relevant work file before acting.
- Use ordered filenames only where order matters.
- Prefer Markdown for human-readable plans and evidence summaries.
- Keep raw evidence files near a short Markdown index when the evidence is not self-explanatory.
- Use the accomplishment authority and evidence gates before archiving a Mission. Preserve superseded records as history without presenting them as current guidance.
