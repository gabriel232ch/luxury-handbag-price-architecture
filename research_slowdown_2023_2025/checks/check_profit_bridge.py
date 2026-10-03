"""Read-only checks of manually transcribed consolidated USD accounts.

Costs are positive inputs; exceptional items are net charges (negative = gain).
Staff/DA/exceptional notes overlap functional costs and MUST NOT be added to them.
Selected DA follows the company's EBITDA reconciliation, NOT all IFRS depreciation.
"""
import csv
from decimal import Decimal as D
from pathlib import Path

root = Path(__file__).resolve().parents[1] / 'data'
with (root / 'chanel_profit_bridge_inputs.csv').open(encoding='utf-8', newline='') as f:
    records = list(csv.DictReader(f))
assert len(records) == 3 and len({r['fiscal_year'] for r in records}) == 3
assert all(None not in r and None not in r.values() for r in records)
rows = {int(r['fiscal_year']): {k: D(v) for k, v in r.items() if k.endswith('_usd_m') and v} for r in records}
def close(a, b):
    assert abs(a-b) <= D('0.1'), (a, b)
def expenses(r):
    return sum(r[k] for k in ('distribution_usd_m', 'advertising_promotion_demonstration_usd_m', 'selling_general_administrative_usd_m'))
for year, r in rows.items():
    close(r['revenue_usd_m'] - r['cost_of_sales_usd_m'], r['gross_profit_usd_m'])
    close(r['gross_profit_usd_m'] - expenses(r), r['operating_profit_usd_m'])
    close(r['operating_profit_usd_m'] + r['finance_income_usd_m'] - r['finance_cost_usd_m'] + r['equity_income_usd_m'] - r['income_tax_usd_m'], r['profit_before_nci_usd_m'])
    close(r['profit_before_nci_usd_m'] - r['nci_usd_m'], r['profit_for_year_usd_m'])
    if year != 2023:
        close(r['operating_profit_usd_m'] + r['exceptional_net_charge_usd_m'] + r['selected_da_usd_m'], r['adjusted_ebitda_usd_m'])
    print(year, 'gross margin', round(r['gross_profit_usd_m']/r['revenue_usd_m']*100, 2), 'operating margin', round(r['operating_profit_usd_m']/r['revenue_usd_m']*100, 2))
for year in (2024, 2025):
    a, b = rows[year-1], rows[year]
    delta = {k: b[k]-a[k] for k in ('revenue_usd_m', 'cost_of_sales_usd_m', 'gross_profit_usd_m', 'distribution_usd_m', 'advertising_promotion_demonstration_usd_m', 'selling_general_administrative_usd_m', 'operating_profit_usd_m', 'staff_cost_usd_m')}
    bridge = delta['gross_profit_usd_m'] - delta['distribution_usd_m'] - delta['advertising_promotion_demonstration_usd_m'] - delta['selling_general_administrative_usd_m']
    close(bridge, delta['operating_profit_usd_m'])
    print(year, delta)
a, b = rows[2024], rows[2025]
close((b['adjusted_ebitda_usd_m']-a['adjusted_ebitda_usd_m']) - (b['exceptional_net_charge_usd_m']-a['exceptional_net_charge_usd_m']) - (b['selected_da_usd_m']-a['selected_da_usd_m']), b['operating_profit_usd_m']-a['operating_profit_usd_m'])
net_finance_delta = (b['finance_income_usd_m']-b['finance_cost_usd_m']) - (a['finance_income_usd_m']-a['finance_cost_usd_m'])
close(net_finance_delta, D('-576.9'))
close(b['profit_before_nci_usd_m']-a['profit_before_nci_usd_m'], D('-486.0'))
print('2025 net finance change', net_finance_delta, '; profit before NCI change -486.0m')
print('PASS: three income statements, two operating bridges, two EBITDA reconciliations and net-profit bridge; rounding tolerance USD 0.1m.')
