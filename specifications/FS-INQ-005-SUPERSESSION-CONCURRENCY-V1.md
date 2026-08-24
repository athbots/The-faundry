# FS-INQ-005 — INQ Formal Supersession & Concurrency v1

Status: VALIDATED REFERENCE MODEL

## Supersession
A later resolution never edits an earlier resolution. It creates an immutable
ResolutionRecord with an explicit `SUPERSEDES` relation, predecessor ID and
predecessor digest, evidence basis, reason, and authority.

## Concurrency
Mutable INQ operations use optimistic concurrency control. Every operation
carries `expected_revision`; a stale revision fails closed with no mutation.
Successful mutations increment the revision.

## Invariants
- no lost update;
- no stale overwrite;
- no silent resolution replacement;
- predecessor digest must match;
- old resolutions remain immutable;
- every successful operation is audited;
- concurrent conflicting writes cannot both succeed against one revision.

This is a reference integrity model, not production distributed-transaction certification.
