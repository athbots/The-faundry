# FS-SYS-002 — Institutional Artifact Identity & Repository Taxonomy v0.1

**Status:** CANDIDATE — NOT RATIFIED
**Purpose:** Prevent identity, location, provenance, validation, and transfer-artifact concepts from being silently substituted for one another.
**Candidate source archive:** `the-foundry-fs-sys-002-artifact-identity-taxonomy-candidate-v0.1.zip`
**Candidate archive SHA-256:** `926feeb34314bd8482813c6566964e6484e622d9bdd7475b700ccf0e1152c40e`
**Transfer package SHA-256:** `539e6702846c057b1ebb8b33ea07fb05ddfb228d3445155d6d8aca9b9b90f3ab6b`
**Candidate validation reported:** 15/15 PASS; repository reproduction is recorded separately below and in the document register.

## 1. Core rule

The Foundry MUST distinguish the following identities:

| Identity | Meaning | May substitute for another? |
|---|---|---|
| Document Control ID | Stable identifier for a controlled document/record | No |
| Institutional ObjectID | Identity of a governed institutional object under FM-001 | No |
| Filesystem Path | Repository navigation/location | No |
| Git Commit/Branch | Version-control provenance | No |
| Validation Run ID | Identity of a specific validation execution | No |
| Evidence ID | Identity of a certification/evidence record | No |
| Release ID | Identity of a declared release snapshot | No |
| Transfer Artifact Name | Name of an archive exchanged between environments | No |

References between these identities MUST be explicit.

## 2. Naming grammar

Controlled specifications:
`FS-<DOMAIN>-<NNN>-<DESCRIPTIVE-TITLE>-V<MAJOR>.<MINOR>.<EXT>`

Validation records:
`<SCOPE>-<DESCRIPTIVE-PURPOSE>-RESULT-V<MAJOR>.<MINOR>.md`

Validation manifests:
`PV-<NNN>-<DESCRIPTIVE-PURPOSE>-V<MAJOR>.<MINOR>.json`

Python tests:
`test_<descriptive_subject>.py`

Integration branches:
`integration/<descriptive-purpose>-v<major>.<minor>`

Candidate transfer archives:
`the-foundry-<descriptive-capability>-candidate-v<major>.<minor>.zip`

Names MUST be descriptive, stable, and machine-safe. Names such as `final`, `new`, `tmp`, `test2`, `candidate-final`, or opaque random directory names MUST NOT be used for controlled artifacts.

## 3. Relationship rules

Every controlled specification MUST identify its implementation, validation evidence, dependencies, and supersession/precedence relationships where applicable.

A Git commit proves repository provenance; it does not itself ratify a document.

A validation pass proves only the claim and conditions recorded by its validation record; it does not confer institutional authority.

A transfer archive is a transport artifact; it is not the canonical repository record unless an explicit release policy says otherwise.

## 4. Status separation

Identity MUST remain separate from lifecycle status. A filename or identifier MUST NOT encode whether an artifact is ratified, certified, current, or obsolete.

Approval, engineering validation, and operational certification MUST remain separately represented.

## 5. Repository taxonomy

Current physical paths remain authoritative for navigation under Documentation Architecture v1.0. This specification does not require directory migration.

Logical classes are:
- System control
- Foundation
- Specification
- Governance decision
- Implementation
- Validation
- Evidence
- Release
- Template
- Transfer artifact

New physical directories MUST NOT be created solely to make the logical taxonomy visually complete.

## 6. Change control

Renaming a controlled artifact MUST preserve predecessor identity, history, references, and rationale. A rename is not a new institutional object merely because its path changed.

Changing a Document Control ID requires explicit change authority and a preserved mapping from old to new identity.

## 7. Self-critique and limits

This candidate does not define institutional ObjectID semantics beyond the existing FM-001 boundary. It does not define governance authority, certification thresholds, release approval, or production storage. Those remain separate decisions.

## 8. Repository reconciliation observations — open, not resolved

This section records the comparison against repository commit `7a34a6f22f776621782726474de143cfaa0c9b79`. It does not amend the existing artifacts or make this candidate authoritative.

### Existing identity semantics

No direct contradiction with frozen `IP-004` was identified: that principle requires permanent institutional object identity independent of representation, revision, owner, or storage; this candidate explicitly leaves ObjectID semantics to FM-001. Documentation Architecture v1.0 also says a repository path is navigation, not an ObjectID, and requires a document-control identifier while reserving ObjectID for artifacts that are institutional objects. The related Founder decision FD-DOC-005 remains pending, so this candidate does not decide which controlled documents also receive an ObjectID.

### Taxonomy crosswalk conflict

