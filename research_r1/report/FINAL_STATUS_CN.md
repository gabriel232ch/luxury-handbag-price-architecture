# Luxury Handbag 研究执行结果（截至 2026-09-09）

## 最终结论

本轮同日刷新和审计已经完成，但没有形成可进入主文的跨品牌价格比较单元。2026-09-09 美国站快照共 8 行，覆盖 Chanel、Hermès、Louis Vuitton 和 Dior；按同市场、同日期、同包型、同尺寸、同材质、数值尺寸和独立家族样本门槛审计后，主文合格单元为 0。研究状态继续为 `limited`，原因是证据门槛未同时满足，而不是采集失败。

原 R1 基线结论保持不变：Chanel 在 2026-08-15 同市场快照中，Classic 与进入/其他核心组之间存在可见价格台阶；这仍是可见标价样本中的描述性观察，不能推出需求、替代、支付意愿或最优价格。

## 本轮数据和审计

| 项目 | 结果 |
|---|---:|
| 同日观察行 | 8 |
| 精确市场/包型/尺寸/材质单元 | 5 |
| Chanel-竞品属性候选 | 2 |
| 严格主文合格单元 | 0 |
| hobo + leather 尺寸逐对检查 | 10 组 |
| 通过三轴 `max(2 cm, 10%)` 尺寸容差 | 1 组 |
| 实际可计算价格比较 | 0 |

唯一通过数值尺寸容差的 hobo 方向是 Chanel AS5293（CHANEL 25 Small）与 Louis Vuitton M25354（Low Key Hobo PM）。它仍然不能进入主文：Chanel 为 `small`、Louis Vuitton 为 `PM`，不是同一命名尺寸；两边 regular/season 状态均未披露；独立家族数也低于每品牌至少 3 个的正式门槛。

## 品牌层面的范围判断

- **Chanel：**AS3260 CHANEL 22 Small 与 AS5293 CHANEL 25 Small 均核验了参考号、价格、皮革材质和数值尺寸，但官方详情页未给出命名的 regular/season 状态。
- **Hermès：**H087987CK10 Videpoches 官方页明确是 Togo calfskin、肩背/斜挎和数值尺寸，但没有命名尺寸，且产品用途是 crossbody。因此它被保留在独立 crossbody 路线，不与 hobo 强行配对。
- **Louis Vuitton：**M25354 Low Key Hobo PM、M47180 CarryAll PM、M12068 Coussin Hobo MM 均具备价格、皮革和数值尺寸，但只有 PM/MM 标签，没有与 Chanel Small 对齐的命名尺寸；页面也没有可核验的命名 regular/season 状态。
- **Dior：**M9319UMOL_M900 Medium Dior Bobby 可在线购买并明确为 hobo、Medium、calfskin；M2867PDUN_M18S Small Dior Toujours 明确属于 Autumn-Winter 2026-2027 Fashion Show，且线上售罄，因此被隔离为季节款。两者都不能与 Chanel Small 形成合格主文单元。

## 为什么没有计算价格差

价格虽然在本轮 8 行中均可读取，但价格可读取不等于可比。严格比较还要求同市场、同日期、同包型、同尺寸、同材质、数值尺寸接近、regular/season 状态可核验，以及足够的独立家族样本。当前没有任何单元同时满足这些条件，因此没有计算中位数差、品牌排名或所谓溢价。

## 项目交付状态

研究执行链已完成：基线、Chanel 定向补充、竞品产品主数据、同日刷新、属性/尺寸门控、敏感性隔离、报告和 GitHub 提交均有独立文件与来源。下一轮若要把状态从 `limited` 提升，必须重新采集同一日期的至少 3 个独立 Chanel hobo 家族和至少 3 个独立竞品同尺寸 hobo 家族，并让 regular/season 状态和数值尺寸同时可核验；不应通过放宽尺寸或季节门槛来制造比较单元。

## 可复核文件

- [2026-09-09 四品牌快照](../data/wave6_same_date_refresh_2026-09-09_us.csv)
- [2026-09-09 快照说明](../data/wave6_same_date_refresh_2026-09-09_us.md)
- [同日配对审计](../outputs/wave6_same_date_pairing_audit_2026-09-09_us.md)
- [属性单元结果](../outputs/wave6_same_date_pairing_cells_2026-09-09_us.csv)
- [逐对候选](../outputs/wave6_same_date_pair_candidates_2026-09-09_us.csv)
- [hobo 尺寸逐对结果](../outputs/wave6_same_date_hobo_dimension_pairs_2026-09-09_us.csv)
