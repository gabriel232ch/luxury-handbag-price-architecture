# Wave 6 四品牌同日配对审计（2026-09-09，美国站）

## 结论

本审计只使用 `wave6_same_date_refresh_2026-09-09_us.csv` 的 8 行；不改写 2026-09-08 或更早面板。共形成 5 个精确市场/包型/尺寸/材质单元和 2 条 Chanel-竞品候选配对。
属性单元状态计数：`{'blocked_unknown_size': 1, 'blocked_no_chanel_subject': 3, 'blocked_seasonal_excluded': 1}`；严格主文状态计数：`{'blocked_unknown_size;blocked_independent_family_sample': 1, 'blocked_no_chanel_subject;blocked_independent_family_sample': 3, 'blocked_seasonal_excluded;blocked_independent_family_sample': 1}`。通过所有主文门槛的单元为 0 个。
在 hobo + leather 路线的 Chanel-to-peer 逐对尺寸检查中，1 个组合通过排序后三轴 `max(2 cm, 10%)` 容差；没有组合同时通过同尺寸标签、regular/season 状态和独立家族样本门槛。

## 关键单元

`US|hobo|small|leather` 包含 Chanel;Dior，品牌计数为 `Chanel:2;Dior:1`，独立家族计数为 `Chanel:2;Dior:1`，属性状态为 `blocked_seasonal_excluded`，严格状态为 `blocked_seasonal_excluded;blocked_independent_family_sample`。
该单元中的 Dior Toujours 行带有明确 Autumn-Winter 2026-2027 标记，已按季节款隔离；即使移除该行，Chanel 也没有同日同尺寸的第二品牌样本。

## 逐对解释

- Hermès Videpoches 只有 crossbody/unknown-size 行，因此不进入 hobo 单元，也不与 Chanel hobo 强行配对。
- Louis Vuitton 本轮是 PM/MM 尺寸，而 Chanel 行是 Small；虽然同为 hobo + leather，但严格同尺寸门槛不通过。
- Dior Bobby 是 Medium；Dior Toujours Small 是明确季节款。Dior Bobby 与 Chanel 没有同尺寸单元。
- 所有 Chanel、Louis Vuitton 和 Dior Bobby 行的 regular/season 状态仍为 `not_disclosed`；不能把未披露推断成常规款。
- 主文比较要求每品牌至少 3 个独立家族；本轮任何跨品牌单元也没有达到该门槛，因此不计算价格差、中位数排名或品牌溢价。

## 决定

本轮研究结论是：2026-09-09 快照完成了证据刷新和门槛审计，但没有产生可进入主文的跨品牌比较单元。研究状态继续为 `limited`；这不是抓取失败，而是官方页面当前可验证的包型、尺寸、季节状态和样本门槛未同时满足。

## 输出

- `wave6_same_date_pairing_panel_2026-09-09_us.csv`：8 行同日证据面板。
- `wave6_same_date_pairing_cells_2026-09-09_us.csv`：属性单元、品牌计数、独立家族计数和严格门槛。
- `wave6_same_date_pair_candidates_2026-09-09_us.csv`：Chanel-竞品逐对门控与价格计算状态。
- `wave6_same_date_hobo_dimension_pairs_2026-09-09_us.csv`：hobo + leather 的逐对尺寸检查。
本轮没有产生价格比较结果；这保持了日期、属性和证据门槛的完整性。
