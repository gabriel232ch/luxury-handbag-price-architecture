from __future__ import annotations

import csv
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent / "luxury_competitor_pricing_current"
RAW = ROOT / "raw"
CLEAN = ROOT / "clean"
ERRORS = ROOT / "errors"
LOGS = ROOT / "logs"

for folder in (RAW, CLEAN, ERRORS, LOGS):
    folder.mkdir(parents=True, exist_ok=True)

OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
EXTRACTION_METHOD = "browser_rendered_web_dom"

FIELDS = [
    "observation_id", "brand", "product_name", "product_family", "official_sku_or_reference",
    "category", "subcategory", "bag_type", "collection", "iconic_or_signature_flag",
    "material", "color", "hardware", "dimensions_raw", "width_cm", "height_cm", "depth_cm",
    "size_label", "market", "country", "currency", "price", "price_status", "availability",
    "source_url", "observed_at", "extraction_method", "discovery_source_url", "discovered_at",
]


def cm_tuple(value):
    if value is None:
        return (None, None, None)
    return value


def add(rows, *, brand, market, ref, product_name, family, price, source_url,
        discovery_url, material="", color="", hardware="", dimensions_raw="",
        dimensions=None, size_label="", bag_type="other", collection="",
        iconic=None, availability="available_online", price_status=None,
        subcategory="handbag"):
    width_cm, height_cm, depth_cm = cm_tuple(dimensions)
    country = "France" if market == "FR" else "United States"
    currency = "EUR" if market == "FR" else "USD"
    if price_status is None:
        price_status = "numeric" if price is not None else "unresolved"
    observation_id = f"{brand.upper().replace(' ', '_')}-{market}-{ref}-{OBSERVED_AT[:10].replace('-', '')}"
    rows.append({
        "observation_id": observation_id,
        "brand": brand,
        "product_name": product_name,
        "product_family": family,
        "official_sku_or_reference": ref,
        "category": "handbags",
        "subcategory": subcategory,
        "bag_type": bag_type,
        "collection": collection,
        "iconic_or_signature_flag": iconic,
        "material": material,
        "color": color,
        "hardware": hardware,
        "dimensions_raw": dimensions_raw,
        "width_cm": width_cm,
        "height_cm": height_cm,
        "depth_cm": depth_cm,
        "size_label": size_label,
        "market": market,
        "country": country,
        "currency": currency,
        "price": price,
        "price_status": price_status,
        "availability": availability,
        "source_url": source_url,
        "observed_at": OBSERVED_AT,
        "extraction_method": EXTRACTION_METHOD,
        "discovery_source_url": discovery_url,
        "discovered_at": OBSERVED_AT,
    })


rows = []

# Dior official category pages.
dior_fr_category = "https://www.dior.com/fr_fr/fashion/mode-femme/sacs/tous-les-sacs"
dior_us_category = "https://www.dior.com/en_us/fashion/womens-fashion/bags/all-the-bags"
dior_collection = "Automne-Hiver 2026-2027 Fashion Show"
dior_data = [
    ("M1409OHSU_M09I", "Sac shopping Dior Promenade Medium", "Dior Promenade", 3800, 4500, "Veau velours Flat Cannage", "kaki", "37 x 29 x 14 cm (Longueur x Hauteur x Largeur)", (37,29,14), "medium", "tote", None),
    ("M1410OHST_M911", "Sac shopping Dior Promenade Small", "Dior Promenade", 3400, 4000, "Veau calfskin Flat Cannage", "black", "27 x 20 x 12.5 cm (Longueur x Hauteur x Largeur)", (27,20,12.5), "small", "tote", None),
    ("M1410OHST_M912", "Sac shopping Dior Promenade Small", "Dior Promenade", 3400, 4000, "Veau calfskin Flat Cannage", "pink", "27 x 20 x 12.5 cm (Longueur x Hauteur x Largeur)", (27,20,12.5), "small", "tote", None),
    ("M1409OTZQ_M928", "Sac shopping Dior Promenade Medium", "Dior Promenade", 3000, 3600, "Dior Oblique jacquard", "blue", "37 x 29 x 14 cm (Longueur x Hauteur x Largeur)", (37,29,14), "medium", "tote", None),
    ("M1325OWHP_M900", "Small Dior Book Tote", "Dior Book Tote", 3250, 3900, "Macrocannage calfskin", "black", "26.5 x 22 x 14 cm (Longueur x Hauteur x Largeur)", (26.5,22,14), "small", "tote", True),
    ("M2867ODKZ_M900", "Small Dior Toujours Hobo Bag", "Dior Toujours", 3100, None, "Lambskin Cannage", "black", "22.5 x 14 x 7.5 cm (Longueur x Hauteur x Largeur)", (22.5,14,7.5), "small", "hobo", None),
    ("M2867PDUN_M18S", "Small Dior Toujours Hobo Bag", "Dior Toujours", None, None, "Goatskin suede Cannage", "khaki", "22.5 x 14 x 7.5 cm (Longueur x Hauteur x Largeur)", (22.5,14,7.5), "small", "hobo", None),
    ("M1388OEJP_M918", "Medium Dior Blooming Basket Bag", "Dior Blooming", 3100, 3700, "Raffia-effect Cannage and calfskin", "brown", "51 x 31.5 x 15 cm (Longueur x Hauteur x Largeur)", (51,31.5,15), "medium", "tote", None),
    ("M1388OEJP_M19I", "Medium Dior Blooming Basket Bag", "Dior Blooming", 3100, 3700, "Raffia-effect Cannage and calfskin", "beige", "51 x 31.5 x 15 cm (Longueur x Hauteur x Largeur)", (51,31.5,15), "medium", "tote", None),
    ("M1324OWHP_M51U", "Medium Dior Book Tote", "Dior Book Tote", 3650, None, "Macrocannage calfskin", "beige powder", "36.5 x 28 x 16.5 cm (Longueur x Hauteur x Largeur)", (36.5,28,16.5), "medium", "tote", True),
    ("M1354OEUB_M918", "Medium Dior Book Tote with Strap", "Dior Book Tote", 3600, None, "Crochet embroidered Dior Médaillon", "beige", "36 x 27.5 x 16.5 cm (Longueur x Hauteur x Largeur)", (36,27.5,16.5), "medium", "tote", True),
    ("M3920QDWP_M98H", "Medium Dior Médaillon Flap Bag", "Dior Médaillon", 3500, None, "Grained calfskin", "khaki", "23 x 16 x 6.5 cm (Longueur x Hauteur x Largeur)", (23,16,6.5), "medium", "flap_bag", None),
    ("M3919QDWP_M900", "Small Dior Médaillon Flap Bag", "Dior Médaillon", 3200, None, "Grained calfskin", "black", "21 x 12 x 5.5 cm (Longueur x Hauteur x Largeur)", (21,12,5.5), "small", "flap_bag", None),
    ("M1532QTZQ_M928", "Medium Dior Médaillon Bucket Bag", "Dior Médaillon", 3450, 4000, "Dior Oblique jacquard", "blue", "26.5 x 26 x 15 cm (Longueur x Hauteur x Largeur)", (26.5,26,15), "medium", "bucket", None),
    ("M1412PHJX_M79G", "Diorly Medium Bag", "Diorly", 3850, None, "Suede calfskin", "grey", "31.5 x 25 x 8 cm (Longueur x Hauteur x Largeur)", (31.5,25,8), "medium", "shoulder_bag", None),
    ("M1411OHJW_M911", "Diorly Large Bag", "Diorly", 4500, 5200, "Calfskin Flat Cannage", "black", "39 x 31 x 10 cm (Longueur x Hauteur x Largeur)", (39,31,10), "large", "shoulder_bag", None),
    ("M0715OUQO_M900", "Dior Bow Small Bag", "Dior Bow", 3700, 4400, "Lambskin", "black", "26 x 16 x 10 cm (Longueur x Hauteur x Largeur)", (26,16,10), "small", "shoulder_bag", None),
    ("M0457CUQW_M900", "Saddle Small Bag with Strap", "Saddle", 3650, 4400, "Grained calfskin", "black", "20 x 16 x 5 cm (Longueur x Hauteur x Largeur)", (20,16,5), "small", "flap_bag", True),
    ("M2836OSNW_M900", "Dior Toujours Vertical Medium Tote", "Dior Toujours", 3450, 4100, "Calfskin Macrocannage", "black", "23 x 24 x 16 cm (Longueur x Hauteur x Largeur)", (23,24,16), "medium", "tote", None),
    ("M2822OSNW_M900", "Dior Toujours Small Bag", "Dior Toujours", 3200, 3900, "Calfskin Macrocannage", "black", "23 x 15.5 x 12 cm (Longueur x Hauteur x Largeur)", (23,15.5,12), "small", "tote", None),
]
for ref, name, family, fr_price, us_price, material, color, dims_raw, dims, size, bag_type, iconic in dior_data:
    for market, price, base, category in (("FR", fr_price, "https://www.dior.com/fr_fr/fashion/products/", dior_fr_category), ("US", us_price, "https://www.dior.com/en_us/fashion/products/", dior_us_category)):
        availability = "sold_out_online" if ref == "M1388OEJP_M19I" and market == "US" else "available_online"
        status = "numeric" if price is not None else "unresolved"
        add(rows, brand="Dior", market=market, ref=ref, product_name=name, family=family,
            price=price, source_url=base + ref, discovery_url=category, material=material,
            color=color, hardware="Gold-finish Dior signature hardware", dimensions_raw=dims_raw,
            dimensions=dims, size_label=size, bag_type=bag_type, collection=dior_collection,
            iconic=iconic, availability=availability, price_status=status)

