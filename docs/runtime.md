# ZeLabel v2 runtime

The Vue/Vite UI is served by Nginx. Nginx forwards `/api/` to Flask on pod loopback. oauth2-proxy is the only public service target and sends authenticated requests to Nginx. There is one public host, `labels.vanness.life`.

The API loads YAML once at startup from `ZELABEL_CONFIG` (default `config/zelabel.yaml`). Each printer has a display name, hostname/IP, TCP port, DPI (203 or 300), media size (`4x2` or `2x2`), and `top_offset_dots` (0–24 in 203-dpi equivalent dots). `routing` maps every template media size to a matching printer. Templates remain in code. The browser shows the destination; the server selects it from the template, never from a client-supplied endpoint.

Complete `config/zelabel.yaml` before starting: replace `REPLACE_WITH_SECOND_PRINTER_HOST` and confirm the second printer's DPI and alignment. The existing ZD621 is assigned 4×2 stock. The file is included in the API image as a configuration template; production mounts a completed ConfigMap over it. Unresolved placeholders, invalid YAML, unsupported settings, missing routes, and media mismatches prevent startup. There is no fallback to the old `PRINTER_*` or `LABEL_TOP_OFFSET_DOTS` environment variables.

`APP_ORIGIN` remains an environment variable (default `https://labels.vanness.life`) and protects print POSTs with an Origin check. OIDC credentials remain in a Kubernetes Secret. There is no database or persistent volume.

Use the owner-confirmed Miniconda `zlabel` environment for local Python execution (the old `.venv` is broken). Run locally after installing the Python and Node dependencies:

```sh
conda activate zlabel
python -m pip install -r requirements.txt
python -m api
npm --prefix web ci
npm --prefix web run dev
```

For local print testing set `APP_ORIGIN=http://127.0.0.1:5173`. Printing sends a real job; use preview for ordinary development. The local development origin has no OIDC barrier. Production has no direct service route to UI or API.

The legacy `app/` and `compose.yaml` are retained as historical source only. The legacy `app/config.yaml` contains a JSONBin credential, which must be rotated if it remains valid. Neither image includes that directory. Preview is rendered locally and sends no label content to Labelary.

Verification (printer transport is mocked; tests send no physical jobs):

```sh
/opt/miniconda3/envs/zlabel/bin/python -m unittest discover -s tests -v
npm --prefix web run build
```

The tests use temporary configuration files and do not require completing the shipped hostname placeholder. For a different local config file, set `ZELABEL_CONFIG=/absolute/path/to/config.yaml`. Restart the API after any configuration change.
