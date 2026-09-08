# 2026-09-07 范围隔离清单

- 输入：Chanel `product_master.csv`（补充快照）和三品牌 `product_master_competitors_2026-09-07_us.csv`（同日美国快照）。
- 总行数：72。
- `scope_status` 计数：{'seasonal_excluded': 2, 'unknown_size': 14, 'status_pending': 51, 'sensitivity_only': 5}。
- 隔离原因计数：{'explicit_seasonal_collection': 2, 'size_label_unknown': 15, 'regular_special_not_disclosed': 70, 'woc_or_small_leather_goods': 5}。

规则：WOC 和小皮具仅保留为 sensitivity；明确季节款排除常规核心；尺寸为 `unknown` 的行阻断严格配对；`regular_special=not_disclosed` 不被猜成常规款，先标记为待核验。Dior 的数值尺寸缺失另标为 `conditional_dimension_review`，不在本步升级为主文比较。

本文件只完成范围隔离，不计算价格差、排名或竞品替代关系。下一步才使用 `pairing_readiness` 和同市场/同日期筛选重建配对审计。
