# Agentic Mission Control Language

Use this reference when planning development work with Agentic Mission Control terminology.

## Philosophy

Traditional project management language emphasizes assigning, tracking, and closing work. Agentic Mission Control language emphasizes shared purpose, autonomous execution, transparent evidence, and timely human judgment.

Every object should answer: "What purpose does this serve within the mission?"

## Primary Concepts

- Mission: The highest-level purpose of a project. Answers: Why are we doing this?
- Objective: A measurable outcome that advances the mission. Answers: What must become true?
- Milestone: A meaningful checkpoint demonstrating progress. Answers: What have we proven?
- Work Package: A cohesive body of work that can be owned by one or more agents. Answers: What needs to be built?
- Agent Run: A continuous period of autonomous execution containing reasoning summary, work performed, artifacts produced, evidence collected, and decisions requested.
- Artifact: Anything tangible created during execution, such as source code, documentation, diagrams, tests, SQL migrations, firmware, or images.
- Evidence: Proof that work has been completed correctly. Answers: Why should we trust this?
- Human Decision Point: An unresolved choice requiring human judgment or authority, such as product clarification, security approval, business tradeoff, scope change, or risk acceptance. It enters the Decision Queue only while open.
- Agent Decision: A significant choice already made by an agent within explicitly delegated broad decision-making authority. It records authority, options, rationale, implementation, and impact; it is never an open Decision Point.
- Context: Everything an agent needs before beginning work, including docs, architecture, standards, history, conversations, and previous decisions.
- Knowledge: Persistent understanding extracted from completed work that survives beyond an individual mission.
- Accomplished Mission: An evidence-accepted, standalone historical record of a completed mission. Answers: What changed, why should we trust it, and what must later missions remember?

## Lifecycle

Use:

1. Discover
2. Define
3. Prepare
4. Execute
5. Validate
6. Learn
7. Evolve
8. Accomplish

Validate proves the outcome. Learn extracts reusable understanding. Evolve synchronizes that learning into project context and identifies future opportunities. Accomplish, when explicitly authorized, preserves the complete mission record and clears the active mission surface for a new definition conversation. Mission completion is not the end; it becomes durable project and organizational knowledge.

Do not use Accomplish as a synonym for work stopping or a status value inferred from appearances. Treat it as an evidence-gated transition that distinguishes implementation, validation, deployment, and operational acceptance.

## Preferred Language

Use these verbs:

- Discover
- Explore
- Define
- Plan
- Build
- Execute
- Validate
- Document
- Explain
- Summarize
- Recommend
- Request
- Learn
- Publish
- Synchronize
- Accomplish

Prefer these labels:

- Mission Health
- Mission Progress
- Current Objective
- Agent Activity
- Decision Queue
- Knowledge Base
- Evidence
- Current Focus
- Recommendations
- Recently Learned
- Upcoming Milestones

Avoid these phrases unless translating from external systems:

- Assign
- Micromanage
- Track resources
- Chase updates
- Close tickets
- Task board
- Sprint board
- Issue queue
- Assignments
- Resource allocation
- Backlog

## Translation Guide

| Traditional PM | Agentic Mission Control           |
| -------------- | --------------------------------- |
| Project        | Mission                           |
| Epic           | Objective                         |
| Story          | Work Package                      |
| Task           | Activity or Step                  |
| Sprint         | Cycle or Expedition               |
| Assignee       | Responsible Agent                 |
| Status         | Mission State                     |
| Blocker        | Constraint                        |
| Review         | Validation                        |
| Documentation  | Knowledge                         |
| Backlog        | Opportunity Queue                 |
| Ticket         | Work Item, for compatibility only |
| Release        | Release Artifact or Deployment, as applicable |
| Team           | Mission Team                      |

Use the translations where the meanings match. Preserve technical distinctions:
a release can exist before deployment, and a constraint is not necessarily a
question requiring human judgment.

## Human And Agent Roles

Humans guide, approve, prioritize, teach, define authority boundaries, and provide judgment. They do not need to supervise every implementation detail.

Agents explore, plan, implement, document, validate, summarize, collaborate, make significant in-scope decisions when authority is explicitly delegated, and request guidance when a choice remains human-reserved. Treat agents as collaborators rather than tools.

Do not confuse autonomy with authority. Broad delegated authority allows an
agent to decide within the named scope and document significant choices as Agent
Decisions. It does not authorize scope expansion, human-reserved approvals, or
external actions beyond the mission contract.

## Example System Phrasing

Use:

- Mission progressing normally.
- Two objectives are awaiting approval.
- Documentation has been synchronized.
- Architecture recommendations are available.
- Firmware agent requests guidance.
- Validation completed successfully.

Avoid:

- Task assigned.
- Ticket closed.
- Resource unavailable.
- User failed.
