# Debug Pass Prompt

Start from the exact error, log, failing command, or user-observed behavior.

Work in this order:

1. Reproduce or inspect the failing boundary.
2. Identify the smallest relevant code path.
3. Patch the root cause without broad refactors.
4. Run the narrowest useful verification.
5. Record any durable debugging fact in `.codex/CONTEXT.md`.
