"""Reconcile reported-USD geography bridges; no constant-currency attribution."""
import csv
from pathlib import Path

root = Path(__file__).resolve().parents[1] / 'data'
with (root / 'chanel_regional_panel.csv').open(newline='', encoding='utf-8') as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == 9
assert len({(r['fiscal_year'], r['region']) for r in rows}) == 9
assert all(None not in r and None not in r.values() for r in rows)
expected_totals = {2023: 19744, 2024: 18699, 2025: 19269}
by_year = {}
for year, total in expected_totals.items():
    subset = {r['region']: int(r['revenue_usd_m']) for r in rows if int(r['fiscal_year']) == year}
    assert set(subset) == {'Europe', 'Asia_Pacific', 'Americas'}
    assert sum(subset.values()) == total
    by_year[year] = subset
    print(f'{year}: reconciled USD {total}m; shares ' + ', '.join(f'{region}={value/total*100:.1f}%' for region, value in subset.items()))
for year in (2024, 2025):
    movement = {region: value - by_year[year-1][region] for region, value in by_year[year].items()}
    assert sum(movement.values()) == expected_totals[year] - expected_totals[year-1]
    print(f'{year} reported-USD bridge: {movement}; total={sum(movement.values())}m')
assert by_year[2024]['Asia_Pacific'] - by_year[2023]['Asia_Pacific'] == -945
assert by_year[2025]['Europe'] - by_year[2024]['Europe'] == 378
assert by_year[2025]['Americas'] - by_year[2024]['Americas'] == 243
assert by_year[2025]['Asia_Pacific'] - by_year[2024]['Asia_Pacific'] == -51
print(f'2024 AP share of net decline: {945/1045*100:.1f}%')
print('PASS: 9 unique records; annual totals and two geography bridges reconcile exactly.')
print('Boundary: reported USD includes FX/scope/mix; regional sales do not identify customer nationality.')
