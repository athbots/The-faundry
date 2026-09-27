# Institutional and Repository Status

- **Status date:** 2026-09-26
- **Status basis:** `main` at `b98ed49ccb1e75b941e8611151828788b05d198d` before this reconciliation commit
- **Control source:** [`DOCUMENTATION-ARCHITECTURE-v1.0.md`](DOCUMENTATION-ARCHITECTURE-v1.0.md)
- **Detail register:** [`DOCUMENT-REGISTER.csv`](DOCUMENT-REGISTER.csv)

This page is a dated status snapshot, not a new ratification. Where a summary conflicts with a decision, release note, or validation manifest, the cited controlling record governs within its stated scope.

## Provenance reconciliation addendum — 2026-09-27

The header's `Status date` and `Status basis` preserve the original 2026-09-26 snapshot input: `main` at `b98ed49ccb1e75b941e8611151828788b05d198d`. For the later curation review, the inspected source was `integration/repository-curation-and-readme-v0.1` at `30000ba70cbee7d9da3e172fd27b9b255c0a5766`; `main` remained at `eb4c82e893afcbf52ed484249b0563f648c49160`. The curation branch includes the G-07 discovery and FS-SYS-002 candidate work and was not merged to `main`.

This addendum clarifies provenance only. It does not refresh or ratify the status rows, change any authority, or claim that the branch-only work is on `main`. The [Repository Curation Audit](REPOSITORY-CURATION-AUDIT-V0.1.md) records the scope and limitations.

## Current state

| Area | Current status | What that status means | Controlling record / open gate |
|---|---|---|---|
| Foundation | **Frozen — Genesis G-0.1** | Phase A foundation set is frozen for downstream work; later files on `main` are not thereby included in Genesis | `07_RELEASES/GENESIS-G0.1/RELEASE-NOTES.md`; exact source commit/full manifest remain unresolved |
| Documentation architecture | **Active — v1.0** | Physical paths are preserved; the logical classes and status axes are defined | `00_SYSTEM/DOCUMENTATION-ARCHITECTURE-v1.0.md` |
| OBS state-machine vocabulary | **Ratification pending** | The request to declare FS-OBS-001 G0.3 the single implementation state machine remains open | `canonical_obs/RATIFICATION-DECISION-REQUIRED.md`; `canonical_obs/MANIFEST.json` |
| OBS semantic-safety boundary | **Ratified — FS-OBS-002 v1** | Ratified by DEC-OBS-002 within the semantic-safety scope; does not settle state-machine vocabulary or general semantic certification | `specifications/DEC-OBS-002-FS-OBS-002-RATIFICATION.json`; `specifications/FS-OBS-002-SEMANTIC-SAFETY-LAYER-V1.md` |
| REAL-SEM-01 | **Mandatory gate — not executed** | No production-grade general semantic-understanding claim or certification | `specifications/REAL-SEM-01.md` |
| DEC | **Validated reference models** | FS-DEC-001/002 headers record reference-model validation; exact CFO/TEAM weights remain unratified | `specifications/FS-DEC-001-DECISION-BOUNDARY-V1.md`; `OVERALL-PROGRESS-LEDGER.json` |
| INQ | **Mixed: proposals and validated reference model** | FS-INQ-001–004 remain proposal/engineering validation; FS-INQ-005 is a validated reference model | Individual FS-INQ files; production transaction guarantees remain open |
| Cross-layer recovery and persistence | **Reference validation only** | PV-16 and PV-17 passes apply to stated reference-model invariants | PV-16/PV-17 manifests; production infrastructure properties remain open |
| G-05 Change Control | **Integrated reference model — focused tests pass** | Lifecycle, scope/provenance integrity, independent verification, release gate, durable history, and audit linkage are exercised through an injected runtime control boundary | `specifications/FS-OPS-005-CHANGE-CONTROL-V1.md`; `production_validation/g05_g06_control/`; production G-09/G-02 binding and authority delegation remain open |
| G-06 Migration Control | **Integrated reference model — focused tests pass** | Authorization, atomic SQLite migration plus history/audit, integrity verification, idempotency, and reversible rollback semantics are exercised | `specifications/FS-OPS-006-MIGRATION-CONTROL-V1.md`; `production_validation/g05_g06_control/`; production storage, authority, and recovery remain open |
| G-08 Certification Evidence | **Integrated reference candidate — focused tests pass; not ratified** | Separate evidence lifecycle binds artifact digest, producer, verifier, result, provenance, idempotency, and shared-boundary audit history; this is not a certification decision | `specifications/FS-CERT-008-CERTIFICATION-EVIDENCE-V1.md`; `production_validation/g08_certification_evidence/`; authority, method qualification, retention, trust anchors, thresholds, and production G-09/G-02 binding remain open |
| G-07 ↔ G-08 evidence boundary | **Fail-closed reference adapter candidate — not full G-07 integration** | Evidence-required resolution callbacks run only when every referenced G-08 record exists, is VERIFIED, and passes audit reconstruction; resolution actor cannot verify the same obligation | `specifications/FS-INT-007-008-EVIDENCE-BOUNDARY-V1.md`; G-07 runtime candidate is absent, so callback lifecycle/durability remains unverified |
| G-07/G-08 crash recovery | **Candidate provenance reconciled; independent SQLite repository reference validated — not production recovery** | Candidate SHA verified and its independent pytest result is 15/15; repository implementation was integrated independently and reports 18/18 crash tests plus 95/95 regression scope | `specifications/FS-INT-008-CRASH-RECOVERY-BOUNDARY-V0.1.md`; `production_validation/g07_g08_crash_recovery/`; power-loss and production G-09/G-02 guarantees remain open |
| Production certification | **NOT CERTIFIED** | A test pass or ratified semantic boundary does not certify deployed production behavior | `OVERALL-PROGRESS-LEDGER.json`; open gates listed there and in REAL-SEM-01 |

