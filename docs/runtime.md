# ZeLabel v2 runtime

The Vue/Vite UI is served by Nginx. Nginx forwards `/api/` to Flask on pod loopback. oauth2-proxy is the only public service target and sends authenticated requests to Nginx. There is one public host, `labels.vanness.life`.

The API sends ZPL over TCP to `PRINTER_HOST` (default `zd621.vanness.life`) on `PRINTER_PORT` (default 9100). `PRINTER_DPI` defaults to the confirmed 203 dpi. `APP_ORIGIN` defaults to `https://labels.vanness.life` and protects print POSTs with an Origin check. Templates are code, so there is no database or persistent volume.

Run locally after installing the Python and Node dependencies:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m api
npm --prefix web ci
npm --prefix web run dev
```

For local print testing set `APP_ORIGIN=http://127.0.0.1:5173`. Printing sends a real job; use preview for ordinary development. The local development origin has no OIDC barrier. Production has no direct service route to UI or API.

The legacy `app/` and `compose.yaml` are retained as historical source only. The legacy `app/config.yaml` contains a JSONBin credential, which must be rotated if it remains valid. Neither image includes that directory. Preview is rendered locally and sends no label content to Labelary.
