# 最终报告附录：数据、方法与证据审计

本附录服务于复核与追溯，不重复主报告的完整叙事。所有结论均保留“公开标价观察”边界：它们不等同于成交价格、需求、支付意愿、利润或管理层意图。

## A. 数据范围与覆盖

### A1. 当前价格面板

| 品牌 | 接受观察 | 独立参考款 | 数值价格 | 非数值 / 未解析 | 法国 / 美国 |
|---|---:|---:|---:|---:|---:|
| Chanel | 41 | 21 | 35 | 6 条询价 | 20 / 21 |
| Hermès | 40 | 37 | 40 | 0 | 20 / 20 |
| Louis Vuitton | 40 | 35 | 40 | 0 | 20 / 20 |
| Dior | 40 | 20 | 32 | 8 条未解析 | 20 / 20 |
| **合计** | **161** | — | **147** | **14** | **80 / 81** |

当前数值覆盖率为 91.3%，但缺失机制不对称：Chanel 的 6 条记录为 Classic 询价，不是随机缺失；Dior 的 8 条为产品页未解析，且 7 条位于美国。

### A2. 历史价格面板

| 品牌 | 接受观察 | 数值观察 | 非当前历史观察 | 产品线 | 同款连续 | 后续版本 | 主要历史边界 |
|---|---:|---:|---:|---:|---:|---:|---|
| Chanel | 21 | 21 | 13 | 4 | 4 | 0 | 法国选定产品线较强；美国历史不足 |
| Hermès | 12 | 12 | 8 | 2 | 1 | 1 | Geta 冲突；不足以做组合级历史 |
| Louis Vuitton | 28 | 28 | 22 | 4 | 2 | 2 | 部分同款连续，其余为后续版本 |
| Dior | 16 | 15 | 10 | 3 | 0 | 3 | 无接受的同款连续线 |
| **合计** | **77** | **76** | **53** | **13** | **7** | **6** | 当前端点为官方锚点，历史非当前观察主要来自专业第三方历史价格资料 |

历史面板包含 24 条高置信度当前端点和 53 条非当前历史观察；历史非当前观察主要来自二级来源的专业价格记录，整体为中等质量。缺失年份不被视为零涨价，也未进行插值。

## B. 价格指标与分位数定义

1. **完整观察范围：**接受的品牌 × 市场 × 参考款行，包括询价与未解析价格；用于覆盖与缺失报告。
2. **数值分析样本：**`price_status=numeric` 且价格为正的行；用于本地货币分布、分位数与价格带。
3. **可比分析样本：**市场、宽口径包型、由尺寸推导的大小组与宽口径材质均相同的数值行；只用于方向性单元。
4. **分位数：**使用含端点的线性插值（inclusive linear interpolation），位置为 `(n − 1) × p`，P25、P50、P75 在排序后线性插值。
5. **经典产品组：**Chanel 将 Classic 11.12 与 Small Classic 作为分析性经典产品组；Mini Classic、Shopping Bag、Bowling Bag 为非经典观察组。6 条 Classic 询价记录不进入数值比值。
6. **询价状态：**保留状态，不估算数值，不放入价格带或中位数。

## C. 价格带构造

价格带按法国与美国分别观察到的价格聚类设置，不将 EUR 与 USD 合并，也不把它们解释成消费者可负担性区间。

| 市场 | 入门层 | 核心价格层 | 高端核心层 | 高价层 | 经典/超高价层 |
|---|---:|---:|---:|---:|---:|
| 法国 | < €3,000 | €3,000–€4,999 | €5,000–€6,999 | €7,000–€9,999 | ≥ €10,000 |
| 美国 | < $4,000 | $4,000–$5,999 | $6,000–$7,999 | $8,000–$10,999 | ≥ $11,000 |

价格带单元显示 0 时，含义为本次采样没有捕获该品牌的数值观察；不表示该品牌全球没有相应产品。价格带份额的分母是该品牌、该市场的数值观察数，而不是完整接受观察数。

## D. 方向性可比单元

指数公式：

`品牌在单元内的中位数 ÷ 该单元所有品牌数值观察的合并中位数 × 100`

该方法保留了市场、包型、尺寸组与材质组约束，但不能消除品牌组合、皮革等级、装饰、细节和产品生命周期差异。N=1 的单元只作方向性提示。

