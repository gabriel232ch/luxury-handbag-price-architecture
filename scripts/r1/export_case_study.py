#!/usr/bin/env python3
"""Export a static, source-linked candidate case-study package for R1."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
R1 = ROOT / "research_r1"
EXPORT = R1 / "export"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def esc(value: object) -> str:
    text = str(value)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def svg_document(title: str, subtitle: str, body: str, width: int = 1000, height: int = 560) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{esc(title)}</title><desc id="desc">{esc(subtitle)}</desc>
  <rect width="100%" height="100%" fill="#f8f6f1"/>
  <style>text{{font-family:Arial,sans-serif;fill:#24221e}} .muted{{fill:#6d665c;font-size:14px}} .axis{{stroke:#aaa397;stroke-width:1}} .grid{{stroke:#ded9cf;stroke-width:1}} .label{{font-size:16px}} .value{{font-size:14px;font-weight:600}}</style>
  <text x="54" y="48" font-size="25" font-weight="700">{esc(title)}</text>
  <text x="54" y="75" class="muted">{esc(subtitle)}</text>
  {body}
</svg>
'''


def landscape_svg(family_rows: list[dict[str, str]]) -> str:
    colors = {"Chanel": "#111111", "Hermès": "#b56b2a", "Louis Vuitton": "#6c4f37", "Dior": "#707070"}
    points = []
    rows = [r for r in family_rows if r["numeric_observations"] != "0"]
    vals = [float(r["p50_sample"]) for r in rows if r["p50_sample"]]
    lo, hi = 0, max(vals) * 1.1 if vals else 1
    x0, x1 = 180, 930
    y0, y1 = 130, 500
    for i, market in enumerate(("FR", "US")):
        subset = [r for r in rows if r["market"] == market]
        y = y0 + i * 185
        points.append(f'<text x="54" y="{y + 18}" class="label">{market} · {"EUR" if market == "FR" else "USD"}</text>')
        points.append(f'<line x1="{x0}" y1="{y + 30}" x2="{x1}" y2="{y + 30}" class="axis"/>')
        for tick in range(0, 6):
            value = hi * tick / 5
            x = x0 + (x1 - x0) * value / hi
            points.append(f'<line x1="{x:.1f}" y1="{y + 30}" x2="{x:.1f}" y2="{y + 160}" class="grid"/>')
            points.append(f'<text x="{x:.1f}" y="{y + 182}" text-anchor="middle" class="muted">{value:,.0f}</text>')
        for j, brand in enumerate(("Chanel", "Hermès", "Louis Vuitton", "Dior")):
            brand_rows = [r for r in subset if r["brand"] == brand and r["p50_sample"]]
            if not brand_rows:
                continue
            value = sum(float(r["p50_sample"]) for r in brand_rows) / len(brand_rows)
            x = x0 + (x1 - x0) * value / hi
            cy = y + 70 + j * 20
            points.append(f'<circle cx="{x:.1f}" cy="{cy}" r="6" fill="{colors[brand]}"/><text x="{x + 12:.1f}" y="{cy + 5}" class="label">{esc(brand)}</text>')
    return svg_document("Price Landscape", "Family medians shown on separate local-currency axes; observed sample only.", "\n".join(points), height=560)


def ladder_svg(ladder: list[dict[str, str]], family_rows: list[dict[str, str]]) -> str:
    body = []
    colors = {"Classic 11.12": "#191817", "Small Classic": "#191817", "Mini Classic": "#a64c3b", "Shopping Bag": "#4d6b67", "Bowling Bag": "#4d6b67"}
    for idx, market in enumerate(("FR", "US")):
        y = 125 + idx * 190
        row = next(r for r in ladder if r["market"] == market)
        fams = [r for r in family_rows if r["brand"] == "Chanel" and r["market"] == market and r["p50_sample"]]
        vals = [float(r["p50_sample"]) for r in fams]
        lo, hi = 0, max(vals) * 1.12 if vals else 1
        x0, x1 = 190, 930
        body.append(f'<text x="54" y="{y + 20}" class="label">{market} · {"EUR" if market == "FR" else "USD"}</text>')
        body.append(f'<line x1="{x0}" y1="{y + 55}" x2="{x1}" y2="{y + 55}" class="axis"/>')
        for fidx, fam in enumerate(["Mini Classic", "Shopping Bag", "Bowling Bag", "Classic 11.12", "Small Classic"]):
            fam_row = next((r for r in fams if r["family"] == fam), None)
            if not fam_row:
                continue
            value = float(fam_row["p50_sample"])
            x = x0 + (x1 - x0) * value / hi
            cy = y + 95 + fidx * 22
            body.append(f'<circle cx="{x:.1f}" cy="{cy}" r="7" fill="{colors[fam]}"/><text x="{x + 13:.1f}" y="{cy + 5}" class="label">{esc(fam)} · {value:,.0f}</text>')
        body.append(f'<text x="54" y="{y + 176}" class="muted">Observed gap {esc(row["observed_gap"])} {esc(row["currency"])} · median distance {esc(row["median_distance"])} · ratio {esc(row["relative_ratio"])}</text>')
    return svg_document("The Price Ladder", "Chanel family medians expand the brand point into an observed ladder.", "\n".join(body))


def history_svg(rows: list[dict[str, str]]) -> str:
    body = []
    if not rows:
        body.append('<text x="54" y="140" class="label">No aligned history available.</text>')
    else:
        vals = [float(r["absolute_gap"]) for r in rows]
        lo, hi = min(vals) * .9, max(vals) * 1.1
        x0, x1, y0, y1 = 150, 900, 170, 430
        body.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" class="axis"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" class="axis"/>')
        coords = []
        for i, row in enumerate(rows):
            x = x0 + (x1 - x0) * (i / max(1, len(rows) - 1))
            value = float(row["absolute_gap"])
            y = y1 - (y1 - y0) * (value - lo) / max(1, hi - lo)
            coords.append(f"{x:.1f},{y:.1f}")
            body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#9b4f3e"/><text x="{x:.1f}" y="{y - 15:.1f}" text-anchor="middle" class="value">{esc(row["absolute_gap"])}</text><text x="{x:.1f}" y="{y1 + 28}" text-anchor="middle" class="label">{esc(row["observed_year"])}</text>')
        if len(coords) > 1:
            body.append(f'<polyline points="{" ".join(coords)}" fill="none" stroke="#9b4f3e" stroke-width="3"/>')
        body.append('<text x="54" y="140" class="muted">Absolute median distance · Chanel France · common observed years only · EUR</text>')
    return svg_document("Moving Together", "Fixed Chanel France lineages; missing years are not interpolated.", "\n".join(body))


def main() -> int:
    validation_path = R1 / "outputs" / "validation.json"
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    if validation.get("status") == "fail":
        raise SystemExit("Refusing export because validation status is fail")
    ladder = read_csv(R1 / "outputs" / "chanel_ladder.csv")
    family = read_csv(R1 / "outputs" / "brand_family_summary.csv")
    aligned = read_csv(R1 / "outputs" / "aligned_history.csv")
    claims = read_csv(R1 / "claims.csv")
    source_rows = read_csv(R1 / "source_registry.csv")
    claim_ids = {row["claim_id"] for row in claims if row.get("publication_decision") != "exclude_from_core"}
    source_ids = {row["source_id"] for row in source_rows}

    scenes = {
        "price-landscape": {"id": "price-landscape", "title": "Price Landscape", "dataFile": "research_r1/outputs/brand_family_summary.csv", "figure": "research_r1/export/figures/price-landscape.svg", "markets": ["FR", "US"], "noJsEquivalent": True},
        "price-ladder": {"id": "price-ladder", "title": "The Price Ladder", "dataFile": "research_r1/outputs/chanel_ladder.csv", "supportingDataFile": "research_r1/outputs/brand_family_summary.csv", "figure": "research_r1/export/figures/price-ladder.svg", "markets": ["FR", "US"], "noJsEquivalent": True},
        "moving-together": {"id": "moving-together", "title": "Moving Together", "dataFile": "research_r1/outputs/aligned_history.csv", "figure": "research_r1/export/figures/moving-together.svg", "markets": ["FR"], "noJsEquivalent": True},
    }
    for scene in scenes.values():
        write_json(EXPORT / "scenes" / f"{scene['id']}.json", scene)
    (EXPORT / "figures" / "price-landscape.svg").write_text(landscape_svg(family), encoding="utf-8")
    (EXPORT / "figures" / "price-ladder.svg").write_text(ladder_svg(ladder, family), encoding="utf-8")
    (EXPORT / "figures" / "moving-together.svg").write_text(history_svg(aligned), encoding="utf-8")

    # Keep the candidate case-study package stable while a supplementary
    # snapshot is still outside the R1 baseline. Its sources remain in the
    # registry and will enter the export only when the supplement is merged.
    source_records = [{"source_id": row["source_id"], "name": row["source_name"], "url": row["source_url"], "quality": row["source_quality"], "effectiveDate": row["source_effective_date"]} for row in source_rows if not row["source_id"].startswith("SRC-SUPP-CH-")]
    case_study = {
        "schemaVersion": "luxury-case-study-1",
        "slug": "luxury-handbag-pricing-architecture",
        "language": "en",
        "researchVersion": "R1",
        "publication": "candidate",
        "noindex": True,
        "observationScope": {"markets": ["France", "United States"], "currencies": ["EUR", "USD"], "currentSnapshot": "2026-08-15", "acceptedCurrentObservations": 161, "numericCurrentObservations": 147, "note": "Observed official local list-price sample; not an assortment census or affordability measure."},
        "title": "The Architecture of Access — Chanel's Handbag Price Ladder in Context",
        "summary": "A source-linked study of visible Chanel entry, family steps and Classic anchors, with three brands as external coordinates.",
        "sections": [
            {"id": "open", "title": "Open", "summary": "The question and its observation boundary.", "paragraphs": ["How does Chanel present visible entry, family-level steps and the Classic high anchor in local official list-price observations?"], "claimIds": ["CLM-LADDER-FR", "CLM-LADDER-US"], "sceneIds": []},
            {"id": "context", "title": "Context", "summary": "Four brands on separate local price axes.", "paragraphs": ["Chanel is the focal case. Hermès, Louis Vuitton and Dior provide external coordinates; the panel is non-weighted and coverage differs by brand and market."], "claimIds": ["CLM-COVERAGE-DIOR-US"], "sceneIds": ["price-landscape"]},
            {"id": "architecture", "title": "Architecture", "summary": "A brand point expanded into family positions.", "paragraphs": ["Classic 11.12 and Small Classic form the Classic group. Mini Classic is an entry observation even though its name contains Classic; Shopping Bag and Bowling Bag are other core observations. Price-upon-request rows stay outside the numeric axis."], "claimIds": ["CLM-LADDER-FR", "CLM-LADDER-US"], "sceneIds": ["price-ladder"]},
            {"id": "evolution", "title": "Evolution", "summary": "Common observed years only.", "paragraphs": ["The Chanel France history panel compares fixed lineages without interpolating missing years. The values are product-line observations, mostly from secondary historical tables."], "claimIds": ["CLM-HISTORY-CHANEL-FR"], "sceneIds": ["moving-together"]},
            {"id": "interpretation", "title": "Interpretation", "summary": "Bounded findings and decision questions.", "paragraphs": ["If the visible distance survives de-variant sensitivity, verify the full SKU ladder and upgrade path. If it moves with family coverage, map the assortment before making a pricing decision."], "claimIds": ["CLM-LADDER-FR", "CLM-LADDER-US", "CLM-COVERAGE-DIOR-US"], "sceneIds": []},
            {"id": "afterlife", "title": "Afterlife", "summary": "Methods, sources and limitations.", "paragraphs": ["The candidate remains noindex and unpublished. All figures point to R1 outputs; Hermès Geta's 2023 France conflict remains excluded from the core narrative."], "claimIds": [], "sceneIds": []},
        ],
        "claims": [{"claimId": row["claim_id"], "text": row["claim_text"], "grade": row["evidence_grade"], "scope": row["scope"], "outputPath": row["output_path"], "limitation": row["limitation"]} for row in claims if row["claim_id"] in claim_ids],
        "sources": source_records,
        "scenes": list(scenes.values()),
    }
    # Contract checks before writing the public candidate.
    all_case_claims = {row["claimId"] for row in case_study["claims"]}
    for section in case_study["sections"]:
        if not set(section["claimIds"]).issubset(all_case_claims):
            raise SystemExit(f"section {section['id']} references a missing claim")
        if not set(section["sceneIds"]).issubset(scenes):
            raise SystemExit(f"section {section['id']} references a missing scene")
    if not source_ids:
        raise SystemExit("source registry is empty")
    write_json(EXPORT / "case-study.json", case_study)
    file_entries = []
    for path in sorted(EXPORT.rglob("*")):
        if path.is_file() and path.name != "manifest.json":
            file_entries.append({"path": str(path.relative_to(ROOT)), "sha256": sha256(path)})
    write_json(EXPORT / "manifest.json", {"schemaVersion": "luxury-case-study-manifest-1", "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"), "source_commit": git_sha(), "research_status": validation.get("status"), "files": file_entries})
    print(json.dumps({"status": validation.get("status"), "claims": len(case_study["claims"]), "scenes": len(scenes), "sources": len(source_records)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
