#!/usr/bin/env python3
"""Build an attribute-filtered audit for the Chanel supplementary snapshot.

The 2026-09-07 Chanel supplement is intentionally kept separate from the
2026-08-15 competitor snapshot. This script identifies directional peer
candidates by market, bag type, size and material, then blocks any price
comparison whose snapshots are not aligned.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
R1 = ROOT / "research_r1"
DATA = R1 / "data"
OUT = R1 / "outputs"
SUPPLEMENT_SNAPSHOT = "supplementary_current_2026-09-07"
BASELINE_SNAPSHOT = "current_2026-08-15"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def group_parts(group_id: str) -> tuple[str, str, str, str]:
    market, bag_type, size_label, material_group = (group_id.split("|", 3) + [""] * 4)[:4]
    return market, bag_type, size_label, material_group


def cell_gate(rows: list[dict[str, str]], peer_count: int) -> tuple[str, str, str]:
    statuses = {row["inclusion_status"] for row in rows}
    if "sensitivity_only" in statuses:
        return "woc_sensitivity_only", "excluded_supplementary", "WOC is outside the main handbag denominator."
    if any(row["size_label"] == "unknown" for row in rows):
        return "unknown_size", "blocked_unknown_size", "Size is unknown; the attribute filter cannot assert a like-for-like cell."
    if "accepted_supplementary_seasonal" in statuses:
        return "seasonal_excluded", "excluded_supplementary", "Seasonal collection rows remain outside the regular-core headline."
    if peer_count == 0:
        return "no_same_group_peer", "blocked_no_peer", "No numeric baseline competitor row shares all four attributes."
    return "cross_snapshot_only", "blocked_cross_snapshot", "Attributes match a directional peer cell, but price comparison is blocked across snapshots."


def main() -> None:
    supplement = [
        row for row in read_csv(DATA / "supplementary_current.csv")
        if row["snapshot_id"] == SUPPLEMENT_SNAPSHOT
    ]
    baseline = [
        row for row in read_csv(DATA / "observations.csv")
        if row["snapshot_id"] == BASELINE_SNAPSHOT
        and row["price_status"] == "numeric"
        and row["inclusion_status"] == "accepted"
        and row["brand"] != "Chanel"
    ]

    peers_by_group: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in baseline:
        peers_by_group[row["comparison_group_id"]].append(row)

    supplement_by_group: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in supplement:
        supplement_by_group[row["comparison_group_id"]].append(row)

    candidate_rows: list[dict[str, str]] = []
    for row in sorted(supplement, key=lambda item: item["observation_id"]):
        if row["inclusion_status"] != "accepted_supplementary" or row["size_label"] == "unknown":
            continue
        peers = peers_by_group.get(row["comparison_group_id"], [])
        for peer in sorted(peers, key=lambda item: (item["brand"], item["observation_id"])):
            market, bag_type, size_label, material_group = group_parts(row["comparison_group_id"])
            candidate_rows.append({
                "pair_id": f"PAIR-{row['observation_id']}-{peer['observation_id']}",
                "market": market,
                "currency": row["currency"],
                "comparison_group_id": row["comparison_group_id"],
                "bag_type": bag_type,
                "size_label": size_label,
                "material_group": material_group,
                "attribute_match": "exact_group",
                "pairing_status": "blocked_cross_snapshot",
                "price_comparison_status": "not_computed",
                "supplement_observation_id": row["observation_id"],
                "supplement_snapshot_id": row["snapshot_id"],
                "supplement_source_id": row["source_id"],
                "supplement_reference_code": row["reference_code"],
                "supplement_family": row["family"],
                "supplement_currency": row["currency"],
                "supplement_price": row["price"],
                "peer_observation_id": peer["observation_id"],
                "peer_snapshot_id": peer["snapshot_id"],
                "peer_source_id": peer["source_id"],
                "peer_brand": peer["brand"],
                "peer_reference_code": peer["reference_code"],
                "peer_family": peer["family"],
                "peer_currency": peer["currency"],
                "peer_price": peer["price"],
                "price_gap": "",
                "limitation": "Directional attribute match only; the two rows come from different snapshots and cannot be used for a price ranking.",
            })

    cell_rows: list[dict[str, str]] = []
    for group_id, group_rows in sorted(supplement_by_group.items()):
        market, bag_type, size_label, material_group = group_parts(group_id)
        peers = peers_by_group.get(group_id, [])
        gate_reason, pairing_status, limitation = cell_gate(group_rows, len(peers))
        cell_rows.append({
            "market": market,
            "currency": group_rows[0]["currency"],
            "comparison_group_id": group_id,
            "bag_type": bag_type,
            "size_label": size_label,
            "material_group": material_group,
            "supplement_snapshot_id": SUPPLEMENT_SNAPSHOT,
            "supplementary_chanel_observations": str(len(group_rows)),
            "supplementary_numeric_observations": str(sum(row["price_status"] == "numeric" for row in group_rows)),
            "supplementary_reference_codes": ";".join(sorted({row["reference_code"] for row in group_rows})),
            "supplementary_families": ";".join(sorted({row["family"] for row in group_rows})),
            "supplementary_inclusion_statuses": ";".join(sorted({row["inclusion_status"] for row in group_rows})),
            "peer_snapshot_id": BASELINE_SNAPSHOT,
            "baseline_peer_count": str(len(peers)),
            "baseline_peer_brands": ";".join(sorted({row["brand"] for row in peers})),
            "baseline_peer_families": ";".join(sorted({row["family"] for row in peers})),
            "attribute_filter": "same market + bag type + size + material group",
            "headline_eligible": "FALSE",
            "pairing_status": pairing_status,
            "price_comparison_status": "not_computed",
            "gate_reason": gate_reason,
            "limitation": limitation,
        })

    write_csv(OUT / "comparable_pair_candidates.csv", candidate_rows, [
        "pair_id", "market", "currency", "comparison_group_id", "bag_type", "size_label", "material_group",
        "attribute_match", "pairing_status", "price_comparison_status", "supplement_observation_id",
        "supplement_snapshot_id", "supplement_source_id", "supplement_reference_code", "supplement_family",
        "supplement_currency", "supplement_price", "peer_observation_id", "peer_snapshot_id", "peer_source_id",
        "peer_brand", "peer_reference_code", "peer_family", "peer_currency", "peer_price", "price_gap", "limitation",
    ])
    write_csv(OUT / "comparable_cells_supplementary.csv", cell_rows, [
        "market", "currency", "comparison_group_id", "bag_type", "size_label", "material_group",
        "supplement_snapshot_id", "supplementary_chanel_observations", "supplementary_numeric_observations",
        "supplementary_reference_codes", "supplementary_families", "supplementary_inclusion_statuses",
        "peer_snapshot_id", "baseline_peer_count", "baseline_peer_brands", "baseline_peer_families",
        "attribute_filter", "headline_eligible", "pairing_status", "price_comparison_status", "gate_reason", "limitation",
    ])
    (OUT / "comparable_pairing_log.md").write_text(
        f"""# Chanel 属性配对审计（第 3 步）

- 补充快照：`{SUPPLEMENT_SNAPSHOT}`；基线竞品快照：`{BASELINE_SNAPSHOT}`。
- 属性过滤：同市场、包型、尺寸标签、材质组；不按相似名称模糊配对。
- 结果：{len(candidate_rows)} 条方向性候选配对，{len(cell_rows)} 个补充属性单元。
- 所有候选价格比较均为 `not_computed`，因为补充快照与竞品基线日期不同。
- 季节集合、WOC 和未知尺寸均保留为审计状态，不进入主文可比单元。

输出：

- `research_r1/outputs/comparable_pair_candidates.csv`
- `research_r1/outputs/comparable_cells_supplementary.csv`
""",
        encoding="utf-8",
    )
    print({"candidate_pairs": len(candidate_rows), "supplementary_cells": len(cell_rows)})


if __name__ == "__main__":
    main()
