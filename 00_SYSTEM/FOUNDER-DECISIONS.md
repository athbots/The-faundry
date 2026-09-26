# Founder Decision Record — Documentation and Governance

- **Record ID:** FND-DEC-DOC-001
- **Version:** 1.0
- **Status:** Partially resolved — FD-DOC-001 closed; FD-DOC-002 through FD-DOC-005 remain open
- **Opened against:** `main` at `dd4676afe15053eedff96747f8195a7472cdcb6b`
- **Related record:** [`DOCUMENTATION-ARCHITECTURE-v1.0.md`](DOCUMENTATION-ARCHITECTURE-v1.0.md)

This register records decisions that remain open after Documentation Architecture v1. FD-DOC-001 is closed by the explicit Founder instruction to implement v1 and reconcile the tree, read together with the earlier instruction to preserve existing implementation directories. The current Repository Charter and artifact-level approval history continue to control other open matters.

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

**Decision:** Pending Founder. **Decision date / authority:** Pending.

## FD-GOV-008-001 — Certification evidence authority and acceptance

**Question:** Which roles may produce, independently verify, accept, retain, invalidate, and rely on G-08 evidence, and what approved rules govern those decisions?

**Evidence:** The G-08 reference candidate records producer provenance, artifact digest, verification method, verifier, result, and audit history. This repository integration uses an injected authorization policy and a verifier-supplied PASS/FAIL result. It does not define role delegation, method qualification, retention, external trust anchors, or certification thresholds. The associated candidate archives were not available in this checkout for byte-level reconciliation.

**Options:**
- Approve a role and independence matrix, evidence classes, method requirements, and retention rules in a separate governance decision.
- Continue with caller-injected authority and treat the implementation as a non-normative reference candidate until those decisions are made.
- Reject or revise the proposed G-08 lifecycle before authorizing implementation.

**CISA recommendation:** Keep this integration at reference-candidate status; separately ratify authority, evidence-method, retention, invalidation, and acceptance rules before certification use.

**Trade-off:** An injected authority seam supports testing without silently selecting decision makers, but leaves the reference implementation unusable as a self-contained certification authority.

**Decision:** Pending Founder. No numerical threshold or authority was inferred. **Decision date / authority:** Pending.

## Closure protocol

For each decision, record the selected option or a custom ruling, rationale, authority, date, affected artifacts, implementation owner, and validation/release evidence. If the Founder rejects every option, preserve the decision as open and state the blocking condition. Update the architecture index only after the relevant decision is recorded.