## Reconciliation notes

1. The Genesis release notes describe what was not authoritative **at Genesis G-0.1**. Later explicit decisions, such as DEC-OBS-002, govern only their later stated scope; the historical release record is not rewritten.
2. OBS has two distinct authority questions: FS-OBS-002 v1 is ratified as the semantic-safety boundary; the broader state-machine vocabulary request for FS-OBS-001 G0.3 remains open. Keep those scopes separate.
3. The old FS-OBS-002 candidate and change record predate DEC-OBS-002. Their status metadata is being amended with history retained so they no longer present a pending ratification as current.
4. PV-17 passed 12/12 reference-model concurrency/persistence invariants. It is not production database, distributed consensus, crash-recovery, or real-execution certification.
5. The previous README's single “current downstream target” repeated the Genesis-era FS-OBS-001 target as if it were current. Current open gates are summarized above; detail and source references live in the register.

## Remaining high-priority unresolved work

- Ratify or revise the common OBS state-machine vocabulary and define how it composes with the ratified FS-OBS-002 semantic boundary.
- Execute REAL-SEM-01 with representative, independently adjudicated OBS data and the acceptance decisions required by its charter.
- Establish exact numerical governance parameters before cases require them.
- Define and validate production persistence, isolation, crash recovery, distributed coordination, and real execution safety.
- Bind the G-05/G-06 reference control contract to the authoritative G-09 persistence and G-02 audit implementations when those implementations are present and approved; the current branch supplies a SQLite reference boundary only.
- Reconcile the earlier G-08 certification-evidence and G-07/G-08 evidence-boundary candidate ZIPs against their reported SHAs. The separate crash-recovery candidate is reconciled in `FS-INT-008-CRASH-RECOVERY-BOUNDARY-V0.1.md`; integrate the gate into the authoritative G-07 runtime only when that runtime candidate is present and its lifecycle contract can be checked.
- Resolve FD-GOV-008-001 before G-08 evidence is used for a certification decision; no authority, method qualification, retention period, trust anchor, or acceptance threshold is selected here.
- Decide the authoritative release source commit and full manifest for Genesis, then define the release process for post-Genesis engineering work.