| 市场 / 单元 | 品牌 | N | 品牌中位数 | 单元基准 | 指数 | 强度 |
|---|---|---:|---:|---:|---:|---|
| 法国 / tote · large · leather | Chanel | 5 | €6,200 | €4,050 | 153 | 中 |
| 法国 / tote · large · leather | Dior | 6 | €3,350 | €4,050 | 83 | 中 |
| 法国 / tote · large · leather | Hermès | 2 | €6,475 | €4,050 | 160 | 中 |
| 法国 / tote · standard · leather | Chanel | 2 | €5,700 | €3,400 | 168 | 中 |
| 法国 / tote · standard · leather | Dior | 3 | €3,400 | €3,400 | 100 | 中 |
| 法国 / tote · standard · leather | Louis Vuitton | 1 | €2,900 | €3,400 | 85 | 中低 |
| 法国 / shoulder · standard · leather | Dior | 2 | €3,775 | €3,600 | 105 | 中 |
| 法国 / shoulder · standard · leather | Hermès | 4 | €4,975 | €3,600 | 138 | 中 |
| 法国 / shoulder · standard · leather | Louis Vuitton | 5 | €3,200 | €3,600 | 89 | 中 |

可比单元没有被升级为主图，是因为它们的样本量和产品等价性不足以支撑全局竞争结论。主报告只使用其最稳定的方向性信息：Chanel 在法国部分 tote 单元明显高于 Dior / Louis Vuitton，并接近 Hermès。

## E. 产品线连续性规则

### `SAME_MODEL_CONTINUOUS`

产品家族、尺寸、材质或参考款连续性足够高，可以把跨期变化作为同款/同一稳定产品线的可比标价路径。仍然不等同于完全不变的 SKU 经济学，也不代表每个缺失年份没有涨价。

### `MODEL_SUCCESSOR`

产品名称或家族延续，但尺寸、材质、版本、当前参考款或商业定位存在变化。它可以支持产品家族的方向性价格上移或当前架构演化，但不能写成“同一只手袋精确上涨 X%”。

### 当前锚点

2026 当前官方页面作为历史路径的最新端点；它们与历史二级来源价格记录中的产品身份已按产品线规则映射。当前端点的官方来源质量较高，但不自动提升历史中间年份的来源质量。

## F. 历史详细路径

### Chanel：法国同款连续路径

| 产品线 | 产品线名称 | 起点 → 当前 | 累计变化 | 主用途 | 置信度 |
|---|---|---:|---:|---|---|
| CH-C01 | Classic 11.12 | €8,990 → €10,500（2022–2026） | +16.8% | 可用于核心结论 | 中 |
| CH-C02 | Small Classic | €8,450 → €10,100（2022–2026） | +19.5% | 可用于核心结论 | 中 |
| CH-C03 | 方形 Mini Classic | €3,350 → €4,850（2020–2026） | +44.8% | 需日期对齐 | 中 |
| CH-C04 | 长方形 Mini Classic | €4,350 → €5,050（2022–2026） | +16.1% | 可用于核心结论 | 中 |

方形 Mini 的 +44.8% 使用 2020 起点，不能与经典产品组的 2022 起点直接比较。对齐窗口下，Mini/进入组为 +16.5%。

### Louis Vuitton

| 产品线 | 产品线 / 市场 | 连续性 | 起点 → 当前 | 累计变化 | 解释强度 |
|---|---|---|---:|---:|---|
| LV-L01 | Speedy 25 / FR | MODEL_SUCCESSOR | €1,180 → €3,200 | +171.2% | 方向性 |
| LV-L01 | Speedy 25 / US | MODEL_SUCCESSOR | $1,650 → $4,150 | +151.5% | 方向性 |
| LV-L02 | Speedy 20 / FR | 同款连续 | €1,960 → €2,400 | +22.5% | 可作核心结论支撑 |
| LV-L03 | Alma BB / FR | MODEL_SUCCESSOR | €1,100 → €2,800 | +154.5% | 方向性 |
| LV-L03 | Alma BB / US | MODEL_SUCCESSOR | $1,480 → $2,000 | +35.1% | 方向性 |
| LV-L04 | Neverfull MM / FR | 同款连续 | €1,150 → €1,500（至 2023） | +30.4% | 当前法国锚点不完整 |
| LV-L04 | Neverfull MM / US | 同款连续 | $1,540 → $2,240 | +45.5% | 可作核心结论支撑 |

### Dior

