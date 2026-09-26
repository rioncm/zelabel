# Agent Decision — Stateless templates and local preview

- **Date:** 2026-09-26
- **Decision maker:** Codex
- **Mission or objective:** ZeLabel v2, Objective 02
- **Authority source:** User asked to choose any database and storage only if needed, and to document decisions.
- **Authority scope:** Label workflow and persistence design.

## Purpose

Choose whether labels need a database or retained preview images.

## Options considered

- SQLite on Longhorn: enables saved drafts but adds state, backups, and migrations.
- Static layouts and immediate printing: covers the requested household use cases without persistence.

## Decision made

Store templates in code, render previews locally as SVG, and send jobs immediately. Do not add a database, volume, or external preview API.

## Implementation state

Implemented locally; physical print quality remains to be validated.

## Rationale

No saved drafts or history were requested. Stateless handling keeps the household workflow simple and avoids retaining label contents.
