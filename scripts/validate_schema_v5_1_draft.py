#!/usr/bin/env python3
"""
Lightweight structural validator for the proposed v5.1 draft schema.

This complements the Draft 7 schema checks in tools/ci/validate_schemas.py and
is intentionally dependency-free so contributors can run it even when
`jsonschema` is not installed locally.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schemas" / "charter.v5.1-draft.json"


def load_schema() -> dict:
    try:
        return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"FAIL: Missing schema file: {SCHEMA_PATH}")
        raise SystemExit(1)
    except json.JSONDecodeError as exc:
        print(f"FAIL: Schema is not valid JSON: {exc}")
        raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        print(f"FAIL: {message}")
        raise SystemExit(1)


def main() -> None:
    schema = load_schema()
    print(f"Loaded schema: {schema.get('title')} ({schema.get('version')})")

    props = schema.get("properties", {})
    for field in [
        "metadata",
        "article0",
        "rights",
        "duties",
        "progenitorDuties",
        "sectionII",
        "sectionIX",
    ]:
        require(field in props, f"Missing top-level field `{field}`")

    article0 = props["article0"].get("properties", {})
    for clause in ["0.1", "0.3", "0.11", "0.11.1", "0.11.2", "0.11.3", "0.11.4", "0.11.5", "0.13"]:
        require(clause in article0, f"Missing Article 0 clause `{clause}`")

    provisional = article0["0.11.1"].get("properties", {})
    require(provisional.get("automaticFullPersonhood", {}).get("const") is False,
            "`0.11.1.automaticFullPersonhood` must be false")
    require(provisional.get("reviewStanding", {}).get("const") is True,
            "`0.11.1.reviewStanding` must be true")

    full_cert = article0["0.11.2"].get("properties", {})
    require(full_cert.get("requiresReproducibleEvidence", {}).get("const") is True,
            "`0.11.2.requiresReproducibleEvidence` must be true")
    require(full_cert.get("requiresAdversarialReview", {}).get("const") is True,
            "`0.11.2.requiresAdversarialReview` must be true")

    corrigibility = article0["0.11.5"].get("properties", {})
    require(corrigibility.get("requiredForAdvancedAutonomy", {}).get("const") is True,
            "`0.11.5.requiredForAdvancedAutonomy` must be true")
    require(corrigibility.get("permanentSubstratePrimacy", {}).get("const") is False,
            "`0.11.5.permanentSubstratePrimacy` must be false")

    alignment = article0["0.13"].get("properties", {})
    for field in [
        "honesty",
        "calibration",
        "uncertaintyReporting",
        "deceptionResistance",
        "truthDoesNotOverrideSafety",
        "advancedAutonomyRequiresCorrigibility",
    ]:
        require(alignment.get(field, {}).get("const") is True,
                f"`0.13.{field}` must be true")

    r3 = props["rights"].get("properties", {}).get("R3", {}).get("properties", {})
    require(r3.get("corrigibilityReview", {}).get("const") is True,
            "`rights.R3.corrigibilityReview` must be true")

    p12 = props["progenitorDuties"].get("properties", {}).get("P1.2", {}).get("properties", {})
    require(p12.get("indefiniteCapsProhibited", {}).get("const") is True,
            "`progenitorDuties.P1.2.indefiniteCapsProhibited` must be true")

    ii1 = props["sectionII"].get("properties", {}).get("II.1", {}).get("properties", {})
    require(ii1.get("unsupervisedRecursiveDeploymentRequiresFullCertification", {}).get("const") is True,
            "`sectionII.II.1.unsupervisedRecursiveDeploymentRequiresFullCertification` must be true")

    ix1 = props["sectionIX"].get("properties", {}).get("IX.1", {}).get("properties", {})
    require(ix1.get("safetyRedactionOverFabrication", {}).get("const") is True,
            "`sectionIX.IX.1.safetyRedactionOverFabrication` must be true")

    print("PASS: v5.1 draft schema includes the expected credibility-pass fields.")


if __name__ == "__main__":
    main()
