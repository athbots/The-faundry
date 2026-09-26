# Repository Curation Audit v0.1

- **Record ID:** FND-REPO-CURATION-AUDIT-001
- **Record type:** Non-normative repository curation and consistency audit
- **Status:** Audit snapshot; not a ratification, release, or certification decision
- **Audit date:** 2026-09-26
- **Branch:** `integration/repository-curation-and-readme-v0.1`
- **Inventory baseline:** merge commit `3a90839f7e9b1f35ad33b659afc22f0525a9774f`
- **Remote source commits:** G-07 discovery `3445d3a5c9344525738d63220626c6dbfa93c492`; FS-SYS-002 `808ac98432d6513301ea0938b0382b567c04a037`
- **Main at audit start:** `eb4c82e893afcbf52ed484249b0563f648c49160`

This audit describes the curation branch snapshot. It incorporates the two existing, pushed work branches above without changing either commit. It does not merge to `main`. The final curation commit and remote branch result are available in the repository history and task report.

## 1. Scope and method

The audit covered all 152 tracked files at the inventory baseline, the current remote refs, the prior verified FIB handoff manifest and its repository reconciliation records, the status/decision/register documents, and the known CISA/FIB work in this repository thread. It included a full tracked-path inventory, status and terminology searches, checks of relative README links and exact path case, inspection of validation manifests/results, and comparison with the Genesis tag. The document register contains 35 rows and is an index, not a complete file inventory.

Tracked-file count by physical area at the inventory baseline:

| Area | Files |
|---|---:|
| `.github/` | 1 |
| `00_SYSTEM/` | 7 |
| `01_FOUNDATION/` | 4 |
| `07_RELEASES/` | 2 |
| `99_TEMPLATES/` | 1 |
| `canonical_obs/` | 8 |
| `dec_core/` | 3 |
| `inq_core/` and `inq_interface/` | 7 |
| `production_validation/` | 68 |
| `runtime/` | 7 |
| `specifications/` | 20 |
| `tests/` | 19 |
| Root records and `.gitignore` | 5 |
| **Total** | **152** |

The curation adds one audit document and revises the README. It creates no directory. The actual tree and branch contents are verified after the changes in Git history and in the task report.

## 2. Inventory summary

