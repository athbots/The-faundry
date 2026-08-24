# FS-INQ-003 — INQ Evidence Amendment & Resolution Conflict v1

Status: PROPOSAL / ENGINEERING VALIDATION
Depends on: FS-INQ-002 v1

## Problem

A resolved INQ must remain historically immutable when new evidence arrives or a later analysis conflicts with its resolution.

Therefore the system needs an explicit amendment/supersession mechanism rather than reopening or overwriting the original INQ.

## Core model

A resolved INQ is immutable.

New material evidence creates an `Amendment` object referencing the original INQ.

An amendment may produce one of three outcomes:

1. `CORROBORATES` — strengthens the existing resolution.
2. `INSUFFICIENT` — does not change the resolution.
3. `CONFLICTS` — materially challenges the resolution.

An amendment never edits the original resolution.

## Conflict handling

A `CONFLICTS` amendment creates a `ResolutionConflict` object.

The conflict contains:

- original INQ ID;
- original resolution digest;
- new evidence IDs;
- amendment ID;
- conflict statement;
- authority;
- status;
- event history.

Conflict lifecycle:

`OPEN → REVIEWING → RESOLVED`

or:

`OPEN → ESCALATED`

A conflict may not silently change the original INQ.

## Supersession

Only an authorized resolution process may create a `SUPERSEDES` relationship.

The original resolution remains permanently accessible.

The new resolution references the old resolution and explains why it supersedes it.

## Evidence amendment rules

New evidence arriving after closure MUST NOT be appended directly into the historical INQ evidence set.

Instead:

`new evidence → Amendment → assessment`

## Safety rules

- No mutation of historical resolution.
- No silent reopening.
- No deletion of old evidence references.
- No conflict resolution without explicit authority.
- No supersession without an evidence basis.
- Every amendment/conflict action is event logged.
- A conflict cannot self-resolve merely because a new result exists.

## Boundary

This specification defines historical integrity and conflict handling.

It does not yet define:
- multi-user distributed locking;
- full investigation work products;
- DEC;
- production persistence.
