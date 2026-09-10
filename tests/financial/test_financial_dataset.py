import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from build_financial_dataset import FIELDNAMES, build_panel, normalize_observation  # noqa: E402


def observation(**overrides):
    row = {
        "observation_id": "TEST-001",
        "entity": "Chanel",
        "reporting_scope": "consolidated_company",
        "segment": "",
        "fiscal_year": "2024",
        "period": "FY",
        "metric": "revenue",
        "value": "18699",
        "unit": "USD_m",
        "currency": "USD",
        "reported_or_constant_currency": "reported",
        "source_type": "official_financial_release",
        "source_id": "CH-FY24",
        "source_title": "Chanel FY2024 Financial Results",
        "source_url": "https://example.com/chanel-fy24.pdf",
        "publication_date": "2025-05-20",
        "page_or_section": "p. 4 / highlights table",
        "extraction_note": "Official reported value.",
        "confidence": "high",
        "caveat": "Consolidated company; not handbag-only.",
        "selection_status": "selected",
        "metric_status": "reported",
        "precision_note": "exact",
    }
    row.update(overrides)
    return row


class FinancialDatasetContractTests(unittest.TestCase):
    def test_schema_contains_lineage_and_status_fields(self):
        required = {
            "entity",
            "reporting_scope",
            "fiscal_year",
            "metric",
            "value",
            "unit",
            "currency",
            "source_id",
            "source_url",
            "page_or_section",
            "confidence",
            "caveat",
            "selection_status",
            "metric_status",
        }
        self.assertTrue(required.issubset(set(FIELDNAMES)))

    def test_normalize_preserves_numeric_value_and_scope(self):
        normalized = normalize_observation(observation(value="18,699"))
        self.assertEqual(normalized["value"], "18699")
        self.assertEqual(normalized["reporting_scope"], "consolidated_company")
        self.assertEqual(normalized["selection_status"], "selected")

    def test_conflicting_observations_are_not_silently_overwritten(self):
        first = observation(observation_id="TEST-A", value="100")
        second = observation(observation_id="TEST-B", value="101")
        result = build_panel([first, second])
        self.assertEqual(len(result["panel"]), 2)
        self.assertEqual(len(result["conflicts"]), 1)
        self.assertEqual(result["conflicts"][0]["conflict_type"], "same_key_different_value")

    def test_unavailable_metric_is_retained_as_missingness(self):
        row = observation(
            observation_id="TEST-UNAVAILABLE",
            metric="handbag_revenue",
            value="",
            metric_status="unavailable",
            selection_status="unavailable",
            confidence="na",
            caveat="Not publicly disclosed; not estimable.",
        )
        result = build_panel([row])
        self.assertEqual(len(result["panel"]), 1)
        self.assertEqual(result["panel"][0]["metric_status"], "unavailable")
        self.assertEqual(len(result["missingness"]), 1)


if __name__ == "__main__":
    unittest.main()
