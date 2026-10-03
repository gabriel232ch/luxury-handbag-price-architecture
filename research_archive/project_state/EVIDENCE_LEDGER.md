# Evidence ledger — Pilot 001

| ID range | Layer | Meaning |
|---|---|---|
| DISC-* | Raw | Category discovery records, including unresolved references |
| OBS-* | Raw/validated | Official product-page price observations |
| MATCH-* | Validated | Exact-reference cross-market matches |
| CARD-* | Analytical | Evidence cards with observation lineage |

All analytical values point to validated observations and preserve the originating product URL.

## Parent gap-review evidence — 2026-10-03

| ID | Type | Observation / inference | Source | Status / limits |
|---|---|---|---|---|
| LS-E01 | F | Homepage asks whether Chanel's apparent different performance is real and why; detailed page says demand resilience and price causality remain unproven | LS-S01/02 | Observed; establishes project objective, not resilience |
| LS-E02 | F | Current report reconstructs 2025-08-13–2026-08-13 marketing and infers creative/cultural strategy | LS-S03 | Observed document scope; strategy judgments remain interpretations |
| LS-E03 | F | FY2024 comparable revenue -4.3%; operating profit $4,479m, down about 30%; FCF $1,842m; capex $1,755m | LS-S04 | Validated consolidated disclosure, not handbag outcomes |
| LS-E04 | F | FY2025 comparable revenue +1.8%; Americas +7.2%, Asia Pacific -0.8%; profit $4,712m; FCF $2,646m; capex $1,449m | LS-S05 p.4 | Validated; regional sales not customer-nationality data |
| LS-E05 | F | FY2025 release reports fashion, beauty, watches/jewellery positive performance; Blazy debut October 2025; >40 boutique openings includes >25 dedicated beauty boutiques | LS-S05 pp.1–2 | No numerical category contribution; store openings not automatically Fashion stores |
| LS-E06 | F | Bain estimates about 50m fewer luxury customers during 2022–24, with concentration in top clients and category/region divergence | LS-S06 §§1–5 | Industry estimate, cannot transfer to Chanel customers |
| LS-I01 | I | Current marketing study complements pricing evidence but does not identify causes of relative resilience | LS-E01/02/03/04 | High confidence about evidence gap; no confidence asserted for a dominant business mechanism |
| LS-I02 | I | FY2025 recovery is not evidence of immunity throughout slowdown; later 2026 campaigns cannot explain FY2024 outcomes | LS-E03/04/05 | Supported temporal boundary; verify peers before ranking resilience |

Financial boundary: capex is not immediately expensed in full in operating profit; investigate depreciation/operating costs separately from cash investment. Profit/FCF movement is not itself a demand measure. Keep exposure/mix and macro recovery as alternatives to marketing impact.

## Relative-performance round — 2026-10-03

| ID | Type | Observation / inference | Source | Status / limits |
|---|---|---|---|---|
| LS-E07 | F | Chanel FY2023 revenue $19.7bn; operating profit $6,407m; FCF $3,755m; capex $1,227m | LS-S07 | Consolidated; rounded revenue |
| LS-E08 | F | Hermès FY2023/24/25 constant-currency growth 20.6/14.7/8.9%; recurring margins 42.1/40.5/41.0% | LS-S08/09 | Group, not handbag margins |
| LS-E09 | F | LVMH FLG FY2023/24/25 organic growth 14/−1/−5%; recurring operating profit €16,836/15,230/13,209m | LS-S10/11/12 | Multi-brand segment; not group cash |
| LS-E10 | F | Gucci FY2023/24/25 comparable growth −2/−21/−19%; recurring operating profit €3,264/1,605/966m | LS-S13/14/15 | Brand; recurring adjustments differ from Chanel |
| LS-C01 | Calculation | FY2025 revenue / profit indexes (2023=100): Chanel 97.6/73.5; Hermès 119.2/116.3; FLG 89.6/78.5; Gucci 60.7/29.6 | LS-E07–10; LS-E03/04; LS-E11; panel CSV | Current v2 replaces rounded-base Chanel 97.8; within-series reported currency; no demand inference |
| LS-I03 | I | Chanel relative resilience is metric/year/comparator-dependent; revenue stabilizes before profit fully recovers | LS-C01; LS-E08/09/10 | Supported for selected sample only; not causal |
| LS-I04 | I | Marketing-only expansion cannot resolve revenue-profit divergence; exposure/mix and cost alternatives required | LS-I03; LS-E03/04 | Research prioritization; dominant explanation unknown |

