from __future__ import annotations

import csv
import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "luxury_historical_pricing"
OBSERVED_AT = "2026-08-15T20:20:39+08:00"
COLLECTION_DATE = "2026-08-16"
REQUESTED_PERIOD = "2020-01-01 through 2026-08-16"
TZ_CN = timezone(timedelta(hours=8))
ACCESSED_AT = datetime.now(TZ_CN).isoformat(timespec="seconds")


FIELDS = [
    "observation_id",
    "brand",
    "product_lineage_id",
    "current_reference",
    "historical_reference",
    "product_name",
    "product_family",
    "product_role",
    "iconic_or_signature_status",
    "market",
    "country",
    "observation_date",
    "date_precision",
    "effective_date_if_known",
    "price",
    "currency",
    "price_status",
    "material",
    "color_if_material",
    "dimensions_raw",
    "width_cm",
    "height_cm",
    "depth_cm",
    "size_label",
    "collection_or_version",
    "continuity_status",
    "continuity_notes",
    "source_type",
    "source_name",
    "source_url",
    "archive_url_if_applicable",
    "source_publication_date",
    "extraction_method",
    "source_quality",
    "confidence",
    "source_ids",
    "conflict_flag",
    "notes",
]


def read_current(path: Path) -> dict[tuple[str, str], dict]:
    rows = {}
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            ref = row.get("official_sku_or_reference") or row.get("sku_or_reference")
            if not ref:
                continue
            market = row.get("market") or ""
            key = (ref, market)
            rows[key] = row
    return rows


CURRENT_FILES = {
    "Chanel": ROOT / "chanel_fr_us_handbags_current" / "clean_data.csv",
    "Hermès": ROOT / "luxury_competitor_pricing_current" / "clean" / "hermes_pricing_clean.csv",
    "Louis Vuitton": ROOT / "luxury_competitor_pricing_current" / "clean" / "louis_vuitton_pricing_clean.csv",
    "Dior": ROOT / "luxury_competitor_pricing_current" / "clean" / "dior_pricing_clean.csv",
}
CURRENT = {brand: read_current(path) for brand, path in CURRENT_FILES.items()}


def source(
    source_id: str,
    brand: str,
    lineage_id: str,
    source_type: str,
    source_name: str,
    original_url: str,
    source_date: str | None,
    primary_or_secondary: str,
    source_quality: str,
    notes: str = "",
):
    SOURCES[source_id] = {
        "source_id": source_id,
        "brand": brand,
        "product_lineage_id": lineage_id,
        "source_type": source_type,
        "source_name": source_name,
        "original_url": original_url,
        "archive_url": "",
        "source_date": source_date or "",
        "accessed_at": ACCESSED_AT,
        "primary_or_secondary": primary_or_secondary,
        "source_quality": source_quality,
        "notes": notes,
    }


SOURCES: dict[str, dict] = {}


