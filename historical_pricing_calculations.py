#!/usr/bin/env python3
"""Reproducible historical luxury-handbag pricing calculations.

This module is intentionally descriptive.  It preserves the historical
dataset's lineage and confidence fields and keeps same-model paths separate
from model-successor paths.  It does not interpolate missing years or make
strategic recommendations.
"""

from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "luxury_historical_pricing"
OUT = ROOT / "historical_pricing_calculations"

BRANDS = ["Chanel", "Hermès", "Louis Vuitton", "Dior"]
CURRENT_ANCHOR_DATE = "2026-08-15"
YEAR_ONLY_RE = re.compile(r"^(\d{4})$")
MONTH_RE = re.compile(r"^(\d{4})-(\d{2})$")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: "" if row.get(k) is None else row.get(k) for k in fieldnames})


def numeric(row: dict[str, str]) -> bool:
    try:
        float(row.get("price", ""))
        return row.get("price_status") == "numeric"
    except (TypeError, ValueError):
        return False


def price(row: dict[str, str]) -> float:
    return float(row["price"])


def is_current_anchor(row: dict[str, str]) -> bool:
    return row.get("observation_date") == CURRENT_ANCHOR_DATE and row.get("source_quality") == "HIGH"


def parse_sort_date(value: str) -> date:
    if YEAR_ONLY_RE.match(value):
        return date(int(value), 1, 1)
    if MONTH_RE.match(value):
        year, month = value.split("-")
        return date(int(year), int(month), 1)
    return date.fromisoformat(value)


def elapsed_years(start: str, end: str) -> float:
    """Elapsed years with a visible convention for year-only source dates."""
    if YEAR_ONLY_RE.match(start) and YEAR_ONLY_RE.match(end):
        return float(int(end) - int(start))
    return (parse_sort_date(end) - parse_sort_date(start)).days / 365.25


def fmt_num(value: float | None, places: int = 2) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return f"{value:.{places}f}"


def pct_change(start: float, end: float) -> float:
    return end / start - 1.0


def q(values: list[float], p: float) -> float | None:
    if not values:
        return None
    values = sorted(values)
    if len(values) == 1:
        return values[0]
    pos = (len(values) - 1) * p
    low = math.floor(pos)
    high = math.ceil(pos)
    if low == high:
        return values[low]
    return values[low] + (values[high] - values[low]) * (pos - low)


def confidence_mix(values: list[str]) -> str:
    order = ["HIGH", "MEDIUM", "LOW"]
    present = [v for v in order if v in set(values)]
    return "+".join(present) if present else ""


def lineage_class(lineage: dict[str, str]) -> str:
    return lineage["continuity_status"]


def event_is_conflict(row: dict[str, str]) -> bool:
    # The accepted event file does not carry conflict_flag, so preserve the
    # documented Hermès Geta conflict through its source registry identifier.
    return "SRC-HM-H01-LUXEFRONT-2022" in row.get("source_ids", "")


def event_is_current_transition(row: dict[str, str]) -> bool:
    return row.get("new_observation_date") == CURRENT_ANCHOR_DATE


