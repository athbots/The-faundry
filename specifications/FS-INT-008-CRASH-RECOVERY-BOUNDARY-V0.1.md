# FS-INT-008 — G-07/G-08 Crash-Recovery Boundary v0.1

- **Status:** Candidate provenance reconciled; independent repository implementation validated; not ratified or certified
- **Implementation:** `runtime/crash_recovery_boundary.py` and `runtime/control_boundary.py`
- **Runtime wiring:** `runtime/canonical_runtime.py`
- **G-08 verification boundary:** `runtime/certification_evidence.py`
- **G-07 evidence/independence gate:** `runtime/g07_g08_evidence_gate.py`
- **Validation record:** `production_validation/g07_g08_crash_recovery/G07-G08-CRASH-RECOVERY-BOUNDARY-RESULT-V0.1.md`

## Required persistence invariant

For each committed object operation, aggregate state, authoritative audit event,
and idempotency entry are written inside the same SQLite transaction. Before
commit, none is authoritative. A process termination after an aggregate update
or event insertion but before commit must leave the prior committed aggregate,
history, and idempotency state intact.

The crash-recovery adapter reuses the existing G-05/G-06 persistence and audit
port. It creates no parallel database, audit log, or idempotency store. It
reconstructs the record from its event chain after create, transition, and
migration execution before returning the resulting snapshot.

## Integrity and recovery

1. Every newly committed snapshot carries a `state_hash` over its canonical JSON
   representation, excluding the `state_hash` field itself.
2. The corresponding event includes that `state_hash`; the event hash chain
   therefore binds the state hash to the audit history.
3. Recovery verifies the event hash chain, creation event, event sequence,
   terminal state/version, and terminal snapshot hash. Corrupt history or
   snapshot state fails closed with an integrity error.
4. Exact retries retain the original idempotency result without adding events;
   reuse of a request key for different input is rejected.
5. Previously committed state remains visible if a later operation terminates
   before commit. Restart reconstruction is performed from the same shared
   record/audit boundary.
6. G-08 evidence is usable only while its existing `VERIFIED` and audit-integrity
   requirements hold. The G-07 gate continues to require independent obligation
   verification.

## Scope and qualification

This is a local SQLite reference boundary. It does not establish filesystem or
device power-loss guarantees, production G-09/G-02 adapter behavior, or G-10
distributed consistency. It does not change G-07 lifecycle semantics or select
governance/certification thresholds.

## Candidate and repository provenance

The transfer candidate is
`the-foundry-g07-g08-crash-recovery-boundary-candidate-v0.1.zip`. Per the
independent candidate-validation provenance supplied with this reconciliation,
its SHA-256 was verified as
`8d9c13485efaba2e926b10044a59ae3c2051ea888ed366ed4f3d557a41552158`; its actual
`tests/test_crash_recovery_boundary.py` was independently executed with pytest
and passed **15/15**. The candidate archive is a transfer artifact; it is not
the canonical repository record.

The repository implementation was independently integrated from the boundary
requirements using the existing shared control persistence/audit port. It was
not blindly copied from the candidate archive. Its separately authored crash
recovery suite passed **18/18**, the stated directly affected regression scope
passed **95/95**, and the combined repository-owned validation passed **113/113**.
The exact repository run is in
`production_validation/g07_g08_crash_recovery/G07-G08-CRASH-RECOVERY-BOUNDARY-RESULT-V0.1.md`.
The candidate and repository results remain separate evidence records.
