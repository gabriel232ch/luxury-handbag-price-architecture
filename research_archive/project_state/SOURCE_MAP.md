# Pilot 001 source map

| Source class | URLs | Use |
|---|---|---|
| Official France category | https://www.chanel.com/fr/mode/sacs/c/1x1x1/ and `/page-2/` | SKU discovery |
| Official United States category | https://www.chanel.com/us/fashion/handbags/c/1x1x1/ and `/page-2/` | SKU discovery |
| Official product pages | `case/pilot_001/data/raw/observations.jsonl` | Current local price and product attributes |
| Direct runtime request | `case/pilot_001/execution_log.md` | HTTP 403 restriction evidence |

Only `chanel.com` sources enter the validated analytical population.

## Parent gap-review sources (separate from pilot price population)

Accessed 2026-10-03.

| ID | Source | Use / limit |
|---|---|---|
| LS-S01 | https://gabrielchen.me/ | User's original question and homepage narrative; read in browser, web retrieval unavailable |
| LS-S02 | https://gabrielchen.me/work/luxury-handbag-pricing-architecture/ | Published price/financial work and explicit evidence limits; not independently re-audited price dataset |
| LS-S03 | chanel_marketing_strategy_analysis.md | Existing marketing synthesis, window 2025-08-13–2026-08-13; interpretations not automatically validated |
| LS-S04 | https://www.chanel.com/puls-img/1747810519727-20250520fy24resultspressreleasefinalwwpdf.pdf | Official FY2024 release; company interpretation carries promotional incentives |
| LS-S05 | https://www.chanel.com/puls-img/1779118002743-fy25-results-press-release-en-final.pdf | Official FY2025 release, pp.1–4; consolidated, no numerical Fashion/handbag segment split |
| LS-S06 | https://www.bain.com/insights/luxury-in-transition-securing-future-growth/ | Bain–Altagamma 2024 study; industry estimates, not Chanel client evidence; vintage differs from later revisions |

## Relative-performance additions — accessed 2026-10-03

| ID | Source | Use / limit |
|---|---|---|
| LS-S07 | https://www.chanel.com/puls-img/1716301904618-pressrelease2023resultsengfinalpdf.pdf | FY2023 consolidated; revenue rounded |
| LS-S08 | https://assets-finance.hermes.com/s3fs-public/node/pdf_file/2025-02/1739475049/hermes_20250214_pr_2024fullyearresults_va.pdf | FY2024 and FY2023 key figures; adjusted FCF definition differs |
| LS-S09 | https://assets-finance.hermes.com/s3fs-public/node/pdf_file/2026-02/1770842738/hermes_20260212_pr_2025fullyearresults_va.pdf | FY2025 and FY2024 key figures; group recurring margin official 41.0% |
| LS-S10 | https://www.lvmh.com/en/publications/2023-new-record-year-for-lvmh | FY2023 FLG tables |
| LS-S11 | https://www.lvmh.com/en/publications/lvmh-achieves-a-solid-performance-despite-an-unfavorable-global-economic-environment | FY2024 FLG tables |
| LS-S12 | https://www.lvmh.com/en/publications/solid-performance-in-a-disrupted-global-economic-and-geopolitical-environment | FY2025 FLG tables |
| LS-S13 | https://www.kering.com/en/news/2023-annual-results/ | FY2023 Gucci growth/margin; not parent FCF |
| LS-S14 | https://www.kering.com/api/download-file/?path=Kering_Press_Release_Annual_Results_2024_110225_d0961a25d1.pdf | FY2024 and FY2023 Gucci revenue/profit |
| LS-S15 | https://www.kering.com/api/download-file/?path=Kering_2025_Results_Press_Release_4165ec0f25.pdf | FY2025 and FY2024 Gucci revenue/profit |
| LS-S16 | /Users/gabrielchen/Documents/ChatGPT/奢侈品/financial_business_performance/clean/financial_panel.csv | User-provided seed data with source registry and calculations; read-only reuse, official figures checked for this round |

All company sources are authoritative for disclosure but management causal explanations are interested-party interpretations. LS-S04/05 are reused for FY2024/25 Chanel. No additional external-source claims about marketing effectiveness were introduced.

## Slowdown localization — accessed 2026-10-03

| ID | Source / publication date | Use / limits |
|---|---|---|
| LS-S17 | https://www.chanel.com/puls-img/1747731312532-20250520fy24resultspressreleasefinalcnpdf.pdf ; 2025-05-20 | Official FY2024 Chinese release p.4: exact FY2023/24 regional revenue; corrects rounded seed FY2023 revenue to $19,744m. Same upstream source as LS-S04, not independent confirmation |
| LS-S18 | https://www.bain.com/insights/2024-china-luxury-goods-market/ ; 2025-01-21 | China FY2024 industry estimates, consumer-location shifts and cautious VICs; early vintage mainland decline 18–20% |
| LS-S19 | https://www.bain.cn/pdfs/202601300953122766.pdf ; released 2026-01-29 | FY2025 China report pp.1–6: mainland decline 3–5%, revised FY2024 17–19%, category divergence, client segments, overseas spending; secondary research/financial information/industry interviews, not independently verified by Bain |
| LS-S20 | https://www.bain.com.cn/news_info.php?id=2102 ; 2026-01-29 | Publisher's report announcement, category estimates and spending repatriation; same cluster as LS-S19 |
| LS-S21 | https://www.bain.com.cn/news_info.php?id=2073 ; 2025-11-25 | Global FY2025 near-year-end forecast: €358bn, constant-currency flat; revised by later historical update |
| LS-S22 | https://www.bain.cn/news_info.php?id=2150 ; 2026-07-14 Chinese publication | 2026 spring update's historical FY2025 figures: €358bn versus FY2024 €364bn, about −2% current/+1% constant currency; only historical paragraph used, no 2026 projection promoted to actual |

