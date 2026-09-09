#!/usr/bin/env python3
"""Audit the independent 2026-09-09 four-brand refresh.

The refresh is deliberately kept outside the 2026-09-08 panel.  This audit
checks exact market/date/bag-type/size/material cells first, then applies the
numeric dimension and sample gates used by the hobo expansion.  It emits both
conditional attribute candidates and the stricter main-text result.
"""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "research_r1/data"
OUTPUT = ROOT / "research_r1/outputs"
INPUT = DATA / "wave6_same_date_refresh_2026-09-09_us.csv"
SOURCE_DATE = "2026-09-09"
MARKET = "US"
MINIMUM_ROWS_PER_BRAND = 2
MINIMUM_INDEPENDENT_FAMILIES = 3
ABSOLUTE_TOLERANCE_CM = 2.0
RELATIVE_TOLERANCE = 0.10


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def dimensions(row: dict[str, str]) -> tuple[float, float, float] | None:
    values = [float(value) for value in re.findall(r"\d+(?:\.\d+)?", row.get("dimensions_cm", ""))]
    if len(values) != 3:
        return None
    return tuple(values)  # type: ignore[return-value]


def signature(row: dict[str, str]) -> tuple[float, float, float] | None:
    values = dimensions(row)
    return tuple(sorted(values, reverse=True)) if values else None


def format_values(values: tuple[float, ...] | None) -> str:
    if values is None:
        return ""
    return " x ".join(f"{value:.1f}".rstrip("0").rstrip(".") for value in values) + " cm"


def dimension_check(left: dict[str, str], right: dict[str, str]) -> tuple[bool, tuple[float, ...] | None, tuple[float, ...] | None]:
    left_signature = signature(left)
    right_signature = signature(right)
    if left_signature is None or right_signature is None:
        return False, None, None
    diffs = tuple(abs(a - b) for a, b in zip(left_signature, right_signature))
    tolerances = tuple(max(ABSOLUTE_TOLERANCE_CM, RELATIVE_TOLERANCE * max(a, b)) for a, b in zip(left_signature, right_signature))
    return all(diff <= tolerance + 1e-9 for diff, tolerance in zip(diffs, tolerances)), diffs, tolerances


def numeric_price(row: dict[str, str]) -> float | None:
    if row.get("price_status") != "numeric":
        return None
    try:
        return float(row["price"])
    except (TypeError, ValueError):
        return None


def group_id(row: dict[str, str]) -> str:
    return "|".join((row.get("market", ""), row.get("bag_type", ""), row.get("size_label", ""), row.get("material_group", "")))


def cell_gate(rows: list[dict[str, str]]) -> dict[str, str | bool]:
    if any(row.get("scope_status") == "seasonal_excluded" or row.get("regular_special") == "seasonal_collection" for row in rows):
        return {"status": "blocked_seasonal_excluded", "reason": "Explicit seasonal rows remain outside the regular-core headline."}
    if any(row.get("scope_status") in {"unknown_size", "sensitivity_only"} or row.get("size_label") in {"", "unknown"} for row in rows):
        return {"status": "blocked_unknown_size", "reason": "Unknown size cannot support like-for-like pairing."}
    if any(row.get("bag_type") in {"", "unknown"} for row in rows):
        return {"status": "blocked_unknown_bag_type", "reason": "Unknown bag type cannot support like-for-like pairing."}
    if any(row.get("material_group") in {"", "unknown"} for row in rows):
        return {"status": "blocked_unknown_material", "reason": "Unknown material group cannot support like-for-like pairing."}
    numeric_rows = [row for row in rows if numeric_price(row) is not None]
    brands = Counter(row.get("brand", "") for row in numeric_rows)
    if "Chanel" not in brands:
        return {"status": "blocked_no_chanel_subject", "reason": "The headline subject is Chanel; competitor-only cells remain contextual."}
    if len(brands) < 2:
        return {"status": "blocked_no_cross_brand_peer", "reason": "No second brand shares the exact attribute cell."}
    if any(count < MINIMUM_ROWS_PER_BRAND for count in brands.values()):
        return {"status": "blocked_sample_insufficient", "reason": f"Each brand needs at least {MINIMUM_ROWS_PER_BRAND} numeric rows in the cell."}
    if any(row.get("regular_special") == "not_disclosed" for row in rows):
        return {"status": "conditional_regular_special_review", "reason": "Exact cell passes observable gates, but regular/season status is not disclosed."}
    return {"status": "attribute_cell_ready", "reason": "Exact same-date attribute cell passes observable gates."}


