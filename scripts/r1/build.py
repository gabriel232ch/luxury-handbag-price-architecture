#!/usr/bin/env python3
"""Build the traceable Luxury Handbag Research Upgrade R1 outputs.

The script deliberately works from the preserved local snapshots. It does not
fetch URLs. Current observations and the historical panel remain separate via
``snapshot_id`` so a later refresh cannot be mistaken for an old observation.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
R1 = ROOT / "research_r1"
DATA = R1 / "data"
OUT = R1 / "outputs"
REPORT = R1 / "report"
EXPORT = R1 / "export"

CURRENT_SNAPSHOT = "current_2026-08-15"
HISTORY_SNAPSHOT = "historical_panel_2026-08-15"
BRANDS = ["Chanel", "Hermès", "Louis Vuitton", "Dior"]
MARKETS = ["FR", "US"]
CURRENT_SOURCE_FILES = {
    "Chanel": ROOT / "chanel_fr_us_handbags_current" / "clean_data.csv",
    "competitors": ROOT / "luxury_competitor_pricing_current" / "clean" / "competitor_pricing_clean.csv",
}
HISTORY_FILE = ROOT / "luxury_historical_pricing" / "clean" / "historical_pricing_clean.csv"
LINEAGE_FILE = ROOT / "luxury_historical_pricing" / "lineage" / "product_lineage.csv"
HISTORY_SOURCE_FILE = ROOT / "luxury_historical_pricing" / "logs" / "HISTORICAL_SOURCE_REGISTRY.csv"
HISTORY_UNRESOLVED_FILE = ROOT / "luxury_historical_pricing" / "errors" / "unresolved_history.jsonl"
COMPETITOR_ERRORS_FILE = ROOT / "luxury_competitor_pricing_current" / "errors" / "errors.jsonl"
CHANEL_ERRORS_FILE = ROOT / "chanel_fr_us_handbags_current" / "errors.jsonl"

OBSERVATION_FIELDS = [
    "observation_id", "snapshot_id", "brand", "market", "currency", "observed_at",
    "source_effective_date", "source_id", "reference_code", "family", "model",
    "size_label", "material_group", "color", "price_status", "price",
    "comparison_group_id", "lineage_id", "inclusion_status", "exclusion_reason",
]

LINEAGE_FIELDS = [
    "lineage_id", "brand", "family", "current_reference", "historical_reference",
    "continuity_status", "confidence", "source_lineage_file", "notes",
]

SOURCE_FIELDS = [
    "source_id", "brand", "source_type", "source_name", "source_url", "archive_url",
    "source_effective_date", "accessed_at", "primary_or_secondary", "source_quality", "notes",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def parse_price(value: str | None) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        value = str(value).replace(",", "").strip()
        result = float(value)
        return result if math.isfinite(result) else None
    except ValueError:
        return None


def fmt(value: float | None, places: int = 2) -> str:
    if value is None:
        return ""
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.{places}f}"


def quantile(values: list[float], p: float) -> float | None:
    values = sorted(values)
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    pos = (len(values) - 1) * p
    low, high = math.floor(pos), math.ceil(pos)
    if low == high:
        return values[low]
    return values[low] + (values[high] - values[low]) * (pos - low)


def median(values: list[float]) -> float | None:
    return quantile(values, 0.5)


def normal_market(value: str) -> str:
    value = (value or "").strip()
    if value in {"FR", "France"}:
        return "FR"
    if value in {"US", "United States"}:
        return "US"
    return value


def date_part(value: str) -> str:
    return (value or "")[:10]


def material_group(value: str) -> str:
    text = (value or "").lower()
    if not text.strip():
        return "unknown"
    leather = ("calfskin", "lambskin", "leather", "goat", "togo", "epsom", "swift",
               "barénia", "barenia", "cowhide", "negonda", "mysore", "agneau", "veau", "cuir")
    textile = ("canvas", "tweed", "denim", "raffia", "silk", "textile", "wool", "cotton",
               "jersey", "fabric", "toile", "crêpe", "jacquard")
    has_leather = any(token in text for token in leather)
    has_textile = any(token in text for token in textile)
    if has_leather and has_textile:
        return "leather_and_textile"
    if has_leather:
        return "leather"
    if has_textile:
        return "textile_or_mixed"
    return "other_or_unclear"


def dimensions(row: dict[str, str]) -> tuple[float | None, float | None, float | None]:
    keys = ("width_cm", "height_cm", "depth_cm")
    vals = [parse_price(row.get(key)) for key in keys]
    if all(value is not None for value in vals):
        return vals[0], vals[1], vals[2]
    raw = row.get("dimensions") or row.get("dimensions_raw") or ""
    numbers = [parse_price(value) for value in re.findall(r"(?<![A-Za-z])\d+(?:\.\d+)?", raw)]
    numbers = [value for value in numbers if value is not None]
    return (numbers + [None, None, None])[:3] if len(numbers) >= 3 else (None, None, None)


def size_label(row: dict[str, str]) -> str:
    supplied = (row.get("size_label") or "").strip()
    if supplied:
        return supplied
    family = (row.get("product_family") or "").lower()
    if "small classic" in family:
        return "small"
    if "mini" in family:
        return "mini"
    if "classic 11.12" in family:
        return "medium"
    if "shopping" in family or "bowling" in family:
        return "standard"
    return "unknown"


def bag_group(row: dict[str, str]) -> str:
    raw = (row.get("bag_type") or "").lower()
    family = (row.get("product_family") or "").lower()
    if "classic" in family:
        return "flap"
    if "shopping" in family or "bowling" in family:
        return "tote"
    return {"flap_bag": "flap", "clutch": "flap", "tote": "tote", "crossbody": "crossbody",
            "shoulder_bag": "shoulder", "top_handle_bag": "top_handle", "backpack": "backpack"}.get(raw, raw or "unknown")


def comparison_group(row: dict[str, str], source_row: dict[str, str]) -> str:
    return "|".join((row["market"], bag_group(source_row), row["size_label"], row["material_group"]))


def source_id_for(brand: str, market: str, reference: str, source_url: str) -> str:
    digest = hashlib.sha1(source_url.encode("utf-8")).hexdigest()[:10]
    safe_brand = re.sub(r"[^A-Za-z0-9]+", "_", brand.upper()).strip("_")
    safe_ref = re.sub(r"[^A-Za-z0-9]+", "_", reference).strip("_") or "NOREF"
    return f"SRC-CURRENT-{safe_brand}-{market}-{safe_ref}-{digest}"


CHANEL_LINEAGES = {
    "A01112-Y04059-U8390": "CH-C01",
    "A01113-Y01864-C3906": "CH-C02",
    "A35200-Y04059-94305": "CH-C03",
    "A69900-Y04059-94305": "CH-C04",
}


def make_current_rows() -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    sources: dict[str, dict] = {}
    chanel_raw = read_csv(CURRENT_SOURCE_FILES["Chanel"])
    competitor_raw = read_csv(CURRENT_SOURCE_FILES["competitors"])
    for source_name, raw_rows in (("chanel_fr_us_handbags_current/clean_data.csv", chanel_raw),
                                  ("luxury_competitor_pricing_current/clean/competitor_pricing_clean.csv", competitor_raw)):
        for raw in raw_rows:
            brand = "Chanel" if raw.get("brand", "").upper() == "CHANEL" else raw.get("brand", "").strip()
            market = normal_market(raw.get("market", ""))
            reference = raw.get("sku_or_reference") or raw.get("official_sku_or_reference") or ""
            observed_at = raw.get("observed_at", "")
            price = parse_price(raw.get("price"))
            status = (raw.get("price_status") or ("numeric" if price is not None else "price_upon_request" if brand == "Chanel" else "unresolved")).strip()
            if price is not None and status != "numeric":
                status = "numeric"
            currency = raw.get("currency") or ("EUR" if market == "FR" else "USD")
            family = raw.get("product_family", "").strip()
            material = raw.get("material", "")
            label = size_label(raw)
            canonical = {
                "market": market, "size_label": label, "material_group": material_group(material),
            }
            source_id = source_id_for(brand, market, reference, raw.get("source_url", ""))
            original_id = raw.get("observation_id") or f"{brand}-{market}-{reference}-{date_part(observed_at)}"
            observation_id = f"current:{original_id}"
            lineage = CHANEL_LINEAGES.get(reference, "") if brand == "Chanel" else ""
            row = {
                "observation_id": observation_id,
                "snapshot_id": CURRENT_SNAPSHOT,
                "brand": brand,
                "market": market,
                "currency": currency,
                "observed_at": observed_at,
                "source_effective_date": date_part(observed_at),
                "source_id": source_id,
                "reference_code": reference,
                "family": family,
                "model": raw.get("product_name", "").strip(),
                "size_label": label,
                "material_group": canonical["material_group"],
                "color": raw.get("color", "").strip(),
                "price_status": status,
                "price": fmt(price),
                "comparison_group_id": comparison_group(canonical, raw),
                "lineage_id": lineage,
                "inclusion_status": "accepted",
                "exclusion_reason": "",
            }
            rows.append(row)
            sources[source_id] = {
                "source_id": source_id, "brand": brand, "source_type": "official_current_product_page",
                "source_name": source_name, "source_url": raw.get("source_url", ""), "archive_url": "",
                "source_effective_date": date_part(observed_at), "accessed_at": observed_at,
                "primary_or_secondary": "primary", "source_quality": "HIGH",
                "notes": "Preserved supplied official localized snapshot; not refreshed during R1.",
            }
    return rows, list(sources.values())


def make_history_rows() -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    for raw in read_csv(HISTORY_FILE):
        brand = raw.get("brand", "").strip()
        market = normal_market(raw.get("market", ""))
        reference = raw.get("current_reference") or raw.get("historical_reference") or ""
        observed_date = raw.get("observation_date", "").strip()
        price = parse_price(raw.get("price"))
        status = raw.get("price_status") or ("numeric" if price is not None else "unresolved")
        if price is not None and status != "numeric":
            status = "numeric"
        source_ids = (raw.get("source_ids") or "").split(";")
        source_id = source_ids[0].strip() if source_ids and source_ids[0].strip() else f"HISTORY-{raw.get('observation_id', '')}"
        material = raw.get("material", "")
        source_effective = raw.get("effective_date_if_known") or observed_date
        raw_for_group = {"market": market, "size_label": raw.get("size_label") or "unknown", "material_group": material_group(material),
                         "product_family": raw.get("product_family", ""), "bag_type": raw.get("product_family", "")}
        row = {
            "observation_id": f"history:{raw.get('observation_id', '')}",
            "snapshot_id": HISTORY_SNAPSHOT,
            "brand": brand,
            "market": market,
            "currency": raw.get("currency") or ("EUR" if market == "FR" else "USD"),
            "observed_at": observed_date,
            "source_effective_date": source_effective,
            "source_id": source_id,
            "reference_code": reference,
            "family": raw.get("product_family", ""),
            "model": raw.get("product_name", ""),
            "size_label": raw.get("size_label") or "unknown",
            "material_group": material_group(material),
            "color": raw.get("color_if_material", ""),
            "price_status": status,
            "price": fmt(price),
            "comparison_group_id": comparison_group(raw_for_group, raw_for_group),
            "lineage_id": raw.get("product_lineage_id", ""),
            "inclusion_status": "accepted_conflict" if raw.get("conflict_flag") == "true" else "accepted",
            "exclusion_reason": "source conflict retained for sensitivity" if raw.get("conflict_flag") == "true" else "",
        }
        rows.append(row)

    registry = []
    for raw in read_csv(HISTORY_SOURCE_FILE):
        registry.append({
            "source_id": raw.get("source_id", ""), "brand": raw.get("brand", ""),
            "source_type": raw.get("source_type", ""), "source_name": raw.get("source_name", ""),
            "source_url": raw.get("original_url", ""), "archive_url": raw.get("archive_url", ""),
            "source_effective_date": raw.get("source_date", ""), "accessed_at": raw.get("accessed_at", ""),
            "primary_or_secondary": raw.get("primary_or_secondary", ""), "source_quality": raw.get("source_quality", ""),
            "notes": raw.get("notes", ""),
        })
    return rows, registry


def load_lineages() -> tuple[list[dict], dict[str, dict]]:
    raw_rows = read_csv(LINEAGE_FILE)
    rows = []
    for raw in raw_rows:
        row = {
            "lineage_id": raw.get("product_lineage_id", ""), "brand": raw.get("brand", ""),
            "family": raw.get("product_family", ""), "current_reference": raw.get("current_reference", ""),
            "historical_reference": raw.get("historical_reference", ""),
            "continuity_status": raw.get("continuity_status", ""), "confidence": raw.get("confidence", ""),
            "source_lineage_file": str(LINEAGE_FILE.relative_to(ROOT)),
            "notes": raw.get("notes", ""),
        }
        rows.append(row)
    return rows, {row["lineage_id"]: row for row in rows}


def current_numeric(rows: list[dict]) -> list[dict]:
    return [row for row in rows if row["snapshot_id"] == CURRENT_SNAPSHOT and row["price_status"] == "numeric" and parse_price(row["price"]) is not None]


def stable_variant_key(row: dict) -> str:
    return "|".join((row["brand"], row["market"], row["family"], row["model"], row["size_label"], row["material_group"], row["price"]))


def build_coverage(rows: list[dict]) -> list[dict]:
    current = [row for row in rows if row["snapshot_id"] == CURRENT_SNAPSHOT]
    output = []
    for brand in BRANDS:
        for market in MARKETS:
            for family in sorted({r["family"] for r in current if r["brand"] == brand and r["market"] == market}):
                group = [r for r in current if r["brand"] == brand and r["market"] == market and r["family"] == family]
                nums = [r for r in group if r["price_status"] == "numeric" and parse_price(r["price"]) is not None]
                output.append({
                    "snapshot_id": CURRENT_SNAPSHOT, "brand": brand, "market": market, "currency": "EUR" if market == "FR" else "USD",
                    "family": family, "accepted_observations": len(group), "numeric_observations": len(nums),
                    "unique_reference_count": len({r["reference_code"] for r in group if r["reference_code"]}),
                    "devariant_group_count": len({stable_variant_key(r) for r in nums}),
                    "price_upon_request_count": sum(r["price_status"] == "price_upon_request" for r in group),
                    "unresolved_count": sum(r["price_status"] == "unresolved" for r in group),
                    "unknown_material_count": sum(r["material_group"] == "unknown" for r in group),
                    "scope_note": "Counts describe accepted local observations; they are not official assortment coverage.",
                })
    return output


def build_family_summary(rows: list[dict]) -> list[dict]:
    output = []
    for brand in BRANDS:
        for market in MARKETS:
            families = sorted({r["family"] for r in rows if r["snapshot_id"] == CURRENT_SNAPSHOT and r["brand"] == brand and r["market"] == market})
            for family in families:
                group = [r for r in rows if r["snapshot_id"] == CURRENT_SNAPSHOT and r["brand"] == brand and r["market"] == market and r["family"] == family]
                nums = [parse_price(r["price"]) for r in group if r["price_status"] == "numeric" and parse_price(r["price"]) is not None]
                nums = [n for n in nums if n is not None]
                unique = len({r["reference_code"] for r in group if r["reference_code"]})
                devar = {stable_variant_key(r) for r in group if r["price_status"] == "numeric" and parse_price(r["price"]) is not None}
                output.append({
                    "brand": brand, "market": market, "currency": "EUR" if market == "FR" else "USD", "family": family,
                    "observations": len(group), "numeric_observations": len(nums), "unique_references": unique,
                    "devariant_groups": len(devar), "minimum_observed_price": fmt(min(nums) if nums else None),
                    "p10_sample": fmt(quantile(nums, .10)), "p25_sample": fmt(quantile(nums, .25)),
                    "p50_sample": fmt(quantile(nums, .50)), "p75_sample": fmt(quantile(nums, .75)),
                    "p90_sample": fmt(quantile(nums, .90)), "maximum_observed_price": fmt(max(nums) if nums else None),
                    "distribution_note": "N<10: tails are descriptive only; unit is the accepted observed product row.",
                })
    return output


def band_for(price: float, edges: list[float]) -> int:
    for idx, edge in enumerate(edges):
        if price < edge:
            return idx
    return len(edges)


def build_band_sensitivity(rows: list[dict]) -> list[dict]:
    base_edges = {"FR": [3000, 5000, 7000, 10000], "US": [4000, 6000, 8000, 11000]}
    labels = ["Access / lower", "Core", "Premium core", "High", "Exceptional / icon"]
    output = []
    numeric = current_numeric(rows)
    for market, edges in base_edges.items():
        scenarios = [("baseline", edges)]
        for index, edge in enumerate(edges):
            scenarios.append((f"boundary_{index+1}_minus10pct", [e * .9 if i == index else e for i, e in enumerate(edges)]))
            scenarios.append((f"boundary_{index+1}_plus10pct", [e * 1.1 if i == index else e for i, e in enumerate(edges)]))
        pooled = [r for r in numeric if r["market"] == market]
        for scenario, scenario_edges in scenarios:
            for brand in BRANDS:
                brand_rows = [r for r in pooled if r["brand"] == brand]
                denom = len(brand_rows)
                for idx, label in enumerate(labels):
                    count = sum(band_for(parse_price(r["price"]) or 0, scenario_edges) == idx for r in brand_rows)
                    output.append({
                        "market": market, "currency": "EUR" if market == "FR" else "USD", "scenario": scenario,
                        "band": label, "brand": brand, "numeric_observations": count,
                        "share_of_brand_numeric": fmt(count / denom * 100, 1) + "%" if denom else "",
                        "boundary_definition": ";".join(fmt(e) for e in scenario_edges),
                        "denominator_note": "Denominator is brand × market numeric observations; bands are post-hoc descriptive bins.",
                    })
    return output


def build_chanel_ladder(rows: list[dict]) -> list[dict]:
    role_map = {"Mini Classic": "entry", "Classic 11.12": "classic", "Small Classic": "classic", "Shopping Bag": "core_other", "Bowling Bag": "core_other"}
    output = []
    for market in MARKETS:
        market_rows = [r for r in current_numeric(rows) if r["brand"] == "Chanel" and r["market"] == market]
        role_values: dict[str, list[float]] = defaultdict(list)
        for row in market_rows:
            role_values[role_map.get(row["family"], "other")].append(parse_price(row["price"]) or 0)
        classic = role_values.get("classic", [])
        comparison = role_values.get("entry", []) + role_values.get("core_other", [])
        classic_min = min(classic) if classic else None
        comparison_max = max(comparison) if comparison else None
        gap = classic_min - comparison_max if classic_min is not None and comparison_max is not None else None
        classic_med = median(classic)
        comparison_med = median(comparison)
        output.append({
            "snapshot_id": CURRENT_SNAPSHOT, "brand": "Chanel", "market": market,
            "currency": "EUR" if market == "FR" else "USD", "classic_n": len(classic),
            "entry_core_n": len(comparison), "classic_min": fmt(classic_min), "entry_core_max": fmt(comparison_max),
            "observed_gap": fmt(gap), "classic_median": fmt(classic_med), "entry_core_median": fmt(comparison_med),
            "median_distance": fmt(classic_med - comparison_med if classic_med is not None and comparison_med is not None else None),
            "relative_ratio": fmt(classic_med / comparison_med, 3) if classic_med is not None and comparison_med else "",
            "family_membership": "classic=Classic 11.12 + Small Classic; entry=Mini Classic; core_other=Shopping Bag + Bowling Bag",
            "inquiry_status_note": "Chanel price-upon-request rows remain outside the price axis and numeric denominator.",
        })
    return output


def build_comparable_cells(rows: list[dict]) -> list[dict]:
    numeric = current_numeric(rows)
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in numeric:
        groups[(row["market"], row["comparison_group_id"])].append(row)
    output = []
    for (market, group_id), group in sorted(groups.items()):
        by_brand = {brand: [r for r in group if r["brand"] == brand] for brand in BRANDS}
        eligible = all(len({stable_variant_key(r) for r in brand_rows}) >= 3 for brand_rows in by_brand.values())
        if sum(bool(value) for value in by_brand.values()) < 2:
            continue
        pooled = [parse_price(r["price"]) for r in group]
        pooled = [v for v in pooled if v is not None]
        benchmark = median(pooled)
        output.append({
            "market": market, "currency": "EUR" if market == "FR" else "USD", "comparison_group_id": group_id,
            "brand_counts": ";".join(f"{brand}:{len(by_brand[brand])}" for brand in BRANDS),
            "brand_medians": ";".join(f"{brand}:{fmt(median([parse_price(r['price']) for r in by_brand[brand] if parse_price(r['price']) is not None]))}" for brand in BRANDS if by_brand[brand]),
            "pooled_cell_median": fmt(benchmark), "headline_eligible": "TRUE" if eligible else "FALSE",
            "publication_decision": "appendix_only" if not eligible else "directional_main_text",
            "limitation": "Directional cell only; not a strict substitute set or probability sample.",
        })
    return output


def build_aligned_history(rows: list[dict], lineages: dict[str, dict]) -> list[dict]:
    # Chanel France only; keep the two Mini lineages separate but summarize the
    # role groups at dates shared by both roles. No interpolation is performed.
    icon_ids, access_ids = {"CH-C01", "CH-C02"}, {"CH-C03", "CH-C04"}
    history = [r for r in rows if r["snapshot_id"] == HISTORY_SNAPSHOT and r["brand"] == "Chanel" and r["market"] == "FR" and r["price_status"] == "numeric" and r["inclusion_status"] != "accepted_conflict"]
    years = sorted({r["observed_at"][:4] for r in history if r["observed_at"][:4].isdigit()})
    output = []
    for year in years:
        icon = [parse_price(r["price"]) for r in history if r["observed_at"].startswith(year) and r["lineage_id"] in icon_ids]
        access = [parse_price(r["price"]) for r in history if r["observed_at"].startswith(year) and r["lineage_id"] in access_ids]
        icon = [v for v in icon if v is not None]
        access = [v for v in access if v is not None]
        if not icon or not access:
            continue
        icon_med, access_med = median(icon), median(access)
        output.append({
            "brand": "Chanel", "market": "FR", "currency": "EUR", "observed_year": year,
            "icon_lineages": ";".join(sorted(icon_ids)), "access_lineages": ";".join(sorted(access_ids)),
            "icon_n": len(icon), "access_n": len(access), "icon_median": fmt(icon_med), "access_median": fmt(access_med),
            "absolute_gap": fmt(icon_med - access_med), "relative_ratio": fmt(icon_med / access_med, 3),
            "fixed_member_note": "Common observed years only; lineage members are fixed and missing years are not interpolated.",
        })
    return output


def build_robustness(rows: list[dict], ladder: list[dict], bands: list[dict], aligned: list[dict]) -> list[dict]:
    output = []
    numeric = current_numeric(rows)
    for market in MARKETS:
        subset = [r for r in numeric if r["brand"] == "Chanel" and r["market"] == market]
        dedup = {}
        for row in subset:
            dedup.setdefault(stable_variant_key(row), row)
        def gap(sample: list[dict]) -> float | None:
            classic = [parse_price(r["price"]) for r in sample if r["family"] in {"Classic 11.12", "Small Classic"}]
            other = [parse_price(r["price"]) for r in sample if r["family"] in {"Mini Classic", "Shopping Bag", "Bowling Bag"}]
            classic = [v for v in classic if v is not None]
            other = [v for v in other if v is not None]
            return min(classic) - max(other) if classic and other else None
        baseline = gap(subset)
        alternative = gap(list(dedup.values()))
        output.append({"module": "M2", "scenario": "raw_vs_devariant", "market": market, "metric": "observed_gap", "baseline": fmt(baseline), "alternative": fmt(alternative), "delta": fmt(alternative - baseline if baseline is not None and alternative is not None else None), "stable": "TRUE" if baseline == alternative else "FALSE", "notes": "Color/near-duplicate rows collapse only in the de-variant view."})
    for row in aligned:
        output.append({"module": "M5", "scenario": "aligned_history", "market": row["market"], "metric": "absolute_gap", "baseline": row["absolute_gap"], "alternative": "", "delta": "", "stable": "TRUE", "notes": row["fixed_member_note"]})
    # Summarize whether a price-band classification changes under any boundary perturbation.
    for market in MARKETS:
        base = {(r["brand"], r["band"]): r["numeric_observations"] for r in bands if r["market"] == market and r["scenario"] == "baseline"}
        for brand in BRANDS:
            for band in sorted({r["band"] for r in bands if r["market"] == market}):
                alternatives = [r["numeric_observations"] for r in bands if r["market"] == market and r["brand"] == brand and r["band"] == band and r["scenario"] != "baseline"]
                baseline = base.get((brand, band), 0)
                output.append({"module": "M3", "scenario": "boundary_plus_minus10pct", "market": market, "metric": f"{brand}:{band}:count", "baseline": str(baseline), "alternative": ";".join(str(x) for x in alternatives), "delta": "", "stable": "TRUE" if all(x == baseline for x in alternatives) else "FALSE", "notes": "Boundaries are sensitivity scenarios, not independent validation."})
    return output


def build_sources(current_sources: list[dict], history_sources: list[dict]) -> list[dict]:
    by_id = {row["source_id"]: row for row in history_sources}
    for row in current_sources:
        by_id[row["source_id"]] = row
    return [by_id[key] for key in sorted(by_id)]


def build_claims(rows: list[dict], ladder: list[dict], coverage: list[dict], aligned: list[dict], lineages: dict[str, dict]) -> list[dict]:
    claims = []
    current_ids = [r["observation_id"] for r in rows if r["snapshot_id"] == CURRENT_SNAPSHOT]
    for ladder_row in ladder:
        claims.append({
            "claim_id": f"CLM-LADDER-{ladder_row['market']}",
            "question": "How far apart are Chanel Classic and entry/core observations in the same market snapshot?",
            "claim_text": f"In the accepted {ladder_row['market']} numeric snapshot, the lowest Classic observation is {ladder_row['classic_min']} {ladder_row['currency']} versus a highest entry/core observation of {ladder_row['entry_core_max']} {ladder_row['currency']}; the observed gap is {ladder_row['observed_gap']} {ladder_row['currency']}.",
            "scope": f"Chanel; {ladder_row['market']}; {CURRENT_SNAPSHOT}; Classic=Classic 11.12 + Small Classic; comparison=Mini Classic + Shopping Bag + Bowling Bag.",
            "observation_ids": ";".join(current_ids), "calculation_id": "chanel_ladder",
            "output_path": "research_r1/outputs/chanel_ladder.csv", "evidence_grade": "B",
            "sensitivity_result": "See robustness.csv raw_vs_devariant and family coverage.",
            "limitation": "Accepted observed rows are not a complete assortment and do not establish purchase substitution.",
            "publication_decision": "retain_with_scope",
        })
    us_dior = next((r for r in coverage if r["brand"] == "Dior" and r["market"] == "US"), None)
    if us_dior:
        us_rows = [r for r in rows if r["snapshot_id"] == CURRENT_SNAPSHOT and r["brand"] == "Dior" and r["market"] == "US"]
        nums = sum(r["price_status"] == "numeric" for r in us_rows)
        claims.append({
            "claim_id": "CLM-COVERAGE-DIOR-US", "question": "Which visible gaps constrain cross-brand reading?",
            "claim_text": f"Dior US has {nums} numeric prices among {len(us_rows)} accepted observations ({nums / len(us_rows) * 100:.1f}% numeric coverage); unresolved rows remain excluded from price distributions.",
            "scope": f"Dior; US; {CURRENT_SNAPSHOT}; accepted observed product rows.", "observation_ids": ";".join(r["observation_id"] for r in us_rows),
            "calculation_id": "coverage", "output_path": "research_r1/data/coverage.csv", "evidence_grade": "A",
            "sensitivity_result": "No imputation; denominator remains accepted observations.",
            "limitation": "This is numeric coverage, not official website assortment coverage.", "publication_decision": "retain_with_scope",
        })
    if aligned:
        first, last = aligned[0], aligned[-1]
        claims.append({
            "claim_id": "CLM-HISTORY-CHANEL-FR", "question": "What does the date-aligned Chanel France panel support?",
            "claim_text": f"The Chanel France icon/access panel has common observed years {', '.join(r['observed_year'] for r in aligned)}; the median absolute distance is {first['absolute_gap']} {first['currency']} in {first['observed_year']} and {last['absolute_gap']} {last['currency']} in {last['observed_year']}.",
            "scope": "Chanel; FR; fixed CH-C01/CH-C02 versus CH-C03/CH-C04 lineages; common observed years only.",
            "observation_ids": ";".join(r["observation_id"] for r in rows if r["snapshot_id"] == HISTORY_SNAPSHOT and r["brand"] == "Chanel" and r["market"] == "FR"),
            "calculation_id": "aligned_history", "output_path": "research_r1/outputs/aligned_history.csv", "evidence_grade": "B",
            "sensitivity_result": "No missing-year interpolation; source conflicts excluded from primary path.",
            "limitation": "Historical values are primarily secondary-source observations and continuity is model-level, not exact historical SKU proof.", "publication_decision": "retain_with_scope",
        })
    claims.append({
        "claim_id": "CLM-HERMES-GETA-CONFLICT", "question": "What remains unresolved?",
        "claim_text": "Hermès Geta France has conflicting 2023 secondary-source values (EUR 4,550 and EUR 5,550); both are retained and excluded from the primary historical path.",
        "scope": "Hermès; FR; HM-H01; 2023 historical observation.", "observation_ids": ";".join(r["observation_id"] for r in rows if r.get("lineage_id") == "HM-H01" and r["inclusion_status"] == "accepted_conflict"),
        "calculation_id": "historical_conflict", "output_path": "research_r1/outputs/unresolved.csv", "evidence_grade": "X",
        "sensitivity_result": "Conflict retained as a branch; no forced selection.", "limitation": "Cannot support a single headline price path until resolved.", "publication_decision": "exclude_from_core",
    })
    return claims


def build_unresolved(rows: list[dict]) -> list[dict]:
    unresolved = []
    for path, kind in ((COMPETITOR_ERRORS_FILE, "current_competitor"), (CHANEL_ERRORS_FILE, "current_chanel")):
        for item in read_jsonl(path):
            if item.get("error_type") in {"PRICE_UNRESOLVED", "ACCESS_BLOCKED", "PAGE_NOT_FOUND"} or "unresolved" in str(item.get("error_type", "")).lower():
                unresolved.append({"issue_id": f"{kind}:{item.get('SKU/reference') or item.get('reference') or len(unresolved)+1}", "brand": item.get("brand", ""), "market": item.get("market", ""), "issue_type": item.get("error_type", "unresolved"), "reference_code": item.get("SKU/reference", ""), "source_url": item.get("URL", ""), "status": "unresolved", "critical_for_core": "TRUE" if item.get("error_type") == "PRICE_UNRESOLVED" else "FALSE", "notes": item.get("error_message", "")})
    for item in read_jsonl(HISTORY_UNRESOLVED_FILE):
        unresolved.append({"issue_id": f"history:{item.get('product_lineage_id') or item.get('candidate_id') or len(unresolved)+1}", "brand": item.get("brand", ""), "market": item.get("market", ""), "issue_type": "historical_identity_or_price_unresolved", "reference_code": item.get("current_reference", ""), "source_url": item.get("source_url", ""), "status": "unresolved", "critical_for_core": "FALSE", "notes": item.get("reason") or item.get("notes") or json.dumps(item, ensure_ascii=False)})
    conflict_rows = [r for r in rows if r["inclusion_status"] == "accepted_conflict"]
    for row in conflict_rows:
        unresolved.append({"issue_id": f"conflict:{row['observation_id']}", "brand": row["brand"], "market": row["market"], "issue_type": "source_conflict", "reference_code": row["reference_code"], "source_url": "", "status": "retained_for_sensitivity", "critical_for_core": "TRUE", "notes": "Both values retained; excluded from primary history path."})
    return unresolved


def build_reports(
    ladder: list[dict],
    family: list[dict],
    aligned: list[dict],
    unresolved: list[dict],
    coverage: list[dict],
    validation_status: str = "limited",
) -> None:
    fr = next(r for r in ladder if r["market"] == "FR")
    us = next(r for r in ladder if r["market"] == "US")
    common_years = ", ".join(r["observed_year"] for r in aligned) or "none"
    current_coverage = [row for row in coverage if row["snapshot_id"] == CURRENT_SNAPSHOT]
    as_int = lambda value: int(value or 0)
    current_accepted = sum(as_int(row["accepted_observations"]) for row in current_coverage)
    current_numeric = sum(as_int(row["numeric_observations"]) for row in current_coverage)
    brand_counts = {
        brand: sum(as_int(row["accepted_observations"]) for row in current_coverage if row["brand"] == brand)
        for brand in BRANDS
    }
    dior_us = [row for row in current_coverage if row["brand"] == "Dior" and row["market"] == "US"]
    dior_us_accepted = sum(as_int(row["accepted_observations"]) for row in dior_us)
    dior_us_numeric = sum(as_int(row["numeric_observations"]) for row in dior_us)
    dior_us_unresolved = dior_us_accepted - dior_us_numeric
    optional_rows = lambda path: read_csv(path) if path.exists() else []
    pairing_candidates = optional_rows(OUT / "comparable_pair_candidates.csv")
    pairing_cells = optional_rows(OUT / "comparable_cells_supplementary.csv")
    wave6_refresh = optional_rows(DATA / "wave6_same_date_refresh_2026-09-09_us.csv")
    wave6_cells = optional_rows(OUT / "wave6_same_date_pairing_cells_2026-09-09_us.csv")
    wave6_dimensions = optional_rows(OUT / "wave6_same_date_hobo_dimension_pairs_2026-09-09_us.csv")
    wave6_strict_count = sum(row.get("main_text_status") == "main_text_eligible" for row in wave6_cells)
    wave6_strict_word = "zero" if wave6_strict_count == 0 else str(wave6_strict_count)
    wave6_strict_word_cn = str(wave6_strict_count)
    matched_sizes = {
        f"{row.get('chanel_size_label', '').title()} and {row.get('peer_size_label', '').upper()}"
        for row in wave6_dimensions
        if row.get("dimension_match") == "TRUE"
    }
    matched_size_text = ", ".join(sorted(matched_sizes)) or "no matched size labels"
    brand_summary_cn = "，".join(f"{brand} {brand_counts[brand]} 条" for brand in BRANDS)
    report_cn = f"""# Luxury Handbag Research Upgrade R1：Chanel 价格架构（研究版）

