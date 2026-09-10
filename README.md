# Chanel Premiumization Strategy

## Handbag Price Architecture, Financial Performance and Competitive Positioning

本项目研究一个更具体的商业问题：**Chanel 如何构建并持续抬升其手袋价格架构？这种 premiumization 在多大程度上伴随着健康的增长、盈利能力与品牌经济性，其表现与 Hermès 及更广泛的奢侈品皮具市场相比如何？**

## 一句话答案

Chanel 的 premiumization 不是单纯把 Classic 价格抬高，而是让可见价格梯整体上移，同时保留 Classic/icon 的高位锚点；2020–2025 年，这一价格演变与 Chanel consolidated business 的强劲复苏、较高经营利润率、现金创造和持续品牌/资本投入共存，但 2024 年的利润和现金压力也说明：价格上移并不能消除行业周期、地域需求和再投资要求。公开证据支持“共同发生 / accompanied by”，不支持“价格导致经营结果”的因果结论。

## 为什么重要

价格架构决定品牌在不同层级面对谁、客户如何从 entry/core 迁移到 icon，以及高端定位需要怎样的品牌、渠道、体验和工艺投入。只看官网标价可以识别架构，却不能单独判断增长质量或品牌经济性；因此本项目把价格、历史路径、官方财务披露和 reporting-grain-valid benchmark 放在同一证据链中。

## 使用的证据

- Chanel 官方本地化手袋价格页面：法国 / 美国 2026-08-15 快照。
- 既有 2020–2026 历史价格面板：same-model continuous 与 model successor 分开处理。
- Chanel Limited 官方 FY2017–FY2025 financial results：consolidated revenue、operating profit、FCF、capex、brand-support investment 与官方经营评论。
- Hermès 官方 FY2020–FY2025 annual results / URD：group 与 Leather Goods & Saddlery métier。
- LVMH 官方 FY2020–FY2025 annual results：group 与 Fashion & Leather Goods business group。
- 有限的官方 / 权威 industry context；不包含消费者评论、社交舆情、问卷、resale、搜索量或 willingness-to-pay 估计。

## 核心发现

1. **Chanel 当前架构是高可见进入门槛 + Classic 锚点。** 当前接受观察为 41 条，35 条有数值价格；法国数值范围为 €4,850–€12,250，美国为 $5,400–$13,500。法国 €6,700 → €10,000、美国 $7,400 → $11,000 是本次样本最大的 pre-icon 到 icon 可见间隔。
2. **历史 evidence 更支持 broad repricing，同时存在一定 ladder stretching。** 在 2022–2026 对齐的 Chanel France 选定产品线中，Classic 中位数上涨 18.1%，Mini/access-core 上涨 16.5%；相对比值约从 2.052× 变为 2.081×，绝对价差从 €4,470 扩大到 €5,350。
3. **经营表现与 premiumization 共存，但不是线性成功故事。** Chanel 2020–2025 名义收入 CAGR 为 13.8%；operating margin 从 20.0%（2020 restated basis）恢复至 24.5%（2025），但 2024 收入 comparable growth 为 -4.3%、经营利润下降 30.1%、FCF 下降 50.9%。2025 FCF 回升 43.6%。
4. **再投资是高端定位的组成部分。** Chanel brand-support investment 在 2020–2025 年间保持在约收入的 11.5%–13.5%；2024 capex/revenue 为 9.4%，2025 为 7.5%。官方披露还指向 boutiques、client experience、craftsmanship、supplier capacity 与 real estate 投入。
5. **竞争必须按 grain 与 tier 比较。** Hermès Leather Goods & Saddlery 是较强的皮具经济 benchmark，但包含 bags、travel、small leather goods、saddlery 与 equestrian products；LVMH Fashion & Leather Goods 是多品牌环境，绝不能改写成 Louis Vuitton 或 Dior 的独立收入。

## 交付物

- [最终战略报告](FINAL_LUXURY_HANDBAG_PRICING_STRATEGY_CN.md)
- [最终报告附录](FINAL_REPORT_APPENDIX_CN.md)
- [研究方法](docs/METHODOLOGY_CN.md)
- [证据地图](docs/EVIDENCE_MAP.md)
- [验证与 readiness](docs/VALIDATION.md)
- [核心 SVG 图表](final_report_assets/)
- [Financial & Business Performance 数据层](financial_business_performance/)
- [策略演示 PPTX（原有交付）](LUXURY_HANDBAG_PRICING_STRATEGY_PRESENTATION.pptx)

## 分析框架

```mermaid
flowchart LR
    A[Research question] --> B[Required evidence]
    B --> C[Official sources and scope]
    C --> D[Structured price + financial panels]
    D --> E[Calculations and conflict logs]
    E --> F[Findings]
    F --> G[Strategic interpretation]
    G --> H[Claim validation and readiness]
```

项目内部使用 BA OS 管理研究问题拆解、source hierarchy、evidence ledger、reporting-grain、冲突和 claim validation；内部状态保存在被忽略的 `.ba-os/`，不作为 public portfolio deliverable。对外只保留可复核的数据、来源、计算、方法与结论。

## 可复现入口

在仓库根目录运行：

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

Financial panel 的每条 observation 都保留 entity、reporting scope、fiscal year、metric、unit、currency、reported / constant-currency basis、source URL、page / section、confidence 和 caveat。冲突不静默覆盖，unavailable disclosure 保留在 missingness register 中。

## 数据边界

- 当前价格是非加权官方页面快照，不是完整商品普查、成交价或销量加权组合。
- 法国与美国价格分开计算；未做 FX、VAT、销售税、关税或 landed-cost 标准化。
- Financial core window 为 FY2020–FY2025；Chanel 另保留 FY2017–FY2019 长历史。2026 价格是 architecture endpoint，不与 FY2026/H1 经营数据混合。
- Chanel financial figures 是 consolidated company，不是 handbag-only；Hermès Leather Goods & Saddlery 不是 handbags-only；LVMH Fashion & Leather Goods 不是 Louis Vuitton / Dior standalone。
- 不估计 Chanel handbag revenue、units、gross margin、Classic revenue、SKU profitability、conversion、demand elasticity、willingness to pay、Louis Vuitton standalone revenue 或 Dior standalone brand revenue。
- “价格没有下降”只能说明 architecture persistence，不能证明需求 resilience。

## R1 基础研究包

原有 `research_r1/` 作为价格研究基础保留，包含当前 / 历史 snapshot、source logs、lineage、计算和 R1 report。其验证边界与 Phase 2 新增财务层已在最终报告、附录和 `docs/VALIDATION.md` 中重新统一。

```bash
python3 scripts/r1/build.py
python3 scripts/r1/validate.py
python3 scripts/r1/export_case_study.py
python3 -m unittest discover -s tests/r1 -p 'test_*.py'
```

## 许可

当前未附带开源许可证。若计划复用代码或数据，请先联系仓库维护者。