| Artifact class | Current repository records and location | Status / qualification |
|---|---|---|
| Genesis and foundation | `01_FOUNDATION/CONST/CONST-001.md`, `IP/IP-001.md`, `FM/FM-001.md`, `AUDITS/GENESIS-G0.1-CROSS-AUDIT.md`; `07_RELEASES/GENESIS-G0.1/{RELEASE-NOTES.md,MANIFEST.json}`; `00_SYSTEM/REPOSITORY-CHARTER.md` | Genesis G-0.1 foundation is frozen within its declared scope. The Genesis release does not include later engineering records by implication. |
| System controls and documentation architecture | `00_SYSTEM/METADATA.yaml`, `DOCUMENTATION-ARCHITECTURE-v0.1.md`, `DOCUMENTATION-ARCHITECTURE-v1.0.md`, `DOCUMENT-REGISTER.csv`, `INSTITUTIONAL-STATUS.md`, `FOUNDER-DECISIONS.md` | v1.0 is active repository organization policy. v0.1 is retained as predecessor. The register is not a source-file inventory. |
| OBS and semantic safety | `canonical_obs/` (manifest, state machine, semantic relation, authority, tests and outputs); `specifications/FS-OBS-002-SEMANTIC-SAFETY-LAYER-V1.md`, `DEC-OBS-002-FS-OBS-002-RATIFICATION.json`, `FS-OBS-002-CHANGE-RECORD.json`, `FS-OBS-002-RATIFICATION-CANDIDATE.md`, `canonical_obs/RATIFICATION-DECISION-REQUIRED.md` | FS-OBS-002 semantic-safety boundary is ratified within its stated scope. OBS state-machine vocabulary remains ratification pending. REAL-SEM-01 remains mandatory and unexecuted. The state-machine and semantic-safety decisions are distinct. |
| DEC and INQ specifications/implementation | `specifications/FS-DEC-001-DECISION-BOUNDARY-V1.md`, `FS-DEC-002-EXECUTION-LOOP-V1.md`, `FS-INQ-001-OBS-INQ-INTERFACE-V1.md`, `FS-INQ-002-INQUIRY-CORE-V1.md`, `FS-INQ-003-EVIDENCE-AMENDMENT-CONFLICT-V1.md`, `FS-INQ-004-INVESTIGATION-WORK-PRODUCTS-V1.md`, `FS-INQ-005-SUPERSESSION-CONCURRENCY-V1.md`; `dec_core/`, `inq_core/`, `inq_interface/` | DEC and INQ statuses are mixed between proposals and validated reference models; exact governance weights and production execution guarantees remain open. |
| G-05 / G-06 | `specifications/FS-OPS-005-CHANGE-CONTROL-V1.md`, `FS-OPS-006-MIGRATION-CONTROL-V1.md`; `runtime/control_boundary.py`, `runtime/canonical_runtime.py`; `tests/test_g05_g06_control.py`; `production_validation/g05_g06_control/`; `.github/workflows/g05-g06-reference-tests.yml` | Integrated SQLite reference controls with focused validation. Not production G-09/G-02 integration and not certified. |
| G-08 and G-07/G-08 evidence boundary | `specifications/FS-CERT-008-CERTIFICATION-EVIDENCE-V1.md`, `FS-INT-007-008-EVIDENCE-BOUNDARY-V1.md`; `runtime/certification_evidence.py`, `runtime/g07_g08_evidence_gate.py`; `tests/test_g08_certification_evidence.py`; `production_validation/g08_certification_evidence/` | Separate G-08 reference evidence lifecycle and caller-owned G-07 callback adapter. G-08 is not ratified/certified; the adapter is not an authoritative G-07 runtime. |
| G-07 runtime discovery | `G07-AUTHORITATIVE-RUNTIME-DISCOVERY-V0.1.md` | Non-normative discovery report. It finds no authoritative G-07 runtime or ControlObligation service; it names the shared reference persistence/audit boundary to reuse and records the caller-owned gate seam. |
| Crash-recovery boundary | `specifications/FS-INT-008-CRASH-RECOVERY-BOUNDARY-V0.1.md`, `runtime/crash_recovery_boundary.py`, `tests/test_crash_recovery_boundary.py`, `production_validation/g07_g08_crash_recovery/G07-G08-CRASH-RECOVERY-BOUNDARY-RESULT-V0.1.md` | SQLite reference candidate. Candidate archive SHA and 15/15 independent result are kept separate from repository 18/18 crash, 95/95 affected regression, and 113/113 total results. No production crash/power-loss claim. |
| Shared persistence and audit reference | `runtime/control_boundary.py`; `specifications/FS-INT-004-CONCURRENCY-PERSISTENCE-V1.md`; `production_validation/pv17_concurrency_persistence/PV17-MANIFEST.json`; `STATUS-PV17.md` | Local SQLite, transaction, event, idempotency, and hash-chain reference behavior. Production G-09 persistence, G-02 audit, and G-10 distributed consistency remain open. |
| Validation, reviews, and evidence records | `production_validation/` contains 68 tracked files across PV-01–PV-17 and G-05/G-06, G-08, and G-07/G-08 crash-recovery packages; `tests/` contains 19 tracked test modules. Architectural findings include `production_validation/pv09_inq_stress/PV09-ARCHITECTURAL-FINDINGS.md` and this G-07 discovery report. | Results are limited to each manifest's identified source, environment, scope, and command. Passing evidence is not ratification or certification. |
| Templates and navigation | `99_TEMPLATES/OBJECT-TEMPLATE.md`; `README.md`, `OVERALL-PROGRESS-LEDGER.json`, `STATUS-PV17.md` | README and status summaries are indexes. They defer to decisions, specifications, release records, and validation manifests. |

