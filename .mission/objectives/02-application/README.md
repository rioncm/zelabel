# Objective 02 — Application

Outcome: iPhone friendly composition and preview with a validated print API.

Success criteria: Vue UI loads template metadata, supports all four layouts and copy count, previews without third party calls, and shows printer errors. API bounds input, escapes ZPL, sends to configurable TCP host, and has a health endpoint. Printing requires same origin; production routes both UI and API through OIDC.

Milestone: local API tests and UI production build pass. Evidence: [local validation](../../evidence/local-validation.md).

Work Packages: [UI](work/01-mobile-ui.md) and [API and labels](work/02-api-and-labels.md). Dependency: Objective 01.
