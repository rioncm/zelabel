# Agent Decision — One protected origin with three pod containers

- **Date:** 2026-09-26
- **Decision maker:** Codex
- **Mission or objective:** ZeLabel v2, Objectives 02–03
- **Authority source:** User asked to define and build v2, document decisions, and surface only critical decisions.
- **Authority scope:** App architecture and deployment design before joint review.

## Purpose

Choose how a separate API can remain on the UI host with Pocket ID protection.

## Options considered

- Flask template app with embedded API: minimal packaging but retains coupled UI and API.
- UI, API, and OIDC proxy in one pod: independent UI/API code with one protected host.

## Decision made

Use Vue/Vite served by Nginx, Flask API on pod loopback, and oauth2-proxy in the same pod as the only public Service target. Require Pocket ID OIDC for the public origin. Pocket ID owns the user access policy; the app applies no group or local user checks.

## Implementation state

Implemented locally and in review-only manifests. The owner confirmed the Pocket ID access boundary on 2026-09-26. OIDC login and cluster routing remain unvalidated.

## Rationale

This satisfies the user's API sidecar and one-host requirements while keeping both browser routes behind OIDC. A frontend framework supports the mobile composer without building a larger service stack.

## Impact

The cluster needs an OIDC client and Secret before deployment.
