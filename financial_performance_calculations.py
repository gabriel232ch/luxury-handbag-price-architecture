from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FINANCIAL_ROOT = ROOT / "financial_business_performance"
PANEL_PATH = FINANCIAL_ROOT / "clean" / "financial_panel.csv"
CALC_DIR = FINANCIAL_ROOT / "calculations"


def to_float(value):
    if value is None or str(value).strip() == "":
        return None
    try:
        number = float(str(value).replace(",", ""))
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def margin(profit, revenue):
    return ratio(profit, revenue)


def ratio(numerator, denominator):
    if numerator is None or denominator in (None, 0):
        return None
    return float(numerator) / float(denominator) * 100.0


def pct_change(prior, current):
    if prior in (None, 0) or current is None:
        return None
    return (float(current) - float(prior)) / float(prior) * 100.0


def index_series(rows, value_field, base_year=2020):
    base = None
    for row in rows:
        if str(row.get("fiscal_year")) == str(base_year):
            base = to_float(row.get(value_field))
            break
    result = []
    for row in rows:
        value = to_float(row.get(value_field))
        copy = dict(row)
        copy["index_value"] = None if base in (None, 0) or value is None else round(value / base * 100.0, 1)
        result.append(copy)
    return result


def read_panel():
    with PANEL_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def selected_series(panel, entity, segment, metric, years=range(2017, 2026)):
    result = {}
    for row in panel:
        if (
            row["entity"] == entity
            and row["segment"] == segment
            and row["metric"] == metric
            and row["selection_status"] == "selected"
            and row["metric_status"] == "reported"
            and row["value"] != ""
        ):
            year = row["fiscal_year"]
            if year.isdigit() and int(year) in years:
                if year in result and result[year]["value"] != row["value"]:
                    raise ValueError(f"duplicate selected observations with different values: {entity}|{segment}|{metric}|{year}")
                result[year] = row
    return {year: result.get(str(year)) for year in years}


def numeric_series(panel, entity, segment, metric, years=range(2017, 2026)):
    return {str(year): to_float(row["value"]) if row else None for year, row in selected_series(panel, entity, segment, metric, years).items()}


def source_ids_for_year(panel, entity, segment, year):
    return ";".join(sorted({
        row["source_id"]
        for row in panel
        if row["entity"] == entity
        and row["segment"] == segment
        and row["fiscal_year"] == str(year)
        and row["selection_status"] == "selected"
        and row["metric_status"] == "reported"
    }))


def combine_source_ids(*source_lists):
    return ";".join(sorted({source_id for source_list in source_lists for source_id in source_list.split(";") if source_id}))


def round_or_none(value, digits=1):
    return None if value is None else round(float(value), digits)


def build_chanel_calculations(panel):
    years = list(range(2017, 2026))
    fields = {
        metric: numeric_series(panel, "Chanel", "", metric, years)
        for metric in [
            "revenue",
            "comparable_growth",
            "reported_growth",
            "operating_profit",
            "free_cash_flow",
            "capex",
            "brand_support_investment",
            "employees",
        ]
    }
    rows = []
    for index, year in enumerate(years):
        key = str(year)
        prior_key = str(years[index - 1]) if index else None
        revenue = fields["revenue"][key]
        op_profit = fields["operating_profit"][key]
        fcf = fields["free_cash_flow"][key]
        capex = fields["capex"][key]
        brand_support = fields["brand_support_investment"][key]
        row = {
            "fiscal_year": key,
            "revenue_usd_m": revenue,
            "reported_growth_pct": fields["reported_growth"][key],
            "comparable_growth_pct": fields["comparable_growth"][key],
            "calculated_revenue_change_pct": round_or_none(pct_change(fields["revenue"][prior_key], revenue) if prior_key else None),
            "operating_profit_usd_m": op_profit,
            "operating_margin_pct": round_or_none(margin(op_profit, revenue)),
            "operating_profit_change_pct": round_or_none(pct_change(fields["operating_profit"][prior_key], op_profit) if prior_key else None),
            "free_cash_flow_usd_m": fcf,
            "fcf_margin_pct": round_or_none(margin(fcf, revenue)),
            "free_cash_flow_change_pct": round_or_none(pct_change(fields["free_cash_flow"][prior_key], fcf) if prior_key else None),
            "capex_usd_m": capex,
            "capex_revenue_pct": round_or_none(ratio(capex, revenue)),
            "capex_change_pct": round_or_none(pct_change(fields["capex"][prior_key], capex) if prior_key else None),
            "brand_support_investment_usd_m": brand_support,
            "brand_support_revenue_pct": round_or_none(ratio(brand_support, revenue)),
            "brand_support_change_pct": round_or_none(pct_change(fields["brand_support_investment"][prior_key], brand_support) if prior_key else None),
            "employees": fields["employees"][key],
            "performance_phase": (
                "pandemic_shock" if year == 2020 else
                "rebound_and_expansion" if year in (2021, 2022, 2023) else
                "deterioration_with_record_investment" if year == 2024 else
                "reported_recovery_with_elevated_investment" if year == 2025 else
                "pre_core_window"
            ),
            "source_ids": source_ids_for_year(panel, "Chanel", "", year),
        }
        rows.append(row)
    return rows