LINEAGES = [
    {
        "product_lineage_id": "CH-C01",
        "brand": "Chanel",
        "product_family": "Classic 11.12",
        "current_reference": "A01112-Y04059-U8390",
        "market_refs": {"FR": "A01112-Y04059-U8390", "US": "A01112-Y04059-U8390"},
        "historical_name": "Medium Chanel Classic / Classic Flap",
        "current_name": "Sac classique 11.12 / Classic 11.12 Handbag",
        "product_role": "signature_icon",
        "iconic_or_signature_status": "signature_in_current_dataset",
        "continuity_status": "SAME_MODEL_CONTINUOUS",
        "continuity_evidence": "Source tables identify the medium Classic / Classic Flap; current official anchor is the same 25.5 cm Classic 11.12 form. Historical references are not shown.",
        "confidence": "HIGH",
        "notes": "France historical series is usable. US historical coverage not found in the accepted sources; current US anchor retained.",
    },
    {
        "product_lineage_id": "CH-C02",
        "brand": "Chanel",
        "product_family": "Small Classic",
        "current_reference": "A01113-Y01864-C3906",
        "market_refs": {"FR": "A01113-Y01864-C3906", "US": "A01113-Y01864-C3906"},
        "historical_name": "Chanel Classic Small",
        "current_name": "Petit sac classique / Small Classic Handbag",
        "product_role": "signature_icon",
        "iconic_or_signature_status": "signature_in_current_dataset",
        "continuity_status": "SAME_MODEL_CONTINUOUS",
        "continuity_evidence": "2022–2024 table labels the same Small Classic size; current official anchor is a 23 cm Small Classic.",
        "confidence": "HIGH",
        "notes": "France historical series is usable. US historical coverage not found in the accepted sources; current US anchor retained.",
    },
    {
        "product_lineage_id": "CH-C03",
        "brand": "Chanel",
        "product_family": "Mini Classic",
        "current_reference": "A35200-Y04059-94305",
        "market_refs": {"FR": "A35200-Y04059-94305", "US": "A35200-Y04059-94305"},
        "historical_name": "Chanel Classic Square Mini",
        "current_name": "Mini sac classique / Mini Classic Handbag",
        "product_role": "signature_access",
        "iconic_or_signature_status": "signature_in_current_dataset",
        "continuity_status": "SAME_MODEL_CONTINUOUS",
        "continuity_evidence": "Historical source labels the square mini; current official anchor is the 13.5 × 17 × 8 cm Mini Classic, distinct from the rectangular mini.",
        "confidence": "HIGH",
        "notes": "France historical series is usable. US historical coverage not found in the accepted sources; current US anchor retained.",
    },
    {
        "product_lineage_id": "CH-C04",
        "brand": "Chanel",
        "product_family": "Mini Classic",
        "current_reference": "A69900-Y04059-94305",
        "market_refs": {"FR": "A69900-Y04059-94305", "US": "A69900-Y04059-94305"},
        "historical_name": "Chanel Classic Rectangular Mini",
        "current_name": "Mini sac classique / Mini Classic Handbag",
        "product_role": "signature_access",
        "iconic_or_signature_status": "signature_in_current_dataset",
        "continuity_status": "SAME_MODEL_CONTINUOUS",
        "continuity_evidence": "Historical source labels the rectangular mini; current official anchor is the 12 × 20 × 6 cm Mini Classic, distinct from the square mini.",
        "confidence": "HIGH",
        "notes": "France historical series is usable. US historical coverage not found in the accepted sources; current US anchor retained.",
    },
    {
        "product_lineage_id": "HM-H01",
        "brand": "Hermès",
        "product_family": "Geta",
        "current_reference": "H085408CKAW",
        "market_refs": {"FR": "H085408CKAW", "US": "H085408CKAW"},
        "historical_name": "Hermès Geta",
        "current_name": "Sac Hermès Geta / Hermès Geta bag",
        "product_role": "core_upper_core",
        "iconic_or_signature_status": "not_flagged_in_current_dataset",
        "continuity_status": "SAME_MODEL_CONTINUOUS",
        "continuity_evidence": "Historical sources identify the Geta model; current official anchors use the same official reference in France and the United States.",
        "confidence": "MEDIUM",
        "notes": "France includes a 2023 source conflict (4,550 vs 5,550 EUR); both are retained. US historical coverage is available for 2023–2024.",
    },
    {
        "product_lineage_id": "HM-H02",
        "brand": "Hermès",
        "product_family": "Jypsière",
        "current_reference": "H088004CC7U (FR); H087119CKAD (US)",
        "market_refs": {"FR": "H088004CC7U", "US": "H087119CKAD"},
        "historical_name": "Hermès Mini Jypsiere / Jypsière Mini",
        "current_name": "Sac Jypsière mini / Jypsiere mini Toile & Cuir bag",
        "product_role": "core_upper_core",
        "iconic_or_signature_status": "not_flagged_in_current_dataset",
        "continuity_status": "MODEL_SUCCESSOR",
        "continuity_evidence": "Historical source identifies Mini Jypsiere in Swift; current France anchor is calfskin and current US anchor is H canvas/Swift with different references.",
        "confidence": "MEDIUM",
        "notes": "France historical series is usable for 2023–2024. US current anchor retained but historical US coverage not found.",
    },
    {
        "product_lineage_id": "LV-L01",
        "brand": "Louis Vuitton",
        "product_family": "Speedy",
        "current_reference": "M2A038",
        "market_refs": {"FR": "M2A038", "US": "M2A038"},
        "historical_name": "Louis Vuitton Speedy Bandouliere 25 canvas",
        "current_name": "Sac / Speedy Bandoulière 25",
        "product_role": "signature_access",
        "iconic_or_signature_status": "signature_in_current_dataset",
        "continuity_status": "MODEL_SUCCESSOR",
        "continuity_evidence": "Historical source identifies Speedy Bandouliere 25 canvas; current anchor is the same model/size with Monogram Dune canvas and a different reference.",
        "confidence": "MEDIUM",
        "notes": "Model continuity is strong, but current special-canvas version is not treated as an exact SKU.",
    },
    {
        "product_lineage_id": "LV-L02",
        "brand": "Louis Vuitton",
        "product_family": "Speedy",
        "current_reference": "M2A099",
        "market_refs": {"FR": "M2A099", "US": "M2A099"},
        "historical_name": "Louis Vuitton Speedy Bandouliere 20 Empreinte",
        "current_name": "Sac Speedy Bandoulière 20",
        "product_role": "core",
        "iconic_or_signature_status": "signature_in_current_dataset",
        "continuity_status": "SAME_MODEL_CONTINUOUS",
        "continuity_evidence": "Historical table identifies Speedy Bandouliere 20 empreinte; current France anchor is the same 20 size and Monogram Empreinte material family.",
        "confidence": "MEDIUM",
        "notes": "France-only current anchor in the supplied dataset; US historical/current match not accepted.",
    },
    {
        "product_lineage_id": "LV-L03",
        "brand": "Louis Vuitton",
        "product_family": "Alma",
        "current_reference": "M3A842 (FR); M46990 (US)",
        "market_refs": {"FR": "M3A842", "US": "M46990"},
        "historical_name": "Louis Vuitton Alma BB canvas",
        "current_name": "Alma BB",
        "product_role": "accessible_core",
        "iconic_or_signature_status": "not_flagged_in_current_dataset",
        "continuity_status": "MODEL_SUCCESSOR",
        "continuity_evidence": "Historical source identifies Alma BB canvas; current US anchor is Monogram but France anchor is an other-leathers version, so the lineage is not treated as exact across markets.",
        "confidence": "MEDIUM",
        "notes": "Both FR and US historical prices are retained with material/version caveat.",
    },
    {
        "product_lineage_id": "LV-L04",
        "brand": "Louis Vuitton",
        "product_family": "Neverfull",
        "current_reference": "M46987 (US)",
        "market_refs": {"FR": "M46987", "US": "M46987"},
        "historical_name": "Louis Vuitton Neverfull MM Monogram canvas",
        "current_name": "Neverfull MM",
        "product_role": "accessible_core",
        "iconic_or_signature_status": "not_flagged_in_current_dataset",
        "continuity_status": "SAME_MODEL_CONTINUOUS",
        "continuity_evidence": "Historical sources identify Neverfull MM Monogram/canvas; current US anchor is official M46987 in Monogram canvas.",
        "confidence": "HIGH",
        "notes": "Current France anchor was not present in the supplied current capture; France historical observations are retained and marked current-FR anchor incomplete.",
    },
    {
        "product_lineage_id": "DI-D01",
        "brand": "Dior",
        "product_family": "Saddle",
        "current_reference": "M0457CUQW_M900",
        "market_refs": {"FR": "M0457CUQW_M900", "US": "M0457CUQW_M900"},
        "historical_name": "Dior Saddle Bag",
        "current_name": "Saddle Small Bag with Strap",
        "product_role": "signature_icon",
        "iconic_or_signature_status": "signature_in_current_dataset",
        "continuity_status": "MODEL_SUCCESSOR",
        "continuity_evidence": "Historical US source identifies Dior Saddle Bag but does not state size/material; current official anchor is the small grained-calfskin version.",
        "confidence": "MEDIUM",
        "notes": "US historical series is usable for 2022–2023 with size/material caveat; France current anchor retained.",
    },
    {
        "product_lineage_id": "DI-D02",
        "brand": "Dior",
        "product_family": "Dior Book Tote",
        "current_reference": "M1325OWHP_M900",
        "market_refs": {"FR": "M1325OWHP_M900", "US": "M1325OWHP_M900"},
        "historical_name": "Small Dior Book Tote Oblique Canvas",
        "current_name": "Small Dior Book Tote",
        "product_role": "signature_core",
        "iconic_or_signature_status": "signature_in_current_dataset",
        "continuity_status": "MODEL_SUCCESSOR",
        "continuity_evidence": "Historical source gives exact small size/dimensions for Oblique Canvas; current anchor is the same size in Macrocannage calfskin.",
        "confidence": "MEDIUM",
        "notes": "Material/version difference is documented; do not treat as exact-SKU continuity.",
    },
    {
        "product_lineage_id": "DI-D03",
        "brand": "Dior",
        "product_family": "Dior Book Tote",
        "current_reference": "M1324OWHP_M51U",
        "market_refs": {"FR": "M1324OWHP_M51U", "US": "M1324OWHP_M51U"},
        "historical_name": "Medium Dior Book Tote Oblique Canvas",
        "current_name": "Medium Dior Book Tote",
        "product_role": "signature_core",
        "iconic_or_signature_status": "signature_in_current_dataset",
        "continuity_status": "MODEL_SUCCESSOR",
        "continuity_evidence": "Historical source gives exact medium size/dimensions for Oblique Canvas; current anchor is the same size in Macrocannage calfskin.",
        "confidence": "MEDIUM",
        "notes": "France current anchor is numeric; US current price was unresolved in the supplied current capture.",
    },
]

LINEAGE_BY_ID = {x["product_lineage_id"]: x for x in LINEAGES}


def current_url(brand: str, row: dict) -> str:
    return row.get("source_url", "")


def market_info(market: str):
    return ("France", "EUR") if market == "FR" else ("United States", "USD")


def current_anchor(lineage: dict, market: str) -> dict:
    brand = lineage["brand"]
    ref = lineage["market_refs"].get(market)
    row = CURRENT[brand].get((ref, market))
    if row is None and market == "FR":
        row = CURRENT[brand].get((ref, "France"))
    if row is None and market == "US":
        row = CURRENT[brand].get((ref, "United States"))
    return row or {}


def official_source_id(lineage: dict, market: str) -> str:
    return f"SRC-{lineage['product_lineage_id']}-CURRENT-{market}"


def add_official_sources():
    for lineage in LINEAGES:
        for market in ("FR", "US"):
            row = current_anchor(lineage, market)
            if not row:
                continue
            source(
                official_source_id(lineage, market),
                lineage["brand"],
                lineage["product_lineage_id"],
                "official_current_product_page",
                f"Official localized current product page captured in supplied 2026 current dataset ({market})",
                row.get("source_url", ""),
                OBSERVED_AT[:10],
                "primary",
                "HIGH",
                "Current 2026 anchor inherited from the supplied official localized product-page capture; not reinterpreted as a historical source.",
            )


HIST: list[dict] = []


def add_hist(
    lineage_id: str,
    market: str,
    date: str,
    price: float | int,
    source_id: str,
    historical_reference: str,
    source_excerpt: str,
    *,
    material: str = "",
    collection: str = "",
    confidence: str = "MEDIUM",
    source_quality: str = "MEDIUM",
    date_precision: str = "year",
    effective_date: str = "",
    conflict_flag: bool = False,
    notes: str = "",
):
    lineage = LINEAGE_BY_ID[lineage_id]
    country, currency = market_info(market)
    row = current_anchor(lineage, market)
    HIST.append({
        "lineage_id": lineage_id,
        "market": market,
        "observation_date": date,
        "date_precision": date_precision,
        "price": price,
        "currency": currency,
        "historical_reference": historical_reference,
        "source_id": source_id,
        "source_excerpt": source_excerpt,
        "material": material,
        "collection": collection,
        "confidence": confidence,
        "source_quality": source_quality,
        "effective_date": effective_date,
        "conflict_flag": conflict_flag,
        "notes": notes,
        "current_row": row,
        "country": country,
    })


