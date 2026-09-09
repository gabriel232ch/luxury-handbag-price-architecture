# Wave 4 hobo + leather 尺寸审计（2026-09-08，美国站）

## 审计结论

合并 Wave 3 和 Wave 4 后，`US|hobo|leather` 包含 Chanel 3 个配置、Louis Vuitton 4 个配置，共 12 个成对组合。
按数值尺寸排序后三轴容差审计，方向性尺寸候选为 1 个；满足主文全部门槛的单元为 0 个。
正式样本门槛要求每边至少 3 个独立家族；本轮核心计数为 Chanel 2、Louis Vuitton 2。

尺寸容差为 `max(2 cm, 10% × 两边较大值)`，只用于识别量级接近，不把品牌 PM/MM/small 标签直接互换。

## 唯一方向性尺寸候选

| Chanel | Louis Vuitton | Chanel 尺寸签名 cm | LV 尺寸签名 cm | 轴差 cm | 阻断原因 |
|---|---|---:|---:|---:|---|
| AS5293-B20304-94305 (CHANEL 25) | M2A323 (Hobo) | 30 x 25.9 x 14 cm | 27.9 x 23.9 x 16 cm | 2.1 x 2 x 2 cm | blocked_regular_special_undisclosed;blocked_sample_insufficient |

## 阻断解释

- AS5293（CHANEL 25 Small）与 M2A323（Low Key Hobo PM）仍是唯一通过三轴数值尺寸容差的组合。
- 该组合的核心独立家族数为 Chanel 2、Louis Vuitton 2，均低于 3；两边常规/季节状态仍为 `not_disclosed`。
- 新增 Chanel AS6617 是明确 Fall Winter 2026 Pre-Collection，继续季节隔离；新增 LV Loop Hobo 和 Hobo Métis 没有命名尺寸，继续未知尺寸隔离。
- 新增 LV Coussin Hobo MM 有明确 MM 标签，但数值尺寸与 Chanel 22/25 不在容差内；因此增加了家族覆盖，却没有形成新的尺寸交集。

## 决策

本轮不升级任何 hobo + leather 单元进入主文比较。新增配置有效扩大了候选池，但没有达到正式样本和状态门槛。

## 输出

- `wave4_hobo_dimension_pairs_2026-09-08_us.csv`：12 个 Chanel–Louis Vuitton hobo 组合的逐对结果。
- 本审计不改写 2026-09-07 主面板，不计算价格差。
