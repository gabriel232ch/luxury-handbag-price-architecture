# 2026-09-07 竞品产品主数据审计

本文件对应第 2 步。数据来自同日美国站快照和官方商品详情页，单独输出到 `product_master_competitors_2026-09-07_us.csv`，没有覆盖现有只含 Chanel 的 `product_master.csv`。

## 字段完成度

| 品牌 | 行数 | 参考号 | 材质 | 尺寸 | 用途/包型 | 常规/季节状态 | 当前可用 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Hermès | 21 | 21/21 | 21/21 | 21/21 | 21/21 | 21 `not_disclosed` | 11 available / 10 unavailable |
| Louis Vuitton | 20 | 20/20 | 20/20 | 20/20 | 20/20 | 20 `not_disclosed` | 20 available |
| Dior | 20 | 20/20 | 20/20 | 20/20（名称尺寸标签） | 20/20 | 20 `not_disclosed` | 20 available |

Dior 的详情页可核实 Small/Medium/Large 等尺寸标签，但可见 `Size & Fit` 面板没有稳定暴露数值长宽深，所以 `dimensions_cm` 保留为空；这 20 条不能进入要求数值尺寸的严格配对单元。Louis Vuitton 和 Hermès 的英寸尺寸已按 2.54 转换为厘米。

## 隔离与保守规则

- Hermès 有 10 条、Louis Vuitton 有 3 条尺寸标签为 `unknown`；这些行保留在主数据中，但必须在配对审计中单独隔离。
- 本批竞品没有 WOC 行。
- 官方详情页没有明确给出稳定的 `regular` / `seasonal` 标记，因此 61 条统一记为 `regular_special=not_disclosed`，没有凭产品名称或当前页面顺序推断季节属性。
- Hermès 详情页选中变体的颜色优先于分类页颜色；例如部分分类页颜色与详情页选中颜色不同，主数据保留详情页当前选中变体并保留原始 URL。
- `availability_status` 只表示页面当前可用性，不代表停产判断；10 条 Hermès 页面显示当前不可用，仍保留参考号、属性和价格作为观察记录。

## 生成与校验

生成脚本：`scripts/r1/build_competitor_product_master.py`

输出文件：`research_r1/data/product_master_competitors_2026-09-07_us.csv`

校验结果：61 行；Hermès/Louis Vuitton/Dior 分别为 21/20/20；品牌内参考号和 `product_id` 均唯一；所有来源为官方美国站 URL；所有行均有 `verified_` 身份状态。当前步骤只完成主数据建档，没有合并到基线观察、没有重跑价格计算，也没有生成新的跨品牌价格比较。
