# Financial & Business Performance

This directory is the auditable financial evidence layer for the Phase 2 Chanel analysis.

- `raw/`: source observations as captured from official releases.
- `clean/`: normalized financial panel and reporting-scope matrix.
- `sources/`: first-party source registry with URL, publication date and page / section.
- `calculations/`: Chanel performance, Hermès benchmark, LVMH Fashion & Leather Goods benchmark, price architecture diagnostics and calculation registries.
- `logs/`: conflict, missingness, build and release-validation logs.

The panel preserves entity grain, fiscal period, currency and reported versus constant-currency basis. Conflicting observations are retained; unavailable metrics are not estimated.