# Chanel: Bagaholic's 2024 EU table covers 2022–2024; the 2020 square-mini value is
# retained separately from PurseBop. Values are nominal EUR list prices.
source("SRC-CH-C01-BAGAHOLIC-2024", "Chanel", "CH-C01", "historical_secondary_table", "Bagaholic Chanel Classic EU price reference guide 2024", "https://lvbagaholic.com/fr/blogs/blog-de-bagaholic-1/chanel-classic-bag-sac-eu-prix-list-reference-guide", "2024", "secondary", "MEDIUM", "Table rows for 2022–2024 medium Classic.")
source("SRC-CH-C02-BAGAHOLIC-2024", "Chanel", "CH-C02", "historical_secondary_table", "Bagaholic Chanel Classic EU price reference guide 2024", "https://lvbagaholic.com/fr/blogs/blog-de-bagaholic-1/chanel-classic-bag-sac-eu-prix-list-reference-guide", "2024", "secondary", "MEDIUM", "Table rows for 2022–2024 Small Classic.")
source("SRC-CH-C03-BAGAHOLIC-2024", "Chanel", "CH-C03", "historical_secondary_table", "Bagaholic Chanel Classic EU price reference guide 2024", "https://lvbagaholic.com/fr/blogs/blog-de-bagaholic-1/chanel-classic-bag-sac-eu-prix-list-reference-guide", "2024", "secondary", "MEDIUM", "Table rows for 2022–2024 square mini.")
source("SRC-CH-C04-BAGAHOLIC-2024", "Chanel", "CH-C04", "historical_secondary_table", "Bagaholic Chanel Classic EU price reference guide 2024", "https://lvbagaholic.com/fr/blogs/blog-de-bagaholic-1/chanel-classic-bag-sac-eu-prix-list-reference-guide", "2024", "secondary", "MEDIUM", "Table rows for 2022–2024 rectangular mini.")
source("SRC-CH-C03-PURSEBOP-2020", "Chanel", "CH-C03", "historical_secondary_table", "PurseBop Chanel price increase 2020", "https://www.pursebop.com/chanel-admits-to-price-increase-here-are-the-new-prices-2020/", "2020", "secondary", "MEDIUM", "2020 square-mini price point; source table also includes a prior price.")

for d, p in [("2022", 8990), ("2023", 9700), ("2024", 10300)]:
    add_hist("CH-C01", "FR", d, p, "SRC-CH-C01-BAGAHOLIC-2024", "Chanel Classic medium / M-L flap", f"Bagaholic table: medium Classic {d} EUR {p}.")
for d, p in [("2022", 8450), ("2023", 9300), ("2024", 9900)]:
    add_hist("CH-C02", "FR", d, p, "SRC-CH-C02-BAGAHOLIC-2024", "Chanel Classic Small", f"Bagaholic table: Small Classic {d} EUR {p}.")
add_hist("CH-C03", "FR", "2020", 3350, "SRC-CH-C03-PURSEBOP-2020", "Mini Classic Flap (Square)", "PurseBop 2020 table: Mini Classic Flap (Square) new price EUR 3,350.", date_precision="year", notes="Observed post-change price; exact effective date is not encoded in the row.")
for d, p in [("2022", 4150), ("2023", 4500), ("2024", 4750)]:
    add_hist("CH-C03", "FR", d, p, "SRC-CH-C03-BAGAHOLIC-2024", "Chanel Classic square mini", f"Bagaholic table: square mini {d} EUR {p}.")
for d, p in [("2022", 4350), ("2023", 4700), ("2024", 4950)]:
    add_hist("CH-C04", "FR", d, p, "SRC-CH-C04-BAGAHOLIC-2024", "Chanel Classic rectangular mini", f"Bagaholic table: rectangular mini {d} EUR {p}.")


# Hermès: public secondary price tables. The Geta 2023 discrepancy is preserved.
source("SRC-HM-H01-PURSEBOP-EU-2024", "Hermès", "HM-H01", "historical_secondary_table", "PurseBop confirmed Hermès Europe prices 2024", "https://www.pursebop.com/new-confirmed-hermes-prices-in-europe-2024/", "2024", "secondary", "MEDIUM", "Geta Europe table reports 2023 EUR 4,550 and 2024 EUR 4,850.")
source("SRC-HM-H01-LUXEFRONT-2022", "Hermès", "HM-H01", "historical_secondary_table", "Luxe Front Hermès bag prices", "https://luxefront.com/2022/12/02/hermes-bag-prices/", "2022-12-02", "secondary", "MEDIUM", "Page includes 2022 table and January 2023 update; Geta 2023 update reports EUR 5,550.")
source("SRC-HM-H01-PURSEBLOG-US-2024", "Hermès", "HM-H01", "historical_secondary_table", "PurseBlog Hermès price increase 2024", "https://www.purseblog.com/hermes/hermes-price-increase-2024-its-here-already/", "2024", "secondary", "MEDIUM", "Geta US table reports 2023 USD 5,950 and 2024 USD 6,450.")
source("SRC-HM-H02-PURSEBOP-EU-2024", "Hermès", "HM-H02", "historical_secondary_table", "PurseBop confirmed Hermès Europe prices 2024", "https://www.pursebop.com/new-confirmed-hermes-prices-in-europe-2024/", "2024", "secondary", "MEDIUM", "Mini Jypsiere Europe table reports 2023 EUR 5,500 and 2024 EUR 6,000.")

add_hist("HM-H01", "FR", "2022", 4550, "SRC-HM-H01-LUXEFRONT-2022", "Geta Bag", "Luxe Front table: Geta Bag 2022 EUR 4,550.")
add_hist("HM-H01", "FR", "2023", 5550, "SRC-HM-H01-LUXEFRONT-2022", "Geta", "Luxe Front January 2023 update: Geta EUR 5,550.", conflict_flag=True, notes="Conflicts with the separate PurseBop 2024 table's 2023 EUR 4,550 value; both retained.")
add_hist("HM-H01", "FR", "2023", 4550, "SRC-HM-H01-PURSEBOP-EU-2024", "Geta", "PurseBop Europe table: Geta 2023 EUR 4,550.", conflict_flag=True, notes="Conflicts with Luxe Front's January 2023 update reporting EUR 5,550; both retained.")
add_hist("HM-H01", "FR", "2024", 4850, "SRC-HM-H01-PURSEBOP-EU-2024", "Geta", "PurseBop Europe table: Geta 2024 EUR 4,850.")
add_hist("HM-H01", "US", "2023", 5950, "SRC-HM-H01-PURSEBLOG-US-2024", "Geta", "PurseBlog US table: Geta 2023 USD 5,950.")
add_hist("HM-H01", "US", "2024", 6450, "SRC-HM-H01-PURSEBLOG-US-2024", "Geta", "PurseBlog US table: Geta 2024 USD 6,450.")
add_hist("HM-H02", "FR", "2023", 5500, "SRC-HM-H02-PURSEBOP-EU-2024", "Mini Jypsiere / Jypsiere Mini", "PurseBop Europe table: Mini Jypsiere 2023 EUR 5,500.", material="Swift", notes="Current France anchor is calfskin; material/version difference is documented in lineage table.")
add_hist("HM-H02", "FR", "2024", 6000, "SRC-HM-H02-PURSEBOP-EU-2024", "Mini Jypsiere / Jypsiere Mini", "PurseBop Europe table: Mini Jypsiere 2024 EUR 6,000.", material="Swift", notes="Current France anchor is calfskin; material/version difference is documented in lineage table.")


