from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FINANCIAL_ROOT = ROOT / "financial_business_performance"
RAW_DIR = FINANCIAL_ROOT / "raw"
CLEAN_DIR = FINANCIAL_ROOT / "clean"
SOURCE_DIR = FINANCIAL_ROOT / "sources"
LOG_DIR = FINANCIAL_ROOT / "logs"
RESEARCH_AS_OF = "2026-09-10"


FIELDNAMES = [
    "observation_id",
    "entity",
    "reporting_scope",
    "segment",
    "fiscal_year",
    "period",
    "metric",
    "value",
    "unit",
    "currency",
    "reported_or_constant_currency",
    "source_type",
    "source_id",
    "source_title",
    "source_url",
    "publication_date",
    "page_or_section",
    "extraction_note",
    "confidence",
    "caveat",
    "selection_status",
    "metric_status",
    "precision_note",
    "source_basis",
]


SOURCE_FIELDS = [
    "source_id",
    "entity",
    "reporting_scope",
    "source_type",
    "source_title",
    "source_url",
    "publication_date",
    "official_or_secondary",
    "page_or_section",
    "notes",
]


SCOPE_FIELDS = [
    "entity",
    "financial_grain",
    "segment_scope",
    "suitable_use",
    "not_comparable_to",
    "notes",
]


