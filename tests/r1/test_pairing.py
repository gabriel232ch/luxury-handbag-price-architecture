import csv
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
R1 = ROOT / "research_r1"


def rows(path: pathlib.Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class PairingAuditTest(unittest.TestCase):
    def test_attribute_filtered_pair_candidates_are_snapshot_blocked(self):
        candidates = rows(R1 / "outputs/comparable_pair_candidates.csv")
        self.assertEqual(len(candidates), 15)
        self.assertTrue(candidates)
        for row in candidates:
            self.assertEqual(row["attribute_match"], "exact_group")
            self.assertEqual(row["pairing_status"], "blocked_cross_snapshot")
            self.assertEqual(row["supplement_snapshot_id"], "supplementary_current_2026-09-07")
            self.assertEqual(row["peer_snapshot_id"], "current_2026-08-15")
            self.assertEqual(row["price_comparison_status"], "not_computed")
            self.assertEqual(row["supplement_currency"], row["peer_currency"])

    def test_pairing_cells_keep_exclusions_and_unknown_size_out_of_main(self):
        cells = rows(R1 / "outputs/comparable_cells_supplementary.csv")
        self.assertEqual(len(cells), 18)
        self.assertTrue(all(row["headline_eligible"] == "FALSE" for row in cells))
        self.assertTrue(any(row["gate_reason"] == "unknown_size" for row in cells))
        self.assertTrue(any(row["gate_reason"] == "seasonal_excluded" for row in cells))
        self.assertTrue(any(row["gate_reason"] == "woc_sensitivity_only" for row in cells))
        self.assertTrue(all(row["price_comparison_status"] == "not_computed" for row in cells))


if __name__ == "__main__":
    unittest.main()
