# 基线结论逐条审计（第 1 步）

本表把旧报告的结论拆成可保留、需收窄、待验证的单元。审计对象是已有公开标价研究，不把附件中的 Portfolio 网站任务带入本项目。`R1` 的“limited”状态仍然有效；本步只建立审计和下一轮取样框，不修改价格或历史计算。

旧结论的原文入口为 `FINAL_LUXURY_HANDBAG_PRICING_STRATEGY_CN.md` 的执行摘要、当前价格架构、历史路径、四品牌比较和结论段，以及 `FINAL_REPORT_APPENDIX_CN.md` 的覆盖、方向性可比单元和历史路径段。下表的 ID 是后续修订时的稳定引用，不代表新的统计结论。

## 审计规则

- `retain_with_scope`：证据与定义仍支持，但必须保留市场、快照、样本和不确定性边界。
- `narrow`：方向可以保留，原来过宽的全局或替代含义要收窄。
- `pending`：需要产品主数据、定向补充或配对证据后再决定。
- `exclude_from_headline`：可以留在附录或问题清单，不能作为主文核心发现。
- `guardrail`：这是研究边界或方法约束，不是商业结果。

## 逐条映射

| ID | 旧报告结论 | R1 当前证据 | 状态 | 缺口/反证 | 本轮动作 |
|---|---|---|---|---|---|
| BASE-01 | Chanel 的差异体现为较高进入门槛、Classic 高位锚点和两个可见价格集群。 | `outputs/chanel_ladder.csv`：FR 观察间隔 3,300 EUR、US 3,600 USD；Classic/进入核心中位数比约 1.81×/1.80×。 | retain_with_scope | 只有现有观察家族；2.55、Boy、19、22、25、WOC 尚未进入当前框。间隔可能因补充而变化。 | 保留为“当前已观察样本”结论；下一步定向补充后重算。 |
| BASE-02 | Chanel 不是所有产品都更贵，而是价格架构与水平共同形成差异。 | `outputs/brand_family_summary.csv` 与 `outputs/chanel_ladder.csv` 支持同市场分层；询价未被估值。 | retain_with_scope | 未建立统一用途、材质、常规/特殊分类，不能把家族层级当作可比替代。 | 在产品主数据中补齐属性，再决定能否保留更强措辞。 |
| BASE-03 | 竞争关系随价格层变化：低层更接近 LV，核心层 Dior/LV，高端层 Chanel/Hermès。 | 价格带和 7 个 `comparable_cells.csv` 单元提供方向性提示。 | narrow | 7 个 R1 可比单元全部 `headline_eligible=FALSE`；没有一对一或成组的合格竞品配对。 | 只保留为“采样价格层的方向性地图”；主文等待 `comparable_pairs`。 |
| BASE-04 | 法国 `tote/large/leather` 等单元中 Chanel 与 Hermès 接近、明显高于 Dior/LV。 | 旧附录中的单元仍可在当前数据重算，但部分品牌 N=1–2；R1 将其全部列为 `appendix_only`。 | exclude_from_headline | 宽口径包型、尺寸和材质不能代替相同用途/规格/版本；不满足正式跨品牌比较门槛。 | 保留审计链和附录；下一轮只验证实际产品对。 |
| BASE-05 | 2022–2026 Chanel 法国对齐产品线中，Classic 和 Mini/进入组都上移，绝对价差扩大。 | `outputs/aligned_history.csv`：共同年份 2022/23/24/26，绝对价差 4,470→5,350 EUR；`claims.csv` 已限定为选定产品线。 | retain_with_scope | 历史主要为二手价格表；是产品线级，不是全 Chanel 或美国历史；没有跨品牌固定篮子。 | 保留为 Chanel 法国选定产品线结论；不扩展为同行涨价排名。 |
| BASE-06 | 四品牌有不同当前架构和历史路径，LV 较低、Dior 核心、Hermès 宽、Chanel 高位锚点。 | 当前家族摘要和历史 lineage 支持描述性差异；Dior US 仅 65% 数值，Hermès 无同口径 signature flag。 | narrow | 家族用途尚未统一；历史连续性不对称，Dior 多为 successor；观察数不是销量或全量组合权重。 | 可作为假设与取样角色，不作为完整品牌战略画像。 |
| BASE-07 | 当前价格带的 0 代表未捕获，不代表品牌没有产品；Chanel POR 和 Dior US 未解析必须分开处理。 | `data/coverage.csv` 和 `outputs/unresolved.csv` 明确记录：Chanel FR/US 各 3 条 POR；Dior US 7 条未解析。 | retain_with_scope | 当前覆盖仍是接受观察覆盖，不是官网 assortment coverage；缺失机制具有品牌/地区选择性。 | 作为采样与 QA 规则写入 `sampling_plan.md`，不做插补。 |
| BASE-08 | Hermès Geta 法国 2023 存在 EUR 4,550 与 EUR 5,550 冲突，不能给出单一确定路径。 | `outputs/unresolved.csv` 两条冲突分支均保留并排除主路径。 | retain_with_scope | 冲突尚未通过更高等级来源解决。 | 继续保留敏感性分支；后续若进入历史决策再单独核实。 |
| BASE-09 | 公开标价可以说明架构位置，但不能推出需求、支付意愿、利润、因果或最优价格。 | `RESEARCH_SPEC.md`、R1 报告和验证规则均保留该边界。 | guardrail | 没有新增反证；数据类型仍是非加权挂牌价。 | 继续作为主文和后续决策卡的硬边界。 |

## 审计后的可用结论层级

当前仍可直接复核的核心是：Chanel 法国/美国现有观察中的 Classic 与进入/核心价格距离，以及 Chanel 法国选定产品线的共同年份路径。四品牌价格层和方向性单元只作为假设和附录证据，直到产品用途、材质、常规/特殊状态和实际产品对完成映射。任何关于“完整组合”“消费者替代”“价格最优”的旧措辞都不应恢复。