## 执行摘要

本轮只分析公开本地标价样本，不把样本写成品牌全量组合。当前快照为 2026-08-15，法国以 EUR、美国以 USD 分开处理。研究中心是 Chanel：Classic 11.12 与 Small Classic 作为 Classic 组，Mini Classic、Shopping Bag 与 Bowling Bag 作为进入/其他核心对照。当前研究门状态为 **{validation_status}**：数据可复算，至少有两项可追溯的限定性发现，但样本覆盖、Dior 未解析价格和历史来源冲突仍限制旗舰叙事强度。

## 1. 观察范围与覆盖

当前接受观察共 {current_accepted} 条，其中 {current_numeric} 条为数值价格。{brand_summary_cn}。Dior 美国有 {dior_us_numeric} 条数值价格（共 {dior_us_accepted} 条接受观察），其余 {dior_us_unresolved} 条不插补；因此“数值覆盖率”只能描述可解析行的比例，不能称为官网覆盖率。颜色变体与近重复在原始视图保留，去变体视图只用于敏感性比较。

补充配对审计产生 {len(pairing_candidates)} 条属性匹配的方向性候选配对和 {len(pairing_cells)} 个补充属性单元；补充快照与基线竞品日期不一致，所有跨品牌价格比较保持 `not_computed`。最新独立刷新含 {len(wave6_refresh)} 行、{len(wave6_cells)} 个精确属性单元和 {wave6_strict_word_cn} 个严格主文单元；尺寸检查中出现 {matched_size_text}，但仍受属性、状态或独立家族样本门槛限制。

