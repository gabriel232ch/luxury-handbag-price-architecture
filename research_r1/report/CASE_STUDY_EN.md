# The Architecture of Access: Chanel's Handbag Price Ladder in Context

**Observation markets:** France (EUR) and United States (USD) · **Current snapshot:** 15 August 2026 · **Research status:** limited

## Research question

The case examines how Chanel presents visible entry points, family-level steps and the Classic high anchor in local official list-price observations. The dataset contains 161 accepted product rows, of which 147 have numeric prices. It maps what was visible on the captured pages; it is not a census of the assortment or a measure of affordability.

## Context

Chanel is the focal case. Hermès, Louis Vuitton and Dior provide competitive context on separate local-currency axes. Dior US has 13 numeric prices among 20 accepted rows; the remaining 7 prices are unresolved and are not imputed. Hermès has no supplied signature flag in the current panel, so its prices do not support a like-for-like icon-premium calculation.

## The price ladder

Within the France snapshot, the lowest Classic observation is €10,000 and the highest entry/core comparison observation is €6,700, a visible sample gap of €3,300. The median distance is €4,700 and the median ratio is 1.810. The US snapshot shows $11,000 versus $7,400, a gap of $3,600, with a median distance of $5,200 and a ratio of 1.800.

The membership rule matters. Classic 11.12 and Small Classic form the Classic group. Mini Classic is an entry observation even though its product name contains “Classic”; Shopping Bag and Bowling Bag remain other core observations. Price-upon-request rows stay separate and are not placed above the numeric axis.

## Moving together

The aligned Chanel France panel compares fixed lineages CH-C01/CH-C02 with CH-C03/CH-C04 only in common observed years (2022, 2023, 2024, 2026). It reports group medians, absolute distance, ratio and lineage counts; missing years are not interpolated. Because most historical rows come from secondary-source tables, the result is a bounded product-line observation, not a complete official repricing calendar. The Hermès Geta France 2023 conflict remains as two branches and is excluded from the primary path.

The later Chanel supplement uses the same market, bag type, size label and material-group filters. It produces 15 directional peer candidates across 18 supplementary cells. The price comparison is blocked because the supplement is dated 7 September 2026 and the competitor baseline is dated 15 August 2026. Unknown-size, seasonal-collection and Wallet on Chain rows stay in separate gates. Latest independent refresh evidence contains 8 rows, 5 exact cells and zero strict main-text cells. The only dimension match is Small and PM; its price comparison also remains blocked.

## What the evidence can support

The evidence supports three conditional next steps. If the ladder gap survives de-variant sensitivity, verify the full SKU ladder and customer upgrade path. If it moves when family coverage changes, map the assortment first. If a historical movement matters to the decision, the next evidence should include same-model identities, common dates and primary price records. The sample cannot establish demand, substitution, profit, brand-equity effects or an optimal future price.

## Audit trail and reproducibility

The public candidate export links its numbers to R1 outputs and claim IDs. The source registry separates page-access dates from effective dates, and the 15 August current snapshot remains separate from later refreshes. Reproduction uses the local Python standard-library scripts and `python3 -m unittest discover -s tests/r1 -p 'test_*.py'`.
