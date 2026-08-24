# PV-02 — Failure Injection

Invariant: state mutation and institutional event append must be atomic.

If execution terminates before commit:
- previous OBS state survives;
- no partial event survives.

If commit succeeds:
- state and event survive restart.

A subsequent process must be able to recover and continue from the durable state.

This gate validates the reference SQLite transaction boundary. It does not certify production storage, hardware, distributed databases, backups, or deployed failure modes.
