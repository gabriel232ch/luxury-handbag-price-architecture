#!/usr/bin/env python3
"""Audit the Wave 4 US hobo/leather expansion without changing the main panel."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "research_r1/data"
OUTPUT = ROOT / "research_r1/outputs"
SOURCE_DATE = "2026-09-08"
MARKET = "US"
MINIMUM_FAMILIES = 3

CHANEL_INPUTS = [
    DATA / "wave3_chanel_dimension_refresh_2026-09-08_us.csv",
    DATA / "wave4_hobo_leather_config_topup_2026-09-08_us.csv",
]
LV_INPUTS = [
    DATA / "wave3_hermes_lv_dimension_refresh_2026-09-08_us.csv",
    DATA / "wave4_hobo_leather_config_topup_2026-09-08_us.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_inputs(paths: list[Path], brand: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for path in paths:
        for row in read_csv(path):
            if row.get("brand") != brand:
                continue
            if row.get("source_effective_date") != SOURCE_DATE or row.get("market") != MARKET:
                continue
            if row.get("bag_type") != "hobo" or row.get("material_group") != "leather":
                continue
            reference = row.get("reference_code", "")
            if reference in seen:
                continue
            seen.add(reference)
            rows.append(row)
    return rows


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


def axis_match(left: dict[str, str], right: dict[str, str]) -> tuple[bool, tuple[float, ...] | None, tuple[float, ...] | None]:
    left_sig = signature(left)
    right_sig = signature(right)
    if left_sig is None or right_sig is None:
        return False, None, None
    diffs = tuple(abs(a - b) for a, b in zip(left_sig, right_sig))
    tolerances = tuple(max(2.0, 0.10 * max(a, b)) for a, b in zip(left_sig, right_sig))
    return all(diff <= tolerance + 1e-9 for diff, tolerance in zip(diffs, tolerances)), diffs, tolerances


def core_row(row: dict[str, str]) -> bool:
    return (
        dimensions(row) is not None
        and row.get("price_status") == "numeric"
        and row.get("scope_status") not in {"seasonal_excluded", "unknown_size", "sensitivity_only"}
        and row.get("size_label") not in {"", "unknown"}
    )


def status_reasons(rows: list[dict[str, str]]) -> list[str]:
    reasons: list[str] = []
    if any(row.get("scope_status") == "seasonal_excluded" or row.get("regular_special") == "seasonal_collection" for row in rows):
        reasons.append("blocked_seasonal_excluded")
    if any(row.get("regular_special") == "not_disclosed" for row in rows):
        reasons.append("blocked_regular_special_undisclosed")
    if any(row.get("scope_status") == "unknown_size" or row.get("size_label") in {"", "unknown"} for row in rows):
        reasons.append("blocked_unknown_size")
    return reasons


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    chanel_rows = read_inputs(CHANEL_INPUTS, "Chanel")
    lv_rows = read_inputs(LV_INPUTS, "Louis Vuitton")
    all_rows = chanel_rows + lv_rows
    family_counts = Counter(row.get("family", "") for row in all_rows if core_row(row))
    chanel_family_count = len({row.get("family", "") for row in chanel_rows if core_row(row)})
    lv_family_count = len({row.get("family", "") for row in lv_rows if core_row(row)})

    pairs: list[dict[str, str]] = []
    for chanel in sorted(chanel_rows, key=lambda row: row["reference_code"]):
        for lv in sorted(lv_rows, key=lambda row: row["reference_code"]):
            match, diffs, tolerances = axis_match(chanel, lv)
            reasons: list[str] = []
            if not match:
                reasons.append("blocked_dimension_mismatch")
            else:
                reasons.extend(status_reasons([chanel, lv]))
                if chanel_family_count < MINIMUM_FAMILIES or lv_family_count < MINIMUM_FAMILIES:
                    reasons.append("blocked_sample_insufficient")
            if match and not reasons:
                decision_status = "main_text_eligible"
            elif match:
                decision_status = "directional_dimension_candidate"
            else:
                decision_status = "not_a_dimension_intersection"
            pairs.append(
                {
                    "pair_id": f"W4-PAIR-{chanel['reference_code']}-LV-{lv['reference_code']}",
                    "source_effective_date": SOURCE_DATE,
                    "market": MARKET,
                    "chanel_reference_code": chanel["reference_code"],
                    "chanel_family": chanel.get("family", ""),
                    "chanel_size_label": chanel.get("size_label", ""),
                    "chanel_dimensions_cm": chanel.get("dimensions_cm", ""),
                    "chanel_dimension_signature_cm": fmt(signature(chanel)),
                    "chanel_scope_status": chanel.get("scope_status", ""),
                    "chanel_regular_special": chanel.get("regular_special", ""),
                    "lv_reference_code": lv["reference_code"],
                    "lv_family": lv.get("family", ""),
                    "lv_size_label": lv.get("size_label", ""),
                    "lv_dimensions_cm": lv.get("dimensions_cm", ""),
                    "lv_dimension_signature_cm": fmt(signature(lv)),
                    "lv_scope_status": lv.get("scope_status", ""),
                    "lv_regular_special": lv.get("regular_special", ""),
                    "lv_availability_status": lv.get("availability_status", ""),
                    "axis_diff_cm": fmt(diffs),
                    "axis_tolerance_cm": fmt(tolerances),
                    "chanel_core_family_count": str(chanel_family_count),
                    "lv_core_family_count": str(lv_family_count),
                    "dimension_match": "TRUE" if match else "FALSE",
                    "decision_status": decision_status,
                    "block_reason": ";".join(dict.fromkeys(reasons)),
                    "chanel_source_url": chanel.get("source_url", ""),
                    "lv_source_url": lv.get("source_url", ""),
                }
            )

    pair_path = OUTPUT / "wave4_hobo_dimension_pairs_2026-09-08_us.csv"
    write_csv(pair_path, pairs)
    directional = [row for row in pairs if row["decision_status"] == "directional_dimension_candidate"]
    eligible = [row for row in pairs if row["decision_status"] == "main_text_eligible"]
    summary = [
        "# Wave 4 hobo + leather 尺寸审计（2026-09-08，美国站）",
        "",
        "## 审计结论",
        "",
        f"合并 Wave 3 和 Wave 4 后，`US|hobo|leather` 包含 Chanel {len(chanel_rows)} 个配置、Louis Vuitton {len(lv_rows)} 个配置，共 {len(pairs)} 个成对组合。",
        f"按数值尺寸排序后三轴容差审计，方向性尺寸候选为 {len(directional)} 个；满足主文全部门槛的单元为 {len(eligible)} 个。",
        f"正式样本门槛要求每边至少 {MINIMUM_FAMILIES} 个独立家族；本轮核心计数为 Chanel {chanel_family_count}、Louis Vuitton {lv_family_count}。",
        "",
        "尺寸容差为 `max(2 cm, 10% × 两边较大值)`，只用于识别量级接近，不把品牌 PM/MM/small 标签直接互换。",
        "",
        "## 唯一方向性尺寸候选",
        "",
    ]
    if directional:
        summary.extend([
            "| Chanel | Louis Vuitton | Chanel 尺寸签名 cm | LV 尺寸签名 cm | 轴差 cm | 阻断原因 |",
            "|---|---|---:|---:|---:|---|",
        ])
        for row in directional:
            summary.append(
                f"| {row['chanel_reference_code']} ({row['chanel_family']}) | {row['lv_reference_code']} ({row['lv_family']}) | {row['chanel_dimension_signature_cm']} | {row['lv_dimension_signature_cm']} | {row['axis_diff_cm']} | {row['block_reason']} |"
            )
    else:
        summary.append("没有形成方向性尺寸候选。")
    summary.extend([
        "",
        "## 阻断解释",
        "",
        "- AS5293（CHANEL 25 Small）与 M2A323（Low Key Hobo PM）仍是唯一通过三轴数值尺寸容差的组合。",
        f"- 该组合的核心独立家族数为 Chanel {chanel_family_count}、Louis Vuitton {lv_family_count}，均低于 {MINIMUM_FAMILIES}；两边常规/季节状态仍为 `not_disclosed`。",
        "- 新增 Chanel AS6617 是明确 Fall Winter 2026 Pre-Collection，继续季节隔离；新增 LV Loop Hobo 和 Hobo Métis 没有命名尺寸，继续未知尺寸隔离。",
        "- 新增 LV Coussin Hobo MM 有明确 MM 标签，但数值尺寸与 Chanel 22/25 不在容差内；因此增加了家族覆盖，却没有形成新的尺寸交集。",
        "",
        "## 决策",
        "",
        "本轮不升级任何 hobo + leather 单元进入主文比较。新增配置有效扩大了候选池，但没有达到正式样本和状态门槛。",
        "",
        "## 输出",
        "",
        "- `wave4_hobo_dimension_pairs_2026-09-08_us.csv`：12 个 Chanel–Louis Vuitton hobo 组合的逐对结果。",
        "- 本审计不改写 2026-09-07 主面板，不计算价格差。",
    ])
    summary_path = OUTPUT / "wave4_hobo_dimension_audit_2026-09-08_us.md"
    summary_path.write_text("\n".join(summary) + "\n", encoding="utf-8")
    print({"chanel_rows": len(chanel_rows), "lv_rows": len(lv_rows), "pairs": len(pairs), "directional": len(directional), "eligible": len(eligible), "chanel_core_families": chanel_family_count, "lv_core_families": lv_family_count})


if __name__ == "__main__":
    main()
