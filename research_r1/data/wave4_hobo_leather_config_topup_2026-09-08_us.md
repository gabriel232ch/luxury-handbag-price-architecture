# Wave 4 hobo + leather configuration top-up — US, 2026-09-08

## Purpose

This is a targeted expansion of the `US|hobo|leather` route after the Wave 3 audit found one directional Chanel–Louis Vuitton dimension candidate but only two Chanel families and one Louis Vuitton family in the cell. It records one additional Chanel family and three additional Louis Vuitton families. It is a top-up file and does not rewrite the 2026-09-07 main panel or rerun the pairing audit.

## Accepted rows

- **Chanel:** AS6617-B26218-94305, Small Hobo Bag, USD 5,200, 7.1 x 9.4 x 2.4 in (18.0 x 23.9 x 6.1 cm), calfskin. The official US page explicitly labels it Fall Winter 2026 Pre-Collection and exposes Contact Us/appointment rather than an online purchase control. It is therefore `seasonal_excluded` and `contact_only`.
- **Louis Vuitton:** M46725 Loop Hobo, USD 3,350, 15 x 10.2 x 3.9 in (38.1 x 25.9 x 9.9 cm), Monogram Empreinte cowhide leather. The page is a women’s handbag detail page, but no size label, regular/season marker or explicit stock control is visible; size remains `unknown` and availability `not_disclosed`.
- **Louis Vuitton:** M12068 Coussin Hobo MM, USD 5,350, 15 x 13 x 3.9 in (38.1 x 33.0 x 9.9 cm), calf leather. The page exposes the `MM` label and numeric dimensions, but no regular/season marker or explicit stock control; `regular_special=not_disclosed` and availability remain conservative.
- **Louis Vuitton:** M27937 Hobo Métis, USD 3,650, 13.8 x 12.8 x 3.9 in (35.1 x 32.5 x 9.9 cm), cowhide leather. Visible color controls show out-of-stock states and Notify Me; no size label or regular/season marker is visible. It remains `out_of_stock` and `unknown_size`.

## Status interpretation

The Chanel row is an explicit seasonal configuration and cannot increase the regular-core sample count. The three LV rows are distinct families, but two lack a named size and one is out of stock. The official LV pages did not expose a reliable regular-versus-seasonal marker, so `not_disclosed` is a source result rather than an access failure; it must not be converted to regular by inference.

## Collection method and limits

All four rows were read from official US product detail pages on 2026-09-08. Prices are USD list prices as displayed. Inch dimensions were converted using 2.54 cm per inch and rounded to one decimal place. The next step is to merge this top-up into a separate Wave 4 hobo audit, apply the same sorted-axis dimension rule, and recalculate independent-family and scope gates. No price comparison is computed in this collection step.

## Official sources

- Chanel AS6617: https://www.chanel.com/us/fashion/p/AS6617B2621894305/small-hobo-bag-calfskin-gold-tone-metal/
- Louis Vuitton M46725: https://us.louisvuitton.com/eng-us/products/loop-hobo-monogram-empreinte-nvprod4790052v/M46725
- Louis Vuitton M12068: https://us.louisvuitton.com/eng-us/products/coussin-hobo-mm-h32-nvprod5900076v/M12068
- Louis Vuitton M27937: https://us.louisvuitton.com/eng-us/products/hobo-metis-monogram-empreinte-nvprod7300029v/M27937

