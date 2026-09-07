# Luxury Handbag Research Upgrade R1 Handoff

执行范围：只执行 `Luxury_Handbag_Flagship_Upgrade_and_Phase3_Plan.md` 的 Luxury Handbag 研究仓库 R0–R5。Portfolio 网站 P1–P5 被识别为另一个项目，未执行。

## 基线与环境

- 仓库：`gabriel232ch/luxury-handbag-price-architecture`
- 基线提交：`5ef2ee7e22e4010d7b951ec09df3e5337ee8e56f`
- 当前 checkout：`codex/luxury-handbag-r1`。R1 已提交；`origin/main` 未被修改或推送。
- 原复现链五条命令均返回 0。竞品构建脚本使用执行日时钟生成 `observed_at`，重跑产生的派生变化已恢复；R1 使用保留的 2026-08-15 快照。

## 实际命令与结果

```text
python3 build_competitor_dataset.py       -> exit 0; 120 competitor rows; 12 errors
python3 competitive_pricing_calculations.py -> exit 0; 161 observations; 147 numeric
python3 build_historical_dataset.py       -> exit 0; 77 rows; 76 numeric; 35 events
python3 historical_pricing_calculations.py -> exit 0; 19 market paths; 13 lineages
python3 build_final_report_assets.py      -> exit 0; 5 SVG assets
python3 scripts/r1/build.py               -> exit 0; current 161/147, history 77/76
python3 scripts/r1/validate.py            -> exit 0; status limited; 0 errors; 9 critical unresolved
python3 scripts/r1/export_case_study.py  -> exit 0; 4 claims; 3 static scenes; 210 sources
python3 -m unittest discover -s tests/r1 -p 'test_*.py' -> 13 tests, 0 failures
python3 -m compileall -q scripts/r1 tests/r1 -> exit 0
git diff --check -> exit 0
```

## 研究产物

- `research_r1/data/observations.csv`：238 条 canonical rows，区分 `current_2026-08-15` 与 `historical_panel_2026-08-15`。
- `research_r1/source_registry.csv`：210 条来源登记；当前官方来源与历史二手来源分开。
- `research_r1/data/coverage.csv`：品牌 × 市场 × 家族接受数、数值数、货号数、去变体组数、询价/未解析数。
- `research_r1/outputs/`：M1 家族分布、M2 Chanel 梯度、M3 价格带敏感性、M4 有边界可比单元、M5 对齐历史与稳健性，以及 unresolved/validation。
- `research_r1/report/REPORT_CN.md`、`CASE_STUDY_EN.md`、`DECISION_MEMO_CN.md`：同一计算口径的研究叙事与决策备忘录。
- `research_r1/export/case-study.json`、`manifest.json`、`scenes/`、`figures/`：候选静态案例包；publication 保持 `candidate`，不提前发布。

## 核心结果变化

1. 当前 2026-08-15 样本为 161 条观察、147 条数值价格；Dior 美国 20 条中仅 13 条可解析价格（65.0%），不做插补。
2. Chanel 同市场/同快照的 Classic（Classic 11.12 + Small Classic）与进入/其他核心（Mini Classic + Shopping Bag + Bowling Bag）观察间隔：法国 3,300 EUR，美国 3,600 USD；中位数距离分别为 4,700 EUR 与 5,200 USD。去变体敏感性中方向保持。
3. Chanel 法国固定产品线的共同观察年份为 2022、2023、2024、2026；组间中位数绝对距离由 4,470 EUR 变为 5,350 EUR。该结果是产品线级、主要基于二手历史表，不是完整官方调价日历。
4. Hermès Geta 法国 2023 的 EUR 4,550 与 EUR 5,550 均保留，作为冲突分支排除出主历史路径。Hermès 当前 40 条观察没有供应商 signature flag，不做同口径图标溢价比较。

## 门槛与下一步

R1 可复算门通过，研究状态为 `limited`，不是“旗舰研究完成”。最小下一步是：补齐 Dior 未解析价格的直接证据；核实 Hermès Geta 冲突；若需要历史决策，再补同款参考号、共同日期和一手历史价格来源。未执行新的全市场刷新、消费者/销售数据采购或网站实现。

## 第 1 步：采样框与基线审计（已完成）

- `research_r1/sampling_plan.md`：定义核心/扩展范围、合格采样单位、状态字典、试采停止规则和 QA 指标。
- `research_r1/feasibility_matrix.csv`：按品牌 × 市场记录当前观察家族、数值覆盖、未解析机制和下一次试采动作；Chanel 2.55、Boy、19、22、25、WOC 作为待验证候选，不被写成已完成覆盖。
- `research_r1/baseline_audit.md`：把旧报告结论逐条映射到 R1 证据，明确保留、收窄和暂不进入主文的结论。

本步没有新增网页采集、没有修改价格/历史计算，也没有把任何 Portfolio 内容带入研究仓库。下一步只有在审阅本步文件后，才进入 `product_master`、`sku_mapping` 和 Chanel 定向补充。
