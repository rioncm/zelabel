# Objective 03 — Cluster delivery

Outcome: review-ready vnme deployment with a single public origin and isolated API sidecar.

Success criteria: API and UI images can be published to `harbor.vanness.me/public`; oauth2-proxy enforces Pocket ID OIDC; only its port is serviced; printer host is an environment variable; image digests, Kubernetes manifests, and operator steps are available for review. No database or Longhorn claim exists because no state is stored.

Milestones: container builds, Kubernetes syntax check, human review, then a separately authorized deployment and physical test. Evidence: [local validation](../../evidence/local-validation.md) and later deployment evidence. Work Package: [container and manifest](work/01-container-and-manifest.md). Dependencies: Objective 02 and a Pocket ID client/Secret for launch.
