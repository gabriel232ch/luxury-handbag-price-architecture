# 官网改版交接

## 改版目标

保留现有价格证据，把经营部分从长周期复苏概述改成放缓期检验。建议标题用英文交稿标题，主页卡片仍可保留 “Luxury Was Slowing. Why Did Chanel Look Different?”，副标题明确回答是集团收入部分恢复，不能预设免疫或手袋胜出。

2026-10-03 已通过浏览器读取当前线上项目页。当前页有十个章节，从 Conclusion 到 Sources，包含价格、历史、长周期财务、竞争、六个判断、张力和建议。无需再把新诊断作为第十一个章节追加；建议按英文交稿的论证次序重新组织。

## 对现有页面的处理

| 当前内容 | 改版动作 | 理由 |
|---|---|---|
| Price architecture / Historical change | 保留价格梯与历史图，压缩重复结论 | 构成价格证据起点 |
| Business trajectory, 2020–2025 | 长序列移至展开区；正文用 FY2023–FY2025 | 避免疫情低基数主导韧性判断 |
| Hermès / LVMH benchmark | 主文增加 Gucci；统一显示各自 FY2023=100 与披露增长定义 | 保留正反参照；不用跨币种规模排名 |
| Six insights / Strategic tensions | 融入主论证及边界，撤掉重复区块 | 让下一段由上一段问题引出 |
| Implications: validate customer migration | 删除项目行动承诺；边界保留客户/交易数据缺口 | 无客户资源，不安排不可执行访谈 |
| Sources and next evidence gate | 链接交接包、诊断报告、底表；结束于已支持答案 | 下一步是改版，不是扩大研究 |

## 两个需要纠正的旧表述

线上原文 “LVMH F&LG slowed in 2024–2025 while Chanel reported a recovery over the same period” 容易让读者认为 Chanel 两年都恢复。改成 Chanel 在 FY2024 下滑，FY2025 才部分恢复。

线上 tote 单元中位数目前只是方向性示例。后续 R1 严格比较门槛没有产生可发布的 headline cells，不能继续把这些示例放成 like-for-like 价格优势证据。保留分层竞争图，但把小样本单元移至方法附录，标明探索性与严格门槛未通过。[R1 最新状态](../research_r1/report/FINAL_STATUS_CN.md)

## 页面图表和数据

主文建议仅用三组视觉证据：可见价格端点；法国 Classic/Mini 历史；FY2023–FY2025 Chanel 收入与经营利润基期比。地区、渠道与利润桥用小表或展开区提供精确数据。长周期现金与投资图保留在附录，不承担因果证明。

精确 Chanel 主序列来自 `research_slowdown_2023_2025/data/chanel_profit_bridge_inputs.csv`。FY2023/FY2024/FY2025 收入分别为 19,743.9 / 18,699.3 / 19,269.1 百万美元；经营利润为 6,407.0 / 4,478.6 / 4,711.5。新页面不要用旧 19,700 约数重算基期比。所有增长标签区分 reported、comparable、constant currency 与 organic。

`content.json` 是内容交接元数据，不是现有网站运行时格式。开发端可继续使用原有交互组件；原 R1 export 保持不变。Markdown 相对链接以仓库根目录为基准解析，再转换成 GitHub/source 链接，不能直接当成网站路由。

## 发布验收

- 卡片、标题、首屏与结尾均不预设持续韧性。
- 价格快照和历史观察窗口与财务窗口分别显示。
- 集团、业务组、品牌、手袋样本的范围标签保留。
- 地区与渠道桥不相加；美妆估计不倒推出手袋收入。
- 不把 2026 商品销售解释为 FY2025 收入，不把公开自述写成访谈结果。
- customer instrument 只在撤回档案出现，不进入网站活跃研究计划。
- 原报告、数据、校验脚本与来源链接均能从远程仓库追溯。

交接包不含网站代码变更，也不代表线上页面已经更新。