def build_paths(observations: list[dict[str, str]], lineages: dict[str, dict[str, str]], events: list[dict[str, str]]) -> list[dict[str, object]]:
    numeric_rows = [r for r in observations if numeric(r)]
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in numeric_rows:
        grouped[(row["product_lineage_id"], row["market"])].append(row)

    events_by_group: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for event in events:
        events_by_group[(event["product_lineage_id"], event["market"])].append(event)

    out: list[dict[str, object]] = []
    for (lineage_id, market), rows in sorted(grouped.items()):
        lineage = lineages[lineage_id]
        all_rows = sorted(rows, key=lambda r: (parse_sort_date(r["observation_date"]), r["observation_id"]))
        conflict_rows = [r for r in all_rows if r.get("conflict_flag") == "true"]
        primary_rows = [r for r in all_rows if r.get("conflict_flag") != "true"]
        if len(primary_rows) < 2:
            continue
        first, last = primary_rows[0], primary_rows[-1]
        years = elapsed_years(first["observation_date"], last["observation_date"])
        group_events = events_by_group.get((lineage_id, market), [])
        positive_events = [e for e in group_events if float(e["percentage_change"]) > 0]
        non_conflict_events = [e for e in positive_events if not event_is_conflict(e)]
        source_conf = confidence_mix([r["confidence"] for r in primary_rows])
        path_scope = lineage_class(lineage)
        calc_conf = "MEDIUM" if path_scope == "SAME_MODEL_CONTINUOUS" else "MEDIUM-LOW"
        out.append(
            {
                "brand": lineage["brand"],
                "product_lineage_id": lineage_id,
                "product_family": lineage["product_family"],
                "market": market,
                "currency": first["currency"],
                "lineage_continuity_status": path_scope,
                "calculation_scope": "same_model_comparable" if path_scope == "SAME_MODEL_CONTINUOUS" else "successor_directional",
                "earliest_observation": first["observation_date"],
                "earliest_price": fmt_num(price(first), 2),
                "latest_observation": last["observation_date"],
                "latest_price": fmt_num(price(last), 2),
                "n_numeric_observations": len(primary_rows),
                "n_conflict_rows_excluded": len(conflict_rows),
                "elapsed_years": fmt_num(years, 3),
                "absolute_change": fmt_num(price(last) - price(first), 2),
                "cumulative_change_pct": fmt_num(pct_change(price(first), price(last)) * 100, 2),
                "n_event_rows_in_file": len(group_events),
                "n_positive_event_rows": len(positive_events),
                "n_non_conflict_positive_event_rows": len(non_conflict_events),
                "source_confidence_mix": source_conf,
                "calculation_confidence": calc_conf,
                "headline_use": "headline_eligible" if path_scope == "SAME_MODEL_CONTINUOUS" and not conflict_rows else "directional_or_sensitivity_only",
                "lineage_note": lineage["notes"],
            }
        )
    return out


def build_cagr(paths: list[dict[str, object]]) -> list[dict[str, object]]:
    out = []
    for row in paths:
        years = float(row["elapsed_years"])
        start = float(row["earliest_price"])
        end = float(row["latest_price"])
        if years <= 0 or start <= 0:
            continue
        cagr = (end / start) ** (1 / years) - 1
        out.append(
            {
                "brand": row["brand"],
                "product_lineage_id": row["product_lineage_id"],
                "product_family": row["product_family"],
                "market": row["market"],
                "currency": row["currency"],
                "lineage_continuity_status": row["lineage_continuity_status"],
                "cagr_status": "comparable_cagr" if row["lineage_continuity_status"] == "SAME_MODEL_CONTINUOUS" else "directional_cagr",
                "earliest_observation": row["earliest_observation"],
                "latest_observation": row["latest_observation"],
                "n_numeric_observations": row["n_numeric_observations"],
                "elapsed_years": row["elapsed_years"],
                "earliest_price": row["earliest_price"],
                "latest_price": row["latest_price"],
                "cagr_pct": fmt_num(cagr * 100, 2),
                "source_confidence_mix": row["source_confidence_mix"],
                "calculation_confidence": row["calculation_confidence"],
                "year_only_date_convention": "YYYY-to-YYYY uses calendar-year difference; otherwise date difference / 365.25.",
            }
        )
    return out


