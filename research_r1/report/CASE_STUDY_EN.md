# The Architecture of Access — Chanel's Handbag Price Ladder in Context

**Observation markets:** France (EUR) and United States (USD) · **Current snapshot:** 15 August 2026 · **Research status:** limited

## Open

This case asks how Chanel presents visible entry, family-level steps and the Classic high anchor in local official list-price observations. The dataset is a non-weighted sample of accepted product rows: 161 observations, 147 numeric prices. It is a map of what was visible in the captured pages, not a census of a brand assortment and not a measure of affordability.

## Context

Chanel is read against Hermès, Louis Vuitton and Dior on separate local currency axes. The competitor panel supplies an external coordinate system, while the deeper interpretation stays with Chanel. Dior US has 13 numeric prices out of 20 accepted rows; 7 unresolved prices remain missing. Hermès has no supplied signature flag in the current panel, so its prices do not support a like-for-like icon premium calculation.

## The price ladder

Within the France snapshot, the lowest Classic observation is 10000 EUR and the highest entry/core comparison observation is 6700 EUR, a visible sample gap of 3300 EUR. The median distance is 4700 EUR and the median ratio is 1.810. The US snapshot shows 11000 versus 7400 USD, a gap of 3600 USD, with a median distance of 5200 USD and a ratio of 1.800.

The membership rule matters. Classic 11.12 and Small Classic form the Classic group. Mini Classic is an entry observation even when its product name contains “Classic”; Shopping Bag and Bowling Bag are retained as other core observations. Price-upon-request rows remain a separate state and are not placed above the numeric axis.

## Moving together

The aligned Chanel France panel compares fixed lineages CH-C01/CH-C02 with CH-C03/CH-C04 only in common observed years (2022, 2023, 2024, 2026). It reports group medians, absolute distance, ratio and lineage counts without interpolating missing years. Historical rows are mostly secondary-source tables, so the result is a bounded product-line observation rather than a complete official repricing calendar. The Hermès Geta France 2023 conflict is kept as two branches and excluded from the primary path.

The later Chanel supplement was filtered by the same market, bag type, size label and material group. It produces 15 directional peer candidates across 18 supplementary cells. The price comparison is blocked because the supplement is dated 7 September 2026 while the competitor baseline is dated 15 August 2026. The audit keeps unknown-size, seasonal-collection and Wallet on Chain rows in separate gates. Latest independent refresh evidence contains 8 rows, 5 exact cells and zero strict main-text cells. The only dimension match is Small and PM, so its price comparison also remains blocked.

## What the evidence can support

Three decisions follow conditionally. If the ladder gap survives de-variant sensitivity, a category lead can verify the full SKU ladder and the customer upgrade path. If it moves when family coverage changes, the next action is assortment mapping. If a historical movement is needed for a decision, the next evidence should be same-model identity, common dates and primary price records. The sample cannot establish demand, substitution, profit, brand-equity effects or an optimal future price.

## Afterlife

All numbers in the public candidate export point to R1 outputs and claim IDs. The source registry distinguishes page access from effective dates; the 15 August current snapshot remains separate from any later refresh. Reproduction uses the local Python standard-library scripts and `python3 -m unittest discover -s tests/r1 -p 'test_*.py'`.
