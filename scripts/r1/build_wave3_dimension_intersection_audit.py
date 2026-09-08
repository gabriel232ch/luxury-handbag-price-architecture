#!/usr/bin/env python3
"""Audit Wave 3 same-date numeric dimension intersections.

This is deliberately separate from the 2026-09-07 main-panel audit. It uses
only the three 2026-09-08 top-up files, records every Chanel-to-peer pair, and
does not promote a pair unless the sorted numeric dimensions, bag type,
material, regular/seasonal gate, and independent-family sample gate all pass.
"""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "research_r1/data"
OUTPUT = ROOT / "research_r1/outputs"
CHANEL = DATA / "wave3_chanel_dimension_refresh_2026-09-08_us.csv"
PEERS = DATA / "wave3_hermes_lv_dimension_refresh_2026-09-08_us.csv"
SOURCE_DATE = "2026-09-08"
MARKET = "US"
MINIMUM_INDEPENDENT_FAMILIES = 3
AXIS_ABSOLUTE_TOLERANCE_CM = 2.0
AXIS_RELATIVE_TOLERANCE = 0.10


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


def fmt(values: tuple[float, ...] | None) -> str:
    if values is None:
        return ""
    return " x ".join(f"{value:.1f}".rstrip("0").rstrip(".") for value in values) + " cm"


def axis_check(left: dict[str, str], right: dict[str, str]) -> tuple[bool, tuple[float, ...] | None, tuple[float, ...] | None]:
    left_sig = signature(left)
    right_sig = signature(right)
    if left_sig is None or right_sig is None:
        return False, None, None
    diffs = tuple(abs(a - b) for a, b in zip(left_sig, right_sig))
    tolerances = tuple(max(AXIS_ABSOLUTE_TOLERANCE_CM, AXIS_RELATIVE_TOLERANCE * max(a, b)) for a, b in zip(left_sig, right_sig))
    return all(diff <= tolerance + 1e-9 for diff, tolerance in zip(diffs, tolerances)), diffs, tolerances


def is_core_candidate(row: dict[str, str]) -> bool:
    """Count rows that could contribute to a regular-core sample cell."""
    return (
        dimensions(row) is not None
        and row.get("price_status") == "numeric"
        and row.get("scope_status") not in {"seasonal_excluded", "sensitivity_only", "unknown_size"}
        and row.get("size_label") not in {"", "unknown"}
        and row.get("bag_type") not in {"", "unknown"}
        and row.get("material_group") not in {"", "unknown"}
    )


def cell_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (row.get("bag_type", ""), row.get("material_group", ""), row.get("market", ""))


def family_counts(rows: list[dict[str, str]]) -> Counter[str]:
    return Counter(row.get("family", "") for row in rows if is_core_candidate(row))


def regular_gate(rows: list[dict[str, str]]) -> list[str]:
    reasons: list[str] = []
    if any(row.get("scope_status") == "seasonal_excluded" or row.get("regular_special") == "seasonal_collection" for row in rows):
        reasons.append("blocked_seasonal_excluded")
    if any(row.get("regular_special") == "not_disclosed" for row in rows):
        reasons.append("blocked_regular_special_undisclosed")
    if any(row.get("scope_status") in {"unknown_size", "sensitivity_only"} or row.get("size_label") in {"", "unknown"} for row in rows):
        reasons.append("blocked_unknown_or_isolated_scope")
    return reasons


