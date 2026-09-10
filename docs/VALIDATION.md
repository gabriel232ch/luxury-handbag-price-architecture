# Validation and Readiness

最后更新：2026-09-10。本文是对外可读的 release gate；内部 evidence ledger 与 analytical decisions 保存在被忽略的 `.ba-os/`。

## 1. Readiness assessment

**状态：READY WITH LIMITATIONS**

数据、来源、计算和报告链路可以供 portfolio review 和复核使用。限制不是 pipeline failure，而是公开证据的结构性边界：Chanel financial disclosure 是 consolidated company，Hermès / LVMH 使用不同 segment grain，价格是非加权 snapshot，需求与 product-level economics 未披露。

## 2. Headline financial reconciliation

所有 headline financial values 先进入 [`financial_panel.csv`](../financial_business_performance/clean/financial_panel.csv)，再由 [`financial_performance_calculations.py`](../financial_performance_calculations.py) 生成 report tables。下表列出报告使用的关键数值及 source ID。

| Headline | 2020 | 2024 | 2025 | Unit / grain | Source IDs |
|---|---:|---:|---:|---|---|
| Chanel revenue | 10,108 | 18,699 | 19,269 | USD m / consolidated company | CH-FY21; CH-FY24; CH-FY25 |
| Chanel operating profit | 2,018 | 4,479 | 4,712 | USD m / consolidated company | CH-FY21; CH-FY24; CH-FY25 |
| Chanel operating margin | 20.0% | 24.0% | 24.5% | derived / rounded figures | CH-FY21; CH-FY24; CH-FY25 |
| Chanel free cash flow | 679 | 1,842 | 2,646 | USD m / company-disclosed FCF | CH-FY21; CH-FY24; CH-FY25 |
| Chanel capex | 1,077 | 1,755 | 1,449 | USD m / company capital investment | CH-FY21; CH-FY24; CH-FY25 |
| Chanel brand-support investment | 1,360 | 2,445 | 2,395 | USD m / company-wide disclosed investment | CH-FY21; CH-FY24; CH-FY25 |
| Hermès Leather Goods & Saddlery revenue | 3,209.2 | 6,457 | 7,070 | EUR m / métier | HM-FY20; HM-FY24; HM-FY25 |
| Hermès group recurring operating margin | 31.0% | 40.5% | 41.0% | official displayed margin / group | HM-FY20; HM-FY24; HM-FY25 |
| LVMH Fashion & Leather Goods revenue | 21,207 | 41,060 | 37,770 | EUR m / multi-brand business group | LVMH-FY20; LVMH-FY24; LVMH-FY25 |
| LVMH Fashion & Leather Goods organic growth | -3.0% | -1.0% | -5.0% | company-reported organic growth | LVMH-FY20; LVMH-FY24; LVMH-FY25 |

Reconciliation checks:

- Chanel 2020 main panel uses the FY2021 release’s restated 2020 operating profit and capex; original FY2020 2,049 operating profit and 1,120 capex remain as `comparative_only` rows.
- Chanel 2022 and 2023 revenue are stored as rounded USD 17,200m and 19,700m because the official releases present $17.2bn and $19.7bn; derived margins are therefore approximate.
- Hermès 2025 margin uses the official displayed 41.0%; the calculation file also retains a 41.1% check derived from rounded 6,569 / 16,002 figures.
- LVMH Fashion & Leather Goods figures are never relabeled as Louis Vuitton or Dior revenue.

## 3. Current pricing reconciliation

The existing current-price foundation was rebuilt with its frozen observation timestamp. Source files and calculations report:

| Check | Result |
|---|---:|
| Accepted observations | 161 |
| Numeric observations | 147 |
| Chanel accepted / numeric | 41 / 35 |
| Hermès accepted / numeric | 40 / 40 |
| Louis Vuitton accepted / numeric | 40 / 40 |
| Dior accepted / numeric | 40 / 32 |
| Chanel France / United States numeric | 17 / 18 |
| Chanel France largest pre-icon → icon gap | €3,300: €6,700 → €10,000 |
| Chanel United States largest pre-icon → icon gap | $3,600: $7,400 → $11,000 |

The 14 non-numeric rows remain visible in the source data. Chanel’s six rows are `contact_us` without a numeric value; they are treated as non-numeric/POR-or-unresolved visibility states, not interpolated. Dior has eight unresolved rows, concentrated in the US. Full diagnostics are in [`architecture_summary.csv`](../financial_business_performance/calculations/architecture_summary.csv) and [`architecture_visibility.csv`](../financial_business_performance/calculations/architecture_visibility.csv).