def build_chanel_summary(chanel_rows):
    def value(year, field):
        row = next((row for row in chanel_rows if row["fiscal_year"] == str(year)), None)
        return row.get(field) if row else None

    revenue_2020 = to_float(value(2020, "revenue_usd_m"))
    revenue_2025 = to_float(value(2025, "revenue_usd_m"))
    op_margin_2020 = to_float(value(2020, "operating_margin_pct"))
    op_margin_2025 = to_float(value(2025, "operating_margin_pct"))
    summary = [
        {"metric": "revenue_cagr", "window": "2020-2025", "value": round_or_none(((revenue_2025 / revenue_2020) ** (1 / 5) - 1) * 100 if revenue_2020 and revenue_2025 else None), "unit": "percent", "calculation_note": "Nominal USD revenue CAGR from selected official company figures; not a constant-currency CAGR."},
        {"metric": "operating_margin_change", "window": "2020-2025", "value": round_or_none(op_margin_2025 - op_margin_2020 if op_margin_2020 is not None and op_margin_2025 is not None else None), "unit": "percentage_points", "calculation_note": "Derived operating profit / revenue margin change; 2020 uses FY2021 restated KPI basis."},
        {"metric": "peak_operating_margin", "window": "2017-2025", "value": max((to_float(row["operating_margin_pct"]) for row in chanel_rows if row["operating_margin_pct"] is not None), default=None), "unit": "percent", "calculation_note": "Derived from reported consolidated company revenue and operating profit."},
        {"metric": "peak_operating_margin_year", "window": "2017-2025", "value": max((row for row in chanel_rows if row["operating_margin_pct"] is not None), key=lambda row: to_float(row["operating_margin_pct"]))["fiscal_year"], "unit": "fiscal_year", "calculation_note": "Derived from reported consolidated company revenue and operating profit."},
        {"metric": "2024_revenue_decline", "window": "2023-2024", "value": value(2024, "comparable_growth_pct"), "unit": "percent", "calculation_note": "Company-reported comparable constant-currency growth; not calculated from rounded / nominal revenue."},
        {"metric": "2025_fcf_change", "window": "2024-2025", "value": value(2025, "free_cash_flow_change_pct"), "unit": "percent", "calculation_note": "Derived from selected official FCF values."},
    ]
    return summary


