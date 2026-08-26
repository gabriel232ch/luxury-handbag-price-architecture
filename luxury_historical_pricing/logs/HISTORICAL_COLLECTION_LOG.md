# Historical luxury handbag pricing collection log
Collection date: 2026-08-16; requested period: 2020-01-01 through 2026-08-16.
## Scope and method
Brands: Chanel, Hermès, Louis Vuitton, Dior. Category: luxury handbags only. Markets: France and United States, with France prioritized. Grain: one brand × product lineage × market × dated observation; irregular observations retained. Historical acquisition used manual web research from public, indexed pages. No authentication, CAPTCHA bypass, resale asking prices, FX conversion, inflation adjustment, interpolation, strategy analysis, or recommendations were used.
The current 2026 anchor rows are inherited from the supplied official localized current-price datasets observed on 2026-08-15. Historical rows are predominantly Tier 3/4 secondary source observations because archived official pages or official historical price lists were not reliably available in the accessible public results.
## Brand-level coverage
| Brand | Candidate products selected | Usable historical series | Observations obtained | HIGH | MEDIUM | LOW | France observations | US observations | Avg historical observations / usable series | Unresolved products |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Chanel | 4 | 4 | 21 | 8 | 13 | 0 | 17 | 4 | 3.25 | 2 |
| Hermès | 2 | 2 | 12 | 4 | 8 | 0 | 8 | 4 | 4.0 | 3 |
| Louis Vuitton | 4 | 4 | 28 | 6 | 22 | 0 | 16 | 12 | 5.5 | 2 |
| Dior | 3 | 3 | 16 | 5 | 10 | 0 | 5 | 10 | 3.33 | 3 |

## Candidate selection and lineage notes
- `CH-C01` Chanel — Sac classique 11.12 / Classic 11.12 Handbag; role `signature_icon`; continuity `SAME_MODEL_CONTINUOUS`; selection reason: France historical series is usable. US historical coverage not found in the accepted sources; current US anchor retained.
- `CH-C02` Chanel — Petit sac classique / Small Classic Handbag; role `signature_icon`; continuity `SAME_MODEL_CONTINUOUS`; selection reason: France historical series is usable. US historical coverage not found in the accepted sources; current US anchor retained.
- `CH-C03` Chanel — Mini sac classique / Mini Classic Handbag; role `signature_access`; continuity `SAME_MODEL_CONTINUOUS`; selection reason: France historical series is usable. US historical coverage not found in the accepted sources; current US anchor retained.
- `CH-C04` Chanel — Mini sac classique / Mini Classic Handbag; role `signature_access`; continuity `SAME_MODEL_CONTINUOUS`; selection reason: France historical series is usable. US historical coverage not found in the accepted sources; current US anchor retained.
- `HM-H01` Hermès — Sac Hermès Geta / Hermès Geta bag; role `core_upper_core`; continuity `SAME_MODEL_CONTINUOUS`; selection reason: France includes a 2023 source conflict (4,550 vs 5,550 EUR); both are retained. US historical coverage is available for 2023–2024.
- `HM-H02` Hermès — Sac Jypsière mini / Jypsiere mini Toile & Cuir bag; role `core_upper_core`; continuity `MODEL_SUCCESSOR`; selection reason: France historical series is usable for 2023–2024. US current anchor retained but historical US coverage not found.
- `LV-L01` Louis Vuitton — Sac / Speedy Bandoulière 25; role `signature_access`; continuity `MODEL_SUCCESSOR`; selection reason: Model continuity is strong, but current special-canvas version is not treated as an exact SKU.
- `LV-L02` Louis Vuitton — Sac Speedy Bandoulière 20; role `core`; continuity `SAME_MODEL_CONTINUOUS`; selection reason: France-only current anchor in the supplied dataset; US historical/current match not accepted.
- `LV-L03` Louis Vuitton — Alma BB; role `accessible_core`; continuity `MODEL_SUCCESSOR`; selection reason: Both FR and US historical prices are retained with material/version caveat.
- `LV-L04` Louis Vuitton — Neverfull MM; role `accessible_core`; continuity `SAME_MODEL_CONTINUOUS`; selection reason: Current France anchor was not present in the supplied current capture; France historical observations are retained and marked current-FR anchor incomplete.
- `DI-D01` Dior — Saddle Small Bag with Strap; role `signature_icon`; continuity `MODEL_SUCCESSOR`; selection reason: US historical series is usable for 2022–2023 with size/material caveat; France current anchor retained.
- `DI-D02` Dior — Small Dior Book Tote; role `signature_core`; continuity `MODEL_SUCCESSOR`; selection reason: Material/version difference is documented; do not treat as exact-SKU continuity.
- `DI-D03` Dior — Medium Dior Book Tote; role `signature_core`; continuity `MODEL_SUCCESSOR`; selection reason: France current anchor is numeric; US current price was unresolved in the supplied current capture.