SOURCES = [
    {
        "source_id": "CH-FY17",
        "entity": "Chanel",
        "reporting_scope": "consolidated_company",
        "source_type": "official_financial_release",
        "source_title": "CHANEL Limited Financial Results for the year ended 31 December 2017",
        "source_url": "https://www.chanel.com/puls-img/1730292703276-chanellimitedfinancialresultsfortheyearended31december2017emeapdf.pdf",
        "publication_date": "2018-06-21",
        "official_or_secondary": "official",
        "page_or_section": "pp. 1, 3 / Financial Highlights",
        "notes": "Chanel Limited consolidates the main entities of CHANEL worldwide; 2017 source reports rounded and exact million-dollar figures.",
    },
    {
        "source_id": "CH-FY18",
        "entity": "Chanel",
        "reporting_scope": "consolidated_company",
        "source_type": "official_financial_release",
        "source_title": "CHANEL Limited Financial Results for the year ended 31 December 2018",
        "source_url": "https://www.chanel.com/puls-img/1730301368943-chanellimitedfinancialresultsfortheyearended31december2018pdf.pdf",
        "publication_date": "2019-06-17",
        "official_or_secondary": "official",
        "page_or_section": "pp. 1, 3 / Financial Highlights",
        "notes": "2017 comparative is restated for merger accounting related to common-control entities.",
    },
    {
        "source_id": "CH-FY19",
        "entity": "Chanel",
        "reporting_scope": "consolidated_company",
        "source_type": "official_financial_release",
        "source_title": "CHANEL Limited Financial Results for the year ended 31 December 2019",
        "source_url": "https://www.chanel.com/puls-img/1730292703542-chanellimitedfinancialresultsfortheyearended31december2019emeapdf.pdf",
        "publication_date": "2020-06-18",
        "official_or_secondary": "official",
        "page_or_section": "pp. 1, 3 / Financial Summary and definitions",
        "notes": "Company-wide consolidated figures; free cash flow and capital investment definitions are retained in the source notes.",
    },
    {
        "source_id": "CH-FY20",
        "entity": "Chanel",
        "reporting_scope": "consolidated_company",
        "source_type": "official_financial_release",
        "source_title": "CHANEL Limited Financial Results for the year ended 31 December 2020",
        "source_url": "https://www.chanel.com/puls-img/1730292703574-pressrelease2020resultsengfinalemeapdf.pdf",
        "publication_date": "2021-06-15",
        "official_or_secondary": "official",
        "page_or_section": "pp. 1–2 / Financial Highlights",
        "notes": "Original FY2020 release; FY2021 later restated certain financial KPIs after a SaaS accounting policy change.",
    },
    {
        "source_id": "CH-FY21",
        "entity": "Chanel",
        "reporting_scope": "consolidated_company",
        "source_type": "official_financial_release",
        "source_title": "CHANEL Limited Financial Results for the year ended 31 December 2021",
        "source_url": "https://www.chanel.com/puls-img/1730292703516-pressrelease2021resultsengfinalemeapdf.pdf",
        "publication_date": "2022-05-24",
        "official_or_secondary": "official",
        "page_or_section": "p. 3 / 2021–2020 (restated)–2019 (restated) table",
        "notes": "Selected basis for the main 2020–2025 Chanel panel where the release explicitly provides restated comparatives.",
    },
    {
        "source_id": "CH-FY22",
        "entity": "Chanel",
        "reporting_scope": "consolidated_company",
        "source_type": "official_financial_release",
        "source_title": "CHANEL Limited Financial Results for the year ended 31 December 2022",
        "source_url": "https://www.chanel.com/puls-img/1730292703537-10202336657438pressrelease2022resultsengfinalemeapdf.pdf",
        "publication_date": "2023-05-25",
        "official_or_secondary": "official",
        "page_or_section": "pp. 1–2 / Financial Highlights and operational highlights",
        "notes": "Revenue is reported as $17.2bn in the release; stored as rounded $17,200m, not false-precision exact revenue.",
    },
    {
        "source_id": "CH-FY23",
        "entity": "Chanel",
        "reporting_scope": "consolidated_company",
        "source_type": "official_financial_release",
        "source_title": "CHANEL Limited Financial Results for the year ended 31 December 2023",
        "source_url": "https://www.chanel.com/puls-img/1716301904618-pressrelease2023resultsengfinalpdf.pdf",
        "publication_date": "2024-05-21",
        "official_or_secondary": "official",
        "page_or_section": "pp. 1–2 / Financial Highlights and operational highlights",
        "notes": "Revenue is reported as $19.7bn in the release; stored as rounded $19,700m.",
    },
    {
        "source_id": "CH-FY24",
        "entity": "Chanel",
        "reporting_scope": "consolidated_company",
        "source_type": "official_financial_release",
        "source_title": "CHANEL Limited Financial Results for the year ended 31 December 2024",
        "source_url": "https://www.chanel.com/puls-img/1747810519727-20250520fy24resultspressreleasefinalwwpdf.pdf",
        "publication_date": "2025-05-20",
        "official_or_secondary": "official",
        "page_or_section": "pp. 1–2 / Financial Highlights and investment commentary",
        "notes": "2024 release labels the year a record year of investment and explains the comparable-growth basis.",
    },
    {
        "source_id": "CH-FY25",
        "entity": "Chanel",
        "reporting_scope": "consolidated_company",
        "source_type": "official_financial_release",
        "source_title": "CHANEL Limited Financial Results for the year ended 31 December 2025",
        "source_url": "https://www.chanel.com/puls-img/1779118002743-fy25-results-press-release-en-final.pdf",
        "publication_date": "2026-05-19",
        "official_or_secondary": "official",
        "page_or_section": "pp. 1, 4 / Financial Highlights and definitions",
        "notes": "2025 release reports $19,269m revenue, reported +3.0% and comparable +1.8%; source publication is after FY2025 close.",
    },
    {
        "source_id": "HM-FY20",
        "entity": "Hermès",
        "reporting_scope": "group_and_métier",
        "source_type": "official_urd",
        "source_title": "Hermès 2020 Universal Registration Document",
        "source_url": "https://assets-finance.hermes.com/s3fs-public/node/pdf_file/2021-04/1619702282/hermes-urd2020-en.pdf",
        "publication_date": "2021-04-29",
        "official_or_secondary": "official",
        "page_or_section": "pp. 25, 26, 370–371 / key consolidated data and revenue by métier",
        "notes": "2020 group and Leather Goods & Saddlery revenue, recurring operating income, operating investments and adjusted free cash flow.",
    },
    {
        "source_id": "HM-FY21",
        "entity": "Hermès",
        "reporting_scope": "group_and_métier",
        "source_type": "official_urd",
        "source_title": "Hermès 2021 Universal Registration Document",
        "source_url": "https://assets-finance.hermes.com/s3fs-public/node/pdf_file/2022-04/1650894186/HERMES-URD2021-EN_03.pdf",
        "publication_date": "2022-04-08",
        "official_or_secondary": "official",
        "page_or_section": "p. 371 / revenue and activity by métier",
        "notes": "2021 group and Leather Goods & Saddlery revenue, mix and current / constant growth; FY2022 release supplies group profitability and investment comparatives.",
    },
    {
        "source_id": "HM-FY22",
        "entity": "Hermès",
        "reporting_scope": "group_and_métier",
        "source_type": "official_financial_release",
        "source_title": "Hermès 2022 Full-Year Results",
        "source_url": "https://assets-finance.hermes.com/s3fs-public/node/pdf_file/2023-02/1676575550/hermes_20230217_pr_2022fullyearresults_va.pdf",
        "publication_date": "2023-02-17",
        "official_or_secondary": "official",
        "page_or_section": "pp. 1, 5–6 / results and key figures",
        "notes": "2022 group and Leather Goods & Saddlery revenue, growth, recurring operating income, margin, investments and adjusted free cash flow.",
    },
    {
        "source_id": "HM-FY23",
        "entity": "Hermès",
        "reporting_scope": "group_and_métier",
        "source_type": "official_financial_release",
        "source_title": "Hermès 2023 Full-Year Results",
        "source_url": "https://assets-finance.hermes.com/s3fs-public/node/pdf_file/2024-02/1707422069/hermes_20240209_pr_2023fullyearresults_va.pdf",
        "publication_date": "2024-02-09",
        "official_or_secondary": "official",
        "page_or_section": "pp. 1–3, 5–7 / results, investments and sector revenue",
        "notes": "Leather Goods & Saddlery includes bags, riding, memory holders and small leather goods; 2023 release gives group recurring profitability and investment.",
    },
    {
        "source_id": "HM-FY24",
        "entity": "Hermès",
        "reporting_scope": "group_and_métier",
        "source_type": "official_financial_release",
        "source_title": "Hermès 2024 Full-Year Results",
        "source_url": "https://assets-finance.hermes.com/s3fs-public/node/pdf_file/2025-02/1739475049/hermes_20250214_pr_2024fullyearresults_va.pdf",
        "publication_date": "2025-02-14",
        "official_or_secondary": "official",
        "page_or_section": "pp. 1, 5–7 / results and revenue by sector",
        "notes": "2024 Leather Goods & Saddlery revenue and current / constant growth; group profitability, investments and adjusted free cash flow.",
    },
    {
        "source_id": "HM-FY25",
        "entity": "Hermès",
        "reporting_scope": "group_and_métier",
        "source_type": "official_financial_release",
        "source_title": "Hermès 2025 Full-Year Results",
        "source_url": "https://assets-finance.hermes.com/s3fs-public/node/pdf_file/2026-02/1770842738/hermes_20260212_pr_2025fullyearresults_va.pdf",
        "publication_date": "2026-02-12",
        "official_or_secondary": "official",
        "page_or_section": "pp. 1, 5–7 / results and revenue by sector",
        "notes": "2025 Leather Goods & Saddlery revenue of €7,070m and group recurring operating margin of 41.0%; PDF query parameters are omitted from the canonical URL.",
    },
    {
        "source_id": "LVMH-FY20",
        "entity": "LVMH",
        "reporting_scope": "group_and_business_group",
        "source_type": "official_annual_results",
        "source_title": "LVMH showed good resilience against the pandemic crisis in 2020",
        "source_url": "https://www.lvmh.com/en/publications/lvmh-showed-good-resilience-against-the-pandemic-crisis-in-2020",
        "publication_date": "2021-01-26",
        "official_or_secondary": "official",
        "page_or_section": "Revenue and profit from recurring operations by business group",
        "notes": "Fashion & Leather Goods segment revenue, reported / organic growth and recurring operating profit; LV and Christian Dior commentary is qualitative.",
    },
    {
        "source_id": "LVMH-FY21",
        "entity": "LVMH",
        "reporting_scope": "group_and_business_group",
        "source_type": "official_annual_results",
        "source_title": "New records for LVMH in 2021",
        "source_url": "https://www.lvmh.com/en/publications/new-records-for-lvmh-in-2021",
        "publication_date": "2022-01-27",
        "official_or_secondary": "official",
        "page_or_section": "Revenue and profit from recurring operations by business group",
        "notes": "Fashion & Leather Goods segment revenue, reported / organic growth and recurring operating profit; multi-brand segment, not standalone brand revenue.",
    },
    {
        "source_id": "LVMH-FY22",
        "entity": "LVMH",
        "reporting_scope": "group_and_business_group",
        "source_type": "official_annual_results",
        "source_title": "New record year for LVMH in 2022",
        "source_url": "https://www.lvmh.com/en/publications/new-record-year-for-lvmh-in-2022",
        "publication_date": "2023-01-26",
        "official_or_secondary": "official",
        "page_or_section": "Revenue and profit from recurring operations by business group",
        "notes": "Fashion & Leather Goods segment revenue, reported / organic growth and recurring operating profit.",
    },
    {
        "source_id": "LVMH-FY23",
        "entity": "LVMH",
        "reporting_scope": "group_and_business_group",
        "source_type": "official_annual_results",
        "source_title": "2023: New record year for LVMH",
        "source_url": "https://www.lvmh.com/en/publications/2023-new-record-year-for-lvmh",
        "publication_date": "2024-01-25",
        "official_or_secondary": "official",
        "page_or_section": "Financial highlights and business-group revenue / profit tables",
        "notes": "Fashion & Leather Goods segment revenue, reported +9%, organic +14%, and recurring operating profit.",
    },
    {
        "source_id": "LVMH-FY24",
        "entity": "LVMH",
        "reporting_scope": "group_and_business_group",
        "source_type": "official_annual_results",
        "source_title": "LVMH achieves a solid performance despite an unfavorable global economic environment",
        "source_url": "https://www.lvmh.com/en/publications/lvmh-achieves-a-solid-performance-despite-an-unfavorable-global-economic-environment",
        "publication_date": "2025-01-28",
        "official_or_secondary": "official",
        "page_or_section": "Financial highlights and Fashion & Leather Goods section",
        "notes": "Fashion & Leather Goods segment revenue, reported -3%, organic -1%, recurring operating profit; commentary attributes profit pressure mainly to FX.",
    },
    {
        "source_id": "LVMH-FY25",
        "entity": "LVMH",
        "reporting_scope": "group_and_business_group",
        "source_type": "official_annual_results",
        "source_title": "Solid performance in a disrupted global economic and geopolitical environment",
        "source_url": "https://www.lvmh.com/en/publications/solid-performance-in-a-disrupted-global-economic-and-geopolitical-environment",
        "publication_date": "2026-01-27",
        "official_or_secondary": "official",
        "page_or_section": "Financial highlights and Fashion & Leather Goods section",
        "notes": "Fashion & Leather Goods segment revenue, reported -8%, organic -5%, recurring operating profit and 35% segment margin.",
    },
]