def build_hermes_benchmark(panel):
    years = list(range(2020, 2026))
    metrics = {
        metric: numeric_series(panel, "Hermès", "", metric, years)
        for metric in ["revenue", "reported_growth", "comparable_growth", "operating_profit", "reported_operating_margin", "operating_investments", "adjusted_free_cash_flow"]
    }
    leather = {
        metric: numeric_series(panel, "Hermès", "Leather Goods & Saddlery", metric, years)
        for metric in ["revenue", "reported_growth", "comparable_growth"]
    }
    rows = []
    for year in years:
        key = str(year)
        group_revenue = metrics["revenue"][key]
        leather_revenue = leather["revenue"][key]
        rows.append({
            "fiscal_year": key,
            "group_revenue_eur_m": group_revenue,
            "group_reported_growth_pct": metrics["reported_growth"][key],
            "group_constant_currency_growth_pct": metrics["comparable_growth"][key],
            "group_recurring_operating_income_eur_m": metrics["operating_profit"][key],
            "group_recurring_operating_margin_pct": metrics["reported_operating_margin"][key],
            "group_recurring_operating_margin_pct_calculated_from_rounded_figures": round_or_none(margin(metrics["operating_profit"][key], group_revenue)),
            "operating_investments_eur_m": metrics["operating_investments"][key],
            "operating_investments_revenue_pct": round_or_none(ratio(metrics["operating_investments"][key], group_revenue)),
            "adjusted_free_cash_flow_eur_m": metrics["adjusted_free_cash_flow"][key],
            "leather_goods_saddlery_revenue_eur_m": leather_revenue,
            "leather_goods_saddlery_share_pct": round_or_none(ratio(leather_revenue, group_revenue)),
            "leather_goods_saddlery_reported_growth_pct": leather["reported_growth"][key],
            "leather_goods_saddlery_constant_currency_growth_pct": leather["comparable_growth"][key],
            "source_ids": combine_source_ids(source_ids_for_year(panel, "Hermès", "", year), source_ids_for_year(panel, "Hermès", "Leather Goods & Saddlery", year)),
        })
    return rows


def build_lvmh_benchmark(panel):
    years = list(range(2020, 2026))
    group_revenue = numeric_series(panel, "LVMH", "", "revenue", years)
    segment = {
        metric: numeric_series(panel, "LVMH", "Fashion & Leather Goods", metric, years)
        for metric in ["revenue", "reported_growth", "organic_growth", "operating_profit"]
    }
    rows = []
    for year in years:
        key = str(year)
        rows.append({
            "fiscal_year": key,
            "group_revenue_eur_m": group_revenue[key],
            "fashion_leather_goods_revenue_eur_m": segment["revenue"][key],
            "fashion_leather_goods_share_pct": round_or_none(ratio(segment["revenue"][key], group_revenue[key])),
            "fashion_leather_goods_reported_growth_pct": segment["reported_growth"][key],
            "fashion_leather_goods_organic_growth_pct": segment["organic_growth"][key],
            "fashion_leather_goods_recurring_operating_profit_eur_m": segment["operating_profit"][key],
            "fashion_leather_goods_recurring_operating_margin_pct": round_or_none(margin(segment["operating_profit"][key], segment["revenue"][key])),
            "source_ids": combine_source_ids(source_ids_for_year(panel, "LVMH", "", year), source_ids_for_year(panel, "LVMH", "Fashion & Leather Goods", year)),
        })
    return rows


def build_comparative_trends(chanel_rows, hermes_rows, lvmh_rows):
    series = [
        ("Chanel consolidated revenue", "USD", chanel_rows, "revenue_usd_m"),
        ("Hermès group revenue", "EUR", hermes_rows, "group_revenue_eur_m"),
        ("Hermès Leather Goods & Saddlery revenue", "EUR", hermes_rows, "leather_goods_saddlery_revenue_eur_m"),
        ("LVMH Fashion & Leather Goods revenue", "EUR", lvmh_rows, "fashion_leather_goods_revenue_eur_m"),
    ]
    rows = []
    for label, currency, source_rows, field in series:
        indexed = index_series(source_rows, field, base_year=2020)
        values = [(row["fiscal_year"], to_float(row.get(field))) for row in source_rows if to_float(row.get(field)) is not None]
        peak_year, peak_value = max(values, key=lambda pair: pair[1]) if values else (None, None)
        trough_year, trough_value = min(values, key=lambda pair: pair[1]) if values else (None, None)
        end_value = to_float(next((row.get(field) for row in source_rows if row["fiscal_year"] == "2025"), None))
        rows.append({
            "series": label,
            "currency": currency,
            "base_year": "2020",
            "end_year": "2025",
            "index_2020": next((row["index_value"] for row in indexed if row["fiscal_year"] == "2020"), None),
            "index_2025": next((row["index_value"] for row in indexed if row["fiscal_year"] == "2025"), None),
            "nominal_change_2020_2025_pct": round_or_none(pct_change(to_float(next((row.get(field) for row in source_rows if row["fiscal_year"] == "2020"), None)), end_value)),
            "peak_year": peak_year,
            "trough_year": trough_year,
            "direction": "up" if end_value and values and end_value > values[0][1] else "down" if end_value and values and end_value < values[0][1] else "mixed_or_unavailable",
            "comparability_note": "Index is within-series only; currencies and reporting grains are not pooled or ranked.",
        })
    return rows


