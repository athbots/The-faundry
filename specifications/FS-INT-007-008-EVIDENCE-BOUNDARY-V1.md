# FS-INT-007-008 — G-07 / G-08 Evidence Boundary v1

- **Status:** Integrated reference adapter candidate; focused tests pass; not ratified
- **G-07 source:** Not present in this repository baseline
- **G-08 source:** `specifications/FS-CERT-008-CERTIFICATION-EVIDENCE-V1.md`
- **Adapter:** `runtime/g07_g08_evidence_gate.py`
- **Validation:** `production_validation/g08_certification_evidence/`

## Normative boundary for this adapter

Before a G-07 obligation requiring evidence may transition to
`RESOLUTION_PENDING`, the caller must provide its identity, explicit evidence
requirement, evidence IDs, and a transition callback. The adapter calls the
callback only after every referenced G-08 record is found, `VERIFIED`, and has
a valid reconstructable audit chain. Missing references, unknown IDs,
`REGISTERED`, `VERIFICATION_PENDING`, `INVALID`, `FAILED`, or audit-integrity
failures reject the request without calling the G-07 callback.

For obligations not requiring evidence, the evidence requirement must still be
explicitly `false`; the G-07 caller remains responsible for all other transition
rules.

G-07 resolution verification is separately guarded: it must follow
`RESOLUTION_PENDING`, and the verifier must differ from the recorded resolution
actor. The callback performs the actual G-07 transition and persistence.

## Conflict and integration limitation

This repository does not contain the G-07 candidate implementation or either
candidate ZIP. The adapter therefore provides a fail-closed boundary around a
caller-owned callback; it does not claim the G-07 lifecycle is implemented or
that callbacks are durably persisted. The candidate package SHAs reported in
the referenced conversation are provenance only and were not reproducible from
files available in this checkout. This limitation is explicit and does not
change G-07 semantic expectations.

The adapter makes no G-10 distributed consistency claim and introduces no
governance weights, certification thresholds, or authority delegation.
