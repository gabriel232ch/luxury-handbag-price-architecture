#!/usr/bin/env python3
"""Release-gate validation for the Phase 2 public evidence chain."""

from __future__ import annotations

import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fail_if(condition: bool, message: str, failures: list[str]) -> None:
    if condition:
        failures.append(message)


def numeric_equal(value: object, expected: float) -> bool:
    try:
        return abs(float(value) - expected) < 1e-9
    except (TypeError, ValueError):
        return False


def main() -> dict[str, object]:
    failures: list[str] = []
    financial_panel = read_csv(ROOT / "financial_business_performance" / "clean" / "financial_panel.csv")
    sources = read_csv(ROOT / "financial_business_performance" / "sources" / "source_registry.csv")
    architecture = read_csv(ROOT / "financial_business_performance" / "calculations" / "architecture_summary.csv")
    chanel = read_csv(ROOT / "financial_business_performance" / "calculations" / "chanel_annual_performance.csv")
    hermes = read_csv(ROOT / "financial_business_performance" / "calculations" / "hermes_benchmark.csv")
    lvmh = read_csv(ROOT / "financial_business_performance" / "calculations" / "lvmh_fashion_leather_goods.csv")
    current_chanel = read_csv(ROOT / "chanel_fr_us_handbags_current" / "clean_data.csv")
    current_competitors = read_csv(ROOT / "luxury_competitor_pricing_current" / "clean" / "competitor_pricing_clean.csv")
    historical = read_csv(ROOT / "luxury_historical_pricing" / "clean" / "historical_pricing_clean.csv")

    required_panel_fields = {
        "entity", "reporting_scope", "fiscal_year", "period", "metric", "value", "unit", "currency",
        "reported_or_constant_currency", "source_id", "source_url", "publication_date", "page_or_section",
        "confidence", "caveat", "selection_status", "metric_status",
    }
    fail_if(not required_panel_fields.issubset(financial_panel[0]), "financial panel schema is incomplete", failures)
    fail_if(any(row["metric_status"] == "reported" and not row["source_url"] for row in financial_panel), "reported financial row lacks source_url", failures)
    fail_if(len(sources) != 21 or any(not row["source_url"] for row in sources), "source registry coverage / URL check failed", failures)
    fail_if(any(row["entity"] in {"Louis Vuitton", "Dior"} and row["metric_status"] == "reported" for row in financial_panel), "brand-level LV / Dior reported financial row found", failures)

    fail_if(len(current_chanel) + len(current_competitors) != 161, "current accepted count is not 161", failures)
    current_numeric = sum(bool(row.get("price", "").strip()) for row in current_chanel) + sum(row.get("price_status") == "numeric" for row in current_competitors)
    fail_if(current_numeric != 147, "current numeric count is not 147", failures)
    fail_if(len(historical) != 77 or sum(bool(row.get("price", "").strip()) for row in historical) != 76, "historical count reconciliation failed", failures)

    chanel_2025 = next((row for row in chanel if row["fiscal_year"] == "2025"), {})
    hermes_2025 = next((row for row in hermes if row["fiscal_year"] == "2025"), {})
    lvmh_2025 = next((row for row in lvmh if row["fiscal_year"] == "2025"), {})
    fail_if(not numeric_equal(chanel_2025.get("revenue_usd_m"), 19269), "Chanel 2025 revenue reconciliation failed", failures)
    fail_if(not numeric_equal(hermes_2025.get("leather_goods_saddlery_revenue_eur_m"), 7070), "Hermes 2025 leather revenue reconciliation failed", failures)
    fail_if(not numeric_equal(lvmh_2025.get("fashion_leather_goods_organic_growth_pct"), -5.0), "LVMH 2025 organic growth reconciliation failed", failures)
    fail_if({row["market"] for row in architecture} != {"FR", "US"}, "Chanel architecture market split missing", failures)
    fail_if(next((row["core_to_icon_step"] for row in architecture if row["market"] == "FR"), "") != "3300", "Chanel France gap reconciliation failed", failures)
    fail_if(next((row["core_to_icon_step"] for row in architecture if row["market"] == "US"), "") != "3600", "Chanel US gap reconciliation failed", failures)

    report_text = (ROOT / "FINAL_LUXURY_HANDBAG_PRICING_STRATEGY_CN.md").read_text(encoding="utf-8").lower()
    prohibited_english = ["price caused revenue", "price increase resulted in", "pricing drove revenue", "caused growth"]
    fail_if(any(phrase in report_text for phrase in prohibited_english), "causal shortcut found in final report", failures)
    fail_if("不是因果证据" not in report_text or "因果结论" not in report_text, "causal boundary language missing", failures)

    chart_files = [ROOT / "final_report_assets" / f"{number:02d}_{name}.svg" for number, name in [
        (1, "four_brand_current_architecture"), (2, "price_band_battleground"), (3, "chanel_current_ladder"),
        (4, "chanel_historical_icon_access"), (5, "four_brand_archetype_matrix"), (6, "chanel_financial_performance"),
        (7, "luxury_benchmark_trajectory"), (8, "strategic_tension_matrix"),
    ]]
    for chart in chart_files:
        try:
            ET.parse(chart)
        except (ET.ParseError, FileNotFoundError) as exc:
            failures.append(f"chart XML check failed: {chart.name}: {exc}")
    fail_if(any("price" in chart.read_text(encoding="utf-8").lower() and "revenue" in chart.read_text(encoding="utf-8").lower() and "dual" not in chart.read_text(encoding="utf-8").lower() for chart in chart_files if chart.exists()), "chart text review needs manual dual-axis inspection", failures)

    result = {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "current_observations": len(current_chanel) + len(current_competitors),
        "current_numeric_observations": current_numeric,
        "historical_observations": len(historical),
        "financial_panel_rows": len(financial_panel),
        "official_source_rows": len(sources),
        "charts_checked": len(chart_files),
        "claim_reconciliation": {
            "chanel_2025_revenue_usd_m": chanel_2025.get("revenue_usd_m"),
            "hermes_2025_leather_revenue_eur_m": hermes_2025.get("leather_goods_saddlery_revenue_eur_m"),
            "lvmh_2025_flg_organic_growth_pct": lvmh_2025.get("fashion_leather_goods_organic_growth_pct"),
        },
    }
    output = ROOT / "financial_business_performance" / "logs" / "phase2_validation.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    result = main()
    raise SystemExit(0 if result["status"] == "PASS" else 1)
