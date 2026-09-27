# Work Package — API and labels

Purpose: produce safe, bounded ZPL for household labels. Context: ZD621 TCP 9100, 203/300 dpi variants, 4×2 and 2×2 media.

Work: implement metadata, preview, print, health routes; input and copy validation; ZPL escaping and TCP timeout. Artifacts: `api/`, `tests/`. Evidence: local tests plus later physical print samples. Dependency: Objective 01.

Agent run 2026-09-26: implemented four layouts and local SVG previews with no database. Printer-specific alignment and media switching remain for physical validation.

Agent run 2026-09-27: owner observed the first line clipping on live prints. Shifted the ZPL rule and all field coordinates down by a configurable 24 dots at 203 dpi (about 3 mm), with the same shift in SVG previews. The value is `LABEL_TOP_OFFSET_DOTS`, limited to 0–24 to keep the lowest content on the label. Local API tests passed at 203 and 300 dpi. Physical alignment still needs a print check.
