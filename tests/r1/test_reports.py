import csv
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
REPORT = ROOT / "research_r1/report"


class ReportContractTest(unittest.TestCase):
    def test_chinese_report_uses_correct_dior_coverage_and_pairing_gate(self):
        text = (REPORT / "REPORT_CN.md").read_text(encoding="utf-8")
        with (ROOT / "research_r1/data/coverage.csv").open(newline="", encoding="utf-8") as handle:
            coverage = list(csv.DictReader(handle))
        dior_us = [
            row for row in coverage
            if row["snapshot_id"] == "current_2026-08-15"
            and row["brand"] == "Dior"
            and row["market"] == "US"
        ]
        numeric = sum(int(row["numeric_observations"]) for row in dior_us)
        accepted = sum(int(row["accepted_observations"]) for row in dior_us)
        with (ROOT / "research_r1/outputs/comparable_pair_candidates.csv").open(newline="", encoding="utf-8") as handle:
            candidate_count = sum(1 for _ in csv.DictReader(handle))
        with (ROOT / "research_r1/outputs/comparable_cells_supplementary.csv").open(newline="", encoding="utf-8") as handle:
            cell_count = sum(1 for _ in csv.DictReader(handle))

        self.assertRegex(text, rf"Dior 美国(?:只有|有) {numeric} 条数值价格")
        self.assertRegex(text, rf"{candidate_count} 条属性匹配的方向性候选配对")
        self.assertRegex(text, rf"{cell_count} 个补充属性单元")
        self.assertIn(f"其余 {accepted - numeric} 条不插补", text)

    def test_english_case_study_exposes_snapshot_limitation(self):
        text = (REPORT / "CASE_STUDY_EN.md").read_text(encoding="utf-8")
        with (ROOT / "research_r1/outputs/comparable_pair_candidates.csv").open(newline="", encoding="utf-8") as handle:
            candidate_count = sum(1 for _ in csv.DictReader(handle))
        self.assertIn(f"{candidate_count} directional peer candidates", text)
        self.assertIn("price comparison is blocked", text)
        self.assertIn("limited", text)

    def test_decision_memo_does_not_recommend_a_price_move(self):
        text = (REPORT / "DECISION_MEMO_CN.md").read_text(encoding="utf-8")
        self.assertIn("日期不一致", text)
        self.assertIn("不据此提出新品价位或涨价方案", text)
        self.assertIn("最多三条", text)

    def test_english_case_study_carries_wave6_gate(self):
        text = (REPORT / "CASE_STUDY_EN.md").read_text(encoding="utf-8")
        with (ROOT / "research_r1/outputs/wave6_same_date_pairing_cells_2026-09-09_us.csv").open(newline="", encoding="utf-8") as handle:
            cells = list(csv.DictReader(handle))
        with (ROOT / "research_r1/outputs/wave6_same_date_hobo_dimension_pairs_2026-09-09_us.csv").open(newline="", encoding="utf-8") as handle:
            dimensions = list(csv.DictReader(handle))
        strict_count = sum(row["main_text_status"] == "main_text_eligible" for row in cells)
        strict_word = "zero" if strict_count == 0 else str(strict_count)
        self.assertIn("Latest independent refresh", text)
        self.assertIn(f"{strict_word} strict main-text cells", text)
        for row in dimensions:
            if row["dimension_match"] == "TRUE":
                size_pair = f"{row['chanel_size_label'].title()} and {row['peer_size_label'].upper()}"
                self.assertIn(size_pair, text)


if __name__ == "__main__":
    unittest.main()
