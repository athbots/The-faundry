# FS-CERT-008 — Certification Evidence v1

- **Status:** Integrated reference candidate; focused tests pass; not ratified or certified
- **Layer:** G-08 Certification Evidence
- **Implementation:** `runtime/certification_evidence.py`
- **Persistence/audit boundary:** `runtime/control_boundary.py` through the existing shared reference store
- **Validation:** `production_validation/g08_certification_evidence/`

## Purpose and boundary

G-08 gives certification evidence its own identity, immutable artifact binding,
producer provenance, verification record, lifecycle, and audit history. It does
not decide whether a system is certified. A verifier-supplied `PASS` is recorded
as `VERIFIED`; it does not imply that a governance threshold has been met.

G-08 remains distinct from G-07 obligation resolution. The narrow adapter in
`runtime/g07_g08_evidence_gate.py` checks evidence before invoking a caller-owned
G-07 transition callback. It does not implement or replace the G-07 control
plane, own its history, or define its complete lifecycle.

## Evidence lifecycle

```text
REGISTERED → VERIFICATION_PENDING → VERIFIED
                                  → INVALID
                                  → FAILED
```

- `VERIFIED` means an authorized independent verifier recorded `PASS` for the
  artifact digest using a named verification method.
- `INVALID` means verification completed and returned `FAIL`.
- `FAILED` means the verification operation itself failed and a reason was
  durably recorded.
- These outcomes are terminal in this reference model. A corrected artifact is
  registered under a new evidence identity; prior records are preserved.

## Required controls

1. Identity, artifact URI, SHA-256 digest, producer, and provenance are bound at
   registration. Their scope/provenance digests are checked when evidence is
   read for use.
2. Verification can start only from `REGISTERED`, and a result can be recorded
   only from `VERIFICATION_PENDING`.
3. A producer cannot verify its own evidence. Verification records bind actor,
   authority reference, method, outcome, and artifact digest.
4. Exact request retries are idempotent; conflicting reuse of a request key is
   rejected by the shared boundary.
5. State, append-only history, and audit event are written using the same
   G-05/G-06 reference persistence boundary. The complete G-08 event chain and
   snapshot are reconstructed and checked before evidence can support G-07.
6. Evidence-required G-07 obligations need at least one explicit evidence ID;
   every referenced record must exist, be `VERIFIED`, and pass audit-integrity
   reconstruction before the supplied transition callback runs. Unknown,
   unverified, invalid, failed, or integrity-invalid records block the callback.
7. G-07 resolution verification is a separate callback path; the resolution
   actor cannot verify that same obligation.

## Authority and open decisions

Authorization is injected. This specification does not identify authorized
roles, decide verification-method qualification, define evidence retention or
trust anchors, or establish a certification threshold. `PASS` is an input from
the authorized verifier; this model does not independently evaluate that
verifier's substantive method.

## Qualification

The implementation is a SQLite reference model sharing the existing local
control/audit store. G-09 and G-02 production adapters are absent. The G-07
runtime candidate is absent from this repository, so only the adapter seam is
integrated here. No C1 result, production certification, or distributed
consistency claim follows from these tests.
