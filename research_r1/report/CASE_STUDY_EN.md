# The Architecture of Access — Chanel's Handbag Price Ladder in Context

**Observation markets:** France (EUR) and United States (USD)

**Baseline snapshot:** 15 August 2026

**Supplementary pairing snapshot:** 7 September 2026

**Latest independent refresh:** 9 September 2026, United States hobo/leather route

**Research status:** limited

## Open

This case asks how Chanel presents visible entry, family-level steps and the Classic high anchor in local official list-price observations. The baseline is a non-weighted sample of 161 accepted product rows, of which 147 have numeric prices. It maps what was visible in the captured pages. It is not an assortment census, an affordability measure or a demand study.

## Context

Chanel is read against Hermès, Louis Vuitton and Dior on separate local currency axes. The competitor panel supplies external coordinates; the deeper interpretation stays with Chanel. Dior US has 13 numeric prices among 20 accepted observations. The eight unresolved rows remain missing and are not imputed. Hermès has no supplied signature flag in the current panel, so its prices do not support a like-for-like icon-premium calculation.

The observation unit is an accepted product row at a market and observation date. France and the United States are kept on their own currency axes; no FX, tax, duty or delivered-cost normalization is applied. Colour variants and near-duplicates remain visible in the raw view. A de-variant view is used only as a sensitivity lens. This matters because a visible cluster can describe the captured page mix without describing the brand's complete assortment.

## Architecture

Classic 11.12 and Small Classic form the Classic group. Mini Classic is treated as an entry observation even though its name contains “Classic”. Shopping Bag and Bowling Bag are retained as other core observations. Within the France baseline snapshot, the lowest Classic observation is 10,000 EUR and the highest entry/core observation is 6,700 EUR, a visible sample gap of 3,300 EUR. The median distance is 4,700 EUR and the median ratio is 1.810. The US snapshot shows 11,000 versus 7,400 USD, a gap of 3,600 USD, with a median distance of 5,200 USD and a ratio of 1.800.

These are same-market, same-snapshot observations. Price-upon-request rows remain a separate state and are not placed above the numeric axis. The de-variant check keeps the direction of both gaps, but it does not make the sample representative.

The group medians reinforce the shape without changing the unit of analysis: the Classic median is 10,500 EUR versus 5,800 EUR for the France comparison group, and 11,700 USD versus 6,500 USD in the United States. Those medians are descriptive summaries of the accepted rows. They should not be read as an average selling price, a willingness-to-pay estimate or a target price.

## Evolution

The aligned Chanel France panel compares fixed lineages CH-C01/CH-C02 with CH-C03/CH-C04 only in common observed years: 2022, 2023, 2024 and 2026. The absolute median distance is 4,470 EUR in 2022 and 5,350 EUR in 2026; the relative ratio moves from 2.052 to 2.081. Missing years are not interpolated. Historical rows are mostly secondary-source tables, so this is a bounded product-line observation rather than a complete official repricing calendar. The Hermès Geta France 2023 conflict is retained as two branches and excluded from the primary historical path.

The historical panel is therefore useful for locating a direction in the fixed lineages, but weak for attributing a mechanism. A larger distance could reflect price changes in either group, changes in the observed variants, or the timing of the available records. The output records group counts and common years so that a later same-model, primary-source panel can replace this bounded view without silently rewriting the past.

## Comparability gate

The baseline comparable output contains seven directional cells. None meets the main-text threshold of at least three de-variant groups for every represented brand, so these cells are appendix evidence rather than strict substitute sets.

The later Chanel supplement was filtered by the same market, bag type, size label and material group. It produces 15 directional peer candidates across 18 supplementary cells. The price comparison is blocked because the supplement is dated 7 September 2026 while the competitor baseline is dated 15 August 2026. The audit keeps unknown-size 2.55 rows, seasonal collection rows, Wallet on Chain rows and cells without a same-group peer in separate gates. It shows where a same-date refresh should look; it does not rank brands across dates.