## 3. Candidate and branch provenance

The remote was fetched before branch preparation. At audit start, GitHub reported:

- `main`: `eb4c82e893afcbf52ed484249b0563f648c49160`.
- `integration/g07-authoritative-runtime-discovery-v0.1`: `3445d3a5c9344525738d63220626c6dbfa93c492`.
- `integration/fs-sys-002-artifact-identity-v0.1`: `808ac98432d6513301ea0938b0382b567c04a037`.

The curation branch was created from the G-07 discovery branch and merged the FS-SYS-002 branch. The merge has both original commits as parents; it preserves their provenance. FS-SYS-002's specification, repository test, and register entry are present in this branch. The candidate ZIP itself is not stored in Git.

The verified handoff package's SHA-256 was `539e6702846c057b1ebb8b33ea07fb05ddfb228d3445155d6d8aca9b9b90f3ab6b`. Its FS-SYS-002 candidate ZIP was `926feeb34314bd8482813c6566964e6484e622d9bdd7475b700ccf0e1152c40e`; its FS-OPS-002 G-07 acceptance candidate ZIP was `453bb9c330b9ad8a62443dca3c88a4a788c70812964ba8dffdbc28eb9a9e42a4`; the standalone G-07 contract was `17ff4305cb8dfd8ec8b98af64e697336bda620ba6e0ca5a9e8f675b8b0e15ede`; and the Genesis comparison archive was `0899eb178f03f77c0f691477f891ec5ea340fa16ecf39ed91018c4fe174855ee`. The package manifest and five payload sizes/hashes were verified in the preceding handoff task and recorded in the G-07 discovery report.

Disposition of those artifacts:

- FS-SYS-002 source specification and test are integrated on this branch as a **candidate, not ratified**. The exact archive is a transfer artifact and is not committed.
- FS-OPS-002 remains a diagnostic acceptance candidate. Its conditions are compared in the G-07 discovery report; no authoritative G-07 runtime or normative implementation was fabricated.
- The Genesis archive is used for comparison; the repository's release records, not the ZIP, remain the canonical institutional record.
- The G-07/G-08 crash-recovery candidate ZIP is not committed. Its hash and independent 15/15 result are recorded in repository evidence.
- Earlier FS-CERT-008 and FS-INT-007-008 candidate archives were not included in the verified handoff package and remain unavailable for byte-level reconciliation. Their repository reference records exist; the archive-level provenance gap remains open.

## 4. FS-SYS-002 conflict register

The following conflicts are recorded by the candidate and rechecked against the current tree. No disposition below is implemented. “Recommended disposition” is a recommendation, not a decision.

