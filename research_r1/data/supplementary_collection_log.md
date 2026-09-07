# Chanel 定向补充采集记录（第 2 步）

## 范围

- 市场：法国（EUR）与美国（USD）。
- 快照：`supplementary_current_2026-09-07`；不回填 `current_2026-08-15`。
- 家族：2.55、Boy、Chanel 19、Chanel 22、Chanel 25、WOC。
- 行粒度：官方参考号 × 市场 × 本次观察时间。

## 结果

- 11 个跨市场参考号，22 条市场观察；22 条均取得正数标价。
- 11 个 `sku_mapping` 均为同一参考号的 FR/US 精确配对，身份、材质、颜色和尺寸字段均来自官方页面内容。
- 2.55 的 Spring Summer 2026 行和 Chanel 25 Mini 的 Spring Summer 2026 行标为 `seasonal_collection`；WOC 标为 `sensitivity_only`，不进入手袋主分母。
- 本轮没有采集 Hermès、Louis Vuitton 或 Dior，也没有建立跨品牌配对。

## 方法与限制

本机直接 Playwright/HTTPS 访问被 Chanel 的边缘访问控制阻断；未使用 CAPTCHA、代理轮换、隐身或其他绕过方式。字段使用官方 Chanel 产品页内容的搜索结果进行人工转录，`extraction_method=manual_official_search_result`，并保留每个官方 URL。页面未明确价格生效日期，因此 `source_effective_date` 留空，观察日期仅表示页面读取日。

这批数据是补充快照，尚未合并进 R1 的价格输出；下一步才决定哪些行可进入产品属性筛选和竞品配对。

输出：

- `research_r1/data/supplementary_current_raw.jsonl`
- `research_r1/data/supplementary_current.csv`
- `research_r1/data/product_master.csv`
- `research_r1/data/sku_mapping.csv`