## 4. Historical pricing reconciliation

| Check | Result |
|---|---:|
| Accepted historical observations | 77 |
| Numeric historical observations | 76 |
| Product lineages | 13 |
| Same-model continuous lineages | 7 |
| Successor lineages | 6 |
| Chanel France aligned years | 2022, 2023, 2024, 2026 |
| Chanel aligned Classic median | €8,720 → €10,300; +18.1% |
| Chanel aligned Mini/access-core median | €4,250 → €4,950; +16.5% |
| Absolute gap | €4,470 → €5,350 |
| Relative ratio | 2.052× → 2.081× |

No missing year is treated as zero change. Hermès France Geta’s conflicting 2023 observations remain in source / conflict files and are not collapsed into a single certain middle-year path.

## 5. Reporting grain and currency validation

- Chanel: consolidated company, USD millions.
- Hermès: group and Leather Goods & Saddlery, EUR millions.
- LVMH: group and Fashion & Leather Goods, EUR millions.
- FR / EUR and US / USD price observations are calculated separately.
- No cross-currency nominal revenue ranking is used; comparative charts use within-series index, growth, margin or direction.
- Reported growth, comparable growth and organic growth are stored in separate columns and are not substituted for each other.
- Annual FY2020–FY2025 financials are not mixed with FY2026 / H1 data.

## 6. Causal-language QA

The final report was checked for these prohibited shortcuts: `price caused revenue`, `drove revenue`, `price increase resulted in`, `pricing success because revenue`, and any statement that treats price persistence as demand resilience. The approved vocabulary is `coexisted with`, `accompanied by`, `coincided with`, `consistent with`, and `not causal evidence`.

The report explicitly states:

- price up + revenue up is not proof of pricing causality;
- a stable list price during a downturn is architecture persistence, not demand resilience;
- entry barrier, conversion risk, substitution, migration and ladder continuity require internal behavior data.

## 7. Chart QA

- Eight SVG assets are generated from structured calculations: current architecture, price bands, Chanel ladder, historical icon/access, four-brand archetype, Chanel financial performance, benchmark trajectory and strategic tension matrix.
- Price and revenue are not plotted on a shared dual axis.
- EUR and USD are not pooled on one nominal scale.
- Financial charts label company / segment grain and retain source / currency caveats.
- Historical chart labels distinguish continuous paths from successor paths where applicable.
- SVG files pass XML well-formedness and are checked for required title / source text during release validation.

## 8. Unavailable / non-estimable metrics

The panel intentionally retains unavailable rows for: Chanel handbag revenue, handbag units, handbag gross margin, Classic revenue; Hermès Leather Goods & Saddlery operating profit; LVMH Fashion & Leather Goods segment investments; Louis Vuitton standalone revenue; Dior standalone brand revenue. These are not replaced with proxies.

## 9. Reproduction commands

```bash
python3 build_competitor_dataset.py
python3 competitive_pricing_calculations.py
python3 build_historical_dataset.py
python3 historical_pricing_calculations.py
python3 build_financial_dataset.py
python3 financial_performance_calculations.py
python3 price_architecture_diagnostics.py
python3 build_final_report_assets.py
python3 build_financial_report_assets.py
python3 -m unittest discover -s tests/financial -p 'test_*.py'
python3 scripts/r1/build.py
python3 scripts/r1/validate.py
python3 scripts/r1/export_case_study.py
python3 -m unittest discover -s tests/r1 -p 'test_*.py'
git diff --check
```

## 10. Existing R1 compatibility note

The R1 validator script completes with `status=limited`, `errors=0`, and three expected warnings for unresolved Dior prices, the Hermès Geta conflict, and uneven historical coverage. The full `tests/r1` suite is green after the report-contract repair, and the Phase 2 financial / architecture test suite remains `12/12` passing.

`research_r1/report/REPORT_CN.md` is an authoritative generated R1 deliverable because `scripts/r1/build.py` writes it as part of the release build. The generator now derives report counts from the structured R1 coverage and pairing outputs, including Dior US coverage and the supplementary / Wave 6 gates; `tests/r1/test_reports.py` checks those data-driven invariants rather than obsolete literal prose. The separate top-level final report remains the portfolio-facing Phase 2 narrative.
