# Builderx Contract

## Files

- Source: `helpers/originals/builderx.sh`
- Released executable: `helpers/released/builderx`
- Documentation: `docs/builderx.md`

Paths are relative to the Scriptorium repository root. Maintain the editable
source and affected documentation together. Release or install only when requested;
`cmp` differences can represent unreleased work and do not authorize synchronization.

## Settings

`builderx` reads `.build/settings.conf`.

Supported target keys:

- `REGISTRY`
- `IMAGE_NAME`
- `VERSION`
- `TAG_SUFFIX`
- `CACHE`
- `CONTEXT`
- `DOCKERFILE_DIR`
- `DOCKERFILE_PATH`
- `BUILD_CONTEXT`
- `BUILDER_NAME`
- `PLATFORM`
- `MIRRORS`

`builderx --setup` creates `.build/settings.conf`, migrates old flat settings
into target sections, and backfills missing keys in existing `[production]` and
`[development]` targets.

## Defaults

- Target: `production`
- Docker context fallback: `amd`
- Platform: `linux/amd64`
- Cache: enabled when `CACHE=true` and `--no-cache` is not passed
- Latest tag: enabled by default
- Combined Dockerfile/build-context default: `DOCKERFILE_DIR=.`
- Dockerfile override: blank `DOCKERFILE_PATH=`
- Build-context override: blank `BUILD_CONTEXT=`
- Default builder name: `pminc-builder-<context>`

Docker context precedence:

1. `--context NAME`
2. target `CONTEXT=`
3. built-in fallback `amd`

## Build Behavior

`DOCKERFILE_DIR` remains the backward-compatible default for both Dockerfile
resolution and the build context. A non-empty `DOCKERFILE_PATH` overrides the
Dockerfile path, and a non-empty `BUILD_CONTEXT` overrides the build context.

The effective build shape is:

```sh
docker buildx build --file \
  "${DOCKERFILE_PATH:-$DOCKERFILE_DIR/Dockerfile}" \
  "${BUILD_CONTEXT:-$DOCKERFILE_DIR}"
```

The script validates both effective paths before switching Docker context or
creating a builder. A normal build includes `--push`; it is not a local-only
validation command. `--bump` writes the selected target's version before the
build runs, so a failed build can still leave a version change.

The build passes `APP_VERSION="$VERSION"` as a build arg. Published tags use
`VERSION` plus normalized `TAG_SUFFIX`.

## Tags And Mirrors

Primary tags are emitted under `REGISTRY/IMAGE_NAME`.

If `MIRRORS` is a Bash array, each non-empty mirror gets the same published
version tag, optional `latest` tag, optional git SHA tag, and any extra tags.

Registry and mirror prefixes are normalized by removing `http://`, `https://`,
and trailing slashes. Tag suffixes such as `dev` are normalized to `-dev`;
explicit `-dev`, `.dev`, and `_dev` forms are preserved.

## Builder And Cache

The buildx builder must use the `docker-container` driver because registry
cache options require it.

If the configured or derived builder exists with another driver, `builderx`
removes and recreates it with `docker-container`.

Registry cache uses:

```text
REGISTRY/IMAGE_NAME:buildcache
```

## Validation

Checks from the Scriptorium root:

```sh
bash -n helpers/originals/builderx.sh
bash -n helpers/released/builderx
cmp -s helpers/originals/builderx.sh helpers/released/builderx
helpers/originals/builderx.sh --help
bash tests/test_builderx.sh
```

The fixture suite uses temporary projects and a fake Docker command. For a
release check, set `BUILDERX_HELPER` to the absolute path of the released or
installed helper when running that same suite. For additional setup checks,
run the source by absolute path from a temporary directory; do not mutate real
project settings for verification.
