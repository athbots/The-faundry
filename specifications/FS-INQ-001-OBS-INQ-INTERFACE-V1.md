# FS-INQ-001 — OBS → INQ Interface v1

Status: PROPOSAL / ENGINEERING VALIDATION
Authority: CISA
Depends On:
- FS-OBS-002 Semantic Safety Layer v1
- OBS authority and transition model
- Evidence immutability
- Existing triage/graduation controls

## Purpose

Define the controlled interface by which validated observations may produce an Inquiry candidate.

This interface exists to prevent semantic clustering, operator preference, or raw observation volume from directly creating authoritative Inquiry.

## Core principle

`OBS ≠ INQ`

An observation is evidence.
An inquiry is a governed question requiring investigation.

Therefore the interface converts evidence into an **Inquiry Candidate**, not an authoritative Inquiry, unless the existing graduation authority explicitly approves it.

## Input contract

An OBS→INQ request MUST contain:

- `observation_ids`
- `evidence_digest`
- `semantic_relation`
- `provenance`
- `requested_by`
- `reason`
- `schema_version`

The request MUST reference immutable OBS objects. Raw evidence is never copied as a replacement for the source OBS.

## Preconditions

The interface SHALL reject a request when:

1. an observation does not exist;
2. an observation is not in an eligible state;
3. provenance is missing;
4. evidence digest does not match;
5. semantic relation is unsafe;
6. authorization is missing;
7. the request attempts to bypass triage;
8. the request attempts to directly create an authoritative INQ.

## Semantic safety

Allowed candidate-forming relations are:

- `EQUIVALENT`
- `RELATED`
- `CONTRADICTORY`
- `VALUE_CONFLICT`

`DISTINCT` SHALL NOT form an Inquiry Candidate.

`UNIT_MISMATCH` SHALL NOT form an Inquiry Candidate until the measurement conflict is resolved or explicitly triaged.

Contradiction and value conflict are not failures of the interface. They are valid reasons to investigate.

## Output contract

The interface SHALL produce:

`InquiryCandidate`

containing:

- deterministic candidate ID;
- source OBS IDs;
- evidence digest;
- relation;
- provenance;
- reason;
- creation event;
- state = `CANDIDATE`.

It SHALL NOT produce authoritative `INQ` directly.

## Authority boundary

Only the existing triage/graduation authority may promote:

`CANDIDATE → INQ`

The OBS→INQ interface cannot self-authorize graduation.

## Traceability invariant

Every candidate MUST be able to answer:

- Which OBS created this?
- What semantic relation caused it?
- What evidence digest was used?
- Who requested it?
- Why was it created?
- Which authority may promote it?
- Which revision of the interface created it?

## Idempotency

The same ordered set of OBS IDs + relation + evidence digest + schema version SHALL produce the same candidate ID.

Repeating the request SHALL return the existing candidate rather than creating a duplicate.

## Historical preservation

Candidate creation and later graduation are events.

Neither event may rewrite or delete the originating OBS history.

## Failure rule

When required evidence or authority is unavailable:

`FAIL CLOSED`

No candidate is created.

## Validation boundary

This specification validates the OBS→INQ interface primitive.

It does not establish:
- whether a candidate deserves investigation;
- whether an Inquiry is scientifically correct;
- whether an investigation produces useful conclusions;
- production-scale queue behavior.
