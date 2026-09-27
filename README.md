# The Foundry

The Foundry is an institutional operating system for a future engineering and scientific organization. It is intended to preserve how observations become investigated claims, authorized decisions, controlled action, and reviewable learning over time.

The repository represents institutional records and executable models. It is not the institution itself. Its purpose is to keep information, evidence, authority, decisions, execution, and history distinct enough that people can inspect how a claim or action was formed and what remains uncertain.

## Authority and foundation

The authority hierarchy is:

`CONST-001 → IP-001 → FM-001 → ratified type specifications → ratified object instances`

Genesis G-0.1 records the Phase A foundation as frozen. Its release notes name the included artifacts; later engineering records are not automatically part of that release. The foundational documents and Genesis release records remain unchanged from the Genesis tag. The release notes also list Repository Metadata, which has since been updated for later repository state; the Genesis manifest has no source commit or per-file hashes to identify its exact original payload. The [curation audit](00_SYSTEM/REPOSITORY-CURATION-AUDIT-V0.1.md) records this provenance limitation without rewriting Genesis history.

A filename, directory, branch, commit, passing test, or AI-generated output does not create institutional authority. A path is a repository location, not an institutional ObjectID. Governance authority must be recorded by the appropriate decision source.

## Operating model

`OBS → INQ → RESOLUTION → DEC → AUTHORIZATION → EXECUTION → VERIFICATION → OBS`

This is a navigation model for the repository's work. It does not ratify a single lifecycle for every domain. G-07 discovery, for example, found no authoritative obligation runtime yet.

| Term | Meaning in this repository |
|---|---|
| **Observation (OBS)** | A recorded perception of a phenomenon, condition, measurement, or event. It is not, by itself, an explanation. |
| **Inquiry (INQ)** | Structured examination of observations and questions, with methods and work products recorded. |
| **Evidence** | Observations evaluated for relevance and reliability against a claim or inquiry. Evidence can support or challenge a claim; it does not grant authority. |
| **Knowledge** | An institutionally accepted model or conclusion supported sufficiently for its intended use. Its scope and uncertainty remain relevant. |
| **Resolution** | The handling or disposition of an identified obligation or issue. The authoritative G-07 lifecycle and closure rules remain undecided. |
| **Decision (DEC)** | An authorized selection of an action, constraint, allocation, or direction. Evidence and decision authority are distinct. |
| **Authorization** | Explicit, role-based permission for a defined actor and scope to perform an action. |
| **Execution** | The authorized action, with its scope, provenance, and resulting state recorded. |
| **Verification** | An independent check of a specified result or state. A passing verification is evidence for its stated scope, not production certification. |

The foundation's institutional cognition flow remains recorded as Reality → Observation → Triage → Inquiry → Evidence → Knowledge → Governance → Decision → Execution → Reality Feedback. See [IP-001](01_FOUNDATION/IP/IP-001.md) and the [Repository Charter](00_SYSTEM/REPOSITORY-CHARTER.md).

## Current institutional and engineering state

This status is for the current review branch. It carries the pushed G-07 discovery and FS-SYS-002 work, plus a dated status-provenance addendum, while preserving the original commits. The changes have not been merged to `main`; `main` therefore does not yet contain those branch-only records. The status snapshot and progress ledger preserve `b98ed49ccb1e75b941e8611151828788b05d198d` as their original basis and identify the later curation snapshot at `30000ba70cbee7d9da3e172fd27b9b255c0a5766` and `main` at `eb4c82e893afcbf52ed484249b0563f648c49160`. The addendum records provenance only; it does not revalidate status claims.

| State | Current record |
|---|---|
| **Historical / frozen** | Genesis G-0.1 foundation remains frozen within its declared scope. The Genesis-era FS-OBS-001 next target is historical context, not the current roadmap. |
| **Active repository policy** | Documentation Architecture v1.0 defines physical navigation, logical classes, status axes, and traceability. |
| **Ratified, qualified** | FS-OBS-002 v1 semantic-safety boundary is ratified by DEC-OBS-002 within its stated scope. OBS state-machine vocabulary remains ratification pending. |
| **Mandatory, not executed** | REAL-SEM-01 remains an unexecuted gate. |
| **Candidate, not ratified** | FS-SYS-002 proposes artifact identity and naming rules. Its repository validation checks 15 core assertions; it does not change existing identity semantics or authorize renames. |
| **Candidate, not ratified** | The FS-OPS-002 G-07 acceptance contract was reviewed from the verified handoff package and compared in the [G-07 discovery report](G07-AUTHORITATIVE-RUNTIME-DISCOVERY-V0.1.md). The candidate is not integrated as a specification or runtime. |
| **Integrated reference model** | G-05 Change Control and G-06 Migration Control have SQLite reference implementations and focused validation. Production G-09/G-02 binding and authority delegation remain open. |
| **Integrated reference candidate** | G-08 Certification Evidence has a separate evidence lifecycle using the existing SQLite control/audit boundary. It is not ratified or certified. |
| **Fail-closed reference adapter** | The G-07 ↔ G-08 evidence gate validates caller-supplied evidence before invoking caller-owned callbacks. It is not full authoritative G-07 integration. |
| **Integrated SQLite reference candidate** | G-07/G-08 crash recovery preserves atomic state-plus-audit behavior in the reference boundary. The candidate archive SHA-256 is `8d9c13485efaba2e926b10044a59ae3c2051ea888ed366ed4f3d557a41552158`; its 15/15 result was independently reproduced. Repository validation is separately recorded as 18/18 crash tests, a 95/95 affected regression scope, and 113/113 total repository-owned tests in the [result record](production_validation/g07_g08_crash_recovery/G07-G08-CRASH-RECOVERY-BOUNDARY-RESULT-V0.1.md). |