| 产品线 | 产品线 / 市场 | 连续性 | 起点 → 当前 | 累计变化 | 解释强度 |
|---|---|---|---:|---:|---|
| DI-D01 | Saddle / US | MODEL_SUCCESSOR | $4,200 → $4,400 | +4.8% | 方向性 |
| DI-D02 | Small Book Tote / FR | MODEL_SUCCESSOR | €2,600 → €3,250 | +25.0% | 方向性 |
| DI-D02 | Small Book Tote / US | MODEL_SUCCESSOR | $3,250 → $3,900 | +20.0% | 方向性 |
| DI-D03 | Medium Book Tote / FR | MODEL_SUCCESSOR | €2,700 → €3,650 | +35.2% | 方向性 |
| DI-D03 | Medium Book Tote / US | MODEL_SUCCESSOR | $2,700 → $3,350（至 2024） | +24.1% | 方向性 |

Dior 没有接受的 `SAME_MODEL_CONTINUOUS` 路径。部分路径包含材质、尺寸或版本变化，因此不承担精确同款涨价结论。

### Hermès

| 产品线 | 产品线 / 市场 | 连续性 | 起点 → 当前 | 累计变化 | 解释强度 |
|---|---|---|---:|---:|---|
| HM-H01 | Geta / FR | 同款连续但有冲突 | €4,550 → €5,300 | +16.5% | 敏感性 / 方向性 |
| HM-H01 | Geta / US | 同款连续 | $5,950 → $7,650 | +28.6% | 产品线层面 |
| HM-H02 | Jypsière / FR | MODEL_SUCCESSOR | €5,500 → €6,850 | +24.5% | 方向性 |

## G. 历史价格变化事件

事件文件是来源支持的观察区间，不是企业完整涨价日历。缺失年份不表示零变化。

| 品牌 | 事件行 | 正向事件 | 原始正向事件中位数 | 排除当前锚点 / 冲突后 | 观察范围中位数 |
|---|---:|---:|---:|---:|---:|
| Chanel | 9 | 9 | 7.9% | 7.9% | 1.0 年 |
| Hermès | 4 | 4 | 8.8% | 8.4% | 1.0 年 |
| Louis Vuitton | 15 | 12 | 10.5% | 10.5% | 1.0 年 |
| Dior | 7 | 7 | 15.5% | 6.1% | 2.6 年 |

Dior 的原始高值被 3 条当前锚点转移抬高；Hermès 的法国 Geta 冲突行会改变中间事件判断。事件频率不用于排名品牌的企业级涨价节奏。

## H. Hermès Geta 来源冲突

法国 Geta 的 2023 价格同时出现：