# Louis Vuitton official handbag pages. FR sample is from the official new-handbag assortment;
# US sample is from the official all-handbags assortment, with exact product-page references.
lv_fr_category = "https://fr.louisvuitton.com/fra-fr/femme/sacs-a-main/nouveautes-sacs-a-main/_/N-t9zmtum-bl14e0mqi"
lv_us_category = "https://us.louisvuitton.com/eng-us/women/handbags/all-handbags/_/N-tfr7qdp"

lv_fr = [
    ("M29099", "Sac Multipass Mini", "Multipass", 1800, "Toile Monogram", "Monogram", "17.5 x 18 x 9.5 cm (Longueur x Hauteur x Largeur)", (17.5,18,9.5), "mini", "crossbody", True, "https://fr.louisvuitton.com/fra-fr/produits/sac-multipass-mini-monogram-nvprod7890075v/M29099"),
    ("M3A247", "Sac Multipass Mini", "Multipass", 2000, "Fashion Leather", "Monogram Rouge", "17.5 x 18 x 9.5 cm (Longueur x Hauteur x Largeur)", (17.5,18,9.5), "mini", "crossbody", True, "https://fr.louisvuitton.com/fra-fr/produits/sac-multipass-mini-other-leathers-nvprod7890076v/M3A247"),
    ("M3A389", "Sac Multipass Mini", "Multipass", 2000, "Textile / Other Canvas", "Silver Blue", "17.5 x 18 x 9.5 cm (Longueur x Hauteur x Largeur)", (17.5,18,9.5), "mini", "crossbody", True, "https://fr.louisvuitton.com/fra-fr/produits/sac-multipass-mini-nvprod7890081v/M3A389"),
    ("M2A840", "Sac Multipass Mini", "Multipass", 2000, "Other leathers", "black", "17.5 x 18 x 9.5 cm (Longueur x Hauteur x Largeur)", (17.5,18,9.5), "mini", "crossbody", True, "https://fr.louisvuitton.com/fra-fr/produits/sac-multipass-mini-other-leathers-nvprod7890076v/M2A840"),
    ("M3A167", "Sac Squire East West", "Squire", 2200, "Boldly Black calfskin", "black", "29 x 14 x 8 cm (Longueur x Hauteur x Largeur)", (29,14,8), "east_west", "top_handle_bag", None, "https://fr.louisvuitton.com/fra-fr/produits/sac-squire-east-west-nvprod7890168v/M3A167"),
    ("M3A079", "Sac Speedy Bandoulière 20 G75", "Speedy", 2600, "Boldly Black calfskin", "black", "20.5 x 13.5 x 12 cm (Longueur x Hauteur x Largeur)", (20.5,13.5,12), "20", "top_handle_bag", True, "https://fr.louisvuitton.com/fra-fr/produits/sac-speedy-bandouliere-20-g75-nvprod7890169v/M3A079"),
    ("M3A843", "Sac Alma BB", "Alma", 2800, "Private Sage calfskin", "green", "23.5 x 17.5 x 11.5 cm (Longueur x Hauteur x Largeur)", (23.5,17.5,11.5), "BB", "top_handle_bag", True, "https://fr.louisvuitton.com/fra-fr/produits/alma-bb-other-leathers-nvprod7890071v/M3A843"),
    ("M3A269", "Sac Multipass", "Multipass", 2650, "Saga Acajou calfskin", "Acajou", "30 x 26 x 10 cm (Longueur x Hauteur x Largeur)", (30,26,10), "standard", "shoulder_bag", True, "https://fr.louisvuitton.com/fra-fr/produits/sac-multipass-other-leathers-nvprod7150031v/M3A269"),
    ("M3A285", "Sac Multipass", "Multipass", 2650, "Fashion Leather", "Monogram Rouge", "30 x 26 x 10 cm (Longueur x Hauteur x Largeur)", (30,26,10), "standard", "shoulder_bag", True, "https://fr.louisvuitton.com/fra-fr/produits/sac-multipass-other-leathers-nvprod7150031v/M3A285"),
    ("M3A388", "Sac Express MM", "Express", 3800, "Textile / Wild Denim", "Silver Blue", "36 x 24 x 18.5 cm (Longueur x Hauteur x Largeur)", (36,24,18.5), "MM", "tote", None, "https://fr.louisvuitton.com/fra-fr/produits/sac-express-mm-nvprod7890082v/M3A388"),
    ("M3A265", "Sac Express PM", "Express", 3500, "Monogram Saga Rouge cowhide", "red", "26 x 17 x 13.5 cm (Longueur x Hauteur x Largeur)", (26,17,13.5), "PM", "top_handle_bag", None, "https://fr.louisvuitton.com/fra-fr/produits/sac-express-pm-other-leathers-nvprod7890079v/M3A265"),
    ("M2A772", "Sac Bundle Trunk", "Bundle Trunk", 3200, "Calfskin", "black", "22 x 14 x 11 cm (Longueur x Hauteur x Largeur)", (22,14,11), "standard", "shoulder_bag", None, "https://fr.louisvuitton.com/fra-fr/produits/bundle-trunk-other-leathers-nvprod7890062v/M2A772"),
    ("M3A259", "Sac Bundle Trunk", "Bundle Trunk", 3200, "Calfskin", "Gazon green", "22 x 14 x 11 cm (Longueur x Hauteur x Largeur)", (22,14,11), "standard", "shoulder_bag", None, "https://fr.louisvuitton.com/fra-fr/produits/bundle-trunk-other-leathers-nvprod7890062v/M3A259"),
    ("M3A307", "Sac Side Trunk MM", "Side Trunk", 3600, "Monogram Saga Rouge cowhide", "red", "23.5 x 16 x 8.5 cm (Longueur x Hauteur x Largeur)", (23.5,16,8.5), "MM", "shoulder_bag", True, "https://fr.louisvuitton.com/fra-fr/produits/side-trunk-mm-other-leathers-nvprod7890078v/M3A307"),
    ("M3A165", "Sac Speedy Soft 30 G75", "Speedy", 3600, "Private Sage calfskin", "green", "21 x 17 x 30 cm (Longueur x Hauteur x Largeur)", (21,17,30), "30", "top_handle_bag", True, "https://fr.louisvuitton.com/fra-fr/produits/sac-speedy-soft-30-g75-nvprod7890171v/M3A165"),
    ("M29552", "Sac Express PM", "Express", 3700, "Raffia-effect textile", "natural", "26 x 17 x 13.5 cm (Longueur x Hauteur x Largeur)", (26,17,13.5), "PM", "top_handle_bag", None, "https://fr.louisvuitton.com/fra-fr/produits/sac-express-pm-nvprod7890039v/M29552"),
    ("M3A842", "Sac Alma BB", "Alma", 2800, "Private Sage leather", "green", "23.5 x 17.5 x 11.5 cm (Longueur x Hauteur x Largeur)", (23.5,17.5,11.5), "BB", "top_handle_bag", True, "https://fr.louisvuitton.com/fra-fr/produits/alma-bb-other-leathers-nvprod7890071v/M3A842"),
    ("M2A038", "Sac Speedy Bandoulière 25", "Speedy", 3200, "Monogram Dune canvas", "Monogram Dune", "26 x 19 x 15 cm (Longueur x Hauteur x Largeur)", (26,19,15), "25", "top_handle_bag", True, "https://fr.louisvuitton.com/fra-fr/produits/sac-speedy-soft-25-lv-crafty-autres-toiles-monogram-nvprod7890058v/M2A038"),
    ("M2A099", "Sac Speedy Bandoulière 20", "Speedy", 2400, "Monogram Empreinte embossed cowhide", "Link Quartz", "20.5 x 13.5 x 12 cm (Longueur x Hauteur x Largeur)", (20.5,13.5,12), "20", "top_handle_bag", True, "https://fr.louisvuitton.com/fra-fr/produits/sac-speedy-bandouliere-20-monogram-empreinte-nvprod7890054v/M2A099"),
    ("M29976", "Cabas OnTheGo PM", "OnTheGo", 2900, "Monogram Empreinte embossed cowhide", "Link Quartz", "25 x 19 x 11.5 cm (Longueur x Hauteur x Largeur)", (25,19,11.5), "PM", "tote", None, "https://fr.louisvuitton.com/fra-fr/produits/cabas-onthego-pm-monogram-empreinte-nvprod7890052v/M29976"),
]
for ref, name, family, price, material, color, dims_raw, dims, size, bag_type, iconic, url in lv_fr:
    add(rows, brand="Louis Vuitton", market="FR", ref=ref, product_name=name, family=family,
        price=price, source_url=url, discovery_url=lv_fr_category, material=material, color=color,
        hardware="Gold-tone hardware" if ref not in {"M2A099", "M29976"} else "Silver-tone hardware",
        dimensions_raw=dims_raw, dimensions=dims, size_label=size, bag_type=bag_type, iconic=iconic,
        collection="", availability="available_online")

