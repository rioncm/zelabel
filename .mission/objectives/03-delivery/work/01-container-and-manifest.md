# Work Package — Container and manifest

Purpose: package the two app components and protect the public route with Pocket ID.

Context: `vnme`, Harbor public project, Traefik, cert-manager, Pocket ID issuer, and explicit review before deployment.

Work: configure builderx image targets; build/publish images; pin image digests; write Namespace, Deployment, Service, and Ingress; document Secret creation, physical stock changes, and smoke checks.

Artifacts: `Dockerfile`, `Dockerfile.ui`, `nginx.conf`, `.build/settings.conf`, `k8s/zelabel.yaml`, `docs/deployment.md`. Evidence: local build output, manifest parse, registry digests, then cluster and physical results. Dependencies: app build and OIDC client Secret.

Agent run 2026-09-26: artifacts prepared. Cluster API is inaccessible from the sandbox for dry-run verification. Deployment and physical printing are reserved for joint review.
