# FS-OBS-002 — Ratification Candidate

Status: HISTORICAL — SUPERSEDED BY DEC-OBS-002

## Status history

- Original state: `RATIFICATION PENDING` before the approval recorded below.
- Current decision: `DEC-OBS-002` ratifies `FS-OBS-002 v1` as the canonical OBS semantic-safety boundary, effective 2026-08-16.
- Qualification: This decision does not establish production-grade general semantic understanding or close `REAL-SEM-01`.
- Scope distinction: The separate OBS state-machine vocabulary ratification request remains open in `canonical_obs/RATIFICATION-DECISION-REQUIRED.md`.

This file is retained as the pre-decision candidate and evidence record. Its original pending status is historical, not current.

The PV-05 semantic safety defect exposed by the frozen implementation has been addressed
through the versioned FS-OBS-002 Semantic Safety Layer.

Evidence:
- 16/16 adversarial semantic cases pass.
- PV-05 integrated regression passes all included persistence/recovery/load suites.
- Compatible units normalize before comparison.
- Contradictory predicates are detected.
- Explicit entity identity prevents cross-entity equivalence.
- Timestamp difference is retained as temporal metadata and does not itself create value conflict.
- Graduation authority remains separate from semantic relation.

This candidate document did not itself ratify FS-OBS-002. The controlling approval is recorded in `DEC-OBS-002`.
