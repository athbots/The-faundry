# FS-INT-004 — Concurrency, Stale-State & Persistence Integrity v1

Reference model: optimistic concurrency control.

Required:
1. Every mutable aggregate has a version.
2. Stale writes fail closed.
3. Exact retries are idempotent.
4. Idempotency-key collisions fail.
5. Terminal states are monotonic.
6. Historical records are append-only.
7. Supersession creates a new identity.
8. Interrupted persistence must not imply successful commit.
9. Recovery is explicit and traceable.
10. Stale governance cannot authorize newer state.

Production implementation must separately define transaction isolation,
durability, crash recovery, distributed consensus/locking, and backups.