Documentation Architecture v1.0 classifies certification evidence within the `Validation` logical class and separately lists `Objects and capabilities` and `Projects`. This candidate lists `Evidence` as a separate logical class, adds `Transfer artifact`, and does not list `Objects and capabilities` or `Projects`. The records do not say whether this is intended as a finer-grained sub-taxonomy, an extension, or a replacement. Keep both classifications visible until an authorized crosswalk decision is recorded. No logical or physical directory was added.

### Existing controlled-specification filename conflicts

The proposed strict `V<MAJOR>.<MINOR>` specification grammar does not match these existing names, which use `V1`, lack a version, or otherwise lack the proposed version segment:

- `specifications/FS-CERT-008-CERTIFICATION-EVIDENCE-V1.md`
- `specifications/FS-DEC-001-DECISION-BOUNDARY-V1.md`
- `specifications/FS-DEC-002-EXECUTION-LOOP-V1.md`
- `specifications/FS-INQ-001-OBS-INQ-INTERFACE-V1.md`
- `specifications/FS-INQ-002-INQUIRY-CORE-V1.md`
- `specifications/FS-INQ-003-EVIDENCE-AMENDMENT-CONFLICT-V1.md`
- `specifications/FS-INQ-004-INVESTIGATION-WORK-PRODUCTS-V1.md`
- `specifications/FS-INQ-005-SUPERSESSION-CONCURRENCY-V1.md`
- `specifications/FS-INT-003-FAILURE-RECOVERY-V1.md`
- `specifications/FS-INT-004-CONCURRENCY-PERSISTENCE-V1.md`
- `specifications/FS-INT-007-008-EVIDENCE-BOUNDARY-V1.md`
- `specifications/FS-OBS-002-RATIFICATION-CANDIDATE.md`
- `specifications/FS-OBS-002-SEMANTIC-SAFETY-LAYER-V1.md`
- `specifications/FS-OPS-005-CHANGE-CONTROL-V1.md`
- `specifications/FS-OPS-006-MIGRATION-CONTROL-V1.md`
- `specifications/REAL-SEM-01.md`

The existing validation manifests also do not follow this candidate's `PV-<NNN>-<DESCRIPTIVE-PURPOSE>-V<MAJOR>.<MINOR>.json` grammar. The 21 current paths are `production_validation/pv17_concurrency_persistence/PV17-MANIFEST.json`, `production_validation/pv16_failure_recovery/PV16-MANIFEST.json`, `production_validation/pv06_operations_rollback/PV06-MANIFEST.json`, `production_validation/pv08_inq_core/PV08-MANIFEST.json`, `production_validation/pv15_cross_layer_integration/PV15-MANIFEST.json`, `production_validation/pv05_semantic_calibration/PV05-MANIFEST.json`, `production_validation/pv05_semantic_calibration/PV05-v1-MANIFEST.json`, `production_validation/pv05_semantic_calibration/PV05-INTEGRATED-MANIFEST.json`, `production_validation/pv11_inq_work_products/PV11-MANIFEST.json`, `production_validation/pv07_obs_inq/PV07-MANIFEST.json`, `production_validation/pv09_inq_stress/PV09-MANIFEST.json`, `production_validation/pv13_dec_governance/PV13-MANIFEST.json`, `production_validation/pv03_recovery/PV03-MANIFEST.json`, `production_validation/pv14_dec_execution_loop/PV14-MANIFEST.json`, `production_validation/pv12_inq_supersession_concurrency/PV12-MANIFEST.json`, `production_validation/g05_g06_control/PV-G05-G06-MANIFEST.json`, `production_validation/g08_certification_evidence/PV-G08-MANIFEST.json`, `production_validation/pv01_security/PV01-MANIFEST.json`, `production_validation/pv02_failure_injection/PV02-MANIFEST.json`, `production_validation/pv04_load/PV04-MANIFEST.json`, and `production_validation/pv10_inq_amendment_conflict/PV10-MANIFEST.json`.

### Existing status-bearing filenames

The candidate separates filename/identity from lifecycle status, while `canonical_obs/RATIFICATION-DECISION-REQUIRED.md` and `specifications/FS-OBS-002-RATIFICATION-CANDIDATE.md` include decision/lifecycle cues in their filenames. They remain unchanged as existing records; their future treatment requires an explicit, traceable decision.

### Disposition

These are compatibility and taxonomy conflicts, not automatic rename instructions. No existing repository file, directory, identity semantic, or Genesis G-0.1 record was changed to conform. The conflicts remain open while FS-SYS-002 is a candidate.

### Candidate test adaptation

The archive test uses a specification path relative to its extraction directory and prints the count of its 15 core phrase checks, although it also executes five prohibited-name checks and two supporting regular-expression checks. The repository test resolves the specification from `tests/`, preserves the 15 core checks, verifies that the prohibited names occur inside an explicit prohibition clause, and reports the core count separately from the test-suite result.