- [Luxe Front｜Hermès bag prices](https://luxefront.com/2022/12/02/hermes-bag-prices/)：报告 2023 更新价格 €5,550；
- [PurseBop｜confirmed Hermès prices in Europe 2024](https://www.pursebop.com/new-confirmed-hermes-prices-in-europe-2024/)：表中为 2023 €4,550、2024 €4,850。

两条记录均保留在 raw / conflict 数据中；主路径计算排除冲突行，敏感性中保留。由此不对 Hermès France Geta 讲单一确定的中间涨幅，也不把该路径提升为 Hermès 组合级历史结论。

## I. 法国—美国本地标价映射

| 品牌 | 数值精确配对 | 美国本地数字 / 法国本地数字：最低 | 中位数 | 最高 | 解释 |
|---|---:|---:|---:|---:|---|
| Chanel | 17 | 1.10 | 1.11 | 1.14 | 仅本地标价映射 |
| Dior | 13 | 1.16 | 1.19 | 1.22 | 仅本地标价映射 |
| Louis Vuitton | 5 | 1.24 | 1.24 | 1.30 | 仅本地标价映射 |
| Hermès | 3 | 1.44 | 1.44 | 1.45 | 仅本地标价映射 |

未进行 FX、VAT / 销售税、关税、运输、落地成本或通胀标准化。因此不能写成地理溢价、市场加价或经济价格差。

## J. 证据层级与置信度框架

### 当前证据

- **高：**官方本地化页面的数值价格、当前样本计数、精确参考款匹配的算术。
- **中：**价格带竞争格局、Chanel 双集群架构、当前经典产品组比值、宽口径可比单元。
- **中低：**将当前样本推广为全量组合、将宽口径单元解释成更严格替代关系。

### 历史证据

- **较强：**Chanel France 选定 `SAME_MODEL_CONTINUOUS` Classic / Mini 线；Louis Vuitton Speedy 20 France、Neverfull 的部分同款连续线。
- **方向性：**所有 Dior 产品线；Louis Vuitton Speedy / Alma 后续版本；Hermès Jypsière 与冲突敏感的 Geta。
- **不可估计：**Chanel 相对 Dior / Louis Vuitton 的历史价差路径，以及向 Hermès 的历史收敛/分离速度。

置信度描述的是证据对限定结论的支持强度，不是某项策略成功的概率。

## K. 详细来源注册表

### K1. 当前官方来源（代表性页面）

| 品牌 | 市场 | 来源 |
|---|---|---|
| Chanel | FR / US | [Classic 11.12 FR](https://www.chanel.com/fr/mode/p/A01112Y04059U8390/sac-classique-11-12-agneau-metal-dore/)；[Classic 11.12 US](https://www.chanel.com/us/fashion/p/A01112Y04059U8390/classic-11-12-handbag-lambskin-gold-tone-metal/) |
| Hermès | FR / US | [Geta FR](https://www.hermes.com/fr/fr/product/sac-hermes-geta-H085408CKAW/)；[Geta US](https://www.hermes.com/us/en/product/hermes-geta-bag-H085408CKAW/) |
| Louis Vuitton | FR / US | [Speedy FR](https://fr.louisvuitton.com/fra-fr/produits/sac-speedy-soft-25-lv-crafty-autres-toiles-monogram-nvprod7890058v/M2A038)；[Speedy US](https://us.louisvuitton.com/eng-us/products/speedy-bandouliere-25-autres-toiles-monogram-nvprod7890058v/M2A038) |
| Dior | FR / US | [Saddle FR](https://www.dior.com/fr_fr/fashion/products/M0457CUQW_M900)；[Saddle US](https://www.dior.com/en_us/fashion/products/M0457CUQW_M900) |

完整当前产品级 URL 随行保存在：`chanel_fr_us_handbags_current/clean_data.csv` 与 `luxury_competitor_pricing_current/clean/competitor_pricing_clean.csv` 的 `source_url` 字段。当前品类页也保存在两份 collection log 中。

### K2. 历史专业来源

| 来源 | 覆盖用途 |
|---|---|
| [Bagaholic｜Chanel Classic EU guide](https://lvbagaholic.com/fr/blogs/blog-de-bagaholic-1/chanel-classic-bag-sac-eu-prix-list-reference-guide) | Chanel Classic、Small Classic、Mini 2022–2024 |
| [PurseBop｜Chanel 2020](https://www.pursebop.com/chanel-admits-to-price-increase-here-are-the-new-prices-2020/) | Chanel 方形 Mini 2020 |
| [Luxe Front｜Hermès 2022 / 2023](https://luxefront.com/2022/12/02/hermes-bag-prices/) | Hermès Geta 来源分支 |
| [PurseBop｜Hermès Europe 2024](https://www.pursebop.com/new-confirmed-hermes-prices-in-europe-2024/) | Hermès Geta / Jypsière |
| [PurseBlog｜Hermès 2024](https://www.purseblog.com/hermes/hermes-price-increase-2024-its-here-already/) | Hermès Geta US |
| [Bagaholic｜Louis Vuitton 2021](https://lvbagaholic.com/blogs/lv_bagaholic/louis-vuitton-increases-prices-worldwide-in-january-2021) | Speedy、Alma、Neverfull 2021 |
| [Luxe Front｜Louis Vuitton price list](https://luxefront.com/2022/12/13/louis-vuitton-bag-price-list-complete-guide-usd-eur/) | Speedy、Alma、Neverfull 2022–2023 |
| [PurseBop｜Louis Vuitton 2024](https://www.pursebop.com/louis-vuitton-global-price-increase-2024/) | Speedy、Alma 2024 |
| [PurseBop｜Dior 2020](https://www.pursebop.com/dior-follows-louis-vuitton-and-chanel-with-price-increases/) | Saddle / Book Tote 2019–2020 |
| [Fifth Avenue Girl｜Dior 2023](https://fifthavenuegirl.com/dior-price-increase-july-2023/) | Dior Saddle / Book Tote 2022–2023 |
| [Bagaholic｜Dior Book Tote guide](https://lvbagaholic.com/blogs/lv_bagaholic/dior-book-tote-reference-guide) | Small / Medium Book Tote 2024 |

历史来源注册表的完整原始字段、产品线 ID、来源质量与访问时间见：`luxury_historical_pricing/logs/HISTORICAL_SOURCE_REGISTRY.csv`。该文件是内部审计索引，不被当作外部证据来源本身。

## L. 可复现计算路径

- 当前价格与价格带：`competitive_pricing_calculations.py` → `competitive_pricing_calculations/`
- 历史路径与经典产品组/进入组：`historical_pricing_calculations.py` → `historical_pricing_calculations/`
- 当前清洗与逐行 URL：`chanel_fr_us_handbags_current/clean_data.csv`、`luxury_competitor_pricing_current/clean/competitor_pricing_clean.csv`
- 历史清洗、事件、产品线：`luxury_historical_pricing/clean/historical_pricing_clean.csv`、`luxury_historical_pricing/events/price_change_events.csv`、`luxury_historical_pricing/lineage/product_lineage.csv`
- 数据来源、清洗边界与连续性判定：`chanel_fr_us_handbags_current/collection_log.md`、`luxury_competitor_pricing_current/logs/collection_log.md`、`luxury_historical_pricing/logs/HISTORICAL_COLLECTION_LOG.md`、`luxury_historical_pricing/logs/HISTORICAL_SOURCE_REGISTRY.csv` 与 `luxury_historical_pricing/lineage/product_lineage.csv`

这些文件用于复核计算与证据链，不替代本文对外使用的官方/历史来源链接。

## M. Financial & Business Performance workstream

### M1. Financial scope matrix

| Entity | Financial grain | Main use | Explicit non-use |
|---|---|---|---|
| Chanel | Chanel Limited consolidated company | Chanel FY2017–FY2025 business performance | Handbag / Classic revenue、units、gross margin、SKU profitability |
| Hermès | Group + Leather Goods & Saddlery métier | Leather-goods benchmark | Métier operating profit、handbags-only economics |
| LVMH | Group + Fashion & Leather Goods business group | Broad luxury leather-goods environment | Louis Vuitton revenue、Dior revenue、brand-level margin |
| Louis Vuitton | No standalone audited financials in this evidence set | Qualitative brand context and price architecture | Standalone revenue / profit / margin |
| Dior | No comparable standalone couture-brand financials in this evidence set | Qualitative brand context and price architecture | Dior couture standalone revenue / profit / margin |

The machine-readable version is [`financial_scope_matrix.csv`](financial_business_performance/clean/financial_scope_matrix.csv). This asymmetry is a finding about public disclosure, not a data-cleaning defect.

### M2. Structured financial panel contract

Every raw observation is retained in [`financial_observations_raw.jsonl`](financial_business_performance/raw/financial_observations_raw.jsonl) and normalized in [`financial_panel.csv`](financial_business_performance/clean/financial_panel.csv). Required audit fields are:

`entity`, `reporting_scope`, `segment`, `fiscal_year`, `period`, `metric`, `value`, `unit`, `currency`, `reported_or_constant_currency`, `source_id`, `source_title`, `source_url`, `publication_date`, `page_or_section`, `extraction_note`, `confidence`, `caveat`, `selection_status`, `metric_status`, `precision_note`, `source_basis`.

The build preserves all observations when a same-key conflict exists. The selected calculation basis is explicit in `selection_status`, and the conflict is logged in [`conflicts.csv`](financial_business_performance/logs/conflicts.csv). Missing / unavailable disclosures are logged in [`missingness.csv`](financial_business_performance/logs/missingness.csv), not filled by proxy.

### M3. Chanel financial panel: FY2020–FY2025

| FY | Revenue USD m | Comparable growth | Operating profit USD m | Operating margin | FCF USD m | Capex USD m | Brand-support investment USD m |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2020 | 10,108 | -18.0% | 2,018 | 20.0% | 679 | 1,077 | 1,360 |
| 2021 | 15,639 | +49.6% | 5,461 | 34.9% | 4,540 | 758 | 1,795 |
| 2022 | 17,200 | +17.0% | 5,776 | 33.6% | 3,534 | 668 | 2,052 |
| 2023 | 19,700 | +16.0% | 6,407 | 32.5% | 3,755 | 1,227 | 2,463 |
| 2024 | 18,699 | -4.3% | 4,479 | 24.0% | 1,842 | 1,755 | 2,445 |
| 2025 | 19,269 | +1.8% comparable / +3.0% reported | 4,712 | 24.5% | 2,646 | 1,449 | 2,395 |

Operating margin、FCF margin、capex / revenue、brand-support / revenue、annual changes 与 CAGR 均由 [`chanel_annual_performance.csv`](financial_business_performance/calculations/chanel_annual_performance.csv) 与 [`chanel_summary.csv`](financial_business_performance/calculations/chanel_summary.csv) 生成。2020–2025 nominal revenue CAGR 为 13.8%；2020–2025 operating margin change 为 +4.5 percentage points；这些是 company-level derived metrics，不是 handbag economics。

### M4. Benchmark panels

- [`hermes_benchmark.csv`](financial_business_performance/calculations/hermes_benchmark.csv)：Hermès group revenue / growth / recurring operating margin / investments / adjusted FCF，以及 Leather Goods & Saddlery revenue、share 和 reported / constant-currency growth。
- [`lvmh_fashion_leather_goods.csv`](financial_business_performance/calculations/lvmh_fashion_leather_goods.csv)：LVMH Fashion & Leather Goods revenue、reported / organic growth、recurring operating profit 与 derived margin。
- [`comparative_trends.csv`](financial_business_performance/calculations/comparative_trends.csv)：以 2020=100 的 within-series index；不做跨币种 nominal ranking。

Hermès Leather Goods & Saddlery 的 segment share 2020 为 50.2%、2025 为 44.2%；LVMH Fashion & Leather Goods 2025 organic growth 为 -5.0%。二者都不能被改写为 handbags-only 或单一品牌数据。

### M5. Official financial source register

| Source family | Coverage | Official source |
|---|---:|---|
| Chanel Limited Financial Results | FY2017–FY2025 | [Chanel Financial Results](https://www.chanel.com/es/financial-results/) |
| Hermès annual results / URD | FY2020–FY2025 | [Hermès FY2025 full-year results](https://assets-finance.hermes.com/s3fs-public/node/pdf_file/2026-02/1770842738/hermes_20260212_pr_2025fullyearresults_va.pdf) |
| LVMH annual results | FY2020–FY2025 | [LVMH FY2025 official results](https://www.lvmh.com/en/publications/solid-performance-in-a-disrupted-global-economic-and-geopolitical-environment) |

The full row-level registry, including each fiscal-year publication date and page / section, is [`source_registry.csv`](financial_business_performance/sources/source_registry.csv). The source set is first-party; no secondary estimate replaces an official disclosure.

### M6. Financial non-estimables

The following remain explicitly unavailable: Chanel handbag revenue, handbag units, handbag gross margin, Classic revenue; Hermès Leather Goods & Saddlery operating profit; LVMH Fashion & Leather Goods segment investment; Louis Vuitton standalone revenue; Dior standalone brand revenue. They are marked `not publicly disclosed / not estimable from available evidence` in the panel.

## N. Phase 2 calculation registry

| Output | Script | Main boundary |
|---|---|---|
| Current architecture, price bands, family summaries | `competitive_pricing_calculations.py` | Non-weighted observed list-price sample |
| SKU / family steps, tier density, visibility, Chanel gaps | `price_architecture_diagnostics.py` | Numeric prices only; missing / unresolved states retained separately |
| Historical paths, same-model / successor, icon-access gap | `historical_pricing_calculations.py` | No interpolation; successor paths are directional |
| Financial panel | `build_financial_dataset.py` | No silent conflict overwrite; no unavailable metric imputation |
| Financial performance / benchmarks | `financial_performance_calculations.py` | Currency and reporting grain remain visible |
| Financial charts | `build_financial_report_assets.py` | No price / revenue dual-axis correlation chart |

## O. Final evidence governance

The external claim map is [`docs/EVIDENCE_MAP.md`](docs/EVIDENCE_MAP.md). The release gate is [`docs/VALIDATION.md`](docs/VALIDATION.md). Together they document:

- claim → price evidence → financial evidence → benchmark → confidence → caveat;
- current and historical price reconciliation;
- headline financial reconciliation and restated comparative treatment;
- reporting grain, currency and reported / constant-currency controls;
- causal-language QA and chart QA;
- remaining unestimable metrics and readiness status.

Final status is **READY WITH LIMITATIONS**. The project is strong enough for a portfolio business-analysis case because the evidence chain is structured and auditable; it is not a substitute for internal Chanel customer, volume, mix, inventory or product-economics data.