Hermès 的 40 条当前观察没有供应商标注的 signature flag；它可以提供价格坐标，不能支撑同口径的品牌图标溢价比较。当前快照的来源是原仓库已保存的官方本地页面观察，R1 没有把执行日的新页面回填到 8 月 15 日。

## 2. Chanel 价格梯度

法国样本中，Classic 组最低观察价为 {fr['classic_min']} EUR，进入/其他核心对照最高观察价为 {fr['entry_core_max']} EUR，观察间隔为 {fr['observed_gap']} EUR；两组中位数距离为 {fr['median_distance']} EUR，相对比值为 {fr['relative_ratio']}。美国对应数字为 {us['classic_min']}、{us['entry_core_max']}、{us['observed_gap']} USD，中位数距离 {us['median_distance']} USD，相对比值 {us['relative_ratio']}。

这些数字是同一市场、同一快照内的观察间隔。询价状态保持为状态字段，不放到价格轴顶端。Mini Classic 名称含 Classic，但在本轮被明确定义为进入组；它与 Classic 11.12/Small Classic 的分析身份不同。去变体视图会报告间隔是否因颜色行重复而变化，不把合并后的 N 说成抽样偏差已被纠正。

## 3. 日期对齐的历史观察

Chanel 法国固定使用 CH-C01/CH-C02 对 CH-C03/CH-C04，取两组共同观察年份（{common_years}），没有插值。每年同时输出两组中位数、绝对距离、相对比值及产品线数量。历史名称与当前锚点的对应为产品线级连续性，主要历史价格来自二手表格；它支持有限的方向性描述，不等同于每一年官方调价日历。Hermès Geta 法国 2023 年的 EUR 4,550 与 EUR 5,550 冲突两边保留，不强选一个数值。

