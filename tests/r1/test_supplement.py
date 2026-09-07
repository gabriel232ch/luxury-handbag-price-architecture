import csv
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
R1 = ROOT / "research_r1"


def rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class SupplementContractTests(unittest.TestCase):
    def test_product_master_has_unique_candidate_references(self):
        master = rows(R1 / "data" / "product_master.csv")
        self.assertEqual(len(master), 11)
        self.assertEqual(len({row["product_id"] for row in master}), 11)
        self.assertEqual({row["family"] for row in master}, {"2.55", "Boy", "Chanel 19", "Chanel 22", "Chanel 25", "WOC"})
        self.assertTrue(all(row["source_url_fr"].startswith("https://www.chanel.com/") for row in master))
        self.assertTrue(all(row["source_url_us"].startswith("https://www.chanel.com/") for row in master))

    def test_sku_mapping_is_exact_cross_market(self):
        mapping = rows(R1 / "data" / "sku_mapping.csv")
        self.assertEqual(len(mapping), 11)
        self.assertTrue(all(row["reference_match"] == "exact" for row in mapping))
        self.assertTrue(all(row["market_pair_status"] == "exact_cross_market_pair" for row in mapping))
        self.assertTrue(all(row["mapping_confidence"] == "HIGH" for row in mapping))

    def test_supplementary_observations_are_separate_and_numeric(self):
        observations = rows(R1 / "data" / "supplementary_current.csv")
        self.assertEqual(len(observations), 22)
        self.assertEqual({row["snapshot_id"] for row in observations}, {"supplementary_current_2026-09-07"})
        self.assertEqual(sum(row["price_status"] == "numeric" for row in observations), 22)
        self.assertEqual(sum(row["market"] == "FR" for row in observations), 11)
        self.assertEqual(sum(row["market"] == "US" for row in observations), 11)
        self.assertEqual(sum(row["inclusion_status"] == "sensitivity_only" for row in observations), 2)
        self.assertEqual(sum(row["inclusion_status"] == "accepted_supplementary_seasonal" for row in observations), 4)

    def test_raw_rows_and_sources_cover_each_observation(self):
        raw = [json.loads(line) for line in (R1 / "data" / "supplementary_current_raw.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        observations = rows(R1 / "data" / "supplementary_current.csv")
        source_rows = rows(R1 / "source_registry.csv")
        source_ids = {row["source_id"] for row in source_rows}
        self.assertEqual(len(raw), 22)
        self.assertEqual({row["record_id"] for row in raw}, {row["observation_id"] for row in observations})
        self.assertTrue(all(row["extraction_method"] == "manual_official_search_result" for row in raw))
        self.assertTrue(all(row["source_id"] in source_ids for row in observations))


if __name__ == "__main__":
    unittest.main()
