# Documentation Architecture v1.1

- **Document ID:** FND-DOC-ARCH-001
- **Version:** 1.1
- **Status:** Founder-approved policy implementation; branch-only pending main integration
- **Effective basis:** Documentation Architecture v1.0 plus Founder decision FD-DOC-005 recorded 2026-09-28 in `00_SYSTEM/FOUNDER-DECISIONS.md`
- **Supersedes:** `00_SYSTEM/DOCUMENTATION-ARCHITECTURE-v1.0.md` for the Founder-decided identity/taxonomy relationship once integrated; v1.0 remains current on main until merge and is retained as history
- **Authority boundary:** Subordinate to `CONST-001`, `IP-001`, `FM-001`, and `00_SYSTEM/REPOSITORY-CHARTER.md`; this architecture does not ratify domain specifications or production claims.

## 1. Purpose and scope

This document defines how the repository is organized, how controlled records are located and related, and how their status is reported. It applies to the repository's documentation, specifications, decisions, implementation references, validation evidence, and release records.

The architecture distinguishes three things that the repository previously conflated:

1. **Institutional authority:** what has been decided or ratified, by whom, and within what scope.
2. **Repository location:** where a representation is stored. A path is navigation, not authority or ObjectID.
3. **Engineering evidence:** what a specific model, build, or test demonstrated under stated conditions. A pass is not ratification or production certification.

This version preserves the authority boundaries in the Repository Charter. The physical tree and primary logical classes remain as v1.0 established. FD-DOC-005 adds an orthogonal artifact-type/provenance axis and clarifies the distinction between Document Control IDs and ObjectIDs. This policy does not ratify unrelated domain proposals or certify implementation. Exact identifier syntax/granularity and class-specific lifecycle/metadata details remain open.

## 2. Foundational control rules

- Authority order remains `CONST-001 → IP-001 → FM-001 → ratified type specifications → ratified object instances`.
- Repository controls and this architecture cannot override foundation authority.
- A proposal, test result, code path, README statement, Git commit, or release label cannot substitute for the approval required by the affected authority layer.
- Frozen foundation files are revised through controlled, versioned change; they are not silently edited to conceal a change.
- Preserve historical records. Correct a stale status by adding a dated, traceable amendment or supersession note that retains the earlier state and names its controlling successor.
- Keep the distinction between a state-machine specification and a semantic-safety specification when recording OBS authority.
- Do not move, delete, or rename existing implementation directories as a consequence of this architecture.

## 3. Physical repository map — current and authoritative for navigation

This is the actual physical organization at the v1 baseline. Paths are preserved; this table does not imply that every artifact in a location has the same authority.

| Current path | Repository function | Status rule |
|---|---|---|
| `00_SYSTEM/` | Repository charter, metadata, architecture, status register, and repository-level decisions | Repository operating controls; subordinate to the foundation |
| `01_FOUNDATION/` | Constitution, Institutional Physics, Meta-Model, and foundation audits | Genesis G-0.1 frozen foundation; changes require its controlled revision path |
| `07_RELEASES/` | Release notes and manifests | Each release covers only its declared contents and scope |
| `99_TEMPLATES/` | Reusable object and record templates | Templates guide creation; they do not confer authority on instances |
| `specifications/` | Type, interface, semantic-safety, and integration specifications | Each version's own approval and supersession record controls |
| `canonical_obs/` | OBS state-machine/semantic implementation, manifests, tests, and an open state-machine ratification request | Code and local status evidence; not a substitute for the applicable ratification decision |
| `dec_core/`, `inq_core/`, `inq_interface/`, `runtime/` | Executable reference and integration implementation | Implementation representation; authority is inherited from approved specifications only within their scope |
| `production_validation/`, `tests/` | Validation manifests, test programs, and test outputs | Evidence is limited to recorded scope, version, and conditions |
| Root status and navigation files | `README.md`, `OVERALL-PROGRESS-LEDGER.json`, `STATUS-PV17.md` | Summaries and indexes; defer to the records they cite |

`02_SPECIFICATIONS/`, `03_OBJECTS/`, `04_GOVERNANCE/`, `05_CAPABILITIES/`, and `06_PROJECTS/` are logical categories retained from the earlier proposed map. They are not current physical directories. Do not create empty directories to make a diagram appear complete. Any future physical migration requires a separately recorded decision, dependency map, path mapping, validation, and rollback plan.

## 4. Logical information architecture