# Louis Vuitton: source tables cover the long-running Speedy, Alma and Neverfull families.
source("SRC-LV-L01-BAGAHOLIC-2021", "Louis Vuitton", "LV-L01", "historical_secondary_table", "Bagaholic Louis Vuitton price increase January 2021", "https://lvbagaholic.com/blogs/lv_bagaholic/louis-vuitton-increases-prices-worldwide-in-january-2021", "2021", "secondary", "MEDIUM", "Speedy B25 old/new 2021 prices in EUR and USD.")
source("SRC-LV-L01-LUXEFRONT-2022", "Louis Vuitton", "LV-L01", "historical_secondary_table", "Luxe Front Louis Vuitton price list", "https://luxefront.com/2022/12/13/louis-vuitton-bag-price-list-complete-guide-usd-eur/", "2022-12-13", "secondary", "MEDIUM", "Speedy Bandouliere 25 canvas 2022/2023 table.")
source("SRC-LV-L01-PURSEBOP-2024", "Louis Vuitton", "LV-L01", "historical_secondary_table", "PurseBop Louis Vuitton global price increase 2024", "https://www.pursebop.com/louis-vuitton-global-price-increase-2024/", "2024", "secondary", "MEDIUM", "Speedy Bandouliere 25 Europe and US 2024 table.")
source("SRC-LV-L02-LUXEFRONT-2022", "Louis Vuitton", "LV-L02", "historical_secondary_table", "Luxe Front Louis Vuitton price list", "https://luxefront.com/2022/12/13/louis-vuitton-bag-price-list-complete-guide-usd-eur/", "2022-12-13", "secondary", "MEDIUM", "Speedy Bandouliere 20 empreinte 2022/2023 table.")
source("SRC-LV-L03-BAGAHOLIC-2021", "Louis Vuitton", "LV-L03", "historical_secondary_table", "Bagaholic Louis Vuitton price increase January 2021", "https://lvbagaholic.com/blogs/lv_bagaholic/louis-vuitton-increases-prices-worldwide-in-january-2021", "2021", "secondary", "MEDIUM", "Alma BB canvas old/new 2021 prices in EUR and USD.")
source("SRC-LV-L03-LUXEFRONT-2022", "Louis Vuitton", "LV-L03", "historical_secondary_table", "Luxe Front Louis Vuitton price list", "https://luxefront.com/2022/12/13/louis-vuitton-bag-price-list-complete-guide-usd-eur/", "2022-12-13", "secondary", "MEDIUM", "Alma BB canvas 2022/2023 table.")
source("SRC-LV-L03-PURSEBOP-2024", "Louis Vuitton", "LV-L03", "historical_secondary_table", "PurseBop Louis Vuitton global price increase 2024", "https://www.pursebop.com/louis-vuitton-global-price-increase-2024/", "2024", "secondary", "MEDIUM", "Alma BB 2024 table.")
source("SRC-LV-L04-BAGAHOLIC-2021", "Louis Vuitton", "LV-L04", "historical_secondary_table", "Bagaholic Louis Vuitton price increase January 2021", "https://lvbagaholic.com/blogs/lv_bagaholic/louis-vuitton-increases-prices-worldwide-in-january-2021", "2021", "secondary", "MEDIUM", "Neverfull MM old/new 2021 prices in EUR and USD.")
source("SRC-LV-L04-LUXEFRONT-2022", "Louis Vuitton", "LV-L04", "historical_secondary_table", "Luxe Front Louis Vuitton price list", "https://luxefront.com/2022/12/13/louis-vuitton-bag-price-list-complete-guide-usd-eur/", "2022-12-13", "secondary", "MEDIUM", "Neverfull MM canvas 2022/2023 table.")
source("SRC-LV-L04-PETITEINPARIS-2023", "Louis Vuitton", "LV-L04", "historical_secondary_table", "Petite in Paris Neverfull price guide", "https://petiteinparis.com/is-the-louis-vuitton-neverfull-worth-the-price/", "2023", "secondary", "MEDIUM", "Neverfull MM Monogram 2023 price in US and Europe.")

add_hist("LV-L01", "FR", "2021", 1180, "SRC-LV-L01-BAGAHOLIC-2021", "Speedy B 25", "Bagaholic Europe table: Speedy B 25 new 2021 EUR 1,180.", effective_date="2021-01-07", date_precision="year")
add_hist("LV-L01", "US", "2021", 1650, "SRC-LV-L01-BAGAHOLIC-2021", "Speedy B 25", "Bagaholic US table: Speedy B 25 new 2021 USD 1,650.", effective_date="2021-01-07", date_precision="year")
add_hist("LV-L01", "FR", "2022", 1390, "SRC-LV-L01-LUXEFRONT-2022", "Speedy Bandouliere 25 canvas", "Luxe Front table: Speedy Bandouliere 25 canvas 2022 EUR 1,390.")
add_hist("LV-L01", "US", "2022", 1820, "SRC-LV-L01-LUXEFRONT-2022", "Speedy Bandouliere 25 canvas", "Luxe Front table: Speedy Bandouliere 25 canvas 2022 USD 1,820.")
add_hist("LV-L01", "FR", "2023", 1450, "SRC-LV-L01-LUXEFRONT-2022", "Speedy Bandouliere 25 canvas", "Luxe Front table: Speedy Bandouliere 25 canvas 2023 EUR 1,450.")
add_hist("LV-L01", "FR", "2024", 1550, "SRC-LV-L01-PURSEBOP-2024", "Speedy Bandouliere 25", "PurseBop Europe table: Speedy Bandouliere 25 2024 EUR 1,550.")
add_hist("LV-L01", "US", "2024", 1820, "SRC-LV-L01-PURSEBOP-2024", "Speedy Bandouliere 25", "PurseBop US table: Speedy Bandouliere 25 2024 USD 1,820.")

add_hist("LV-L02", "FR", "2022", 1960, "SRC-LV-L02-LUXEFRONT-2022", "Speedy Bandouliere 20 empreinte", "Luxe Front table: Speedy Bandouliere 20 empreinte 2022 EUR 1,960.", material="Empreinte")
add_hist("LV-L02", "FR", "2023", 2050, "SRC-LV-L02-LUXEFRONT-2022", "Speedy Bandouliere 20 empreinte", "Luxe Front table: Speedy Bandouliere 20 empreinte 2023 EUR 2,050.", material="Empreinte")

add_hist("LV-L03", "FR", "2021", 1100, "SRC-LV-L03-BAGAHOLIC-2021", "Alma BB canvas", "Bagaholic Europe table: Alma BB canvas new 2021 EUR 1,100.", effective_date="2021-01-07")
add_hist("LV-L03", "US", "2021", 1480, "SRC-LV-L03-BAGAHOLIC-2021", "Alma BB canvas", "Bagaholic US table: Alma BB canvas new 2021 USD 1,480.", effective_date="2021-01-07")
add_hist("LV-L03", "FR", "2022", 1340, "SRC-LV-L03-LUXEFRONT-2022", "Alma BB canvas", "Luxe Front table: Alma BB canvas 2022 EUR 1,340.")
add_hist("LV-L03", "US", "2022", 1760, "SRC-LV-L03-LUXEFRONT-2022", "Alma BB canvas", "Luxe Front table: Alma BB canvas 2022 USD 1,760.")
add_hist("LV-L03", "FR", "2023", 1400, "SRC-LV-L03-LUXEFRONT-2022", "Alma BB canvas", "Luxe Front table: Alma BB canvas 2023 EUR 1,400.")
add_hist("LV-L03", "US", "2024", 1820, "SRC-LV-L03-PURSEBOP-2024", "Alma BB", "PurseBop US table: Alma BB 2024 USD 1,820.")
add_hist("LV-L03", "FR", "2024", 1550, "SRC-LV-L03-PURSEBOP-2024", "Alma BB", "PurseBop Europe table: Alma BB 2024 EUR 1,550.")

add_hist("LV-L04", "FR", "2021", 1150, "SRC-LV-L04-BAGAHOLIC-2021", "Neverfull MM", "Bagaholic Europe table: Neverfull MM new 2021 EUR 1,150.", effective_date="2021-01-07")
add_hist("LV-L04", "US", "2021", 1540, "SRC-LV-L04-BAGAHOLIC-2021", "Neverfull MM", "Bagaholic US table: Neverfull MM new 2021 USD 1,540.", effective_date="2021-01-07")
add_hist("LV-L04", "FR", "2022", 1500, "SRC-LV-L04-LUXEFRONT-2022", "Neverfull MM canvas", "Luxe Front table: Neverfull MM canvas 2022 EUR 1,500.", material="Monogram canvas")
add_hist("LV-L04", "US", "2022", 2030, "SRC-LV-L04-LUXEFRONT-2022", "Neverfull MM canvas", "Luxe Front table: Neverfull MM canvas 2022 USD 2,030.", material="Monogram canvas")
add_hist("LV-L04", "FR", "2023", 1500, "SRC-LV-L04-PETITEINPARIS-2023", "Neverfull MM", "Petite in Paris table: Neverfull MM Europe 2023 EUR 1,500.", material="Monogram canvas")
add_hist("LV-L04", "US", "2023", 2030, "SRC-LV-L04-PETITEINPARIS-2023", "Neverfull MM", "Petite in Paris table: Neverfull MM US 2023 USD 2,030.", material="Monogram canvas")


