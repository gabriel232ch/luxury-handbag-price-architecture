# Wave 2 Hobo 候选核验日志（2026-09-08，美国站）

## 本步范围

本步只核验 `US|hobo|small|leather` 的官方美国站候选，不把 2026-09-08 新行并入 2026-09-07 主面板，也不重跑配对审计。

## 核验结果

- Chanel `AS6411-B24762-U8389`：官网明确标为 **Métiers d'art 2026 Small Hobo Bag**，USD 8,200，Lambskin，7.1 × 11.4 × 3.1 in（约 18.0 × 29.0 × 7.9 cm）。它满足包型、Small、皮革和数值价格字段，但明确是季节款，只能进入季节敏感性候选，不能进入常规主文。
- Chanel `AS6570-B25732-94305`：官网明确标为 **Fall Winter 2026 Pre-Collection Hobo Handbag**，USD 6,200，Grained Calfskin，8.3 × 11.8 × 3.5 in（约 21.1 × 30.0 × 8.9 cm）。页面没有 Small 标签，故保留 `unknown_size`，不进入 Small 单元。
- Dior `S3202UDBB_M900`：官网为 Diorstar Hobo Bag with Chain，USD 2,850，Black Macrocannage Lambskin，22 × 14.5 × 10 cm。页面没有 Small 标签，保留 `unknown_size`。
- Dior `S3202PNIO_M900`：官网为 Diorstar Hobo Bag with Chain，USD 2,850，Black Macrocannage Crinkled Calfskin，22 × 14.5 × 10 cm。页面没有 Small 标签，保留 `unknown_size`。

当前 Dior 官方 Hobo 分类页列出的 Small Hobo 仍主要是已有的 Dior Toujours 变体；本步没有找到可同时新增、明确标 Small、且不重复已有参考号的第二个独立 Dior 小号 Hobo 配置。因此不能把 Diorstar 的尺寸或容量描述推断成 Small。

## 隔离与门槛决定

- 新增可审计候选：4 条；其中 1 条满足 `hobo/small/leather` 属性，但为显式季节款。
- 正式主文新增合格行：0 条。Chanel 的 AS6411 被 `seasonal_excluded`；AS6570 和两条 Diorstar 被 `unknown_size` 阻断。
- 现有 2026-09-07 主面板、四品牌快照和配对输出均未修改。

## 官方来源

- [Chanel AS6411 Small Hobo Bag](https://www.chanel.com/us/fashion/p/AS6411B24762U8389/small-hobo-bag-lambskin-gold-tone-metal/)
- [Chanel AS6570 Hobo Handbag](https://www.chanel.com/us/fashion/p/AS6570B2573294305/hobo-handbag-grained-calfskin-gold-tone-metal/)
- [Diorstar S3202UDBB_M900](https://www.dior.com/en_us/fashion/products/S3202UDBB_M900)
- [Diorstar S3202PNIO_M900](https://www.dior.com/en_us/fashion/products/S3202PNIO_M900)
- [Dior US Hobo category](https://www.dior.com/en_us/fashion/discover/hobo-bag-for-women)

## 下一步

下一步应在同一 2026-09-08 快照中处理“明确 Small 标签”的缺口：继续追踪 Chanel 历史/当前 Small Hobo 页面是否能取得完整美国价格与尺寸，同时从 Dior 官方目录继续寻找带明确 Small 标签的非-Toujours Hobo；若仍只有 unknown-size 或季节款，Wave 2 应保留为方向性、不得升级主文。
