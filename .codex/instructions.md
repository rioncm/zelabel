# Agent Instructions

- Read `.codex/CONTEXT.md` before making broad changes.
- Read `.codex/about.md` for collaboration preferences.
- Follow `.codex/coding-style.md` for engineering style.
- Before executing project code, confirm the required execution environment. 
- If the required execution environment it is not documented in `.codex/CONTEXT.md`, request the necessary information before proceeding.
- Prefer current repo patterns over introducing new abstractions.
- Keep edits scoped to the user's request and the surrounding code.
- Preserve user work in a dirty tree. Do not revert unrelated changes.
- Update `.codex/CONTEXT.md` when a durable repo fact becomes important for
  future work.
- Validate changes with the narrowest useful command and record any command
  that future sessions should reuse.