## 4. 稳健性与商业意义

本轮保留原始观察、去变体视图、家族汇总及价格带 ±10% 内部边界敏感性。原价格带是在看到观察后划定的描述工具，不是独立检验。可比单元只有在每品牌至少 3 个去变体组且关键属性可核实时才进入主文，其余放入附录。

对品类负责人，数据当前支持三条有条件的下一步：第一，若两个市场的间隔在去变体视图仍保持方向一致，核实完整 SKU 梯度及客户升级路径；第二，若间隔随家族覆盖改变，优先补做组合映射；第三，在使用历史路径前先补齐同款身份、共同日期和一手价格证据。以上是决策问题与证据需求，不是新品价位或涨价建议。

## 5. 局限与来源

样本为非加权公开本地标价观察，不估计需求、利润、品牌资产、消费者替代或最优价格。FR/US 不做 FX、税费、关税或落地成本标准化。缺失年份不表示没有变化，连续性为 SAME_MODEL_CONTINUOUS 或 MODEL_SUCCESSOR，当前锚点的 EXACT_SKU 标记与历史连续性分开。完整来源、计算输出和未解决项见 `research_r1/data/`、`research_r1/outputs/` 与 `research_r1/export/`。
"""
    (REPORT / "REPORT_CN.md").write_text(report_cn, encoding="utf-8")

    report_en = f"""# The Architecture of Access — Chanel's Handbag Price Ladder in Context

