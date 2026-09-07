# Chanel 属性配对审计（第 3 步）

- 补充快照：`supplementary_current_2026-09-07`；基线竞品快照：`current_2026-08-15`。
- 属性过滤：同市场、包型、尺寸标签、材质组；不按相似名称模糊配对。
- 结果：15 条方向性候选配对，18 个补充属性单元。
- 所有候选价格比较均为 `not_computed`，因为补充快照与竞品基线日期不同。
- 季节集合、WOC 和未知尺寸均保留为审计状态，不进入主文可比单元。

输出：

- `research_r1/outputs/comparable_pair_candidates.csv`
- `research_r1/outputs/comparable_cells_supplementary.csv`