| Existing artifact(s) | Proposed rule | Conflict | Impact | Recommended disposition | Authority required |
|---|---|---|---|---|---|
| **16 specifications:** `specifications/FS-CERT-008-CERTIFICATION-EVIDENCE-V1.md`, `FS-DEC-001-DECISION-BOUNDARY-V1.md`, `FS-DEC-002-EXECUTION-LOOP-V1.md`, `FS-INQ-001-OBS-INQ-INTERFACE-V1.md`, `FS-INQ-002-INQUIRY-CORE-V1.md`, `FS-INQ-003-EVIDENCE-AMENDMENT-CONFLICT-V1.md`, `FS-INQ-004-INVESTIGATION-WORK-PRODUCTS-V1.md`, `FS-INQ-005-SUPERSESSION-CONCURRENCY-V1.md`, `FS-INT-003-FAILURE-RECOVERY-V1.md`, `FS-INT-004-CONCURRENCY-PERSISTENCE-V1.md`, `FS-INT-007-008-EVIDENCE-BOUNDARY-V1.md`, `FS-OBS-002-RATIFICATION-CANDIDATE.md`, `FS-OBS-002-SEMANTIC-SAFETY-LAYER-V1.md`, `FS-OPS-005-CHANGE-CONTROL-V1.md`, `FS-OPS-006-MIGRATION-CONTROL-V1.md`, `REAL-SEM-01.md` | Candidate grammar requires a descriptive version segment of the form `V<major>.<minor>`. | These paths use `V1`, omit a version, or otherwise do not match the proposed grammar. | Renaming could invalidate links, tests, manifest references, or historical correspondence; path and identity must remain separate. | Grandfather existing paths while authority decides whether future additions follow the candidate grammar; if migration is chosen, create a complete old-to-new mapping and preserve compatibility/history. | Founder under open FD-DOC-005 and change authority in FD-DOC-003; any normative identity decision must be explicit. |
| **21 validation manifests:** `production_validation/pv17_concurrency_persistence/PV17-MANIFEST.json`, `pv16_failure_recovery/PV16-MANIFEST.json`, `pv06_operations_rollback/PV06-MANIFEST.json`, `pv08_inq_core/PV08-MANIFEST.json`, `pv15_cross_layer_integration/PV15-MANIFEST.json`, `pv05_semantic_calibration/PV05-MANIFEST.json`, `pv05_semantic_calibration/PV05-v1-MANIFEST.json`, `pv05_semantic_calibration/PV05-INTEGRATED-MANIFEST.json`, `pv11_inq_work_products/PV11-MANIFEST.json`, `pv07_obs_inq/PV07-MANIFEST.json`, `pv09_inq_stress/PV09-MANIFEST.json`, `pv13_dec_governance/PV13-MANIFEST.json`, `pv03_recovery/PV03-MANIFEST.json`, `pv14_dec_execution_loop/PV14-MANIFEST.json`, `pv12_inq_supersession_concurrency/PV12-MANIFEST.json`, `g05_g06_control/PV-G05-G06-MANIFEST.json`, `g08_certification_evidence/PV-G08-MANIFEST.json`, `pv01_security/PV01-MANIFEST.json`, `pv02_failure_injection/PV02-MANIFEST.json`, `pv04_load/PV04-MANIFEST.json`, `pv10_inq_amendment_conflict/PV10-MANIFEST.json` (all under `production_validation/`) | Candidate manifest grammar requires `PV-<number>-<purpose>-V<major>.<minor>.json`. | Existing stable paths use several legacy PV naming forms and do not match that grammar. | Manifest paths are embedded in registers, reports, workflows, and historical records. A blind rename would impair traceability. | Preserve the existing paths. Decide grandfathering or a versioned migration map before applying any new naming rule to existing records. | Founder/change authority under FD-DOC-003 and the unresolved artifact lifecycle/identifier decision FD-DOC-005. |
| `canonical_obs/RATIFICATION-DECISION-REQUIRED.md`; `specifications/FS-OBS-002-RATIFICATION-CANDIDATE.md` | Separate stable artifact identity/path from lifecycle status. | Both names carry decision/status cues; the second is a historical candidate superseded within the semantic-safety scope. | A path can be mistaken for current status or authority if read without the register and decision. | Preserve the historical names and their links; make status explicit in controlling records. Consider filename policy only under an approved compatibility plan. | The relevant OBS authority for the state-machine record; Founder for naming/identity policy under FD-DOC-005. |
| `FM-001`, Documentation Architecture v1.0, FS-SYS-002, and FD-DOC-005 | Keep Document Control ID, Institutional ObjectID, filesystem path, Git provenance, evidence ID, and validation-run identity distinct. | The candidate and active architecture agree that path is not ObjectID, but FD-DOC-005 has not decided which controlled documents are institutional objects or how IDs are allocated. This is an unresolved boundary, not a demonstrated direct contradiction with IP-004. | A new identifier could imply object status or duplicate identity if assigned without the object taxonomy. | Keep current semantics; do not assign ObjectIDs to documents or change existing identities until classes and lifecycle are decided. | Founder under FD-DOC-005; preserve the FM-001 / IP-004 authority boundary. |
| Documentation Architecture v1.0 and FS-SYS-002 logical taxonomies | Candidate presents Evidence and Transfer Artifact as logical classes; v1.0 places certification evidence under Validation and separately retains Objects and capabilities and Projects. | The candidate does not state whether its categories refine, extend, or replace v1.0 categories. | Readers could classify identical records differently; a physical reorganization would make the ambiguity appear settled when it is not. | Record a crosswalk or an explicit successor decision first. Keep current physical paths and do not create placeholder directories. | Founder under documentation/object taxonomy authority; FD-DOC-001 settled preservation of the current physical baseline, while FD-DOC-005 remains open on artifact classes and identity. |