Several candidates illustrate why the gate is necessary. A Small Boy row can share a France flap/small/leather cell with Dior rows, and a Chanel 19 row can share a France shoulder/standard/leather cell with Hermès and Louis Vuitton rows. Those are attribute matches, not proof of consumer substitution. The output keeps the two source snapshots, the peer references and the exact gate status so the next refresh can recompute the cell without mixing vintages.

The audit also records negative results. No same-group baseline peer was found for several Chanel 22 and Chanel 25 cells. The 2.55 supplement has an unknown size label in the normalized observation table, even though its page dimensions are retained in the product master; the analysis does not infer a commercial size class from dimensions alone. Seasonal collection rows and Wallet on Chain rows remain outside the regular handbag denominator.

## Latest same-date refresh

The independent 9 September 2026 US refresh contains eight official rows: two Chanel, one Hermès, three Louis Vuitton and two Dior. It produces five exact market/bag-type/size/material cells and two Chanel-peer candidates: zero strict main-text cells pass the gates.

The only hobo/leather pair that passes the sorted three-axis `max(2 cm, 10%)` dimension tolerance is Chanel AS5293 CHANEL 25 Small versus Louis Vuitton M25354 Low Key Hobo PM. The named sizes are Small and PM, so the pair is not like-for-like. Regular/season status is also undisclosed and independent-family counts remain below the three-family threshold. Hermès Videpoches stays in a crossbody/unknown-size route. Dior Bobby is Medium, while the Dior Toujours row is explicitly Autumn-Winter 2026-2027 and is isolated as seasonal. No price gap, ranking or premium is calculated from this refresh.

The refresh is stored as a separate evidence layer and does not overwrite the 15 August baseline or the 7 September supplementary panel. The reproducible audit is in `research_r1/outputs/wave6_same_date_pairing_audit_2026-09-09_us.md`.

## Sensitivity and challenge

The visible ladder survives the raw-versus-de-variant gap check in both markets: the France gap remains 3,300 EUR and the US gap remains 3,600 USD. That is a stability result for this definition, not a correction for sampling. The price bands behave differently. Because their boundaries were set after seeing the observations, moving an internal boundary by plus or minus ten percent changes several counts; for example, the France Chanel Premium core count ranges from six to ten, and the US Core count ranges from zero to seven. The bands are therefore a descriptive view, not an independent validation of a market tier.

The strongest counterargument is coverage: the apparent Classic step may be partly a product-family selection effect. The runner-up explanation is use-case separation: a flap, tote or hobo may serve different jobs even when the observed attributes line up. The current evidence cannot distinguish those explanations. A same-date, attribute-complete assortment map and a customer path would be the smallest next test that could change the interpretation.

## Interpretation

The strongest supported reading is narrow: in the visible baseline sample, Chanel places its Classic group above the observed entry and other-core groups in both markets. A wider interpretation—that customers climb this ladder, that the distance expresses brand management intent, or that the gap implies a profitable price move—remains untested. Family coverage, product use and missing competitor prices can explain part of the visible separation.

If a same-date, attribute-complete refresh preserves the gap, the next question is the full SKU ladder and the customer upgrade path. If the gap moves when family coverage changes, assortment mapping has priority. If a historical decision is required, same-model identity, common effective dates and primary historical price records are the next evidence. The sample cannot establish demand, substitution, profit, brand equity or an optimal future price.

The practical handoff is consequently staged. The latest same-date refresh has now been completed, and its strict gate remains closed. The remaining upgrade path is to map at least three independent Chanel hobo families and three independent same-size competitor hobo families on one date, with numeric dimensions and regular/season status visible. Only if those gates clear should a price comparison be calculated. If historical movement is decision-relevant, replace the secondary lineage points with same-reference, dated primary observations. Until then, the responsible output is a bounded research candidate rather than a pricing recommendation.

## Afterlife

The candidate remains noindex and unpublished. Baseline numbers point to the R1 outputs and claim IDs; the 7 September and 9 September supplementary evidence layers are kept in separate CSVs with explicit snapshot gates. The source registry distinguishes access dates from effective dates. Reproduction uses the local standard-library scripts and `python3 -m unittest discover -s tests/r1 -p 'test_*.py'`.
