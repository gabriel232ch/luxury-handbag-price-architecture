#!/usr/bin/env python3
"""Build a same-date US cross-brand pairing audit.

This audit is intentionally separate from the historical R1 outputs.  It uses
only the 2026-09-07 US refresh, joins verified competitor product attributes,
and infers only conservative Chanel taxonomy from the visible product name and
material.  Explicit seasonal, WOC/small-leather-goods and unknown-size rows are
kept in the audit but cannot enter the headline cells.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "research_r1/data"
OUTPUT = ROOT / "research_r1/outputs"
LIVE_REFRESH = DATA / "live_refresh_2026-09-07_us.csv"
COMPETITOR_MASTER = DATA / "product_master_competitors_2026-09-07_us.csv"
SEASONAL_OVERRIDES = DATA / "seasonal_tote_attribute_overrides_2026-09-07_us.csv"
SNAPSHOT_ID = "refresh_2026-09-07_us"
SOURCE_DATE = "2026-09-07"
MINIMUM_PER_BRAND = 2


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_seasonal_overrides(path: Path = SEASONAL_OVERRIDES) -> dict[str, dict[str, str]]:
    """Read verified seasonal labels without altering the raw live snapshot."""
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {row["reference_code"]: row for row in rows}


def material_group(material: str) -> str:
    value = (material or "").lower()
    has_textile = any(token in value for token in ("canvas", "silk", "wool", "tweed", "technical fabric"))
    has_leather = any(
        token in value
        for token in (
            "leather",
            "calfskin",
            "goatskin",
            "cowhide",
            "lambskin",
            "swift",
            "epsom",
            "togo",
            "negonda",
            "evercolor",
            "clemence",
            "box calfskin",
            "chamkila",
        )
    )
    if has_textile and has_leather:
        return "mixed_textile_leather"
    if has_textile:
        return "textile"
    if has_leather:
        return "leather"
    return "unknown"


def classify_chanel_row(row: dict[str, str], seasonal_overrides: dict[str, dict[str, str]] | None = None) -> dict[str, str]:
    """Infer a bounded taxonomy for a Chanel live-refresh row."""
    name = row.get("product_name", "")
    lower = name.lower()
    if "shopping" in lower or "bowling" in lower:
        # Match the existing R1 taxonomy, where Shopping/Bowling are ``tote``.
        bag_type = "tote"
    elif "flap" in lower or "classic" in lower:
        bag_type = "flap"
    elif "backpack" in lower:
        bag_type = "backpack"
    elif "hobo" in lower:
        bag_type = "hobo"
    elif "bucket" in lower:
        bag_type = "bucket"
    else:
        bag_type = "unknown"

    if "maxi" in lower:
        size_label = "maxi"
    elif "large" in lower:
        size_label = "large"
    elif "small" in lower:
        size_label = "small"
    elif "mini" in lower:
        size_label = "mini"
    else:
        size_label = "unknown"

    if "chanel 25" in lower:
        family = "Chanel 25"
    elif "classic" in lower:
        family = "Classic"
    elif "flap" in lower:
        family = "Flap"
    elif "shopping" in lower:
        family = "Shopping"
    elif "backpack" in lower:
        family = "Backpack"
    elif "hobo" in lower:
        family = "Hobo"
    elif "bucket" in lower:
        family = "Bucket"
    elif "bowling" in lower:
        family = "Bowling"
    else:
        family = "Unknown"

    reasons: list[str] = []
    if "woc" in lower or "wallet on chain" in lower:
        reasons.append("woc_or_small_leather_goods")
    if size_label == "unknown":
        reasons.append("size_label_unknown")
    override = (seasonal_overrides or {}).get(row.get("reference_code", ""))
    if override:
        reasons.append("explicit_seasonal_collection")
        regular_special = override["regular_special"]
        collection_label = override.get("collection_label", "")
    else:
        reasons.append("regular_special_not_disclosed")
        regular_special = "not_disclosed"
        collection_label = ""
    if "woc_or_small_leather_goods" in reasons:
        scope_status = "sensitivity_only"
    elif "explicit_seasonal_collection" in reasons:
        scope_status = "seasonal_excluded"
    elif size_label == "unknown":
        scope_status = "unknown_size"
    else:
        scope_status = "status_pending"

    return {
        "family": family,
        "model": name,
        "size_label": size_label,
        "use_tag": bag_type,
        "bag_type": bag_type,
        "material_group": material_group(row.get("material_raw", "")),
        "material_raw": row.get("material_raw", ""),
        "dimensions_cm": "",
        "regular_special": regular_special,
        "collection_label": collection_label,
        "scope_status": scope_status,
        "isolation_reason": ";".join(reasons),
        "pairing_readiness": "blocked" if scope_status != "status_pending" else "conditional_regular_special_review",
        "dimension_status": "unknown",
    }


def classify_competitor_row(row: dict[str, str]) -> dict[str, str]:
    reasons: list[str] = []
    if row["bag_type"] == "small_leather_goods" or row["use_tag"] == "small-leather-goods":
        reasons.append("woc_or_small_leather_goods")
    if row["regular_special"] == "seasonal_collection":
        reasons.append("explicit_seasonal_collection")
    if row["size_label"] == "unknown":
        reasons.append("size_label_unknown")
    if row["regular_special"] == "not_disclosed":
        reasons.append("regular_special_not_disclosed")

    if "woc_or_small_leather_goods" in reasons:
        scope_status = "sensitivity_only"
    elif "explicit_seasonal_collection" in reasons:
        scope_status = "seasonal_excluded"
    elif "size_label_unknown" in reasons:
        scope_status = "unknown_size"
    else:
        scope_status = "status_pending"

    return {
        "family": row["family"],
        "model": row["model"],
        "size_label": row["size_label"],
        "use_tag": row["use_tag"],
        "bag_type": row["bag_type"],
        "material_group": row["material_group"],
        "material_raw": row["material_raw"],
        "dimensions_cm": row["dimensions_cm"],
        "regular_special": row["regular_special"],
        "collection_label": "",
        "scope_status": scope_status,
        "isolation_reason": ";".join(reasons),
        "pairing_readiness": "blocked" if scope_status != "status_pending" else "conditional_regular_special_review",
        "dimension_status": "numeric" if row["dimensions_cm"].strip() else "unknown",
    }


def numeric_price(row: dict[str, str]) -> float | None:
    if row.get("price_status", "numeric") != "numeric":
        return None
    try:
        return float(row["price"])
    except (TypeError, ValueError):
        return None


def gate_cell(rows: list[dict[str, str]], minimum_per_brand: int = MINIMUM_PER_BRAND) -> dict[str, str | bool]:
    """Apply the headline cell gates without relaxing unknown attributes."""
    if any(row.get("scope_status") == "sensitivity_only" for row in rows):
        return {"headline_eligible": False, "pairing_status": "blocked_woc_sensitivity_only", "limitation": "WOC/small leather goods remain sensitivity-only."}
    if any(row.get("scope_status") == "seasonal_excluded" for row in rows):
        return {"headline_eligible": False, "pairing_status": "blocked_seasonal_excluded", "limitation": "Explicit seasonal rows remain outside the regular-core headline."}
    if any(row.get("size_label") == "unknown" or row.get("scope_status") == "unknown_size" for row in rows):
        return {"headline_eligible": False, "pairing_status": "blocked_unknown_size", "limitation": "Unknown size cannot support like-for-like pairing."}
    if any(row.get("bag_type") == "unknown" for row in rows):
        return {"headline_eligible": False, "pairing_status": "blocked_unknown_bag_type", "limitation": "Unknown bag type cannot support like-for-like pairing."}
    if any(row.get("material_group") == "unknown" for row in rows):
        return {"headline_eligible": False, "pairing_status": "blocked_unknown_material", "limitation": "Unknown material group cannot support like-for-like pairing."}

    numeric_rows = [row for row in rows if numeric_price(row) is not None]
    brands = Counter(row["brand"] for row in numeric_rows)
    if "Chanel" not in brands:
        return {"headline_eligible": False, "pairing_status": "blocked_no_chanel_subject", "limitation": "The R1 headline subject is Chanel; competitor-only cells remain contextual."}
    if len(brands) < 2:
        return {"headline_eligible": False, "pairing_status": "blocked_no_cross_brand_peer", "limitation": "No second brand shares the exact attribute cell."}
    if any(count < minimum_per_brand for count in brands.values()):
        return {"headline_eligible": False, "pairing_status": "blocked_sample_insufficient", "limitation": f"Each brand needs at least {minimum_per_brand} numeric rows in the cell."}

    status_caveat = "regular_special_not_disclosed" if any(row.get("regular_special") == "not_disclosed" for row in rows) else ""
    limitation = "Exact same-date attribute cell; regular/seasonal marker remains undisclosed." if status_caveat else "Exact same-date attribute cell."
    return {"headline_eligible": True, "pairing_status": "same_date_exact_attributes", "limitation": limitation}


def enrich_panel(
    live_rows: list[dict[str, str]],
    competitor_rows: list[dict[str, str]],
    seasonal_overrides: dict[str, dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    competitors = {(row["brand"], row["canonical_reference"]): row for row in competitor_rows}
    panel: list[dict[str, str]] = []
    for source in live_rows:
        if source["source_effective_date"] != SOURCE_DATE or source["market"] != "US":
            continue
        if source["brand"] == "Chanel":
            attrs = classify_chanel_row(source, seasonal_overrides)
            source_url = source["source_url"]
        else:
            master = competitors[(source["brand"], source["reference_code"])]
            attrs = classify_competitor_row(master)
            source_url = master["source_url_us"] or source["source_url"]
        panel.append(
            {
                "snapshot_id": source["snapshot_id"],
                "source_effective_date": source["source_effective_date"],
                "brand": source["brand"],
                "market": source["market"],
                "currency": source["currency"],
                "reference_code": source["reference_code"],
                "product_name": source["product_name"],
                "price_status": source["price_status"],
                "price": source["price"],
                "source_url": source_url,
                **attrs,
            }
        )
    return panel


def group_id(row: dict[str, str]) -> str:
    return "|".join((row["market"], row["bag_type"], row["size_label"], row["material_group"]))


def fmt_number(value: float) -> str:
    return f"{value:.1f}".rstrip("0").rstrip(".")


def main() -> None:
    live_rows = read_csv(LIVE_REFRESH)
    competitor_rows = read_csv(COMPETITOR_MASTER)
    seasonal_overrides = read_seasonal_overrides()
    panel = enrich_panel(live_rows, competitor_rows, seasonal_overrides)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in panel:
        row["comparison_group_id"] = group_id(row)
        grouped[row["comparison_group_id"]].append(row)

    cell_rows: list[dict[str, str]] = []
    candidate_rows: list[dict[str, str]] = []
    for comparison_group_id, rows in sorted(grouped.items()):
        gate = gate_cell(rows)
        numeric_rows = [row for row in rows if numeric_price(row) is not None]
        brands = sorted({row["brand"] for row in numeric_rows})
        counts = Counter(row["brand"] for row in numeric_rows)
        medians = {brand: median([numeric_price(row) for row in numeric_rows if row["brand"] == brand]) for brand in brands}
        market, bag_type, size_label, material = comparison_group_id.split("|", 3)
        status_caveat = "regular_special_not_disclosed" if any(row["regular_special"] == "not_disclosed" for row in rows) else ""
        cell_id = "CELL-" + comparison_group_id.replace("|", "-")
        cell_rows.append(
            {
                "cell_id": cell_id,
                "market": market,
                "source_effective_date": SOURCE_DATE,
                "comparison_group_id": comparison_group_id,
                "bag_type": bag_type,
                "size_label": size_label,
                "material_group": material,
                "brands": ";".join(brands),
                "brand_counts": ";".join(f"{brand}:{counts[brand]}" for brand in brands),
                "brand_medians": ";".join(f"{brand}:{fmt_number(medians[brand])}" for brand in brands),
                "regular_special_status": status_caveat or "verified_regular",
                "headline_eligible": "TRUE" if gate["headline_eligible"] else "FALSE",
                "pairing_status": str(gate["pairing_status"]),
                "price_comparison_status": "computed" if gate["headline_eligible"] else "not_computed",
                "gate_reason": "" if gate["headline_eligible"] else str(gate["pairing_status"]),
                "limitation": str(gate["limitation"]),
            }
        )

        chanel_rows = [row for row in numeric_rows if row["brand"] == "Chanel"]
        peers = [row for row in numeric_rows if row["brand"] != "Chanel"]
        for chanel in sorted(chanel_rows, key=lambda row: row["reference_code"]):
            for peer in sorted(peers, key=lambda row: (row["brand"], row["reference_code"])):
                chanel_price = numeric_price(chanel)
                peer_price = numeric_price(peer)
                candidate_rows.append(
                    {
                        "pair_id": f"PAIR-{chanel['reference_code']}-{peer['brand']}-{peer['reference_code']}",
                        "cell_id": cell_id,
                        "market": market,
                        "source_effective_date": SOURCE_DATE,
                        "comparison_group_id": comparison_group_id,
                        "bag_type": bag_type,
                        "size_label": size_label,
                        "material_group": material,
                        "pairing_status": str(gate["pairing_status"]),
                        "headline_eligible": "TRUE" if gate["headline_eligible"] else "FALSE",
                        "price_comparison_status": "computed" if gate["headline_eligible"] else "not_computed",
                        "chanel_reference_code": chanel["reference_code"],
                        "chanel_price": fmt_number(chanel_price),
                        "peer_brand": peer["brand"],
                        "peer_reference_code": peer["reference_code"],
                        "peer_price": fmt_number(peer_price),
                        "price_gap_peer_minus_chanel": fmt_number(peer_price - chanel_price) if gate["headline_eligible"] else "",
                        "limitation": str(gate["limitation"]),
                    }
                )

    panel_fields = [
        "snapshot_id", "source_effective_date", "brand", "market", "currency", "reference_code", "product_name",
        "price_status", "price", "family", "model", "size_label", "use_tag", "bag_type", "material_raw",
        "material_group", "dimensions_cm", "regular_special", "collection_label", "scope_status", "isolation_reason", "pairing_readiness",
        "dimension_status", "comparison_group_id", "source_url",
    ]
    cell_fields = list(cell_rows[0]) if cell_rows else []
    candidate_fields = list(candidate_rows[0]) if candidate_rows else []
    write_csv(OUTPUT / "same_date_pairing_panel_2026-09-07_us.csv", panel, panel_fields)
    write_csv(OUTPUT / "same_date_pairing_cells_2026-09-07_us.csv", cell_rows, cell_fields)
    write_csv(OUTPUT / "same_date_pair_candidates_2026-09-07_us.csv", candidate_rows, candidate_fields)

    eligible = [row for row in cell_rows if row["headline_eligible"] == "TRUE"]
    status_counts = Counter(row["pairing_status"] for row in cell_rows)
    (OUTPUT / "same_date_pairing_audit_2026-09-07_us.md").write_text(
        f"""# 2026-09-07 美国站同日跨品牌配对审计

