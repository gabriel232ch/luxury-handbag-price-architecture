# Wave 2 Hobo 路线决定（2026-09-08，美国站）

## 决定

将 `US|hobo|small|leather` 标记为 `blocked_sample_insufficient`，保留为方向性路线，不进入常规主文价格比较。

## 证据

- Chanel 当前可核验的明确 Small Hobo 只有既有 `AS6617B2621894305` 和季节候选 `AS6411-B24762-U8389`；`AS6411` 明确属于 Métiers d'art 2026。`AS6570` 虽有完整价格、材质和尺寸，但官方名称没有 Small 标签。
- Chanel 历史分类页列出的 `AS6022-B22652-U5336` 详情路径当前重定向到 Fashion 首页，缺少可复核的美国价格和尺寸，不能进入 2026-09-08 快照。
- Dior 当前官方 Hobo 分类页明确标 Small 的 6 个 Dior Toujours 变体已覆盖现有面板；Diorstar Hobo 页面虽有价格、材质和尺寸，但没有 Small 标签。

## 隔离规则

- `seasonal_collection`：保留在候选和季节敏感性记录中，排除常规核心。
- `unknown_size`：保留原始字段，禁止由尺寸数值或容量描述反推 Small。
- 历史分类可见但详情不可复核的产品：记录阻断线索，不写入同日快照。

## 对主面板的影响

本决定不修改 `live_refresh_2026-09-07_us.csv`、`same_date_pairing_panel_2026-09-07_us.csv` 或配对结果；它只更新采样目标状态和路线审计。

## 下一路线

转入 Wave 3：先为 Chanel、Hermès、Louis Vuitton 建立数值尺寸采集和标准化规则，再判断是否能形成跨品牌的可比尺寸单元。Wave 3 仍须保持同市场、同日期、同包型、同尺寸、同材质和样本门槛。