The logical model is a classification of records, not a mandated one-to-one directory scheme:

| Logical class | Existing primary location(s) | Intended contents |
|---|---|---|
| System control | `00_SYSTEM/` | Repository policy, architecture, status indexes, repository-scope decisions |
| Foundation | `01_FOUNDATION/` | Constitutional and architectural foundations, audits, controlled amendments |
| Specifications | `specifications/` | Normative candidates and approved type/integration specifications; status is per version |
| Governance decisions | `00_SYSTEM/` for repository-wide decisions; source domain locations for domain decisions | Decision, authority, rationale, scope, effective date, dependencies, and supersession |
| Objects and capabilities | No dedicated current directory | Add only when the object taxonomy and governing specification establish a need; do not create placeholder folders |
| Projects | No dedicated current directory | Add when governed project records exist and their lifecycle is defined |
| Implementation | `canonical_obs/`, `dec_core/`, `inq_core/`, `inq_interface/`, `runtime/` | Executable representations, with explicit links to specification versions |
| Validation | `production_validation/`, `tests/` | Test designs, run manifests, results, limitations, and certification evidence |
| Releases | `07_RELEASES/` | Reproducible snapshots with exact source commit/tree, included artifacts, exclusions, and validation state |
| Templates | `99_TEMPLATES/` | Controlled starting forms with owner, version, and applicable artifact class |

The logical classification permits future growth without forcing premature folder creation or breaking code imports and historical links.

### 4.1 Orthogonal artifact-type and provenance classification

The primary classes above continue to describe institutional function. The Founder selected the FS-SYS-002 concepts as a separate classification axis, not as replacements for those classes. This adopts only the crosswalk semantics stated here; it does not ratify FS-SYS-002 as a whole. A record may carry both a primary class and one or more artifact-type/provenance labels.

- **Evidence** is a cross-cutting role that may qualify a validation result or another record; it is not limited to a single physical directory.
- **Transfer artifact** describes an exchange or transport representation. It does not replace the canonical record it carries.
- **Objects and capabilities** and **Projects** remain logical classes even though no dedicated physical directory currently exists.
- Classification does not establish authority, lifecycle state, identity, or certification. FS-SYS-002's proposed filename grammar is not adopted by this decision.

## 5. Status model

Status is reported on separate axes. Do not compress approval, engineering validation, and deployment certification into one word.

### 5.1 Document authority/lifecycle axis

- **PROPOSED:** submitted for review; no authority to govern implementation.
- **RATIFICATION PENDING:** an explicit approval decision is required and not recorded.
- **RATIFIED:** an identified authority approved a specific version and scope. Record the decision reference and qualifications.
- **SUPERSEDED:** replaced for the named scope by a later record; preserve this version as history.
- **HISTORICAL:** retained for provenance; not a current instruction.
- **OPEN DECISION:** an identified decision is unresolved; do not infer an answer from implementation.

### 5.2 Engineering evidence axis

- **NOT VALIDATED:** no relevant validation is recorded.
- **PROPOSAL / ENGINEERING VALIDATION:** technical validation is in progress or incomplete.
- **VALIDATED REFERENCE MODEL:** stated reference-model tests pass; this does not establish production deployment properties.
- **PASS / FAIL:** test outcome for the specifically identified validation run only.

### 5.3 Operational/certification axis

- **NOT CERTIFIED:** no production certification decision exists.
- **CERTIFIED:** only when the competent authority records scope, evidence, conditions, and effective period.
- **GATE OPEN:** an identified mandatory condition remains unmet or unverified.

Status authority follows this order: a valid decision record for its stated scope; an artifact's approval metadata; a release record for its snapshot; a validation manifest for the run; then index and README summaries. Newer timestamps alone do not supersede higher-authority records.

## 6. Current reconciled status baseline

The live status snapshot is maintained in [`INSTITUTIONAL-STATUS.md`](INSTITUTIONAL-STATUS.md), with the decision-sensitive artifact register in [`DOCUMENT-REGISTER.csv`](DOCUMENT-REGISTER.csv). At this v1 baseline:

- **Foundation:** Genesis G-0.1 records the Phase A foundation as frozen. Its release notes name the included foundation documents; later files on `main` are not automatically members of that release.
- **OBS state machine:** the repository's state-machine ratification request remains open in `canonical_obs/RATIFICATION-DECISION-REQUIRED.md` and its manifest. Do not mistake it for the separate semantic-safety decision.
- **OBS semantic safety:** `FS-OBS-002 v1` is ratified for the semantic-safety boundary by `DEC-OBS-002`. This does not ratify every OBS state-machine vocabulary and does not certify general semantic understanding.
- **REAL-SEM-01:** mandatory future gate; not executed. Production semantic certification remains prohibited until an authorized gate decision changes this status.
- **DEC and INQ:** each file retains its declared proposal or validated-reference-model status. A validated model is not a ratified organizational policy.
- **PV-17:** 12/12 reference-model concurrency/persistence invariants pass. Production database durability/isolation, distributed consensus, crash recovery, real execution safety, exact governance weights, and REAL-SEM-01 remain open; production is not certified.
- **Documentation architecture:** The Founder has decided the orthogonal taxonomy relationship and conceptual Document Control ID/ObjectID distinction. Exact ID syntax/granularity, class-level metadata/lifecycle rules, specification authority, approval delegations, and complete release provenance remain open. This v1.1 implementation is on a review branch; current `main` remains at v1.0 until merge.

## 7. Traceability requirements

For every new controlled document, record:

1. a Document Control ID; use a separate `ObjectID` only when the artifact is an institutional object instance governed under FM-001. A controlled document does not automatically receive an ObjectID and may reference one without reusing it;
2. title, version, lifecycle/authority status, and effective date or explicit absence;
3. approving authority and decision reference, or explicit `PROPOSED` / `RATIFICATION PENDING` state;
4. purpose, scope, exclusions, and governing sources;
5. dependencies and relationships to predecessor, implementation, validation, and release records;
6. evidence and limitations, or an explicit statement that validation has not occurred;
7. dated revision history distinguishing proposal, decision, implementation, and validation.

The `DOCUMENT-REGISTER.csv` is the maintained index for high-consequence normative, governance, release, and certification records. It is not an inventory of every source file, test output, or generated artifact. Every row must link to a controlling record and include scope qualifications. The status snapshot is an explanation; the controlling artifacts remain authoritative. Document Control ID syntax, whether an ID names a series or an individual version, and any retroactive assignment remain open under FD-DOC-005; this version assigns no new IDs.

## 8. Change and release workflow

For a controlled change: identify the current source of authority; define the requested change and reason; list impacted artifacts and contradictions; obtain the authority required for the affected layer; record the decision and dissent; revise with history preserved; update the register and status snapshot; validate only the affected claims; and release a reproducible snapshot where required.

Every release record must identify the source commit and tree, included artifact versions, exclusions, validation run identifiers, open gates, and release authority. A Git tag or commit hash is provenance evidence, not an institutional object identity or ratification by itself.

## 9. Founder decisions carried forward

`FOUNDER-DECISIONS.md` records which choices this version implements and which remain open. FD-DOC-001 continues to preserve current paths and treat the numeric map as logical classification unless a later migration decision says otherwise. FD-DOC-005 now adopts the orthogonal artifact-type/provenance axis and separates Document Control IDs from ObjectIDs. A proposed path map is recorded in Annex A of the Founder Decision Record; it is not authorization to move or rename files. Domain-specification ratification beyond explicit existing decisions, change-authority delegation, complete Genesis source snapshot/release policy, and the remaining FD-DOC-005 implementation details are still open.

## 10. Risks, trade-offs, and self-critique

- **Risk:** inconsistent legacy labels can still mislead readers; the register and status page reduce ambiguity but cannot change authority in the underlying decisions.
- **Risk:** the Genesis manifest has no source commit or full file manifest, so exact historical reproducibility remains unresolved.
- **Trade-off:** retaining the existing physical tree protects links, imports, and provenance but requires readers to use a logical map across technical directories.
- **Alternative considered:** bulk migration into `02_*` to `06_*` folders would improve superficial uniformity but would create path churn before authority and object taxonomies are settled; staged mapping is safer and more traceable.
- **Self-critique:** the second classification axis adds assignment work and can become confusing without class rules. This architecture cannot determine who may ratify future domain specifications, prove that all historical claims are correct, or close production gates. The status register is curated and can drift; each entry therefore names its source, and any status change must be made against that source rather than copied from a summary.

## Revision history

- **v1.1 — 2026-09-28:** records the Founder-selected orthogonal taxonomy relationship and Document Control ID/ObjectID distinction. Preserves the current physical tree. Exact ID format/granularity, class-specific metadata/lifecycle details, and physical migration execution remain open. Founder-approved implementation is branch-only pending main integration.