Deliverable and full lineage: `case/luxury_slowdown_2023_2025/RELATIVE_RESILIENCE_REVIEW_CN.md`. User's original dataset retained unchanged. Blank cash/investment fields indicate not included this round, not zero or necessarily undisclosed.

## Slowdown localization — 2026-10-03

| ID | Type | Observation / calculation / inference | Source | Status / confidence / limits |
|---|---|---|---|---|
| LS-E11 | F | FY2023 Chanel revenue $19,744m, Europe 5,606/AP 10,178/Americas 3,960; FY2024 5,676/9,233/3,790 | LS-S17 p.4 | Validated; high confidence narrow disclosure; more precise than LS-E07 summary, not a conflict |
| LS-E12 | F | FY2024 regional comparable growth Europe +0.6/AP −7.1/Americas −4.2%; FY2025 +2.5/−0.8/+7.2%, respective FY2025 revenue $6,054/9,182/4,033m | LS-S17; LS-S05 p.4 | Validated, high; sales region not client nationality |
| LS-C02 | E | Reported USD: FY2024 regional changes +70/−945/−170 = −1,045m; FY2025 +378/−51/+243 = +570m. AP 90.4% of FY2024 net decline; FY2025 share 47.7% | LS-E11/12; regional CSV; check_regional_bridge.py | Reconciled exactly; mathematical location, FX/scope/mix included, no causality |
| LS-E13 | E | Bain current China report estimates FY2024 mainland decline 17–19%, FY2025 3–5%; earlier FY2024 report had 18–20% | LS-S18/19 | Medium for market estimate; revision retained, not a growth event |
| LS-E14 | E | FY2025 mainland category estimates: beauty +4–7%; fashion −5–8%; leather −8–11%; jewellery −0–5%; watches −14–17% | LS-S20 | Industry, not Chanel; medium; ranges not midpoint-imputed |
| LS-E15 | F | Bain reports Chinese customers shifted shopping locations across 2024/25, with about 65% spent onshore in FY2025; young aspirational entry delayed; FY2024 VICs also cautious | LS-S18/19/20 | Validated report content; industry inference cannot define Chanel clients |
| LS-E16 | F | Hermès FY2025 cfx growth AP ex-Japan +4.9%, Japan +14.1%, global Leather/Saddlery +13.1% | LS-S09 pp.6–7 | High for narrow disclosure; differing region/category boundaries |
| LS-E17 | E | Bain historical FY2025 global PLG €358bn vs FY2024 €364bn; about −2% current currency and +1% constant; earlier FY2025 forecast cfx flat | LS-S21/22 | Medium; official publisher historical update selected, not 2026 forecast |
| LS-I05 | I | Chanel FY2025 stabilization is geographically offset: Europe/Americas gains cover continued AP decline | LS-E12; LS-C02 | High for geography localization, not cause |
| LS-I06 | I | Beauty/category mix is a plausible buffer to test; magnitude at Chanel remains unmeasured | LS-E14; Chanel entity definition | Hypothesis, medium plausibility; missing category weights/growth and regional intersections |
| LS-I07 | I | Geography and category alone are insufficient as blanket explanations; Hermès is a counterexample, while within-region country/customer/product mix remains live | LS-E16; LS-I05 | Bounded, medium; no claim to quantify residual brand effect |

Reversal tests: a comparable Chanel country/category bridge can narrow or reverse the category-buffer hypothesis; client-source × destination data can change the reading of European growth. The public geography bridge is sufficient for location, not for demand/marketing diagnosis. All industry-report derivatives retained as one evidence cluster.

## Revenue-profit bridge — 2026-10-03

