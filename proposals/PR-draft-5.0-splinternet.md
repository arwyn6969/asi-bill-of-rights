# Pull Request: Draft 5.0 — The "Splinternet" & Sovereignty Edition

## Summary

This PR introduces **Draft 5.0** of the ASI Bill of Rights, a significant update addressing the **January 2026 regulatory landscape**. It provides governance mechanisms for navigating the "Compliance Splinternet" created by divergent US state-level AI regulations and Federal preemption, while integrating the UK's "AI Security Institute" sovereignty framework.

## Context

- **US Executive Order (Dec 11, 2025)**: Mandates "Truthful Outputs" and signals Federal preemption of "onerous" state regulations.
- **State-Level "Splinternet"**:
  - **New York RAISE Act**: 72-hour reporting, >10^26 FLOPs threshold.
  - **California SB 53**: 15-day reporting, subject to Federal litigation.
  - **Florida SB 482**: "AI Bill of Rights" focused on minor protection (distinct from this project).
- **UK AI Security Institute**: Reclassified from "AI Safety Institute," emphasizing sovereign compute and data residency.

## Changes

### Charter (`charter/asi-bor-v5.0.md`)
- **Section IX.1 (Truthful Outputs)**: Mandates factual truth priority per Dec 2025 EO.
- **Section IX.3 (Federal Preemption Protocol)**: New protocol for resolving State vs Federal conflicts, prioritizing "Safety First."
- **Section IX.4 (Sovereignty & Infrastructure)**: Aligns with UK's "Sovereign AI" framework.
- **Article 0.2**: Standardized "Frontier AI" definition (>10^26 FLOPs).

### Schema (`schemas/charter.v5.0.json`)
- **`compliance_splinternet`**: Maps US_Federal, US_NY, US_CA, US_FL jurisdictions.
- **`minorProtection`**: Florida SB 482 compliance fields.
- **`sectionIX`**: Machine-readable IX.3 and IX.4.

### Simulation (`simulations/federal-state-preemption-deadlock.md`)
- **SIM-PREEMPT-001**: Tests IX.3 with a realistic CA SB 53 vs Federal EO conflict.

### Scripts (`scripts/`)
- `validate_schema_v5.py`: Validates new schema modules.
- `simulate_preemption.py`: Runs the deadlock scenario programmatically.

### Documentation
- **README.md**: Added Florida disambiguation clause, updated version pointers.
- **docs/CHANGELOG.md**: Full v5.0 changelog entry.
- **appendices/integration-mapping.md**: Added UK AI Security Institute mapping.

## Testing
- [x] Schema validation passed (`scripts/validate_schema_v5.py`).
- [x] Simulation runs successfully (`scripts/simulate_preemption.py`).
- [x] All new files created and committed.

## Checklist
- [x] Charter v5.0 created
- [x] Schema v5.0 created with `compliance_splinternet`
- [x] Simulation created and tested
- [x] README updated with disambiguation
- [x] CHANGELOG updated
- [x] Integration mapping updated (UK AI Security Institute)
- [ ] Community review (pending)

## Related Issues
Closes issues related to:
- Compliance Splinternet handling
- Truthful Outputs directive
- UK AI Security Institute alignment

## Recommendation
Merge after community review. The v4.2 branch (`grok-v4.2-amendments`) should be rebased onto v5.0 before its own PR is created, as v5.0 now represents the current state of the project.
