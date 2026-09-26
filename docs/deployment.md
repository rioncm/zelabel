# vnme deployment review

`k8s/zelabel.yaml` is prepared for review and has not been applied. The images are published as `harbor.vanness.me/public/zelabel-api:2.0.0` and `harbor.vanness.me/public/zelabel-ui:2.0.0`; the manifest pins their current digests. The `oidc` sidecar uses oauth2-proxy v7.15.4. Pocket ID is at `https://id.vanness.me`.

Before applying:

1. The owner confirmed the ZD621 is 203 dpi and its hostname is `zd621.vanness.life`, matching the manifest. Confirm both media sizes are available and the printer accepts raw ZPL on TCP 9100 from vnme nodes. Changing between 4×2 and 2×2 stock is a physical media operation; the UI cannot change the stock.
2. Create a confidential OIDC client in Pocket ID with callback `https://labels.vanness.life/oauth2/callback` and scopes `openid profile email`. Pocket ID controls which users may access the client. ZeLabel uses only the successful OIDC authentication result; it does not add group or local user checks.
3. Create Secret `zelabel-oidc` in namespace `zelabel` with keys `client-id`, `client-secret`, and a base64-encoded random 32-byte `cookie-secret`. Keep values outside Git. For example, create the namespace first and then use `kubectl --context vnme -n zelabel create secret generic zelabel-oidc --from-literal=client-id=... --from-literal=client-secret=... --from-literal=cookie-secret=...`.
4. Check DNS for `labels.vanness.life`, cert-manager issuer `letsencrypt`, and image pull access from Harbor.
5. Rotate the historical JSONBin credential in `app/config.yaml` if it is still live. It is excluded from new images but remains in repository history.

Build after review with `builderx --target production --context vnme` for the API and `builderx --target ui --context vnme` for the UI. Builderx publishes images. Verify image digests and refresh the manifest pins after any rebuild before applying `k8s/zelabel.yaml`. Use `kubectl --context vnme apply --dry-run=client -f k8s/zelabel.yaml` for local schema validation; an actual apply remains for joint review.

After deployment, verify browser sign-in and sign-out on an iPhone, unauthenticated access denial to `/api/templates` and `/api/print`, local SVG previews, and one physical print on each stock size. Inspect paper alignment, wrapping, and copy count. A TCP send acknowledges transport only; it does not prove that a physical label printed.