## 5. Structural and curation findings

- The physical tree matches Documentation Architecture v1.0's actual-path map. It has the expected engineering, specification, validation, template, foundation, and system-control areas. The five `02_*`–`06_*` logical categories remain non-physical as documented.
- The branch contains professional descriptive paths. No tracked `tmp`, `candidate_final`, random numeric folder, Python bytecode, or pytest cache artifact was found in the work being reconciled.
- No duplicate authoritative G-07 obligation, persistence, audit, or evidence implementation was found. The G-07 discovery report distinguishes the callback adapter, generic SQLite reference boundary, separate G-08 lifecycle, and missing G-07 domain runtime.
- Documentation Architecture v0.1 and v1.0 are intentionally retained as predecessor and successor. The multiple PV-05 manifests are separately named validation revisions/variants, not evidence that one result supersedes all others. The FS-OBS-002 candidate record and ratification decision also have distinct historical and controlling roles.
- The document register's 35 rows cover high-consequence controlled records; it is not expected to list every source, test, or output. This non-normative audit is linked from the README and is not added as a new authority-bearing register entry.
- The document register has 35 rows and repeats `FND-DOC-ARCH-001` for v1.0 (active) and v0.1 (superseded). These are two versions of one controlled document series with explicit predecessor/successor status, not duplicate authoritative documents. No other repeated record ID was found.
- The curation branch does not create a second persistence or audit model. It documents the existing SQLite reference boundary and its production gaps.

## 6. README and link audit

Before revision, the README had seven relative links, all resolving with exact path case. It identified the historical Genesis next target as historical, but did not define the requested OBS-to-verification operating model, summarize the FS-SYS-002 candidate, or state the G-07 discovery finding. It therefore did not expose the latest branch-only work to a reader entering through the README.

The revised README adds those missing distinctions, links the discovery and curation records, maps the physical tree, distinguishes implementation/candidate/reference validation/ratification/certification, and identifies current open gates. Final relative-link count and exact-case result are recorded after validation below. No link to an unverified branch or file is intended.

## 7. Cross-document consistency and contradictions

