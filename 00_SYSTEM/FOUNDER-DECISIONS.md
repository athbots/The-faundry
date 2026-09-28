# Founder Decision Record — Documentation and Governance

- **Record ID:** FND-DEC-DOC-001
- **Version:** 1.1
- **Status:** Partially resolved — FD-DOC-001 closed; FD-DOC-005 decided in principle; FD-DOC-002 through FD-DOC-004 and FD-DOC-005 implementation details remain open
- **Opened against:** `main` at `dd4676afe15053eedff96747f8195a7472cdcb6b`
- **Related record:** [`DOCUMENTATION-ARCHITECTURE-v1.1.md`](DOCUMENTATION-ARCHITECTURE-v1.1.md)

**Revision history:** v1.1 (2026-09-28) records the Founder-selected FD-DOC-005 taxonomy/identity principles and a proposed path map. No migration is authorized.

This register records decisions after Documentation Architecture v1. FD-DOC-001 is closed by the explicit Founder instruction to implement v1 and reconcile the tree, read together with the earlier instruction to preserve existing implementation directories. On 2026-09-28, the Founder decided the taxonomy relationship and identity distinction under FD-DOC-005; the decision does not assign identifier formats, retroactive IDs, or authorize migration. The current Repository Charter and artifact-level approval history continue to control other open matters.

## FD-DOC-001 — Repository's physical and logical architecture

**Question:** Resolved for v1: how should the intended logical taxonomy relate to the current physical tree?

**Evidence:** At the v1 baseline, the README-described `02_SPECIFICATIONS/` through `06_PROJECTS/` folders were absent. Specification files, implementation, and validation artifacts occupy different current paths. The Founder directed implementation of Architecture v1 and preservation of existing implementation directories.

**Decision:** Adopt the existing physical tree as the navigation baseline. Retain `02_SPECIFICATIONS/` through `06_PROJECTS/` as logical classes only; do not create empty folders or move/rename current implementation directories. Any later physical migration requires a separate decision and a traceable mapping, dependency check, validation, and rollback plan.

**Authority / date:** Founder direction in this task, with the earlier explicit preservation constraint; 2026-09-26.

**Trade-off accepted:** The logical categories improve future classification while physical preservation protects code imports, links, and provenance; readers must consult the actual-tree map until a separately approved migration.

**Implementation:** `00_SYSTEM/DOCUMENTATION-ARCHITECTURE-v1.0.md` and updated root `README.md`.

## FD-DOC-002 — Normative authority of current specifications

**Question:** Beyond existing artifact-specific approval decisions, which specifications are authorized for implementation, and who may authorize them?

**Evidence:** The Genesis release notes describe authority at Genesis G-0.1. Later records include an explicit active ratification of FS-OBS-002 v1 by DEC-OBS-002; older FS-OBS-002 candidate/change records had not reflected that decision. The separate OBS state-machine ratification request remains open. Other FS-DEC/INQ/INT records declare mixed proposal or validated-reference-model states. A repository-wide implementation-authorization matrix does not exist.

**Options:**
- Ratify individually by specification with explicit version and dependencies.
- Ratify an approved set under a single decision, with per-document exceptions.
- Preserve current work as non-normative until each decision is made.

**CISA recommendation:** Maintain artifact-level decisions and the source-linked register; do not infer ratification or implementation authorization from a merge, filename, or passing test. Explicitly resolve the state-machine/semantic-boundary composition and identify the authority for each new approval.

**Trade-off:** Individual decisions take more governance effort but reduce authority ambiguity and make supersession precise.

**Decision:** Pending Founder. **Decision date / authority:** Pending.

## FD-DOC-003 — Change authority and review roles

**Question:** Who may propose, review, approve, and release changes at repository-control, specification, implementation, validation, and foundation layers?

**Evidence:** The charter requires authority appropriate to the affected layer; role-based authority is a resolved foundation principle, but this repository snapshot does not provide a complete role-to-decision delegation table.

**Options:**
- Founder retains all ratification authority until explicit delegation.
- Define delegated authorities by artifact class and risk tier, with reserved Founder decisions.
- Establish a review council with documented quorum, dissent, conflict, and escalation rules.

**CISA recommendation:** Start with a written delegation matrix, reserve constitutional/foundation changes and unresolved cross-layer conflicts to the Founder, and require recorded rationale and dissent for delegated decisions.

**Trade-off:** Central control preserves consistency but creates a bottleneck; delegation increases throughput but requires explicit limits and auditability.

**Decision:** Pending Founder. **Decision date / authority:** Pending.

## FD-DOC-004 — Release scope and freeze boundary

**Question:** What is frozen by `GENESIS-G0.1`, and how should post-Genesis artifacts already present on `main` be identified and released?

**Evidence:** Genesis notes name the foundation artifacts and say the foundation is frozen; `main` has later specification, implementation, and PV-17 records. The release manifest does not list a source commit or complete file manifest.

**Options:**
- Keep Genesis scoped to named foundation artifacts and issue a new release for later work.
- Define a new repository-wide release baseline and explicitly supersede the earlier snapshot metadata.
- Maintain separate foundation releases and engineering snapshots with distinct identifiers and authority.