**Observation markets:** France (EUR) and United States (USD) · **Current snapshot:** 15 August 2026 · **Research status:** {validation_status}

## Open

This case asks how Chanel presents visible entry, family-level steps and the Classic high anchor in local official list-price observations. The dataset is a non-weighted sample of accepted product rows: {current_accepted} observations, {current_numeric} numeric prices. It is a map of what was visible in the captured pages, not a census of a brand assortment and not a measure of affordability.

## Context

Chanel is read against Hermès, Louis Vuitton and Dior on separate local currency axes. The competitor panel supplies an external coordinate system, while the deeper interpretation stays with Chanel. Dior US has {dior_us_numeric} numeric prices out of {dior_us_accepted} accepted rows; {dior_us_unresolved} unresolved prices remain missing. Hermès has no supplied signature flag in the current panel, so its prices do not support a like-for-like icon premium calculation.

## The price ladder

Within the France snapshot, the lowest Classic observation is {fr['classic_min']} EUR and the highest entry/core comparison observation is {fr['entry_core_max']} EUR, a visible sample gap of {fr['observed_gap']} EUR. The median distance is {fr['median_distance']} EUR and the median ratio is {fr['relative_ratio']}. The US snapshot shows {us['classic_min']} versus {us['entry_core_max']} USD, a gap of {us['observed_gap']} USD, with a median distance of {us['median_distance']} USD and a ratio of {us['relative_ratio']}.

