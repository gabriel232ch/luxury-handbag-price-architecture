import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
REPORT = ROOT / "research_r1/report"


class ReportContractTest(unittest.TestCase):
    def test_chinese_report_uses_correct_dior_coverage_and_pairing_gate(self):
        text = (REPORT / "REPORT_CN.md").read_text(encoding="utf-8")
        self.assertIn("13 条数值价格", text)
        self.assertNotIn("32 条数值价格", text)
        self.assertIn("15 条属性匹配的方向性候选配对", text)
        self.assertIn("18 个补充属性单元", text)

    def test_english_case_study_exposes_snapshot_limitation(self):
        text = (REPORT / "CASE_STUDY_EN.md").read_text(encoding="utf-8")
        self.assertIn("15 directional peer candidates", text)
        self.assertIn("price comparison is blocked", text)
        self.assertIn("limited", text)

    def test_decision_memo_does_not_recommend_a_price_move(self):
        text = (REPORT / "DECISION_MEMO_CN.md").read_text(encoding="utf-8")
        self.assertIn("日期不一致", text)
        self.assertIn("不据此提出新品价位或涨价方案", text)
        self.assertIn("最多三条", text)

    def test_english_case_study_carries_wave6_gate(self):
        text = (REPORT / "CASE_STUDY_EN.md").read_text(encoding="utf-8")
        self.assertIn("Latest independent refresh", text)
        self.assertIn("zero strict main-text cells", text)
        self.assertIn("Small and PM", text)


if __name__ == "__main__":
    unittest.main()