def build_event_summary(events: list[dict[str, str]], lineages: dict[str, dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for event in events:
        grouped[event["brand"]].append(event)
    out = []
    for brand in BRANDS:
        rows = grouped.get(brand, [])
        positive = [r for r in rows if float(r["percentage_change"]) > 0]
        positive_nonconflict = [r for r in positive if not event_is_conflict(r)]
        positive_noncurrent = [r for r in positive if not event_is_current_transition(r)]
        positive_noncurrent_nonconflict = [r for r in positive_noncurrent if not event_is_conflict(r)]
        intervals = [elapsed_years(r["prior_observation_date"], r["new_observation_date"]) for r in rows]
        pos_by_lineage = Counter(r["product_lineage_id"] for r in positive)
        event_years = sorted({r["new_observation_date"][:4] for r in rows})
        lineage_ids = sorted({r["product_lineage_id"] for r in rows})
        top_share = max(pos_by_lineage.values()) / len(positive) if positive else None
        # Median/range are deliberately shown in both raw-file and sensitivity form:
        # current-anchor transitions and conflict-derived rows are not equivalent to
        # observed within-history repricing events.
        vals = [float(r["percentage_change"]) for r in positive]
        vals_sens = [float(r["percentage_change"]) for r in positive_noncurrent_nonconflict]
        out.append(
            {
                "brand": brand,
                "event_rows_in_file": len(rows),
                "positive_increase_rows": len(positive),
                "zero_change_intervals": sum(float(r["percentage_change"]) == 0 for r in rows),
                "conflict_derived_rows": sum(event_is_conflict(r) for r in rows),
                "current_anchor_transition_rows": sum(event_is_current_transition(r) for r in rows),
                "lineages_with_positive_events": len(pos_by_lineage),
                "lineages_with_any_event": len(lineage_ids),
                "positive_event_lineage_coverage": fmt_num(len(pos_by_lineage) / len(lineage_ids) * 100, 1) if lineage_ids else "",
                "top_lineage_share_of_positive_events": fmt_num(top_share * 100, 1) if top_share is not None else "",
                "median_single_event_pct_all_positive": fmt_num(median(vals), 2) if vals else "",
                "median_single_event_pct_excluding_current_and_conflict": fmt_num(median(vals_sens), 2) if vals_sens else "",
                "min_single_event_pct_all_positive": fmt_num(min(vals), 2) if vals else "",
                "max_single_event_pct_all_positive": fmt_num(max(vals), 2) if vals else "",
                "p25_single_event_pct_all_positive": fmt_num(q(vals, 0.25), 2) if vals else "",
                "p75_single_event_pct_all_positive": fmt_num(q(vals, 0.75), 2) if vals else "",
                "median_observation_interval_years": fmt_num(median(intervals), 2) if intervals else "",
                "event_observation_years": ";".join(event_years),
                "event_lineage_counts": ";".join(f"{k}:{v}" for k, v in sorted(pos_by_lineage.items())),
                "event_strength_mix": ";".join(f"{k}:{v}" for k, v in sorted(Counter(r["evidence_strength"] for r in rows).items())),
                "interpretation_boundary": "Observed event frequency only; missing years do not imply no price change.",
            }
        )
    return out


def build_icon_core(observations: list[dict[str, str]], lineages: dict[str, dict[str, str]]) -> list[dict[str, object]]:
    # Only Chanel has a defensible, aligned icon/access taxonomy in the accepted
    # historical panel.  The two icon and two access Mini Classic lineages are
    # compared at common observed dates without interpolation.
    chanel = [r for r in observations if r["brand"] == "Chanel" and r["market"] == "FR" and numeric(r) and r.get("conflict_flag") != "true"]
    icon_ids = {k for k, v in lineages.items() if v["brand"] == "Chanel" and v["product_role"] == "signature_icon"} if "product_role" in next(iter(lineages.values()), {}) else {"CH-C01", "CH-C02"}
    # product_role lives in the observation file, not the lineage file.  Keep the
    # explicit lineage set auditable and stable.
    icon_ids = {"CH-C01", "CH-C02"}
    access_ids = {"CH-C03", "CH-C04"}
    by_year_role: dict[tuple[str, str], list[float]] = defaultdict(list)
    by_year_ids: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in chanel:
        year = row["observation_date"][:4]
        role = "icon" if row["product_lineage_id"] in icon_ids else "access_core" if row["product_lineage_id"] in access_ids else "other"
        if role == "other":
            continue
        by_year_role[(year, role)].append(price(row))
        by_year_ids[(year, role)].add(row["product_lineage_id"])

    rows = []
    for year in sorted({key[0] for key in by_year_role}):
        if (year, "icon") not in by_year_role or (year, "access_core") not in by_year_role:
            continue
        icon_med = median(by_year_role[(year, "icon")])
        core_med = median(by_year_role[(year, "access_core")])
        rows.append(
            {
                "brand": "Chanel",
                "market": "FR",
                "currency": "EUR",
                "observed_year": year,
                "icon_lineages": ";".join(sorted(by_year_ids[(year, "icon")])),
                "access_core_lineages": ";".join(sorted(by_year_ids[(year, "access_core")])),
                "icon_n_observations": len(by_year_role[(year, "icon")]),
                "access_core_n_observations": len(by_year_role[(year, "access_core")]),
                "icon_median": fmt_num(icon_med, 2),
                "access_core_median": fmt_num(core_med, 2),
                "icon_core_ratio": fmt_num(icon_med / core_med, 3),
                "absolute_gap": fmt_num(icon_med - core_med, 2),
                "confidence": "MEDIUM",
                "calculation_note": "Common observed years only; no interpolation. This is a narrow Chanel France icon/access comparison, not a four-brand icon taxonomy.",
            }
        )
    base = next((r for r in rows if r["observed_year"] == "2022"), None)
    if base:
        base_icon = float(base["icon_median"])
        base_core = float(base["access_core_median"])
        for row in rows:
            row["icon_index_2022_100"] = fmt_num(float(row["icon_median"]) / base_icon * 100, 2)
            row["access_core_index_2022_100"] = fmt_num(float(row["access_core_median"]) / base_core * 100, 2)
    return rows


def build_ladder(observations: list[dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in observations:
        if numeric(row) and row.get("conflict_flag") != "true":
            grouped[(row["brand"], row["market"], row["currency"], row["observation_date"][:4],)].append(row)
    rows = []
    for (brand, market, currency, year), group in sorted(grouped.items()):
        role_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in group:
            role_groups[row["product_role"]].append(row)
        for role, role_rows in sorted(role_groups.items()):
            rows.append(
                {
                    "brand": brand,
                    "market": market,
                    "currency": currency,
                    "observed_year": year,
                    "observed_product_role": role,
                    "n_observations": len(role_rows),
                    "n_lineages": len({r["product_lineage_id"] for r in role_rows}),
                    "lineages": ";".join(sorted({r["product_lineage_id"] for r in role_rows})),
                    "median_price": fmt_num(median([price(r) for r in role_rows]), 2),
                    "min_price": fmt_num(min(price(r) for r in role_rows), 2),
                    "max_price": fmt_num(max(price(r) for r in role_rows), 2),
                    "confidence": "MEDIUM" if any(not is_current_anchor(r) for r in role_rows) else "HIGH",
                    "calculation_note": "Observed role medians; missing years are not interpolated and roles are not assumed to be equivalent across brands.",
                }
            )
    return rows


def build_readiness(observations: list[dict[str, str]], lineages: dict[str, dict[str, str]], events: list[dict[str, str]], unresolved: list[dict[str, object]]) -> list[dict[str, object]]:
    unresolved_by_brand = Counter(str(r.get("brand", "")) for r in unresolved)
    rows = []
    for brand in BRANDS:
        brand_rows = [r for r in observations if r["brand"] == brand]
        numeric_rows = [r for r in brand_rows if numeric(r)]
        hist_rows = [r for r in brand_rows if not is_current_anchor(r)]
        hist_numeric = [r for r in hist_rows if numeric(r)]
        brand_lineages = [v for v in lineages.values() if v["brand"] == brand]
        # Include current anchors in coverage years.  A current 2026 anchor is
        # an observed endpoint even when the non-current historical subset has
        # no earlier observation in that year.
        years = sorted({r["observation_date"][:4] for r in brand_rows if r.get("observation_date")})
        observed_year_ints = {int(y) for y in years if y.isdigit()}
        requested_years = set(range(2020, 2027))
        missing_years = sorted(requested_years - observed_year_ints)
        brand_events = [r for r in events if r["brand"] == brand]
        rows.append(
            {
                "brand": brand,
                "accepted_panel_observations_including_current_anchor": len(brand_rows),
                "numeric_panel_observations": len(numeric_rows),
                "noncurrent_historical_observations": len(hist_rows),
                "noncurrent_historical_numeric_observations": len(hist_numeric),
                "FR_observations": sum(r["market"] == "FR" for r in brand_rows),
                "US_observations": sum(r["market"] == "US" for r in brand_rows),
                "years_covered_in_panel": ";".join(sorted({r["observation_date"][:4] for r in brand_rows})),
                "missing_years_2020_2026": ";".join(str(y) for y in missing_years),
                "lineages": len(brand_lineages),
                "SAME_MODEL_CONTINUOUS_lineages": sum(lineage_class(v) == "SAME_MODEL_CONTINUOUS" for v in brand_lineages),
                "MODEL_SUCCESSOR_lineages": sum(lineage_class(v) == "MODEL_SUCCESSOR" for v in brand_lineages),
                "source_confidence_mix_all_panel_rows": ";".join(f"{k}:{v}" for k, v in sorted(Counter(r["confidence"] for r in brand_rows).items())),
                "source_quality_mix_all_panel_rows": ";".join(f"{k}:{v}" for k, v in sorted(Counter(r["source_quality"] for r in brand_rows).items())),
                "conflict_rows": sum(r.get("conflict_flag") == "true" for r in brand_rows),
                "event_rows_in_file": len(brand_events),
                "positive_event_rows": sum(float(r["percentage_change"]) > 0 for r in brand_events),
                "unresolved_candidates": unresolved_by_brand[brand],
                "readiness_boundary": "Observation coverage is not the same as comparable historical-series coverage; missing years are not zero changes.",
            }
        )
    return rows


def build_brand_summary(readiness: list[dict[str, object]], paths: list[dict[str, object]], cagr: list[dict[str, object]], events: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for base in readiness:
        brand = base["brand"]
        brand_paths = [p for p in paths if p["brand"] == brand]
        same = [p for p in brand_paths if p["lineage_continuity_status"] == "SAME_MODEL_CONTINUOUS"]
        successor = [p for p in brand_paths if p["lineage_continuity_status"] == "MODEL_SUCCESSOR"]
        same_changes = [float(p["cumulative_change_pct"]) for p in same]
        successor_changes = [float(p["cumulative_change_pct"]) for p in successor]
        same_cagr = [float(p["cagr_pct"]) for p in cagr if p["brand"] == brand and p["cagr_status"] == "comparable_cagr"]
        successor_cagr = [float(p["cagr_pct"]) for p in cagr if p["brand"] == brand and p["cagr_status"] == "directional_cagr"]
        rows.append(
            {
                "brand": brand,
                "accepted_panel_observations": base["accepted_panel_observations_including_current_anchor"],
                "noncurrent_historical_observations": base["noncurrent_historical_observations"],
                "numeric_panel_observations": base["numeric_panel_observations"],
                "lineages": base["lineages"],
                "same_model_lineages": base["SAME_MODEL_CONTINUOUS_lineages"],
                "successor_lineages": base["MODEL_SUCCESSOR_lineages"],
                "FR_observations": base["FR_observations"],
                "US_observations": base["US_observations"],
                "same_model_market_paths_with_2plus_observations": len(same),
                "successor_market_paths_with_2plus_observations": len(successor),
                "median_same_model_cumulative_change_pct": fmt_num(median(same_changes), 2) if same_changes else "",
                "median_successor_directional_change_pct": fmt_num(median(successor_changes), 2) if successor_changes else "",
                "median_same_model_cagr_pct": fmt_num(median(same_cagr), 2) if same_cagr else "",
                "median_successor_directional_cagr_pct": fmt_num(median(successor_cagr), 2) if successor_cagr else "",
                "event_rows": base["event_rows_in_file"],
                "positive_event_rows": base["positive_event_rows"],
                "conflict_rows": base["conflict_rows"],
                "unresolved_candidates": base["unresolved_candidates"],
                "brand_level_readiness": {
                    "Chanel": "READY WITH LIMITATIONS",
                    "Hermès": "NOT READY for broad brand-wide repricing; product-specific only",
                    "Louis Vuitton": "READY WITH LIMITATIONS",
                    "Dior": "READY WITH LIMITATIONS",
                }[brand],
            }
        )
    return rows


def build_chart_paths(observations: list[dict[str, str]], lineages: dict[str, dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in observations:
        if numeric(row) and row.get("conflict_flag") != "true":
            grouped[(row["product_lineage_id"], row["market"])].append(row)
    for (lineage_id, market), group in sorted(grouped.items()):
        group = sorted(group, key=lambda r: (parse_sort_date(r["observation_date"]), r["observation_id"]))
        base = price(group[0])
        lineage = lineages[lineage_id]
        for row in group:
            rows.append(
                {
                    "brand": row["brand"],
                    "product_lineage_id": lineage_id,
                    "product_family": row["product_family"],
                    "market": market,
                    "currency": row["currency"],
                    "observation_date": row["observation_date"],
                    "price": fmt_num(price(row), 2),
                    "index_base_earliest_observation_100": fmt_num(price(row) / base * 100, 2),
                    "lineage_continuity_status": lineage["continuity_status"],
                    "current_anchor_flag": "TRUE" if is_current_anchor(row) else "FALSE",
                    "confidence": row["confidence"],
                    "chart_use": "comparable_path" if lineage["continuity_status"] == "SAME_MODEL_CONTINUOUS" else "directional_successor_path",
                }
            )
    return rows


def main() -> None:
    OUT.mkdir(exist_ok=True)
    observations = read_csv(DATA / "clean" / "historical_pricing_clean.csv")
    lineage_rows = read_csv(DATA / "lineage" / "product_lineage.csv")
    event_rows = read_csv(DATA / "events" / "price_change_events.csv")
    lineages = {r["product_lineage_id"]: r for r in lineage_rows}
    unresolved = []
    unresolved_path = DATA / "errors" / "unresolved_history.jsonl"
    with unresolved_path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                unresolved.append(json.loads(line))

    paths = build_paths(observations, lineages, event_rows)
    cagr = build_cagr(paths)
    readiness = build_readiness(observations, lineages, event_rows, unresolved)
    event_summary = build_event_summary(event_rows, lineages)
    icon_core = build_icon_core(observations, lineages)
    ladder = build_ladder(observations)
    brand_summary = build_brand_summary(readiness, paths, cagr, event_rows)
    chart_paths = build_chart_paths(observations, lineages)

    write_csv(
        OUT / "historical_data_readiness.csv",
        readiness,
        list(readiness[0].keys()),
    )
    write_csv(
        OUT / "lineage_price_paths.csv",
        paths,
        [
            "brand", "product_lineage_id", "product_family", "market", "currency",
            "lineage_continuity_status", "calculation_scope", "earliest_observation",
            "earliest_price", "latest_observation", "latest_price", "n_numeric_observations",
            "n_conflict_rows_excluded", "elapsed_years", "absolute_change", "cumulative_change_pct",
            "n_event_rows_in_file", "n_positive_event_rows", "n_non_conflict_positive_event_rows",
            "source_confidence_mix", "calculation_confidence", "headline_use", "lineage_note",
        ],
    )
    write_csv(
        OUT / "cumulative_price_changes.csv",
        paths,
        [
            "brand", "product_lineage_id", "product_family", "market", "currency",
            "lineage_continuity_status", "calculation_scope", "earliest_observation",
            "earliest_price", "latest_observation", "latest_price", "n_numeric_observations",
            "elapsed_years", "absolute_change", "cumulative_change_pct", "source_confidence_mix",
            "calculation_confidence", "headline_use",
        ],
    )
    write_csv(
        OUT / "historical_cagr.csv",
        cagr,
        [
            "brand", "product_lineage_id", "product_family", "market", "currency",
            "lineage_continuity_status", "cagr_status", "earliest_observation", "latest_observation",
            "n_numeric_observations", "elapsed_years", "earliest_price", "latest_price", "cagr_pct",
            "source_confidence_mix", "calculation_confidence", "year_only_date_convention",
        ],
    )
    write_csv(
        OUT / "price_change_event_summary.csv",
        event_summary,
        list(event_summary[0].keys()),
    )
    write_csv(
        OUT / "icon_core_evolution.csv",
        icon_core,
        [
            "brand", "market", "currency", "observed_year", "icon_lineages", "access_core_lineages",
            "icon_n_observations", "access_core_n_observations", "icon_median", "access_core_median",
            "icon_core_ratio", "absolute_gap", "icon_index_2022_100", "access_core_index_2022_100",
            "confidence", "calculation_note",
        ],
    )
    write_csv(
        OUT / "price_ladder_evolution.csv",
        ladder,
        [
            "brand", "market", "currency", "observed_year", "observed_product_role", "n_observations",
            "n_lineages", "lineages", "median_price", "min_price", "max_price", "confidence", "calculation_note",
        ],
    )
    write_csv(
        OUT / "brand_historical_summary.csv",
        brand_summary,
        list(brand_summary[0].keys()),
    )
    write_csv(
        OUT / "chart_representative_price_evolution.csv",
        chart_paths,
        list(chart_paths[0].keys()),
    )

    run_summary = {
        "input_observations": len(observations),
        "input_numeric_observations": sum(numeric(r) for r in observations),
        "input_lineages": len(lineages),
        "same_model_continuous_lineages": sum(lineage_class(r) == "SAME_MODEL_CONTINUOUS" for r in lineages.values()),
        "model_successor_lineages": sum(lineage_class(r) == "MODEL_SUCCESSOR" for r in lineages.values()),
        "input_event_rows": len(event_rows),
        "output_market_paths": len(paths),
        "output_cagr_rows": len(cagr),
        "unresolved_candidates": len(unresolved),
        "conflict_observation_rows": sum(r.get("conflict_flag") == "true" for r in observations),
        "calculation_notes": [
            "No missing years were interpolated.",
            "SAME_MODEL_CONTINUOUS and MODEL_SUCCESSOR paths remain separate.",
            "Conflict observations are excluded from primary path calculations and retained in readiness/event sensitivity fields.",
            "Current 2026 anchors are included as current endpoint observations; successor paths are directional only.",
        ],
    }
    (OUT / "run_summary.json").write_text(json.dumps(run_summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
