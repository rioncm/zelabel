# Current app review, 2026-09-26

- `app/app.py` serves one Flask-rendered Bootstrap page and `/api/v1/templates` plus `/api/v1/print`. The form has no local preview and uses alerts for feedback.
- `app/mods/printctl.py` reads the printer from `app/config.yaml`, uses one hardcoded 4×2 geometry even though templates vary, and sends raw ZPL over TCP 9100. It reports a successful socket send as a print success.
- `app/mods/utility.py` renders through a `zpl` package. The template `justify` value is ignored, and width and height property names do not match the reader, making geometry unreliable. Text is logged.
- `app/mods/imgen.py` sends preview data to the external Labelary API and saves an image; v2 uses a local preview.
- `app/config.yaml` contains an old printer IP and a JSONBin key. The new images exclude it. Rotate the key if live; historical commits may also contain it.
- `compose.yaml` exposes the old app at `labels.vanness.life` with no OIDC enforcement. It is not the v2 deployment path.

The old app remains in `app/` as reference while v2 code lives in `api/` and `web/`.
