# ZeLabel v2

A mobile first label composer for the household Zebra ZD621. It includes four layouts for storage boxes, jars and cans, to do lists, and project cards on 4×2 or 2×2 direct thermal stock. The browser previews labels locally before sending ZPL to the printer.

The production design is one `labels.vanness.life` origin with a Vue UI, Flask API sidecar, and Pocket ID OIDC proxy. See the [mission](.mission/README.md) for scope and status, [runtime guide](docs/runtime.md) for local use, and [deployment guide](docs/deployment.md) for the vnme review gates.

The historical v1 app remains in `app/`; v2 images exclude it. The owner launched the app in vnme on 2026-09-26. See the [live DNS incident evidence](.mission/evidence/2026-09-26-live-dns.md) for the interface timeout correction and remaining validation.