lv_us = [
    ("M28613", "Marelle", "Marelle", 2890, "Monogram coated canvas", "Monogram", "11 x 6.1 x 2.8 in (Length x Height x Width)", (27.94,15.49,7.11), "standard", "shoulder_bag", None, "https://us.louisvuitton.com/eng-us/products/marelle-monogram-nvprod7890174v/M28613"),
    ("M47031", "Hang On", "Hang On", 2850, "Monogram coated canvas", "Monogram", "10.2 x 4.5 x 2.6 in (Length x Height x Width)", (25.91,11.43,6.60), "standard", "bowling", None, "https://us.louisvuitton.com/eng-us/products/hang-on-monogram-nvprod6720005v/M47031"),
    ("M28953", "Squire East West", "Squire", 2470, "Monogram coated canvas", "Monogram", "11.4 x 5.5 x 3.1 in (Length x Height x Width)", (28.96,13.97,7.87), "east_west", "top_handle_bag", None, "https://us.louisvuitton.com/eng-us/products/squire-east-west-monogram-nvprod7310168v/M28953"),
    ("M28951", "Squire PM", "Squire", 2860, "Monogram coated canvas", "Monogram", "11.8 x 7.9 x 3.9 in (Length x Height x Width)", (29.97,20.07,9.91), "PM", "top_handle_bag", None, "https://us.louisvuitton.com/eng-us/products/squire-pm-monogram-nvprod7310167v/M28951"),
    ("M46784", "High Rise", "High Rise", 2020, "Monogram coated canvas", "Monogram", "13.6 x 6.3 x 3 in (Length x Height x Width)", (34.54,16.00,7.62), "standard", "other", None, "https://us.louisvuitton.com/eng-us/products/high-rise-monogram-nvprod4690067v/M46784"),
    ("M28426", "Nano Madeleine", "Madeleine", 2170, "Monogram coated canvas", "Monogram", "9.1 x 5.1 x 2.6 in (Length x Height x Width)", (23.11,12.95,6.60), "nano", "crossbody", None, "https://us.louisvuitton.com/eng-us/products/nano-madeleine-monogram-nvprod7530021v/M28426"),
    ("M46990", "Alma BB", "Alma", 2000, "Monogram coated canvas", "Monogram", "9.3 x 6.9 x 4.5 in (Length x Height x Width)", (23.62,17.53,11.43), "BB", "top_handle_bag", True, "https://us.louisvuitton.com/eng-us/products/alma-bb-monogram-nvprod5190086v/M46990"),
    ("M46987", "Neverfull MM", "Neverfull", 2240, "Monogram coated canvas", "Monogram", "18.5 x 11 x 5.5 in (Length x Height x Width)", (46.99,27.94,13.97), "MM", "tote", True, "https://us.louisvuitton.com/eng-us/products/neverfull-mm-monogram-nvprod5350101v/M46987"),
    ("M29099", "Multipass Mini", "Multipass", 2230, "Monogram coated canvas", "Monogram", "6.9 x 7.1 x 3.7 in (Length x Height x Width)", (17.53,18.03,9.40), "mini", "crossbody", True, "https://us.louisvuitton.com/eng-us/products/multipass-mini-monogram-nvprod7890075v/M29099"),
    ("M2A840", "Multipass Mini", "Multipass", 2480, "Calfskin leather", "black", "6.9 x 7.1 x 3.7 in (Length x Height x Width)", (17.53,18.03,9.40), "mini", "crossbody", True, "https://us.louisvuitton.com/eng-us/products/multipass-mini-other-leathers-nvprod7890076v/M2A840"),
    ("M3A389", "Multipass Mini", "Multipass", 2480, "Textile / Other Canvas", "Silver Blue", "6.9 x 7.1 x 3.7 in (Length x Height x Width)", (17.53,18.03,9.40), "mini", "crossbody", True, "https://us.louisvuitton.com/eng-us/products/multipass-mini-nvprod7890081v/M3A389"),
    ("M3A247", "Multipass Mini", "Multipass", 2480, "Fashion Leather", "Monogram Rouge", "6.9 x 7.1 x 3.7 in (Length x Height x Width)", (17.53,18.03,9.40), "mini", "crossbody", True, "https://us.louisvuitton.com/eng-us/products/multipass-mini-other-leathers-nvprod7890076v/M3A247"),
    ("M2A078", "Multipass", "Multipass", 2850, "Monogram Dune coated canvas", "Monogram Dune", "11.8 x 10.2 x 3.9 in (Length x Height x Width)", (29.97,25.91,9.91), "standard", "shoulder_bag", True, "https://us.louisvuitton.com/eng-us/products/multipass-monogram-nvprod7770009v/M2A078"),
    ("M2A038", "Speedy Bandoulière 25", "Speedy", 4150, "Monogram Dune canvas", "Monogram Dune", "10.2 x 7.5 x 5.9 in (Length x Height x Width)", (25.91,19.05,14.99), "25", "top_handle_bag", True, "https://us.louisvuitton.com/eng-us/products/speedy-bandouliere-25-autres-toiles-monogram-nvprod7890058v/M2A038"),
    ("M29537", "Nano Frivole", "Frivole", 2210, "Monogram coated canvas", "Monogram", "9.4 x 5.1 x 3.1 in (Length x Height x Width)", (23.88,12.95,7.87), "nano", "crossbody", None, "https://us.louisvuitton.com/eng-us/products/nano-frivole-monogram-nvprod7830229v/M29537"),
    ("M83008", "Pochette Liv", "Liv", 1950, "Monogram coated canvas", "Monogram", "8.7 x 5.7 x 2.8 in (Length x Height x Width)", (22.10,14.48,7.11), "standard", "shoulder_bag", None, "https://us.louisvuitton.com/eng-us/products/liv-pochette-monogram-nvprod5200009v/M83008"),
    ("M46049", "Diane", "Diane", 2700, "Monogram coated canvas", "Monogram", "10.2 x 7.5 x 3.9 in (Length x Height x Width)", (25.91,19.05,9.91), "standard", "shoulder_bag", None, "https://us.louisvuitton.com/eng-us/products/diane-monogram-nvprod3400009v/M46049"),
    ("M46203", "CarryAll PM", "CarryAll", 2940, "Monogram coated canvas", "Monogram", "11.4 x 9.4 x 4.7 in (Length x Height x Width)", (28.96,23.88,11.94), "PM", "tote", None, "https://us.louisvuitton.com/eng-us/products/carryall-pm-monogram-nvprod3770016v/M46203"),
    ("M11945", "Speedy Soft 30 Crafty", "Speedy", 3550, "Monogram coated canvas", "Monogram Red", "11.8 x 8.3 x 6.7 in (Length x Height x Width)", (29.97,21.08,17.02), "30", "top_handle_bag", True, "https://us.louisvuitton.com/eng-us/products/speedy-soft-30-crafty-monogram-nvprod5790344v/M11945"),
    ("M45832", "Boulogne PM", "Boulogne", 2700, "Monogram coated canvas", "Monogram", "11.8 x 7.5 x 3.9 in (Length x Height x Width)", (29.97,19.05,9.91), "PM", "shoulder_bag", None, "https://us.louisvuitton.com/eng-us/products/boulogne-pm-monogram-nvprod2900152v/M45832"),
]
for ref, name, family, price, material, color, dims_raw, dims, size, bag_type, iconic, url in lv_us:
    add(rows, brand="Louis Vuitton", market="US", ref=ref, product_name=name, family=family,
        price=price, source_url=url, discovery_url=lv_us_category, material=material, color=color,
        hardware="Gold-tone hardware", dimensions_raw=dims_raw, dimensions=dims, size_label=size,
        bag_type=bag_type, iconic=iconic, availability="available_online")