# Dior: historical secondary tables for Saddle and Book Tote.
source("SRC-DI-D01-PURSEBOP-2020", "Dior", "DI-D01", "historical_secondary_table", "PurseBop Dior price increase 2020", "https://www.pursebop.com/dior-follows-louis-vuitton-and-chanel-with-price-increases/", "2020-07-09", "secondary", "MEDIUM", "2019/2020 US Oblique Saddle table; used as version context only.")
source("SRC-DI-D01-FIFTHAVENUE-2023", "Dior", "DI-D01", "historical_secondary_table", "Fifth Avenue Girl Dior price increase July 2023", "https://fifthavenuegirl.com/dior-price-increase-july-2023/", "2023-07-09", "secondary", "MEDIUM", "US Dior Saddle Bag 2022/July 2023 prices; source does not state size/material.")
source("SRC-DI-D02-BAGAHOLIC-2024", "Dior", "DI-D02", "historical_secondary_table", "Bagaholic Dior Book Tote reference guide 2024", "https://lvbagaholic.com/blogs/lv_bagaholic/dior-book-tote-reference-guide", "2024", "secondary", "MEDIUM", "Small Book Tote Oblique Canvas price and dimensions.")
source("SRC-DI-D03-PURSEBOP-2020", "Dior", "DI-D03", "historical_secondary_table", "PurseBop Dior price increase 2020", "https://www.pursebop.com/dior-follows-louis-vuitton-and-chanel-with-price-increases/", "2020-07-09", "secondary", "MEDIUM", "2019/2020 US Oblique Book Tote table.")
source("SRC-DI-D03-FIFTHAVENUE-2023", "Dior", "DI-D03", "historical_secondary_table", "Fifth Avenue Girl Dior price increase July 2023", "https://fifthavenuegirl.com/dior-price-increase-july-2023/", "2023-07-09", "secondary", "MEDIUM", "US Medium Book Tote old/new July 2023 prices.")
source("SRC-DI-D03-BAGAHOLIC-2024", "Dior", "DI-D03", "historical_secondary_table", "Bagaholic Dior Book Tote reference guide 2024", "https://lvbagaholic.com/blogs/lv_bagaholic/dior-book-tote-reference-guide", "2024", "secondary", "MEDIUM", "Medium Book Tote Oblique Canvas price and dimensions.")

add_hist("DI-D01", "US", "2022", 4200, "SRC-DI-D01-FIFTHAVENUE-2023", "Dior Saddle Bag", "Fifth Avenue Girl table: Dior Saddle Bag old 2022 USD 4,200.", notes="Source does not state size/material; current anchor is Small grained calfskin.")
add_hist("DI-D01", "US", "2023", 4400, "SRC-DI-D01-FIFTHAVENUE-2023", "Dior Saddle Bag", "Fifth Avenue Girl table: Dior Saddle Bag new July 2023 USD 4,400.", effective_date="2023-07-05", date_precision="day", notes="Source does not state size/material; current anchor is Small grained calfskin.")

add_hist("DI-D02", "FR", "2024", 2600, "SRC-DI-D02-BAGAHOLIC-2024", "Small Dior Book Tote Oblique Canvas", "Bagaholic table: Small Dior Book Tote Oblique Canvas EUR 2,600; dimensions 26.5 × 21 × 14 cm.", material="Oblique canvas", collection="Oblique canvas", notes="Current anchor is same size in Macrocannage calfskin.")
add_hist("DI-D02", "US", "2024", 3250, "SRC-DI-D02-BAGAHOLIC-2024", "Small Dior Book Tote Oblique Canvas", "Bagaholic table: Small Dior Book Tote Oblique Canvas USD 3,250; dimensions 26.5 × 21 × 14 cm.", material="Oblique canvas", collection="Oblique canvas", notes="Current anchor is same size in Macrocannage calfskin.")

add_hist("DI-D03", "US", "2019", 2700, "SRC-DI-D03-PURSEBOP-2020", "Dior Oblique Canvas Book Tote", "PurseBop 2020 table: Dior Oblique Canvas Book Tote 2019 USD 2,700.", material="Oblique canvas", collection="Oblique canvas", notes="Current anchor is same size in Macrocannage calfskin.")
add_hist("DI-D03", "US", "2020", 2900, "SRC-DI-D03-PURSEBOP-2020", "Dior Oblique Canvas Book Tote", "PurseBop 2020 table: Dior Oblique Canvas Book Tote 2020 USD 2,900.", material="Oblique canvas", collection="Oblique canvas", notes="Current anchor is same size in Macrocannage calfskin.")
add_hist("DI-D03", "US", "2023-07", 3350, "SRC-DI-D03-FIFTHAVENUE-2023", "Medium Book Tote", "Fifth Avenue Girl table: Medium Book Tote old price USD 3,350 before July 2023 change.", material="Not specified", collection="Medium Book Tote", date_precision="month", notes="Current US anchor price unresolved in supplied current capture.")
add_hist("DI-D03", "US", "2023-07-05", 3450, "SRC-DI-D03-FIFTHAVENUE-2023", "Medium Book Tote", "Fifth Avenue Girl table: Medium Book Tote new July 2023 price USD 3,450.", material="Not specified", collection="Medium Book Tote", effective_date="2023-07-05", date_precision="day", notes="Current US anchor price unresolved in supplied current capture.")
add_hist("DI-D03", "FR", "2024", 2700, "SRC-DI-D03-BAGAHOLIC-2024", "Medium Dior Book Tote Oblique Canvas", "Bagaholic table: Medium Dior Book Tote Oblique Canvas EUR 2,700; dimensions 36 × 27.5 × 16.5 cm.", material="Oblique canvas", collection="Oblique canvas", notes="Current France anchor is same size in Macrocannage calfskin.")
add_hist("DI-D03", "US", "2024", 3350, "SRC-DI-D03-BAGAHOLIC-2024", "Medium Dior Book Tote Oblique Canvas", "Bagaholic table: Medium Dior Book Tote Oblique Canvas USD 3,350; dimensions 36 × 27.5 × 16.5 cm.", material="Oblique canvas", collection="Oblique canvas", notes="Current US anchor price unresolved in supplied current capture.")


def normalize_value(v: str | None):
    return "" if v is None else str(v)


