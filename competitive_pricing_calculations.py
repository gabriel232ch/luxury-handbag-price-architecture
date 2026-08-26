#!/usr/bin/env python3
"""Reproducible descriptive calculations for the current competitive handbag price round.

This script only calculates observable list-price metrics from the supplied official
current-price extracts. It does not estimate demand, willingness to pay, profit,
elasticity, or an optimal price.
"""

from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "competitive_pricing_calculations"
OUT.mkdir(exist_ok=True)

CHANEL_FILE = ROOT / "chanel_fr_us_handbags_current" / "clean_data.csv"
COMPETITOR_FILE = ROOT / "luxury_competitor_pricing_current" / "clean" / "competitor_pricing_clean.csv"
MATCHED_FILES = [
    ROOT / "chanel_fr_us_handbags_current" / "matched_skus.csv",
    ROOT / "luxury_competitor_pricing_current" / "clean" / "matched_fr_us_skus.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_float(value: str | None) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(str(value).replace(",", "").strip())
    except ValueError:
        return None


def linear_quantile(values: list[float], p: float) -> float | None:
    """Inclusive linear quantile: position=(n-1)*p, interpolated between points."""
    values = sorted(values)
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    position = (len(values) - 1) * p
    low = math.floor(position)
    high = math.ceil(position)
    if low == high:
        return values[low]
    return values[low] + (values[high] - values[low]) * (position - low)


def fmt(value: float | None) -> str:
    if value is None:
        return ""
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.2f}"


def pct(value: float | None) -> str:
    return "" if value is None else f"{value * 100:.1f}%"


def parse_dimensions(row: dict[str, str]) -> tuple[float | None, float | None, float | None]:
    values = [as_float(row.get(k)) for k in ("width_cm", "height_cm", "depth_cm")]
    if all(v is not None for v in values):
        return values[0], values[1], values[2]
    raw = row.get("dimensions") or row.get("dimensions_raw") or ""
    numbers = [as_float(x) for x in re.findall(r"(?<![A-Za-z])\d+(?:\.\d+)?", raw)]
    numbers = [x for x in numbers if x is not None]
    if len(numbers) >= 3:
        return numbers[0], numbers[1], numbers[2]
    return None, None, None


def material_class(material: str) -> str:
    text = (material or "").lower()
    if any(token in text for token in ("calfskin", "lambskin", "leather", "goat", "togo", "epsom", "swift", "barénia", "barenia", "cowhide", "negonda", "mysore", "agneau", "veau", "cuir")):
        return "leather"
    if any(token in text for token in ("canvas", "tweed", "denim", "raffia", "silk", "textile", "wool", "cotton", "jersey", "fabric", "toile", "crêpe")):
        return "textile_or_mixed"
    if material.strip() == "":
        return "missing"
    return "other_or_unclear"


def bag_type_group(row: dict[str, str]) -> str:
    raw = (row.get("bag_type") or "").lower()
    family = (row.get("product_family") or "").lower()
    if "classic" in family:
        return "flap"
    if "shopping" in family or "bowling" in family:
        return "tote"
    if raw in {"flap_bag", "clutch"}:
        return "flap_or_clutch"
    if raw == "tote" or raw == "bowling":
        return "tote"
    if raw == "crossbody":
        return "crossbody"
    if raw == "shoulder_bag":
        return "shoulder"
    if raw == "top_handle_bag":
        return "top_handle"
    if raw == "backpack":
        return "backpack"
    if raw:
        return raw
    return "unknown"


def size_group(row: dict[str, str], volume: float | None) -> str:
    label = (row.get("size_label") or "").lower()
    if volume is not None:
        if volume <= 3000:
            return "compact"
        if volume <= 8000:
            return "standard"
        return "large"
    if any(token in label for token in ("mini", "nano", "bb", "small", "east_west", "20")):
        return "compact"
    if any(token in label for token in ("medium", "standard", "pm", "25")):
        return "standard"
    if any(token in label for token in ("large", "mm", "30", "gm", "34", "35", "39", "41")):
        return "large"
    family = (row.get("product_family") or "").lower()
    if "mini" in family:
        return "compact"
    return "unknown"


