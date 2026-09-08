# 2026-09-07 美国站同日跨品牌配对审计

- 输入：`live_refresh_2026-09-07_us.csv`（Chanel、Hermès、Louis Vuitton、Dior，共 81 行）和竞品产品主数据。
- 同日门槛：`market=US`、`source_effective_date=2026-09-07`。
- 严格属性门槛：同市场、同日期、同包型、同尺寸、同材质；显式季节款、WOC/小皮具和未知尺寸单独隔离。
- 样本门槛：每个品牌在单元内至少 2 条数值观察，且至少包含 Chanel 与另一个品牌。
- `regular_special=not_disclosed` 不被猜成常规款；若其他门槛通过，单元可作为条件性主文候选，并在限制列保留该缺口。已核实的季节覆盖写入 `seasonal_tote_attribute_overrides_2026-09-07_us.csv`，明确季节款不进入常规核心。

结果：共 45 个属性单元，17 条 Chanel-竞品候选配对，0 个单元通过主文门槛。

配对状态计数：`{'blocked_unknown_size': 11, 'blocked_no_chanel_subject': 25, 'blocked_no_cross_brand_peer': 2, 'blocked_sample_insufficient': 2, 'blocked_woc_sensitivity_only': 1, 'blocked_seasonal_excluded': 1, 'blocked_unknown_bag_type': 3}`。

输出：

- `same_date_pairing_panel_2026-09-07_us.csv`：用于审计的 81 行同日面板及归类字段，其中两条 AS6495 已标记为季节款。
- `same_date_pairing_cells_2026-09-07_us.csv`：单元级门槛和品牌中位数。
- `same_date_pair_candidates_2026-09-07_us.csv`：Chanel 与竞品的逐行候选配对。

本步骤只完成同日配对审计和可比单元筛选；既有 R1 报告和历史基线输出未被重写。
