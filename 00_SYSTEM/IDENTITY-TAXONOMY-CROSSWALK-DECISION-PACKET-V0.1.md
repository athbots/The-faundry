# Identity and Taxonomy Crosswalk — Founder Decision Packet v0.1

- **Record type:** Non-normative decision-support packet
- **Status:** For Founder review; not a decision, ratification, or naming rule
- **Prepared:** 2026-09-27
- **Main baseline inspected:** `effc241f285c414f1134327bd7dda3140d63f5fe`
- **FS-SYS-002 candidate source:** `integration/fs-sys-002-artifact-identity-v0.1` at `808ac98432d6513301ea0938b0382b567c04a037`
- **Prior curation inventory:** `integration/repository-curation-and-readme-v0.1` at `30000ba70cbee7d9da3e172fd27b9b255c0a5766`; later provenance branch at `19b8384d2cd0b0d806c93e7247e0e8798d5b4a1c`

This packet prepares the open FD-DOC-005 decision. It does not make FS-SYS-002 authoritative, change identity semantics, or direct a file move or rename. No new Document Control ID or ObjectID is assigned here because their allocation boundary is part of the decision being prepared.

The Founder has already directed the sequence: decide the identity and taxonomy crosswalk first; prepare a mapped physical-migration plan afterward. That sequence does not authorize migration execution. Existing paths remain in place pending a separate decision.

## 1. Repository and candidate baseline

The current GitHub `main` baseline inspected for this packet is `effc241f285c414f1134327bd7dda3140d63f5fe`. It contains 132 tracked paths, 14 entries under `specifications/`, and 19 JSON validation manifests under `production_validation/`.

FS-SYS-002 is a candidate on its own pushed branch, not part of current `main`. Its archive SHA-256 is `926feeb34314bd8482813c6566964e6484e622d9bdd7475b700ccf0e1152c40e`; the candidate reported 15/15 assertions passing. The curation branch recorded a repository reproduction separately. Candidate validation does not ratify the candidate's identity or naming rules.

The curation inventory at `30000ba70cbee7d9da3e172fd27b9b255c0a5766` covered 153 tracked paths, 20 specification-directory entries, and 21 validation manifests after combining earlier integration branches. It identified 16 existing specification names and 21 manifest names that do not meet the candidate's proposed filename grammar. Those counts include work absent from current `main`; they must not be described as the current-main inventory. No such branch-only work is treated as merged by this packet.

## 2. What is already decided

- The Repository Charter says the repository represents institutional records; the repository is not itself the institution.
- Documentation Architecture v1.0 preserves the current physical tree for navigation and treats the numbered `02_*` through `06_*` scheme as logical classification, not a set of required directories.
- A filesystem path is not an ObjectID. Git branches, commits, filenames, and tests do not create institutional authority.
- FM-001 and IP-004 retain institutional object identity independently of representation. A document path or revision does not replace an object's identity.
- FD-DOC-001 forbids moving, renaming, or deleting current implementation directories as an effect of Documentation Architecture v1.0.
- FD-DOC-005 remains open on which documentation artifacts are governed objects and which identifiers, metadata, and lifecycle states apply.
- The user-directed migration sequence is recorded in the current `FOUNDER-DECISIONS.md`: crosswalk decision first, mapped migration plan next, with execution requiring a separate decision.

## 3. Taxonomy crosswalk for decision

The table compares Documentation Architecture v1.0's logical classes with the classes listed by candidate FS-SYS-002. A match below is a proposed mapping for review, not an adopted taxonomy.

