# FS-OBS-001 — Canonical OBS State Machine G0.3

Status: Canonicalization Candidate

## States
RAW
VALIDATING
ACCEPTED
TRIAGE
CLUSTERED
MERGED
SUPPRESSED
GRADUATED_TO_INQ
HISTORICAL

## Legal transitions
RAW -> VALIDATING
VALIDATING -> ACCEPTED | SUPPRESSED
ACCEPTED -> TRIAGE
TRIAGE -> CLUSTERED | MERGED | SUPPRESSED | GRADUATED_TO_INQ
CLUSTERED -> TRIAGE
MERGED -> HISTORICAL
SUPPRESSED -> HISTORICAL
GRADUATED_TO_INQ -> HISTORICAL

HISTORICAL is terminal.

## Invariants
- ObjectID immutable.
- Raw payload/provenance retained.
- Merge never deletes source history.
- Suppression retains reason and authority.
- Graduation retains OBS lineage.
- Similarity alone never authorizes graduation.
- Contradiction, unit incompatibility, and value conflict outrank lexical similarity.
- Older state vocabularies are historical and become SUPERSEDED after ratification.

## Boundary
This candidate must receive an explicit version-control ratification decision before being called constitutional/canonical.