**CISA recommendation:** Keep foundation releases distinct from engineering snapshots; every release should identify exact commit/tree, included artifact versions, exclusions, and validation state.

**Trade-off:** Separate tracks preserve constitutional stability and engineering iteration, but require clear mapping to prevent version confusion.

**Decision:** Pending Founder. **Decision date / authority:** Pending.

## FD-DOC-005 — Document identity, metadata, and lifecycle vocabulary

**Question:** Which documentation artifacts are governed institutional objects, and what identifiers, required metadata, and lifecycle states apply to each class?

**Evidence:** FM-001 establishes object identity principles; current repository documents and code artifacts use mixed naming and status conventions, and a path is explicitly not an ObjectID.

**Options:**
- Assign ObjectIDs only to governed institutional objects and use a separate document-control key for working specifications and evidence.
- Treat every controlled document as an object under a defined object type.
- Keep status and identity minimal until the object taxonomy is ratified.

**CISA recommendation:** Define classes first, then IDs and lifecycle states per class; avoid equating Git paths or semantic filenames with identity.

**Trade-off:** Rich metadata improves traceability but creates maintenance burden and can imply authority if status terms are not governed.

**Founder decision (2026-09-28):** Adopt option 2 for the taxonomy relationship: retain Documentation Architecture v1.0's logical classes as the primary institutional-function classification and use FS-SYS-002's artifact-type/provenance concepts as a separate, orthogonal classification axis. Evidence is a cross-cutting role that can qualify a validation result or another record. Transfer artifact describes an exchange/transport representation, not the canonical record. Retain Objects and capabilities and Projects. A record may carry more than one classification. This adopts only the crosswalk semantics stated here; it does not ratify FS-SYS-002 as a whole, adopt its filename grammar, or create physical directories.

**Founder decision (2026-09-28):** Adopt option 1 for identity separation. Controlled documents covered by Documentation Architecture v1.0 use a Document Control ID. ObjectID is reserved for an institutional object instance governed under FM-001. A controlled document does not automatically become an institutional object; it may reference an ObjectID without reusing it. Filesystem paths, Git refs, validation-run identifiers, Evidence IDs, Release IDs, and transfer-artifact names remain distinct from both identity classes.

**Decision authority:** Founder direction, “go as recommended,” in the CISA review thread; 2026-09-28. Decision basis: `integration/identity-taxonomy-crosswalk-v0.1` at `6ab4cf49b414f5f9858fb213ab7e686a78bb8220`.

**Scope limits / remaining implementation decisions:** FD-DOC-005 is resolved for the taxonomy relationship and the distinction between document identity and object identity. The exact Document Control ID syntax and granularity, assignment to existing records, per-class required metadata, and lifecycle vocabulary remain open. No ObjectIDs or new Document Control IDs are assigned retroactively by this decision. Current paths and filenames remain unchanged pending a separate physical-migration decision.

**Founder direction — migration planning sequence (2026-09-27):** The Founder directed that the document-identity and taxonomy crosswalk be decided before preparing a mapped physical-migration plan. The direction set sequence only; it did not select naming rules, require migration, authorize file or directory renames, or approve execution. This v1.1 record captures the crosswalk decision and the required proposed map. Preserve existing paths until a separate migration decision is recorded.

## Annex A — Proposed physical-migration map (not authorized for execution)

- **Status:** Proposed planning artifact within this decision record; no files or directories have been moved or renamed.
- **Baseline:** GitHub `main` at `effc241f285c414f1134327bd7dda3140d63f5fe`, inspected 2026-09-28. The tracked tree has 132 paths; `specifications/` has 14 entries (12 Markdown specifications and 2 JSON decision/change records); `production_validation/` has 19 JSON manifests.
- **Inventory boundary:** This map covers only paths present on that exact `main` commit. It excludes artifacts present only on unmerged integration branches, including the FS-SYS-002 candidate integration, G-05/G-06 and G-07/G-08 integration work, and the crosswalk review branch. Before any migration execution is considered, re-inventory the selected source commit and extend or replace this map to include every then-current tracked artifact; this proposal does not imply that excluded branch work is approved for integration.
- **Purpose:** Map the records that could move if a later Founder decision materializes logical classes as physical directories. The selected orthogonal taxonomy does not itself require physical moves.

### Recommended disposition

Keep the current physical tree in place unless the Founder separately authorizes migration. Documentation Architecture v1.0 already makes `specifications/` the physical home for specifications and preserves other paths for navigation, import, and provenance stability. The overlay classification can be recorded in document metadata without changing paths. The table below is a concrete optional mapping if a future physical migration is chosen; it is not a current instruction.

