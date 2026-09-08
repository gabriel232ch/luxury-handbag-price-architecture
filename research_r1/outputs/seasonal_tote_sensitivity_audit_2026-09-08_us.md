# 季节款 Tote 敏感性路线门槛审计（美国站）

本审计只检查独立季节路线，不改写常规核心主面板。数值中位数保留为描述性上下文；只有样本量、属性和常规/季节状态门槛同时通过，才允许计算跨品牌价格差。

## 审计结果

| 快照日期 | Chanel 配置 | Dior 配置 | Chanel 中位数 | Dior 中位数 | 样本门槛 | 状态门槛 | 价格比较 | 发布决定 |
|---|---:|---:|---:|---:|---|---|---|---|
| 2026-09-07 / small | 2 | 5 | 6600 | 4000 | blocked | blocked | `not_computed` | `sensitivity_context_only` |
| 2026-09-08 / small | 3 | 3 | 6700 | 3900 | pass | blocked | `not_computed` | `sensitivity_context_only` |
| 2026-09-08 / mini | 1 | 0 | 5400 | — | blocked | blocked | `not_computed` | `excluded_size_mismatch` |

## 阻断原因

- 2026-09-07：Chanel 只有 2 个季节小号 Tote，低于每个比较角色至少 3 个独立配置；Dior 的 5 条上下文记录均为 `not_disclosed`，不能确认是季节款。
- 2026-09-08：Chanel 与 Dior 均已达到 3 个独立配置的样本门槛，但 Dior 的常规/季节状态仍为 `not_disclosed`，因此状态门槛未通过。
- Mini 行单独隔离，不与 small Tote 配对。

## 结论

本轮没有任何可发布的季节对季节价格差。2026-09-08 的样本量门槛已达到，但 Dior 状态门槛仍未通过；当前输出只能作为敏感性路线的描述性背景。

来源数据：[seasonal_tote_sensitivity_2026-09-08_us.csv](../data/seasonal_tote_sensitivity_2026-09-08_us.csv)。
