import csv
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
R1 = ROOT / "research_r1"


def read_rows(path: pathlib.Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class Wave6PairingAuditTest(unittest.TestCase):
    def test_wave6_refresh_is_separate_and_complete(self):
        rows = read_rows(R1 / "data/wave6_same_date_refresh_2026-09-09_us.csv")
        self.assertEqual(len(rows), 8)
        self.assertEqual({row["brand"] for row in rows}, {"Chanel", "Hermès", "Louis Vuitton", "Dior"})
        self.assertTrue(all(row["source_effective_date"] == "2026-09-09" for row in rows))

    def test_wave6_audit_keeps_all_price_comparisons_blocked(self):
        cells = read_rows(R1 / "outputs/wave6_same_date_pairing_cells_2026-09-09_us.csv")
        candidates = read_rows(R1 / "outputs/wave6_same_date_pair_candidates_2026-09-09_us.csv")
        self.assertEqual(len(cells), 5)
        self.assertEqual(len(candidates), 2)
        self.assertTrue(all(row["price_comparison_status"] == "not_computed" for row in cells))
        self.assertTrue(all(row["price_comparison_status"] == "not_computed" for row in candidates))
        self.assertTrue(any(row["attribute_gate_status"] == "blocked_seasonal_excluded" for row in cells))
        self.assertTrue(any(row["attribute_gate_status"] == "blocked_unknown_size" for row in cells))

    def test_only_dimension_match_is_not_same_size(self):
        pairs = read_rows(R1 / "outputs/wave6_same_date_hobo_dimension_pairs_2026-09-09_us.csv")
        matches = [row for row in pairs if row["dimension_match"] == "TRUE"]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["same_size_label"], "FALSE")
        self.assertEqual(matches[0]["peer_brand"], "Louis Vuitton")


if __name__ == "__main__":
    unittest.main()
