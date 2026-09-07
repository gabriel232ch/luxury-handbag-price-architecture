import csv
import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("r1_build", ROOT / "scripts/r1/build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class MetricFixturesTest(unittest.TestCase):
    def test_linear_quantile_fixture(self):
        self.assertEqual(build.quantile([100, 200, 400, 800], .25), 175)
        self.assertEqual(build.quantile([100, 200, 400, 800], .50), 300)
        self.assertEqual(build.quantile([100, 200, 400, 800], .75), 500)

    def test_gap_ratio_and_overlap_are_not_clipped(self):
        self.assertEqual(min([500, 600]) - max([100, 200]), 300)
        self.assertAlmostEqual(550 / 150, 3.6666666667)
        self.assertEqual(min([500, 700]) - max([100, 600]), -100)

    def test_price_status_and_market_rules(self):
        self.assertIsNone(build.parse_price("POR"))
        self.assertEqual(build.normal_market("France"), "FR")
        self.assertEqual(build.normal_market("United States"), "US")
        self.assertEqual(build.material_group("Calfskin and silk"), "leather_and_textile")

    def test_bin_boundary_is_upper_exclusive(self):
        edges = [100, 200]
        self.assertEqual(build.band_for(99.99, edges), 0)
        self.assertEqual(build.band_for(100, edges), 1)
        self.assertEqual(build.band_for(200, edges), 2)

    def test_aligned_history_uses_intersection(self):
        rows = [
            {"snapshot_id": build.HISTORY_SNAPSHOT, "brand": "Chanel", "market": "FR", "price_status": "numeric", "inclusion_status": "accepted", "observed_at": "2022", "lineage_id": "CH-C01", "price": "100"},
            {"snapshot_id": build.HISTORY_SNAPSHOT, "brand": "Chanel", "market": "FR", "price_status": "numeric", "inclusion_status": "accepted", "observed_at": "2024", "lineage_id": "CH-C01", "price": "120"},
            {"snapshot_id": build.HISTORY_SNAPSHOT, "brand": "Chanel", "market": "FR", "price_status": "numeric", "inclusion_status": "accepted", "observed_at": "2024", "lineage_id": "CH-C03", "price": "60"},
        ]
        output = build.build_aligned_history(rows, {})
        self.assertEqual([row["observed_year"] for row in output], ["2024"])


if __name__ == "__main__":
    unittest.main()
