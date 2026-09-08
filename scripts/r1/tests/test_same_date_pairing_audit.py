import unittest

from scripts.r1.build_same_date_pairing_audit import (
    classify_chanel_row,
    gate_cell,
)


class SameDatePairingAuditTests(unittest.TestCase):
    def test_chanel_small_shopping_row_gets_exact_group_attributes(self):
        row = {
            "brand": "Chanel",
            "reference_code": "AS6495B25347UC476",
            "product_name": "Small Shopping Bag",
            "material_raw": "Lambskin & Gold-Tone Metal",
        }

        result = classify_chanel_row(row)

        self.assertEqual(result["bag_type"], "tote")
        self.assertEqual(result["size_label"], "small")
        self.assertEqual(result["material_group"], "leather")

    def test_verified_seasonal_override_blocks_regular_core(self):
        row = {
            "brand": "Chanel",
            "reference_code": "AS6495B25347UC476",
            "product_name": "Small Shopping Bag",
            "material_raw": "Lambskin & Gold-Tone Metal",
        }

        result = classify_chanel_row(
            row,
            {
                "AS6495B25347UC476": {
                    "regular_special": "seasonal_collection",
                    "collection_label": "Fall Winter 2026 Pre-Collection",
                }
            },
        )

        self.assertEqual(result["regular_special"], "seasonal_collection")
        self.assertEqual(result["collection_label"], "Fall Winter 2026 Pre-Collection")
        self.assertEqual(result["scope_status"], "seasonal_excluded")
        self.assertEqual(result["pairing_readiness"], "blocked")

    def test_cell_requires_two_numeric_rows_per_brand_and_two_brands(self):
        rows = [
            {"brand": "Chanel", "price": "6600", "scope_status": "status_pending", "size_label": "small"},
            {"brand": "Chanel", "price": "6600", "scope_status": "status_pending", "size_label": "small"},
            {"brand": "Dior", "price": "4000", "scope_status": "status_pending", "size_label": "small"},
            {"brand": "Dior", "price": "4000", "scope_status": "status_pending", "size_label": "small"},
        ]

        result = gate_cell(rows, minimum_per_brand=2)

        self.assertTrue(result["headline_eligible"])
        self.assertEqual(result["pairing_status"], "same_date_exact_attributes")

    def test_unknown_size_is_blocked_even_when_sample_is_large(self):
        rows = [
            {"brand": "Chanel", "price": "6600", "scope_status": "unknown_size", "size_label": "unknown"},
            {"brand": "Chanel", "price": "6600", "scope_status": "unknown_size", "size_label": "unknown"},
            {"brand": "Dior", "price": "4000", "scope_status": "status_pending", "size_label": "unknown"},
            {"brand": "Dior", "price": "4000", "scope_status": "status_pending", "size_label": "unknown"},
        ]

        result = gate_cell(rows, minimum_per_brand=2)

        self.assertFalse(result["headline_eligible"])
        self.assertEqual(result["pairing_status"], "blocked_unknown_size")


if __name__ == "__main__":
    unittest.main()
