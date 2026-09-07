import csv
import json
import pathlib
import unittest
import importlib.util


ROOT = pathlib.Path(__file__).resolve().parents[2]
R1 = ROOT / "research_r1"
validate_spec = importlib.util.spec_from_file_location("r1_validate", ROOT / "scripts/r1/validate.py")
validator = importlib.util.module_from_spec(validate_spec)
validate_spec.loader.exec_module(validator)


def read(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class R1ContractTest(unittest.TestCase):
    def test_observation_schema_and_counts(self):
        rows = read(R1 / "data/observations.csv")
        required = {"observation_id", "snapshot_id", "brand", "market", "currency", "observed_at", "source_effective_date", "source_id", "reference_code", "family", "model", "size_label", "material_group", "color", "price_status", "price", "comparison_group_id", "lineage_id", "inclusion_status", "exclusion_reason"}
        self.assertTrue(required.issubset(rows[0]))
        self.assertEqual(len(rows), 238)
        self.assertEqual(len({row["observation_id"] for row in rows}), len(rows))

    def test_market_currency_and_price_status_contract(self):
        for row in read(R1 / "data/observations.csv"):
            self.assertEqual(row["currency"], {"FR": "EUR", "US": "USD"}[row["market"]])
            if row["price_status"] == "numeric":
                self.assertGreater(float(row["price"]), 0)
            else:
                self.assertEqual(row["price"], "")

    def test_source_lineage_and_claim_references(self):
        rows = read(R1 / "data/observations.csv")
        ids = {row["observation_id"] for row in rows}
        sources = {row["source_id"] for row in read(R1 / "source_registry.csv")}
        lineage_ids = {row["lineage_id"] for row in read(R1 / "data/lineage.csv")}
        self.assertTrue(all(row["source_id"] in sources for row in rows))
        self.assertTrue(all(not row["lineage_id"] or row["lineage_id"] in lineage_ids for row in rows))
        for claim in read(R1 / "claims.csv"):
            self.assertTrue(all(item in ids for item in filter(None, claim["observation_ids"].split(";"))))

    def test_validation_is_limited_without_failure(self):
        validation = json.loads((R1 / "outputs/validation.json").read_text(encoding="utf-8"))
        self.assertIn(validation["status"], {"pass", "limited"})
        self.assertGreaterEqual(validation["unresolved_critical_count"], 1)

    def test_invalid_fixtures_fail_contract(self):
        base = {
            "observation_id": "fixture-1", "snapshot_id": "current_2026-08-15", "brand": "Chanel",
            "market": "FR", "currency": "EUR", "observed_at": "2026-08-15", "source_effective_date": "2026-08-15",
            "source_id": "SRC-OK", "reference_code": "A", "family": "Classic 11.12", "model": "Classic",
            "size_label": "medium", "material_group": "leather", "color": "black", "price_status": "numeric",
            "price": "100", "comparison_group_id": "x", "lineage_id": "", "inclusion_status": "accepted", "exclusion_reason": "",
        }
        duplicate = [dict(base), dict(base)]
        self.assertTrue(any("duplicate" in item for item in validator.observation_contract_errors(duplicate, set())))
        wrong_currency = dict(base, currency="USD")
        self.assertTrue(any("must use EUR" in item for item in validator.observation_contract_errors([wrong_currency], set())))
        por_as_zero = dict(base, price_status="price_upon_request", price="0")
        self.assertTrue(any("non-numeric status" in item for item in validator.observation_contract_errors([por_as_zero], set())))
        orphan_source = dict(base, source_id="SRC-MISSING")
        self.assertTrue(any("orphan source_id" in item for item in validator.observation_contract_errors([orphan_source], set(), {"SRC-OK"})))


if __name__ == "__main__":
    unittest.main()
