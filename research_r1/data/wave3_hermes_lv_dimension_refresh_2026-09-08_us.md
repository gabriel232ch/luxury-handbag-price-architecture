# Wave 3 Hermès / Louis Vuitton dimension refresh — US, 2026-09-08

## Purpose

This file is the second, separate refresh leg of Wave 3. It records same-date official US detail-page observations for three Hermès and three Louis Vuitton configurations after the Chanel dimension refresh. It is a top-up evidence file; it does not replace the 2026-09-07 main panel and it does not promote a cross-brand pair by itself.

## What was captured

- Hermès: H086717CKAC (Neo Garden Voyage 41), H089099CAAA (Neo Double Sens 35), and H085054CK37 (So Medor).
- Louis Vuitton: M2A323 (Low Key Hobo PM), M2A467 (Neverfull Inside Out BB), and M46203 (CarryAll PM).
- All six rows have a numeric US price and numeric inch dimensions from an official US product detail page. Inch values were converted to centimeters at 2.54 cm per inch and rounded to one decimal place.
- All six rows are marked `available_online` because the observed official pages were current product pages with an online purchase path at refresh time. This is a snapshot availability status, not an enduring inventory claim.
- None of the six pages exposed a reliable regular-versus-seasonal marker, so `regular_special=not_disclosed` and `scope_status=status_pending` are retained.
- Size labels remain the brand labels shown by the products. The independent numeric dimension audit has not yet been run; `pairing_readiness=conditional_regular_special_review` is therefore provisional.

## Excluded official pages in this leg

Hermès H085414CKAO (Herbag Zip 20) and H082901CCCA (Bolide 1923-25 verso) were not added to this same-date top-up because their official US pages explicitly reported that the products were no longer available. Their previously observed reference, price, material and dimensions remain in the competitor product master and historical panel, but they should not be treated as currently purchasable refresh rows.

## Why this remains separate from the main panel

The refresh provides comparable numeric dimensions and current prices for the next audit. It does not yet establish same-market, same-date, same-bag-type, same-size, same-material intersections with Chanel. The next step is a deterministic dimension intersection audit using the Wave 3 rule: compare sorted numeric axes, require both rows to have numeric dimensions, and allow no more than `max(2 cm, 10%)` per axis. Only units that also pass regular/seasonal and sample-size gates can enter the main comparison.

## Official sources

- Hermès H086717CKAC: https://www.hermes.com/us/en/product/neo-garden-voyage-41-bag-H086717CKAC/
- Hermès H089099CAAA: https://www.hermes.com/us/en/product/neo-double-sens-35-bicolor-bag-H089099CAAA/
- Hermès H085054CK37: https://www.hermes.com/us/en/product/so-medor-bag-H085054CK37/
- Louis Vuitton M2A323: https://us.louisvuitton.com/eng-us/products/low-key-hobo-pm-h31-nvprod5580029v/M2A323
- Louis Vuitton M2A467: https://us.louisvuitton.com/eng-us/products/neverfull-bandouliere-inside-out-bb-h33-nvprod5770174v/M2A467
- Louis Vuitton M46203: https://us.louisvuitton.com/eng-us/products/carryall-pm-monogram-nvprod3770016v/M46203

