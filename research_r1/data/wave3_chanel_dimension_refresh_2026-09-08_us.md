# Wave 3 Chanel 尺寸刷新日志（2026-09-08，美国站）

## 本步范围

本步只补采 Chanel 官方美国站的数值尺寸，作为 Wave 3 尺寸标准化的第一组新快照候选。数据保存在独立 top-up 文件，不并入 2026-09-07 主面板，也不替换旧快照。

## 采集结果

共记录 5 条官方美国站候选，全部包含参考号、美元价格、产品/包型、材质和官网原始尺寸；英寸已按 2.54 换算为厘米。

| 参考号 | 产品 | 原始尺寸 | 标准化尺寸 | 状态 | 处理 |
| --- | --- | --- | --- | --- | --- |
| `AS6498-B25468-UC476` | Small Flap Bag | 4.3 × 10.6 × 2.4 in | 10.9 × 26.9 × 6.1 cm | Fall Winter 2026 Pre-Collection | 季节隔离 |
| `AS3260-B19059-94305` | CHANEL 22 Small Handbag | 13.8 × 14.6 × 2.8 in | 35.1 × 37.1 × 7.1 cm | 未披露 | 条件性尺寸候选 |
| `AS5293-B20304-94305` | CHANEL 25 Small Handbag | 11.8 × 10.2 × 5.5 in | 30.0 × 25.9 × 14.0 cm | 未披露 | 条件性尺寸候选 |
| `AS6288-B24248-94305` | Small Shopping Bag | 5.9 × 12.6 × 4.5 in | 15.0 × 32.0 × 11.4 cm | Spring Summer 2026 | 季节隔离 |
| `A01113-Y04059-UB639` | Small Classic Handbag | 5.7 × 9.1 × 2.4 in | 14.5 × 23.1 × 6.1 cm | Fall Winter 2026 Pre-Collection | 季节隔离 |

## 资格判断

- 数值尺寸刷新候选：5 条。
- 可暂作非季节尺寸候选：2 条（`AS3260`、`AS5293`），但 `regular_special` 仍是 `not_disclosed`，不能自动视为常规款。
- 季节款：3 条，继续排除常规核心；它们的尺寸可以用于尺寸规则压力测试，但不用于常规价格比较。
- 本步没有修改主面板，也没有声称 Chanel 已形成跨品牌正式单元；Hermès/Louis Vuitton 尚未在本步刷新。

## 维度处理

保留官网英寸原文和厘米换算值；后续跨品牌匹配使用排序后的三边签名，并按 Wave 3 规则执行每轴容差。产品页面明确标为 CHANEL 22/25 Hobo 分类的两条记录采用 `hobo`；其他产品按官网产品名和现有保守分类记录。

## 官方来源

- [AS6498 Small Flap Bag](https://www.chanel.com/us/fashion/p/AS6498B25468UC476/small-flap-bag-patinated-lambskin-gold-tone-metal/)
- [AS3260 CHANEL 22 Small Handbag](https://www.chanel.com/us/fashion/p/AS3260B1905994305/chanel-22-small-handbag-shiny-calfskin-gold-tone-metal/)
- [AS5293 CHANEL 25 Small Handbag](https://www.chanel.com/us/fashion/p/AS5293B2030494305/chanel-25-small-handbag-grained-calfskin-gold-tone-metal/)
- [AS6288 Small Shopping Bag](https://www.chanel.com/us/fashion/p/AS6288B2424894305/small-shopping-bag-grained-calfskin-gold-tone-metal/)
- [A01113 Small Classic Handbag](https://www.chanel.com/us/fashion/p/A01113Y04059UB639/small-classic-handbag-lambskin-gold-tone-metal/)
