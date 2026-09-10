# 研究方法与可复现性

## 1. 研究问题

本项目的核心问题是：

> Chanel 如何构建并持续抬升其手袋价格架构？这种 premiumization 在多大程度上伴随着健康的增长、盈利能力与品牌经济性，其表现与 Hermès 及更广泛的奢侈品皮具市场相比如何？

“伴随 / accompanied by”是有意选择的表述。价格与经营指标按时间对齐可以支持共同发生的描述，但公开证据不能识别价格变化对收入、利润、现金流或需求的因果影响。

## 2. BA OS 研究链

本阶段内部按 BA OS 管理：

`Research Question → Required Evidence → Source Hierarchy → Structured Data → Calculation → Finding → Strategic Interpretation → Claim Validation`

内部研究状态保存在被 `.gitignore` 忽略的 `.ba-os/`，包括 context、research plan、source map、evidence ledger 与 analytical decisions。public repository 只呈现经过筛选的 source registry、结构化数据、计算、验证和最终报告。

## 3. 四个 workstreams

| Workstream | 研究对象 | 核心输出 | 主要边界 |
|---|---|---|---|
| WS1 | Chanel 当前法国 / 美国官方标价 | entry / core / premium / icon、SKU steps、family steps、tier density、numeric vs non-numeric visibility | 非加权快照；不是完整 assortment census |
| WS2 | 2020–2026 历史价格 | aligned access/core 与 Classic/icon、绝对 gap、relative ratio、same-model / successor paths | 缺失年份不插值；successor 不写成精确同款 |
| WS3 | FY2020–FY2025 financial performance | Chanel company panel、Hermès Leather Goods & Saddlery、LVMH Fashion & Leather Goods | reporting grain 不对称；不估计 handbag-only economics |
| WS4 | 联合战略解释 | premiumization quality、resilience context、investment requirement、strategic tensions | 不把时间共变写成因果模型 |

Financial core window 截止完整 FY2025。2026 仅作为当前价格架构 endpoint；不把 FY2026 / H1 与完整年度横向比较混用。

## 4. Source hierarchy 与验证

### Tier 1：第一方 / 官方

- Chanel official Financial Results、Chanel Limited annual financial/result releases、官方法国 / 美国产品页。
- Hermès Universal Registration Document、annual results、official financial publications。
- LVMH annual results、annual report 与 official business-group tables。

### Tier 2：有限行业 context

Bain、McKinsey、BCG、Deloitte 等仅用于补充 luxury cycle、区域需求或皮具市场背景。行业层不替代公司财报，也不扩展成完整 luxury industry report。Phase 2 的 headline financial figures 全部来自 Tier 1。

每条关键 financial observation 保留：`entity`、`reporting_scope`、`segment`、`fiscal_year`、`period`、`metric`、`value`、`unit`、`currency`、`reported_or_constant_currency`、`source_id`、`source_url`、`publication_date`、`page_or_section`、`extraction_note`、`confidence`、`caveat`。完整 registry 在 `financial_business_performance/sources/source_registry.csv`。

## 5. Reporting grain

| Entity | Financial grain | 可支持的用途 | 不可写成 |
|---|---|---|---|
| Chanel | Chanel Limited consolidated company | Chanel business performance | Chanel handbag revenue / handbag margin |
| Hermès | Group + Leather Goods & Saddlery métier | 皮具经济 benchmark | handbags-only revenue 或 segment profit |
| LVMH | Group + Fashion & Leather Goods business group | 广泛 luxury leather-goods environment | Louis Vuitton revenue、Dior revenue |
| Louis Vuitton | 本证据集中无 comparable standalone audited financials | 价格架构与定性品牌 context | standalone revenue / margin |
| Dior | 本证据集中无 comparable standalone couture-brand financials | 价格架构与定性品牌 context | Dior couture standalone revenue / margin |

Hermès 的 Leather Goods & Saddlery 包含 bags、travel items、small leather goods、saddlery 与 equestrian products。LVMH Fashion & Leather Goods 是多品牌 business group；Christian Dior SE / Finance consolidated figures 也没有被改写为 Dior couture brand financials。

## 6. WS1 当前价格计算

当前价格使用既有 2026-08-15 官方价格 snapshot，并重新运行原有 current-price pipeline。数值分析只使用 `price_status=numeric` 的正数；询价、未解析和其他 non-numeric 状态保留在覆盖率表中，不进行插补。

市场按 FR / EUR 与 US / USD 分开计算，不做 FX、VAT、销售税、关税或 landed-cost 标准化。

新增诊断位于 `financial_business_performance/calculations/`：

- `sku_price_steps.csv`：按市场、品牌将数值 SKU 价格排序，计算相邻价格点的绝对 / 相对 step；重复价格保留为 0 step。
- `family_step_up.csv`：按产品家族数值中位数排序，计算相邻 family median step。
- `tier_density.csv`：沿用现有市场价格带并折叠为 entry / core / premium / icon；这是观察价格 tier，不是 affordability tier。
- `architecture_visibility.csv`：numeric displayed price 与 non-numeric / POR-or-unresolved 的可见性统计。
- `architecture_summary.csv`：Chanel 的最大相邻 SKU gap、pre-icon → icon gap、family median gap 和 entry-tier missingness。

