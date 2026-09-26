# Work Package — API and labels

Purpose: produce safe, bounded ZPL for household labels. Context: ZD621 TCP 9100, 203/300 dpi variants, 4×2 and 2×2 media.

Work: implement metadata, preview, print, health routes; input and copy validation; ZPL escaping and TCP timeout. Artifacts: `api/`, `tests/`. Evidence: local tests plus later physical print samples. Dependency: Objective 01.

Agent run 2026-09-26: implemented four layouts and local SVG previews with no database. Printer-specific alignment and media switching remain for physical validation.