- 输入：`live_refresh_2026-09-07_us.csv`（Chanel、Hermès、Louis Vuitton、Dior，共 {len(panel)} 行）和竞品产品主数据。
- 同日门槛：`market=US`、`source_effective_date=2026-09-07`。
- 严格属性门槛：同市场、同日期、同包型、同尺寸、同材质；显式季节款、WOC/小皮具和未知尺寸单独隔离。
- 样本门槛：每个品牌在单元内至少 {MINIMUM_PER_BRAND} 条数值观察，且至少包含 Chanel 与另一个品牌。
- `regular_special=not_disclosed` 不被猜成常规款；若其他门槛通过，单元可作为条件性主文候选，并在限制列保留该缺口。已核实的季节覆盖写入 `seasonal_tote_attribute_overrides_2026-09-07_us.csv`，明确季节款不进入常规核心。

结果：共 {len(cell_rows)} 个属性单元，{len(candidate_rows)} 条 Chanel-竞品候选配对，{len(eligible)} 个单元通过主文门槛。

配对状态计数：`{dict(status_counts)}`。

输出：

- `same_date_pairing_panel_2026-09-07_us.csv`：用于审计的 81 行同日面板及归类字段，其中两条 AS6495 已标记为季节款。
- `same_date_pairing_cells_2026-09-07_us.csv`：单元级门槛和品牌中位数。
- `same_date_pair_candidates_2026-09-07_us.csv`：Chanel 与竞品的逐行候选配对。

本步骤只完成同日配对审计和可比单元筛选；既有 R1 报告和历史基线输出未被重写。
""",
        encoding="utf-8",
    )
    print({"panel_rows": len(panel), "cells": len(cell_rows), "candidate_pairs": len(candidate_rows), "headline_eligible_cells": len(eligible), "pairing_status": dict(status_counts)})


if __name__ == "__main__":
    main()
