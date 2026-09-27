# Local validation, 2026-09-26

- `.venv/bin/python -m unittest discover -s tests -q`: 5 tests passed. Covers all templates at 203 and 300 dpi, ZPL command escaping, field overflow, HTML escaping, print Origin, copy count, and printer failure behavior. No real print job was sent.
- `npm --prefix web run build`: passed with Vite 7.3.6 and Vue 3.5.13. Output is in ignored `web/dist/`.
- `kubectl create --dry-run=client --validate=false -f k8s/zelabel.yaml -o name` and the Ruby YAML parser loaded four Kubernetes resources: Namespace, Deployment, Service, Ingress. `kubectl --context vnme apply --dry-run=client` could not reach the cluster API from the sandbox, so live schema and resource validation remain pending.
- `builderx --target production --context vnme` published API `2.0.0` and `latest` to Harbor. Registry index digest: `sha256:fbf8d85471d159a4f25642d6d0ea99db54f7691fd11dfeb981400bd7deca0359`.
- `builderx --target ui --context vnme` published UI `2.0.0` and `latest` to Harbor. Registry index digest: `sha256:48917158249ff2953e7be85053a06c0f0c794764b45314a33aa0b1b2b3cfe57c`.
- Both digests were read back from Harbor with `docker buildx imagetools inspect` and pinned in `k8s/zelabel.yaml`.
- Pulled the published amd64 images on local Docker: Nginx configuration passed `nginx -t`, and API `/api/healthz` and `/api/templates` returned 200.
- OIDC client creation, live login, iPhone usability, printer connection, and physical 4×2/2×2 print quality have not been validated. These are deployment review gates.

- Owner confirmation on 2026-09-26: printer resolution is 203 dpi; Pocket ID owns user authorization. Existing image DPI defaults and OIDC boundary already match.
- Owner confirmed `zd621.vanness.life` is the printer hostname. The API default and manifest already use it; no rebuild was required.
- Added a standalone, placeholder-only `zelabel-oidc` Secret template. A Ruby YAML check matched its three keys to the Deployment `secretKeyRef` entries, and `kubectl create --dry-run=client --validate=false` recognized the Secret. No credential values were generated or applied.
