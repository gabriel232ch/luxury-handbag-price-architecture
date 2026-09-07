import json
import pathlib
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
EXPORT = ROOT / "research_r1/export"


class ExportContractTest(unittest.TestCase):
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

    def test_static_figures_and_scene_data_exist(self):
        case = json.loads((EXPORT / "case-study.json").read_text(encoding="utf-8"))
        for scene in case["scenes"]:
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
