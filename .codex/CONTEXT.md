# Project Context

Use this file as the repo-local source of truth before broad exploration.
Record durable facts, verification commands, and contracts that future agent
sessions should preserve.

## What This Project Is

ZeLabel v2 is a Vue label composer with a Flask API that renders previews and sends raw ZPL to household Zebra printers. Templates have fixed 4×2 or 2×2 media sizes; YAML routes each size to a dedicated printer.

## Important Paths

- `api/`: active API, configuration validation, templates, and printer transport.
- `web/`: active Vue/Vite UI.
- `config/zelabel.yaml`: runtime configuration template, with an unresolved second-printer hostname.
- `k8s/zelabel.yaml`: plain manifests including the mounted configuration.
- `app/`: historical v1 only; excluded from v2 images.

## Runtime And Verification

- Runtime setup is documented in `docs/runtime.md`; the API image uses Python 3.13.
- The owner-confirmed local Python environment is Miniconda `zlabel` at `/opt/miniconda3/envs/zlabel` (Python 3.12). Run tests with `/opt/miniconda3/envs/zlabel/bin/python -m unittest discover -s tests -v`. Transport is mocked; no physical jobs are sent.
- UI build: `npm --prefix web run build` after `npm --prefix web ci`.
- On 2026-11-07 the existing `.venv` pointed to a missing Homebrew Python 3.14 installation. Use the confirmed Miniconda environment instead.

## External Systems

- vnme Kubernetes deployment; Pocket ID authentication via oauth2-proxy.
- Existing 203-dpi printer: `zd621.vanness.life`; second printer hostname and calibration remain unconfirmed.

## Do Not Break

- `ZELABEL_CONFIG` selects the YAML file, loaded and validated once at startup. Restart the API to adopt config changes. Legacy printer environment settings are no longer read.
- Keep credentials in the OIDC Secret. Keep printer endpoints server-side; clients select templates, and the server routes by size.
- Preview and ZPL share per-printer alignment in 203-dpi equivalent coordinates.
- Physical printing and live Kubernetes deployment require owner authorization.

## Current Notes

- Two-printer changes require new API/UI images and refreshed manifest digest pins before rollout. Existing pins still reference the previous release.
- Two-printer verification on 2026-11-07: all 13 Python tests passed in `zlabel`, the local npm production build passed, and `git diff --check` passed. Physical printer acceptance and image publishing/deployment remain pending.
