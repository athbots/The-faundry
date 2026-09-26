# The Foundry

Institutional operating system for the Institution.

## Authority and foundation

The Genesis G-0.1 release records the Phase A foundation as frozen. Its release scope is the foundation artifacts named in its release notes; later engineering and governance records on `main` are not automatically part of that release.

**Authority hierarchy:** `CONST-001 → IP-001 → FM-001 → ratified type specifications → ratified object instances`

**Institutional cognition flow:** Reality → Observation → Triage → Inquiry → Evidence → Knowledge → Governance → Decision → Execution → Reality Feedback

Frozen foundation artifacts are not edited in place to conceal change. Proposals must declare dependencies and authority, preserve history, and use the revision process for the affected layer. A path, filename, commit, or passing test does not by itself create institutional authority. Files are representations; `ObjectID` is the institutional identity for governed objects.

## Current Engineering State

- The Genesis G-0.1 foundation remains **frozen**. Its release scope and historical records are preserved.
- Documentation Architecture **v1.0 is active**; see [Documentation Architecture](00_SYSTEM/DOCUMENTATION-ARCHITECTURE-v1.0.md).
- The FS-OBS-002 semantic-safety boundary is **ratified within its stated scope** by DEC-OBS-002.
- OBS state-machine vocabulary remains **ratification pending**.
- REAL-SEM-01 remains **mandatory and unexecuted**.
- G-05 Change Control is an **integrated reference model**, not production-certified.
- G-06 Migration Control is an **integrated reference model**, not production-certified.
- G-08 Certification Evidence is an **integrated reference candidate**, not ratified or certified.
- The G-07 ↔ G-08 evidence boundary is a **fail-closed reference adapter**, not full authoritative G-07 integration.
- G-07/G-08 crash recovery is an **integrated SQLite reference candidate**. Its [integration specification](specifications/FS-INT-008-CRASH-RECOVERY-BOUNDARY-V0.1.md) and [validation/provenance record](production_validation/g07_g08_crash_recovery/G07-G08-CRASH-RECOVERY-BOUNDARY-RESULT-V0.1.md) distinguish candidate validation from repository validation:
  - Candidate archive SHA-256: `8d9c13485efaba2e926b10044a59ae3c2051ea888ed366ed4f3d557a41552158`.
  - Candidate validation: **15/15 independently reproduced**.
  - Repository crash-recovery validation: **18/18 PASS**.
  - Affected regression scope: **95/95 PASS**.
  - Total repository-owned validation reported: **113/113 PASS**.
- **C1 is NOT claimed.**
- **Production certification is NOT claimed.** Reference validation results do not establish production guarantees or certification.

See [Institutional and Repository Status](00_SYSTEM/INSTITUTIONAL-STATUS.md), the [Document Register](00_SYSTEM/DOCUMENT-REGISTER.csv), the [Founder Decision Record](00_SYSTEM/FOUNDER-DECISIONS.md), and [Overall Progress Ledger](OVERALL-PROGRESS-LEDGER.json) for source-linked status and decision records.

## Current Open Gates

1. Authoritative G-07 runtime integration.
2. Production G-09 persistence.
3. Production G-02 audit.
4. Crash and power-loss production guarantees.
5. G-10 distributed consistency decision.
6. REAL-SEM-01 execution.
7. Exact governance parameters.
8. G-08 certification authority, threshold, method, retention, and trust-anchor decisions.
9. Production execution safety.
10. Approved change/migration authority delegation.

These are open gates, not claims that the corresponding production capabilities or governance decisions are complete.

## Engineering Workflow

`CISA → validated candidate → FIB integration → branch → repository validation → review → merge/ratification`

- **CISA** owns architecture and review.
- **FIB** performs repository integration and execution.
- **Founder** holds authority and resolves institutional decisions that remain open.

Merge and ratification are separate outcomes: repository integration or passing validation does not itself ratify a specification, resolve a Founder decision, or establish certification.

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

`02_SPECIFICATIONS/`, `03_OBJECTS/`, `04_GOVERNANCE/`, `05_CAPABILITIES/`, and `06_PROJECTS/` remain logical classes, not current physical directories. Architecture v1 does not move, delete, or rename existing implementation directories.

## Historical Genesis G-0.1 next target

The Genesis release notes recorded `FS-OBS-001 — Observation Object Specification` as the next target at that release. This records the roadmap at the time of Genesis G-0.1 and is retained as history. The current engineering state and open gates are listed above; the historical target is not the current work plan.