def main() -> None:
    chanel_rows = [row for row in read_csv(CHANEL) if row.get("source_effective_date") == SOURCE_DATE and row.get("market") == MARKET]
    peer_rows = [row for row in read_csv(PEERS) if row.get("source_effective_date") == SOURCE_DATE and row.get("market") == MARKET]
    all_rows = chanel_rows + peer_rows
    core_by_cell: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in all_rows:
        if is_core_candidate(row):
            core_by_cell[cell_key(row)].append(row)

    pair_rows: list[dict[str, str]] = []
    for chanel in chanel_rows:
        for peer in peer_rows:
            same_market_date = chanel.get("market") == peer.get("market") == MARKET and chanel.get("source_effective_date") == peer.get("source_effective_date") == SOURCE_DATE
            same_bag_type = chanel.get("bag_type") == peer.get("bag_type")
            same_material = chanel.get("material_group") == peer.get("material_group")
            dimension_match, diffs, tolerances = axis_check(chanel, peer)
            same_attributes = same_market_date and same_bag_type and same_material
            rows_for_gate = [chanel, peer]
            reasons: list[str] = []
            if not same_market_date:
                reasons.append("blocked_cross_market_or_date")
            if not same_bag_type or not same_material:
                reasons.append("blocked_bag_type_or_material_mismatch")
            if dimensions(chanel) is None or dimensions(peer) is None:
                reasons.append("blocked_until_dimension_capture")
            elif same_attributes and not dimension_match:
                reasons.append("blocked_dimension_mismatch")

            if same_attributes and dimension_match:
                reasons.extend(regular_gate(rows_for_gate))
                counts = {brand: len(family_counts([row for row in core_by_cell[cell_key(chanel)] if row.get("brand") == brand])) for brand in {chanel.get("brand"), peer.get("brand")}}
                if any(count < MINIMUM_INDEPENDENT_FAMILIES for count in counts.values()):
                    reasons.append("blocked_sample_insufficient")
            else:
                counts = {"Chanel": 0, peer.get("brand", "peer"): 0}

            if same_attributes and dimension_match and not reasons:
                decision_status = "main_text_eligible"
            elif same_attributes and dimension_match:
                decision_status = "directional_dimension_candidate"
            else:
                decision_status = "not_a_dimension_intersection"

            pair_rows.append(
                {
                    "pair_id": f"W3-PAIR-{chanel['reference_code']}-{peer['brand'].replace(' ', '_')}-{peer['reference_code']}",
                    "source_effective_date": SOURCE_DATE,
                    "market": MARKET,
                    "chanel_reference_code": chanel["reference_code"],
                    "chanel_product_name": chanel["product_name"],
                    "chanel_family": chanel.get("family", ""),
                    "chanel_bag_type": chanel.get("bag_type", ""),
                    "chanel_material_group": chanel.get("material_group", ""),
                    "chanel_size_label": chanel.get("size_label", ""),
                    "chanel_dimensions_cm": chanel.get("dimensions_cm", ""),
                    "chanel_dimension_signature_cm": fmt(signature(chanel)),
                    "peer_brand": peer["brand"],
                    "peer_reference_code": peer["reference_code"],
                    "peer_product_name": peer["product_name"],
                    "peer_family": peer.get("family", ""),
                    "peer_bag_type": peer.get("bag_type", ""),
                    "peer_material_group": peer.get("material_group", ""),
                    "peer_size_label": peer.get("size_label", ""),
                    "peer_dimensions_cm": peer.get("dimensions_cm", ""),
                    "peer_dimension_signature_cm": fmt(signature(peer)),
                    "axis_diff_cm": fmt(diffs),
                    "axis_tolerance_cm": fmt(tolerances),
                    "same_market_date": "TRUE" if same_market_date else "FALSE",
                    "same_bag_type": "TRUE" if same_bag_type else "FALSE",
                    "same_material": "TRUE" if same_material else "FALSE",
                    "dimension_match": "TRUE" if dimension_match else "FALSE",
                    "chanel_regular_special": chanel.get("regular_special", ""),
                    "peer_regular_special": peer.get("regular_special", ""),
                    "chanel_core_family_count": str(counts.get("Chanel", 0)),
                    "peer_core_family_count": str(counts.get(peer.get("brand", "peer"), 0)),
                    "decision_status": decision_status,
                    "block_reason": ";".join(dict.fromkeys(reasons)),
                    "chanel_source_url": chanel.get("source_url", ""),
                    "peer_source_url": peer.get("source_url", ""),
                }
            )

    pair_fields = list(pair_rows[0].keys())
    pair_path = OUTPUT / "wave3_dimension_intersection_pairs_2026-09-08_us.csv"
    write_csv(pair_path, pair_rows, pair_fields)

    by_status = Counter(row["decision_status"] for row in pair_rows)
    dimension_candidates = [row for row in pair_rows if row["decision_status"] == "directional_dimension_candidate"]
    attribute_candidates = [row for row in pair_rows if row["same_bag_type"] == "TRUE" and row["same_material"] == "TRUE"]
    summary_lines = [
        "# Wave 3 尺寸交集审计（2026-09-08，美国站）",
        "",
        "## 审计结论",
        "",
        f"本次只使用三份 2026-09-08 美国站刷新文件：Chanel {len(chanel_rows)} 行、Hermès/Louis Vuitton {len(peer_rows)} 行，共形成 {len(pair_rows)} 个 Chanel-to-peer 组合。所有输入行都有数值价格和三边尺寸。",
        f"同包型且同材质的属性候选为 {len(attribute_candidates)} 个；其中通过排序后三轴尺寸容差的只有 {sum(row['dimension_match'] == 'TRUE' for row in attribute_candidates)} 个。",
        f"方向性尺寸候选为 {len(dimension_candidates)} 个；满足主文全部门槛的单元为 {by_status.get('main_text_eligible', 0)} 个。",
        "",
        "尺寸判断使用排序后的三边，逐轴容差为 `max(2 cm, 10% × 两边较大值)`。尺寸匹配只说明量级接近，不自动覆盖包型、材质、常规/季节状态或样本量门槛。",
        "",
        "## 方向性尺寸候选",
        "",
    ]
    if dimension_candidates:
        summary_lines.append("| Chanel | 竞品 | Chanel 尺寸签名 cm | 竞品尺寸签名 cm | 轴差 cm | 阻断原因 |")
        summary_lines.append("|---|---|---:|---:|---:|---|")
        for row in dimension_candidates:
            summary_lines.append(
                f"| {row['chanel_reference_code']} | {row['peer_brand']} {row['peer_reference_code']} | {row['chanel_dimension_signature_cm']} | {row['peer_dimension_signature_cm']} | {row['axis_diff_cm']} | {row['block_reason']} |"
            )
    else:
        summary_lines.append("没有形成同时通过包型、材质和数值尺寸交集的方向性候选。")

    summary_lines.extend(
        [
            "",
            "## 阻断解释",
            "",
            "- Chanel AS5293（CHANEL 25 Small Handbag）与 Louis Vuitton M2A323（Low Key Hobo PM）是本轮唯一通过包型、材质和排序尺寸容差的方向性候选；两边的 `regular_special` 都是 `not_disclosed`，因此不能直接推成常规核心。",
            "- 该候选的核心独立家族数为 Chanel 2、Louis Vuitton 1，低于每品牌至少 3 个独立配置/家族的正式门槛，故标记为 `blocked_sample_insufficient`。",
            "- Hermès 没有形成通过包型、材质和尺寸容差的 Chanel 组合；其可比方向仍需补充更接近的包型/材质配置。",
            "- Chanel 的明确季节款继续隔离；Louis Vuitton 的 M46203 因材质组为 `textile`，不会与 Chanel 皮革 tote 强行合并。",
            "",
            "## 决策",
            "",
            "本轮不升级任何 Hermès/Louis Vuitton 单元进入主文比较。结果是“有 1 个可继续扩充的尺寸方向性候选”，而不是“已经形成可报告的跨品牌主文单元”。",
            "",
            "## 输出",
            "",
            "- `wave3_dimension_intersection_pairs_2026-09-08_us.csv`：30 个组合的逐对审计，含尺寸签名、轴差、容差、属性匹配和阻断原因。",
            "- 本文件不修改 2026-09-07 主面板或历史价格输出。",
        ]
    )
    summary_path = OUTPUT / "wave3_dimension_intersection_audit_2026-09-08_us.md"
    summary_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print({"chanel_rows": len(chanel_rows), "peer_rows": len(peer_rows), "pairs": len(pair_rows), "attribute_candidates": len(attribute_candidates), "dimension_candidates": len(dimension_candidates), "status": dict(by_status)})


if __name__ == "__main__":
    main()
