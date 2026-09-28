# Institutional and Repository Status

- **Status date:** 2026-09-26
- **Status basis:** `main` at `b98ed49ccb1e75b941e8611151828788b05d198d` before this reconciliation commit
- **Control source:** [`DOCUMENTATION-ARCHITECTURE-v1.1.md`](DOCUMENTATION-ARCHITECTURE-v1.1.md)
- **Detail register:** [`DOCUMENT-REGISTER.csv`](DOCUMENT-REGISTER.csv)

This page is a dated status snapshot, not a new ratification. Where a summary conflicts with a decision, release note, or validation manifest, the cited controlling record governs within its stated scope.

## Dated amendment — 2026-09-28

On review branch `integration/fd-doc-005-crosswalk-migration-plan-v0.1`, Founder Decision Record `FND-DEC-DOC-001` v1.1 records the FD-DOC-005 taxonomy and identity decisions. In this branch, Documentation Architecture v1.1 is the successor policy. Current `main` remains at the v1.0 baseline until a later integration decision. The successor retains the v1.0 physical tree and logical classes, adds the limited FS-SYS-002 crosswalk as an orthogonal artifact-type/provenance axis, and distinguishes Document Control IDs from ObjectIDs. The mapped physical-migration proposal is not execution authority; no paths have changed. This amendment updates only these documentation-architecture and identity claims. It does not revalidate the other 2026-09-26 status entries or change their original basis.

## Current state

| Area | Current status | What that status means | Controlling record / open gate |
|---|---|---|---|
| Foundation | **Frozen — Genesis G-0.1** | Phase A foundation set is frozen for downstream work; later files on `main` are not thereby included in Genesis | `07_RELEASES/GENESIS-G0.1/RELEASE-NOTES.md`; exact source commit/full manifest remain unresolved |
| Documentation architecture | **Active — v1.1** | Preserves v1.0's physical tree/logical classes; adds the orthogonal artifact-type/provenance axis and identity distinction | `00_SYSTEM/DOCUMENTATION-ARCHITECTURE-v1.1.md`; `FOUNDER-DECISIONS.md` |
| OBS state-machine vocabulary | **Ratification pending** | The request to declare FS-OBS-001 G0.3 the single implementation state machine remains open | `canonical_obs/RATIFICATION-DECISION-REQUIRED.md`; `canonical_obs/MANIFEST.json` |
| OBS semantic-safety boundary | **Ratified — FS-OBS-002 v1** | Ratified by DEC-OBS-002 within the semantic-safety scope; does not settle state-machine vocabulary or general semantic certification | `specifications/DEC-OBS-002-FS-OBS-002-RATIFICATION.json`; `specifications/FS-OBS-002-SEMANTIC-SAFETY-LAYER-V1.md` |
| REAL-SEM-01 | **Mandatory gate — not executed** | No production-grade general semantic-understanding claim or certification | `specifications/REAL-SEM-01.md` |
| DEC | **Validated reference models** | FS-DEC-001/002 headers record reference-model validation; exact CFO/TEAM weights remain unratified | `specifications/FS-DEC-001-DECISION-BOUNDARY-V1.md`; `OVERALL-PROGRESS-LEDGER.json` |
| INQ | **Mixed: proposals and validated reference model** | FS-INQ-001–004 remain proposal/engineering validation; FS-INQ-005 is a validated reference model | Individual FS-INQ files; production transaction guarantees remain open |
| Cross-layer recovery and persistence | **Reference validation only** | PV-16 and PV-17 passes apply to stated reference-model invariants | PV-16/PV-17 manifests; production infrastructure properties remain open |
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
- Decide the authoritative release source commit and full manifest for Genesis, then define the release process for post-Genesis engineering work.
