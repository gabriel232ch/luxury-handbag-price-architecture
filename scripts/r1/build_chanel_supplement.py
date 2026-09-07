#!/usr/bin/env python3
"""Materialize the step-2 Chanel supplement from manually reviewed official pages.

The local sandbox cannot reach Chanel's Akamai-protected pages and the local
Playwright browser cannot start on this host. The records below therefore keep
the exact official URLs and the fields transcribed from the official page
content returned by the web search fallback. This script never changes the
2026-08-15 baseline observations or R1 calculations.
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
R1 = ROOT / "research_r1"
DATA = R1 / "data"
SNAPSHOT = "supplementary_current_2026-09-07"
OBSERVED_AT = "2026-09-07T10:18:05+08:00"
SOURCE_DATE = "2026-09-07"


def product(
    product_id: str,
    family: str,
    model: str,
    size_label: str,
    use_tag: str,
    bag_type: str,
    reference: str,
    material_raw: str,
    color: str,
    dimensions_cm: str,
    regular_special: str,
    collection_label: str,
    fr_price: int,
    fr_title: str,
    fr_url: str,
    us_price: int,
    us_title: str,
    us_url: str,
    notes: str = "",
) -> dict:
    return {
        "product_id": product_id,
        "brand": "Chanel",
        "family": family,
        "model": model,
        "size_label": size_label,
        "use_tag": use_tag,
        "bag_type": bag_type,
        "canonical_reference": reference,
        "material_raw": material_raw,
        "material_group": "leather",
        "color": color,
        "dimensions_cm": dimensions_cm,
        "regular_special": regular_special,
        "collection_label": collection_label,
        "availability_status": "contact_or_boutique",
        "identity_status": "verified_official_reference_and_attributes",
        "fr": {
            "market": "FR",
            "currency": "EUR",
            "price": fr_price,
            "title": fr_title,
            "url": fr_url,
        },
        "us": {
            "market": "US",
            "currency": "USD",
            "price": us_price,
            "title": us_title,
            "url": us_url,
        },
        "notes": notes,
    }


PRODUCTS = [
    product(
        "CH-SUP-255-A37586-B23746-94305", "2.55", "2.55 Handbag", "unknown", "flap", "flap",
        "A37586-B23746-94305", "Lambskin & Gold-Tone Metal", "Black", "16 x 24 x 7.5 cm",
        "seasonal_collection", "Spring Summer 2026", 12500,
        "Spring Summer 2026 2.55 Handbag Lambskin & Gold-Tone Metal Black",
        "https://www.chanel.com/fr/mode/p/A37586B2374694305/sac-2-55-agneau-metal-dore/", 13800,
        "Spring Summer 2026 2.55 Handbag Lambskin & Gold-Tone Metal Black",
        "https://www.chanel.com/us/fashion/p/A37586B2374694305/2-55-handbag-lambskin-gold-tone-metal/",
        "Seasonal collection row; keep outside a regular-core headline unless sensitivity is explicit.",
    ),
    product(
        "CH-SUP-255-A37586-Y04634-C3906", "2.55", "2.55 Handbag", "unknown", "flap", "flap",
        "A37586-Y04634-C3906", "Aged Calfskin & Gold-Tone Metal", "Black & Burgundy", "16 x 24 x 7.5 cm",
        "not_disclosed", "", 10500,
        "2.55 Handbag Aged Calfskin & Gold-Tone Metal Black & Burgundy",
        "https://www.chanel.com/fr/mode/p/A37586Y04634C3906/sac-2-55-veau-vieilli-metal-dore/", 11700,
        "2.55 Handbag Aged Calfskin & Gold-Tone Metal Black & Burgundy",
        "https://www.chanel.com/us/fashion/p/A37586Y04634C3906/2-55-handbag-aged-calfskin-gold-tone-metal/",
    ),
    product(
        "CH-SUP-BOY-A67085-Y09953-94305", "Boy", "Small BOY CHANEL Handbag", "small", "flap", "flap",
        "A67085-Y09953-94305", "Calfskin & Ruthenium-Finish Metal", "Black", "12 x 20.5 x 8.5 cm",
        "not_disclosed", "", 6200,
        "Small BOY CHANEL Calfskin & Ruthenium-Finish Metal Black",
        "https://www.chanel.com/fr/mode/p/A67085Y0995394305/petit-sac-boy-chanel-veau-metal-finition-ruthenium/", 6900,
        "Small BOY CHANEL Handbag Calfskin & Ruthenium-Finish Metal Black",
        "https://www.chanel.com/us/fashion/p/A67085Y0995394305/small-boy-chanel-handbag-calfskin-ruthenium-finish-metal/",
    ),
    product(
        "CH-SUP-BOY-A67086-Y09953-94305", "Boy", "BOY CHANEL Handbag", "standard", "flap", "flap",
        "A67086-Y09953-94305", "Calfskin & Ruthenium-Finish Metal", "Black", "15 x 25 x 9 cm",
        "not_disclosed", "", 6900,
        "BOY CHANEL Calfskin & Ruthenium-Finish Metal Black",
        "https://www.chanel.com/fr/mode/p/A67086Y0995394305/sac-boy-chanel-veau-metal-finition-ruthenium/", 7400,
        "BOY CHANEL Handbag Calfskin & Ruthenium-Finish Metal Black",
        "https://www.chanel.com/us/fashion/p/A67086Y0995394305/boy-chanel-handbag-calfskin-ruthenium-finish-metal/",
    ),
    product(
        "CH-SUP-19-AS1160-B04852-94305", "Chanel 19", "CHANEL 19 Handbag", "standard", "shoulder", "shoulder",
        "AS1160-B04852-94305", "Shiny Lambskin, Gold-Tone, Silver-Tone & Ruthenium-Finish Metal", "Black", "16 x 26 x 9 cm",
        "not_disclosed", "", 6650,
        "CHANEL 19 Shiny Lambskin, Gold-Tone, Silver-Tone & Ruthenium-Finish Metal Black",
        "https://www.chanel.com/fr/mode/p/AS1160B0485294305/sac-chanel-19-agneau-brillant-metal-dore-argente-finition-ruthenium/", 7200,
        "CHANEL 19 Handbag Shiny Lambskin, Gold-Tone, Silver-Tone & Ruthenium-Finish Metal Black",
        "https://www.chanel.com/us/fashion/p/AS1160B0485294305/chanel-19-handbag-shiny-lambskin-gold-tone-silver-tone-ruthenium-finish-metal/",
    ),
    product(
        "CH-SUP-19-AS1161-B04852-94305", "Chanel 19", "CHANEL 19 Large Handbag", "large", "shoulder", "shoulder",
        "AS1161-B04852-94305", "Shiny Lambskin, Gold-Tone, Silver-Tone & Ruthenium-Finish Metal", "Black", "20 x 30 x 10 cm",
        "not_disclosed", "", 7250,
        "CHANEL 19 Large Shiny Lambskin, Gold-Tone, Silver-Tone & Ruthenium-Finish Metal Black",
        "https://www.chanel.com/fr/mode/p/AS1161B0485294305/grand-sac-chanel-19-agneau-brillant-metal-dore-argente-finition-ruthenium/", 7900,
        "CHANEL 19 Large Handbag Shiny Lambskin, Gold-Tone, Silver-Tone & Ruthenium-Finish Metal Black",
        "https://www.chanel.com/us/fashion/p/AS1161B0485294305/chanel-19-large-handbag-shiny-lambskin-gold-tone-silver-tone-ruthenium-finish-metal/",
    ),
    product(
        "CH-SUP-22-AS3980-B19059-94305", "Chanel 22", "CHANEL 22 Mini Handbag", "mini", "shoulder", "hobo",
        "AS3980-B19059-94305", "Shiny Calfskin & Gold-Tone Metal", "Black", "20 x 19 x 6 cm",
        "not_disclosed", "", 5050,
        "Mini CHANEL 22 Shiny Calfskin & Gold-Tone Metal Black",
        "https://www.chanel.com/fr/mode/p/AS3980B1905994305/mini-sac-chanel-22-veau-brillant-metal-dore/", 5500,
        "CHANEL 22 Mini Handbag Shiny Calfskin & Gold-Tone Metal Black",
        "https://www.chanel.com/us/fashion/p/AS3980B1905994305/chanel-22-mini-handbag-shiny-calfskin-gold-tone-metal/",
    ),
    product(
        "CH-SUP-22-AS3261-B19059-94305", "Chanel 22", "CHANEL 22 Handbag", "standard", "shoulder", "hobo",
        "AS3261-B19059-94305", "Shiny Calfskin & Gold-Tone Metal", "Black", "36 x 42 x 8 cm",
        "not_disclosed", "", 5950,
        "CHANEL 22 Shiny Calfskin & Gold-Tone Metal Black",
        "https://www.chanel.com/fr/mode/p/AS3261B1905994305/sac-chanel-22-veau-brillant-metal-dore/", 6400,
        "CHANEL 22 Handbag Shiny Calfskin & Gold-Tone Metal Black",
        "https://www.chanel.com/us/fashion/p/AS3261B1905994305/chanel-22-handbag-shiny-calfskin-gold-tone-metal/",
    ),
    product(
        "CH-SUP-25-AS5631-B20304-10601", "Chanel 25", "CHANEL 25 Mini Handbag", "mini", "shoulder", "hobo",
        "AS5631-B20304-10601", "Grained Calfskin & Gold-Tone Metal", "White", "20 x 22 x 12.5 cm",
        "seasonal_collection", "Spring Summer 2026", 5600,
        "Spring Summer 2026 CHANEL 25 Mini Handbag Grained Calfskin & Gold-Tone Metal White",
        "https://www.chanel.com/fr/mode/p/AS5631B2030410601/mini-sac-chanel-25-veau-graine-metal-dore/", 6300,
        "Spring Summer 2026 CHANEL 25 Mini Handbag Grained Calfskin & Gold-Tone Metal White",
        "https://www.chanel.com/us/fashion/p/AS5631B2030410601/chanel-25-mini-handbag-grained-calfskin-gold-tone-metal/",
        "Seasonal collection row; keep outside a regular-core headline unless sensitivity is explicit.",
    ),
    product(
        "CH-SUP-25-AS5311-B20304-94305", "Chanel 25", "CHANEL 25 Medium Handbag", "medium", "shoulder", "hobo",
        "AS5311-B20304-94305", "Grained Calfskin & Gold-Tone Metal", "Black", "40 x 30 x 15 cm",
        "not_disclosed", "", 6400,
        "CHANEL 25 Medium Grained Calfskin & Gold-Tone Metal Black",
        "https://www.chanel.com/fr/mode/p/AS5311B2030494305/moyen-sac-chanel-25-veau-graine-metal-dore/", 7000,
        "CHANEL 25 Medium Handbag Grained Calfskin & Gold-Tone Metal Black",
        "https://www.chanel.com/us/fashion/p/AS5311B2030494305/chanel-25-medium-handbag-grained-calfskin-gold-tone-metal/",
    ),
    product(
        "CH-SUP-WOC-AP4241-Y01480-C3906", "WOC", "Classic Wallet on Chain", "small", "small-leather-goods", "small_leather_goods",
        "AP4241-Y01480-C3906", "Lambskin & Silver-Tone Metal", "Black & Burgundy", "12.3 x 19.2 x 3.5 cm",
        "not_disclosed", "", 3550,
        "Classic Wallet on Chain Lambskin & Silver-Tone Metal Black & Burgundy",
        "https://www.chanel.com/fr/mode/p/AP4241Y01480C3906/wallet-on-chain-classique-agneau-metal-argente/", 3850,
        "Classic Wallet on Chain Lambskin & Silver-Tone Metal Black & Burgundy",
        "https://www.chanel.com/us/fashion/p/AP4241Y01480C3906/classic-wallet-on-chain-lambskin-silver-tone-metal/",
        "Sensitivity only: WOC is a small leather good and is outside the main handbag denominator.",
    ),
]


def source_id(market: str, reference: str) -> str:
    safe = reference.replace("-", "")
    return f"SRC-SUPP-CH-{market}-{safe}"


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_csv_with_stable_header(path: Path, rows: list[dict], fields: list[str]) -> None:
    """Keep the pre-existing placeholder header byte-stable and append LF rows."""
    path.parent.mkdir(parents=True, exist_ok=True)
    header = ",".join(fields).encode("utf-8") + b"\r\n"
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
    writer.writerows(rows)
    path.write_bytes(header + buffer.getvalue().encode("utf-8"))


def append_registry_rows(path: Path, existing: list[dict[str, str]], rows: list[dict[str, str]], fields: list[str]) -> None:
    """Preserve the registry's existing line endings and append new rows as LF."""
    if not path.exists():
        write_csv(path, [*existing, *rows], fields)
        return
    if not rows:
        return
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
    writer.writerows(rows)
    raw = path.read_bytes()
    if raw and not raw.endswith(b"\n"):
        raw += b"\n"
    path.write_bytes(raw + buffer.getvalue().encode("utf-8"))


