# G-07 Authoritative Runtime Discovery v0.1

- **Record type:** Non-normative architecture discovery; no G-07 implementation performed
- **Repository baseline:** integration/foundry-readme-current-state-v0.1 at 7a34a6f22f776621782726474de143cfaa0c9b79
- **Remote state:** origin was fetched before discovery; the baseline branch matched its remote-tracking ref
- **Main at discovery:** eb4c82e893afcbf52ed484249b0563f648c49160
- **G-07 acceptance candidate reviewed:** the-foundry-fs-ops-002-g07-authoritative-runtime-acceptance-candidate-v0.1.zip, SHA-256 453bb9c330b9ad8a62443dca3c88a4a788c70812964ba8dffdbc28eb9a9e42a4

## Finding

No authoritative G-07 runtime exists in the inspected repository state, under another name or under a G-07 name. The repository contains a generic SQLite control-record persistence boundary, G-05 and G-06 reference services, a G-08 evidence reference service, a G-07/G-08 evidence gate, and a generic crash-recovery wrapper. None owns the G-07 obligation lifecycle.

The G-07/G-08 gate remains caller-owned: callers provide both an obligation dictionary and a callback. The gate validates the supplied data and evidence, then invokes the callback. It neither retrieves nor controls a persisted G-07 obligation. Generic tests manually create kind G07 records and transition them through the shared SQLite reference boundary; those tests do not establish an authoritative G-07 service.

## Existing implementation inventory

| Classification | Exact repository path | Discovered responsibility | Qualification |
|---|---|---|---|
| Shared reference persistence/audit boundary | runtime/control_boundary.py | ControlBoundaryPort plus SQLiteControlBoundary store generic snapshots, events, idempotency fingerprints and reconstruction checks. | Local SQLite reference boundary used by G-05/G-06/G-08 and G-07-shaped tests; not production G-09 or G-02. |
| G-05 reference service | runtime/control_boundary.py — ChangeControl | G-05 change lifecycle and authorization checks. | Kind G05; not an obligation service. |
| G-06 reference service | runtime/control_boundary.py — MigrationControl | G-06 migration lifecycle and execution checks. | Kind G06; not an obligation service. |
| G-08 reference service | runtime/certification_evidence.py — CertificationEvidence | Evidence registration, independent verification, producer provenance and audit reconstruction. | Separate G-08 lifecycle; it does not own G-07 resolution. |
| G-07/G-08 reference adapter | runtime/g07_g08_evidence_gate.py — EvidenceResolutionGate | Checks caller-supplied evidence references and actor separation before invoking callbacks. | Not an obligation aggregate, lifecycle owner or persistence service. |
| Generic recovery wrapper | runtime/crash_recovery_boundary.py — CrashRecoveryBoundary | Delegates generic create/transition calls to the shared boundary and verifies reconstruction. | Accepts a kind string, including G07 in tests; it defines no G-07 transitions. |
| Runtime composition | runtime/canonical_runtime.py — CanonicalRuntime | Wires the injected reference boundary, G-05/G-06/G-08 services, gate and recovery wrapper. | Exposes no G-07 obligation creation, assignment, resolution or closure service. |
| Authoritative G-07 implementation | None found | — | G-07 is not integrated. |

Other nearby code does not fill the gap: canonical_obs owns OBS behavior; DirectStateGuard and GraduationAuthority concern OBS protection/graduation. Repository-wide tracked-file searches found no ControlObligation symbol, FS-OPS-002 specification, G-07 assignment/assigned_to API, or G-07 control-plane implementation file. The FS-OPS-002 candidate is available only in the verified temporary handoff extraction and is not integrated into the repository.

Relevant existing records are specifications/FS-INT-007-008-EVIDENCE-BOUNDARY-V1.md, specifications/FS-INT-008-CRASH-RECOVERY-BOUNDARY-V0.1.md, specifications/FS-CERT-008-CERTIFICATION-EVIDENCE-V1.md, production_validation/g08_certification_evidence/PV-G08-MANIFEST.json, production_validation/g07_g08_crash_recovery/G07-G08-CRASH-RECOVERY-BOUNDARY-RESULT-V0.1.md, tests/test_g08_certification_evidence.py and tests/test_crash_recovery_boundary.py. The status records consistently qualify G-07 runtime integration as open.

## Actual call path

~~~mermaid
flowchart TD
    CR[CanonicalRuntime with injected boundary and authorizer]
    CR --> RB[CrashRecoveryBoundary over shared ControlBoundaryPort]
    CR --> CE[CertificationEvidence over the same reference boundary]
    CR --> EG[EvidenceResolutionGate]
    CALLER[Caller or test supplies obligation dictionary and callback] -->|enter_resolution_pending| EG
    EG -->|validate every supplied evidence ID| CE
    CE -->|reconstruct evidence snapshot and audit history| RB
    EG -->|only after checks| CB[Caller-owned transition callback]
    CB -->|in current tests| TR[CrashRecoveryBoundary.transition with kind G07]
    TR --> DB[SQLiteControlBoundary.transition]
    CALLER -->|verify_resolution with dictionary and callback| EG
    EG -->|state, actor and evidence checks only| VCB[Caller-owned verification callback]
    VCB --> TR
