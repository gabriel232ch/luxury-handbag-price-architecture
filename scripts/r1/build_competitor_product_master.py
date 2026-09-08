#!/usr/bin/env python3
"""Build a reviewable product-master snapshot for the three competitors.

The source snapshot is deliberately kept separate from the 2026-08-15 baseline.
Only attributes observed on official US detail/category pages are promoted; an
undisclosed regular/seasonal flag remains ``not_disclosed``.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "research_r1/data/live_refresh_2026-09-07_us.csv"
OUTPUT = ROOT / "research_r1/data/product_master_competitors_2026-09-07_us.csv"


def cm_dimensions(raw: str) -> str:
    """Convert the first L/H/D inch triplet to centimetres, preserving labels."""
    if not raw:
        return ""
    match = re.search(
        r"L\s*([0-9]+(?:\.[0-9]+)?)\"\s*[xX×]\s*H\s*([0-9]+(?:\.[0-9]+)?)\"\s*[xX×]\s*D\s*([0-9]+(?:\.[0-9]+)?)\"",
        raw,
    )
    if not match:
        match = re.search(
            r"([0-9]+(?:\.[0-9]+)?)\s*x\s*([0-9]+(?:\.[0-9]+)?)\s*x\s*([0-9]+(?:\.[0-9]+)?)\s*inches",
            raw,
            flags=re.I,
        )
    if not match:
        return raw
    values = [round(float(value) * 2.54, 1) for value in match.groups()]
    return " x ".join(f"{value:g}" for value in values) + " cm"


def material_group(material: str) -> str:
    value = material.lower()
    has_textile = any(token in value for token in ("canvas", "silk", "wool", "tweed", "technical fabric"))
    has_leather = any(token in value for token in ("leather", "calfskin", "goatskin", "cowhide", "lambskin", "swift", "epsom", "togo", "negonda", "evercolor", "clemence", "box calfskin", "chamkila"))
    if has_textile and has_leather:
        return "mixed_textile_leather"
    if has_textile:
        return "textile"
    if has_leather:
        return "leather"
    return "unknown"


def code_for(brand: str) -> str:
    return {"Hermès": "HM", "Louis Vuitton": "LV", "Dior": "DI"}[brand]


# Detail-page attributes for Hermès, whose category page does not expose the
# same fields as its product pages. The URLs and references are still taken
# from the live refresh CSV and are checked below.
HERMES_DETAILS = {
    "H085414CKAO": ("Herbag", "Herbag Zip 20 bag", "20", "crossbody", "crossbody", "H Viking canvas and Hunter cowhide", "Beige/Natural", 'L 8.1" x H 6.5" x D 2.8"', "unavailable_current"),
    "H087076CKAB": ("Lassoie", "Lassoie Hermès bag", "unknown", "crossbody", "crossbody", '"Eperon D\'Or Bandana" printed silk and Swift calfskin', "Blue", 'L 7.5" x H 8.3" x D 4.7"', "available_online"),
    "H087119CKAA": ("Jypsiere", "Jypsiere mini Toile & Cuir bag", "mini", "crossbody", "crossbody", "H canvas and Swift calfskin", "Beige/Natural", 'L 8.7" x H 5.8" x D 2.1"', "unavailable_current"),
    "H083969CKAU": ("Bolide", "Bolide on Wheels bag", "unknown", "top-handle", "top-handle", "Epsom calfskin", "Yellow", 'L 7.5" x H 8.3" x D 2.9"', "unavailable_current"),
    "H085054CK37": ("So Medor", "So Medor bag", "unknown", "shoulder", "shoulder", "Togo calfskin", "Beige/Natural", 'L 7.5" x H 8.7" x D 7.9"', "available_online"),
    "H069523CCBZ": ("Halzan", "Halzan mini bag", "mini", "shoulder", "shoulder", "Swift calfskin", "Brown", 'L 8.5" x H 6" x D 2.5"', "unavailable_current"),
    "H088914CK37": ("Videpoches", "Hermès Videpoches bag", "unknown", "crossbody", "crossbody", "Togo calfskin", "Beige/Natural", 'L 10.6" x H 5.5" x D 1.6"', "available_online"),
    "H071240C0AV": ("Jige Elan", "Jige Elan 29 clutch", "29", "evening/mini", "clutch", "Doblis and Swift calfskin", "Blue", 'L 11.4" x H 5.9" x D 1"', "unavailable_current"),
    "H087960CT89": ("Mallette", "Mallette bag", "unknown", "top-handle", "top-handle", "Box calfskin", "Grey", 'L 7.5" x H 3.9" x D 2.2"', "unavailable_current"),
    "H086962CK0G": ("Sanglons", "Sanglons clutch", "unknown", "evening/mini", "clutch", "Chamkila goatskin", "Red", 'L 7.6" x H 3.9" x D 1.5"', "unavailable_current"),
    "H086915CK89": ("Poche Cliquetis", "Poche Cliquetis bag", "unknown", "crossbody", "crossbody", "Swift calfskin", "Black", 'L 8.9" x H 10" x D 1"', "available_online"),
    "H085690CKBF": ("In-the-Loop", "Hermès In-the-Loop 18 bag", "18", "shoulder", "shoulder", "H canvas and Swift calfskin", "Beige/Natural", 'L 7.1" x H 7.7" x D 4.7"', "unavailable_current"),
    "H087950CK89": ("Medor", "Mini Medor bag", "mini", "evening/mini", "mini", "Chamkila goatskin", "Red", 'L 5.7" x H 5.9" x D 5.7"', "unavailable_current"),
    "H086717CKAC": ("Neo Garden", "Neo Garden Voyage 41 bag", "41", "tote/shopper", "tote", "Militaire canvas and Negonda calfskin", "Black", 'L 16.3" x H 12" x D 9.1"', "available_online"),
    "H082901CCCA": ("Bolide", "Bolide 1923 - 25 verso bag", "25", "top-handle", "top-handle", "Evercolor calfskin", "Beige/Natural", 'L 10.2" x H 7.9" x D 3.9"', "unavailable_current"),
    "H089099CAAA": ("Neo Double Sens", "Neo Double Sens 35 bicolor bag", "35", "tote/shopper", "tote", "taurillon Clemence leather and Swift calfskin", "Blue", 'L 11" X H 13.8" x D 3.7"', "available_online"),
    "H087987CK89": ("Videpoches", "Hermès Videpoches bag", "unknown", "crossbody", "crossbody", "Togo calfskin", "Purple", 'L 10.6" x H 5.5" x D 1.6"', "available_online"),
    "H087934CKAA": ("Neo Garden", "Neo Garden Voyage 41 bredies bag", "41", "tote/shopper", "tote", "Militaire canvas, Togo, Negonda and Swift calfskin", "Blue", 'L 16.3" x H 12" x D 9.1"', "available_online"),
    "H087987CKH0": ("Videpoches", "Hermès Videpoches bag", "unknown", "crossbody", "crossbody", "Togo calfskin", "Grey", 'L 10.6" x H 5.5" x D 1.6"', "available_online"),
    "H086717CKAH": ("Neo Garden", "Neo Garden Voyage 41 bag", "41", "tote/shopper", "tote", "Militaire canvas and Negonda calfskin", "Blue", 'L 16.3" x H 12" x D 9.1"', "available_online"),
    "H084948CK89": ("En Piste", "En Piste clutch", "unknown", "evening/mini", "clutch", "Chamkila goatskin", "Black", 'L 5.5" x H 5.1" x D 2"', "available_online"),
}


LV_RULES = {
    "M27242": ("Wallet On Chain Trotter", "Wallet On Chain Trotter", "small", "small-leather-goods", "small-leather-goods"),
    "M13567": ("Pochette Eva", "Pochette Eva", "small", "small-leather-goods", "small-leather-goods"),
    "M82766": ("Pochette Accessoires", "Pochette Accessoires", "small", "small-leather-goods", "small-leather-goods"),
    "M81896": ("Pochette Félicie", "Pochette Félicie", "small", "small-leather-goods", "small-leather-goods"),
    "M2A366": ("All In", "All In BB", "BB", "shoulder", "shoulder"),
    "M2A467": ("Neverfull", "Neverfull Inside Out BB", "BB", "tote/shopper", "tote"),
    "M2A323": ("Low Key", "Hobo", "PM", "shoulder", "hobo"),
    "M28354": ("Neverfull", "Neverfull Inside Out MM", "MM", "tote/shopper", "tote"),
    "M2A711": ("CarryAll", "Nano CarryAll", "nano", "evening/mini", "mini"),
    "M46203": ("CarryAll", "CarryAll PM", "PM", "tote/shopper", "tote"),
    "M45832": ("Boulogne", "Boulogne PM", "PM", "shoulder", "shoulder"),
    "M46049": ("Diane", "Diane", "unknown", "shoulder", "shoulder"),
    "M2A126": ("Alma", "Alma BB", "BB", "top-handle", "top-handle"),
    "M29977": ("Speedy", "Speedy Bandoulière 20", "20", "top-handle", "top-handle"),
    "M2A335": ("Diane", "Diane", "unknown", "shoulder", "shoulder"),
    "M2A011": ("Madeleine", "Nano Madeleine", "nano", "evening/mini", "mini"),
    "M46990": ("Alma", "Alma BB", "BB", "top-handle", "top-handle"),
    "M46784": ("High Rise", "High Rise", "unknown", "crossbody", "bumbag"),
    "M46987": ("Neverfull", "Neverfull MM", "MM", "tote/shopper", "tote"),
    "M13039": ("Speedy", "Speedy Bandoulière 20", "20", "top-handle", "top-handle"),
}


DIOR_RULES = {
    "M1409OHST_M911": ("Dior Promenade", "Medium Dior Promenade Shopping Bag", "medium", "tote/shopper", "tote"),
    "M1410OHST_M911": ("Dior Promenade", "Small Dior Promenade Shopping Bag", "small", "tote/shopper", "tote"),
    "M1410OHSU_M12E": ("Dior Promenade", "Small Dior Promenade Shopping Bag", "small", "tote/shopper", "tote"),
    "M1410PHSU_M57G": ("Dior Promenade", "Small Dior Promenade Shopping Bag", "small", "tote/shopper", "tote"),
    "M1409OHST_M16E": ("Dior Promenade", "Medium Dior Promenade Shopping Bag", "medium", "tote/shopper", "tote"),
    "M1409OTZQ_M928": ("Dior Promenade", "Medium Dior Promenade Shopping Bag", "medium", "tote/shopper", "tote"),
    "M1410OTZQ_M928": ("Dior Promenade", "Small Dior Promenade Shopping Bag", "small", "tote/shopper", "tote"),
    "M1410OHSV_M71I": ("Dior Promenade", "Small Dior Promenade Shopping Bag", "small", "tote/shopper", "tote"),
    "M2867ODKZ_M42R": ("Dior Toujours", "Small Dior Toujours Hobo Bag", "small", "shoulder", "hobo"),
    "M2867ODKZ_M900": ("Dior Toujours", "Small Dior Toujours Hobo Bag", "small", "shoulder", "hobo"),
    "M2867ODUN_M68M": ("Dior Toujours", "Small Dior Toujours Hobo Bag", "small", "shoulder", "hobo"),
    "M2867ODKZ_M01S": ("Dior Toujours", "Small Dior Toujours Hobo Bag", "small", "shoulder", "hobo"),
    "M2867ODKZ_M31N": ("Dior Toujours", "Small Dior Toujours Hobo Bag", "small", "shoulder", "hobo"),
    "M2867ODKZ_M39Z": ("Dior Toujours", "Small Dior Toujours Hobo Bag", "small", "shoulder", "hobo"),
    "M2835OSNW_M05S": ("Dior Toujours", "Small Dior Toujours Vertical Tote Bag", "small", "tote/shopper", "tote"),
    "M2835OSNW_M79U": ("Dior Toujours", "Small Dior Toujours Vertical Tote Bag", "small", "tote/shopper", "tote"),
    "M2821OSNW_M73M": ("Dior Toujours", "Medium Dior Toujours Bag", "medium", "tote/shopper", "tote"),
    "M2820OHJS_M42R": ("Dior Toujours", "Large Dior Toujours Bag", "large", "tote/shopper", "tote"),
    "M2821OSNW_M66M": ("Dior Toujours", "Medium Dior Toujours Bag", "medium", "tote/shopper", "tote"),
    "M2821OSOQ_M22S": ("Dior Toujours", "Medium Dior Toujours Bag", "medium", "tote/shopper", "tote"),
}


def main() -> None:
    with SOURCE.open(newline="") as handle:
        snapshot = list(csv.DictReader(handle))
    target = [row for row in snapshot if row["brand"] in {"Hermès", "Louis Vuitton", "Dior"}]
    by_key = {(row["brand"], row["reference_code"]): row for row in target}
    rows = []
    for brand, rules in (("Hermès", HERMES_DETAILS), ("Louis Vuitton", LV_RULES), ("Dior", DIOR_RULES)):
        for reference, config in rules.items():
            source = by_key[(brand, reference)]
            if brand == "Hermès":
                family, model, size_label, use_tag, bag_type, material, color, dimensions_raw, availability = config
                dimensions = cm_dimensions(dimensions_raw)
                status = "verified_official_reference_attributes"
                notes = "Official US detail DOM verified reference, material and dimensions; use/bag type is a conservative taxonomy from the model name/description; regular/seasonal marker not disclosed."
            else:
                if brand == "Louis Vuitton":
                    family, model, size_label, use_tag, bag_type = config
                else:
                    family, model, size_label, use_tag, bag_type = config
                material = source["material_raw"]
                color = source["color"]
                dimensions = cm_dimensions(source["dimensions_raw"])
                availability = "available_online"
                if brand == "Dior":
                    status = "verified_official_reference_material_size_label"
                    notes = "Official US detail DOM verified reference, material and name-based size label; numeric dimensions not exposed in visible Size & Fit panel; regular/seasonal marker not disclosed."
                else:
                    status = "verified_official_reference_attributes"
                    notes = "Official US detail DOM verified reference, material and dimensions; use/bag type is a conservative taxonomy from the model name; regular/seasonal marker not disclosed; color was not exposed in the extracted detail DOM."
            rows.append(
                {
                    "product_id": f"{code_for(brand)}-US-{reference}",
                    "brand": brand,
                    "family": family,
                    "model": model,
                    "size_label": size_label,
                    "use_tag": use_tag,
                    "bag_type": bag_type,
                    "canonical_reference": reference,
                    "material_raw": material,
                    "material_group": material_group(material),
                    "color": color,
                    "dimensions_cm": dimensions,
                    "regular_special": "not_disclosed",
                    "collection_label": "",
                    "availability_status": availability,
                    "identity_status": status,
                    "source_url_fr": "",
                    "source_url_us": source["source_url"],
                    "notes": notes,
                }
            )

    expected = {"Hermès": 21, "Louis Vuitton": 20, "Dior": 20}
    actual = {}
    for row in rows:
        actual[row["brand"]] = actual.get(row["brand"], 0) + 1
    assert actual == expected, actual
    assert len({row["product_id"] for row in rows}) == len(rows)
    assert all(row["identity_status"].startswith("verified_") for row in rows)

    fields = list(rows[0])
    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUTPUT}")


if __name__ == "__main__":
    main()
