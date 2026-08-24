# PV-06 — Operations & Rollback Validation

## Purpose

Prove that a deployed Foundry component can be changed, detected as defective,
rolled back to the last known-good version, and resumed without loss of
institutional evidence or authority state.

## Required invariants

1. A release has an immutable release identifier.
2. A known-good release is recorded before a new release becomes active.
3. A failed release cannot silently become authoritative.
4. Rollback restores the prior known-good implementation.
5. OBS evidence and event history survive rollback.
6. Rollback itself is recorded as an institutional event.
7. Re-execution after rollback uses the restored release.
8. A partial rollout cannot leave mixed authoritative versions.
9. Recovery does not rewrite historical evidence.
10. Rollback must fail closed if the known-good release is unavailable.

## Qualification

This gate validates a deterministic reference deployment/rollback controller.
It is not a production deployment certification.