SCOPE_MATRIX = [
    {
        "entity": "Chanel",
        "financial_grain": "Consolidated company",
        "segment_scope": "All Chanel group activities",
        "suitable_use": "Chanel business performance",
        "not_comparable_to": "Chanel handbag-only revenue or margin",
        "notes": "Private company; disclosed revenue includes Fashion, Leather Goods, Watches & Fine Jewellery, Fragrance & Beauty and other activities.",
    },
    {
        "entity": "Hermès",
        "financial_grain": "Group + Leather Goods & Saddlery métier",
        "segment_scope": "Bags, travel items, small leather goods, saddlery and equestrian products",
        "suitable_use": "Strong leather-goods benchmark",
        "not_comparable_to": "Chanel handbag-only revenue; Hermès handbag-only revenue",
        "notes": "The métier is broader than handbags; group profitability is used because segment profit is not disclosed in this evidence set.",
    },
    {
        "entity": "LVMH",
        "financial_grain": "Group + Fashion & Leather Goods business group",
        "segment_scope": "Multi-brand Fashion & Leather Goods segment",
        "suitable_use": "Broad luxury leather-goods environment benchmark",
        "not_comparable_to": "Louis Vuitton revenue; Dior brand revenue; Chanel consolidated revenue ranking in nominal currency",
        "notes": "Louis Vuitton and Christian Dior are discussed only qualitatively where official releases name them.",
    },
    {
        "entity": "Louis Vuitton",
        "financial_grain": "No standalone audited brand financials in this evidence set",
        "segment_scope": "Not separately disclosed",
        "suitable_use": "Qualitative brand context only",
        "not_comparable_to": "Standalone revenue, margin or profit",
        "notes": "Do not relabel LVMH Fashion & Leather Goods figures as Louis Vuitton.",
    },
    {
        "entity": "Dior",
        "financial_grain": "No comparable standalone couture-brand financials in this evidence set",
        "segment_scope": "Not separately disclosed",
        "suitable_use": "Qualitative brand context only",
        "not_comparable_to": "Standalone Dior couture revenue, margin or profit",
        "notes": "Christian Dior SE / Finance consolidated figures are not used as standalone Dior couture-brand performance.",
    },
]


