import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from price_architecture_diagnostics import (  # noqa: E402
    adjacent_steps,
    family_step_rows,
    summarize_visibility,
    tier_for_price,
)


class PriceArchitectureDiagnosticTests(unittest.TestCase):
    def test_adjacent_steps_preserve_duplicate_price_points(self):
        rows = adjacent_steps([100, 150, 150, 300])
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[1]["absolute_step"], 0.0)
        self.assertEqual(rows[2]["absolute_step"], 150.0)

    def test_visibility_separates_numeric_from_non_numeric(self):
        result = summarize_visibility([{"price": 100}, {"price": None}, {"price": 200}])
        self.assertEqual(result["total_observations"], 3)
        self.assertEqual(result["numeric_observations"], 2)
        self.assertEqual(result["non_numeric_or_por_observations"], 1)

    def test_tier_rule_uses_existing_market_boundaries(self):
        self.assertEqual(tier_for_price("FR", 4_850), "core")
        self.assertEqual(tier_for_price("FR", 10_000), "icon")
        self.assertEqual(tier_for_price("US", 7_400), "premium")
        self.assertEqual(tier_for_price("US", 11_000), "icon")

    def test_family_steps_are_sorted_by_observed_median(self):
        rows = [
            {"product_family": "Icon", "median": 1000},
            {"product_family": "Entry", "median": 400},
            {"product_family": "Core", "median": 700},
        ]
        steps = family_step_rows(rows)
        self.assertEqual([(r["lower_family"], r["upper_family"]) for r in steps], [
            ("Entry", "Core"),
            ("Core", "Icon"),
        ])
        self.assertEqual(steps[-1]["absolute_step"], 300.0)


if __name__ == "__main__":
    unittest.main()
