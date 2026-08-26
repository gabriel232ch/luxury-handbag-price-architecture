# Current competitor handbag pricing collection log

Observation timestamp used for this collection: `2026-08-15T20:20:39+08:00` (Asia/Shanghai).

## Sources and method

- Dior FR category: https://www.dior.com/fr_fr/fashion/mode-femme/sacs/tous-les-sacs
- Dior US category: https://www.dior.com/en_us/fashion/womens-fashion/bags/all-the-bags
- Louis Vuitton FR category: https://fr.louisvuitton.com/fra-fr/femme/sacs-a-main/nouveautes-sacs-a-main/_/N-t9zmtum-bl14e0mqi
- Louis Vuitton US category: https://us.louisvuitton.com/eng-us/women/handbags/all-handbags/_/N-tfr7qdp
- Hermès FR category: https://www.hermes.com/fr/fr/category/maroquinerie/sacs-et-pochettes/sacs-et-pochettes-femme/
- Hermès US category: https://www.hermes.com/us/en/category/leather-goods/bags-and-clutches/womens-bags-and-clutches/

Accepted records were collected from official localized rendered pages and use `browser_rendered_web_dom`. No manual records were used. Raw observations are preserved in `raw/all_raw_data.jsonl`; normalized observations are in `clean/`.

## Brand coverage

### Dior
- category pages used: official localized FR and US handbag pages listed above
- product URLs discovered / accepted: 40
- unique references discovered / accepted: 20
- accepted France observations: 20
- accepted US observations: 20
- numeric prices: 32
- price-upon-request records: 0
- France–US matched SKUs: 13
- automatically collected observations: 40
- manually collected observations: 0
- unresolved observations: 8
- main limitation: several US product pages exposed product details but not a current numeric price in the rendered response; those rows remain `price_status=unresolved`.

### Louis Vuitton
- category pages used: official localized FR and US handbag pages listed above
- product URLs discovered / accepted: 40
- unique references discovered / accepted: 35
- accepted France observations: 20
- accepted US observations: 20
- numeric prices: 40
- price-upon-request records: 0
- France–US matched SKUs: 5
- automatically collected observations: 40
- manually collected observations: 0
- unresolved observations: 0
- main limitation: the France and US assortments were not identical; exact-reference matching is limited to references observed in both localized assortments.

### Hermès
- category pages used: official localized FR and US handbag pages listed above
- product URLs discovered / accepted: 40
- unique references discovered / accepted: 37
- accepted France observations: 20
- accepted US observations: 20
- numeric prices: 40
- price-upon-request records: 0
- France–US matched SKUs: 3
- automatically collected observations: 40
- manually collected observations: 0
- unresolved observations: 0
- main limitation: the Hermès category included stale product links returning 404; those failures are recorded in `errors/errors.jsonl`, while resolvable official product pages were retained.

## QA checks

- One row per brand × market × official reference × observation timestamp.
- France rows use EUR; United States rows use USD.
- Numeric prices are positive and were retained only when displayed on the official localized product page or its official category/product response.
- Every accepted row contains an official localized source URL and observation timestamp.
- Final France–US matches use exact official reference equality and are marked high confidence.
- No strategy interpretation, cross-brand equivalence, geographic premium, averages, or price-ladder calculations were performed.

## Error file

Recorded collection errors / limitations: 12. See `errors/errors.jsonl` for stage, type, message, URL, and reference where known.