| Documentation Architecture v1.0 class | FS-SYS-002 candidate class | Current physical locations or examples | Crosswalk issue for Founder |
|---|---|---|---|
| System control | System control | `00_SYSTEM/` | Direct correspondence; records still vary in authority and lifecycle. |
| Foundation | Foundation | `01_FOUNDATION/` and Genesis release records | Direct correspondence; Genesis scope remains controlled by its own release records. |
| Specifications | Specification | `specifications/` | Direct correspondence at class level; strict candidate filename grammar conflicts with existing names. |
| Governance decisions | Governance decision | `00_SYSTEM/`, domain records under `specifications/`, and `canonical_obs/` ratification records | Class is present, but physical location is not one-to-one with the logical class. |
| Objects and capabilities | No explicit corresponding class | No dedicated physical directory; governed object types and capabilities are not a complete repository inventory | Candidate omission does not decide that these classes are unnecessary or superseded. |
| Projects | No explicit corresponding class | No dedicated physical directory | Candidate omission does not decide that project records should be removed or absorbed into another class. |
| Implementation | Implementation | `canonical_obs/`, `dec_core/`, `inq_core/`, `inq_interface/`, `runtime/` | Direct correspondence at class level. Some physical directories also contain manifests, tests, or lifecycle records, so classify records individually. |
| Validation | Validation and Evidence | `production_validation/`, `tests/`; outputs and manifests | Candidate separates Evidence from Validation. v1.0 already includes evidence within validation's intended contents, including certification evidence. Their relationship is undefined. |
| Releases | Release | `07_RELEASES/` | Direct correspondence; release ID remains separate from its path and source commit. |
| Templates | Template | `99_TEMPLATES/` | Direct correspondence. |
| No v1.0 logical class for transport archives | Transfer artifact | Candidate ZIPs are exchanged outside the canonical repository | A transport archive is not the same thing as the canonical source record it carries. Candidate status does not require an archive directory. |

The taxonomies are not currently one-to-one. In particular, FS-SYS-002 adds Evidence and Transfer artifact but omits Objects and capabilities and Projects. It also does not say whether Evidence is a subtype of Validation, a cross-cutting role, or a replacement class.

### Founder choice: relationship between the taxonomies

1. **Replace v1.0 logical classes with FS-SYS-002.** This would require an explicit successor decision for Documentation Architecture v1.0 and a disposition for Objects and capabilities and Projects.
2. **Treat FS-SYS-002 as an orthogonal artifact-type/provenance layer over v1.0** (**CISA recommendation**). Preserve v1.0's institutional-function classes. Treat Evidence as a cross-cutting role that may qualify a validation result or another record, and Transfer artifact as an exchange/transport type. Retain Objects and capabilities and Projects. A single record may carry more than one classification where needed; physical paths remain unchanged.
3. **Defer the taxonomy relation.** Keep both proposals visible but do not use FS-SYS-002 categories for repository-wide classification until a later decision.

Option 2 preserves v1.0 while making the candidate's additions useful, but it adds a second classification axis that will need concise definitions and clear assignment rules. Option 1 is simpler to explain but makes a candidate omission look like a substantive institutional decision. Option 3 minimizes commitment but leaves cross-repository classification inconsistent.

## 4. Identity crosswalk for decision

| Identity or reference | Meaning supported by existing records/candidate | Current repository evidence | Boundary that remains open |
|---|---|---|---|
| Document Control ID | Identifier for a controlled document or record | The document register uses record IDs such as `FND-DOC-ARCH-001`, `FS-OBS-002-v1`, and `PV-17`. | FD-DOC-005 has not decided which document classes are governed objects, the required ID coverage, or whether a record ID identifies a document series or one version. |
| Institutional ObjectID | Persistent identity of a governed institutional object under FM-001/IP-004 | It is distinct from a path under the charter and v1.0 architecture. | Which document-like artifacts, if any, are also institutional objects; do not infer ObjectID from a filename or register ID. |
| Filesystem path | Current repository location | Physical locations are documented by v1.0; `canonical_obs/` demonstrates that one directory can hold different record roles. | A future path change may require a mapping and compatibility work, but path is not itself the object's identity. |
| Git commit or branch | Version-control provenance | Current `main` is `effc241…`; FS-SYS-002 and curation work remain on separate branches. | A commit proves repository history, not ratification, release authority, or object identity. |
| Validation program/manifest and validation run | A validation plan/configuration versus one execution and its result | Main has 19 validation manifests. It uses names such as `PV17-MANIFEST.json`; PV-05 has multiple manifest variants. The register identifies `PV-17`, while output files record execution results. | The candidate names a Validation Run ID separately but does not specify how it relates to existing PV identifiers, manifest revisions, repeated runs, or output files. |
| Evidence ID | Identity for an evidence record, separate from its payload and validation run | FS-SYS-002 proposes a distinct Evidence ID. G-08 candidate work on another branch has an evidence lifecycle; it is not in current `main`. | Evidence record classes, IDs, provenance, and relationship to validation outputs require a defined crosswalk; do not treat every passing test as a certification-evidence record. |
| Release ID | Identity of a declared repository snapshot | Genesis uses `GENESIS-G0.1`; its release manifest does not identify a source commit or complete file hashes. | Release ID must remain distinct from a Git commit and from the path where release files are stored. |
| Transfer artifact name and digest | Name and byte-level identity of an exchanged archive | FS-SYS-002's candidate archive is identified by its filename and SHA-256 in the candidate provenance. | The archive is transport, not the canonical institutional record; retention and archival rules are not set by this candidate. |

