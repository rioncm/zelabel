# Work Package — Mobile UI

Purpose: create an elegant, minimal composer for iPhone 15 and 16. Context: four template definitions and the API contract.

Work: build Vue/Vite layout selection, content form, local preview, copy selector, print status, and accessible touch targets. Artifact: `web/`. Evidence: production build and device review. Dependency: API metadata and preview routes.

Agent run 2026-09-26: implemented layout cards, responsive editor, preview, example values, and status feedback. Physical iPhone review remains pending.

Agent run 2026-09-27: added a 44 px clear control within each populated field and a Clear fields action that keeps the selected template and copy count for consecutive labels. Cleared fields immediately blank the preview, and stale preview responses are ignored. Production build passed; live iPhone review is pending.
