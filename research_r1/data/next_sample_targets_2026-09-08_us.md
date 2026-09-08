# 2026-09-08 美国站下一轮采样目标

本文件冻结下一轮采样目标，不代表新数据已经采集。目标快照必须由 Chanel、Hermès、Louis Vuitton、Dior 在同一日期重新刷新；不能把 2026-09-08 新行直接并入 2026-09-07 价格单元。

## 目标门槛

- 每个进入正式比较的品牌至少 3 个独立配置/去变体组；当前审计的每品牌 2 条数值行只作为筛选门槛，不作为最终旗舰主文门槛。
- 继续要求同市场、同日期、同包型、同尺寸、同材质和数值价格。
- 显式季节款、WOC/小皮具、未知尺寸、未知包型和未知材质继续隔离。
- `regular_special` 必须保留真实状态；页面没有披露时标记为 `not_disclosed`，不能推成常规款。

## 采样波次

### 波次 1：加深已通过的 Chanel–Dior 单元

目标单元为 `US|tote|small|leather`。当前 Chanel 有 2 条、1 个独立 Shopping 家族；Dior 有 5 条、2 个独立家族。下一轮至少新增 Chanel 2 个独立配置、Dior 1 个独立配置，才接近每品牌 3 个独立组的正式门槛。

### 波次 2：验证第二个 Chanel–Dior 单元

目标单元为 `US|hobo|small|leather`。当前 Chanel 只有 1 条、Dior 的 6 条主要集中在 Toujours。下一轮至少新增 Chanel 2 个独立配置、Dior 2 个独立配置；如果仍集中在同一家族，保留为方向性单元，不升级为正式主文。

### 波次 3：为 Hermès/Louis Vuitton 建立可行的尺寸交集

当前严格标签没有形成 Chanel–Hermès 或 Chanel–Louis Vuitton 单元，主要原因是品牌尺寸标签不可直接等同：Hermès 使用 18、20、25、35、41 等数字或未知；Louis Vuitton 使用 BB、PM、MM、nano；Chanel 刷新行又缺少可见数值尺寸。波次 3 先采集 Chanel 数值尺寸和明确用途，再对 Hermès/LV 使用同一尺寸标准化规则；没有完成这一步前，不把 `BB=small`、`PM=medium` 或 `nano=mini` 当作事实。

## 每条新行必须留存

官方美国站 URL、采集时间、有效日期、参考号、数值价格、产品用途/包型、尺寸原文与标准化尺寸、材质原文与材质组、常规/季节状态、可售状态和字段证据备注。四品牌必须使用同一个新快照日期，旧的 2026-09-07 快照保持不可变。

## 停止条件

如果新快照仍没有至少一个 Chanel–Hermès/LV 单元同时满足属性和 3 个独立配置门槛，结果继续标记为 `blocked_until_dimension_capture` 或 `blocked_sample_insufficient`，不为了填满样本而放宽尺寸或材质匹配。