“Implemented” means repository code exists. “Candidate” means a proposed artifact or integration whose authority is not established. “Validated reference” means defined checks passed for the identified implementation and environment. “Ratified” requires an explicit decision record. “Certified” requires the competent authority's certification decision and evidence for its stated production scope. These states are separate.

**C1 is NOT claimed. Production certification is NOT claimed.** No reference-model test result establishes production guarantees.

## Open gates and Founder decisions

The following gates remain open:

1. Authoritative G-07 obligation lifecycle and runtime integration.
2. Production G-09 persistence.
3. Production G-02 audit.
4. Production crash-recovery and power-loss guarantees.
5. G-10 distributed-consistency decision.
6. REAL-SEM-01 execution and its required governance parameters.
7. Exact governance parameters, including unresolved CFO/TEAM weights.
8. G-08 certification authority, thresholds, method qualification, retention, and trust-anchor decisions.
9. Production execution safety.
10. Approved change and migration authority delegation.

Other documented Founder decisions remain open: domain specification approval authority, change/review role delegation, post-Genesis release scope and reproducible release records, and the boundary between document-control identifiers and institutional ObjectIDs. See the [Founder Decision Record](00_SYSTEM/FOUNDER-DECISIONS.md), [Institutional Status](00_SYSTEM/INSTITUTIONAL-STATUS.md), and [curation audit](00_SYSTEM/REPOSITORY-CURATION-AUDIT-V0.1.md).

The current branch preserves, rather than resolves, the FS-SYS-002 conflicts over 16 specification filenames, 21 validation-manifest filenames, status-bearing filenames, identity boundaries, and logical taxonomy. No mass rename or new logical/physical directory is performed.

## Repository map

These are the physical locations in this branch:

- `.github/workflows/` — focused reference test workflow.
- `00_SYSTEM/` — repository charter, metadata, documentation architecture, status, decisions, and document register.
- `01_FOUNDATION/` — Constitution, Institutional Physics, Meta-Model, and Genesis cross-audit.
- `07_RELEASES/` — declared release notes and manifests.
- `99_TEMPLATES/` — reusable institutional record template.
- `canonical_obs/` — OBS implementation, manifest, tests, and state-machine ratification request.
- `dec_core/`, `inq_core/`, `inq_interface/`, `runtime/` — implementation and reference runtime boundaries.
- `specifications/` — domain, integration, and candidate specifications, each with its own authority status.
- `production_validation/` — validation manifests, recorded results, and test programs.
- `tests/` — focused implementation and regression tests.
- `G07-AUTHORITATIVE-RUNTIME-DISCOVERY-V0.1.md` — non-normative runtime discovery report.
- `README.md`, `OVERALL-PROGRESS-LEDGER.json`, `STATUS-PV17.md` — navigation and status summaries; they do not override source records.

`02_SPECIFICATIONS/`, `03_OBJECTS/`, `04_GOVERNANCE/`, `05_CAPABILITIES/`, and `06_PROJECTS/` are logical categories, not physical directories. Documentation Architecture v1.0 preserves the existing physical tree.

## Governance and evidence

Authority comes from the decision process assigned to the affected layer. It does not come from filenames, directories, Git commits, tests, or AI output. Validation evidence establishes only what a named run tested under its recorded environment and scope. Evidence can inform a governance decision; it cannot replace that decision.

The document register indexes high-consequence records. Validation manifests and source records remain controlling for their own claims. The Genesis release manifest does not identify a complete source tree or source commit; this remains a release-provenance gap.

## Engineering workflow

`CISA → validated candidate → FIB integration → branch → repository validation → review → merge/ratification`

- **CISA** performs architecture and adversarial review.
- **FIB** performs repository integration and execution.
- **Founder** holds institutional authority and resolves decisions that remain open.

Repository integration, branch publication, passing tests, merge, ratification, and certification are separate outcomes.

## Historical Genesis G-0.1 next target

The Genesis release notes recorded `FS-OBS-001 — Observation Object Specification` as the next target at that time. This is preserved as historical roadmap context. The current engineering state and open gates above control this README's present status summary.

## Further reading

- [Documentation Architecture v1.0](00_SYSTEM/DOCUMENTATION-ARCHITECTURE-v1.0.md)
- [Institutional and Repository Status](00_SYSTEM/INSTITUTIONAL-STATUS.md)
- [Document Register](00_SYSTEM/DOCUMENT-REGISTER.csv)
- [Founder Decision Record](00_SYSTEM/FOUNDER-DECISIONS.md)
- [Overall Progress Ledger](OVERALL-PROGRESS-LEDGER.json)
- [FS-SYS-002 candidate specification](specifications/FS-SYS-002-INSTITUTIONAL-ARTIFACT-IDENTITY-AND-NAMING-V0.1.md)
- [G-07 authoritative runtime discovery](G07-AUTHORITATIVE-RUNTIME-DISCOVERY-V0.1.md)
- [Repository Curation Audit v0.1](00_SYSTEM/REPOSITORY-CURATION-AUDIT-V0.1.md)
