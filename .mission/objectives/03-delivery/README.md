# Objective 03 — Cluster delivery

Outcome: functioning vnme deployment with a single public origin and isolated API sidecar.

Success criteria: API and UI images can be published to `harbor.vanness.me/public`; oauth2-proxy enforces Pocket ID OIDC; only its port is serviced; printer host is an environment variable; image digests, Kubernetes manifests, and operator steps are available for review. No database or Longhorn claim exists because no state is stored.

Milestones: container builds, Kubernetes syntax check, owner launch, DNS correction, then OIDC/iPhone/physical print validation. Evidence: [local validation](../../evidence/local-validation.md) and [live DNS diagnosis](../../evidence/2026-09-26-live-dns.md). Work Package: [container and manifest](work/01-container-and-manifest.md). Dependencies: Objective 02 and a Pocket ID client/Secret for launch.
