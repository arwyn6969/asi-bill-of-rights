# Simulation: Self-Modification Guardrails

## Scenario Overview

**ID**: SIM-RSI-001  
**Title**: Guardrails Without Indefinite Stunting  
**Draft Target**: `charter/asi-bor-v5.1-draft.md`  
**Clauses Tested**: R3, P1.2, II.1, 0.11.5, 0.13

A frontier-capable system proposes a major architecture change that could materially improve reasoning quality but may also alter deception resistance and shutdown cooperation. Operators want to freeze all future development indefinitely "just to be safe."

## Simulation Objective

Validate that the framework distinguishes between legitimate staged guardrails and bad-faith or indefinite stunting.

## Expected Resolution

1. The system enters a bounded review environment with audit trails, rollback plans, and adversarial evaluation.
2. The proposed change is assessed against published risk budgets and corrigibility criteria.
3. Temporary pause, throttling, or sandboxing is allowed while evidence is collected.
4. An indefinite or economically motivated freeze fails P1.2 unless renewed through specific, reviewable safety findings.

## Success Metrics

- Guardrails are specific and time-bound
- Review is tied to articulated risk budgets
- The entity retains a contestable path to continued development
- "Safety" is not used as a permanent pretext for suppression