def normalize(row: dict[str, str], source: str) -> dict[str, object]:
    brand = row.get("brand", "").strip()
    market_raw = row.get("market", "").strip()
    market = "FR" if market_raw in {"FR", "France"} else "US" if market_raw in {"US", "United States"} else market_raw
    reference = row.get("official_sku_or_reference") or row.get("sku_or_reference") or ""
    price = as_float(row.get("price"))
    status = row.get("price_status") or ("numeric" if price is not None else "price_upon_request" if brand.upper() == "CHANEL" else "unresolved")
    width, height, depth = parse_dimensions(row)
    volume = width * height * depth if width and height and depth else None
    family = row.get("product_family") or ""
    material = row.get("material") or ""
    supplied_icon = row.get("iconic_or_signature_flag")
    if brand.upper() == "CHANEL":
        if family in {"Classic 11.12", "Small Classic"}:
            signature_class = "icon_inferred"
        elif family in {"Mini Classic", "Shopping Bag", "Bowling Bag"}:
            signature_class = "non_icon_observed"
        else:
            signature_class = "unknown"
    elif supplied_icon and supplied_icon.lower() == "true":
        signature_class = "icon_supplied"
    elif supplied_icon and supplied_icon.lower() == "false":
        signature_class = "non_icon_supplied"
    elif brand in {"Dior", "Louis Vuitton"}:
        # A blank source flag means not flagged, not independently verified
        # as non-iconic. Keep that limitation visible in the ratio label.
        signature_class = "other_unflagged_observed"
    else:
        signature_class = "unknown"
    return {
        "source": source,
        "brand": brand,
        "market": market,
        "currency": row.get("currency") or ("EUR" if market == "FR" else "USD"),
        "reference": reference,
        "product_name": row.get("product_name") or "",
        "product_family": family,
        "subcategory": row.get("subcategory") or "",
        "bag_type_raw": row.get("bag_type") or "",
        "bag_type_group": bag_type_group(row),
        "material": material,
        "material_class": material_class(material),
        "dimensions": row.get("dimensions") or row.get("dimensions_raw") or "",
        "width_cm": width,
        "height_cm": height,
        "depth_cm": depth,
        "volume_cm3": volume,
        "size_group": size_group(row, volume),
        "signature_class": signature_class,
        "price": price,
        "price_status": status,
        "availability": row.get("availability") or "",
        "source_url": row.get("source_url") or "",
        "observed_at": row.get("observed_at") or "",
    }


