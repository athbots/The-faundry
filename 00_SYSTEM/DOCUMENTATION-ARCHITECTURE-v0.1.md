# Documentation Architecture and Control Index

- **Document ID:** FND-DOC-ARCH-001
- **Version:** 0.1
- **Status:** Draft for Founder review
- **Baseline:** `main` at `dd4676afe15053eedff96747f8195a7472cdcb6b` (2026-08-24)
- **Authority boundary:** This document is subordinate to `00_SYSTEM/REPOSITORY-CHARTER.md`, `CONST-001`, `IP-001`, and `FM-001`.

## 1. Purpose

This index establishes how readers should locate, interpret, and trace documentation in the repository as it exists today. It is a routing and control layer. It does not ratify the repository's future folder layout, change the authority of existing artifacts, or declare unratified specifications canonical.

## 2. What is already decided

- The repository is a representation layer, not the institution itself.
- The locked authority stack is `CONST-001 → IP-001 → FM-001 → Type Specifications → Object Instances`.
- Frozen foundation artifacts are not silently edited in place; changes must preserve history, identify impacts, and receive the authority appropriate to the affected layer.
- A path, filename, branch, tag, or commit is not an institutional `ObjectID`.
- The current README presents `02_SPECIFICATIONS/`, `03_OBJECTS/`, `04_GOVERNANCE/`, `05_CAPABILITIES/`, and `06_PROJECTS/` as the repository layout, but those directories are absent from the inspected `main` tree. The actual specification files are in `specifications/`; implementation, validation, and release records also live in separate top-level directories.

## 3. Current repository map (observed, not a target design)

| Location | Current role | Control interpretation |
|---|---|---|
| `00_SYSTEM/` | Repository charter and metadata | Repository operating rules; subordinate to institutional constitutional authority |
| `01_FOUNDATION/` | CONST, IP, FM, and Genesis cross-audit | Frozen foundation per Genesis G-0.1 records |
| `specifications/` | FS-DEC, FS-INQ, FS-OBS, integration specifications, and related records | Specification artifacts; each file's own status and ratification record govern its use |
| `canonical_obs/` | OBS state machine, semantic relation, authority implementation, manifest, and ratification-required record | Code and governance evidence adjacent to one implemented domain; not a general documentation tier |
| `dec_core/`, `inq_core/`, `inq_interface/`, `runtime/` | Implementation | Executable representations; not normative authority by code presence alone |
| `production_validation/`, `tests/` | Validation plans, manifests, results, and automated checks | Evidence with scope limited to the artifact, build, and conditions recorded in each manifest |
| `07_RELEASES/` | Genesis G-0.1 release notes and manifest | Release snapshots and their declared scope |
| `99_TEMPLATES/` | Object template | Reusable form; not an authoritative instance |
| Root files | README, progress ledger, and current status note | Navigation and status summaries; reconcile against controlling records before relying on them |

This inventory is a snapshot, not a guarantee that these folders are complete or mutually exclusive. No existing implementation directory is to be deleted, renamed, or moved as a consequence of this document.

## 4. Documentation classes and reading order

When records disagree, follow the authority hierarchy in the Repository Charter and the specific ratification/supersession history of the affected artifact. A convenient location or newer commit does not by itself confer authority.

1. **Constitutional and foundational authority:** `01_FOUNDATION/CONST/`, `IP/`, `FM/`, and approved foundation decisions.
2. **Repository control:** `00_SYSTEM/`, within the limits set by foundation authority.
3. **Normative specifications:** files in `specifications/` only to the extent their own status and approval permit.
4. **Institutional instances and decisions:** governed records with identity, authority, relationships, validation, and history as applicable.
5. **Implementation:** code expresses a design but does not ratify it.
6. **Validation evidence:** supports only its stated scope, version, and conditions; passing tests are not production certification unless an authorized decision says so.
7. **Releases and exports:** snapshots of identified repository states, not new authority unless their release record explicitly grants it.
8. **Templates and summaries:** aids to creation and navigation; never substitutes for the controlling record.

## 5. Minimum traceability for new controlled documentation

Before a new document is treated as controlled, its record should make discoverable:

- stable institutional identifier when the artifact is an institutional object; do not use its path as identity;
- title, version, lifecycle status, and effective date or explicit absence of one;
- issuing/approval authority and the decision or delegation that supports it;
- purpose, scope, and explicit exclusions;
- governing sources and dependencies;
- relationships to replaced, superseded, implementing, or validating artifacts;
- validation method and evidence, or a clear statement that validation has not occurred;
- change history that distinguishes proposal, approval, and implementation.

Until the Founder ratifies a complete metadata schema and status vocabulary, this list is a review checklist, not a claim that every legacy file already conforms.

## 6. Change route

For controlled documentation changes: identify the source and affected authority; state the proposed change and reason; map dependencies and contradictory records; obtain review and the required decision; preserve the prior version and record the decision; update the artifact and its index links; validate the affected claims; then include it in a release record if release policy requires it. Keep proposal, decision, implementation, and validation as distinguishable events.

Do not use a README edit, code change, passing test, or Git commit alone as evidence of institutional ratification. When an authority conflict exists, record it and stop the affected downstream work until the proper decision is made.

## 7. Release and status interpretation

`GENESIS-G0.1` identifies a foundation-frozen release in the release records. It does not, by itself, mean that every document later present in `main` belongs to that release or is ratified. The current tree contains later specification and production-validation work; its inclusion, authority, and relationship to the release require explicit provenance and release-scope decisions.

Likewise, root status summaries are navigation aids. For example, README language calling Phase A complete and the ledger's PV-17 result do not establish production certification; the ledger explicitly lists open certification gates. Use the artifact's own approval and evidence records for decisions.

## 8. Known risks and trade-offs

- **Risk — mixed physical and conceptual structure:** Readers can confuse target folders in README with folders that exist, or mistake code adjacency for normative authority.
- **Risk — release boundary ambiguity:** Current `main` contains substantial work beyond the foundation documents named in the Genesis release notes; without a baseline-to-release manifest, frozen scope can be misread.
- **Risk — document authority drift:** “Canonical” is used in some artifact names/statuses while another file still says ratification is required. Indexing cannot resolve that conflict.
- **Trade-off — defer migration:** Keeping paths intact preserves history and reduces accidental breakage, but leaves navigation less uniform until a founder decision and migration plan exist.
- **Better alternative to bulk reorganization:** Ratify a logical architecture and migration policy first; then migrate in traceable, reviewable batches with redirects or durable references and a manifest mapping old to new paths.

## 9. Open governance dependencies

See [`FOUNDER-DECISIONS.md`](FOUNDER-DECISIONS.md). Until those decisions are resolved, this index is a draft routing control and the existing charter and artifact-level authority remain controlling.

## 10. Self-critique

This index improves discoverability but cannot establish whether the current live tree matches the historical Genesis G-0.1 release artifact, nor settle the contradictory OBS ratification status. The mapping is based on the inspected Git tree and selected controlling files; it is intentionally not an exhaustive audit of every document. Its weakest point is the use of a practical reading order before the Founder has approved a unified document taxonomy. That order is explicitly provisional and should be replaced if it conflicts with ratified authority.