def source_by_id(source_id: str) -> dict:
    return next(source for source in SOURCES if source["source_id"] == source_id)


def observation(
    observation_id: str,
    entity: str,
    reporting_scope: str,
    segment: str,
    fiscal_year: str,
    metric: str,
    value,
    unit: str,
    currency: str,
    source_id: str,
    page_or_section: str,
    extraction_note: str,
    *,
    reported_or_constant_currency: str = "not_applicable",
    selection_status: str = "selected",
    metric_status: str = "reported",
    confidence: str = "high",
    caveat: str = "",
    precision_note: str = "exact",
    source_basis: str = "current_year_release",
) -> dict:
    source = source_by_id(source_id)
    return {
        "observation_id": observation_id,
        "entity": entity,
        "reporting_scope": reporting_scope,
        "segment": segment,
        "fiscal_year": str(fiscal_year),
        "period": "FY",
        "metric": metric,
        "value": "" if value is None else str(value),
        "unit": unit,
        "currency": currency,
        "reported_or_constant_currency": reported_or_constant_currency,
        "source_type": source["source_type"],
        "source_id": source_id,
        "source_title": source["source_title"],
        "source_url": source["source_url"],
        "publication_date": source["publication_date"],
        "page_or_section": page_or_section,
        "extraction_note": extraction_note,
        "confidence": confidence,
        "caveat": caveat,
        "selection_status": selection_status,
        "metric_status": metric_status,
        "precision_note": precision_note,
        "source_basis": source_basis,
    }


def unavailable(
    observation_id: str,
    entity: str,
    reporting_scope: str,
    segment: str,
    metric: str,
    caveat: str,
) -> dict:
    return {
        "observation_id": observation_id,
        "entity": entity,
        "reporting_scope": reporting_scope,
        "segment": segment,
        "fiscal_year": "2017-2025",
        "period": "full_history",
        "metric": metric,
        "value": "",
        "unit": "not_available",
        "currency": "not_available",
        "reported_or_constant_currency": "not_applicable",
        "source_type": "scope_boundary",
        "source_id": "SCOPE-BOUNDARY",
        "source_title": "Financial scope and non-estimables register",
        "source_url": "",
        "publication_date": RESEARCH_AS_OF,
        "page_or_section": "scope matrix",
        "extraction_note": "No reliable public disclosure was found in the defined source universe.",
        "confidence": "na",
        "caveat": caveat,
        "selection_status": "unavailable",
        "metric_status": "unavailable",
        "precision_note": "not_estimable",
        "source_basis": "scope_boundary",
    }


