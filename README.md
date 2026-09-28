# The Foundry

Institutional operating system for the Institution.

For a plain-language explanation of the project's purpose, see [Project Purpose](PROJECT-PURPOSE.md).

## Authority and foundation

The Genesis G-0.1 release records the Phase A foundation as frozen. Its release scope is the foundation artifacts named in its release notes; later engineering and governance records on `main` are not automatically part of that release.

**Authority hierarchy:** `CONST-001 → IP-001 → FM-001 → ratified type specifications → ratified object instances`

**Institutional cognition flow:** Reality → Observation → Triage → Inquiry → Evidence → Knowledge → Governance → Decision → Execution → Reality Feedback

Frozen foundation artifacts are not edited in place to conceal change. Proposals must declare dependencies and authority, preserve history, and use the revision process for the affected layer. A path, filename, commit, or passing test does not by itself create institutional authority. Files are representations; `ObjectID` is the institutional identity for governed objects.

## Current repository status

- Foundation: **Frozen — Genesis G-0.1**.
- Documentation architecture: Founder-approved **v1.1** is recorded on this review branch; current `main` remains at v1.0 pending integration. See [Documentation Architecture](00_SYSTEM/DOCUMENTATION-ARCHITECTURE-v1.1.md).
- OBS semantic-safety boundary: **FS-OBS-002 v1 ratified within its stated scope** by DEC-OBS-002.
- OBS state-machine vocabulary: **ratification pending**; this is a separate decision from semantic-safety ratification.
- REAL-SEM-01: **mandatory future gate, not executed**.
- Production certification: **NOT CERTIFIED**. PV-17's 12/12 reference-model invariants do not establish production database or execution guarantees.

See [Institutional and Repository Status](00_SYSTEM/INSTITUTIONAL-STATUS.md), the [Document Register](00_SYSTEM/DOCUMENT-REGISTER.csv), the [Founder Decision Record](00_SYSTEM/FOUNDER-DECISIONS.md), and [Overall Progress Ledger](OVERALL-PROGRESS-LEDGER.json) for source-linked details and open gates.

## Current physical tree

These are the directories that exist in the repository today:

- `00_SYSTEM/` — repository control, architecture, status, and repository-level decisions
- `01_FOUNDATION/` — constitutional and architectural foundation
- `07_RELEASES/` — release snapshots
- `99_TEMPLATES/` — controlled templates
- `canonical_obs/` — OBS code, tests, manifests, and state-machine ratification record
- `dec_core/`, `inq_core/`, `inq_interface/`, `runtime/` — implementation
- `production_validation/`, `tests/` — validation plans, manifests, and tests
- `specifications/` — specification records and domain decisions

`02_SPECIFICATIONS/`, `03_OBJECTS/`, `04_GOVERNANCE/`, `05_CAPABILITIES/`, and `06_PROJECTS/` remain logical classes, not current physical directories. Architecture v1.1 preserves current paths. Its orthogonal artifact-type/provenance axis does not move, delete, or rename files; any physical migration requires a separate Founder decision.

## Genesis G-0.1 next target

The Genesis release notes recorded `FS-OBS-001 — Observation Object Specification` as the next target at that release. Current open authority and engineering gates are listed in the status page; do not treat the historical target line as a complete current work plan.