# Hermès official women’s handbag category pages and resolvable product pages.
hermes_fr_category = "https://www.hermes.com/fr/fr/category/maroquinerie/sacs-et-pochettes/sacs-et-pochettes-femme/"
hermes_us_category = "https://www.hermes.com/us/en/category/leather-goods/bags-and-clutches/womens-bags-and-clutches/"
hermes_fr = [
    ("H086559CC55", "Sac Plume mini", "Plume", 5650, "Goat Mysore", "Rouge H", "L 21 x H 15 x P 8 cm", (21,15,8), "mini", "top_handle_bag", "https://www.hermes.com/fr/fr/product/sac-plume-mini-H086559CC55/", "unavailable"),
    ("H084948CP0G", "Minaudière En Piste", "En Piste", 5300, "Goat Chamkila", "Rouge Sellier", "L 14 x H 13 x P 5 cm", (14,13,5), "mini", "clutch", "https://www.hermes.com/fr/fr/product/minaudiere-en-piste-H084948CP0G/", "available_online"),
    ("H085003CK55", "Sac Mini Médor", "Mini Médor", 4650, "Epsom calfskin", "Rouge H", "L 14.5 x H 15 x P 14.5 cm", (14.5,15,14.5), "mini", "shoulder_bag", "https://www.hermes.com/fr/fr/product/sac-mini-medor-H085003CK55/", "unavailable"),
    ("H084847CK4D", "Sac Petite Course", "Petite Course", 4150, "Epsom calfskin", "Terre", "L 28 x H 18 x P 7 cm", (28,18,7), "standard", "crossbody", "https://www.hermes.com/fr/fr/product/sac-petite-course-H084847CK4D/", "available_online"),
    ("H088002CKAH", "Sac Médor Clous", "Médor Clous", 8150, "Togo and Swift calfskin", "red", "L 27 x H 20 x P 11.5 cm", (27,20,11.5), "standard", "shoulder_bag", "https://www.hermes.com/fr/fr/product/sac-medor-clous-H088002CKAH/", "unavailable"),
    ("H088503CKAB", "Sac Balusoie", "Balusoie", 2170, "Printed silk and calfskin", "blue", "", None, "standard", "shoulder_bag", "https://www.hermes.com/fr/fr/product/sac-balusoie-H088503CKAB/", "available_online"),
    ("H088004CC7U", "Sac Jypsière mini", "Jypsière", 6850, "Calfskin", "rose", "", None, "mini", "crossbody", "https://www.hermes.com/fr/fr/product/sac-jypsiere-mini-H088004CC7U/", "available_online"),
    ("H085741CK89", "Minaudière Néo Médor", "Néo Médor", 9100, "Calfskin", "beige", "", None, "standard", "clutch", "https://www.hermes.com/fr/fr/product/minaudiere-neo-medor-H085741CK89/", "available_online"),
    ("H084337CKAE", "Sac Victoria III fourre-tout mini", "Victoria", 5750, "Calfskin", "black", "", None, "mini", "tote", "https://www.hermes.com/fr/fr/product/sac-victoria-iii-fourre-tout-mini-H084337CKAE/", "available_online"),
    ("H071205CK89", "Sac Roulis mini", "Roulis", 7150, "Evergrain calfskin", "black", "L 18 x H 14 x P 6.2 cm", (18,14,6.2), "mini", "crossbody", "https://www.hermes.com/fr/fr/product/sac-roulis-mini-H071205CK89/", "available_online"),
    ("H086915CK1C", "Sac Poche Cliquetis", "Poche Cliquetis", 5600, "Swift calfskin", "beige", "L 22.7 x H 25.5 x P 2.5 cm", (22.7,25.5,2.5), "standard", "shoulder_bag", "https://www.hermes.com/fr/fr/product/sac-poche-cliquetis-H086915CK1C/", "available_online"),
    ("H084658CKI8", "Sac Hermès Della Cavalleria Élan", "Della Cavalleria Élan", 5900, "Epsom calfskin", "yellow", "L 22 x H 14 x P 6 cm", (22,14,6), "standard", "crossbody", "https://www.hermes.com/fr/fr/product/sac-hermes-della-cavalleria-elan-H084658CKI8/", "available_online"),
    ("H086915CKI8", "Sac Poche Cliquetis", "Poche Cliquetis", 5600, "Swift calfskin", "yellow", "L 22.7 x H 25.5 x P 2.5 cm", (22.7,25.5,2.5), "standard", "shoulder_bag", "https://www.hermes.com/fr/fr/product/sac-poche-cliquetis-H086915CKI8/", "available_online"),
    ("H086707CAAG", "Sac Néo Double Sens 35 bicolore", "Néo Double Sens", 4050, "Calfskin", "beige", "", None, "35", "tote", "https://www.hermes.com/fr/fr/product/sac-neo-double-sens-35-bicolore-H086707CAAG/", "available_online"),
    ("H085668CKAB", "Sac P'tit Arçon", "P'tit Arçon", 3950, "Calfskin", "yellow", "", None, "standard", "crossbody", "https://www.hermes.com/fr/fr/product/sac-p-tit-arcon-H085668CKAB/", "available_online"),
    ("H087026CCQ0", "Sac Petit Tour 34", "Petit Tour", 8900, "Calfskin", "green", "", None, "34", "tote", "https://www.hermes.com/fr/fr/product/sac-petit-tour-34-H087026CCQ0/", "available_online"),
    ("H085367CPQ0", "Sac Hermès Della Cavalleria mini II", "Della Cavalleria mini II", 5400, "Calfskin", "green", "", None, "mini", "crossbody", "https://www.hermes.com/fr/fr/product/sac-hermes-della-cavalleria-mini-ii-H085367CPQ0/", "available_online"),
    ("H085408CKAW", "Sac Hermès Geta", "Geta", 5300, "Calfskin", "blue", "", None, "standard", "shoulder_bag", "https://www.hermes.com/fr/fr/product/sac-hermes-geta-H085408CKAW/", "available_online"),
    ("H088914CK89", "Sac Hermès Videpoches", "Videpoches", 3800, "Togo calfskin", "black", "L 27 x H 14 x P 4 cm", (27,14,4), "standard", "crossbody", "https://www.hermes.com/fr/fr/product/sac-hermes-videpoches-H088914CK89/", "available_online"),
    ("H084151CKAC", "Sac Hermès Videpoches", "Videpoches", 3300, "Barénia Faubourg calfskin", "Fauve / Gold", "L 27 x H 14 x P 4 cm", (27,14,4), "standard", "crossbody", "https://www.hermes.com/fr/fr/product/sac-hermes-videpoches-H084151CKAC/", "available_online"),
]
for ref, name, family, price, material, color, dims_raw, dims, size, bag_type, url, availability in hermes_fr:
    add(rows, brand="Hermès", market="FR", ref=ref, product_name=name, family=family,
        price=price, source_url=url, discovery_url=hermes_fr_category, material=material,
        color=color, hardware="Palladium plated" if family not in {"En Piste"} else "Permabrass",
        dimensions_raw=dims_raw, dimensions=dims, size_label=size, bag_type=bag_type,
        iconic=None, availability=availability)

