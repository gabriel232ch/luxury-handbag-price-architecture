# 研究方法与可复现性

## 研究问题与范围

本项目以公开可见的本地标价为基础，描述 Chanel、Hermès、Louis Vuitton 与 Dior 在法国和美国手袋样本中的价格架构，并考察有限历史面板中可支持的价格路径结论。分析对象仅为手袋；当前观察日期为 2026-08-15，历史面板覆盖 2020–2026（其中一条 Dior 观察早于该区间）。

项目不估计成交价、需求、支付意愿、利润、库存、品牌管理层意图或最优定价。法国与美国以各自本币分别分析；未进行汇率、税费、关税或落地成本标准化。

## 数据与血缘

| 主题 | 主要数据 | 用途 |
|---|---|---|
| Chanel 当前价格 | `chanel_fr_us_handbags_current/` | 官方法国与美国页面的原始记录、清洗表、匹配表和异常记录 |
| 三个竞品当前价格 | `luxury_competitor_pricing_current/` | Hermès、Louis Vuitton 与 Dior 的官方本地化页面观察 |
| 当前价格计算 | `competitive_pricing_calculations/` | 价格带、品牌摘要、家族梯度、可比单元和法国—美国精确货号映射 |
| 历史价格面板 | `luxury_historical_pricing/` | 历史观察、来源登记、产品线连续性、事件和未解决项 |
| 历史价格计算 | `historical_pricing_calculations/` | 路径、累计变化、CAGR、事件摘要与 Chanel 经典/进入组演化 |

当前页数据保留 `source_url`、观察时间、价格状态和原始文本。数值分析仅使用 `price_status=numeric` 的接受观察；询价和未解决状态保留在覆盖度统计中，但不插补为数值。

历史资料以公开专业价格来源为主，当前锚点来自官方页面。`luxury_historical_pricing/lineage/product_lineage.csv` 明确区分 `SAME_MODEL_CONTINUOUS` 与 `MODEL_SUCCESSOR`：前者支持更强的同款变化描述，后者仅支持产品线方向性判断。来源质量、冲突和未解决候选项见历史来源注册表、采集日志与异常文件。

## 计算定义

- 价格带在单一市场和币种内基于观察到的数值价格建立，不把 EUR 与 USD 合并。
- 品牌和产品家族摘要使用非加权样本统计；它们描述被采集的产品，而非完整全球商品组合或销售加权结构。
- 可比单元按市场、宽泛包型、尺寸组和材料类别分组，仅作方向性比较，不表示严格替代关系。
- 法国—美国映射仅限精确货号对照，呈现本地展示价格关系，不构成经济意义上的地理溢价。
- 历史价格变化不插补缺失年份；事件表只统计有来源支持的观察区间，不能视为完整调价日历。

## 复现

环境要求：Python 3.10 或更高版本；所有脚本仅依赖标准库。建议在仓库根目录依次运行：

```bash
python3 build_competitor_dataset.py
python3 competitive_pricing_calculations.py
python3 build_historical_dataset.py
python3 historical_pricing_calculations.py
python3 build_final_report_assets.py
```

数据构建脚本会重建当前或历史数据目录中的派生文件；计算脚本会重写对应的计算输出；图表脚本会重写 `final_report_assets/` 中的 SVG。因此，如需保留某次运行状态，请在执行前使用版本控制记录该状态。

## 主要局限性

- 当前价格为公开本地标价快照，不是完整商品普查，也不反映交易或库存。
- 价格询问状态和未解决页面不进行价格插补；样本覆盖限制会影响价格带与分布的完整性。
- 历史面板不均衡，非当前历史观察以二级来源为主；部分产品线是后续版本，且存在可见来源冲突。
- 没有足够对齐的跨品牌历史可比单元，因此不能从本项目推断跨品牌相对涨价或收敛趋势。
