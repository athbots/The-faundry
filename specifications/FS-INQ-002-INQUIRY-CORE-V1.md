# FS-INQ-002 — Inquiry Core v1

Status: PROPOSAL / ENGINEERING VALIDATION
Purpose: define what an INQ is and what institutional capability it provides.

## Foundational decision

INQ is primarily an **uncertainty-resolution object**.

It exists to turn a material uncertainty, conflict, anomaly, or unresolved question into a governed investigation.

Therefore:

- OBS = evidence
- INQ = governed uncertainty-resolution process
- DEC = decision made from sufficiently resolved evidence

INQ may support hypothesis testing and decision preparation, but INQ is not itself a decision.

## Why this model is preferred

This avoids four architectural failures:

1. Treating every observation as a problem.
2. Treating every conflict as a decision request.
3. Making the investigation object equivalent to a hypothesis.
4. Allowing an investigation mechanism to acquire decision authority.

The canonical relationship is:

OBS → INQ → evidence synthesis → DEC

where DEC is a later governance boundary, not part of INQ v1.

## INQ object

An INQ SHALL contain:

- `inq_id`
- `title`
- `question`
- `status`
- `trigger_observation_ids`
- `evidence_digest`
- `reason`
- `scope`
- `hypotheses`
- `investigation_plan`
- `owner`
- `authority`
- `created_at`
- `schema_version`

## Status lifecycle

`CANDIDATE → OPEN → INVESTIGATING → RESOLVED → CLOSED`

Additional terminal state:

`CANCELLED`

Rules:

- CANDIDATE requires triage authority to become OPEN.
- OPEN establishes a bounded investigation.
- INVESTIGATING means active evidence acquisition/evaluation.
- RESOLVED requires an explicit resolution statement and evidence basis.
- CLOSED requires closure authority.
- CANCELLED requires an explicit reason and authority.
- No state transition may delete historical events.

## What INQ is for

INQ may represent:

### 1. Uncertainty
"Why did system X change?"

### 2. Conflict
"Which of these incompatible observations is supported?"

### 3. Anomaly
"Why did this behavior depart from the expected operating envelope?"

### 4. Hypothesis test
"Does hypothesis H explain the observed evidence?"

### 5. Decision preparation
"What evidence must be established before a decision can be responsibly made?"

The fifth case prepares a later DEC object; INQ does not make the decision.

## What INQ is NOT

INQ is not:

- raw telemetry;
- a semantic cluster;
- a final conclusion;
- an authorization;
- a decision;
- a task list without a question;
- a generic project-management ticket.

## Resolution requirement

An INQ cannot become RESOLVED merely because work was performed.

It requires:

- resolution statement;
- evidence references;
- confidence/uncertainty statement;
- unresolved residuals, if any;
- authority record.

## Institutional invariant

Every INQ must answer:

1. What uncertainty are we resolving?
2. Why does it matter?
3. What evidence triggered it?
4. What would count as resolution?
5. What remains unknown?
6. Who is authorized to close it?

## Anti-loop rule

An INQ must not create another INQ solely because it exists.

A new INQ requires a distinct uncertainty with independent evidence or a formally identified unresolved residual.

## Boundary to DEC

INQ produces a resolution/evidence state.

A later DEC object may consume the resolved evidence.

No INQ transition may directly authorize organizational action outside its investigation authority.

## Validation boundary

FS-INQ-002 v1 defines the canonical INQ primitive and lifecycle.

It does not yet define:
- the full DEC system;
- organizational strategy;
- resource allocation;
- enterprise workflow;
- production-scale investigation scheduling.