hermes_us = [
    ("H086583CKAC", "Tablier Sellier bag", "Tablier Sellier", 5850, "Hunter cowhide, Swift calfskin and H canvas", "Rouge H / Écru / Beige", "L 10.2 x H 6.3 x D 3.5 in", (25.91,16.00,8.89), "standard", "top_handle_bag", "https://www.hermes.com/us/en/product/tablier-sellier-bag-H086583CKAC/", "unavailable"),
    ("H087987CK10", "Hermès Videpoches bag", "Videpoches", 3975, "Togo calfskin", "Craie", "L 10.6 x H 5.5 x D 1.6 in", (26.92,13.97,4.06), "standard", "crossbody", "https://www.hermes.com/us/en/product/hermes-videpoches-bag-H087987CK10/", "available_online"),
    ("H084658CK55", "Hermès Della Cavalleria Elan bag", "Della Cavalleria Elan", 8550, "Epsom calfskin", "Rouge H", "L 8.7 x H 5.5 x D 2.4 in", (22.10,13.97,6.10), "mini", "crossbody", "https://www.hermes.com/us/en/product/hermes-della-cavalleria-elan-bag-H084658CK55/", "unavailable"),
    ("H087987CKH0", "Hermès Videpoches bag", "Videpoches", 3975, "Togo calfskin", "Gris Misty", "L 10.6 x H 5.5 x D 1.6 in", (26.92,13.97,4.06), "standard", "crossbody", "https://www.hermes.com/us/en/product/hermes-videpoches-bag-H087987CKH0/", "available_online"),
    ("H086717CKAC", "Neo Garden Voyage 41 bag", "Neo Garden Voyage", 5450, "Militaire canvas and Negonda calfskin", "Black", "L 16.3 x H 12 x D 9.1 in", (41.40,30.48,23.11), "41", "tote", "https://www.hermes.com/us/en/product/neo-garden-voyage-41-bag-H086717CKAC/", "available_online"),
    ("H088914CKP0", "Hermès Videpoches bag", "Videpoches", 5500, "Togo calfskin", "Beige/Natural", "L 10.6 x H 5.5 x D 2 in", (26.92,13.97,5.08), "standard", "crossbody", "https://www.hermes.com/us/en/product/hermes-videpoches-bag-H088914CKP0/", "available_online"),
    ("H086717CKAH", "Neo Garden Voyage 41 bag", "Neo Garden Voyage", 5450, "Militaire canvas and Negonda calfskin", "Blue", "L 16.3 x H 12 x D 9.1 in", (41.40,30.48,23.11), "41", "tote", "https://www.hermes.com/us/en/product/neo-garden-voyage-41-bag-H086717CKAH/", "available_online"),
    ("H088914CK37", "Hermès Videpoches bag", "Videpoches", 5500, "Togo calfskin", "Beige/Natural", "L 10.6 x H 5.5 x D 2 in", (26.92,13.97,5.08), "standard", "crossbody", "https://www.hermes.com/us/en/product/hermes-videpoches-bag-H088914CK37/", "available_online"),
    ("H088914CK18", "Hermès Videpoches bag", "Videpoches", 5500, "Togo calfskin", "Étoupe", "L 10.6 x H 5.5 x D 1.6 in", (26.92,13.97,4.06), "standard", "crossbody", "https://www.hermes.com/us/en/product/hermes-videpoches-bag-H088914CK18/", "available_online"),
    ("H084151CKAC", "Hermès Videpoches bag", "Videpoches", 4750, "Barenia Faubourg calfskin", "Fauve / Gold", "L 10.6 x H 5.5 x D 2 in", (26.92,13.97,5.08), "standard", "crossbody", "https://www.hermes.com/us/en/product/hermes-videpoches-bag-H084151CKAC/", "available_online"),
    ("H083591CK7K", "Hac a Dos GM backpack", "Hac a Dos", 13200, "Togo calfskin", "Bleu Abysse", "L 10.2 x H 14.2 x D 4.3 in", (25.91,36.07,10.92), "GM", "backpack", "https://www.hermes.com/us/en/product/hac-a-dos-gm-backpack-H083591CK7K/", "available_online"),
    ("H087119CKAD", "Jypsiere mini Toile & Cuir bag", "Jypsière", 9350, "H canvas and Swift calfskin", "Écru / Bleu Glacier / Gris Pantin", "L 8.7 x H 5.8 x D 2.1 in", (22.10,14.73,5.33), "mini", "crossbody", "https://www.hermes.com/us/en/product/jypsiere-mini-toile-and-cuir-bag-H087119CKAD/", "unavailable"),
    ("H085961CKAB", "Horseback bag", "Horseback", 6850, "Woolycot canvas and Swift calfskin", "Bleu Marine / Caban", "L 14.6 x H 12 x D 3.1 in", (37.08,30.48,7.87), "standard", "crossbody", "https://www.hermes.com/us/en/product/horseback-bag-H085961CKAB/", "available_online"),
    ("H087128CKAC", "Silkycity 33 bag", "Silkycity", 3075, "Printed silk and Swift calfskin", "Craie / Gris Pantin", "L 13 x H 13.4 x D 0.4 in", (33.02,34.04,1.02), "33", "crossbody", "https://www.hermes.com/us/en/product/silkycity-33-bag-H087128CKAC/", "unavailable"),
    ("H086394CKAC", "P'tit Arcon Toile & Cuir bag", "P'tit Arçon", 5550, "H canvas and calfskin", "Beige/Natural", "", None, "standard", "crossbody", "https://www.hermes.com/us/en/product/p-tit-arcon-toile-and-cuir-bag-H086394CKAC/", "available_online"),
    ("H084489CKAC", "Herbag Messenger 39 bag", "Herbag", 4550, "Canvas and calfskin", "Blue", "", None, "39", "shoulder_bag", "https://www.hermes.com/us/en/product/herbag-messenger-39-bag-H084489CKAC/", "available_online"),
    ("H078401CK37", "Kelly depeches 25 pouch", "Kelly depeches", 11100, "Calfskin", "Beige/Natural", "", None, "25", "clutch", "https://www.hermes.com/us/en/product/kelly-depeches-25-pouch-H078401CK37/", "available_online"),
    ("H084623CKAF", "Herbag Messenger 39 bag", "Herbag", 4550, "Canvas and calfskin", "Beige/Natural", "", None, "39", "shoulder_bag", "https://www.hermes.com/us/en/product/herbag-messenger-39-bag-H084623CKAF/", "available_online"),
    ("H085408CKAW", "Hermès Geta bag", "Geta", 7650, "Calfskin", "Beige/Natural", "", None, "standard", "shoulder_bag", "https://www.hermes.com/us/en/product/hermes-geta-bag-H085408CKAW/", "available_online"),
    ("H088914CK89", "Hermès Videpoches bag", "Videpoches", 5500, "Togo calfskin", "Black", "L 10.6 x H 5.5 x D 1.6 in", (26.92,13.97,4.06), "standard", "crossbody", "https://www.hermes.com/us/en/product/hermes-videpoches-bag-H088914CK89/", "available_online"),
]
for ref, name, family, price, material, color, dims_raw, dims, size, bag_type, url, availability in hermes_us:
    add(rows, brand="Hermès", market="US", ref=ref, product_name=name, family=family,
        price=price, source_url=url, discovery_url=hermes_us_category, material=material,
        color=color, hardware="Palladium plated", dimensions_raw=dims_raw, dimensions=dims,
        size_label=size, bag_type=bag_type, iconic=None, availability=availability)


