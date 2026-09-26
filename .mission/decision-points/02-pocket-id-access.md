---
status: resolved
resolved_at: 2026-09-26
resolved_by: user
---
# Human Decision Point — Who may print

The owner confirmed that Pocket ID controls authorized users. ZeLabel must accept the OIDC authentication result from `https://id.vanness.me` and must not add group checks, local user lists, or other OIDC-derived authorization data. The prepared oauth2-proxy sidecar enforces login before forwarding UI or API traffic. ZeLabel's API does not read or store OIDC identity claims.