### Founder choice: document identity and allocation

1. **Separate document identity from object identity** (**CISA recommendation; consistent with the existing path/ObjectID boundary**): assign Document Control IDs to defined controlled-document classes; reserve ObjectIDs for instances governed as institutional objects under FM-001. A document may reference an ObjectID without reusing it.
2. **Treat every controlled document as an institutional object:** assign both a governed object type/ObjectID and document-control metadata. This requires an explicit object model and lifecycle before assigning identities.
3. **Defer ObjectID allocation until the object taxonomy is decided:** preserve current register/path references and define Document Control ID coverage separately.

The candidate asserts that these identity kinds must not substitute for one another, but it does not define the allocation rules or formats. Choosing an option does not automatically rename existing files, change register values, or retroactively assign ObjectIDs.

## 5. Compatibility evidence — not a migration map

The FS-SYS-002 candidate proposes specification filenames with a `V<major>.<minor>` segment and validation manifest filenames of the form `PV-<number>-<purpose>-V<major>.<minor>.json`. Current `main` has 12 Markdown specification/gate names that do not follow the proposed specification form, including the `FS-DEC-001`, `FS-INQ-001`, `FS-INT-003`, `FS-OBS-002-RATIFICATION-CANDIDATE`, and `REAL-SEM-01` records. The broader curation branch inventory adds four such specification names from other integration work, producing the previously reported total of 16.

All 19 validation manifest paths on current `main` use legacy forms such as `PV17-MANIFEST.json`; the broader curation inventory contains 21 manifest paths, including branch-only G-05/G-06 and G-08 records. Existing names such as `canonical_obs/RATIFICATION-DECISION-REQUIRED.md` and `specifications/FS-OBS-002-RATIFICATION-CANDIDATE.md` also place lifecycle cues in paths, contrary to the candidate's identity/status separation principle.

These are compatibility observations only. This packet intentionally supplies no proposed destination filenames, directory tree, or old-to-new path mapping. Those belong in the mapped migration plan, after the crosswalk decision. The complete 16-specification and 21-manifest lists are recorded in the curation inventory at commit `30000ba70cbee7d9da3e172fd27b9b255c0a5766`.

## 6. Recommended decision sequence and limits

1. Decide whether FS-SYS-002 is a second classification axis over v1.0 or a replacement; decide the relationship between Validation and Evidence and preserve the omitted v1.0 classes explicitly.
2. Decide which record classes receive Document Control IDs and which are institutional objects with ObjectIDs. Keep paths, commits, run IDs, Evidence IDs, Release IDs, and transfer-artifact names distinct.
3. Record the decision under FD-DOC-005, including scope, authority, rationale, effective date, and exceptions. Until then, FS-SYS-002 remains a candidate and existing identity semantics remain unchanged.
4. After the crosswalk decision, prepare the previously directed mapped migration plan. It should inventory affected paths, propose any path mappings, identify links/imports/manifests and history dependencies, specify validation and rollback, and request a separate execution decision. Do not rename or move files as part of this packet.

### Risks and self-critique

- A two-axis taxonomy can preserve meaning while adding classification work; without clear assignment rules it could make records harder to find.
- Treating all evidence as validation would be too narrow; treating every test output as G-08 evidence would overstate its authority.
- The curation inventory is broader than current `main`, so branch-only counts must remain labeled and must not be represented as merged state.
- This packet is a decision aid, not a complete automated record-by-record classification. It does not settle identity semantics, file naming, retention policy, nor certify repository or production behavior.