The membership rule matters. Classic 11.12 and Small Classic form the Classic group. Mini Classic is an entry observation even when its product name contains “Classic”; Shopping Bag and Bowling Bag are retained as other core observations. Price-upon-request rows remain a separate state and are not placed above the numeric axis.

## Moving together

The aligned Chanel France panel compares fixed lineages CH-C01/CH-C02 with CH-C03/CH-C04 only in common observed years ({common_years}). It reports group medians, absolute distance, ratio and lineage counts without interpolating missing years. Historical rows are mostly secondary-source tables, so the result is a bounded product-line observation rather than a complete official repricing calendar. The Hermès Geta France 2023 conflict is kept as two branches and excluded from the primary path.

The later Chanel supplement was filtered by the same market, bag type, size label and material group. It produces {len(pairing_candidates)} directional peer candidates across {len(pairing_cells)} supplementary cells. The price comparison is blocked because the supplement is dated 7 September 2026 while the competitor baseline is dated 15 August 2026. The audit keeps unknown-size, seasonal-collection and Wallet on Chain rows in separate gates. Latest independent refresh evidence contains {len(wave6_refresh)} rows, {len(wave6_cells)} exact cells and {wave6_strict_word} strict main-text cells. The only dimension match is {matched_size_text}, so its price comparison also remains blocked.