def chanel_rows() -> list[dict]:
    rows = []
    data = {
        "2017": {"revenue": 9623, "comparable_growth": 11.0, "operating_profit": 2692, "free_cash_flow": 1628, "capex": 429, "brand_support_investment": 1457, "employees": 20197, "source": "CH-FY17", "note": "Exact million-dollar table values; comparable revenue growth is source-reported.", "page": "p. 3 / Financial Highlights"},
        "2018": {"revenue": 11119, "comparable_growth": 10.5, "operating_profit": 2998, "free_cash_flow": 1214, "capex": 1007, "brand_support_investment": 1653, "employees": 25295, "source": "CH-FY18", "note": "Exact million-dollar table values; 2017 comparative is restated in source.", "page": "p. 3 / Financial Highlights"},
        "2019": {"revenue": 12273, "comparable_growth": 13.0, "operating_profit": 3496, "free_cash_flow": 2245, "capex": 771, "brand_support_investment": 1770, "employees": 27713, "source": "CH-FY19", "note": "Exact million-dollar table values.", "page": "p. 1 / Key 2019 Financial Information"},
        "2020": {"revenue": 10108, "comparable_growth": -18.0, "operating_profit": 2018, "free_cash_flow": 679, "capex": 1077, "brand_support_investment": 1360, "employees": 27018, "source": "CH-FY21", "note": "Selected restated comparative from FY2021 release for consistent 2020–2025 series; revenue and cash flow are unchanged from original release, while certain KPIs were restated after SaaS accounting policy change.", "page": "p. 3 / 2021–2020 (restated)–2019 (restated) table", "basis": "FY2021_restated_comparative"},
        "2021": {"revenue": 15639, "comparable_growth": 49.6, "operating_profit": 5461, "free_cash_flow": 4540, "capex": 758, "brand_support_investment": 1795, "employees": 28467, "source": "CH-FY21", "note": "Exact million-dollar table values.", "page": "p. 3 / Financial Highlights"},
        "2022": {"revenue": 17200, "comparable_growth": 17.0, "operating_profit": 5776, "free_cash_flow": 3534, "capex": 668, "brand_support_investment": 2052, "employees": 32000, "source": "CH-FY22", "note": "Revenue is rounded from the release’s $17.2bn; other values are source-reported million-dollar figures.", "page": "p. 1 / Key Financial Highlights", "precision": "rounded_to_nearest_100m_revenue"},
        "2023": {"revenue": 19700, "comparable_growth": 16.0, "operating_profit": 6407, "free_cash_flow": 3755, "capex": 1227, "brand_support_investment": 2463, "employees": 36500, "source": "CH-FY23", "note": "Revenue is rounded from the release’s $19.7bn; other values are source-reported million-dollar figures.", "page": "p. 1 / Key Financial Highlights", "precision": "rounded_to_nearest_100m_revenue"},
        "2024": {"revenue": 18699, "comparable_growth": -4.3, "operating_profit": 4479, "free_cash_flow": 1842, "capex": 1755, "brand_support_investment": 2445, "employees": 38422, "source": "CH-FY24", "note": "Exact million-dollar revenue and operating / cash / investment figures; source highlights 2024 revenue down 4.3% on comparable constant-currency basis.", "page": "p. 1 / Key 2024 Financial Highlights"},
        "2025": {"revenue": 19269, "comparable_growth": 1.8, "reported_growth": 3.0, "operating_profit": 4712, "free_cash_flow": 2646, "capex": 1449, "brand_support_investment": 2395, "employees": 37984, "source": "CH-FY25", "note": "Exact million-dollar table values; source reports +3.0% reported and +1.8% comparable growth.", "page": "p. 4 / Highlights table"},
    }
    for year, item in data.items():
        common = {
            "entity": "Chanel",
            "reporting_scope": "consolidated_company",
            "segment": "",
            "fiscal_year": year,
            "currency": "USD",
            "source_id": item["source"],
            "page_or_section": item["page"],
            "extraction_note": item["note"],
            "caveat": "Consolidated company; not handbag-only."
            + (" Rounded revenue; derived margins should be read as approximate." if item.get("precision") else ""),
            "precision_note": item.get("precision", "exact"),
            "source_basis": item.get("basis", "current_year_release"),
        }
        for metric in ["revenue", "operating_profit", "free_cash_flow", "capex", "brand_support_investment", "employees"]:
            rows.append(observation(
                f"CH-{year}-{metric}",
                metric=metric,
                value=item.get(metric),
                unit="USD_m",
                **common,
            ))
        growth_common = dict(common)
        rows.append(observation(
            f"CH-{year}-comparable-growth",
            metric="comparable_growth",
            value=item.get("comparable_growth"),
            reported_or_constant_currency="constant_currency_comparable_structure",
            unit="percent",
            **growth_common,
        ))
        if item.get("reported_growth") is not None:
            rows.append(observation(
                f"CH-{year}-reported-growth",
                metric="reported_growth",
                value=item["reported_growth"],
                reported_or_constant_currency="reported_current_exchange_rate",
                unit="percent",
                **common,
            ))
    rows.extend([
        unavailable("CH-NA-handbag-revenue", "Chanel", "consolidated_company", "", "handbag_revenue", "Chanel does not publicly disclose handbag-only revenue; not estimable from consolidated accounts."),
        unavailable("CH-NA-handbag-units", "Chanel", "consolidated_company", "", "handbag_units", "Handbag unit sales are not publicly disclosed."),
        unavailable("CH-NA-handbag-margin", "Chanel", "consolidated_company", "", "handbag_gross_margin", "Handbag gross margin is not publicly disclosed."),
        unavailable("CH-NA-classic-revenue", "Chanel", "consolidated_company", "", "classic_revenue", "Classic handbag revenue is not publicly disclosed."),
    ])
    # Preserve the original FY2020 KPI observations in the clean source layer.
    original_2020 = {
        "operating_profit": 2049,
        "capex": 1120,
        "brand_support_investment": 1360,
        "free_cash_flow": 679,
    }
    for metric, value in original_2020.items():
        rows.append(observation(
            f"CH-2020-original-{metric}",
            "Chanel",
            "consolidated_company",
            "",
            "2020",
            metric,
            value,
            "USD_m",
            "USD",
            "CH-FY20",
            "p. 1 / Key Financial Highlights",
            "Original FY2020 release; preserved as comparative-only because FY2021 later restated certain financial KPIs.",
            selection_status="comparative_only",
            caveat="Original FY2020 release; main panel uses FY2021 restated comparative for the affected KPI series.",
            source_basis="original_year_release",
        ))
    return rows