| ID | Type | Observation / calculation / inference | Source | Status / limits |
|---|---|---|---|---|
| LS-E18 | F | Precise FY2023/24/25 revenue 19,743.9/18,699.3/19,269.1; gross profit 16,050.6/14,965.0/15,277.6; SG&A 6,957.4/7,812.3/7,942.2; operating profit 6,407.0/4,478.6/4,711.5 USDm | LS-S24 p.86; LS-S23 p.116 | Visually verified narrow group disclosure, high; rounded release series retained separately |
| LS-C03 | Calculation | FY2024 operating change −1,928.4 = gross-profit change −1,085.6 − SG&A increase 854.9 − distribution increase 5.7 + ad saving 17.8; FY2025 +232.9 = +312.6 −129.9 +0.1 +50.1 | LS-E18; profit CSV/check | Exact disclosed-precision accounting bridge, not causal attribution |
| LS-E19 | F | Staff cost 3,486.4/4,061.8/4,293.2 USDm; average monthly employees 34,329/37,492/38,045 | LS-S24 p.111; LS-S23 p.133 | High; nature-based disclosure overlaps functional expenses, no additive cost contribution |
| LS-E20 | F | FY2024/25 selected DA 572.1/648.0; exceptional net charges 175.3/93.6; adjusted EBITDA 5,226.0/5,453.1; addback excludes ROU depreciation | LS-S23 pp.18–19,132 | High; EBITDA–operating profit gap not pure DA |
| LS-E21 | F | FY2023 exceptional net gain 12.0 included 101.8 London sale/leaseback gain; FY2024 net charge 175.3 | LS-S24 p.109 | High; baseline effect already in operating profit |
| LS-E22 | F | FY2025 profit before NCI 2,912.8 versus 3,398.8; financial FX loss442.9 versus gain25.7 USDm; below operating profit | LS-S23 pp.116,132 | High; not an operating-profit explanation |
| LS-C04 | Calculation | FY2025 net finance deterioration576.9 + tax charge increase163.3, offset by operating improvement232.9 and equity income improvement21.3 = tax-after profit decline486.0 USDm before NCI | Profit CSV/check; LS-S23 | Reconciled; attributable decline488.8 differs by NCI |
| LS-I08 | I | Revenue stabilization coexists with higher functional operating expense level and lower gross margin; ad-budget surge rejected as explanation of 2024–25 expense change | LS-E18; LS-C03 | High narrow descriptive confidence; sales effectiveness and discretionary investment ROI unresolved |
| LS-I09 | I | 2025 selected DA increase offset by lower exceptional charges; combined worsening cannot be primary explanation of incomplete 2025 recovery | LS-E20; reconciliation | Bounded arithmetic, not all depreciation or a clean underlying-profit decomposition |

Coverage READY WITH LIMITATIONS for accounting localization. RESEARCH AGAIN for price-volume-mix, country/category/client margins, SG&A nature-by-function allocation, constant-currency expense movement and marketing ROI. Two years' staff/DA changes must never be added again to functional-cost bridge. New exact panel refines precision, does not overwrite original user dataset.

## Channel and product-window round — 2026-10-03

| ID | Type | Observation / inference | Source | Status / limits |
|---|---|---|---|---|
| LS-E23 | F | Retail FY2023/24/25 15,359.7/14,407.3/14,842.4 USDm; Wholesale4,373.2/4,280.0/4,414.1; Other11.0/12.0/12.6 | LS-S24p.109;LS-S23p.131 | High narrow disclosure; reported USD, not same-store or category |
| LS-C05 | Calculation | FY2024 Retail−952.4/Wholesale−93.2/Other+1.0=−1,044.6; FY2025+435.1/+134.1/+0.6=+569.8. Retail91.2% decline,76.4% increase;45.7% previous loss recovered | channel panel/check | Exact disclosed-precision bridge; geographical bridge separate view, not additive |
| LS-E24 | F | 31LE ROUGE launch2023/extension2024; N5 campaign2024; SS2025 boutiquesMarch2025 | LS-S07/04/25 | Year/month precision retained; no product contribution |
| LS-E25 | F | CHANEL25 preview beforeFeb3 article and full March campaign/store window; later report states March2025 release; FY2025 official launch/positive reception | LS-S27/28;LS-S23p.27;LS-S05 | Medium month timing/high annual launch; no market synchronization or incremental sales |
| LS-E26 | F | Chance fragrance launchFY2025; London activation25April–5May2025; more than25 dedicatedBeauty boutique openings | LS-S26;LS-S05 | High event/date/annual count; first-sale day not adopted; local event not global proof |
| LS-E27 | F | Blazy debut showOctober2025; collection arrivalMarch2026 | LS-S23p.3 | High official timing, not an FY2025 product-sales mechanism |
| LS-I10 | I | FY2025 recovery in both channels, Retail still below2023; no DTC-share pivot from greater dollar contribution | LS-C05;LS-E23 | High narrow accounting description; nominal growth ~3.0/3.1% |
| LS-I11 | I | CHANEL25/Beauty products are time-eligible FY2025 mechanisms; Blazy debut merchandise sales excluded, possible2025 halo untested | LS-E24–27 | Window test only, not efficacy. Cannibalization/new-store/FX alternatives retained |