| Finding | Records compared | Assessment / disposition |
|---|---|---|
| Genesis metadata provenance | Genesis release notes and manifest; `00_SYSTEM/METADATA.yaml`; Genesis tag `f63dd2f6a46796785337ecf5c0fb678e68ee5d96`; v1 documentation change `eb4c82e893afcbf52ed484249b0563f648c49160` | The Genesis release notes list Repository Metadata. Git history shows `METADATA.yaml` changed at the v1 architecture commit to include post-Genesis status fields. The foundation files, charter, and Genesis release records match the Genesis tag, but the manifest does not pin the original metadata bytes. Do not describe the current metadata file as byte-identical to the Genesis payload. Exact release-source provenance remains open under FD-DOC-004. This audit does not edit Genesis records or metadata. |
| G-07 authority | README, Institutional Status, G-07 discovery, evidence-boundary spec, crash-recovery result, register | Consistent after README reconciliation: no authoritative G-07 runtime exists; the G-07/G-08 gate is a caller-owned adapter; crash-recovery tests use a generic SQLite reference boundary. Some isolated phrases about durable G-07-shaped transitions could be overread, so the README now points to the discovery report and states the limitation. |
| G-08 and certification | G-08 specification/manifest, Founder Decision Record, status, ledger, README | The records state that G-08 is a reference candidate, not ratified or certified; authority, method, retention, trust-anchor, threshold, and production G-09/G-02 decisions remain open. No C1 or production certification claim was found. |
| Crash-recovery validation | Result record, status, ledger, README | The candidate archive's 15/15 independent result is separate from repository 18/18 crash tests, 95/95 affected regression scope, and 113/113 repository-owned total. The README retains those separate denominators. |
| FS-SYS-002 status and naming | Candidate spec/test, document register, FD-DOC-005, Documentation Architecture v1.0 | The candidate is explicitly not ratified. Its conflicts remain documented; no proposed rule has been silently applied to old paths or identities. |
| PV-17 raw output | `STATUS-PV17.md`, PV-17 manifest and test-output file | The status record notes a spreadsheet-runtime warmup timeout after the PASS summary while the manifest records exit code 0 and 12/12 PASS. This limitation remains visible and should be clarified before the output is treated as a clean reproducibility artifact. |
| Main versus feature branches | Remote refs and curation branch | The README now states that the discovery and FS-SYS work are on the curation branch and have not been merged to `main`. This is branch scope, not a claim that main already contains them. |
| Status/progress basis metadata | `00_SYSTEM/INSTITUTIONAL-STATUS.md`, `OVERALL-PROGRESS-LEDGER.json`, remote `main` | Both files still name `b98ed49ccb1e75b941e8611151828788b05d198d` as a basis, while `main` is at `eb4c82e893afcbf52ed484249b0563f648c49160` and the curation branch adds later work. The field may describe an earlier reconciliation input, but the current wording does not make that scope clear. The README flags this; the status/ledger files are left unchanged pending a traceable status update. |
| Legacy OBS regression programs | `tests/test_c014_regression.py` through `test_c019_capability_issuance.py`; canonical OBS API | Direct runs report pre-existing failures: C014 1/5, C015 7/8, C017 0/6, C018 1/6; C016 4/4 and C019 5/5 pass. The principal failures are stale calls missing `authority_service` or `capability`, plus one semantic-safety assertion. They are outside this documentation-only change and were not altered. |

Search review found no controlling record that claims C1 or production certification is complete. The exact CFO/TEAM governance weights remain unratified. No status language was changed in an underlying specification, validation manifest, or Genesis record as part of this audit.

## 8. Missing artifacts and open integration work

These are absent or incomplete by design/status, not files silently omitted from an otherwise complete implementation:

- **Authoritative G-07:** no G-07 obligation lifecycle service, assignment API, authoritative resolution/closure path, or G-07-owned persistence command exists. The G-07 report recommends one service at the existing `ControlBoundaryPort` boundary after lifecycle and authority decisions.
- **FS-OPS-002:** acceptance contract remains an external, non-ratified candidate; its comparison is in the discovery report. There is no G-07 implementation satisfying it.
- **Earlier G-08/evidence-boundary archives:** the source specifications and reference test records exist, but the original FS-CERT-008 and FS-INT-007-008 candidate ZIPs were not in the verified handoff package and have not been byte-reconciled.
- **Production G-09/G-02:** production persistence and audit adapters are absent. The shared local SQLite reference boundary is not a production substitute.
- **REAL-SEM-01 corpus/evaluation:** the chartered gate exists but remains unexecuted; no representative accepted corpus or Founder-approved thresholds are established in this repository snapshot.
- **Production execution and recovery:** real execution safety, backup/restore, power-loss behavior, and production rollback guarantees remain unverified.
- **Genesis release provenance:** the release manifest lacks the source commit and complete file-level hashes; the exact Repository Metadata payload at Genesis cannot be proven from that manifest.

