#!/usr/bin/env python3
"""Create an explicit isolation inventory before cross-brand pairing."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "research_r1/data"
OUTPUT = DATA / "scope_isolation_2026-09-07_us.csv"
LOG = DATA / "scope_isolation_2026-09-07_us_audit.md"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def classify(row: dict[str, str], snapshot_id: str, market_scope: str) -> dict[str, str]:
    reasons: list[str] = []
    if row["family"].strip().upper() == "WOC" or row["bag_type"] == "small_leather_goods" or row["use_tag"] == "small-leather-goods":
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
    elif "regular_special_not_disclosed" in reasons:
        scope_status = "status_pending"
    else:
        scope_status = "screenable"

    dimension_status = "numeric" if row["dimensions_cm"].strip() else "unknown"
    if scope_status in {"sensitivity_only", "seasonal_excluded", "unknown_size"}:
        pairing_readiness = "blocked"
    elif dimension_status == "unknown":
        pairing_readiness = "conditional_dimension_review"
    elif scope_status == "status_pending":
        pairing_readiness = "conditional_regular_special_review"
    else:
        pairing_readiness = "ready"

    result = {
        "product_id": row["product_id"],
        "brand": row["brand"],
        "market_scope": market_scope,
        "snapshot_id": snapshot_id,
        "canonical_reference": row["canonical_reference"],
        "family": row["family"],
        "model": row["model"],
        "use_tag": row["use_tag"],
        "bag_type": row["bag_type"],
        "size_label": row["size_label"],
        "material_group": row["material_group"],
        "regular_special": row["regular_special"],
        "dimension_status": dimension_status,
        "scope_status": scope_status,
        "isolation_reason": ";".join(reasons),
        "pairing_readiness": pairing_readiness,
        "source_url_us": row["source_url_us"],
        "notes": row["notes"],
    }
    return result


def main() -> None:
    chanel = read(DATA / "product_master.csv")
    competitors = read(DATA / "product_master_competitors_2026-09-07_us.csv")
    rows = [classify(row, "supplementary_current_2026-09-07", "FR+US") for row in chanel]
    rows.extend(classify(row, "refresh_2026-09-07_us", "US") for row in competitors)
    fields = list(rows[0])
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    counts = {}
    for row in rows:
        counts[row["scope_status"]] = counts.get(row["scope_status"], 0) + 1
    reasons = {}
    for row in rows:
        for reason in filter(None, row["isolation_reason"].split(";")):
            reasons[reason] = reasons.get(reason, 0) + 1
    LOG.write_text(
        f"""# 2026-09-07 范围隔离清单

- 输入：Chanel `product_master.csv`（补充快照）和三品牌 `product_master_competitors_2026-09-07_us.csv`（同日美国快照）。
- 总行数：{len(rows)}。
- `scope_status` 计数：{counts}。
- 隔离原因计数：{reasons}。

规则：WOC 和小皮具仅保留为 sensitivity；明确季节款排除常规核心；尺寸为 `unknown` 的行阻断严格配对；`regular_special=not_disclosed` 不被猜成常规款，先标记为待核验。Dior 的数值尺寸缺失另标为 `conditional_dimension_review`，不在本步升级为主文比较。

本文件只完成范围隔离，不计算价格差、排名或竞品替代关系。下一步才使用 `pairing_readiness` 和同市场/同日期筛选重建配对审计。
""",
        encoding="utf-8",
    )
    print({"rows": len(rows), "scope_status": counts, "isolation_reason": reasons})


if __name__ == "__main__":
    main()