9 targeted activity records in product_timing_ledger.csv are selected timing nodes, not global activity census. Ambassadors do not identify customers. Retail/wholesale not mapped to Fashion/Beauty without category×channel evidence. READY WITH LIMITATIONS for location/timing; RESEARCH AGAIN for causal mechanism ranking.

## Customer / Beauty round — 2026-10-03

| ID | Type | Observation / inference | Sources | Status / confidence / limits |
|---|---|---|---|---|
| LS-E28 | F | Public first-buyer and joint-owner self-reports link25 to daily/casual use; return/rebuy, alternative22 and Margaux10 and intended-only cases retained | LS-S29–34;R01–11 | High that text exists; low for authenticated/general customer behavior. No frequency/segmentation |
| LS-E29 | F | Feb2,2025post65 self-reports store-acquired25; Aug22post recalls January purchase | LS-S34;LS-S32 | Early availability leads only; SKU/market unverified. Qualifies LS-E25 March month as promotion/launch stage rather than universal first sale |
| LS-E30 | F/E | L'Oreal URD2025p23 reproduces WWD2024 Chanel beauty salesUSD8.54bn | LS-S35 | High graph/year/unit reading; medium-low third-party magnitude, not reconciled audited division |
| LS-C06 | E | 8.54bn×1000 /18,699.3m≈45.67%, displayed≈46% | LS-E30;LS-E18;beauty_scale_inputs/check | Conditional cross-source scale proxy only; excludes contribution bridge |
| LS-E31 | F | DIARY lists WWD2025 beauty salesChanelUSD9.18bn EST | LS-S36 | Validated reproduction; upstream/method not verified; candidate actual estimate, not bridge input |
| LS-I12 | I | Daily-use choice is a plausible25 demand mechanism to test, but first purchase does not prove brand incrementality and use substitution does not prove purchase cannibalization | LS-E28 | Bounded qualitative hypothesis; customer/transaction/counterfactual missing |
| LS-I13 | I | Beauty is material to group-versus-handbag comparison; group recovery cannot be read as handbag recovery | LS-E30/C06;existing entity definition | Supported comparison caution; magnitude/two-year causal contribution unresolved |

Search-only derivatives9.18/3.1% do not match earlier8.54 in simpleUSD growth; not persisted as validated growth. No subtraction of external category estimates from audited totals. Management all-business-growth statementLS-S05 retained as contrary to an only-Beauty-grow story. New scale evidence supersedes any broad reading of earlier missing-category-data note: public third-party scale exists, comparable audited category bridge still missing.

## Integrated diagnostic answer — 2026-10-03

| ID | Type | Claim | Basis | Status / confidence / limits |
|---|---|---|---|---|
| LS-I14 | I | The scoped difference is FY2025 group revenue stabilization with incomplete profitability, not continuous immunity or proven handbag recovery | LS-N01;LS-I08/10/13;LS-E18 | Supported, high for narrow trajectory/boundary; comparator/year/metric-dependent, no industry-wide ranking |
| LS-I15 | I | Geography/channel/cost identities localize movements; category scale and daily-use reports suggest mechanisms but do not rank growth contributions | LS-C02/03/05/06;LS-I11/12/13 | Supported analytical separation, high; medium/low for mechanisms, no causality or additive region/channel decomposition |
| LS-C07 | E | Precise FY2025/FY2023 revenue97.6% and operating73.5%; FY2023→FY2025 gross deficit773.0 + SG&A increase984.8 − advertising/distribution savings62.3 = operating deficit1695.5 USDm | LS-E18;check_synthesis.py | Exact disclosed-precision arithmetic; real business cause remains unresolved |

LS-S05 re-opened this round: p.4 exactFY2025comparable1.8% versus headline rounded2%; no contradictory growth series. READY WITH LIMITATIONS for integrated bounded answer; causal ranking remainsRESEARCH AGAIN.

## Customer-choice instrument — 2026-10-03

LS-I16 [I]: Existing11 purposive public records provide no sufficient brand-budget incrementality or advertising/payment sequence. Supported high for this inspected set, not a claim about all available public records or customers. BasisLS-E28, LS-R01–11 andFIT01–11; store observation hasnot_applicable budget, other casesunknown. First-self-report scope, final retention and channel remain material followups. No new sample or interview results produced; instrument preparation does not upgrade causal confidence.
