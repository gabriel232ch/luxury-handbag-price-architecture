"""Reported-USD channel bridge; not category, same-store or sell-through data."""
import csv
from decimal import Decimal as D
from pathlib import Path

root = Path(__file__).resolve().parents[1] / 'data'
with (root/'chanel_channel_panel.csv').open(encoding='utf-8', newline='') as f:
    records = list(csv.DictReader(f))
assert len(records) == 9 and len({(r['fiscal_year'],r['channel']) for r in records}) == 9
assert all(None not in r and None not in r.values() for r in records)
with (root/'chanel_profit_bridge_inputs.csv').open(encoding='utf-8', newline='') as f:
    totals = {int(r['fiscal_year']): D(r['revenue_usd_m']) for r in csv.DictReader(f)}
rows = {}
for year,total in totals.items():
    rows[year] = {r['channel']:D(r['revenue_usd_m']) for r in records if int(r['fiscal_year'])==year}
    assert set(rows[year]) == {'Retail','Wholesale','Other'}
    assert sum(rows[year].values())==total
    print(year,'retail share',round(rows[year]['Retail']/total*100,2))
for year in (2024,2025):
    delta = {c:rows[year][c]-rows[year-1][c] for c in rows[year]}
    assert sum(delta.values())==totals[year]-totals[year-1]
    print(year,'USDm bridge',delta)
    for c in ('Retail','Wholesale'):
        print(c,'growth',round(delta[c]/rows[year-1][c]*100,2),'net-change contribution',round(delta[c]/sum(delta.values())*100,2))
assert rows[2025]['Retail']-rows[2023]['Retail']==D('-517.3')
assert rows[2025]['Wholesale']-rows[2023]['Wholesale']==D('40.9')
print('2025 retail recovery of 2024 loss',round(D('435.1')/D('952.4')*100,1))
print('PASS: 9 unique rows, 3 annual totals and 2 channel bridges reconcile exactly.')

with (root/'product_timing_ledger.csv').open(encoding='utf-8', newline='') as f:
    activities=list(csv.DictReader(f))
assert len({r['activity_id'] for r in activities})==len(activities)
assert all(None not in r and None not in r.values() for r in activities)
blazy = next(r for r in activities if r['activity_id']=='LS-A07')
assert blazy['communication_period']=='2025-10' and blazy['availability_period']=='2026-03'
assert blazy['fy2025_product_sales_eligible']=='no'
print('PASS: activity IDs unique, precision/availability explicit, Blazy product-sales exclusion retained.')
