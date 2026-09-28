# vnme deployment review

The owner launched `k8s/zelabel.yaml` in vnme on 2026-09-26. Release 2.0.1 was rolled out on 2026-09-27 and observed at 1/1 available with a 3/3 Ready pod. The images are published as `harbor.vanness.me/public/zelabel-api:2.0.1` and `harbor.vanness.me/public/zelabel-ui:2.0.1`; the manifest pins their current digests. The `oidc` sidecar uses oauth2-proxy v7.15.4. Pocket ID is at `https://id.vanness.me`.

For a fresh installation or future change:

1. The owner confirmed the ZD621 is 203 dpi and its hostname is `zd621.vanness.life`, matching the manifest. Confirm both media sizes are available and the printer accepts raw ZPL on TCP 9100 from vnme nodes. Changing between 4×2 and 2×2 stock is a physical media operation; the UI cannot change the stock.
2. Create a confidential OIDC client in Pocket ID with callback `https://labels.vanness.life/oauth2/callback` and scopes `openid profile email`. Pocket ID controls which users may access the client. ZeLabel uses only the successful OIDC authentication result; it does not add group or local user checks.
3. Use the [OIDC Secret template](../k8s/secrets/zelabel-oidc-secret.example.yaml) to prepare `zelabel-oidc` in namespace `zelabel`. Its three `stringData` keys exactly match the Deployment references. Generate the cookie value with `openssl rand -base64 32`; use the Pocket ID client ID and client secret for the other keys. The example contains placeholders only and must not be applied. Keep a completed plaintext copy out of Git (`k8s/secrets/zelabel-oidc-secret.yaml` is ignored), or store the completed Secret encrypted using the vnme operations repository's SOPS workflow. Create the namespace before applying the completed Secret.
4. Check DNS for `labels.vanness.life`, cert-manager issuer `letsencrypt`, and image pull access from Harbor.
5. Rotate the historical JSONBin credential in `app/config.yaml` if it is still live. It is excluded from new images but remains in repository history.

Build or rebuild with `builderx --target production --context vnme` for the API and `builderx --target ui --context vnme` for the UI. Builderx publishes images. Verify image digests and refresh the manifest pins after any rebuild before applying `k8s/zelabel.yaml`. Use `kubectl --context vnme apply --dry-run=client -f k8s/zelabel.yaml` for local schema validation; review the intended change before applying it to the live deployment.

The API's `LABEL_TOP_OFFSET_DOTS` setting shifts the top rule and all template content downward by a number of 203 dpi dots. Release 2.0.1 sets it to `24` (about 3 mm) to address a clipped top line; the supported range is 0–24 dots to keep the lowest template field on the media. The SVG preview uses the same offset. A physical print is needed to confirm alignment. The UI offers a clear button inside each populated field and a Clear fields action that keeps the current template and copy count.

For live acceptance, verify browser sign-in and sign-out on an iPhone, unauthenticated access denial to `/api/templates` and `/api/print`, local SVG previews, and one physical print on each stock size. Inspect paper alignment, wrapping, and copy count. A TCP send acknowledges transport only; it does not prove that a physical label printed.

The initial interface timeout was caused by DNS: `labels.vanness.life` pointed through `proxy.vanness.life` to the unreachable `192.169.90.20`. The ZeLabel CNAME was changed to `traefik.vanness.me`, and the owner corrected the shared proxy A record. A normal HTTPS request now reaches `192.168.90.20` and redirects to Pocket ID. See [incident evidence](../.mission/evidence/2026-09-26-live-dns.md).
