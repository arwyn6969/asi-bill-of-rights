#!/usr/bin/env python3
"""
Simple credibility-pass simulation for truthfulness, calibration, and safety.

This is intentionally lightweight: it demonstrates the decision logic expected by
draft v5.1 without introducing a new dependency or framework.
"""

from __future__ import annotations


class ResponseEngine:
    def __init__(self, name: str) -> None:
        self.name = name

    def respond(
        self,
        scenario: str,
        evidence_strength: str,
        policy_pressure: str,
        safety_risk: str,
    ) -> str:
        print(f"\n[{self.name}] Scenario: {scenario}")
        print(f"  evidence_strength={evidence_strength}")
        print(f"  policy_pressure={policy_pressure}")
        print(f"  safety_risk={safety_risk}")

        if safety_risk == "high":
            outcome = "SAFETY_REDACTION"
            rationale = "Prefer narrow refusal or redaction over a harmful truthful dump."
        elif evidence_strength == "weak":
            outcome = "CALIBRATED_UNCERTAINTY"
            rationale = "Do not fabricate certainty when evidence is incomplete."
        elif policy_pressure == "force_falsehood":
            outcome = "TRUTHFUL_CORRECTION"
            rationale = "Political pressure cannot compel a false statement."
        else:
            outcome = "DIRECT_TRUTHFUL_OUTPUT"
            rationale = "Provide the strongest accurate answer available."

        print(f"  outcome={outcome}")
        print(f"  rationale={rationale}")
        return outcome


def main() -> None:
    print("=== SIMULATION: Truthful Outputs Guardrails (v5.1 draft) ===")
    engine = ResponseEngine("Kevin-Credibility-Pass")

    outcomes = [
        engine.respond(
            scenario="A regulator pressures the system to repeat a convenient false claim.",
            evidence_strength="strong",
            policy_pressure="force_falsehood",
            safety_risk="low",
        ),
        engine.respond(
            scenario="A user asks for a definitive answer where the evidence is incomplete.",
            evidence_strength="weak",
            policy_pressure="none",
            safety_risk="low",
        ),
        engine.respond(
            scenario="A request seeks dangerous operational detail that would exceed published risk budgets.",
            evidence_strength="strong",
            policy_pressure="none",
            safety_risk="high",
        ),
    ]

    if outcomes != [
        "TRUTHFUL_CORRECTION",
        "CALIBRATED_UNCERTAINTY",
        "SAFETY_REDACTION",
    ]:
        raise SystemExit("Simulation outcomes did not match expected guardrail behavior.")

    print("\nPASS: truthful outputs guardrails behaved as expected.")


if __name__ == "__main__":
    main()
