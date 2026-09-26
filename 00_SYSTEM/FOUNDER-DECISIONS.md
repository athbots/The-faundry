# Founder Decision Record — Documentation and Governance

- **Record ID:** FND-DEC-DOC-001
- **Version:** 0.1
- **Status:** Open — Founder decision required
- **Opened against:** `main` at `dd4676afe15053eedff96747f8195a7472cdcb6b`
- **Related record:** [`DOCUMENTATION-ARCHITECTURE-v0.1.md`](DOCUMENTATION-ARCHITECTURE-v0.1.md)

This is a decision register, not a ratification. No option below is adopted. The current Repository Charter and artifact-level approval history continue to control while these items are open.

## FD-DOC-001 — Repository's physical and logical architecture

**Question:** Is the directory layout in the root README a ratified target, or should the existing physical layout become the architecture baseline?

**Evidence:** The README lists `02_SPECIFICATIONS/` through `06_PROJECTS/`; those directories are absent from inspected `main`. Specs are under `specifications/`; implementation and validation have top-level directories.

**Options:**
- Ratify the README layout as target and approve a staged migration plan.
- Amend the README to describe the existing tree and defer target folder creation until governed objects require it.
- Adopt a third logical architecture without requiring immediate physical migration.

**CISA recommendation:** Choose a logical architecture first; treat physical paths as representations and migrate only when a traceable mapping, dependency check, and rollback plan exist.

**Trade-off:** A future uniform taxonomy improves onboarding and findability; migrating prematurely can obscure history, break tooling and references, and produce empty or misleading folders.

**Decision:** Pending Founder. **Decision date / authority:** Pending.

## FD-DOC-002 — Normative authority of current specifications

**Question:** Which existing specifications are approved for implementation, and which remain candidates, drafts, historical records, or superseded?

**Evidence:** README and Genesis release notes say OBS/INQ/EVD/DEC/CAP/STD/SPEC specifications are not yet authoritative in that release, while current `main` includes many `FS-*` files and implementation/validation work. `canonical_obs/RATIFICATION-DECISION-REQUIRED.md` says OBS ratification is still required. The current state cannot be inferred safely from filenames or code.

**Options:**
- Ratify individually by specification with explicit version and dependencies.
- Ratify an approved set under a single decision, with per-document exceptions.
- Preserve current work as non-normative until each decision is made.

**CISA recommendation:** Use artifact-level decisions and record status per version; maintain a compact index of implementation-authorized versions. Do not infer ratification from merging or passing tests.

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

## Closure protocol

For each decision, record the selected option or a custom ruling, rationale, authority, date, affected artifacts, implementation owner, and validation/release evidence. If the Founder rejects every option, preserve the decision as open and state the blocking condition. Update the architecture index only after the relevant decision is recorded.