No repository representation was fabricated for an external transfer artifact. The FS-SYS-002 and crash-recovery ZIPs remain provenance references, not canonical source files.

## 9. Changes made and deliberately not made

**Made on the curation branch**

- Rewrote `README.md` as the institutional entry point for the current branch state, with authority/status distinctions, open gates, repository map, and working method.
- Added this curation audit at `00_SYSTEM/REPOSITORY-CURATION-AUDIT-V0.1.md`.
- Preserved the original G-07 discovery and FS-SYS-002 commits and their provenance in the branch history.

**Deliberately not made**

- No code or implementation directory changes; no directory creation; no mass rename, move, or deletion.
- No change to Genesis foundation files, release notes, manifest, or historical claims.
- No changes to identity semantics, governance thresholds, G-07 lifecycle/authority, G-08 acceptance rules, G-10 consistency, or certification criteria.
- No rewrite of earlier validation manifests or candidate documents to suppress their historical status.
- No addition of transfer ZIPs, cache files, bytecode, or generated temporary artifacts.
- No merge to `main`.

## 10. Validation and final repository status

The curation validation record is:

- README relative links: **16/16 resolved**; exact-case check: **0 broken or case-mismatched**.
- Focused commands used the bundled Python 3.12.14 interpreter at `C:\Users\aniru\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe` because `python` was not on the shell PATH:
  - `-m unittest discover -s tests -p test_artifact_identity_policy.py -v`: **4/4 tests PASS**, candidate **15/15 core assertions PASS**.
  - `-m unittest discover -s tests -p test_crash_recovery_boundary.py -q`: **18/18 PASS**.
  - `-m unittest discover -s tests -p test_g05_g06_control.py -q`: **19/19 PASS**.
  - `-m unittest discover -s tests -p test_g08_certification_evidence.py -q`: **20/20 PASS**.
  - Total across the four focused suites: **61/61 tests PASS**.
- Broad discovery command `python -m unittest discover -s tests -v`: **67 discovered; 61 test methods passed; 6 import errors** because six legacy C014–C019 files execute at import time and raise `SystemExit`. It is not a passing whole-suite result. Direct legacy-script commands reported: C014 **1/5**, C015 **7/8**, C016 **4/4**, C017 **0/6**, C018 **1/6**, C019 **5/5**. Failures are the existing OBS API/semantic-safety regression issues described above; no implementation code was changed.
- JSON structural check: **26/26 files parsed**. CSV register: **35 rows**, all referenced files present. The only repeated ID is `FND-DOC-ARCH-001` for the active v1.0 and superseded v0.1 versions of the same series; no other repeated IDs. Tracked generated cache/bytecode files: **0**.
- `git diff --check`: **PASS**, with no whitespace errors. Git reports only its configured LF-to-CRLF normalization notice for `README.md`.
- Final working tree: **clean after commit**. The curation branch remains unmerged; the task report records the remote-ref comparison after push.

The intended final branch is `integration/repository-curation-and-readme-v0.1`. It must remain unmerged to `main` pending review. The authoritative production state remains **NOT CERTIFIED**; C1 is **NOT CLAIMED**.

## 11. Quality gate and self-critique

With the revised README and linked status, register, decisions, validation records, and discovery report, a principal engineer or research scientist should be able to orient to the institution and its current boundaries within 15 minutes. This does not let a reader independently reproduce every historical validation result from the README; that requires following the manifests and commands. The unresolved FS-SYS taxonomy crosswalk, incomplete Genesis snapshot provenance, caller-owned G-07 gate, PV-17 runner-noise discrepancy, and absent production adapters remain concrete obstacles. The curation improves navigation and makes those limitations visible; it does not close them.
