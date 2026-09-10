import csv
import json
import copy
import importlib.util
import pathlib
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
EXPORT = ROOT / "research_r1/export"


def load_export_module():
    spec = importlib.util.spec_from_file_location("export_case_study", ROOT / "scripts/r1/export_case_study.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ExportContractTest(unittest.TestCase):
    def current_dior_counts(self):
        with (ROOT / "research_r1/data/observations.csv").open(newline="", encoding="utf-8") as handle:
            rows = [
                row for row in csv.DictReader(handle)
                if row["snapshot_id"] == "current_2026-08-15"
                and row["brand"] == "Dior"
                and row["market"] == "US"
            ]
        return sum(row["price_status"] == "numeric" for row in rows), len(rows)

    def test_case_study_has_six_sections_three_scenes_and_candidate_status(self):
        case = json.loads((EXPORT / "case-study.json").read_text(encoding="utf-8"))
        self.assertEqual(case["publication"], "candidate")
        self.assertTrue(case["noindex"])
        self.assertEqual(len(case["sections"]), 6)
        self.assertEqual(len(case["scenes"]), 3)
        claim_ids = {claim["claimId"] for claim in case["claims"]}
        scene_ids = {scene["id"] for scene in case["scenes"]}
        for section in case["sections"]:
            self.assertTrue(set(section["claimIds"]).issubset(claim_ids))
            self.assertTrue(set(section["sceneIds"]).issubset(scene_ids))

    def test_case_study_carries_report_boundaries_into_export(self):
        case = json.loads((EXPORT / "case-study.json").read_text(encoding="utf-8"))
        scope = case["observationScope"]
        self.assertEqual(scope["currentSnapshot"], "2026-08-15")
        self.assertIn("supplementary_current_2026-09-07", scope["supplementarySnapshots"])
        with (ROOT / "research_r1/outputs/comparable_pair_candidates.csv").open(newline="", encoding="utf-8") as handle:
            candidate_count = sum(1 for _ in csv.DictReader(handle))
        with (ROOT / "research_r1/outputs/comparable_cells_supplementary.csv").open(newline="", encoding="utf-8") as handle:
            cell_count = sum(1 for _ in csv.DictReader(handle))
        self.assertEqual(scope["supplementaryPairingAudit"]["candidatePairs"], candidate_count)
        self.assertEqual(scope["supplementaryPairingAudit"]["cells"], cell_count)
        sections = {section["id"]: section for section in case["sections"]}
        numeric, accepted = self.current_dior_counts()
        self.assertIn(f"{numeric} numeric prices among {accepted}", sections["context"]["paragraphs"][0])
        self.assertIn("blocked", sections["interpretation"]["paragraphs"][0])

    def test_case_study_uses_current_dior_coverage_counts(self):
        numeric, accepted = self.current_dior_counts()
        unresolved = accepted - numeric
        case = json.loads((EXPORT / "case-study.json").read_text(encoding="utf-8"))
        context = next(section for section in case["sections"] if section["id"] == "context")["paragraphs"][0]
        self.assertIn(f"{numeric} numeric prices among {accepted}", context)
        self.assertIn(f"{unresolved} unresolved rows remain missing", context)

    def test_case_study_contract_rejects_duplicate_sections_and_missing_scope(self):
        module = load_export_module()
        case = json.loads((EXPORT / "case-study.json").read_text(encoding="utf-8"))
        scenes = {scene["id"]: scene for scene in case["scenes"]}
        source_ids = {source["source_id"] for source in case["sources"]}
        duplicate = copy.deepcopy(case)
        duplicate["sections"][1]["id"] = duplicate["sections"][0]["id"]
        with self.assertRaises(ValueError):
            module.validate_case_study(duplicate, scenes, source_ids)
        missing_snapshot = copy.deepcopy(case)
        del missing_snapshot["observationScope"]["currentSnapshot"]
        with self.assertRaises(ValueError):
            module.validate_case_study(missing_snapshot, scenes, source_ids)

    def test_static_figures_and_scene_data_exist(self):
        case = json.loads((EXPORT / "case-study.json").read_text(encoding="utf-8"))
        for scene in case["scenes"]:
            self.assertTrue(scene["noJsEquivalent"])
            self.assertTrue(scene["markets"])
            self.assertTrue((ROOT / scene["dataFile"]).exists())
            figure = ROOT / scene["figure"]
            self.assertTrue(figure.exists())
            self.assertIn("<svg", figure.read_text(encoding="utf-8"))

    def test_semantic_case_study_is_stable_across_export(self):
        before = json.loads((EXPORT / "case-study.json").read_text(encoding="utf-8"))
        subprocess.run(["python3", "scripts/r1/export_case_study.py"], cwd=ROOT, check=True, capture_output=True, text=True)
        after = json.loads((EXPORT / "case-study.json").read_text(encoding="utf-8"))
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
