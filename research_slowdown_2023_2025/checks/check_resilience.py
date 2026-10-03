"""Read-only checks and FY2023-based calculations; never rewrites seed data."""
import csv
import math
from pathlib import Path

data_dir = Path(__file__).resolve().parents[1] / 'data'
with (data_dir / 'resilience_panel.csv').open(newline='', encoding='utf-8') as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
assert len(rows) == 12
assert all(None not in row and None not in row.values() for row in rows), 'Malformed CSV'
assert len({(r['entity'], r['scope'], r['fiscal_year']) for r in rows}) == 12
for row in rows:
    assert row['source_ids'] and row['money_unit'] == 'million'
    for field in ('revenue', 'operating_profit', 'margin_pct', 'comparable_growth_pct'):
        assert math.isfinite(float(row[field]))
    assert abs(float(row['operating_profit']) / float(row['revenue']) * 100 - float(row['margin_pct'])) < 0.12

print('Entity | Revenue index 2025 (2023=100) | Profit index | 2025 profit vs 2023')
expected = {'Chanel': (97.6, 73.5), 'Hermes': (119.2, 116.3), 'LVMH': (89.6, 78.5), 'Gucci': (60.7, 29.6)}
for entity, targets in expected.items():
    series = sorted([r for r in rows if r['entity'] == entity], key=lambda r: r['fiscal_year'])
    assert [r['fiscal_year'] for r in series] == ['2023', '2024', '2025']
    assert len({r['currency'] for r in series}) == 1
    assert len({r['scope'] for r in series}) == 1
    indexes = tuple(round(float(series[-1][field]) / float(series[0][field]) * 100, 1) for field in ('revenue', 'operating_profit'))
    assert indexes == targets, (entity, indexes)
    change = (float(series[-1]['operating_profit']) - float(series[0]['operating_profit'])) / float(series[0]['operating_profit']) * 100
    print(f'{entity} | {indexes[0]:.1f} | {indexes[1]:.1f} | {change:+.1f}%')
    if series[-1]['free_cash_flow']:
        cash_index = float(series[-1]['free_cash_flow']) / float(series[0]['free_cash_flow']) * 100
        print(f'  Within-series cash index: {cash_index:.1f}; basis: {series[-1]["cash_basis"]}')
    if series[-1]['investment']:
        print('  Investment/revenue: ' + ' -> '.join(f'{float(r["investment"])/float(r["revenue"])*100:.1f}%' for r in series))
print('PASS: 12 unique observations; numeric, margin, currency, scope and index checks.')