def main() -> None:
    product_fields = [
        "product_id", "brand", "family", "model", "size_label", "use_tag", "bag_type",
        "canonical_reference", "material_raw", "material_group", "color", "dimensions_cm",
        "regular_special", "collection_label", "availability_status", "identity_status",
        "source_url_fr", "source_url_us", "notes",
    ]
    master_rows = []
    mapping_rows = []
    supplement_rows = []
    raw_rows = []
    registry_rows = []

    for item in PRODUCTS:
        master_rows.append({
            **{key: item[key] for key in product_fields if key in item},
            "source_url_fr": item["fr"]["url"],
            "source_url_us": item["us"]["url"],
        })
        fr_source = source_id("FR", item["canonical_reference"])
        us_source = source_id("US", item["canonical_reference"])
        mapping_rows.append({
            "mapping_id": f"MAP-{item['product_id']}",
            "product_id": item["product_id"],
            "brand": "Chanel",
            "canonical_reference": item["canonical_reference"],
            "fr_reference": item["canonical_reference"],
            "us_reference": item["canonical_reference"],
            "reference_match": "exact",
            "model_match": "same_product_family_and_model",
            "size_match": "same_reference_and_dimensions",
            "material_match": "same_material_family",
            "color_match": "same_color",
            "dimension_match": "same_dimensions_after_unit_conversion",
            "market_pair_status": "exact_cross_market_pair",
            "mapping_confidence": "HIGH",
            "source_id_fr": fr_source,
            "source_id_us": us_source,
            "notes": item["notes"],
        })
        for market_key in ("fr", "us"):
            market = item[market_key]["market"]
            currency = item[market_key]["currency"]
            source = source_id(market, item["canonical_reference"])
            observation_id = f"supp:CHANEL-{market}-{item['canonical_reference'].replace('-', '')}-20260907"
            inclusion = "accepted_supplementary"
            exclusion = ""
            if item["family"] == "WOC":
                inclusion = "sensitivity_only"
                exclusion = "WOC is outside the main handbag denominator"
            elif item["regular_special"] == "seasonal_collection":
                inclusion = "accepted_supplementary_seasonal"
                exclusion = "seasonal collection; exclude from regular-core headline unless sensitivity is explicit"
            supplement_rows.append({
                "observation_id": observation_id,
                "snapshot_id": SNAPSHOT,
                "brand": "Chanel",
                "market": market,
                "currency": currency,
                "observed_at": OBSERVED_AT,
                "source_effective_date": "",
                "source_id": source,
                "reference_code": item["canonical_reference"],
                "family": item["family"],
                "model": item["model"],
                "size_label": item["size_label"],
                "material_group": item["material_group"],
                "color": item["color"],
                "price_status": "numeric",
                "price": item[market_key]["price"],
                "comparison_group_id": f"{market}|{item['bag_type']}|{item['size_label']}|{item['material_group']}",
                "lineage_id": "",
                "inclusion_status": inclusion,
                "exclusion_reason": exclusion,
            })
            raw_rows.append({
                "record_id": observation_id,
                "source_url": item[market_key]["url"],
                "observed_at": OBSERVED_AT,
                "market": market,
                "retrieval_status": "accepted_manual_fallback",
                "extraction_method": "manual_official_search_result",
                "raw_title": item[market_key]["title"],
                "raw_price_text": f"{item[market_key]['price']} {currency}",
                "raw_material_text": item["material_raw"],
                "raw_color_text": item["color"],
                "raw_dimensions_text": item["dimensions_cm"],
                "raw_reference_text": item["canonical_reference"],
                "raw_collection_text": item["collection_label"],
                "manual_transcription_basis": "Official CHANEL product-page content returned by the web search fallback; URL preserved for review.",
                "notes": item["notes"],
            })
        for market_key in ("fr", "us"):
            market = item[market_key]["market"]
            registry_rows.append({
                "source_id": source_id(market, item["canonical_reference"]),
                "brand": "Chanel",
                "source_type": "official_product_page",
                "source_name": f"CHANEL {market} official product page (manual fallback)",
                "source_url": item[market_key]["url"],
                "archive_url": "",
                "source_effective_date": "",
                "accessed_at": SOURCE_DATE,
                "primary_or_secondary": "primary",
                "source_quality": "high_with_access_limit",
                "notes": "Local Playwright/curl access was blocked; fields transcribed from official page content returned by the web search fallback. No access-control bypass used.",
            })

    write_csv(DATA / "product_master.csv", master_rows, product_fields)
    write_csv(DATA / "sku_mapping.csv", mapping_rows, [
        "mapping_id", "product_id", "brand", "canonical_reference", "fr_reference", "us_reference",
        "reference_match", "model_match", "size_match", "material_match", "color_match", "dimension_match",
        "market_pair_status", "mapping_confidence", "source_id_fr", "source_id_us", "notes",
    ])
    write_csv_with_stable_header(DATA / "supplementary_current.csv", supplement_rows, [
        "observation_id", "snapshot_id", "brand", "market", "currency", "observed_at",
        "source_effective_date", "source_id", "reference_code", "family", "model", "size_label",
        "material_group", "color", "price_status", "price", "comparison_group_id", "lineage_id",
        "inclusion_status", "exclusion_reason",
    ])
    with (DATA / "supplementary_current_raw.jsonl").open("w", encoding="utf-8") as handle:
        for row in raw_rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    registry_path = R1 / "source_registry.csv"
    existing = []
    if registry_path.exists():
        with registry_path.open(newline="", encoding="utf-8") as handle:
            existing = list(csv.DictReader(handle))
    known = {row.get("source_id") for row in existing}
    missing = [row for row in registry_rows if row["source_id"] not in known]
    if missing:
        existing.extend(missing)
    registry_fields = [
        "source_id", "brand", "source_type", "source_name", "source_url", "archive_url",
        "source_effective_date", "accessed_at", "primary_or_secondary", "source_quality", "notes",
    ]
    append_registry_rows(registry_path, existing, missing, registry_fields)

    log = f"""# Chanel 定向补充采集记录（第 2 步）

## 范围

- 市场：法国（EUR）与美国（USD）。
- 快照：`{SNAPSHOT}`；不回填 `current_2026-08-15`。
- 家族：2.55、Boy、Chanel 19、Chanel 22、Chanel 25、WOC。
- 行粒度：官方参考号 × 市场 × 本次观察时间。

## 结果

- 11 个跨市场参考号，22 条市场观察；22 条均取得正数标价。
- 11 个 `sku_mapping` 均为同一参考号的 FR/US 精确配对，身份、材质、颜色和尺寸字段均来自官方页面内容。
- 2.55 的 Spring Summer 2026 行和 Chanel 25 Mini 的 Spring Summer 2026 行标为 `seasonal_collection`；WOC 标为 `sensitivity_only`，不进入手袋主分母。
- 本轮没有采集 Hermès、Louis Vuitton 或 Dior，也没有建立跨品牌配对。

## 方法与限制

本机直接 Playwright/HTTPS 访问被 Chanel 的边缘访问控制阻断；未使用 CAPTCHA、代理轮换、隐身或其他绕过方式。字段使用官方 Chanel 产品页内容的搜索结果进行人工转录，`extraction_method=manual_official_search_result`，并保留每个官方 URL。页面未明确价格生效日期，因此 `source_effective_date` 留空，观察日期仅表示页面读取日。

这批数据是补充快照，尚未合并进 R1 的价格输出；下一步才决定哪些行可进入产品属性筛选和竞品配对。

输出：

- `research_r1/data/supplementary_current_raw.jsonl`
- `research_r1/data/supplementary_current.csv`
- `research_r1/data/product_master.csv`
- `research_r1/data/sku_mapping.csv`
"""
    (DATA / "supplementary_collection_log.md").write_text(log, encoding="utf-8")
    print(json.dumps({
        "snapshot": SNAPSHOT,
        "products": len(PRODUCTS),
        "observations": len(supplement_rows),
        "numeric": sum(row["price_status"] == "numeric" for row in supplement_rows),
        "new_sources": len(missing),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