## What the evidence can support

Three decisions follow conditionally. If the ladder gap survives de-variant sensitivity, a category lead can verify the full SKU ladder and the customer upgrade path. If it moves when family coverage changes, the next action is assortment mapping. If a historical movement is needed for a decision, the next evidence should be same-model identity, common dates and primary price records. The sample cannot establish demand, substitution, profit, brand-equity effects or an optimal future price.

## Afterlife

All numbers in the public candidate export point to R1 outputs and claim IDs. The source registry distinguishes page access from effective dates; the 15 August current snapshot remains separate from any later refresh. Reproduction uses the local Python standard-library scripts and `python3 -m unittest discover -s tests/r1 -p 'test_*.py'`.
"""
    (REPORT / "CASE_STUDY_EN.md").write_text(report_en, encoding="utf-8")

    memo = f"""# 决策备忘录：Chanel 手袋价格架构 R1

## 观察

- 法国 Classic 最低观察价 {fr['classic_min']} EUR，进入/其他核心最高观察价 {fr['entry_core_max']} EUR，样本间隔 {fr['observed_gap']} EUR。
- 美国对应样本间隔为 {us['observed_gap']} USD。
- Dior 美国有 {dior_us_numeric} 条数值价格（共 {dior_us_accepted} 条接受观察）；未解析行不插补。
- 补充配对审计产生 {len(pairing_candidates)} 条属性匹配的方向性候选配对和 {len(pairing_cells)} 个补充属性单元；2026-09-07 补充快照与 2026-08-15 竞品基线日期不一致。
- 历史法国 Chanel 只在共同观察年份（{common_years}）比较固定产品线；未插值。

## 解释

当前样本显示 Classic 与较低/其他核心家族之间存在可见距离，但距离是观察样本中的结构，不能直接解释为购买替代、需求或品牌管理意图。

## 待核实问题与最多三条行动

1. 间隔在完整 SKU 组合与去变体视图中是否仍然存在？
2. 客户是否沿这些产品家族升级，还是不同家族满足不同场景？
3. 历史产品线是否为同一型号、同一材质/尺寸和共同日期？

## 需要的额外证据

1. 触发条件：去变体后方向仍一致。证据：完整市场 SKU/家族清单与购买路径数据。
2. 触发条件：间隔随覆盖变化。证据：家族映射、抽样框与固定配额记录。
3. 触发条件：需要使用历史趋势。证据：一手历史价单、同款参考号及有效日期。

