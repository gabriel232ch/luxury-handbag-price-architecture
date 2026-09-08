# Wave 3 尺寸盘点与标准化规则（2026-09-08，美国站）

## 盘点范围

本步检查的是现有 `2026-09-07` 美国同日面板，盘点日期为 `2026-09-08`。它不是新的四品牌快照，也不把旧面板改写成新日期。

| 品牌 | 面板行数 | 有官方数值尺寸 | 只有品牌/产品尺寸标签 | 完全缺尺寸 |
| --- | ---: | ---: | ---: | ---: |
| Chanel | 20 | 0 | 15 | 5 |
| Hermès | 21 | 21 | 0 | 0 |
| Louis Vuitton | 20 | 20 | 0 | 0 |

Chanel 的 15 条 `small/maxi/mini/large` 等标签来自产品名称或分类字段，但没有可见的数值尺寸三元组；Hermès 的 21 条和 Louis Vuitton 的 20 条都有数值尺寸。Louis Vuitton 的 `BB/PM/MM/nano/20` 和 Hermès 的 `18/20/25/29/35/41` 保留为原始品牌标签，不能直接等价为 Chanel 的 `small` 或 `medium`。

## 统一字段

每条新观察必须同时保留：

- `dimensions_raw`：官网原文和原单位；
- `dimensions_cm`：转换后的三元组，保留官网顺序；英寸统一乘以 2.54；
- `dimension_signature_cm`：将三元组从大到小排序后的签名，仅用于跨品牌尺寸量级匹配；
- `dimension_volume_cm3`：三边乘积，仅作诊断和异常检查，不单独决定可比性；
- `dimension_status`：`numeric_official`、`label_only` 或 `unknown`；
- `size_label_raw`：官网/产品名称中的原始标签，不被标准化规则覆盖。

## 初始匹配规则

1. 只有两条记录都为 `numeric_official`，才允许进入跨品牌尺寸候选。
2. 先把三边排序，再逐轴比较；每一轴必须满足绝对差不超过 2 cm 或相对差不超过 10%（取两者中较宽的容差）。
3. 尺寸匹配仍必须同时满足同市场、同日期、同包型和同材质；尺寸相近不能覆盖其他属性缺口。
4. 品牌标签只用于审计展示，禁止执行 `BB=small`、`PM=medium`、`nano=mini` 或 `Hermès 25=Chanel small` 这类固定映射。
5. 若一方缺少数值尺寸，单元标记为 `blocked_until_dimension_capture`；若数值尺寸存在但样本不足，标记为 `blocked_sample_insufficient`。
6. 季节款、WOC/小皮具、未知包型和未知材质继续隔离；尺寸标准化不会改变这些范围规则。

## 当前结论

现有面板无法形成 Chanel–Hermès 或 Chanel–Louis Vuitton 的数值尺寸交集，因为 Chanel 的 20 条美国刷新行全部缺少可见数值尺寸。下一步应在同一个新快照日期先补采 Chanel 的官方数值尺寸，同时刷新 Hermès 和 Louis Vuitton 的对应候选；完成前不升级任何跨品牌尺寸单元。

## 不变更范围

本步只写入盘点和规则文件，不修改 `live_refresh_2026-09-07_us.csv`、`same_date_pairing_panel_2026-09-07_us.csv` 或历史价格分析。
