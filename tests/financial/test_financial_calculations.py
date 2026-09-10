import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from financial_performance_calculations import (  # noqa: E402
    index_series,
    margin,
    pct_change,
    ratio,
)


class FinancialCalculationTests(unittest.TestCase):
    def test_margin_is_dimensionally_consistent(self):
        self.assertAlmostEqual(margin(250, 1000), 25.0)
        self.assertIsNone(margin(None, 1000))
        self.assertIsNone(margin(250, 0))

    def test_ratio_returns_percent(self):
        self.assertAlmostEqual(ratio(50, 200), 25.0)
        self.assertIsNone(ratio(None, 200))

    def test_pct_change_does_not_impute_missing_prior(self):
        self.assertAlmostEqual(pct_change(100, 125), 25.0)
        self.assertIsNone(pct_change(None, 125))

    def test_index_series_uses_explicit_base_year(self):
        rows = [
            {"fiscal_year": "2020", "value": "100"},
            {"fiscal_year": "2021", "value": "125"},
        ]
        indexed = index_series(rows, "value", base_year=2020)
        self.assertEqual(indexed[0]["index_value"], 100.0)
        self.assertEqual(indexed[1]["index_value"], 125.0)


if __name__ == "__main__":
    unittest.main()
