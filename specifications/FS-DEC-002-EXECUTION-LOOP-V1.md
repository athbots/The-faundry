# FS-DEC-002 — Decision Revision, Execution Authorization & Closed-Loop Verification v1

Status: VALIDATED REFERENCE MODEL
Depends on: FS-DEC-001, FS-INQ-005

## Purpose

Define what happens after a decision is made.

The Foundry must distinguish:

DECISION → AUTHORIZED EXECUTION → OBSERVED OUTCOME → VERIFICATION

A decision does not itself execute.

## Decision immutability

A final DecisionRecord is immutable.

If the institution changes a decision, it creates a new DecisionRevision with:

- predecessor decision ID;
- predecessor digest;
- change reason;
- new decision outcome;
- authority;
- evidence basis.

The predecessor remains permanently addressable.

## Execution authorization

Only a final `YES` decision may request execution authorization.

An execution authorization MUST contain:

- decision ID and decision digest;
- execution scope;
- responsible executor;
- authorization authority;
- start conditions;
- stop/abort conditions;
- expected outcome;
- verification plan;
- rollback/containment plan;
- schema version.

Execution authorization does not change the Decision.

## Fail-closed conditions

Authorization is denied if:

- decision is unknown;
- decision outcome is not YES;
- decision digest does not match;
- executor is missing;
- scope is missing;
- stop conditions are missing;
- verification plan is missing;
- authorization authority is missing.

## Execution lifecycle

`AUTHORIZED → EXECUTING → VERIFYING → VERIFIED`

Alternative terminal state:

`ABORTED`

An execution cannot become VERIFIED merely because the executor reports success.

Verification requires outcome evidence.

## Closed-loop verification

After execution, the system produces outcome observations:

`EXECUTION → OBS`

Those OBS become the evidence used to verify whether the decision produced its expected result.

If the expected result is not supported:

`VERIFICATION FAILURE → INQ`

The system must not force an execution failure into a successful DEC.

## Containment

If stop/abort conditions are triggered, execution moves to ABORTED and records:

- trigger;
- time;
- executor;
- observed evidence;
- containment action.

## Revision relationship

Decision revisions use:

`D2 SUPERSEDES D1`

No previous decision is edited.

An execution already authorized under D1 does not silently become authorized under D2.

## Institutional loop

Canonical loop:

OBS → INQ → RESOLUTION → DEC → EXECUTION → OBS

This is the minimum closed-loop operating cycle.

## Boundary

This is a reference institutional execution model.

It does not certify real-world safety, legal authorization, infrastructure rollback, or domain-specific operational controls.