def hermes_rows() -> list[dict]:
    rows = []
    data = {
        "2020": {"group_revenue": 6389.4, "group_growth_reported": -7.2, "group_growth_constant": -6.0, "group_op": 1981.4, "group_margin": 31.0, "investments": 448.4, "fcf": 995.3, "leather_revenue": 3209.2, "leather_growth_reported": -6.0, "leather_growth_constant": -4.8, "source": "HM-FY20", "page": "pp. 25–26, 370–371"},
        "2021": {"group_revenue": 8982, "group_growth_reported": 40.6, "group_growth_constant": 41.8, "group_op": 3530, "group_margin": 39.3, "investments": 532, "fcf": 2661, "leather_revenue": 4091, "leather_growth_reported": 27.0, "leather_growth_constant": 29.0, "source": "HM-FY21", "group_source": "HM-FY22", "page": "p. 371 / revenue and activity by métier"},
        "2022": {"group_revenue": 11602, "group_growth_reported": 29.2, "group_growth_constant": 23.4, "group_op": 4697, "group_margin": 40.5, "investments": 518, "fcf": 3405, "leather_revenue": 4963, "leather_growth_reported": 21.3, "leather_growth_constant": 15.6, "source": "HM-FY22", "page": "pp. 5–6 / key figures and sector revenue"},
        "2023": {"group_revenue": 13427, "group_growth_reported": 15.7, "group_growth_constant": 20.6, "group_op": 5650, "group_margin": 42.1, "investments": 859, "fcf": 3192, "leather_revenue": 5547, "leather_growth_reported": 11.8, "leather_growth_constant": 16.7, "source": "HM-FY23", "page": "pp. 5–7 / key figures and sector revenue"},
        "2024": {"group_revenue": 15170, "group_growth_reported": 13.0, "group_growth_constant": 14.7, "group_op": 6150, "group_margin": 40.5, "investments": 1067, "fcf": 3767, "leather_revenue": 6457, "leather_growth_reported": 16.4, "leather_growth_constant": 18.3, "source": "HM-FY24", "page": "pp. 5–7 / key figures and revenue by sector"},
        "2025": {"group_revenue": 16002, "group_growth_reported": 5.5, "group_growth_constant": 8.9, "group_op": 6569, "group_margin": 41.0, "investments": 1161, "fcf": 3880, "leather_revenue": 7070, "leather_growth_reported": 9.5, "leather_growth_constant": 13.1, "source": "HM-FY25", "page": "pp. 5–7 / key figures and revenue by sector"},
    }
    for year, item in data.items():
        common = {
            "reporting_scope": "group_and_métier",
            "fiscal_year": year,
            "currency": "EUR",
            "source_id": item.get("group_source", item["source"]),
            "page_or_section": item["page"],
            "extraction_note": "Official Hermès value; Leather Goods & Saddlery includes more than handbags.",
            "caveat": "Hermès group and métier grain; Leather Goods & Saddlery includes bags, travel, small leather goods, saddlery and equestrian products.",
        }
        for metric, value in [("revenue", item["group_revenue"]), ("operating_profit", item["group_op"]), ("reported_operating_margin", item["group_margin"]), ("operating_investments", item["investments"]), ("adjusted_free_cash_flow", item["fcf"]), ("reported_growth", item["group_growth_reported"]), ("comparable_growth", item["group_growth_constant"])]:
            rows.append(observation(
                f"HM-{year}-group-{metric}",
                "Hermès",
                segment="",
                metric=metric,
                value=value,
                unit="percent" if metric in ("reported_growth", "comparable_growth", "reported_operating_margin") else "EUR_m",
                reported_or_constant_currency=("reported_current_exchange_rate" if metric == "reported_growth" else "constant_currency" if metric == "comparable_growth" else "reported" if metric == "reported_operating_margin" else "not_applicable"),
                **common,
            ))
        leather_common = dict(common)
        leather_common["source_id"] = item["source"]
        for metric, value in [("revenue", item["leather_revenue"]), ("reported_growth", item["leather_growth_reported"]), ("comparable_growth", item["leather_growth_constant"])]:
            rows.append(observation(
                f"HM-{year}-leather-{metric}",
                "Hermès",
                segment="Leather Goods & Saddlery",
                metric=metric,
                value=value,
                unit="percent" if metric in ("reported_growth", "comparable_growth") else "EUR_m",
                reported_or_constant_currency=("reported_current_exchange_rate" if metric == "reported_growth" else "constant_currency" if metric == "comparable_growth" else "not_applicable"),
                **leather_common,
            ))
    rows.append(unavailable("HM-NA-leather-profit", "Hermès", "group_and_métier", "Leather Goods & Saddlery", "segment_operating_profit", "Hermès does not disclose Leather Goods & Saddlery operating profit in the source set; group recurring operating income is the compatible profitability context."))
    return rows


