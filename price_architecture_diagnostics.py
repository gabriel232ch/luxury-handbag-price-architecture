#!/usr/bin/env python3
"""Reproducible diagnostics for the observed current handbag price ladder.

The calculations describe the supplied official list-price snapshot. They do
not infer affordability, demand, willingness to pay, conversion, elasticity,
or profitability. Missing and unresolved prices remain outside numeric
distribution calculations and are reported as a visibility limitation.
"""

from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CHANEL_FILE = ROOT / "chanel_fr_us_handbags_current" / "clean_data.csv"
COMPETITOR_FILE = ROOT / "luxury_competitor_pricing_current" / "clean" / "competitor_pricing_clean.csv"
OUT = ROOT / "financial_business_performance" / "calculations"
OUT.mkdir(parents=True, exist_ok=True)


# These are the already-used market-specific analytical price bands, collapsed
# to the four reporting tiers requested for Phase 2. They are observed-price
# bands, not affordability or willingness-to-pay thresholds.
TIER_RULES = {
    "FR": [(0, 2_999, "entry"), (3_000, 4_999, "core"), (5_000, 9_999, "premium"), (10_000, math.inf, "icon")],
    "US": [(0, 3_999, "entry"), (4_000, 5_999, "core"), (6_000, 10_999, "premium"), (11_000, math.inf, "icon")],
}


def as_float(value: object) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(str(value).replace(",", "").strip())
    except ValueError:
        return None


def fmt(value: float | None) -> str:
    if value is None:
        return ""
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.2f}"


def pct(value: float | None) -> str:
    return "" if value is None else f"{value:.1f}%"


def market_code(value: str) -> str:
    return {"France": "FR", "United States": "US"}.get(value, value)


def adjacent_steps(values: list[float]) -> list[dict[str, float | int]]:
    """Return sorted adjacent SKU price steps, retaining zero steps."""
    ordered = sorted(values)
    result = []
    for rank, (lower, upper) in enumerate(zip(ordered, ordered[1:]), start=1):
        result.append({
            "lower_rank": rank,
            "upper_rank": rank + 1,
            "lower_price": lower,
            "upper_price": upper,
            "absolute_step": upper - lower,
            "relative_step_pct": (upper / lower - 1) * 100 if lower else None,
        })
    return result


