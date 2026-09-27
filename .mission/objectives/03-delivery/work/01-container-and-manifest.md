# Work Package — Container and manifest

Purpose: package the two app components and protect the public route with Pocket ID.

Context: `vnme`, Harbor public project, Traefik, cert-manager, Pocket ID issuer, and explicit review before deployment.

Work: configure builderx image targets; build/publish images; pin image digests; write Namespace, Deployment, Service, and Ingress; document Secret creation, physical stock changes, and smoke checks.

Artifacts: `Dockerfile`, `Dockerfile.ui`, `nginx.conf`, `.build/settings.conf`, `k8s/zelabel.yaml`, `k8s/secrets/zelabel-oidc-secret.example.yaml`, `docs/deployment.md`. Evidence: local build output, manifest parse, registry digests, then cluster and physical results. Dependencies: app build and OIDC client Secret.

Agent run 2026-09-26: artifacts prepared. Cluster API is inaccessible from the sandbox for dry-run verification. Deployment and physical printing are reserved for joint review.

Agent run 2026-09-26: added the placeholder-only OIDC Secret template and documented its keys and completion path. No real credential was created or applied.

Agent run 2026-09-26: after the owner launched the deployment, diagnosed the interface timeout as an incorrect DNS target and changed only the ZeLabel CNAME to Traefik. Live pod and OIDC redirect checks passed. See [incident evidence](../../../evidence/2026-09-26-live-dns.md).

Agent run 2026-09-26: owner corrected the remaining shared DNS record. An ordinary HTTPS request to ZeLabel now returns the Pocket ID redirect. Authenticated and physical-print acceptance remain open.
