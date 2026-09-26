---
name: builderx
description: Maintain or use Scriptorium's builderx Docker buildx helper, including .build/settings.conf, targets, build paths, contexts, registry cache, tags, and version bumps.
---

# Builderx

Use this skill for work on the `builderx` helper in
`/Users/rion/VSCode/personal/Scriptorium`. When using it in another project,
read the reference and that project's settings; use `command -v builderx` to
identify the executable. Maintenance paths below belong to Scriptorium.

## Maintenance Workflow

1. For maintenance, work from the Scriptorium root and read operator docs first,
   then inspect the editable source and released copy:
   - `helpers/originals/builderx.sh`
   - `helpers/released/builderx`
   - `docs/builderx.md`
2. Compare behavior against the contract in [references/builderx.md](references/builderx.md).
3. Edit the source and affected documentation. Update the released or installed
   copy only when the user requests a release; source/release drift can be intentional.
4. Preserve `DOCKERFILE_DIR` as the backward-compatible combined default while
   allowing `DOCKERFILE_PATH` and `BUILD_CONTEXT` to override its two roles.
5. Validate edited shell files with `bash -n`. For build-path or setup changes,
   run `bash tests/test_builderx.sh`; it uses temporary settings and a fake Docker.
6. For setup changes, smoke test against a temporary directory so the real repo
   settings are not mutated.

## Review Priorities

- Settings migration and backfill in `builderx --setup`.
- Source/released drift.
- Documentation drift around path precedence, defaults, and effective build
  command.
- Docker context selection precedence.
- Registry cache requiring a `docker-container` buildx driver.
- Version bump behavior and target-specific `.build/settings.conf` updates.

## Avoid

- Do not rename the existing script paths as part of unrelated work.
- Do not run a real Docker build or push unless the user explicitly asks.
- Do not mutate a project's real `.build/settings.conf` for verification when a
  temporary fixture can prove the behavior.