def make_row(
    lineage: dict,
    market: str,
    observation_date: str,
    date_precision: str,
    price,
    currency: str,
    price_status: str,
    source_id: str,
    source_quality: str,
    confidence: str,
    *,
    historical_reference: str = "",
    material: str = "",
    collection: str = "",
    effective_date: str = "",
    conflict_flag: bool = False,
    notes: str = "",
    source_excerpt: str = "",
    is_current: bool = False,
):
    row = current_anchor(lineage, market)
    country, local_currency = market_info(market)
    current_ref = lineage["market_refs"].get(market, lineage["current_reference"])
    if is_current:
        price = row.get("price", "")
        currency = row.get("currency", currency)
        price_status = row.get("price_status", "") or ("numeric" if str(row.get("price", "")).strip() else "unresolved")
        material = row.get("material", "")
        current_ref = row.get("official_sku_or_reference") or row.get("sku_or_reference") or current_ref
        source_excerpt = "Current anchor inherited from supplied current official localized product-page capture."
        notes = lineage["notes"]
        continuity_status = "EXACT_SKU"
        source_quality = "HIGH"
        confidence = "HIGH"
    else:
        continuity_status = lineage["continuity_status"]
    return {
        "observation_id": f"{lineage['product_lineage_id']}-{market}-{observation_date}-{source_id.split('-')[-1]}",
        "brand": lineage["brand"],
        "product_lineage_id": lineage["product_lineage_id"],
        "current_reference": current_ref,
        "historical_reference": historical_reference,
        "product_name": row.get("product_name", "") or lineage["current_name"],
        "product_family": lineage["product_family"],
        "product_role": lineage["product_role"],
        "iconic_or_signature_status": lineage["iconic_or_signature_status"],
        "market": market,
        "country": country,
        "observation_date": observation_date,
        "date_precision": date_precision,
        "effective_date_if_known": effective_date,
        "price": price,
        "currency": currency or local_currency,
        "price_status": price_status,
        "material": material or (row.get("material", "") if is_current else ""),
        "color_if_material": row.get("color", "") if is_current else "",
        "dimensions_raw": row.get("dimensions_raw", "") if is_current else ("36 × 27.5 × 16.5 cm" if lineage["product_lineage_id"] == "DI-D03" and "Medium" in historical_reference else "26.5 × 21 × 14 cm" if lineage["product_lineage_id"] == "DI-D02" else ""),
        "width_cm": row.get("width_cm", "") if is_current else "",
        "height_cm": row.get("height_cm", "") if is_current else "",
        "depth_cm": row.get("depth_cm", "") if is_current else "",
        "size_label": row.get("size_label", "") if is_current else ("small" if lineage["product_lineage_id"] == "DI-D02" else "medium" if lineage["product_lineage_id"] == "DI-D03" else ""),
        "collection_or_version": collection or (row.get("collection", "") if is_current else ""),
        "continuity_status": continuity_status,
        "continuity_notes": lineage["continuity_evidence"],
        "source_type": SOURCES[source_id]["source_type"],
        "source_name": SOURCES[source_id]["source_name"],
        "source_url": SOURCES[source_id]["original_url"],
        "archive_url_if_applicable": SOURCES[source_id]["archive_url"],
        "source_publication_date": SOURCES[source_id]["source_date"],
        "extraction_method": "manual_web_research",
        "source_quality": source_quality,
        "confidence": confidence,
        "source_ids": source_id,
        "conflict_flag": "true" if conflict_flag else "false",
        "notes": (notes + (" Source excerpt: " + source_excerpt if source_excerpt else "")).strip(),
    }


def build_rows():
    rows = []
    for lineage in LINEAGES:
        for market in ("FR", "US"):
            anchor = current_anchor(lineage, market)
            if not anchor:
                continue
            rows.append(make_row(
                lineage,
                market,
                OBSERVED_AT[:10],
                "day",
                anchor.get("price", ""),
                anchor.get("currency", ""),
                anchor.get("price_status", ""),
                official_source_id(lineage, market),
                "HIGH",
                "HIGH",
                is_current=True,
            ))
    for h in HIST:
        rows.append(make_row(
            LINEAGE_BY_ID[h["lineage_id"]],
            h["market"],
            h["observation_date"],
            h["date_precision"],
            h["price"],
            h["currency"],
            "numeric",
            h["source_id"],
            h["source_quality"],
            h["confidence"],
            historical_reference=h["historical_reference"],
            material=h["material"],
            collection=h["collection"],
            effective_date=h["effective_date"],
            conflict_flag=h["conflict_flag"],
            notes=h["notes"],
            source_excerpt=h["source_excerpt"],
        ))
    return rows


def add_events():
    events = []

    def event(lineage_id, market, prior_date, prior_price, new_date, new_price, currency, source_ids, notes="", evidence="MEDIUM"):
        abs_change = new_price - prior_price
        pct = abs_change / prior_price * 100 if prior_price else None
        events.append({
            "brand": LINEAGE_BY_ID[lineage_id]["brand"],
            "product_lineage_id": lineage_id,
            "market": market,
            "prior_observation_date": prior_date,
            "prior_price": prior_price,
            "new_observation_date": new_date,
            "new_price": new_price,
            "currency": currency,
            "absolute_change": abs_change,
            "percentage_change": round(pct, 4) if pct is not None else "",
            "evidence_strength": evidence,
            "source_ids": ";".join(source_ids),
            "event_interval_note": "Exact effective date not asserted unless stated in source.",
            "notes": notes,
        })

    for lid, vals in {
        "CH-C01": [("2022", 8990, "2023", 9700), ("2023", 9700, "2024", 10300)],
        "CH-C02": [("2022", 8450, "2023", 9300), ("2023", 9300, "2024", 9900)],
        "CH-C03": [("2020", 3350, "2022", 4150), ("2022", 4150, "2023", 4500), ("2023", 4500, "2024", 4750)],
        "CH-C04": [("2022", 4350, "2023", 4700), ("2023", 4700, "2024", 4950)],
    }.items():
        for prior, pp, new, np in vals:
            ids = [f"SRC-{lid}-BAGAHOLIC-2024"]
            if lid == "CH-C03" and prior == "2020":
                ids = ["SRC-CH-C03-PURSEBOP-2020", "SRC-CH-C03-BAGAHOLIC-2024"]
            event(lid, "FR", prior, pp, new, np, "EUR", ids, notes="Source table supports both price points; exact effective date is not asserted.")

    event("HM-H01", "FR", "2022", 4550, "2023", 5550, "EUR", ["SRC-HM-H01-LUXEFRONT-2022"], notes="One of two conflicting 2023 Geta observations.", evidence="MEDIUM")
    event("HM-H01", "FR", "2023", 4550, "2024", 4850, "EUR", ["SRC-HM-H01-PURSEBOP-EU-2024"], notes="Uses the PurseBop 2023 observation; Luxe Front reports a conflicting 2023 price.", evidence="MEDIUM")
    event("HM-H01", "US", "2023", 5950, "2024", 6450, "USD", ["SRC-HM-H01-PURSEBLOG-US-2024"])
    event("HM-H02", "FR", "2023", 5500, "2024", 6000, "EUR", ["SRC-HM-H02-PURSEBOP-EU-2024"])

    for lid, market, currency, vals in [
        ("LV-L01", "FR", "EUR", [("2021", 1180, "2022", 1390), ("2022", 1390, "2023", 1450), ("2023", 1450, "2024", 1550)]),
        ("LV-L01", "US", "USD", [("2021", 1650, "2022", 1820), ("2022", 1820, "2024", 1820)]),
        ("LV-L02", "FR", "EUR", [("2022", 1960, "2023", 2050)]),
        ("LV-L03", "FR", "EUR", [("2021", 1100, "2022", 1340), ("2022", 1340, "2023", 1400), ("2023", 1400, "2024", 1550)]),
        ("LV-L03", "US", "USD", [("2021", 1480, "2022", 1760), ("2022", 1760, "2024", 1820)]),
        ("LV-L04", "FR", "EUR", [("2021", 1150, "2022", 1500), ("2022", 1500, "2023", 1500)]),
        ("LV-L04", "US", "USD", [("2021", 1540, "2022", 2030), ("2022", 2030, "2023", 2030)]),
    ]:
        for prior, pp, new, np in vals:
            source_map = {
                "LV-L01": ["SRC-LV-L01-BAGAHOLIC-2021", "SRC-LV-L01-LUXEFRONT-2022", "SRC-LV-L01-PURSEBOP-2024"],
                "LV-L02": ["SRC-LV-L02-LUXEFRONT-2022"],
                "LV-L03": ["SRC-LV-L03-BAGAHOLIC-2021", "SRC-LV-L03-LUXEFRONT-2022", "SRC-LV-L03-PURSEBOP-2024"],
                "LV-L04": ["SRC-LV-L04-BAGAHOLIC-2021", "SRC-LV-L04-LUXEFRONT-2022", "SRC-LV-L04-PETITEINPARIS-2023"],
            }
            ids = source_map[lid]
            if len(ids) == 1:
                supporting = ids
            elif prior == "2021":
                supporting = [ids[0], ids[1]]
            elif new == "2024":
                supporting = [ids[1], ids[2]]
            else:
                supporting = [ids[1]]
            event(lid, market, prior, pp, new, np, currency, supporting, notes="Source table supports both price points; exact effective date is not asserted.")

    event("DI-D01", "US", "2022", 4200, "2023", 4400, "USD", ["SRC-DI-D01-FIFTHAVENUE-2023"], notes="Source does not state size/material; current anchor is Small grained calfskin.")
    event("DI-D02", "FR", "2024", 2600, OBSERVED_AT[:10], 3250, "EUR", ["SRC-DI-D02-BAGAHOLIC-2024", "SRC-DI-D02-CURRENT-FR"], notes="Model/version interval; historical Oblique Canvas to current Macrocannage calfskin.")
    event("DI-D02", "US", "2024", 3250, OBSERVED_AT[:10], 3900, "USD", ["SRC-DI-D02-BAGAHOLIC-2024", "SRC-DI-D02-CURRENT-US"], notes="Model/version interval; historical Oblique Canvas to current Macrocannage calfskin.")
    event("DI-D03", "US", "2019", 2700, "2020", 2900, "USD", ["SRC-DI-D03-PURSEBOP-2020"])
    event("DI-D03", "US", "2020", 2900, "2023-07", 3350, "USD", ["SRC-DI-D03-PURSEBOP-2020", "SRC-DI-D03-FIFTHAVENUE-2023"], notes="Interval ends at the pre-increase July 2023 observation.")
    event("DI-D03", "US", "2023-07", 3350, "2023-07-05", 3450, "USD", ["SRC-DI-D03-FIFTHAVENUE-2023"], notes="Source states July 5, 2023 increase.")
    event("DI-D03", "FR", "2024", 2700, OBSERVED_AT[:10], 3650, "EUR", ["SRC-DI-D03-BAGAHOLIC-2024", "SRC-DI-D03-CURRENT-FR"], notes="Model/version interval; historical Oblique Canvas to current Macrocannage calfskin.")
    return events


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_clean_rows(rows: list[dict]):
    return [{k: normalize_value(row.get(k, "")) for k in FIELDS} for row in rows]