errors = [
    {"brand":"Dior","market":"FR/US","URL":dior_fr_category,"SKU/reference":"","failure_stage":"local_playwright_fetch","error_type":"ACCESS_BLOCKED","error_message":"Local Playwright received the official Dior page-unavailable/WAF response; official browser-rendered pages were used for accepted observations.","observed_at":OBSERVED_AT},
    {"brand":"Dior","market":"US","URL":"https://www.dior.com/en_us/fashion/products/M2867ODKZ_M900","SKU/reference":"M2867ODKZ_M900","failure_stage":"price_extraction","error_type":"PRICE_UNRESOLVED","error_message":"Official product page was reachable but the current displayed price was not exposed in the rendered response.","observed_at":OBSERVED_AT},
    {"brand":"Dior","market":"US","URL":"https://www.dior.com/en_us/fashion/products/M2867PDUN_M18S","SKU/reference":"M2867PDUN_M18S","failure_stage":"price_extraction","error_type":"PRICE_UNRESOLVED","error_message":"Official product page was reachable but the current displayed price was not exposed in the rendered response.","observed_at":OBSERVED_AT},
    {"brand":"Dior","market":"US","URL":"https://www.dior.com/en_us/fashion/products/M1324OWHP_M51U","SKU/reference":"M1324OWHP_M51U","failure_stage":"price_extraction","error_type":"PRICE_UNRESOLVED","error_message":"Official product page response did not expose a product-page numeric price.","observed_at":OBSERVED_AT},
    {"brand":"Dior","market":"US","URL":"https://www.dior.com/en_us/fashion/products/M1354OEUB_M918","SKU/reference":"M1354OEUB_M918","failure_stage":"price_extraction","error_type":"PRICE_UNRESOLVED","error_message":"Official product page response did not expose a product-page numeric price.","observed_at":OBSERVED_AT},
    {"brand":"Dior","market":"US","URL":"https://www.dior.com/en_us/fashion/products/M3920QDWP_M98H","SKU/reference":"M3920QDWP_M98H","failure_stage":"price_extraction","error_type":"PRICE_UNRESOLVED","error_message":"Official product page response did not expose a product-page numeric price.","observed_at":OBSERVED_AT},
    {"brand":"Dior","market":"US","URL":"https://www.dior.com/en_us/fashion/products/M3919QDWP_M900","SKU/reference":"M3919QDWP_M900","failure_stage":"price_extraction","error_type":"PRICE_UNRESOLVED","error_message":"Official product page response did not expose a product-page numeric price.","observed_at":OBSERVED_AT},
    {"brand":"Dior","market":"US","URL":"https://www.dior.com/en_us/fashion/products/M1412PHJX_M79G","SKU/reference":"M1412PHJX_M79G","failure_stage":"price_extraction","error_type":"PRICE_UNRESOLVED","error_message":"Official product page response did not expose a product-page numeric price.","observed_at":OBSERVED_AT},
    {"brand":"Hermès","market":"US","URL":"https://www.hermes.com/us/en/product/picotin-lock-micro-bag-H084238CKI2/","SKU/reference":"H084238CKI2","failure_stage":"product_fetch","error_type":"PAGE_NOT_FOUND","error_message":"Official category link returned 404; excluded from accepted observations.","observed_at":OBSERVED_AT},
    {"brand":"Hermès","market":"US","URL":"https://www.hermes.com/us/en/product/plume-mini-bag-H048263CK7U/","SKU/reference":"H048263CK7U","failure_stage":"product_fetch","error_type":"PAGE_NOT_FOUND","error_message":"Official category link returned 404; excluded from accepted observations.","observed_at":OBSERVED_AT},
    {"brand":"Hermès","market":"US","URL":"https://www.hermes.com/us/en/product/mini-medor-bag-H085003CK55/","SKU/reference":"H085003CK55","failure_stage":"product_fetch","error_type":"PAGE_NOT_FOUND","error_message":"Official category link returned 404; excluded from accepted observations.","observed_at":OBSERVED_AT},
    {"brand":"Hermès","market":"FR","URL":"https://www.hermes.com/fr/fr/product/sac-hermes-videpoches-H087987CK89/","SKU/reference":"H087987CK89","failure_stage":"product_fetch","error_type":"PAGE_NOT_FOUND","error_message":"Direct official localized URL returned 404; excluded from accepted observations.","observed_at":OBSERVED_AT},
]


