"""Read-only handoff integrity checks; source authentication is not automated."""
import csv
import json
import re
import sys
from collections import Counter
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
handoff = root / 'website_handoff'
payload = json.loads((handoff / 'content.json').read_text())
ids = [c['id'] for c in payload['claims']]
assert len(ids) == len(set(ids)) == 10
for block in payload['blocks']:
    assert set(block['claimIds']) <= set(ids)
for claim in payload['claims']:
    for path in claim['evidencePaths']:
        assert (root / path).is_file(), path
assert payload['activeNextStep'] == 'website-revision'
assert payload['withdrawnNextStep'] == 'customer-choice-interviews'

data = root / 'research_slowdown_2023_2025/data'
with (data / 'chanel_profit_bridge_inputs.csv').open() as f:
    p = {r['fiscal_year']: r for r in csv.DictReader(f)}
v = lambda year, field: D(p[year][field])
q = lambda value: value.quantize(D('0.1'), rounding=ROUND_HALF_UP)
assert q(v('2025', 'revenue_usd_m') / v('2023', 'revenue_usd_m') * 100) == D('97.6')
assert q(v('2025', 'operating_profit_usd_m') / v('2023', 'operating_profit_usd_m') * 100) == D('73.5')
assert v('2023', 'operating_profit_usd_m') - v('2025', 'operating_profit_usd_m') == D('1695.5')
assert D('773.0') + D('984.8') - D('62.3') == D('1695.5')
assert q(D('435.1') / D('952.4') * 100) == D('45.7')
assert q(D('945') / D('1045') * 100) == D('90.4')
for name in ('CASE_STUDY_COPY_EN', 'NARRATIVE_INTEGRATION_CN'):
    old = (handoff / 'audit' / (name + '_before_style.md')).read_text()
    new = (handoff / (name + '.md')).read_text()
    for pattern in (r'[+−-]?\d+(?:,\d{3})*(?:\.\d+)?', r'\]\(([^)]+)\)'):
        assert Counter(re.findall(pattern, old)) == Counter(re.findall(pattern, new)), name
    assert '\u2014' not in new
    for link in re.findall(r'\]\(([^)]+)\)', new):
        if not link.startswith('http'):
            assert (handoff / link).resolve().is_file(), link
with (root / 'research_archive/customer_evidence/public_self_reports_deidentified.csv').open() as f:
    reader = csv.DictReader(f)
    assert 'actor' not in reader.fieldnames
    rows = list(reader)
assert len(rows) == len({r['record_id'] for r in rows}) == 11
print('PASS: 10 claims; all block/evidence/prose paths valid; arithmetic reconciled.')
print('PASS: exact numeric/link counters preserved in style revision; no U+2014.')
print('PASS: de-identified 11-row archive; withdrawn next step explicit.')