Products not included in the primary lineages because identity, size, or historical price evidence was insufficient are listed in `errors/unresolved_history.jsonl`.
## Source limitations
- No accepted historical observation in this run came from an archived official product page or official historical price list. Current anchor observations are official primary sources from the supplied current datasets.
- Secondary tables sometimes use family/size labels rather than official references. Those observations are marked `MODEL_SUCCESSOR` or `SAME_MODEL_CONTINUOUS` according to the documented lineage evidence; approximate family-only candidates were not promoted into the primary lineages.
- Hermès Geta has a credible-source conflict for 2023 France (EUR 4,550 vs EUR 5,550); both observations are preserved with `conflict_flag=true`.
- France coverage is materially stronger for Chanel and Hermès. US history is incomplete for Chanel and Hermès Jypsière, and current US Dior Medium Book Tote price was unresolved in the supplied capture.
- Historical prices are nominal local-currency retail/list prices as reported by the source. No FX or inflation normalization was performed.

## Historical coverage summary
Accepted observation rows: 77; numeric price observations: 76; usable historical lineages: 13; price-change events: 35; unresolved products/candidates: 10.
Historical lineage continuity counts: EXACT_SKU 0; SAME_MODEL_CONTINUOUS 7; MODEL_SUCCESSOR 6; APPROXIMATE_FAMILY_MATCH 0. Current anchor rows are labeled EXACT_SKU separately.
Source mix by accepted observation rows: official current primary 31.2%; secondary historical 68.8%. Source mix by numeric price observations: official current primary 30.3%; secondary historical 69.7%.
Lineage-level high-confidence series: 5; same-model-continuous series: 7; model-successor series: 6; approximate-family matches: 0.
## Output files
- `raw/historical_price_observations_raw.jsonl` — raw-like accepted observations including source excerpts and extraction metadata.
- `clean/historical_pricing_clean.csv` — validated normalized observation panel, including current anchor rows and confidence/continuity fields.
- `clean/chanel_historical_pricing.csv`, `clean/hermes_historical_pricing.csv`, `clean/louis_vuitton_historical_pricing.csv`, `clean/dior_historical_pricing.csv` — brand subsets.
- `lineage/product_lineage.csv` — product identity and continuity map.
- `events/price_change_events.csv` — source-supported observed price-change intervals only.
- `logs/HISTORICAL_SOURCE_REGISTRY.csv` — source registry for accepted observations.
- `errors/unresolved_history.jsonl` — unresolved candidates and source limitations.
## Gate assessment
Overall: READY WITH LIMITATIONS. Chanel and Louis Vuitton have usable multi-observation France series across four lineages; Dior has three usable lineages with material/version caveats; Hermès has two usable lineages and a documented Geta conflict. France is READY WITH LIMITATIONS; United States is READY WITH LIMITATIONS because Chanel and Hermès coverage is sparse and the Dior medium Book Tote current US anchor is unresolved. Brand-level readiness: Chanel READY WITH LIMITATIONS; Hermès NOT READY for a broad multi-family comparison; Louis Vuitton READY WITH LIMITATIONS; Dior READY WITH LIMITATIONS. This is a data-coverage statement only, not an analytical conclusion.
