# Wave 3 尺寸交集审计（2026-09-08，美国站）

## 审计结论

本次只使用三份 2026-09-08 美国站刷新文件：Chanel 5 行、Hermès/Louis Vuitton 6 行，共形成 30 个 Chanel-to-peer 组合。所有输入行都有数值价格和三边尺寸。
同包型且同材质的属性候选为 4 个；其中通过排序后三轴尺寸容差的只有 1 个。
方向性尺寸候选为 1 个；满足主文全部门槛的单元为 0 个。

尺寸判断使用排序后的三边，逐轴容差为 `max(2 cm, 10% × 两边较大值)`。尺寸匹配只说明量级接近，不自动覆盖包型、材质、常规/季节状态或样本量门槛。

## 方向性尺寸候选

| Chanel | 竞品 | Chanel 尺寸签名 cm | 竞品尺寸签名 cm | 轴差 cm | 阻断原因 |
|---|---|---:|---:|---:|---|
| AS5293-B20304-94305 | Louis Vuitton M2A323 | 30 x 25.9 x 14 cm | 27.9 x 23.9 x 16 cm | 2.1 x 2 x 2 cm | blocked_regular_special_undisclosed;blocked_sample_insufficient |

## 阻断解释

- Chanel AS5293（CHANEL 25 Small Handbag）与 Louis Vuitton M2A323（Low Key Hobo PM）是本轮唯一通过包型、材质和排序尺寸容差的方向性候选；两边的 `regular_special` 都是 `not_disclosed`，因此不能直接推成常规核心。
- 该候选的核心独立家族数为 Chanel 2、Louis Vuitton 1，低于每品牌至少 3 个独立配置/家族的正式门槛，故标记为 `blocked_sample_insufficient`。
- Hermès 没有形成通过包型、材质和尺寸容差的 Chanel 组合；其可比方向仍需补充更接近的包型/材质配置。
- Chanel 的明确季节款继续隔离；Louis Vuitton 的 M46203 因材质组为 `textile`，不会与 Chanel 皮革 tote 强行合并。

## 决策

本轮不升级任何 Hermès/Louis Vuitton 单元进入主文比较。结果是“有 1 个可继续扩充的尺寸方向性候选”，而不是“已经形成可报告的跨品牌主文单元”。

## 输出

- `wave3_dimension_intersection_pairs_2026-09-08_us.csv`：30 个组合的逐对审计，含尺寸签名、轴差、容差、属性匹配和阻断原因。
- 本文件不修改 2026-09-07 主面板或历史价格输出。