def build_lineage_rows():
    return [
        {
            "product_lineage_id": x["product_lineage_id"],
            "brand": x["brand"],
            "product_family": x["product_family"],
            "current_reference": x["current_reference"],
            "historical_reference": x["historical_name"],
            "historical_name": x["historical_name"],
            "current_name": x["current_name"],
            "continuity_status": x["continuity_status"],
            "continuity_evidence": x["continuity_evidence"],
            "confidence": x["confidence"],
            "notes": x["notes"],
        }
        for x in LINEAGES
    ]


def build_errors():
    unresolved = [
        ("Chanel", "Small Shopping Bag", "France; United States", "AS6495-B25347-UA954", "PRICE_NOT_FOUND", "https://www.chanel.com/fr/mode/p/AS6495B25347UA954/petit-cabas-agneau-metal-dore/", "No accepted historical source identified that maps the selected current reference to dated retail prices."),
        ("Chanel", "Mini Shopping Bag", "France; United States", "AS6199-B25388-94305", "PRICE_NOT_FOUND", "https://www.chanel.com/fr/mode/p/AS6199B2538894305/mini-cabas-veau-metal-dore/", "Current family was reviewed as a lower/core candidate; no traceable historical price table accepted."),
        ("Hermès", "Herbag Messenger 39", "United States", "H084489CKAC", "PRODUCT_IDENTITY_UNCERTAIN", "https://www.hermes.com/us/en/product/herbag-messenger-39-bag-H084489CKAC/", "Available historical sources identify Herbag Zip 31, not the current Messenger 39; size mismatch prevents primary continuity."),
        ("Hermès", "Videpoches", "France; United States", "H084151CKAC", "PRICE_NOT_FOUND", "https://www.hermes.com/fr/fr/product/sac-hermes-videpoches-H084151CKAC/", "Current official reference found, but no accepted dated historical retail-price observation for the same model/material."),
        ("Hermès", "P'tit Arçon", "France; United States", "H085668CKAB / H086394CKAC", "PRICE_NOT_FOUND", "https://www.hermes.com/fr/fr/product/sac-p-tit-arcon-H085668CKAB/", "Current family found, but no accepted dated historical retail-price observation."),
        ("Louis Vuitton", "OnTheGo PM", "France", "M29976", "PRICE_NOT_FOUND", "https://fr.louisvuitton.com/fra-fr/produits/cabas-onthego-pm-monogram-empreinte-nvprod7890052v/M29976", "Current product was considered as upper-core candidate; no accepted historical table mapped to the current reference/material."),
        ("Louis Vuitton", "Multipass Mini", "France; United States", "M29099", "PRODUCT_DISCONTINUED", "https://fr.louisvuitton.com/fra-fr/produits/sac-multipass-mini-monogram-nvprod7890075v/M29099", "New/current 2026 family in supplied capture; no 2020–2025 historical series identified."),
        ("Dior", "Dior Promenade Medium", "France; United States", "M1409OHSU_M09I", "PRODUCT_DISCONTINUED", "https://www.dior.com/fr_fr/fashion/products/M1409OHSU_M09I", "Current seasonal 2026 product; no earlier retail-price observation identified."),
        ("Dior", "Dior Toujours", "France; United States", "M2836OSNW_M900 / M2822OSNW_M900", "DATE_UNRESOLVED", "https://www.dior.com/fr_fr/fashion/news-savoir-faire/folder-actualites-et-evenements/le-sac-dior-toujours", "Family introduced in 2023, but accepted sources did not provide a dated price for the mapped current size/material."),
        ("Dior", "Dior Bow", "France; United States", "M0715OUQO_M900", "PRICE_NOT_FOUND", "https://www.dior.com/fr_fr/fashion/products/M0715OUQO_M900", "Current official product found; no accepted dated historical price evidence."),
    ]
    return [
        {
            "brand": brand,
            "product": product,
            "market": market,
            "requested_period": REQUESTED_PERIOD,
            "failure_type": failure_type,
            "attempted_source": attempted_source,
            "reason": reason,
            "timestamp": ACCESSED_AT,
        }
        for brand, product, market, ref, failure_type, attempted_source, reason in unresolved
    ]


