# Dior 常规/季节状态核验（2026-09-08，美国站）

## 访问结论

三条官方美国站详情页均可正常访问，并能读取参考号、产品名称、价格、材质和尺寸：

- [`M1325OWHP_M900`](https://www.dior.com/en_us/fashion/products/M1325OWHP_M900) Small Dior Book Tote，USD 3,900，calfskin，26.5 × 22 × 14 cm。
- [`M2835PNUC_M900`](https://www.dior.com/en_us/fashion/products/M2835PNUC_M900) Small Dior Toujours Vertical Tote Bag，USD 3,900，calfskin，18.5 × 18.5 × 12 cm。
- [`1LLME216MAL_H00N`](https://www.dior.com/en_us/fashion/products/1LLME216MAL_H00N) Small Dior Normandie Tote Bag，USD 6,800，calfskin，38 × 29 × 16 cm。

## 字段核验

在三条页面正文中检索 `collection`、`season`、`Fall` 和 `Spring`，均未找到匹配文本。页面也没有提供可把这些行标记为常规款或季节款的明确系列字段。

因此，`regular_special=not_disclosed` 是官网当前可见内容的结果，不是访问受阻、权限不足或页面解析失败。三条记录继续保留在季节敏感性路线的 Dior 上下文中，但不被强行归类为常规或季节。

## 处理决定

本轮不再重复抓取同一详情页；季节路线正式收口为描述性敏感性背景，不发布 Dior 与 Chanel 的季节价格差。若后续需要状态标签，应改查 Dior 官方系列目录、发布资料或其他明确标注系列的官方来源，并单独记录来源类型。