~~~

The demonstrated test path for creating a G-07-shaped record is separate: tests/test_crash_recovery_boundary.py constructs a generic document in a fixture and calls CrashRecoveryBoundary.create with kind G07. Its resolution callback manually invokes generic transition from OPEN to RESOLUTION_PENDING; its verification callback manually transitions from RESOLUTION_PENDING to VERIFIED.

G-08 has its own service path: CertificationEvidence.register → begin_verification → verify or fail → the shared reference boundary. Before evidence supports the adapter, require_verified_and_audited reconstructs the evidence record and checks the recorded verification event and hash-linked history.

## Lifecycle ownership and actual coverage

| Step | What the repository does | What is missing |
|---|---|---|
| Obligation creation | Test/caller constructs an arbitrary dictionary; generic create can store it under kind G07. | No domain constructor or G-07 creation validation. |
| Assignment | No G-07 assignment method, assigned actor field contract or assignment transition found. | Assignment lifecycle and authority. |
| Resolution | enter_resolution_pending validates the supplied dictionary and invokes the supplied callback. | No authoritative record lookup or G-07 transition owner. |
| Evidence requirement | Caller supplies requires_evidence and evidence_ids. If evidence is required, the gate rejects an empty list and checks each supplied ID. | The gate does not bind those values to persisted immutable G-07 scope; a caller can supply different values. |
| Independent verification | verify_resolution checks the supplied state equals RESOLUTION_PENDING and requires distinct actor strings. It compares the supplied resolution_actor only when present. | No authoritative lookup of the recorded resolution actor, G-07 authorization policy, or G-07-owned commit path. |
| Closure | No G-07 close operation or closure state rule found. Current G-07-shaped tests stop at generic VERIFIED. | Whether VERIFIED is terminal or precedes CLOSED is undefined in this implementation. |

SQLiteControlBoundary.transition enforces expected-current-state and record integrity checks, but has no G-07 transition map or G-07 authorization check. State strings appearing in tests are caller-provided generic values, not a complete G-07 lifecycle contract.

## Existing persistence and audit boundary

The boundary to reuse is ControlBoundaryPort in runtime/control_boundary.py. Its current SQLiteControlBoundary reference implementation stores snapshots in control_aggregates, events in control_events and request fingerprints in control_idempotency. create and transition write the snapshot and event under the same local database transaction. Events carry audit_ref values and a hash-linked sequence; history and reconstruct validate sequence, chain, terminal state/version and state hash. CrashRecoveryBoundary delegates to that same port and then reconstructs.

This is a local reference boundary, not production G-09 persistence or the G-02 audit service. No production audit adapter is present in the inspected path; audit_ref is a field in the local control event. G-09/G-02 production binding, physical power-loss guarantees and G-10 distributed consistency remain open. The repository already has one shared reference persistence/audit model; a G-07 integration should reuse it rather than introduce another.

## Comparison with the supplied FS-OPS-002 acceptance candidate

The package-level manifest was verified before file inspection: outer package SHA-256 539e6702846c057b1ebb8b33ea07fb05ddfb228d3445155d6d8aca9b9b90f3ab6b; all five listed payload sizes and SHA-256 values matched. The G-07 candidate ZIP matched 453bb9c330b9ad8a62443dca3c88a4a788c70812964ba8dffdbc28eb9a9e42a4, and its standalone contract hash matched 17ff4305cb8dfd8ec8b98af64e697336bda620ba6e0ca5a9e8f675b8b0e15ede.

The acceptance candidate is a diagnostic contract, not ratified authority. Its 15 conditions compare as follows; these are discovery findings, not pass/fail certification results.