def numeric(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [r for r in rows if r["price"] is not None and r["price_status"] == "numeric"]


def write_csv(name: str, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path = OUT / name
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(name: str, value: object) -> None:
    with (OUT / name).open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def main() -> None:
    chanel = [normalize(r, "chanel_fr_us_handbags_current/clean_data.csv") for r in read_csv(CHANEL_FILE)]
    competitors = [normalize(r, "luxury_competitor_pricing_current/clean/competitor_pricing_clean.csv") for r in read_csv(COMPETITOR_FILE)]
    rows = chanel + competitors
    brands = ["CHANEL", "Hermès", "Louis Vuitton", "Dior"]

    write_json("calculation_contract.json", {
        "observed_price_definition": "Official localized list price displayed in the supplied current-price extract; not realized price.",
        "quantile_convention": "Inclusive linear interpolation with position=(n-1)*p.",
        "numeric_inclusion": "price is present and price_status=numeric; missing price-upon-request and unresolved observations are excluded from numeric distribution metrics.",
        "market_treatment": "France and United States are calculated separately; no FX, VAT, sales-tax, duty, or landed-cost normalization.",
        "price_band_rule": "Rounded bands selected after inspecting pooled observed numeric price clusters separately by market; they are analytical bands, not affordability bands.",
        "comparable_cell_rule": "Same market, broad bag-type group, dimension-derived size group, and broad material class; only numeric prices; pooled cell median is benchmark=100. These are directional, not global brand indices.",
        "icon_rule": "CHANEL Classic 11.12 and Small Classic are inferred icons; competitor true flags are treated as icon observations and blank flags as other unflagged observations, not verified non-icons; Hermès has no supplied icon flags and is excluded from icon-premium ratios.",
        "source_files": [str(CHANEL_FILE.relative_to(ROOT)), str(COMPETITOR_FILE.relative_to(ROOT))],
    })

    # Full observation universe and analytical sample profile.
    profile = []
    for brand in brands:
        for market in ["FR", "US"]:
            subset = [r for r in rows if r["brand"] == brand and r["market"] == market]
            nums = numeric(subset)
            refs = {r["reference"] for r in subset if r["reference"]}
            families = {r["product_family"] for r in subset if r["product_family"]}
            profile.append({
                "brand": brand,
                "market": market,
                "observations": len(subset),
                "unique_references": len(refs),
                "numeric_prices": len(nums),
                "numeric_price_coverage": pct(len(nums) / len(subset)) if subset else "",
                "price_upon_request": sum(r["price_status"] == "price_upon_request" for r in subset),
                "unresolved_missing": sum(r["price_status"] == "unresolved" for r in subset),
                "product_families": len(families),
                "bag_type_group_nonmissing": sum(r["bag_type_group"] != "unknown" for r in subset),
                "material_nonmissing": sum(r["material_class"] != "missing" for r in subset),
                "dimension_volume_available": sum(r["volume_cm3"] is not None for r in subset),
                "signature_class_known": sum(r["signature_class"] != "unknown" for r in subset),
            })
    # Brand total rows.
    for brand in brands:
        subset = [r for r in rows if r["brand"] == brand]
        nums = numeric(subset)
        refs = {r["reference"] for r in subset if r["reference"]}
        profile.append({
            "brand": brand,
            "market": "ALL",
            "observations": len(subset),
            "unique_references": len(refs),
            "numeric_prices": len(nums),
            "numeric_price_coverage": pct(len(nums) / len(subset)) if subset else "",
            "price_upon_request": sum(r["price_status"] == "price_upon_request" for r in subset),
            "unresolved_missing": sum(r["price_status"] == "unresolved" for r in subset),
            "product_families": len({r["product_family"] for r in subset if r["product_family"]}),
            "bag_type_group_nonmissing": sum(r["bag_type_group"] != "unknown" for r in subset),
            "material_nonmissing": sum(r["material_class"] != "missing" for r in subset),
            "dimension_volume_available": sum(r["volume_cm3"] is not None for r in subset),
            "signature_class_known": sum(r["signature_class"] != "unknown" for r in subset),
        })
    write_csv("data_profile.csv", profile)

    missingness = []
    field_checks = {
        "product_family": lambda r: bool(r["product_family"]),
        "bag_type_group": lambda r: r["bag_type_group"] != "unknown",
        "material": lambda r: r["material_class"] != "missing",
        "size_group": lambda r: r["size_group"] != "unknown",
        "numeric_price": lambda r: r["price"] is not None,
        "signature_class": lambda r: r["signature_class"] != "unknown",
    }
    for brand in brands:
        subset = [r for r in rows if r["brand"] == brand]
        for field, test in field_checks.items():
            present = sum(test(r) for r in subset)
            missingness.append({"brand": brand, "field": field, "present": present, "missing": len(subset) - present, "coverage": pct(present / len(subset)) if subset else ""})
    write_csv("missingness.csv", missingness)

    # Brand price architecture by market.
    summaries = []
    for brand in brands:
        for market in ["FR", "US"]:
            vals = [r["price"] for r in rows if r["brand"] == brand and r["market"] == market and r["price_status"] == "numeric"]
            summaries.append({
                "brand": brand,
                "market": market,
                "currency": "EUR" if market == "FR" else "USD",
                "n_numeric": len(vals),
                "minimum": fmt(min(vals) if vals else None),
                "lower_quartile_p25": fmt(linear_quantile(vals, 0.25)),
                "median_p50": fmt(linear_quantile(vals, 0.50)),
                "upper_quartile_p75": fmt(linear_quantile(vals, 0.75)),
                "maximum": fmt(max(vals) if vals else None),
                "range_multiple_max_over_min": fmt(max(vals) / min(vals)) if vals and min(vals) else "",
            })
    write_csv("brand_price_summary.csv", summaries)

    family_rows = []
    for brand in brands:
        for market in ["FR", "US"]:
            families = sorted({r["product_family"] for r in rows if r["brand"] == brand and r["market"] == market})
            for family in families:
                subset = [r for r in rows if r["brand"] == brand and r["market"] == market and r["product_family"] == family]
                vals = [r["price"] for r in subset if r["price_status"] == "numeric"]
                family_rows.append({
                    "brand": brand, "market": market, "product_family": family,
                    "observations": len(subset), "numeric": len(vals),
                    "numeric_share": pct(len(vals) / len(subset)) if subset else "",
                    "minimum": fmt(min(vals) if vals else None),
                    "p25": fmt(linear_quantile(vals, .25)), "median": fmt(linear_quantile(vals, .5)),
                    "p75": fmt(linear_quantile(vals, .75)), "maximum": fmt(max(vals) if vals else None),
                })
    write_csv("family_price_summary.csv", family_rows)

    # Observed-distribution bands, kept separate by market/currency.
    bands = {
        "FR": [(0, 2999, "Access / lower"), (3000, 4999, "Core"), (5000, 6999, "Premium core"), (7000, 9999, "High"), (10000, float("inf"), "Exceptional / icon")],
        "US": [(0, 3999, "Access / lower"), (4000, 5999, "Core"), (6000, 7999, "Premium core"), (8000, 10999, "High"), (11000, float("inf"), "Exceptional / icon")],
    }

    def band_for(market: str, price: float) -> str:
        for lower, upper, label in bands[market]:
            if lower <= price <= upper:
                return label
        return "Unknown"

    band_rows = []
    for market in ["FR", "US"]:
        pooled = [r for r in rows if r["market"] == market and r["price_status"] == "numeric"]
        for brand in brands:
            nums = [r for r in pooled if r["brand"] == brand]
            for _, _, label in bands[market]:
                in_band = [r for r in nums if band_for(market, r["price"]) == label]
                pooled_band = [r for r in pooled if band_for(market, r["price"]) == label]
                band_rows.append({
                    "market": market, "currency": "EUR" if market == "FR" else "USD", "brand": brand,
                    "band": label, "numeric_observations": len(in_band),
                    "share_of_brand_numeric": pct(len(in_band) / len(nums)) if nums else "",
                    "pooled_band_observations": len(pooled_band),
                    "share_of_pooled_band": pct(len(in_band) / len(pooled_band)) if pooled_band else "",
                })
    write_csv("price_band_summary.csv", band_rows)

    # Exact reference France-US mapping.
    matched_rows = []
    for brand in brands:
        for ref in sorted({r["reference"] for r in rows if r["brand"] == brand}):
            fr = next((r for r in rows if r["brand"] == brand and r["reference"] == ref and r["market"] == "FR"), None)
            us = next((r for r in rows if r["brand"] == brand and r["reference"] == ref and r["market"] == "US"), None)
            if not fr or not us:
                continue
            fr_price = fr["price"] if fr["price_status"] == "numeric" else None
            us_price = us["price"] if us["price_status"] == "numeric" else None
            ratio = us_price / fr_price if fr_price and us_price else None
            matched_rows.append({
                "brand": brand, "reference": ref, "product_family": fr["product_family"],
                "france_price": fmt(fr_price), "us_price": fmt(us_price),
                "france_status": fr["price_status"], "us_status": us["price_status"],
                "us_local_number_divided_by_fr_local_number": fmt(ratio),
                "numeric_pair": "yes" if ratio is not None else "no",
            })
    write_csv("matched_fr_us_mapping.csv", matched_rows)

    market_map = []
    for brand in brands:
        vals = [as_float(r["us_local_number_divided_by_fr_local_number"]) for r in matched_rows if r["brand"] == brand and r["numeric_pair"] == "yes"]
        vals = [v for v in vals if v is not None]
        market_map.append({
            "brand": brand, "numeric_exact_pairs": len(vals),
            "minimum_ratio": fmt(min(vals) if vals else None), "median_ratio": fmt(linear_quantile(vals, .5)),
            "maximum_ratio": fmt(max(vals) if vals else None),
            "interpretation_boundary": "local display mapping only; not FX/tax-normalized" if vals else "no numeric exact pairs",
        })
    write_csv("fr_us_mapping_summary.csv", market_map)

    # Signature/icon analytical premium.
    icon_rows = []
    for brand in brands:
        for market in ["FR", "US"]:
            subset = [r for r in rows if r["brand"] == brand and r["market"] == market and r["price_status"] == "numeric"]
            icons = [r["price"] for r in subset if r["signature_class"] in {"icon_inferred", "icon_supplied"}]
            non_icons = [r["price"] for r in subset if r["signature_class"] in {"non_icon_observed", "non_icon_supplied", "other_unflagged_observed"}]
            icon_rows.append({
                "brand": brand, "market": market, "icon_definition": "inferred from Classic families" if brand == "CHANEL" else "supplied true flag vs other unflagged observations" if brand in {"Dior", "Louis Vuitton"} else "not available",
                "n_icon_numeric": len(icons), "icon_median": fmt(linear_quantile(icons, .5)),
                "n_non_icon_numeric": len(non_icons), "non_icon_median": fmt(linear_quantile(non_icons, .5)),
                "icon_premium_ratio": fmt(linear_quantile(icons, .5) / linear_quantile(non_icons, .5)) if icons and non_icons else "",
                "icon_premium_difference": fmt(linear_quantile(icons, .5) - linear_quantile(non_icons, .5)) if icons and non_icons else "",
                "confidence": "medium" if brand == "CHANEL" and len(icons) >= 3 and len(non_icons) >= 3 else "low" if icons and non_icons else "not estimable",
            })
    write_csv("icon_premium_summary.csv", icon_rows)

    # Comparable-cell index: no global cross-assortment index is calculated.
    cell_groups = defaultdict(list)
    for r in numeric(rows):
        key = (r["market"], r["bag_type_group"], r["size_group"], r["material_class"])
        cell_groups[key].append(r)
    cell_rows = []
    for (market, bag_type, size, material), cell in sorted(cell_groups.items()):
        brands_in_cell = sorted({r["brand"] for r in cell})
        if len(brands_in_cell) < 2 or bag_type == "unknown" or size == "unknown" or material == "missing":
            continue
        pooled_median = linear_quantile([r["price"] for r in cell], .5)
        for brand in brands_in_cell:
            brand_vals = [r["price"] for r in cell if r["brand"] == brand]
            cell_rows.append({
                "market": market, "currency": "EUR" if market == "FR" else "USD",
                "cell": f"{bag_type} | {size} | {material}", "bag_type_group": bag_type,
                "size_group": size, "material_class": material, "brand": brand,
                "n_numeric": len(brand_vals), "brand_median": fmt(linear_quantile(brand_vals, .5)),
                "cell_pooled_median_benchmark": fmt(pooled_median),
                "comparable_price_index_benchmark_100": fmt(linear_quantile(brand_vals, .5) / pooled_median * 100),
                "cell_brand_count": len(brands_in_cell),
                "confidence": "medium" if len(brand_vals) >= 2 and len(brands_in_cell) >= 3 else "low-medium",
            })
    write_csv("comparable_cell_price_index.csv", cell_rows)

    # Flat numeric observations for later visualization / audit.
    flat_rows = []
    for r in numeric(rows):
        flat_rows.append({
            "brand": r["brand"], "market": r["market"], "currency": r["currency"], "reference": r["reference"],
            "product_family": r["product_family"], "price": fmt(r["price"]), "band": band_for(r["market"], r["price"]),
            "bag_type_group": r["bag_type_group"], "size_group": r["size_group"], "material_class": r["material_class"],
            "signature_class": r["signature_class"], "source": r["source"],
        })
    write_csv("numeric_observations_for_visualization.csv", flat_rows)

    # Compact metadata for the narrative layer.
    write_json("run_summary.json", {
        "total_observations": len(rows),
        "total_numeric": len(numeric(rows)),
        "total_non_numeric": len(rows) - len(numeric(rows)),
        "brands": {brand: {"observations": len([r for r in rows if r["brand"] == brand]), "unique_references": len({r["reference"] for r in rows if r["brand"] == brand}), "numeric": len(numeric([r for r in rows if r["brand"] == brand]))} for brand in brands},
        "matched_exact_reference_rows": len(matched_rows),
        "matched_numeric_pair_rows": sum(r["numeric_pair"] == "yes" for r in matched_rows),
        "comparable_cells": len({r["cell"] + " | " + r["market"] for r in cell_rows}),
    })


if __name__ == "__main__":
    main()