| Current path | Proposed path if migration is separately approved | Classification / reason |
|---|---|---|
| `specifications/FS-DEC-001-DECISION-BOUNDARY-V1.md` | `02_SPECIFICATIONS/FS-DEC-001-DECISION-BOUNDARY-V1.md` | Decision-system specification |
| `specifications/FS-DEC-002-EXECUTION-LOOP-V1.md` | `02_SPECIFICATIONS/FS-DEC-002-EXECUTION-LOOP-V1.md` | Decision/execution specification |
| `specifications/FS-INQ-001-OBS-INQ-INTERFACE-V1.md` | `02_SPECIFICATIONS/FS-INQ-001-OBS-INQ-INTERFACE-V1.md` | Interface specification |
| `specifications/FS-INQ-002-INQUIRY-CORE-V1.md` | `02_SPECIFICATIONS/FS-INQ-002-INQUIRY-CORE-V1.md` | Inquiry specification |
| `specifications/FS-INQ-003-EVIDENCE-AMENDMENT-CONFLICT-V1.md` | `02_SPECIFICATIONS/FS-INQ-003-EVIDENCE-AMENDMENT-CONFLICT-V1.md` | Inquiry/evidence specification |
| `specifications/FS-INQ-004-INVESTIGATION-WORK-PRODUCTS-V1.md` | `02_SPECIFICATIONS/FS-INQ-004-INVESTIGATION-WORK-PRODUCTS-V1.md` | Inquiry specification |
| `specifications/FS-INQ-005-SUPERSESSION-CONCURRENCY-V1.md` | `02_SPECIFICATIONS/FS-INQ-005-SUPERSESSION-CONCURRENCY-V1.md` | Inquiry/integrity specification |
| `specifications/FS-INT-003-FAILURE-RECOVERY-V1.md` | `02_SPECIFICATIONS/FS-INT-003-FAILURE-RECOVERY-V1.md` | Integration specification |
| `specifications/FS-INT-004-CONCURRENCY-PERSISTENCE-V1.md` | `02_SPECIFICATIONS/FS-INT-004-CONCURRENCY-PERSISTENCE-V1.md` | Integration specification |
| `specifications/FS-OBS-002-RATIFICATION-CANDIDATE.md` | `02_SPECIFICATIONS/FS-OBS-002-RATIFICATION-CANDIDATE.md` | Historical candidate specification; retain its status distinction |
| `specifications/FS-OBS-002-SEMANTIC-SAFETY-LAYER-V1.md` | `02_SPECIFICATIONS/FS-OBS-002-SEMANTIC-SAFETY-LAYER-V1.md` | Ratified specification; decision remains a separate record |
| `specifications/REAL-SEM-01.md` | `02_SPECIFICATIONS/REAL-SEM-01.md` | Future validation gate specification |
| `canonical_obs/OBS-CANONICAL-STATE-MACHINE-G0.3.md` | `02_SPECIFICATIONS/OBS-CANONICAL-STATE-MACHINE-G0.3.md` | State-machine specification; its ratification remains pending |
| `specifications/DEC-OBS-002-FS-OBS-002-RATIFICATION.json` | `04_GOVERNANCE/OBS/DEC-OBS-002-FS-OBS-002-RATIFICATION.json` | Domain approval decision record |
| `specifications/FS-OBS-002-CHANGE-RECORD.json` | `04_GOVERNANCE/OBS/FS-OBS-002-CHANGE-RECORD.json` | Domain change/governance record |
| `canonical_obs/RATIFICATION-DECISION-REQUIRED.md` | `04_GOVERNANCE/OBS/RATIFICATION-DECISION-REQUIRED.md` | Open state-machine ratification request |

All other current paths remain at their present locations in this proposal: repository controls under `00_SYSTEM/`, frozen foundation under `01_FOUNDATION/`, release records under `07_RELEASES/`, templates under `99_TEMPLATES/`, code under implementation directories, and validation programs/manifests/outputs under `production_validation/` and `tests/`. No `03_OBJECTS/`, `05_CAPABILITIES/`, or `06_PROJECTS/` directories are proposed because no approved physical inventory requires them. Filename basenames are preserved; this plan does not adopt the FS-SYS-002 filename grammar.

### Dependencies, execution gates, validation, and rollback

Before any move is authorized, create an exhaustive source-to-target manifest with hashes and current Git blob IDs; search and update Markdown links, README maps, document-register paths, manifests, workflow references, import paths, and test fixtures; confirm exact-case paths on a clean checkout; preserve Git history; and validate the destination tree against the approved classification. Run the repository's full relevant validation suite and review every changed reference. No migration commit should be merged until an explicit execution decision records the scope and approver.

If approved migration validation fails, revert the migration commit as one unit, restore the source-path map, and rerun the baseline checks. Keep a pre-migration tag or commit reference and retain the source-to-target manifest with the migration record. Do not use a partial rollback that leaves duplicate or dangling canonical paths.

**Decision still required:** whether to execute any physical move, whether to materialize the logical directories, and whether to adopt any filename convention. The present recommendation is to keep current paths and use the adopted second taxonomy axis as metadata until a measured retrieval or governance need justifies the cost of path churn.

## Closure protocol

For each decision, record the selected option or a custom ruling, rationale, authority, date, affected artifacts, implementation owner, and validation/release evidence. If the Founder rejects every option, preserve the decision as open and state the blocking condition. Update the architecture index only after the relevant decision is recorded.