| ID | Candidate acceptance condition | Discovery result in this repository |
|---|---|---|
| G07-AC-001 | Single lifecycle owner | Not met: no G-07 lifecycle service exists. |
| G07-AC-002 | Explicit identity | Partial reference only: generic records carry identity, but no G-07 identity owner exists. |
| G07-AC-003 | Controlled transitions | Not met: generic boundary has no G-07 transition map. |
| G07-AC-004 | No caller-owned closure | Not met: gate delegates lifecycle mutation to a caller callback; no closure path is owned. |
| G07-AC-005 | Rejection is not closure | Unspecified: no G-07 verification-rejection transition or preserved unresolved lifecycle exists. |
| G07-AC-006 | Blocked is not resolved | Unspecified: no G-07 blocked/escalated lifecycle states or transitions exist. |
| G07-AC-007 | G-08 gate is runtime-owned | Partial reference only: the evidence check exists, but the G-07 lifecycle and callback remain caller-owned. |
| G07-AC-008 | Independent verification | Partial adapter check: actor strings must differ, but the obligation/verifier relationship is not loaded from authoritative G-07 history. |
| G07-AC-009 | Evidence provenance | Partial: G-08 evidence has artifact/provenance verification; G-07 evidence requirements and references are not bound to a stored obligation by a service. |
| G07-AC-010 | Atomic persistence/audit | Partial reference mechanics: the generic SQLite transition writes state and event transactionally, but the gate does not require callbacks to use that boundary; production G-09/G-02 binding is absent. |
| G07-AC-011 | Idempotency | Partial generic mechanics: the store supports request-key fingerprints; there is no G-07 command service defining accepted retry semantics. |
| G07-AC-012 | Parent/lineage integrity | Not present as a G-07 relationship model; generic scope can contain data but does not enforce lineage. |
| G07-AC-013 | Recovery reconstruction | Partial reference evidence: generic recovery/reconstruction is tested for kind G07, not an authoritative lifecycle. |
| G07-AC-014 | Fail-closed uncertainty | Partial adapter behavior: unknown, unverified and audit-invalid supplied evidence blocks callbacks; authoritative G-07 closure is absent. |
| G07-AC-015 | Duplicate-runtime detection | Discovery found no competing G-07 runtime, but also found no runtime eligible for acceptance. |

The candidate contract includes five structural tests. The bundled Python runtime did not have pytest installed; direct invocation of the five plain assertion functions under UTF-8 mode passed 5/5. This validates presence of the candidate contract text only; no G-07 runtime acceptance test was executed. The candidate extraction included pytest cache and bytecode artifacts; none were added to the repository.

## Caller-owned boundary and risks

The caller-owned seam is runtime/g07_g08_evidence_gate.py. Both public methods receive an obligation dictionary and a callback. The dictionary is not fetched through ControlBoundaryPort, and the callback can choose its persistence path and state transition. Therefore:

- A caller can provide a requires_evidence value or evidence_ids list that differs from the persisted G-07-shaped record.
- The optional resolution_actor check is based on the supplied dictionary, not a reconstructed G-07 actor record.
- The gate does not apply a G-07 authorization predicate or state-transition matrix.
- Evidence validation and callback commit are separate operations; the gate itself does not establish an atomic G-07 state-plus-audit transaction.
- SQLite/hash-chain tests establish only the stated local reference behavior, not production durability or distributed consistency.

These limitations do not mean the G-08 gate itself is ineffective: for the values it receives, it fails closed on missing, unverified, invalid or audit-integrity-invalid evidence. They mean the values and resulting G-07 transition are not owned by an authoritative G-07 runtime.

## Conflicts, duplicates and recommended boundary

No duplicate G-07 obligation, persistence, audit or evidence model was found. The name “ControlBoundary” refers to the generic G-05/G-06 shared persistence/audit reference boundary, not a G-07 Control Plane. Tests using kind G07 and the G-07/G-08 crash-recovery title can suggest broader integration than exists; the result record explicitly limits that work to generic reference recovery.

After the G-07 lifecycle and authorities are decided, integrate a single G-07 domain/application service into the existing runtime composition. It should own create, assignment, allowed transitions, resolution, independent verification and closure; load the persisted obligation and its evidence requirement; invoke the existing G-08 service/gate using those persisted values; and commit G-07 state plus audit through the existing ControlBoundaryPort. If transaction-scoped evidence validation is required, extend the shared port narrowly. Do not create a second persistence, audit, obligation or evidence model.

## Unresolved Founder decisions and gates

The repository has no controlling G-07 lifecycle/authority specification. These choices remain open and must not be inferred from test fixture states or the acceptance candidate:

1. G-07 lifecycle semantics: assignment, resolution, verification, closure, and rejection, blocked/escalated, reopen or failure paths; whether VERIFIED is terminal or precedes CLOSED.
2. Which obligation fields define immutable scope and evidence requirements, and who may set or amend them.
3. Authority delegation for creation, assignment, resolution, verification and closure; the existing FD-DOC-003 record states that a complete role-to-decision delegation table is absent.
4. Whether an authoritative G-07 runtime may span services/processes and what G-10 distributed consistency guarantees apply.
5. Production G-09 persistence, G-02 audit, physical crash/power-loss guarantees and production execution safety.
6. G-08 authority, acceptance threshold, verification-method qualification, retention and trust-anchor decisions under pending FD-GOV-008-001.

No thresholds, roles, state transitions or distributed-consistency policy are selected here. G-07 is **not claimed integrated**. C1 and production certification are **not claimed**.