def family_step_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Calculate adjacent family-median steps after sorting by median price."""
    ordered = sorted(rows, key=lambda row: (float(row["median"]), str(row["product_family"])))
    result = []
    for rank, (lower, upper) in enumerate(zip(ordered, ordered[1:]), start=1):
        lower_value = float(lower["median"])
        upper_value = float(upper["median"])
        result.append({
            "step_rank": rank,
            "lower_family": lower["product_family"],
            "upper_family": upper["product_family"],
            "lower_median": lower_value,
            "upper_median": upper_value,
            "absolute_step": upper_value - lower_value,
            "relative_step_pct": (upper_value / lower_value - 1) * 100 if lower_value else None,
        })
    return result


def summarize_visibility(rows: list[dict[str, object]]) -> dict[str, object]:
    numeric_count = sum(as_float(row.get("price")) is not None for row in rows)
    total = len(rows)
    return {
        "total_observations": total,
        "numeric_observations": numeric_count,
        "non_numeric_or_por_observations": total - numeric_count,
        "numeric_share_pct": numeric_count / total * 100 if total else None,
    }


def tier_for_price(market: str, price: float) -> str:
    for lower, upper, tier in TIER_RULES[market]:
        if lower <= price <= upper:
            return tier
    return "unclassified"


def read_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with CHANEL_FILE.open(newline="", encoding="utf-8") as handle:
        for raw in csv.DictReader(handle):
            price = as_float(raw.get("price"))
            rows.append({
                "brand": "CHANEL",
                "market": market_code(raw.get("market", "")),
                "currency": raw.get("currency") or ("EUR" if market_code(raw.get("market", "")) == "FR" else "USD"),
                "product_family": raw.get("product_family", ""),
                "reference": raw.get("sku_or_reference", ""),
                "price": price,
                "visibility_class": "numeric" if price is not None else "non_numeric_or_por",
                "availability": raw.get("availability", ""),
                "source_url": raw.get("source_url", ""),
            })
    with COMPETITOR_FILE.open(newline="", encoding="utf-8") as handle:
        for raw in csv.DictReader(handle):
            price = as_float(raw.get("price"))
            rows.append({
                "brand": raw.get("brand", ""),
                "market": raw.get("market", ""),
                "currency": raw.get("currency", ""),
                "product_family": raw.get("product_family", ""),
                "reference": raw.get("official_sku_or_reference", ""),
                "price": price if raw.get("price_status") == "numeric" else None,
                "visibility_class": "numeric" if raw.get("price_status") == "numeric" and price is not None else "non_numeric_or_por",
                "availability": raw.get("availability", ""),
                "source_url": raw.get("source_url", ""),
            })
    return rows


def write_csv(name: str, rows: list[dict[str, object]], fields: list[str] | None = None) -> None:
    path = OUT / name
    fields = fields or (list(rows[0]) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = read_rows()
    brands = ["CHANEL", "Hermès", "Louis Vuitton", "Dior"]
    markets = ["FR", "US"]

    visibility_rows = []
    for brand in brands:
        for market in markets:
            subset = [row for row in rows if row["brand"] == brand and row["market"] == market]
            summary = summarize_visibility(subset)
            summary.update({
                "brand": brand,
                "market": market,
                "currency": "EUR" if market == "FR" else "USD",
                "visibility_definition": "numeric displayed list price vs non-numeric/POR or unresolved observation",
                "caveat": "Non-numeric observations are excluded from price distributions; unresolved does not prove formal POR.",
            })
            visibility_rows.append(summary)
    write_csv("architecture_visibility.csv", visibility_rows, [
        "brand", "market", "currency", "total_observations", "numeric_observations",
        "non_numeric_or_por_observations", "numeric_share_pct", "visibility_definition", "caveat",
    ])

    step_rows = []
    for brand in brands:
        for market in markets:
            subset = [row for row in rows if row["brand"] == brand and row["market"] == market and row["price"] is not None]
            values = [float(row["price"]) for row in subset]
            for step in adjacent_steps(values):
                step_rows.append({
                    "brand": brand, "market": market, "currency": "EUR" if market == "FR" else "USD",
                    **{key: fmt(value) if isinstance(value, float) and value is not None else value for key, value in step.items()},
                    "step_definition": "adjacent sorted numeric SKU observations; duplicate prices retained",
                })
    write_csv("sku_price_steps.csv", step_rows, [
        "brand", "market", "currency", "lower_rank", "upper_rank", "lower_price", "upper_price",
        "absolute_step", "relative_step_pct", "step_definition",
    ])

    family_rows = []
    for brand in brands:
        for market in markets:
            grouped: dict[str, list[float]] = defaultdict(list)
            for row in rows:
                if row["brand"] == brand and row["market"] == market and row["price"] is not None and row["product_family"]:
                    grouped[str(row["product_family"])].append(float(row["price"]))
            medians = [{"product_family": family, "median": sorted(values)[(len(values) - 1) // 2] if len(values) % 2 else (sorted(values)[len(values) // 2 - 1] + sorted(values)[len(values) // 2]) / 2} for family, values in grouped.items()]
            for step in family_step_rows(medians):
                family_rows.append({
                    "brand": brand, "market": market, "currency": "EUR" if market == "FR" else "USD",
                    **{key: fmt(value) if isinstance(value, float) else value for key, value in step.items()},
                    "step_definition": "adjacent product-family medians sorted by observed numeric median",
                })
    write_csv("family_step_up.csv", family_rows, [
        "brand", "market", "currency", "step_rank", "lower_family", "upper_family", "lower_median",
        "upper_median", "absolute_step", "relative_step_pct", "step_definition",
    ])

    tier_rows = []
    for brand in brands:
        for market in markets:
            subset = [row for row in rows if row["brand"] == brand and row["market"] == market]
            numeric_rows = [row for row in subset if row["price"] is not None]
            for tier in ["entry", "core", "premium", "icon"]:
                values = [float(row["price"]) for row in numeric_rows if tier_for_price(market, float(row["price"])) == tier]
                tier_rows.append({
                    "brand": brand, "market": market, "currency": "EUR" if market == "FR" else "USD",
                    "tier": tier, "numeric_skus": len(values),
                    "share_of_brand_numeric_pct": pct(len(values) / len(numeric_rows) * 100) if numeric_rows else "",
                    "minimum": fmt(min(values) if values else None), "maximum": fmt(max(values) if values else None),
                    "tier_definition": "collapsed from the existing market-specific observed-price bands; not affordability bands",
                })
    write_csv("tier_density.csv", tier_rows, [
        "brand", "market", "currency", "tier", "numeric_skus", "share_of_brand_numeric_pct",
        "minimum", "maximum", "tier_definition",
    ])

    architecture_rows = []
    for market in markets:
        subset = [row for row in rows if row["brand"] == "CHANEL" and row["market"] == market]
        numeric_rows = [row for row in subset if row["price"] is not None]
        values = sorted(float(row["price"]) for row in numeric_rows)
        steps = adjacent_steps(values)
        premium_values = [value for value in values if tier_for_price(market, value) == "premium"]
        icon_values = [value for value in values if tier_for_price(market, value) == "icon"]
        entry_values = [value for value in values if tier_for_price(market, value) == "entry"]
        core_values = [value for value in values if tier_for_price(market, value) == "core"]
        largest = max(steps, key=lambda row: row["absolute_step"]) if steps else {}
        family_steps = [row for row in family_rows if row["brand"] == "CHANEL" and row["market"] == market]
        family_largest = max(family_steps, key=lambda row: float(row["absolute_step"])) if family_steps else {}
        architecture_rows.append({
            "brand": "CHANEL", "market": market, "currency": "EUR" if market == "FR" else "USD",
            "accepted_observations": len(subset), "numeric_skus": len(numeric_rows),
            "non_numeric_or_por": len(subset) - len(numeric_rows),
            "numeric_share_pct": pct(len(numeric_rows) / len(subset) * 100) if subset else "",
            "lowest_numeric_price": fmt(min(values) if values else None),
            "highest_numeric_price": fmt(max(values) if values else None),
            "largest_adjacent_sku_gap": fmt(float(largest.get("absolute_step"))) if largest else "",
            "largest_adjacent_gap_from": fmt(float(largest.get("lower_price"))) if largest else "",
            "largest_adjacent_gap_to": fmt(float(largest.get("upper_price"))) if largest else "",
            "entry_to_core_step": "" if not entry_values or not core_values else fmt(min(core_values) - min(entry_values)),
            "entry_to_core_note": "Not estimable from observed snapshot: no numeric entry/lower-tier SKU." if not entry_values else "Lowest observed entry/lower price to lowest observed core price.",
            "core_to_icon_step": fmt(min(icon_values) - max(core_values + premium_values)) if icon_values and (core_values or premium_values) else "",
            "core_to_icon_note": "Lowest observed icon price minus highest observed pre-icon price; visible gap, not a demand barrier.",
            "largest_family_median_gap": fmt(float(family_largest.get("absolute_step"))) if family_largest else "",
            "largest_family_gap_from": family_largest.get("lower_family", ""),
            "largest_family_gap_to": family_largest.get("upper_family", ""),
            "diagnostic_scope": "Chanel official current handbag snapshot; France and United States calculated separately.",
            "interpretation_boundary": "A price gap describes visible list-price spacing only; it does not prove conversion risk, substitution, or demand resilience.",
        })
    write_csv("architecture_summary.csv", architecture_rows)

    registry = [
        {"calculation": "sku_price_steps", "definition": "Adjacent sorted numeric SKU observations, including zero steps for duplicate prices.", "unit": "local currency", "caveat": "Observed sample is not a complete assortment census."},
        {"calculation": "family_step_up", "definition": "Adjacent product-family median prices sorted by observed median.", "unit": "local currency", "caveat": "Family composition and sample counts differ by brand."},
        {"calculation": "tier_density", "definition": "Numeric SKU count and share in collapsed existing market-specific price bands.", "unit": "count / percent", "caveat": "Analytical tiers are not affordability or willingness-to-pay tiers."},
        {"calculation": "entry_to_core_step", "definition": "Lowest observed core numeric price minus lowest observed entry/lower numeric price.", "unit": "local currency", "caveat": "Blank when the snapshot contains no numeric entry/lower-tier SKU."},
        {"calculation": "core_to_icon_step", "definition": "Lowest observed icon price minus highest observed pre-icon numeric price.", "unit": "local currency", "caveat": "Visible list-price gap; not evidence of a demand barrier."},
        {"calculation": "numeric_vs_non_numeric", "definition": "Displayed numeric price versus non-numeric/POR or unresolved observation.", "unit": "count / percent", "caveat": "Unresolved does not prove formal price upon request."},
    ]
    write_csv("price_architecture_calculation_registry.csv", registry)

    with (OUT / "price_architecture_run_summary.json").open("w", encoding="utf-8") as handle:
        json.dump({
            "accepted_observations": len(rows),
            "numeric_observations": sum(row["price"] is not None for row in rows),
            "outputs": ["architecture_summary.csv", "architecture_visibility.csv", "sku_price_steps.csv", "family_step_up.csv", "tier_density.csv", "price_architecture_calculation_registry.csv"],
            "price_window": "2026 current snapshot as observed 2026-08-15",
        }, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
