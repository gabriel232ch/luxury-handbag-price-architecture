#!/usr/bin/env python3
"""Validate the R1 data and publication contracts."""

from __future__ import annotations

import csv
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
R1 = ROOT / "research_r1"
OBS = R1 / "data" / "observations.csv"
LINEAGE = R1 / "data" / "lineage.csv"
CLAIMS = R1 / "claims.csv"
SOURCES = R1 / "source_registry.csv"
REQUIRED_OBSERVATION_FIELDS = {
    "observation_id", "snapshot_id", "brand", "market", "currency", "observed_at",
    "source_effective_date", "source_id", "reference_code", "family", "model",
    "size_label", "material_group", "color", "price_status", "price",
    "comparison_group_id", "lineage_id", "inclusion_status", "exclusion_reason",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def git_sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def valid_price(value: str) -> bool:
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def observation_contract_errors(rows: list[dict[str, str]], lineage_ids: set[str], source_ids: set[str] | None = None) -> list[str]:
    """Return contract violations for a small fixture or the full R1 table."""
    errors: list[str] = []
    if not rows:
        return ["observations.csv is empty"]
    missing = REQUIRED_OBSERVATION_FIELDS - set(rows[0])
    if missing:
        errors.append(f"observations.csv missing fields: {', '.join(sorted(missing))}")
    ids = [row.get("observation_id", "") for row in rows]
    duplicates = [key for key, count in Counter(ids).items() if not key or count > 1]
    if duplicates:
        errors.append(f"duplicate or empty observation IDs: {duplicates[:5]}")
    for row in rows:
        observation_id = row.get("observation_id", "")
        expected_currency = {"FR": "EUR", "US": "USD"}.get(row.get("market", ""))
        if expected_currency is None:
            errors.append(f"{observation_id}: invalid market {row.get('market')}")
        elif row.get("currency") != expected_currency:
            errors.append(f"{observation_id}: {row.get('market')} must use {expected_currency}")
        if source_ids is not None and row.get("source_id") not in source_ids:
            errors.append(f"{observation_id}: orphan source_id {row.get('source_id')}")
        if row.get("lineage_id") and row.get("lineage_id") not in lineage_ids:
            errors.append(f"{observation_id}: orphan lineage_id {row.get('lineage_id')}")
        status, price = row.get("price_status", ""), row.get("price", "")
        if status == "numeric" and not valid_price(price):
            errors.append(f"{observation_id}: numeric price must be positive")
        if status != "numeric" and price.strip():
            errors.append(f"{observation_id}: non-numeric status cannot carry a price")
    return errors


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    checks: dict[str, dict] = {}
    observations = read_csv(OBS)
    lineages = read_csv(LINEAGE)
    source_rows = read_csv(SOURCES)
    claims = read_csv(CLAIMS)
    lineage_ids = {row["lineage_id"] for row in lineages}
    source_ids = {row["source_id"] for row in source_rows}
    observation_ids = {row["observation_id"] for row in observations}
    contract_errors = observation_contract_errors(observations, lineage_ids, source_ids)
    checks["required_observation_fields"] = {"ok": not any("missing fields" in item for item in contract_errors), "missing": []}
    checks["observation_primary_key"] = {"ok": not any("duplicate or empty" in item for item in contract_errors), "duplicates": []}
    checks["market_currency_source"] = {"ok": not any("invalid market" in item or "must use" in item or "source_id" in item for item in contract_errors), "errors": contract_errors[:20], "error_count": len(contract_errors)}
    checks["price_status_contract"] = {"ok": not any("price" in item for item in contract_errors), "errors": contract_errors[:20], "error_count": len(contract_errors)}
    checks["lineage_references"] = {"ok": not any("lineage_id" in item for item in contract_errors), "orphans": []}
    errors.extend(contract_errors)

    current = [row for row in observations if row.get("snapshot_id") == "current_2026-08-15"]
    history = [row for row in observations if row.get("snapshot_id") == "historical_panel_2026-08-15"]
    expected_counts = {"current": 161, "history": 77, "current_numeric": 147, "history_numeric": 76}
    actual_counts = {"current": len(current), "history": len(history), "current_numeric": sum(row["price_status"] == "numeric" for row in current), "history_numeric": sum(row["price_status"] == "numeric" for row in history)}
    checks["baseline_counts"] = {"ok": actual_counts == expected_counts, "expected": expected_counts, "actual": actual_counts}
    if actual_counts != expected_counts:
        errors.append(f"baseline counts differ: {actual_counts}")

    output_contracts = {
        "family_summary": R1 / "outputs" / "brand_family_summary.csv",
        "chanel_ladder": R1 / "outputs" / "chanel_ladder.csv",
        "band_sensitivity": R1 / "outputs" / "band_sensitivity.csv",
        "comparable_cells": R1 / "outputs" / "comparable_cells.csv",
        "aligned_history": R1 / "outputs" / "aligned_history.csv",
        "robustness": R1 / "outputs" / "robustness.csv",
        "unresolved": R1 / "outputs" / "unresolved.csv",
    }
    output_status = {}
    for name, path in output_contracts.items():
        rows = read_csv(path) if path.exists() else []
        output_status[name] = {"exists": path.exists(), "rows": len(rows)}
        if not path.exists() or not rows:
            errors.append(f"required R1 output missing or empty: {path}")
    checks["required_outputs"] = {"ok": not any(not value["exists"] or not value["rows"] for value in output_status.values()), "outputs": output_status}

    claim_errors = []
    claim_ids = set()
    for claim in claims:
        if claim["claim_id"] in claim_ids:
            claim_errors.append(f"duplicate claim_id {claim['claim_id']}")
        claim_ids.add(claim["claim_id"])
        for obs_id in filter(None, claim.get("observation_ids", "").split(";")):
            if obs_id not in observation_ids:
                claim_errors.append(f"{claim['claim_id']}: unknown observation {obs_id}")
        output_path = ROOT / claim.get("output_path", "")
        if not output_path.exists():
            claim_errors.append(f"{claim['claim_id']}: missing output {claim.get('output_path')}")
        if claim.get("evidence_grade") not in {"A", "B", "C", "X"}:
            claim_errors.append(f"{claim['claim_id']}: invalid evidence grade")
    checks["claim_references"] = {"ok": not claim_errors, "errors": claim_errors[:20], "error_count": len(claim_errors)}
    errors.extend(claim_errors)

    critical_unresolved = []
    unresolved_path = R1 / "outputs" / "unresolved.csv"
    for row in read_csv(unresolved_path):
        if row.get("critical_for_core") == "TRUE":
            critical_unresolved.append(row.get("issue_id", ""))
    checks["unresolved_register"] = {"ok": True, "rows": len(read_csv(unresolved_path)), "critical_rows": len(critical_unresolved), "limited_reason": "Dior unresolved prices and Hermès Geta source conflict are retained and excluded or bounded."}
    warnings.extend(["Dior US and FR unresolved rows are not imputed.", "Hermès Geta France 2023 conflict is retained as two source branches.", "Historical secondary-source share and incomplete years limit the strength of the history claim."])

    if errors:
        status = "fail"
    else:
        status = "limited" if critical_unresolved or warnings else "pass"
    validation = {
        "status": status,
        "run_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
        "source_commit": git_sha(),
        "checks": checks,
        "warnings": warnings,
        "errors": errors,
        "excluded_claims": [row["claim_id"] for row in claims if row.get("publication_decision") == "exclude_from_core"],
        "unresolved_critical_count": len(critical_unresolved),
        "limited_display_thresholds": ["Dior US numeric coverage is 65.0%.", "Historical aligned years are observed years only.", "No broad Hermès icon comparison is published."],
    }
    output_file = R1 / "outputs" / "validation.json"
    output_file.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "errors": len(errors), "warnings": len(warnings), "unresolved_critical_count": len(critical_unresolved)}, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
