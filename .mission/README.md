# ZeLabel v2 household printing mission

## Mission intent

Deliver a mobile first household label composer for the Zebra ZD621, protected by Pocket ID, with 4×2 and 2×2 direct thermal layouts and review-ready vnme deployment artifacts. The household should be able to prepare and preview a label on iPhone 15 or 16 and send it to the printer through a single `labels.vanness.life` origin.

## Objectives and milestones

1. [Define the product contract](objectives/01-product/README.md): the current app is understood, label needs and constraints are explicit.
2. [Build the application](objectives/02-application/README.md): four templates, local preview, validated printing API, and mobile UI work together.
3. [Prepare cluster delivery](objectives/03-delivery/README.md): publishable API/UI images, OIDC sidecar, and Kubernetes manifests are reviewable.
4. Joint review and deployment: after the owner reviews evidence, verify OIDC, iPhone use, media calibration, and physical prints in vnme. No deployment is authorized by mission progress alone.

The active work is preparing and validating cluster delivery. [Architecture](knowledge/architecture.md), [review evidence](evidence/local-validation.md), [runtime guide](../docs/runtime.md), and [deployment guide](../docs/deployment.md) carry the detailed contracts. The owner confirmed [203 dpi](decision-points/01-printer-resolution.md), [Pocket ID access ownership](decision-points/02-pocket-id-access.md), and the [zd621.vanness.life hostname](decision-points/03-printer-hostname.md). No Human Decision Points remain open.

Agent decisions within the delegated v2 scope are recorded under [agent-decisions](agent-decisions/). No database or persistent volume is required. The new images exclude the legacy app and its credential-bearing configuration.