Hermès LS-S09 pp.6–7 reused for FY2025 region/category counterexample; AP excludes Japan, which is separate. Bain source pages/reports share an upstream research cluster; they are not counted as independent corroborations. English FY2024 Chanel PDF text extraction omitted the financial table; official Chinese version provided a directly readable table. Web screenshots were requested but wrapper returned text references only, so no unseen chart was used to assign values. All adopted numerical category ranges also appear in publisher prose.

## Revenue-profit bridge — accessed 2026-10-03

| ID | Source / filing date | Use / limits |
|---|---|---|
| LS-S23 | https://find-and-update.company-information.service.gov.uk/company/00203669/filing-history/MzUyNzQxOTg3MmFkaXF6a2N4/document?download=0&format=pdf ; filed 2026-06-29 | FY2025 group accounts, 199 PDF pages; printed pp.18–19 EBITDA definition/reconciliation, 116 consolidated USD income, 131 channels, 132 exceptional/finance, 133 staff. Image-only scan downloaded and pages viewed locally |
| LS-S24 | https://find-and-update.company-information.service.gov.uk/company/00203669/filing-history/MzQ2ODQzNTAzN2FkaXF6a2N4/document?download=0&format=pdf ; filed 2025-06-02 | FY2024 group accounts, 180 PDF pages; printed p.86 income with FY2023 comparative, 109 channel/exceptional, 111 staff |

Original PDFs retained under case/luxury_slowdown_2023_2025/sources; SHA256 and page offsets in working/PROFIT_STYLE_REVIEW.md. Company 00203669 is UK group parent; consolidated statements are USD, company-only statements not substituted. Web redirect retrieval failed, direct public-document download succeeded. No third-party GBP conversion used. Same upstream corporate disclosure as releases, not independent causal corroboration.

## Channel / product timing — 2026-10-03

| ID | Source | Use / limits |
|---|---|---|
| LS-S25 | https://pressroom.chanel.com/sites/8/chanel_campagne-pret-a-porter-printemps-ete-2025_en.pdf | Official SS2025 campaign release, one page: boutiques from March2025; no quantified collection sales |
| LS-S26 | https://www.chanel.com/gb/news-and-events/ | Chance Street London25April–5May2025; localized activation, not global launch date. Duplicate display sections deduplicated; ambiguous Bond Street year excluded |
| LS-S27 | https://www.purseblog.com/chanel/dua-lipa-fronts-the-new-chanel-25-bag-campaign/ ; published2025-02-03 | Original runway October2024, recent Dua preview, planned full campaign/store window March2025. Secondary timing only; affiliate incentives; comments not analyzed |
| LS-S28 | https://www.marieclaire.co.uk/fashion/the-one-chanel-25-handbag | Retrospective March2025 CHANEL25 release month; promotional claims not adopted; independence from brand communications not assumed |

Reused LS-S23 p.3 showOctober2025/arrivalMarch2026, p.27 Fashion, p.131 channels; LS-S24 p.109 channels; LS-S07/04/05 product/boutique highlights. Channels and availability rows visually verified from retained local PDFs. Current fashion campaign pages may reflect2026 Mini rather than original2025 campaign; not used to backdate.

## Customer / Beauty round — accessed 2026-10-03

| ID | Source | Use / limits |
|---|---|---|
| LS-S29 | https://www.reddit.com/r/chanel/comments/1jct9ib/megathread_my_first_chanel/ | First-purchase self-report with unresolved return concern; actor and exact-comment-date limits in CSV |
| LS-S30 | https://www.reddit.com/r/chanel/comments/1okv32a/im_buying_a_chanel_bag_for_my_40th_chanel_25_or/ | Thread2025-10-31; first buyer, joint owner, planned purchase; comments not automatically thread-dated |
| LS-S31 | https://www.reddit.com/r/chanel/comments/1oyed94/phew_finally_got_my_25_medium_the_scarcity_is/ | Thread2025-11-16; London/Tokyo purchase and US availability counterexample; no stock audit |
| LS-S32 | https://www.reddit.com/r/chanel/comments/1mxeq4d/chanel_25/ | Thread2025-08-22; January recalled purchase, return/rebuy, non-selection; anonymous unauthenticated |
| LS-S33 | https://forum.purseblog.com/threads/marvelous-march-2025-chanel-purchases.1074511/page-2 | Mar13,2025post18; 31/25 considered,22 selected; retail/resale route unspecified |
| LS-S34 | https://forum.purseblog.com/threads/fabulous-january-2025-chanel-purchases.1073181/page-5 | Feb2post65 and Feb8post73 contemporary early ownership leads; no SKU/receipt check |
| LS-S35 | https://www.loreal-finance.com/eng/2025-universal-registration-document/en/article/23/ | FY2025URD printed23/PDF25 has FY2024 beauty sales graph ChanelUSD8.54bn; WWD April2025 upstream, not audited Chanel segment |
| LS-S36 | https://www.diarydirectory.com/newsarticle/wwd-reveals-the-2025-top-100-beauty-companies/71474 ; posted2026-04-20 | WWD FY2025 ranking reproduction ChanelUSD9.18bn EST; candidate, not comparable contribution input |

Reddit/PurseForum public firsthand self-reports, not verified customers; enthusiast-selection and anonymous recall bias. No interview invitations, private-account inspection or identity enrichment. L'Oreal/DIARY same WWD cluster, not independent corroboration. WWD full original unavailable402/homepage; Yahoo FY2024 unavailable429. Search-only mirrors of growth3.1% retained only as unresolved comparability warning, not validated growth. Full local PDF and SHA256 in working/CUSTOMER_BEAUTY_STYLE_COVERAGE.md.
