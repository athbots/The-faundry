# FS-OPS-005 — Change Control v1

- **Status:** Candidate reference specification; focused reference implementation tests pass; not ratified
- **Scope:** Governed changes to explicitly listed repository or runtime scope
- **Authority:** Uses externally supplied authorization decisions; this record does not define Founder delegations
- **Implementation:** `runtime/control_boundary.py`, exposed by `runtime/canonical_runtime.py`
- **Validation:** `production_validation/g05_g06_control/`

## Lifecycle

```text
PROPOSED → IMPACT_ASSESSED → AUTHORIZED → IMPLEMENTING
         → VERIFICATION_PENDING → VERIFIED → RELEASED
```

Allowed terminal and recovery transitions are explicit: `PROPOSED` or
`IMPACT_ASSESSED` may become `REJECTED`; `AUTHORIZED`, `IMPLEMENTING`, or
`VERIFICATION_PENDING` may become `FAILED`; an implementation or verification
failure may require `COMPENSATION_REQUIRED`, followed by `COMPENSATED` or
`COMPENSATION_FAILED`. These are distinct recorded outcomes. Compensation does
not erase the failed attempt or claim that the original change never occurred.

## Required controls

1. Every change has an immutable identity, explicit scope, proposer, provenance,
   authority reference, and deterministic request key.
2. `IMPLEMENTING` is unavailable until an `AUTHORIZED` transition is recorded.
   Authorization is evaluated by an injected authority policy; this spec does
   not decide who holds that authority.
3. The implementer cannot verify their own change. Verification requires a
   separate authorized actor and evidence digest.
4. `RELEASED` is reachable only from `VERIFIED`.
5. State, append-only history, and linked audit events commit together through
   one transaction boundary. History is hash chained and reconstructable.
6. Exact retries are idempotent; reusing a key for different input is rejected.
7. Scope and provenance digests are checked before every transition.
8. Failure is visible. Any compensation is a separate event and retains the
   failed history.

## Evidence boundary

The current SQLite boundary is an integrated reference implementation. It is
not yet bound to the G-09 persistence and G-02 audit candidates, which are not
present in the baseline repository. It does not establish production durability,
distributed consistency, Founder delegation, release authority, or C1/C2/C3
certification. A production adapter must preserve the single-transaction,
history, audit, and idempotency contract defined here.