def build_log(rows: list[dict], events: list[dict], errors: list[dict]):
    numeric = [r for r in rows if r.get("price_status") == "numeric" and str(r.get("price", "")) != ""]
    log = []
    log.append("# Historical luxury handbag pricing collection log\n")
    log.append(f"Collection date: {COLLECTION_DATE}; requested period: {REQUESTED_PERIOD}.\n")
    log.append("## Scope and method\n")
    log.append("Brands: Chanel, Hermès, Louis Vuitton, Dior. Category: luxury handbags only. Markets: France and United States, with France prioritized. Grain: one brand × product lineage × market × dated observation; irregular observations retained. Historical acquisition used manual web research from public, indexed pages. No authentication, CAPTCHA bypass, resale asking prices, FX conversion, inflation adjustment, interpolation, strategy analysis, or recommendations were used.\n")
    log.append("The current 2026 anchor rows are inherited from the supplied official localized current-price datasets observed on 2026-08-15. Historical rows are predominantly Tier 3/4 secondary source observations because archived official pages or official historical price lists were not reliably available in the accessible public results.\n")
    log.append("## Brand-level coverage\n")
    log.append("| Brand | Candidate products selected | Usable historical series | Observations obtained | HIGH | MEDIUM | LOW | France observations | US observations | Avg historical observations / usable series | Unresolved products |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n")
    for brand in ["Chanel", "Hermès", "Louis Vuitton", "Dior"]:
        ls = [x for x in LINEAGES if x["brand"] == brand]
        br = [r for r in rows if r["brand"] == brand]
        h = [r for r in br if r["price_status"] == "numeric" and r["continuity_status"] != "EXACT_SKU"]
        hist_series = {r["product_lineage_id"] for r in h}
        counts = Counter(r["confidence"] for r in br if r["price_status"] == "numeric")
        fr = sum(1 for r in br if r["market"] == "FR" and r["price_status"] == "numeric")
        us = sum(1 for r in br if r["market"] == "US" and r["price_status"] == "numeric")
        avg = round(len(h) / len(hist_series), 2) if hist_series else 0
        unresolved = sum(1 for e in errors if e["brand"] == brand)
        log.append(f"| {brand} | {len(ls)} | {len(hist_series)} | {len(br)} | {counts['HIGH']} | {counts['MEDIUM']} | {counts['LOW']} | {fr} | {us} | {avg} | {unresolved} |\n")
    log.append("\n## Candidate selection and lineage notes\n")
    for x in LINEAGES:
        log.append(f"- `{x['product_lineage_id']}` {x['brand']} — {x['current_name']}; role `{x['product_role']}`; continuity `{x['continuity_status']}`; selection reason: {x['notes']}\n")
    log.append("\nProducts not included in the primary lineages because identity, size, or historical price evidence was insufficient are listed in `errors/unresolved_history.jsonl`.\n")
    log.append("## Source limitations\n")
    log.append("- No accepted historical observation in this run came from an archived official product page or official historical price list. Current anchor observations are official primary sources from the supplied current datasets.\n")
    log.append("- Secondary tables sometimes use family/size labels rather than official references. Those observations are marked `MODEL_SUCCESSOR` or `SAME_MODEL_CONTINUOUS` according to the documented lineage evidence; approximate family-only candidates were not promoted into the primary lineages.\n")
    log.append("- Hermès Geta has a credible-source conflict for 2023 France (EUR 4,550 vs EUR 5,550); both observations are preserved with `conflict_flag=true`.\n")
    log.append("- France coverage is materially stronger for Chanel and Hermès. US history is incomplete for Chanel and Hermès Jypsière, and current US Dior Medium Book Tote price was unresolved in the supplied capture.\n")
    log.append("- Historical prices are nominal local-currency retail/list prices as reported by the source. No FX or inflation normalization was performed.\n")
    official_rows = sum(1 for r in rows if r["source_type"] == "official_current_product_page")
    secondary_rows = sum(1 for r in rows if r["source_type"] != "official_current_product_page")
    historical_lineages = len({r["product_lineage_id"] for r in rows if r["continuity_status"] != "EXACT_SKU"})
    lineage_status_counts = Counter(x["continuity_status"] for x in LINEAGES)
    high_conf_series = sum(1 for x in LINEAGES if x["confidence"] == "HIGH")
    numeric_official = sum(1 for r in rows if r["source_type"] == "official_current_product_page" and r["price_status"] == "numeric")
    numeric_secondary = sum(1 for r in rows if r["source_type"] != "official_current_product_page" and r["price_status"] == "numeric")
    log.append("\n## Historical coverage summary\n")
    log.append(f"Accepted observation rows: {len(rows)}; numeric price observations: {len(numeric)}; usable historical lineages: {historical_lineages}; price-change events: {len(events)}; unresolved products/candidates: {len(errors)}.\n")
    log.append(f"Historical lineage continuity counts: EXACT_SKU {0}; SAME_MODEL_CONTINUOUS {lineage_status_counts['SAME_MODEL_CONTINUOUS']}; MODEL_SUCCESSOR {lineage_status_counts['MODEL_SUCCESSOR']}; APPROXIMATE_FAMILY_MATCH {lineage_status_counts['APPROXIMATE_FAMILY_MATCH']}. Current anchor rows are labeled EXACT_SKU separately.\n")
    log.append(f"Source mix by accepted observation rows: official current primary {official_rows / len(rows) * 100:.1f}%; secondary historical {secondary_rows / len(rows) * 100:.1f}%. Source mix by numeric price observations: official current primary {numeric_official / len(numeric) * 100:.1f}%; secondary historical {numeric_secondary / len(numeric) * 100:.1f}%.\n")
    log.append(f"Lineage-level high-confidence series: {high_conf_series}; same-model-continuous series: {lineage_status_counts['SAME_MODEL_CONTINUOUS']}; model-successor series: {lineage_status_counts['MODEL_SUCCESSOR']}; approximate-family matches: {lineage_status_counts['APPROXIMATE_FAMILY_MATCH']}.\n")
    log.append("## Output files\n")
    log.append("- `raw/historical_price_observations_raw.jsonl` — raw-like accepted observations including source excerpts and extraction metadata.\n")
    log.append("- `clean/historical_pricing_clean.csv` — validated normalized observation panel, including current anchor rows and confidence/continuity fields.\n")
    log.append("- `clean/chanel_historical_pricing.csv`, `clean/hermes_historical_pricing.csv`, `clean/louis_vuitton_historical_pricing.csv`, `clean/dior_historical_pricing.csv` — brand subsets.\n")
    log.append("- `lineage/product_lineage.csv` — product identity and continuity map.\n")
    log.append("- `events/price_change_events.csv` — source-supported observed price-change intervals only.\n")
    log.append("- `logs/HISTORICAL_SOURCE_REGISTRY.csv` — source registry for accepted observations.\n")
    log.append("- `errors/unresolved_history.jsonl` — unresolved candidates and source limitations.\n")
    log.append("## Gate assessment\n")
    log.append("Overall: READY WITH LIMITATIONS. Chanel and Louis Vuitton have usable multi-observation France series across four lineages; Dior has three usable lineages with material/version caveats; Hermès has two usable lineages and a documented Geta conflict. France is READY WITH LIMITATIONS; United States is READY WITH LIMITATIONS because Chanel and Hermès coverage is sparse and the Dior medium Book Tote current US anchor is unresolved. Brand-level readiness: Chanel READY WITH LIMITATIONS; Hermès NOT READY for a broad multi-family comparison; Louis Vuitton READY WITH LIMITATIONS; Dior READY WITH LIMITATIONS. This is a data-coverage statement only, not an analytical conclusion.\n")
    return "".join(log)


def main():
    add_official_sources()
    rows = build_rows()
    clean_rows = build_clean_rows(rows)
    events = add_events()
    errors = build_errors()

    # Raw output retains source excerpts and an explicit raw extraction record.
    raw_rows = []
    for row in rows:
        raw = dict(row)
        raw["raw_price_value"] = row.get("price", "")
        raw["raw_observation_date"] = row.get("observation_date", "")
        raw["review_status"] = "VALID" if row.get("price_status") in {"numeric", "unresolved", "contact_us"} else "REVIEW_REQUIRED"
        raw_rows.append(raw)

    write_jsonl(OUT / "raw" / "historical_price_observations_raw.jsonl", raw_rows)
    write_csv(OUT / "clean" / "historical_pricing_clean.csv", clean_rows, FIELDS)
    for brand, slug in [("Chanel", "chanel"), ("Hermès", "hermes"), ("Louis Vuitton", "louis_vuitton"), ("Dior", "dior")]:
        write_csv(OUT / "clean" / f"{slug}_historical_pricing.csv", [r for r in clean_rows if r["brand"] == brand], FIELDS)

    write_csv(OUT / "lineage" / "product_lineage.csv", build_lineage_rows(), [
        "product_lineage_id", "brand", "product_family", "current_reference", "historical_reference", "historical_name", "current_name", "continuity_status", "continuity_evidence", "confidence", "notes"
    ])
    write_csv(OUT / "events" / "price_change_events.csv", events, [
        "brand", "product_lineage_id", "market", "prior_observation_date", "prior_price", "new_observation_date", "new_price", "currency", "absolute_change", "percentage_change", "evidence_strength", "source_ids", "event_interval_note", "notes"
    ])
    write_csv(OUT / "logs" / "HISTORICAL_SOURCE_REGISTRY.csv", list(SOURCES.values()), [
        "source_id", "brand", "product_lineage_id", "source_type", "source_name", "original_url", "archive_url", "source_date", "accessed_at", "primary_or_secondary", "source_quality", "notes"
    ])
    write_jsonl(OUT / "errors" / "unresolved_history.jsonl", errors)
    (OUT / "logs" / "HISTORICAL_COLLECTION_LOG.md").write_text(build_log(clean_rows, events, errors), encoding="utf-8")

    print(json.dumps({
        "output": str(OUT),
        "total_rows": len(clean_rows),
        "numeric_price_observations": sum(1 for r in clean_rows if r["price_status"] == "numeric"),
        "current_anchor_rows": sum(1 for r in clean_rows if r["continuity_status"] == "EXACT_SKU"),
        "events": len(events),
        "errors": len(errors),
        "sources": len(SOURCES),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
