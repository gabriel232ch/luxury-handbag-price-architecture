# Wave 2 Hobo 候选搜索审计（2026-09-08，美国站）

## 搜索目的

在不放宽 `US|hobo|small|leather` 属性门槛的前提下，寻找新的官方美国站候选：

1. Chanel：明确写出 Small Hobo、并能取得美国价格、材质和尺寸；
2. Dior：明确写出 Small 的非-Toujours Hobo。

本步只记录搜索结果，不修改主面板、不重跑配对审计。

## Chanel

- 当前官方 Hobo 分类页列出的可见 Small Hobo 是 `AS6411-B24762-U8389`；该行已经在上一笔 Wave 2 候选记录中，并且明确属于 Métiers d'art 2026 季节款。
- 当前分类页另列 `AS6570-B25732-94305` Hobo Handbag，但名称没有 Small 标签；该行已经按 `unknown_size` 隔离。
- 官方历史分类页仍显示 Cruise 2025/26 的 `AS6022-B22652-U5336` Small Hobo Bag（Suede Calfskin, Tortoise-Shell Effect Plexi & Gold-Tone Metal，Pink）。点击官方详情链接后重定向到 Fashion 首页，未返回产品价格或尺寸；同时该产品属于历史 Cruise 2025/26，而非当前可复核的同日美国可售详情。因此不写入 2026-09-08 候选数据。

## Dior

- [Dior US Hobo 分类页](https://www.dior.com/en_us/fashion/discover/hobo-bag-for-women) 当前明确标注 Small 的 Hobo 为 6 个 Dior Toujours 变体：Deep Amaranth、Black、Marron Bobby、Soupir Green、Ballet Pink、Ice Blue；这些参考号已经覆盖当前 2026-09-07 面板的 6 条 Dior hobo 行。
- 同一官方分类页列出多个 Diorstar Hobo Bag with Chain，但产品名称均没有 Small 标签。此前核验的 `S3202UDBB_M900` 和 `S3202PNIO_M900` 已按 `unknown_size` 阻断；不能用尺寸或“适合手机/卡夹”等容量描述推断 Small。
- 当前官方 Handbags 页面也只把上述 Dior Toujours Hobo 变体标为 Small，未发现新的非-Toujours Small Hobo。

## 搜索决定

- 本次搜索没有新增可以进入正式主文的行。
- `AS6022` 保留为“历史分类可见、当前详情不可复核”的阻断线索，不纳入快照。
- Dior 的非-Toujours Hobo 继续保持 `unknown_size`，不降级为 Small。
- Wave 2 仍是方向性路线；在取得至少两个新的、明确 Small、字段完整的 Chanel 配置以及两个新的 Dior 配置前，不升级主文。

## 官方来源

- [Chanel 当前 Hobo 分类](https://www.chanel.com/us/fashion/handbags/c/1x1x1x4/hobo-bags//)
- [Chanel 历史 Hobo 分类（含 AS6022）](https://www.chanel.com/us/fashion/handbags/c/1x1x1x4/hobo-bags/)
- [Chanel AS6022 历史详情路径（当前重定向）](https://www.chanel.com/us/fashion/p/AS6022B22652U5336/small-hobo-bag-suede-calfskin-turtoise-shell-effect-plexi-gold-tone-metal/)
- [Dior US Hobo 分类](https://www.dior.com/en_us/fashion/discover/hobo-bag-for-women)
- [Dior US Handbags 分类](https://www.dior.com/en_us/fashion/womens-fashion/bags/handbags)