def lvmh_rows() -> list[dict]:
    rows = []
    data = {
        "2020": {"group_revenue": 44651, "flg_revenue": 21207, "reported": -5.0, "organic": -3.0, "flg_op": 7188, "source": "LVMH-FY20"},
        "2021": {"group_revenue": 64215, "flg_revenue": 30896, "reported": 46.0, "organic": 47.0, "flg_op": 12842, "source": "LVMH-FY21"},
        "2022": {"group_revenue": 79184, "flg_revenue": 38648, "reported": 25.0, "organic": 20.0, "flg_op": 15709, "source": "LVMH-FY22"},
        "2023": {"group_revenue": 86153, "flg_revenue": 42169, "reported": 9.0, "organic": 14.0, "flg_op": 16836, "source": "LVMH-FY23"},
        "2024": {"group_revenue": 84683, "flg_revenue": 41060, "reported": -3.0, "organic": -1.0, "flg_op": 15230, "source": "LVMH-FY24"},
        "2025": {"group_revenue": 80807, "flg_revenue": 37770, "reported": -8.0, "organic": -5.0, "flg_op": 13209, "source": "LVMH-FY25"},
    }
    for year, item in data.items():
        source = source_by_id(item["source"])
        common = {
            "reporting_scope": "group_and_business_group",
            "fiscal_year": year,
            "currency": "EUR",
            "source_id": item["source"],
            "page_or_section": "official annual-results business-group tables",
            "extraction_note": "Official LVMH value; Fashion & Leather Goods is a multi-brand business group.",
            "caveat": "LVMH Fashion & Leather Goods is not Louis Vuitton or Dior standalone financial performance.",
        }
        rows.append(observation(f"LVMH-{year}-group-revenue", "LVMH", segment="", metric="revenue", value=item["group_revenue"], unit="EUR_m", **common))
        for metric, value, basis in [
            ("revenue", item["flg_revenue"], "current_year_release"),
            ("reported_growth", item["reported"], "current_year_release"),
            ("organic_growth", item["organic"], "current_year_release"),
            ("operating_profit", item["flg_op"], "current_year_release"),
        ]:
            rows.append(observation(
                f"LVMH-{year}-flg-{metric}",
                "LVMH",
                segment="Fashion & Leather Goods",
                metric=metric,
                value=value,
                unit="percent" if metric in ("reported_growth", "organic_growth") else "EUR_m",
                reported_or_constant_currency=("reported_current_exchange_rate" if metric == "reported_growth" else "constant_currency_organic" if metric == "organic_growth" else "not_applicable"),
                source_basis=basis,
                **common,
            ))
    rows.append(unavailable("LVMH-NA-flg-investments", "LVMH", "group_and_business_group", "Fashion & Leather Goods", "segment_operating_investments", "Segment-level investment is not consistently disclosed in the source set; group operating investments are not substituted into the segment panel."))
    rows.append(unavailable("LVMH-NA-lv-revenue", "Louis Vuitton", "brand_level", "", "standalone_brand_revenue", "No standalone audited Louis Vuitton revenue is disclosed in this evidence set."))
    rows.append(unavailable("LVMH-NA-dior-revenue", "Dior", "brand_level", "", "standalone_brand_revenue", "No comparable standalone Dior couture-brand revenue is disclosed; LVMH segment or Christian Dior SE figures are not substituted."))
    return rows


def all_observations() -> list[dict]:
    return chanel_rows() + hermes_rows() + lvmh_rows()


def normalize_value(value: str) -> str:
    if value is None:
        return ""
    raw = str(value).strip()
    if not raw:
        return ""
    raw = raw.replace(",", "").replace(" ", "")
    raw = raw.replace("%", "")
    if re.fullmatch(r"-?\d+\.0+", raw):
        return str(int(float(raw)))
    return raw


def normalize_observation(row: dict) -> dict:
    normalized = {field: str(row.get(field, "") or "").strip() for field in FIELDNAMES}
    normalized["value"] = normalize_value(row.get("value", ""))
    normalized["fiscal_year"] = str(row.get("fiscal_year", "") or "").strip()
    normalized["period"] = str(row.get("period", "FY") or "FY").strip()
    return normalized


def _panel_key(row: dict) -> tuple:
    return (
        row["entity"],
        row["reporting_scope"],
        row["segment"],
        row["fiscal_year"],
        row["period"],
        row["metric"],
        row["unit"],
        row["currency"],
        row["reported_or_constant_currency"],
    )


