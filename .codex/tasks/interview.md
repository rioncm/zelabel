# Interview

Use this task to interview the user about the current project at any point in
the project lifecycle.

The goal is to improve shared understanding, not to force a rigid intake form.
Ask a few high-signal questions, reflect back what you heard, and capture
durable facts in `.codex/CONTEXT.md` when the user wants that retained.

## When To Use

- A project has no README or useful context yet.
- `.codex/CONTEXT.md` is missing, sparse, stale, or uncertain.
- The user asks for orientation before implementation.
- The project direction, constraints, users, or technical approach may have
  changed.
- A new phase is starting and old assumptions need to be checked.

## If There Is No Project Context

Run a brief discovery interview to get the general shape:

1. What is this project for, and who uses it?
2. What does a successful first version or next milestone look like?
3. What are the most important files, systems, or workflows to understand?
4. What should an agent avoid changing casually?
5. How should changes be verified?

Keep the first pass compact. If the user gives enough to proceed, summarize it
and ask whether to save the durable parts in `.codex/CONTEXT.md`.

## If Project Context Exists

Read `.codex/CONTEXT.md` and any project README first. Then interview to
confirm understanding:

1. Summarize the current understanding in a few bullets.
2. Ask what is wrong, stale, or missing.
3. Ask whether any core direction has changed.
4. Ask whether verification, deployment, or external-system assumptions have
   changed.
5. Ask whether there are new "do not break" contracts.

After the user answers, update `.codex/CONTEXT.md` only with durable facts.

## Interview Style

- Ask one to three questions at a time.
- Prefer concrete questions over abstract categories.
- Use the user's own terminology when reflecting answers.
- Keep temporary uncertainty out of durable context unless it is useful as a
  warning.
- Do not overwrite existing context wholesale; patch the parts that changed.

## Output

End with:

- A short summary of what was learned.
- Any open questions.
- Whether `.codex/CONTEXT.md` was updated.