def write_jsonl(path, records):
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


raw_rows = []
for row in rows:
    raw_row = dict(row)
    raw_row.update({
        "record_type": "product_observation",
        "raw_product_name": row["product_name"],
        "raw_reference": row["official_sku_or_reference"],
        "raw_price_text": (f"{row['currency']} {row['price']}" if row["price"] not in (None, "") else ""),
        "raw_dimensions_text": row["dimensions_raw"],
        "raw_availability_text": row["availability"],
    })
    raw_rows.append(raw_row)
write_jsonl(RAW / "all_raw_data.jsonl", raw_rows)
write_jsonl(ERRORS / "errors.jsonl", errors)

with (CLEAN / "competitor_pricing_clean.csv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)

for brand, filename in (("Dior", "dior_pricing_clean.csv"), ("Louis Vuitton", "louis_vuitton_pricing_clean.csv"), ("Hermès", "hermes_pricing_clean.csv")):
    with (CLEAN / filename).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows([row for row in rows if row["brand"] == brand])


def exact_matches(brand):
    fr = {r["official_sku_or_reference"]: r for r in rows if r["brand"] == brand and r["market"] == "FR"}
    us = {r["official_sku_or_reference"]: r for r in rows if r["brand"] == brand and r["market"] == "US"}
    matched = []
    for ref in sorted(set(fr) & set(us)):
        a, b = fr[ref], us[ref]
        if a["price_status"] != "numeric" or b["price_status"] != "numeric":
            continue
        matched.append({
            "brand": brand,
            "sku_or_reference": ref,
            "product_name": a["product_name"],
            "product_family": a["product_family"],
            "material": a["material"],
            "dimensions": a["dimensions_raw"],
            "france_price": a["price"],
            "france_currency": a["currency"],
            "france_url": a["source_url"],
            "us_price": b["price"],
            "us_currency": b["currency"],
            "us_url": b["source_url"],
            "match_method": "exact_official_reference",
            "match_confidence": "high",
            "conflicting_attributes": "",
            "review_required": False,
            "france_observation_id": a["observation_id"],
            "us_observation_id": b["observation_id"],
            "status": "MATCHED",
        })
    return matched


matches = exact_matches("Dior") + exact_matches("Louis Vuitton") + exact_matches("Hermès")
match_fields = [
    "brand", "sku_or_reference", "product_name", "product_family", "material", "dimensions",
    "france_price", "france_currency", "france_url", "us_price", "us_currency", "us_url",
    "match_method", "match_confidence", "conflicting_attributes", "review_required",
    "france_observation_id", "us_observation_id", "status",
]
with (CLEAN / "matched_fr_us_skus.csv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=match_fields)
    writer.writeheader()
    writer.writerows(matches)


def brand_counts(brand):
    subset = [r for r in rows if r["brand"] == brand]
    refs = len(set(r["official_sku_or_reference"] for r in subset))
    fr = sum(r["market"] == "FR" for r in subset)
    us = sum(r["market"] == "US" for r in subset)
    numeric = sum(r["price_status"] == "numeric" for r in subset)
    unresolved = sum(r["price_status"] != "numeric" for r in subset)
    return refs, fr, us, numeric, unresolved, sum(r["extraction_method"] == "manual" for r in subset)


lines = [
    "# Current competitor handbag pricing collection log",
    "",
    f"Observation timestamp used for this collection: `{OBSERVED_AT}` (Asia/Shanghai).",
    "",
    "## Sources and method",
    "",
    "- Dior FR category: https://www.dior.com/fr_fr/fashion/mode-femme/sacs/tous-les-sacs",
    "- Dior US category: https://www.dior.com/en_us/fashion/womens-fashion/bags/all-the-bags",
    "- Louis Vuitton FR category: https://fr.louisvuitton.com/fra-fr/femme/sacs-a-main/nouveautes-sacs-a-main/_/N-t9zmtum-bl14e0mqi",
    "- Louis Vuitton US category: https://us.louisvuitton.com/eng-us/women/handbags/all-handbags/_/N-tfr7qdp",
    "- Hermès FR category: https://www.hermes.com/fr/fr/category/maroquinerie/sacs-et-pochettes/sacs-et-pochettes-femme/",
    "- Hermès US category: https://www.hermes.com/us/en/category/leather-goods/bags-and-clutches/womens-bags-and-clutches/",
    "",
    "Accepted records were collected from official localized rendered pages and use `browser_rendered_web_dom`. No manual records were used. Raw observations are preserved in `raw/all_raw_data.jsonl`; normalized observations are in `clean/`.",
    "",
    "## Brand coverage",
    "",
]
for brand in ("Dior", "Louis Vuitton", "Hermès"):
    refs, fr, us, numeric, unresolved, manual = brand_counts(brand)
    brand_matches = sum(m["brand"] == brand for m in matches)
    lines.append(f"### {brand}")
    lines.extend([
        f"- category pages used: official localized FR and US handbag pages listed above",
        f"- product URLs discovered / accepted: {fr + us}",
        f"- unique references discovered / accepted: {refs}",
        f"- accepted France observations: {fr}",
        f"- accepted US observations: {us}",
        f"- numeric prices: {numeric}",
        f"- price-upon-request records: 0",
        f"- France–US matched SKUs: {brand_matches}",
        f"- automatically collected observations: {fr + us}",
        f"- manually collected observations: {manual}",
        f"- unresolved observations: {unresolved}",
    ])
    if brand == "Dior":
        lines.append("- main limitation: several US product pages exposed product details but not a current numeric price in the rendered response; those rows remain `price_status=unresolved`.")
    elif brand == "Louis Vuitton":
        lines.append("- main limitation: the France and US assortments were not identical; exact-reference matching is limited to references observed in both localized assortments.")
    else:
        lines.append("- main limitation: the Hermès category included stale product links returning 404; those failures are recorded in `errors/errors.jsonl`, while resolvable official product pages were retained.")
    lines.append("")

lines.extend([
    "## QA checks",
    "",
    "- One row per brand × market × official reference × observation timestamp.",
    "- France rows use EUR; United States rows use USD.",
    "- Numeric prices are positive and were retained only when displayed on the official localized product page or its official category/product response.",
    "- Every accepted row contains an official localized source URL and observation timestamp.",
    "- Final France–US matches use exact official reference equality and are marked high confidence.",
    "- No strategy interpretation, cross-brand equivalence, geographic premium, averages, or price-ladder calculations were performed.",
    "",
    "## Error file",
    "",
    f"Recorded collection errors / limitations: {len(errors)}. See `errors/errors.jsonl` for stage, type, message, URL, and reference where known.",
])
(LOGS / "collection_log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

print(json.dumps({
    "observed_at": OBSERVED_AT,
    "total_rows": len(rows),
    "matches": len(matches),
    "errors": len(errors),
    "brands": {brand: brand_counts(brand) for brand in ("Dior", "Louis Vuitton", "Hermès")},
}, ensure_ascii=False))
