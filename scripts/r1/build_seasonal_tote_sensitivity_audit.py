#!/usr/bin/env python3
"""Audit the isolated seasonal tote sensitivity route without publishing price gaps."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "research_r1/data"
ROUTE = DATA / "seasonal_tote_sensitivity_2026-09-08_us.csv"
OUTPUT = ROOT / "research_r1/outputs"
MINIMUM_PER_ROLE = 3


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def numeric_prices(rows: list[dict[str, str]]) -> list[float]:
    values: list[float] = []
    for row in rows:
        if row.get("price_status") != "numeric":
            continue
        try:
            values.append(float(row["price"]))
        except (TypeError, ValueError):
            continue
    return values


def fmt(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.1f}".rstrip("0").rstrip(".")


def audit_group(snapshot_date: str, chanel: list[dict[str, str]], dior: list[dict[str, str]]) -> dict[str, str]:
    chanel_prices = numeric_prices(chanel)
    dior_prices = numeric_prices(dior)
    chanel_statuses = sorted({row.get("regular_special", "") for row in chanel})
    dior_statuses = sorted({row.get("regular_special", "") for row in dior})
    blockers: list[str] = []
    if len(chanel) < MINIMUM_PER_ROLE:
        blockers.append("chanel_sample_lt3")
    if len(dior) < MINIMUM_PER_ROLE:
        blockers.append("dior_sample_lt3")
    if not dior or any(status != "seasonal_collection" for status in dior_statuses):
        blockers.append("dior_regular_season_status_undisclosed")
    if not chanel or any(status != "seasonal_collection" for status in chanel_statuses):
        blockers.append("chanel_season_status_not_explicit")
    comparison_status = "computed" if not blockers else "not_computed"
    if comparison_status == "computed":
        publication_decision = "eligible_for_sensitivity_statistic"
    elif "dior_regular_season_status_undisclosed" in blockers:
        publication_decision = "descriptive_only_status_undisclosed"
    else:
        publication_decision = "sensitivity_context_only"
    return {
        "audit_id": f"SEASONAL-US-{snapshot_date}-tote-small-leather",
        "snapshot_date": snapshot_date,
        "market": "US",
        "bag_type": "tote",
        "size_label": "small",
        "material_group": "leather",
        "chanel_configurations": str(len(chanel)),
        "dior_configurations": str(len(dior)),
        "chanel_median_usd": fmt(median(chanel_prices) if chanel_prices else None),
        "dior_median_usd": fmt(median(dior_prices) if dior_prices else None),
        "chanel_statuses": ";".join(chanel_statuses),
        "dior_statuses": ";".join(dior_statuses),
        "sample_gate": "pass" if not any(item.endswith("_sample_lt3") for item in blockers) else "blocked",
        "status_gate": "pass" if not any(item.endswith("status_undisclosed") or item.endswith("status_not_explicit") for item in blockers) else "blocked",
        "comparison_status": comparison_status,
        "publication_decision": publication_decision,
        "blocking_reasons": ";".join(blockers),
    }


def main() -> None:
    rows = read_csv(ROUTE)
    target = [
        row for row in rows
        if row["bag_type"] == "tote" and row["size_label"] == "small" and row["material_group"] == "leather"
    ]
    grouped: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for row in target:
        grouped[row["snapshot_date"]][row["comparison_role"]].append(row)

    audit_rows: list[dict[str, str]] = []
    for snapshot_date in sorted(grouped):
        roles = grouped[snapshot_date]
        audit_rows.append(
            audit_group(
                snapshot_date,
                roles.get("chanel_seasonal_small_tote", []),
                roles.get("dior_same_date_context", []),
            )
        )

    mini = [row for row in rows if row.get("comparison_role") == "chanel_seasonal_mini_context"]
    mini_prices = numeric_prices(mini)
    audit_rows.append(
        {
            "audit_id": "SEASONAL-US-2026-09-08-tote-mini-leather",
            "snapshot_date": "2026-09-08",
            "market": "US",
            "bag_type": "tote",
            "size_label": "mini",
            "material_group": "leather",
            "chanel_configurations": str(len(mini)),
            "dior_configurations": "0",
            "chanel_median_usd": fmt(median(mini_prices) if mini_prices else None),
            "dior_median_usd": "",
            "chanel_statuses": ";".join(sorted({row.get("regular_special", "") for row in mini})),
            "dior_statuses": "",
            "sample_gate": "blocked",
            "status_gate": "blocked",
            "comparison_status": "not_computed",
            "publication_decision": "excluded_size_mismatch",
            "blocking_reasons": "mini_outside_small_tote_route;no_dior_peer",
        }
    )

    fields = list(audit_rows[0])
    output_csv = OUTPUT / "seasonal_tote_sensitivity_audit_2026-09-08_us.csv"
    write_csv(output_csv, audit_rows, fields)

    output_md = OUTPUT / "seasonal_tote_sensitivity_audit_2026-09-08_us.md"
    lines = [
        "# 季节款 Tote 敏感性路线门槛审计（美国站）",
        "",
        "本审计只检查独立季节路线，不改写常规核心主面板。数值中位数保留为描述性上下文；只有样本量、属性和常规/季节状态门槛同时通过，才允许计算跨品牌价格差。",
        "",
        "## 审计结果",
        "",
        "| 快照日期 | Chanel 配置 | Dior 配置 | Chanel 中位数 | Dior 中位数 | 样本门槛 | 状态门槛 | 价格比较 | 发布决定 |",
        "|---|---:|---:|---:|---:|---|---|---|---|",
    ]
    for row in audit_rows:
        lines.append(
            f"| {row['snapshot_date']} / {row['size_label']} | {row['chanel_configurations']} | {row['dior_configurations']} | {row['chanel_median_usd'] or '—'} | {row['dior_median_usd'] or '—'} | {row['sample_gate']} | {row['status_gate']} | `{row['comparison_status']}` | `{row['publication_decision']}` |"
        )
    lines += [
        "",
        "## 阻断原因",
        "",
        "- 2026-09-07：Chanel 只有 2 个季节小号 Tote，低于每个比较角色至少 3 个独立配置；Dior 的 5 条上下文记录均为 `not_disclosed`，不能确认是季节款。",
        "- 2026-09-08：Chanel 与 Dior 均已达到 3 个独立配置的样本门槛，但 Dior 的常规/季节状态仍为 `not_disclosed`，因此状态门槛未通过。",
        "- Mini 行单独隔离，不与 small Tote 配对。",
        "",
        "## 结论",
        "",
        "本轮没有任何可发布的季节对季节价格差。2026-09-08 的样本量门槛已达到，但 Dior 状态门槛仍未通过；官网详情页可正常访问且未出现 collection/season/Fall/Spring 标记，因此本路线正式收口为描述性敏感性背景。",
        "",
        "来源数据：[seasonal_tote_sensitivity_2026-09-08_us.csv](../data/seasonal_tote_sensitivity_2026-09-08_us.csv)。",
        "",
    ]
    output_md.write_text("\n".join(lines), encoding="utf-8")
    print({"rows": len(audit_rows), "output_csv": str(output_csv), "output_md": str(output_md), "computed": sum(row["comparison_status"] == "computed" for row in audit_rows)})


if __name__ == "__main__":
    main()
