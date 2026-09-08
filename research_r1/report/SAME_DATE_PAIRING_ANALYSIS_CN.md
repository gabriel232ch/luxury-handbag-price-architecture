# 2026-09-07 美国站同日跨品牌配对分析附录

**研究对象：**Chanel、Hermès、Louis Vuitton、Dior 的官方美国站公开标价观察

**主审计日期：**2026-09-07

**用途：**解释同日属性配对审计结果，并把明确季节款保留在独立敏感性路线；本附录不覆盖原有 R1 主报告，也不把季节款价格差当作常规核心结论。

## 结论先行

重新核实 Chanel 官方分类页和详情页后，原 `tote / small / leather` 单元中的两条 Chanel AS6495 记录被确认属于 Fall Winter 2026 Pre-Collection。[Chanel 分类页](https://www.chanel.com/us/fashion/handbags/c/1x1x1/)、[AS6495 官方页](https://www.chanel.com/us/fashion/p/AS6495B25347UA954/small-shopping-bag-lambskin-gold-tone-metal/)

因此，2026-09-07 同日审计当前没有通过常规核心主文门槛的跨品牌单元。原单元仍保留 2 条 Chanel 和 5 条 Dior 的数值价格，但状态已经改为：

- `headline_eligible=FALSE`
- `pairing_status=blocked_seasonal_excluded`
- `price_comparison_status=not_computed`

Chanel 6,600 USD 与 Dior 4,000 USD 的中位数仍作为记录中的描述性字段保留，但不再计算或报告为常规核心品牌价格差。

## 口径与门槛

本附录使用 [同日面板](../outputs/same_date_pairing_panel_2026-09-07_us.csv) 的 81 行观察。主审计行均为美国市场、2026-09-07 有效日期和数值价格；货币统一为 USD，不做汇率、税费或落地成本调整。

常规核心候选单元必须同时满足：

1. 同市场、同有效日期、同包型、同尺寸标签、同材质组；
2. 至少包含 Chanel 与另一个品牌；
3. 每个品牌至少 2 条数值观察；
4. 显式季节款、WOC/小皮具、未知尺寸、未知包型或未知材质不进入主文候选。

`regular_special=not_disclosed` 不被猜成常规款；如果其他门槛通过，只能标为条件性候选。已确认的季节款直接进入季节敏感性路线。

## 常规核心审计结果

| 市场/日期 | 属性单元 | 品牌样本 | 原始中位数记录 | 当前状态 | 价格比较 |
|---|---|---|---|---|---|
| US / 2026-09-07 | tote / small / leather | Chanel（2）；Dior（5） | Chanel 6,600 USD；Dior 4,000 USD | `blocked_seasonal_excluded` | 不计算 |

该单元的阻断来自 Chanel 两条 AS6495 记录的明确季节标签，而不是价格缺失或样本数量不足。逐行候选仍用于追溯，但所有候选的 `price_comparison_status` 均为 `not_computed`。

## 季节款敏感性路线

季节路线与常规核心主文分开保存，见 [季节敏感性路线说明](../data/seasonal_tote_sensitivity_2026-09-08_us.md) 和 [逐条数据](../data/seasonal_tote_sensitivity_2026-09-08_us.csv)。当前只做描述性记录，不计算跨品牌价格差：

| 快照日期 | Chanel 季节小号 Tote | Dior 上下文 | 阻断原因 |
|---|---:|---:|---|
| 2026-09-07 | 2；中位数 6,600 USD | 5；中位数 4,000 USD | Dior 常规/季节状态未披露，不能构成清晰的季节对季节比较 |
| 2026-09-08 | 3；中位数 6,700 USD | 3；中位数 3,900 USD | 双方样本量已达到 3 个独立配置，但 Dior 常规/季节状态仍未披露 |

`AS6248` 是 Spring Summer 2026 的 Mini Shopping Bag，继续作为尺寸不匹配的季节上下文隔离，不进入小号 Tote 路线。WOC、未知尺寸和未知包型继续沿用各自的敏感性或阻断状态。

## 其他品牌的阻断情况

Hermès 和 Louis Vuitton 已进入 2026-09-07 同日面板，但没有与 Chanel 同时满足完整属性和样本要求的常规核心单元。阻断情况按属性单元计数如下：

| 审计状态 | 单元数 | 含义 |
|---|---:|---|
| `blocked_no_chanel_subject` | 25 | 只有竞品或没有 Chanel，不作为本项目主对象的主文比较 |
| `blocked_unknown_size` | 11 | 尺寸标签缺失，不能声称同尺寸 |
| `blocked_unknown_bag_type` | 3 | 包型无法从当前页面信息稳定核实 |
| `blocked_no_cross_brand_peer` | 2 | Chanel 单独形成单元，没有第二品牌共享全部属性 |
| `blocked_sample_insufficient` | 2 | 有跨品牌交集，但至少一个品牌只有 1 条数值观察 |
| `blocked_woc_sensitivity_only` | 1 | WOC/小皮具只保留为敏感性观察 |
| `blocked_seasonal_excluded` | 1 | 明确季节款，移出常规核心并保留在敏感性路线 |

## 分析含义

当前证据支持的结论是：在严格常规核心口径下，2026-09-07 美国站没有可报告的 Chanel 跨品牌价格差单元。季节路线显示了可供后续研究的价格背景，但不能解释为 Chanel 对 Dior 的常规溢价，也不能扩展为全品类价格排名、需求或替代关系。

下一阶段需要取得更多同日期、同包型、同尺寸、同材质的独立配置，并明确常规/季节状态。只有当每个比较角色至少达到 3 个独立配置、状态口径清晰且属性可复核时，才考虑发布季节敏感性统计。

## 校验与复现

- [同日审计说明](../outputs/same_date_pairing_audit_2026-09-07_us.md)
- [属性单元结果](../outputs/same_date_pairing_cells_2026-09-07_us.csv)
- [逐行候选配对](../outputs/same_date_pair_candidates_2026-09-07_us.csv)
- [季节覆盖规则](../data/seasonal_tote_attribute_overrides_2026-09-07_us.csv)
- [季节路线门槛审计](../outputs/seasonal_tote_sensitivity_audit_2026-09-08_us.md)
- [审计脚本](../../scripts/r1/build_same_date_pairing_audit.py)

已重新计算并核对：面板 81 行，品牌计数为 Chanel 20、Hermès 21、Louis Vuitton 20、Dior 20；属性单元 45 个；候选配对 17 条；常规核心通过门槛的单元 0 个。原始价格和季节记录仍可从面板与敏感性路线复现。