def build_panel(raw_rows: list[dict]) -> dict:
    panel = [normalize_observation(row) for row in raw_rows]
    grouped: dict[tuple, list[dict]] = {}
    for row in panel:
        grouped.setdefault(_panel_key(row), []).append(row)
    conflicts = []
    for key, rows in grouped.items():
        values = sorted({row["value"] for row in rows if row["value"] != ""})
        if len(values) > 1:
            conflicts.append({
                "conflict_key": "|".join(key),
                "entity": key[0],
                "reporting_scope": key[1],
                "segment": key[2],
                "fiscal_year": key[3],
                "period": key[4],
                "metric": key[5],
                "unit": key[6],
                "currency": key[7],
                "reported_or_constant_currency": key[8],
                "values": ";".join(values),
                "observation_ids": ";".join(row["observation_id"] for row in rows),
                "conflict_type": "same_key_different_value",
                "resolution": "preserved_all_rows; calculation selects explicit selection_status=selected basis",
            })
    missingness = []
    for row in panel:
        if row["metric_status"] != "reported" or row["value"] == "":
            missingness.append({
                "observation_id": row["observation_id"],
                "entity": row["entity"],
                "reporting_scope": row["reporting_scope"],
                "segment": row["segment"],
                "fiscal_year": row["fiscal_year"],
                "metric": row["metric"],
                "metric_status": row["metric_status"],
                "selection_status": row["selection_status"],
                "reason": row["caveat"] or "value unavailable",
            })
    return {"panel": panel, "conflicts": conflicts, "missingness": missingness}


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def build_dataset() -> dict:
    raw_rows = all_observations()
    result = build_panel(raw_rows)
    for directory in [RAW_DIR, CLEAN_DIR, SOURCE_DIR, LOG_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    write_jsonl(RAW_DIR / "financial_observations_raw.jsonl", raw_rows)
    write_csv(CLEAN_DIR / "financial_panel.csv", FIELDNAMES, result["panel"])
    write_csv(SOURCE_DIR / "source_registry.csv", SOURCE_FIELDS, SOURCES)
    write_csv(CLEAN_DIR / "financial_scope_matrix.csv", SCOPE_FIELDS, SCOPE_MATRIX)
    write_csv(LOG_DIR / "conflicts.csv", [
        "conflict_key", "entity", "reporting_scope", "segment", "fiscal_year", "period", "metric",
        "unit", "currency", "reported_or_constant_currency", "values", "observation_ids", "conflict_type", "resolution"
    ], result["conflicts"])
    write_csv(LOG_DIR / "missingness.csv", [
        "observation_id", "entity", "reporting_scope", "segment", "fiscal_year", "metric", "metric_status", "selection_status", "reason"
    ], result["missingness"])
    profile = []
    for entity in sorted({row["entity"] for row in result["panel"]}):
        entity_rows = [row for row in result["panel"] if row["entity"] == entity]
        profile.append({
            "entity": entity,
            "rows": len(entity_rows),
            "numeric_rows": sum(row["value"] != "" and row["metric_status"] == "reported" for row in entity_rows),
            "unavailable_rows": sum(row["metric_status"] != "reported" for row in entity_rows),
            "fiscal_years": ";".join(sorted({row["fiscal_year"] for row in entity_rows})),
            "scopes": ";".join(sorted({row["reporting_scope"] for row in entity_rows})),
        })
    write_csv(LOG_DIR / "data_profile.csv", ["entity", "rows", "numeric_rows", "unavailable_rows", "fiscal_years", "scopes"], profile)
    summary = {
        "research_as_of": RESEARCH_AS_OF,
        "raw_observations": len(raw_rows),
        "clean_panel_rows": len(result["panel"]),
        "numeric_reported_rows": sum(row["value"] != "" and row["metric_status"] == "reported" for row in result["panel"]),
        "conflict_groups": len(result["conflicts"]),
        "missingness_rows": len(result["missingness"]),
        "source_count": len(SOURCES),
        "scope_matrix_rows": len(SCOPE_MATRIX),
        "conflict_policy": "no silent overwrite; all observations are retained and calculation basis is explicit",
    }
    (LOG_DIR / "run_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LOG_DIR / "BUILD_LOG.md").write_text(
        "# Financial Dataset Build Log\n\n"
        f"- Research as of: `{RESEARCH_AS_OF}`\n"
        f"- Raw observations: `{len(raw_rows)}`\n"
        f"- Clean panel rows: `{len(result['panel'])}`\n"
        f"- Numeric reported rows: `{summary['numeric_reported_rows']}`\n"
        f"- Conflict groups preserved: `{len(result['conflicts'])}`\n"
        f"- Missingness / unavailable rows: `{len(result['missingness'])}`\n\n"
        "The build is deterministic, retains source metadata, preserves original and restated Chanel comparatives, and does not estimate unavailable metrics.\n",
        encoding="utf-8",
    )
    return summary


if __name__ == "__main__":
    result = build_dataset()
    print(json.dumps(result, ensure_ascii=False, indent=2))