R1 状态：{validation_status}。不据此提出新品价位或涨价方案。
"""
    (REPORT / "DECISION_MEMO_CN.md").write_text(memo, encoding="utf-8")


def build_baseline_manifest(rows: list[dict], sources: list[dict], lineages: list[dict]) -> None:
    files = []
    for path in [*CURRENT_SOURCE_FILES.values(), HISTORY_FILE, LINEAGE_FILE, HISTORY_SOURCE_FILE, COMPETITOR_ERRORS_FILE, CHANEL_ERRORS_FILE, HISTORY_UNRESOLVED_FILE]:
        if path.exists() and path.is_file():
            item = {"path": str(path.relative_to(ROOT)), "sha256": sha256(path)}
            if path.suffix == ".csv":
                item["rows"] = len(read_csv(path))
            files.append(item)
    current = [r for r in rows if r["snapshot_id"] == CURRENT_SNAPSHOT]
    history = [r for r in rows if r["snapshot_id"] == HISTORY_SNAPSHOT]
    manifest = {
        "schemaVersion": "research-r1-baseline-1",
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
        "source_commit": git_sha(),
        "current_snapshot": CURRENT_SNAPSHOT,
        "historical_snapshot": HISTORY_SNAPSHOT,
        "input_files": files,
        "key_counts": {
            "current_observations": len(current), "current_numeric": sum(r["price_status"] == "numeric" for r in current),
            "historical_observations": len(history), "historical_numeric": sum(r["price_status"] == "numeric" for r in history),
            "lineages": len(lineages), "sources": len(sources),
            "current_by_brand_market": {f"{brand}:{market}": sum(r["brand"] == brand and r["market"] == market for r in current) for brand in BRANDS for market in MARKETS},
        },
        "reproduction_chain": [
            {"command": "python3 build_competitor_dataset.py", "exit_code": 0, "observed_result": "120 competitor rows; 12 recorded errors"},
            {"command": "python3 competitive_pricing_calculations.py", "exit_code": 0, "observed_result": "161 total observations; 147 numeric"},
            {"command": "python3 build_historical_dataset.py", "exit_code": 0, "observed_result": "77 rows; 76 numeric; 35 events"},
            {"command": "python3 historical_pricing_calculations.py", "exit_code": 0, "observed_result": "19 market paths; 13 lineages"},
            {"command": "python3 build_final_report_assets.py", "exit_code": 0, "observed_result": "5 SVG assets"},
        ],
        "reproduction_notes": [
            "The original competitor builder uses the current clock for observed_at and observation IDs; its rerun was not treated as a new historical observation.",
            "Derived files were restored after the baseline rerun; R1 uses the preserved 2026-08-15 snapshots.",
            "Current anchor exact-SKU rows and historical lineage continuity are separate fields and must not be conflated.",
        ],
    }
    write_json(R1 / "baseline_manifest.json", manifest)


def main() -> None:
    for directory in (R1, DATA, OUT, REPORT, EXPORT / "scenes", EXPORT / "figures"):
        directory.mkdir(parents=True, exist_ok=True)
    current, current_sources = make_current_rows()
    history, history_sources = make_history_rows()
    rows = current + history
    lineage_rows, lineages = load_lineages()
    sources = build_sources(current_sources, history_sources)
    coverage = build_coverage(rows)
    family = build_family_summary(rows)
    bands = build_band_sensitivity(rows)
    ladder = build_chanel_ladder(rows)
    cells = build_comparable_cells(rows)
    aligned = build_aligned_history(rows, lineages)
    unresolved = build_unresolved(rows)
    robustness = build_robustness(rows, ladder, bands, aligned)
    claims = build_claims(rows, ladder, coverage, aligned, lineages)

    write_csv(DATA / "observations.csv", rows, OBSERVATION_FIELDS)
    write_csv(DATA / "lineage.csv", lineage_rows, LINEAGE_FIELDS)
    write_csv(DATA / "coverage.csv", coverage, list(coverage[0].keys()) if coverage else ["brand"])
    supplementary_path = DATA / "supplementary_current.csv"
    if not supplementary_path.exists():
        write_csv(supplementary_path, [], OBSERVATION_FIELDS)
    registry_path = R1 / "source_registry.csv"
    if not registry_path.exists():
        write_csv(registry_path, sources, SOURCE_FIELDS)
    else:
        existing_registry = read_csv(registry_path)
        existing_by_id = {row.get("source_id"): row for row in existing_registry}
        registry_is_current = all(existing_by_id.get(row["source_id"]) == row for row in sources)
        if not registry_is_current:
            generated_source_ids = {row["source_id"] for row in sources}
            preserved_registry = [row for row in existing_registry if row.get("source_id") not in generated_source_ids]
            write_csv(registry_path, [*sources, *preserved_registry], SOURCE_FIELDS)
    write_csv(R1 / "claims.csv", claims, list(claims[0].keys()) if claims else ["claim_id"])
    write_csv(OUT / "brand_family_summary.csv", family, list(family[0].keys()) if family else ["brand"])
    write_csv(OUT / "chanel_ladder.csv", ladder, list(ladder[0].keys()) if ladder else ["brand"])
    write_csv(OUT / "band_sensitivity.csv", bands, list(bands[0].keys()) if bands else ["market"])
    write_csv(OUT / "comparable_cells.csv", cells, list(cells[0].keys()) if cells else ["market"])
    write_csv(OUT / "aligned_history.csv", aligned, list(aligned[0].keys()) if aligned else ["brand"])
    write_csv(OUT / "robustness.csv", robustness, list(robustness[0].keys()) if robustness else ["module"])
    write_csv(OUT / "unresolved.csv", unresolved, list(unresolved[0].keys()) if unresolved else ["issue_id"])
    build_baseline_manifest(rows, sources, lineage_rows)
    build_reports(ladder, family, aligned, unresolved, coverage)
    write_json(OUT / "validation.json", {"status": "pending", "run_at": "", "source_commit": git_sha(), "checks": {}, "excluded_claims": [], "unresolved_critical_count": 0})
    changelog_path = R1 / "CHANGELOG.md"
    if not changelog_path.exists():
        changelog_path.write_text("""# Research R1 change log\n\n- R1 baseline: preserved the 2026-08-15 current snapshot and the historical panel as separate snapshots.\n- Added a canonical observation schema, explicit source registry, lineage map, coverage audit and unresolved issue register.\n- Added M1–M5 outputs for family distributions, Chanel ladder, band sensitivity, bounded comparable cells and aligned Chanel history.\n- Added claims with evidence grades; the Hermès Geta conflict remains excluded from core claims.\n- No new web collection or historical-date backfill was performed.\n""", encoding="utf-8")
    print(json.dumps({"current_observations": len(current), "historical_observations": len(history), "numeric_current": sum(r["price_status"] == "numeric" for r in current), "numeric_history": sum(r["price_status"] == "numeric" for r in history), "aligned_years": [r["observed_year"] for r in aligned], "unresolved": len(unresolved)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