`core_to_icon_step` 定义为最低观察 icon 价格减去最高观察 pre-icon 数值价格；它是可见标价间隔，不是 conversion barrier。若没有 numeric entry/lower-tier observation，`entry_to_core_step` 留空并记录为 not estimable，而不是制造一个 entry 价格。

## 7. WS2 历史价格计算

既有历史面板继续作为基础，保留：

- `SAME_MODEL_CONTINUOUS`：产品身份、尺寸、材质或 reference 连续性足以支持较强的跨期标价描述。
- `MODEL_SUCCESSOR`：产品家族延续但版本、材质、尺寸或商业定位发生变化，只支持方向性路径。

Chanel France 的 icon/access-core 比较只使用四个共同观察年份（2022、2023、2024、2026），不插值 2021 或 2025。核心指标为：

- `absolute_gap = icon_median - access_core_median`
- `relative_ratio = icon_median / access_core_median`
- `indexed_value = value / value_in_2022 × 100`

“Broad repricing”要求多个层级都上移；“ladder stretching”要求层级间 gap 或 ratio 的变化有明确证据。比例较稳定但绝对 gap 扩大时，结论应写成“整体上移并伴随绝对距离扩大”，而不是宣称 Classic 单独造成 premiumization。

## 8. WS3 财务计算

脚本 `build_financial_dataset.py` 将已确认的官方 observations 标准化到 `financial_business_performance/clean/financial_panel.csv`，并生成 raw、source registry、scope matrix、conflicts、missingness 与 build log。

脚本 `financial_performance_calculations.py` 生成：

- Chanel：annual revenue、reported / comparable growth、operating profit、operating margin、FCF、FCF margin、capex、capex/revenue、brand-support investment、brand-support/revenue、annual change、performance phase。
- Hermès：group revenue / growth / recurring operating income / margin / investments / adjusted FCF，以及 Leather Goods & Saddlery revenue、share、reported / constant-currency growth。
- LVMH：Fashion & Leather Goods revenue、reported / organic growth、recurring operating profit 与 derived margin；同时保留 group revenue 作为 scope context。
- Comparative：within-series 2020=100 index、growth direction、peak / trough；不做跨币种 nominal revenue ranking。

核心公式：

```text
operating_margin = operating_profit / revenue × 100
FCF_margin = free_cash_flow / revenue × 100
investment_intensity = investment / revenue × 100
annual_change = (current - prior) / prior × 100
revenue_CAGR = (revenue_end / revenue_start)^(1 / years) - 1
within_series_index = value / value_2020 × 100
```

reported growth 与 constant-currency / comparable / organic growth 始终分列。Chanel 2020 主 panel 使用 FY2021 release 明确提供的 restated comparative；原始 FY2020 operating profit 与 capex 仍作为 `comparative_only` 保存，并在 conflict log 中可追溯。

Hermès official displayed group margin 优先于用已四舍五入 revenue / profit 反推的 margin；derived check 同时保留。不同公司 FCF、investment 与 operating-profit label 的定义不被强行统一成一个会计指标。

## 9. Evidence → finding → interpretation

每个外部 claim 都必须回答三件事：

1. **Evidence：**哪一个 price / financial / benchmark observation 支持它？
2. **Finding：**这组数字本身显示什么？
3. **Interpretation：**这对 Chanel 的架构或战略意味着什么，且最强反例是什么？

“价格上升、收入上升、策略成功”不属于允许的自动推导。最终报告优先使用 `coexisted with`、`accompanied by`、`coincided with`、`consistent with` 等非因果措辞。价格在下行周期中保持不变只支持 architecture persistence，不支持 demand resilience。

## 10. 可复现路径

环境要求：Python 3.10+，脚本只依赖标准库。

```bash
python3 build_competitor_dataset.py
python3 competitive_pricing_calculations.py
python3 build_historical_dataset.py
python3 historical_pricing_calculations.py
python3 build_financial_dataset.py
python3 financial_performance_calculations.py
python3 price_architecture_diagnostics.py
python3 build_final_report_assets.py
python3 build_financial_report_assets.py
```

相关输出：

- 当前价格：`chanel_fr_us_handbags_current/`、`luxury_competitor_pricing_current/`、`competitive_pricing_calculations/`
- 历史价格：`luxury_historical_pricing/`、`historical_pricing_calculations/`
- 财务：`financial_business_performance/raw/`、`clean/`、`sources/`、`calculations/`、`logs/`
- 图表：`final_report_assets/01–08_*.svg`

## 11. 主要局限性与 readiness

- 价格是公开本地 list-price snapshot，不是 realized price、销量加权组合或完整 assortment census。
- Chanel financials 是 consolidated company，不能拆出 handbag / Classic revenue、units 或 product profitability。
- Hermès Leather Goods & Saddlery 与 LVMH Fashion & Leather Goods 的 reporting grain 与 Chanel 不对称；比较以 growth、margin context、within-series index 和 direction 为主。
- historical panel 不均衡；Dior 以 successor paths 为主，Hermès France Geta 有冲突，跨品牌历史 repricing ranking 不可估计。
- 价格、收入、利润、现金与 investment 的 temporal co-movement 不是 causal evidence。

在这些边界下，本项目的 final gate 为 **READY WITH LIMITATIONS**：数据层、来源定位、冲突处理、计算和 claim QA 可供 portfolio review；但任何完整需求模型、手袋级盈利模型或消费者行为结论都需要 Chanel 内部数据。