def main() -> None:
    rows = [row for row in read_csv(INPUT) if row.get("market") == MARKET and row.get("source_effective_date") == SOURCE_DATE]
    for row in rows:
        row["comparison_group_id"] = group_id(row)

    panel_fields = list(rows[0].keys()) if rows else []
    write_csv(OUTPUT / "wave6_same_date_pairing_panel_2026-09-09_us.csv", rows, panel_fields)

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["comparison_group_id"]].append(row)

    cells: list[dict[str, str]] = []
    candidates: list[dict[str, str]] = []
    dimension_pairs: list[dict[str, str]] = []
    for comparison_group_id, cell_rows in sorted(grouped.items()):
        gate = cell_gate(cell_rows)
        numeric_rows = [row for row in cell_rows if numeric_price(row) is not None]
        brands = sorted({row["brand"] for row in numeric_rows})
        counts = Counter(row["brand"] for row in numeric_rows)
        family_counts = {brand: len({row.get("family", "") for row in numeric_rows if row.get("brand") == brand}) for brand in brands}
        medians = {brand: median([numeric_price(row) for row in numeric_rows if row["brand"] == brand]) for brand in brands}
        market, bag_type, size_label, material = comparison_group_id.split("|", 3)
        strict_reasons: list[str] = []
        if gate["status"] != "attribute_cell_ready":
            strict_reasons.append(str(gate["status"]))
        if family_counts and any(count < MINIMUM_INDEPENDENT_FAMILIES for count in family_counts.values()):
            strict_reasons.append("blocked_independent_family_sample")
        strict_status = "main_text_eligible" if not strict_reasons and len(brands) >= 2 else ";".join(dict.fromkeys(strict_reasons or ["blocked_no_cross_brand_peer"]))
        cells.append(
            {
                "cell_id": "CELL-" + comparison_group_id.replace("|", "-"),
                "market": market,
                "source_effective_date": SOURCE_DATE,
                "comparison_group_id": comparison_group_id,
                "bag_type": bag_type,
                "size_label": size_label,
                "material_group": material,
                "brands": ";".join(brands),
                "brand_counts": ";".join(f"{brand}:{counts[brand]}" for brand in brands),
                "independent_family_counts": ";".join(f"{brand}:{family_counts[brand]}" for brand in brands),
                "brand_medians": ";".join(f"{brand}:{medians[brand]:.1f}" for brand in brands),
                "attribute_gate_status": str(gate["status"]),
                "main_text_status": strict_status,
                "price_comparison_status": "computed" if strict_status == "main_text_eligible" else "not_computed",
                "gate_reason": str(gate["reason"]),
                "strict_gate_reason": ";".join(dict.fromkeys(strict_reasons)),
            }
        )
        chanel_rows = [row for row in numeric_rows if row["brand"] == "Chanel"]
        peers = [row for row in numeric_rows if row["brand"] != "Chanel"]
        for chanel in sorted(chanel_rows, key=lambda row: row["reference_code"]):
            for peer in sorted(peers, key=lambda row: (row["brand"], row["reference_code"])):
                dim_match, diffs, tolerances = dimension_check(chanel, peer)
                pair_reasons: list[str] = []
                if not dim_match:
                    pair_reasons.append("blocked_dimension_mismatch")
                if gate["status"] != "attribute_cell_ready":
                    pair_reasons.append(str(gate["status"]))
                if family_counts.get("Chanel", 0) < MINIMUM_INDEPENDENT_FAMILIES or family_counts.get(peer["brand"], 0) < MINIMUM_INDEPENDENT_FAMILIES:
                    pair_reasons.append("blocked_independent_family_sample")
                status = "main_text_eligible" if not pair_reasons else "directional_candidate" if dim_match else "not_a_dimension_intersection"
                candidates.append(
                    {
                        "pair_id": f"W6-PAIR-{chanel['reference_code']}-{peer['brand'].replace(' ', '_')}-{peer['reference_code']}",
                        "cell_id": "CELL-" + comparison_group_id.replace("|", "-"),
                        "market": market,
                        "source_effective_date": SOURCE_DATE,
                        "comparison_group_id": comparison_group_id,
                        "chanel_reference_code": chanel["reference_code"],
                        "chanel_family": chanel.get("family", ""),
                        "peer_brand": peer["brand"],
                        "peer_reference_code": peer["reference_code"],
                        "peer_family": peer.get("family", ""),
                        "chanel_dimensions_cm": chanel.get("dimensions_cm", ""),
                        "peer_dimensions_cm": peer.get("dimensions_cm", ""),
                        "chanel_dimension_signature_cm": format_values(signature(chanel)),
                        "peer_dimension_signature_cm": format_values(signature(peer)),
                        "axis_diff_cm": format_values(diffs),
                        "axis_tolerance_cm": format_values(tolerances),
                        "dimension_match": "TRUE" if dim_match else "FALSE",
                        "pairing_status": status,
                        "block_reason": ";".join(dict.fromkeys(pair_reasons)),
                        "chanel_price": f"{numeric_price(chanel):.1f}",
                        "peer_price": f"{numeric_price(peer):.1f}",
                        "price_comparison_status": "computed" if status == "main_text_eligible" else "not_computed",
                        "chanel_source_url": chanel.get("source_url", ""),
                        "peer_source_url": peer.get("source_url", ""),
                    }
                )

    write_csv(OUTPUT / "wave6_same_date_pairing_cells_2026-09-09_us.csv", cells, list(cells[0].keys()) if cells else [])
    write_csv(OUTPUT / "wave6_same_date_pair_candidates_2026-09-09_us.csv", candidates, list(candidates[0].keys()) if candidates else [])

    all_hobo_leather = [row for row in rows if row.get("bag_type") == "hobo" and row.get("material_group") == "leather"]
    hobo_dimension_pairs: list[dict[str, str]] = []
    for left in sorted([row for row in all_hobo_leather if row["brand"] == "Chanel"], key=lambda row: row["reference_code"]):
        for right in sorted([row for row in all_hobo_leather if row["brand"] != "Chanel"], key=lambda row: (row["brand"], row["reference_code"])):
            match, diffs, tolerances = dimension_check(left, right)
            hobo_dimension_pairs.append(
                {
                    "pair_id": f"W6-DIM-{left['reference_code']}-{right['brand'].replace(' ', '_')}-{right['reference_code']}",
                    "source_effective_date": SOURCE_DATE,
                    "market": MARKET,
                    "chanel_reference_code": left["reference_code"],
                    "chanel_family": left.get("family", ""),
                    "chanel_size_label": left.get("size_label", ""),
                    "peer_brand": right["brand"],
                    "peer_reference_code": right["reference_code"],
                    "peer_family": right.get("family", ""),
                    "peer_size_label": right.get("size_label", ""),
                    "chanel_dimension_signature_cm": format_values(signature(left)),
                    "peer_dimension_signature_cm": format_values(signature(right)),
                    "axis_diff_cm": format_values(diffs),
                    "axis_tolerance_cm": format_values(tolerances),
                    "dimension_match": "TRUE" if match else "FALSE",
                    "same_size_label": "TRUE" if left.get("size_label") == right.get("size_label") else "FALSE",
                    "block_reason": "" if match else "blocked_dimension_mismatch",
                    "chanel_source_url": left.get("source_url", ""),
                    "peer_source_url": right.get("source_url", ""),
                }
            )
    write_csv(OUTPUT / "wave6_same_date_hobo_dimension_pairs_2026-09-09_us.csv", hobo_dimension_pairs, list(hobo_dimension_pairs[0].keys()) if hobo_dimension_pairs else [])

    status_counts = Counter(row["attribute_gate_status"] for row in cells)
    strict_counts = Counter(row["main_text_status"] for row in cells)
    dimension_matches = sum(row["dimension_match"] == "TRUE" for row in hobo_dimension_pairs)
    small_cell = next((row for row in cells if row["comparison_group_id"] == "US|hobo|small|leather"), None)
    summary = [
        "# Wave 6 四品牌同日配对审计（2026-09-09，美国站）",
        "",
        "## 结论",
        "",
        f"本审计只使用 `wave6_same_date_refresh_2026-09-09_us.csv` 的 {len(rows)} 行；不改写 2026-09-08 或更早面板。共形成 {len(cells)} 个精确市场/包型/尺寸/材质单元和 {len(candidates)} 条 Chanel-竞品候选配对。",
        f"属性单元状态计数：`{dict(status_counts)}`；严格主文状态计数：`{dict(strict_counts)}`。通过所有主文门槛的单元为 {sum(row['main_text_status'] == 'main_text_eligible' for row in cells)} 个。",
        f"在 hobo + leather 路线的 Chanel-to-peer 逐对尺寸检查中，{dimension_matches} 个组合通过排序后三轴 `max(2 cm, 10%)` 容差；没有组合同时通过同尺寸标签、regular/season 状态和独立家族样本门槛。",
        "",
        "## 关键单元",
        "",
    ]
    if small_cell:
        summary.extend([
            f"`US|hobo|small|leather` 包含 {small_cell['brands']}，品牌计数为 `{small_cell['brand_counts']}`，独立家族计数为 `{small_cell['independent_family_counts']}`，属性状态为 `{small_cell['attribute_gate_status']}`，严格状态为 `{small_cell['main_text_status']}`。",
            "该单元中的 Dior Toujours 行带有明确 Autumn-Winter 2026-2027 标记，已按季节款隔离；即使移除该行，Chanel 也没有同日同尺寸的第二品牌样本。",
        ])
    summary.extend([
        "",
        "## 逐对解释",
        "",
        "- Hermès Videpoches 只有 crossbody/unknown-size 行，因此不进入 hobo 单元，也不与 Chanel hobo 强行配对。",
        "- Louis Vuitton 本轮是 PM/MM 尺寸，而 Chanel 行是 Small；虽然同为 hobo + leather，但严格同尺寸门槛不通过。",
        "- Dior Bobby 是 Medium；Dior Toujours Small 是明确季节款。Dior Bobby 与 Chanel 没有同尺寸单元。",
        "- 所有 Chanel、Louis Vuitton 和 Dior Bobby 行的 regular/season 状态仍为 `not_disclosed`；不能把未披露推断成常规款。",
        "- 主文比较要求每品牌至少 3 个独立家族；本轮任何跨品牌单元也没有达到该门槛，因此不计算价格差、中位数排名或品牌溢价。",
        "",
        "## 决定",
        "",
        "本轮研究结论是：2026-09-09 快照完成了证据刷新和门槛审计，但没有产生可进入主文的跨品牌比较单元。研究状态继续为 `limited`；这不是抓取失败，而是官方页面当前可验证的包型、尺寸、季节状态和样本门槛未同时满足。",
        "",
        "## 输出",
        "",
        "- `wave6_same_date_pairing_panel_2026-09-09_us.csv`：8 行同日证据面板。",
        "- `wave6_same_date_pairing_cells_2026-09-09_us.csv`：属性单元、品牌计数、独立家族计数和严格门槛。",
        "- `wave6_same_date_pair_candidates_2026-09-09_us.csv`：Chanel-竞品逐对门控与价格计算状态。",
        "- `wave6_same_date_hobo_dimension_pairs_2026-09-09_us.csv`：hobo + leather 的逐对尺寸检查。",
        "本轮没有产生价格比较结果；这保持了日期、属性和证据门槛的完整性。",
    ])
    (OUTPUT / "wave6_same_date_pairing_audit_2026-09-09_us.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print({
        "rows": len(rows),
        "cells": len(cells),
        "candidates": len(candidates),
        "attribute_status": dict(status_counts),
        "strict_status": dict(strict_counts),
        "hobo_dimension_pairs": len(hobo_dimension_pairs),
        "hobo_dimension_matches": dimension_matches,
    })


if __name__ == "__main__":
    main()