CALCULATION_REGISTRY = [
    {"calculation_id": "CALC-01", "output": "Chanel operating margin", "formula": "operating_profit / revenue * 100", "unit": "percent", "type": "derived", "caveat": "Consolidated company; operating profit label is company-reported."},
    {"calculation_id": "CALC-02", "output": "Chanel FCF margin", "formula": "free_cash_flow / revenue * 100", "unit": "percent", "type": "derived", "caveat": "Company-disclosed FCF definition; not comparable as a universal accounting metric across companies."},
    {"calculation_id": "CALC-03", "output": "Chanel capex intensity", "formula": "capex / revenue * 100", "unit": "percent", "type": "derived", "caveat": "Company capital investment; company-wide, not handbag-only."},
    {"calculation_id": "CALC-04", "output": "Chanel brand-support intensity", "formula": "brand_support_investment / revenue * 100", "unit": "percent", "type": "derived", "caveat": "Brand-support investment includes disclosed client-support activities and is not a handbag marketing expense."},
    {"calculation_id": "CALC-05", "output": "Hermès leather-goods share", "formula": "Leather Goods & Saddlery revenue / group revenue * 100", "unit": "percent", "type": "derived", "caveat": "Métier includes bags, travel items, small leather goods, saddlery and equestrian products."},
    {"calculation_id": "CALC-06", "output": "LVMH Fashion & Leather Goods margin", "formula": "segment recurring operating profit / segment revenue * 100", "unit": "percent", "type": "derived", "caveat": "Multi-brand segment; not Louis Vuitton or Dior standalone."},
    {"calculation_id": "CALC-07", "output": "Indexed evolution", "formula": "value / value_in_2020 * 100", "unit": "index", "type": "derived", "caveat": "Within-series only; no cross-currency or cross-grain nominal ranking."},
    {"calculation_id": "CALC-08", "output": "Hermès group recurring operating margin", "formula": "use official displayed margin; retain derived check from rounded profit / revenue", "unit": "percent", "type": "reported_plus_check", "caveat": "Official displayed margin is preferred because source revenue and profit may be rounded; Leather Goods & Saddlery segment margin is unavailable."},
]


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if value is None else value for key, value in row.items()})


def calculate_all(panel=None):
    panel = read_panel() if panel is None else panel
    CALC_DIR.mkdir(parents=True, exist_ok=True)
    chanel = build_chanel_calculations(panel)
    hermes = build_hermes_benchmark(panel)
    lvmh = build_lvmh_benchmark(panel)
    comparative = build_comparative_trends(chanel, hermes, lvmh)
    write_csv(CALC_DIR / "chanel_annual_performance.csv", chanel)
    write_csv(CALC_DIR / "chanel_summary.csv", build_chanel_summary(chanel))
    write_csv(CALC_DIR / "hermes_benchmark.csv", hermes)
    write_csv(CALC_DIR / "lvmh_fashion_leather_goods.csv", lvmh)
    write_csv(CALC_DIR / "comparative_trends.csv", comparative)
    write_csv(CALC_DIR / "calculation_registry.csv", CALCULATION_REGISTRY)
    summary = {
        "chanel_years": len(chanel),
        "hermes_years": len(hermes),
        "lvmh_years": len(lvmh),
        "comparative_series": len(comparative),
        "currency_policy": "USD and EUR retained; index / growth / margin preferred over nominal cross-currency ranking",
        "causal_policy": "temporal co-movement is not causal evidence",
    }
    (CALC_DIR / "run_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(calculate_all(), ensure_ascii=False, indent=2))
