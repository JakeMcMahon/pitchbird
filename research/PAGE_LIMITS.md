# Page Capacity & Split Rules

## Available Content Area

**A4 portrait dimensions:**
- Total height: 297mm
- Header band: 22mm (navy bg, logo + URL)
- Body top padding: 14mm
- Body bottom margin: 14mm  
- Footer area: 14mm (page number + nav arrow)
- **Available content area: ~233mm**

This 233mm is the safe zone for content before page breaks trigger.

## Estimated Row/Block Heights (by template type)

Measured from CSS in `generate_lead_magnet.py`:

| Template Type | Per-Item Height | Notes |
|---|---|---|
| `.we-block` (word economy) | ~36mm | Padding + label + rule + dual example |
| `.pt-row` (pressure test) | ~38mm | Icon + name + description + signals |
| `.ex-card` (example) | ~52mm | Two-column layout (name + body + take) |
| `.t60-row` (first 60 seconds) | ~42mm | Three-column (window, what, question) |
| `.dodont-row` (do/don't pair) | ~14mm | Two-column grid with icons |
| `.fail-row` (failure mode) | ~20mm | Three-column (mode, detail, fix box) |
| `.mh-row` (must-have) | ~22mm | Icon + number + title + description |
| `.callout` (problem/solution) | ~58mm | Colored panel with pill + headline + body |
| `.principle` (design principle) | ~22mm | Dot + title + description |

## Max Items Per Page

Derived from math: `available_area ÷ per_item_height = max_items`

| Template Type | Max Per Page | Rationale |
|---|---|---|
| `we_block` | 5 | 233 ÷ 36 = 6.5 → use 5 (safe margin) |
| `pt_row` | 3 | 233 ÷ 38 = 6.1 → use 3 (splits across 2 pages) |
| `ex_card` | 2 | 233 ÷ 52 = 4.5 → use 2 (preserves hierarchy) |
| `t60_row` | 4 | 233 ÷ 42 = 5.5 → use 4 (or 2 if 8-line-rule band present) |
| `dodont_row` | 8 | 233 ÷ 14 = 16.6 → use 8 (high density, acceptable) |
| `fail_row` | 6 | 233 ÷ 20 = 11.6 → use 6 (readability threshold) |
| `mh_row` | 8 | 233 ÷ 22 = 10.6 → use 8 (grid layout allows it) |
| `callout` | 4 | 233 ÷ 58 = 4.0 → use 4 per page |
| `principle` | 4 | 233 ÷ 22 = 10.6 → use 4 (visual balance) |

**Note on pressure_test splits:** Historical git shows 5 tests exist total. Current layout: 3 on page A, 2 on page B + closing statement. This is space-optimal.

## Before You Add a New Page

Checklist for future content authors:

- [ ] Does the new section fit the established limits above?
- [ ] If new template type: measure CSS height (padding + font + gap), divide available 233mm
- [ ] Will adding N items split naturally across pages?
- [ ] Test render with `--slug one-pager` and confirm PDF page count
- [ ] If split across pages, ensure each chunk feels complete (no orphaned items)
- [ ] Verify no template is set to `page-break-inside: avoid` without being added to the CSS list
- [ ] Update PAGE_SPLIT_RULES dict in `generate_lead_magnet.py` if introducing new type
- [ ] Document reasoning in git commit (e.g., "add 4 callouts per page per CSS height math")

## Historical Split Decisions

From git log analysis:

- **v9/v8:** pressure-test split into 3 + 2 (was 5 total, too dense on one page)
- **v7:** first-60-seconds split: rows 1-2 on page A, rows 3-4 + rule on page B
- **v6:** examples: 2 cards on page A, 1 + framework on page B
- **Early versions:** word-economy discovered 5 items max (no more fit cleanly)

Each split was discovered post-render. This document captures the math to *prevent* future overflow.
