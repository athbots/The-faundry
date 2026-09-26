# FS-OPS-006 — Migration Control v1

- **Status:** Candidate reference specification; focused reference implementation tests pass; not ratified
- **Scope:** Explicitly scoped and versioned data or runtime migrations
- **Authority:** Authorization and rollback decisions are injected; this record does not define Founder delegations
- **Implementation:** `runtime/control_boundary.py`, exposed by `runtime/canonical_runtime.py`
- **Validation:** `production_validation/g05_g06_control/`

## Lifecycle

```text
PREPARED → VALIDATING → AUTHORIZED → EXECUTING
         → POST_VERIFYING → COMPLETED
```

Precondition, execution, or post-integrity failure becomes `MIGRATION_FAILED`.
An authorized recovery decision may move it to `ROLLBACK_REQUIRED`; only a
reversible migration with recorded compensation evidence may become
`ROLLED_BACK`. A non-reversible migration cannot claim rollback. Failed state,
attempted phases, and audit history remain visible after rollback.

## Required controls

1. A migration has immutable identity, explicit scope, provenance, reversibility
   declaration, authority references, and deterministic idempotency key.
2. Preconditions are checked before authorization; execution requires an
   authorized record and a separately authorized execution actor.
3. Migration mutation, lifecycle events, and linked audit events commit within
   one database transaction. A failed operation rolls back the mutation and
   writes a durable failure event in a separate transaction.
4. Post-migration verification requires a distinct actor, authority reference,
   and passing integrity evidence before `COMPLETED`.
5. Scope and provenance digests are checked before execution. Exact retries do
   not rerun a completed migration; key collisions fail closed.
6. `ROLLBACK_REQUIRED` and `ROLLED_BACK` are distinct from `COMPLETED` and from
   compensation of non-reversible external effects. Such external effects are
   outside this SQLite reference model.

## Evidence boundary

The current SQLite boundary is an integrated reference implementation. The
baseline repository contains no G-09/G-02 runtime boundary to reuse. This work
does not claim production persistence, distributed consistency, a migration
authority delegation, production recovery, or certification. Any eventual G-09
adapter must preserve the atomic state-plus-audit contract and idempotency.
