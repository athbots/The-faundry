# G07-G08 Crash-Recovery Boundary — Validation Result v0.1

- **Branch:** `integration/g07-g08-crash-recovery-v0.1`
- **Tested source commit:** `4a51d1427004a8707085e65656c0851bee4ba75c`
- **Recorded:** 2026-09-26 16:33 UTC
- **Provenance reconciliation and post-reconciliation rerun:** 2026-09-26 16:45 UTC
- **Environment:** Windows 11 10.0.26200, AMD64, Python 3.12.14, standard library only
- **Status:** Candidate provenance reconciled; repository-owned reference validation passed; not certified

## Results

All directly affected repository-owned tests completed with **113 PASS, 0 FAIL**:

| Scope | Command | PASS | FAIL | Exit |
|---|---|---:|---:|---:|
| Crash-recovery boundary | `python -m unittest tests.test_crash_recovery_boundary -v` | 18 | 0 | 0 |
| G-08 certification evidence | `python -m unittest tests.test_g08_certification_evidence -v` | 20 | 0 | 0 |
| G-05/G-06 controls | `python -m unittest tests.test_g05_g06_control -v` | 19 | 0 | 0 |
| PV-15 cross-layer integration | `python tests/test_pv15_cross_layer_integration.py` | 12 | 0 | 0 |
| PV-17 concurrency/persistence | `python tests/test_pv17_concurrency_persistence.py` | 12 | 0 | 0 |
| PV-16 failure recovery | `python production_validation/pv16_failure_recovery_test.py` | 12 | 0 | 0 |
| PV-16 recovery regression | `python production_validation/pv16_test.py` | 12 | 0 | 0 |
| PV-06 operations rollback | `python production_validation/pv06_operations_rollback/test_pv06_operations_rollback.py` | 8 | 0 | 0 |
| **Total** |  | **113** | **0** | **0 for all runs** |

Commands above were executed using:

`C:\Users\aniru\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`

The crash tests terminate a child process after the aggregate and audit-event
SQL writes but before transaction commit. Reopening the database confirms both
uncommitted changes were rolled back and the prior committed state reconstructs.

## Candidate validation provenance

Candidate: `the-foundry-g07-g08-crash-recovery-boundary-candidate-v0.1.zip`

- SHA-256, independently verified: `8d9c13485efaba2e926b10044a59ae3c2051ea888ed366ed4f3d557a41552158`.
- Candidate test file: `tests/test_crash_recovery_boundary.py`.
- Candidate command: `pytest tests/test_crash_recovery_boundary.py`.
- Independent candidate result: **15/15 PASS**, as supplied in the Founder's reconciliation instruction.
- This candidate result is separate from the repository-owned test runs below; it is not counted in their 113/113 total.

The repository implementation was independently integrated from the required
boundary behavior and shared repository persistence/audit contract; it was not
blindly copied from the transfer archive. The repository's 18 crash tests and
its 95-test regression scope remain separately reported below.

An initial repository development run reported 11 passing tests and 5 teardown
errors because the tests left SQLite handles open on Windows. Test cleanup was
corrected; the final repository run passed all 18 crash tests without errors.

## Integrated behavior

- Aggregate snapshot, state hash, authoritative audit event, and idempotency
  entry commit in the existing SQLite control-boundary transaction.
- Process termination before commit leaves neither the proposed state mutation
  nor its audit event authoritative.
- Recovery verifies hash-linked event history, the creation audit reference,
  event sequence, terminal state/version, and terminal snapshot state hash.
- Exact retry returns the committed result without duplicating history;
  idempotency-key collisions are rejected.
- G-08 evidence must still be `VERIFIED` with valid audit integrity before the
  G-07 resolution callback runs; evidence producers cannot self-verify.
- G-07 resolution actors cannot verify their own obligations. The integration
  tests exercise durable `RESOLUTION_PENDING` and independent-verification
  transitions through the shared boundary.

## Remaining gaps and qualification

- The actual G-07 candidate runtime is still not part of this repository
  integration. The G-07 gate is connected through the shared persistence
  adapter; complete integration into an authoritative G-07 runtime remains open.
- The implementation is a SQLite reference model. Device/power-loss guarantees,
  production G-09 persistence, production G-02 audit, and G-10 distributed
  consistency remain unverified.
- Governance authority, certification thresholds, C1, and production
  certification remain open/not claimed.
