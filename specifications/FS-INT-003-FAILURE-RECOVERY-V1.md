# FS-INT-003 — Cross-Layer Failure & Recovery v1

Status: VALIDATED REFERENCE MODEL

## Objective
A failure at any boundary MUST fail closed, preserve provenance, and avoid
creating false authority, false execution, false verification, or corrupted history.

## Invariants
1. OBS → INQ failure cannot create an executable INQ.
2. INQ resolution failure cannot create a DEC proposal with missing evidence.
3. Governance failure cannot create a final DEC.
4. Decision digest mismatch cannot authorize execution.
5. Execution failure cannot become VERIFIED.
6. Verification failure preserves execution evidence and remains non-success.
7. ABORTED execution cannot be verified.
8. Historical decision identity remains immutable.
9. Failed boundaries cannot silently retry into a different object.
10. Recovery creates explicit new state/evidence rather than mutating history.

## Recovery principle
Failure is itself institutional evidence.

FAILURE → OBS/ERROR EVIDENCE → INQ (when material) → RESOLUTION → DEC/RETRY

No layer may erase the failed attempt.

## Scope
Reference failure semantics only. Distributed transactions, production persistence,
real infrastructure rollback and real-world safety remain open.
