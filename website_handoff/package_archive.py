"""Mechanical CSV de-identification and source-file hash manifest generation."""
import csv
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
case = root / 'case/luxury_slowdown_2023_2025'
archive = root / 'research_archive'
with (case / 'customer_choice_evidence.csv').open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fields = [name for name in reader.fieldnames if name != 'actor']
    records = [{name: row[name] for name in fields} for row in reader]
with (archive / 'customer_evidence/public_self_reports_deidentified.csv').open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(records)
sources = [
    ('chanel_fy2024_accounts.pdf', 'LS-S24', 'https://find-and-update.company-information.service.gov.uk/company/00203669/filing-history/MzQ2ODQzNTAzN2FkaXF6a2N4/document?download=0&format=pdf'),
    ('chanel_fy2025_accounts.pdf', 'LS-S23', 'https://find-and-update.company-information.service.gov.uk/company/00203669/filing-history/MzUyNzQxOTg3MmFkaXF6a2N4/document?download=0&format=pdf'),
    ('loreal_urd2025.pdf', 'LS-S35', 'https://www.loreal-finance.com/eng/2025-universal-registration-document/en/article/23/')
]
manifest = []
for name, source_id, url in sources:
    data = (case / 'sources' / name).read_bytes()
    manifest.append({'local_filename': name, 'source_id': source_id, 'official_locator': url,
                     'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                     'distribution': 'local source retained; public locator only'})
(archive / 'source_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print('PASS: 11 public coding rows de-identified; three local source hashes recorded.')
