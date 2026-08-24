# FS-OBS-002 — Semantic Safety Layer v1

Status: RATIFIED
Authority: CISA
Direction: Founder-approved
Effective: 2026-08-16
Predecessor: FS-OBS-001 G0.3 semantic boundary

## Ratification decision

FS-OBS-002 v1 is ratified as the canonical semantic safety boundary for OBS.

The ratification is conditional in one specific sense:

FS-OBS-002 does NOT constitute production-grade general semantic understanding or semantic certification.

The following remains mandatory before such a claim may be made:

`REAL-SEM-01 — Representative OBS Semantic Validation`

## Reason for ratification

PV-05 exposed material defects in the previous frozen semantic implementation:

- contradictory propositions were not reliably identified;
- explicit entity differences could collapse into related observations;
- measurement-unit representation was not normalized safely;
- temporal differences could be confused with value conflict.

The revised layer addresses these failure classes through structured normalization and relation analysis.

## Canonical normalized proposition

`P = (entity, predicate, value, unit, timestamp, provenance)`

## Safety principles

1. Raw OBS evidence remains immutable.
2. Semantic normalization never replaces raw evidence.
3. Explicit entity mismatch prevents equivalence.
4. Compatible units are normalized before comparison.
5. Incompatible or unresolved units cannot be treated as equivalent.
6. Mutually exclusive predicate values may produce contradiction.
7. Temporal metadata remains available downstream.
8. Semantic relation does not independently authorize INQ graduation.
9. Insufficient evidence must not be converted into false certainty.
10. Production semantic certification requires REAL-SEM-01.

## Evidence

- PV-05 adversarial calibration: 16/16 PASS.
- PV-02 failure-injection regression: PASS.
- PV-03 recovery regression: PASS.
- PV-04 sustained-load regression: PASS.

## Scope boundary

This ratification authorizes use of FS-OBS-002 as the institutional semantic safety architecture.

It does not authorize claims about:
- general natural-language understanding;
- production false-positive/false-negative rates;
- complete entity resolution;
- domain-specific measurement tolerances;
- semantic performance on an unreviewed real-world corpus.

## Supersession

The affected semantic portion of FS-OBS-001 G0.3 is superseded by FS-OBS-002.

G0.3 remains preserved as historical institutional memory and is not deleted.

## Future mandatory gate

REAL-SEM-01 must establish a reviewed gold-label corpus and measure:
- entity-resolution accuracy;
- contradiction detection;
- equivalence precision;
- value-conflict detection;
- unit normalization;
- false-positive and false-negative behavior.

Until REAL-SEM-01 passes, semantic certification remains provisional.
