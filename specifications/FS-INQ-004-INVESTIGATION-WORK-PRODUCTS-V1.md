# FS-INQ-004 — Investigation Work Products v1

Status: PROPOSAL / ENGINEERING VALIDATION
Depends on: FS-INQ-002 v1 and FS-INQ-003 v1

## Purpose

Define the institutional artifacts produced during an INQ investigation without
turning INQ into a generic project-management system.

## Core decision

An investigation produces **evidence-bearing work products**.

A work product is not merely a task completion record. It must preserve:
- what was done;
- why it was done;
- inputs;
- outputs;
- actor;
- authority;
- method/tool version;
- time;
- provenance;
- result;
- limitations.

## Work-product classes

v1 defines six classes:

1. `OBSERVATION` — a newly acquired observation produced during investigation.
2. `EXPERIMENT` — a controlled intervention/test with defined method and expected result.
3. `ANALYSIS` — a transformation or interpretation of existing evidence.
4. `SIMULATION` — a computational/model-based investigation artifact.
5. `REVIEW` — an independent assessment of an evidence-bearing result.
6. `DECISION_EVIDENCE` — a bounded synthesis explicitly prepared for a future decision authority.

A work product may reference other work products but may not erase or replace their history.

## Mandatory provenance

Every work product MUST contain:

- `work_product_id`
- `inq_id`
- `class`
- `title`
- `purpose`
- `inputs`
- `outputs`
- `actor`
- `authority`
- `method`
- `method_version`
- `created_at`
- `result`
- `limitations`
- `provenance`
- `schema_version`

## Result rule

A work product result is a claim about the work performed.

It is NOT automatically an INQ resolution.

Only the INQ resolution authority can convert accumulated evidence into a resolution.

## Negative results

Negative, failed, inconclusive, or null results are first-class work products.

The system MUST NOT discard them because they do not support the current hypothesis.

## Reproducibility

Where technically applicable, a work product MUST identify:
- method/tool;
- version;
- inputs;
- relevant parameters;
- output references.

## Independence

A REVIEW work product must identify the reviewed work product and reviewer.

The author of the original work product cannot be represented as an independent reviewer for the same artifact.

## Immutability

Work products are append-only after creation.

Corrections use a new work product or explicit amendment/supersession mechanism.

## Boundary to resolution

The INQ may aggregate work products into an evidence basis.

It cannot treat:
- number of work products;
- elapsed time;
- task completion;
- reviewer approval alone

as proof of resolution.

Resolution requires an explicit statement and evidence basis under FS-INQ-002.

## Boundary to DEC

`DECISION_EVIDENCE` prepares evidence for a future DEC authority.

It does not create or authorize a decision.

## Validation boundary

This specification validates the work-product primitive and its provenance/authority rules.

It does not certify:
- scientific correctness of a method;
- domain-specific experimental validity;
- production storage;
- distributed collaboration.
