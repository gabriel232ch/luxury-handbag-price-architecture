# 2026-09-07 US live refresh

本文件记录第 1 步的同日美国站快照。采集通过用户本地 Chrome 的可见页面完成，页面内容使用浏览器渲染后的 DOM 读取；没有覆盖 2026-08-15 基线文件。

## Coverage

| Brand | Rows | Market | Price status | Source page |
| --- | ---: | --- | --- | --- |
| Chanel | 20 | US | 20 numeric | [US handbags](https://www.chanel.com/us/fashion/handbags/c/1x1x1/) |
| Hermès | 21 | US | 21 numeric | [Women’s bags and clutches](https://www.hermes.com/us/en/category/leather-goods/bags-and-clutches/womens-bags-and-clutches/) |
| Louis Vuitton | 20 | US | 20 numeric | [All handbags](https://us.louisvuitton.com/eng-us/women/handbags/all-handbags/_/N-tfr7qdp) |
| Dior | 20 | US | 20 numeric | [All bags](https://www.dior.com/en_us/fashion/womens-fashion/bags/all-the-bags) |

总计 81 条，全部为 `source_effective_date=2026-09-07`、`market=US`，参考号在品牌内唯一，价格均为数值型。

## Issue resolution

- Dior 美国站之前 7 条未解析价格，本次进入商品详情页逐条读取，20 条当前样本均得到美元价格。`M2821OSNW_M73M` 首次渲染有延迟，等待后确认价格为 `$4,300`。
- Hermès 之前的 4 个失效链接没有继续写入快照；本次以当前分类页返回的有效商品 URL 为准，21 条均能在分类 DOM 中读取名称、颜色和价格。
- Chanel 和 Dior 的可见详情页没有稳定提供数值尺寸，因此尺寸留空并在 `notes` 标明，后续产品主数据步骤再单独核实；这一步不把未知尺寸强行配对。
- Hermès 当前分类页快照未展开材质和数值尺寸，材质留空，等待产品主数据步骤补录。
- Louis Vuitton 详情页同时提供尺寸和材质，本次一并记录；英寸原样保留，后续统一转换或匹配。

## Validation

`live_refresh_2026-09-07_us.csv` 已通过结构检查：81 行、17 个字段；四品牌计数为 20/21/20/20；官方域名、同市场、同日期、数值价格和品牌内参考号唯一性均通过。

这一步只建立同日原始快照，不更新 `product_master.csv`、`observations.csv` 或主文配对结果。产品主数据和配对审计应在下一步基于该快照执行。
