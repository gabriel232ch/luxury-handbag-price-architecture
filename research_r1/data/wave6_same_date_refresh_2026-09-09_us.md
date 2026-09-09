# Wave 6 四品牌同日刷新（2026-09-09，美国站）

本文件对应获授权的下一步采集：在同一观察日重新打开 Chanel、Hermès、Louis Vuitton 和 Dior 的官方美国站详情页，并把结果写入独立的 2026-09-09 快照。该快照不覆盖、也不并入 2026-09-08 的主比较面板。

## 本轮结果

- 共 8 行：Chanel 2 行、Hermès 1 行、Louis Vuitton 3 行、Dior 2 行。
- Chanel：CHANEL 22 Small（AS3260）与 CHANEL 25 Small（AS5293）均能核验参考号、价格、皮革材质、Small 标签和数值尺寸，但页面只显示 Contact Us/预约，没有披露 regular/season 标记。
- Hermès：Videpoches（H087987CK10）能核验价格、Add to cart、Togo calfskin、肩背/斜挎方式、尺寸和参考号；产品页没有命名尺寸，因此保留 `unknown_size`，并按 `crossbody` 独立隔离，不塞进 hobo 单元。
- Louis Vuitton：Low Key Hobo PM（M25354）、CarryAll PM（M47180）和 Coussin Hobo MM（M12068）均有明确尺寸标签、皮革材质、价格和数值尺寸；页面没有可核验的命名 regular/season 状态，所以保留 `not_disclosed`。
- Dior：Medium Dior Bobby（M9319UMOL_M900）当前可 Add to Cart，页面明确 hobo、Medium、calfskin、价格和尺寸，但没有命名季节标记；Small Dior Toujours（M2867PDUN_M18S）明确标为 Autumn-Winter 2026-2027 Fashion Show，且 Sold out online，因此标为 `seasonal_excluded`，单独隔离。

## 证据和字段规则

所有行的 `observed_at` 与 `source_effective_date` 都是 `2026-09-09`。英寸尺寸按 2.54 换算并四舍五入到 0.1 cm；Dior 页面同时给出 cm 与 inch，保留页面 cm 作为标准化值。`regular_special` 只有在官方页面出现明确命名季节/系列标记时才赋值；“edited this season”等非命名措辞不推断为季节款。

官方来源：

- Chanel AS3260：<https://www.chanel.com/us/fashion/p/AS3260B1905994305/chanel-22-small-handbag-shiny-calfskin-gold-tone-metal/>
- Chanel AS5293：<https://www.chanel.com/us/fashion/p/AS5293B2030494305/chanel-25-small-handbag-grained-calfskin-gold-tone-metal/>
- Hermès H087987CK10：<https://www.hermes.com/us/en/product/hermes-videpoches-bag-H087987CK10/>
- Louis Vuitton M25354：<https://us.louisvuitton.com/eng-us/products/low-key-hobo-pm-h31-nvprod5580029v/M25354>
- Louis Vuitton M47180：<https://us.louisvuitton.com/eng-us/products/carryall-pm-monogram-empreinte-nvprod3990011v/M47180>
- Louis Vuitton M12068：<https://us.louisvuitton.com/eng-us/products/coussin-hobo-mm-h32-nvprod5900076v/M12068>
- Dior M9319UMOL_M900：<https://www.dior.com/en_us/fashion/products/M9319UMOL_M900>
- Dior M2867PDUN_M18S：<https://www.dior.com/en_us/fashion/products/M2867PDUN_M18S>

本轮仍然只是证据层刷新，尚未进行 2026-09-09 的配对审计、样本门槛判断或价格比较。下一步应在获得授权后，对该快照单独运行同市场、同日期、同包型、同尺寸、同材质及样本量门槛审计。
