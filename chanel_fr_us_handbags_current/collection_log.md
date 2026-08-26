# Chanel France / United States handbags — current collection log

## Scope

- Brand: CHANEL
- Category: Handbags
- Markets: France and United States
- Grain: one official SKU/reference × one market × one observation timestamp
- Observation timestamp: `2026-08-15T19:20:31+08:00`
- Current prices only; no historical or resale prices collected.

## Acquisition

- Discovery sources: official Chanel France classic-handbag and shopping/bowling category pages; official Chanel United States classic-handbag and shopping/bowling category pages.
- Detail sources: individual official Chanel product pages reached from the category listings.
- Runtime: Python 3.12.14; Crawlee 1.9.1; Playwright 1.62.0.
- Methods used: official category-page discovery plus browser-rendered official page DOM extraction (`extraction_method = browser_rendered_web_dom`).
- Playwright dependency check passed, but Chromium launch failed locally because of a macOS sandbox permission error. Direct HTTP DNS was also unavailable. The permitted browser-rendered web route was used instead; no CAPTCHA bypass, proxy rotation, stealth, credentials, or access-control circumvention was used.

## Counts

- Product URLs discovered: 42 candidate market-specific detail URLs (21 references × 2 markets); 41 resolved and 1 unresolved.
- Unique SKUs discovered: 21
- Records attempted: 42
- Accepted observations: 41
- France accepted observations: 20
- US accepted observations: 21
- Exact France-US matched SKUs: 20
- Automatically extracted observations: 41
- Manually extracted observations: 0
- Unresolved observations: 1

## Limitations

- The France detail page for reference `AS6200-B25749-UD596` timed out in the browser-rendered fetch after being observed on the official France category page. It is excluded from accepted France observations and matches, and is recorded in `errors.jsonl`.
- Chanel product pages expose a contact CTA rather than an explicit stock quantity in the collected view. `availability` is normalized to `contact_us`; original CTA text is preserved in `raw_data.jsonl`.
- Pages showing “Price upon request” retain a blank numeric price and blank currency; the original price-status string is preserved in raw data.

## Outputs

- [`raw_data.jsonl`](./raw_data.jsonl)
- [`clean_data.csv`](./clean_data.csv)
- [`errors.jsonl`](./errors.jsonl)
- [`matched_skus.csv`](./matched_skus.csv)
- [`collection_log.md`](./collection_log.md)
