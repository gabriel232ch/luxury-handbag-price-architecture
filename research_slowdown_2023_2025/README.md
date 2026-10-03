# Luxury slowdown diagnostic: Chanel FY2023–FY2025

This research extension supplies business-performance context for the project's Chanel handbag price-architecture work. It answers the homepage question “Luxury Was Slowing. Why Did Chanel Look Different?” using company results, comparable peer disclosures, industry estimates, selected product timing, and bounded customer-choice evidence.

## Current status

The evidence supports a narrower finding than “Chanel was immune to the slowdown.” Chanel's consolidated revenue stabilized in FY2025 after a FY2024 decline, while operating profit remained well below FY2023. European and Americas reported revenue increases offset continued Asia Pacific softness. Retail and wholesale both recovered in FY2025, but retail remained below FY2023.

Beauty scale and CHANEL 25 daily-use accounts suggest mechanisms worth testing. Neither the available category data nor purposive public self-reports establish how much either mechanism contributed. The material is descriptive and accounting-based; it does not estimate marketing ROI, handbag-only demand, or causal contribution.

## Reports

- [研究状态与下一步](RESEARCH_STATUS_CN.md)
- [Integrated answer to the homepage question](reports/LUXURY_SLOWDOWN_SYNTHESIS_CN.md)
- [Relative performance across Chanel, Hermès, LVMH Fashion & Leather Goods, and Gucci](reports/RELATIVE_RESILIENCE_REVIEW_CN.md)
- [Geographic localization and industry context](reports/SLOWDOWN_LOCATION_REVIEW_CN.md)
- [Revenue and operating-profit bridge](reports/PROFIT_RECOVERY_REVIEW_CN.md)
- [Retail/wholesale bridge and product timing](reports/CHANNEL_PRODUCT_REVIEW_CN.md)
- [Customer-choice mechanisms and beauty scale](reports/CUSTOMER_BEAUTY_REVIEW_CN.md)

## Data and checks

`data/` contains the peer performance panel, Chanel regional and channel panels, filed-account profit inputs, product-timing ledger, and beauty-scale inputs. The beauty amount is a third-party estimate reproduced by L'Oréal from WWD, not an audited Chanel segment figure. The customer accounts were purposively selected public self-reports; this public package omits account handles and the row-level account ledger.

The `source_id` columns map to [SOURCE_INDEX.md](SOURCE_INDEX.md); sources are also linked at the corresponding claims in the reports.

Run the read-only reconciliation scripts from this directory with Python 3:

```bash
python3 checks/check_resilience.py
python3 checks/check_regional_bridge.py
python3 checks/check_profit_bridge.py
python3 checks/check_channel_bridge.py
```

The scripts validate arithmetic and selected table structures. They do not authenticate the underlying sources or establish causality. Sources are linked beside the relevant claims in each report.

## Research boundary and website handoff

Customer-choice validation has been withdrawn from the active plan by the user: there is no accessible client sample or recruitment route. Category, customer and marketing contribution remain unranked. The public-source phase closes with a bounded answer, not an interview promise. Use [the integrated website handoff](../website_handoff/README.md) for the next step: connecting price architecture, historical repricing and the slowdown diagnostic into one argument. Historical future directions in individual reports are not current tasks.

Prepared 2026-10-03. Historical company results and source links were checked as part of the underlying research. This is not an update to the project's handbag-price sample.
