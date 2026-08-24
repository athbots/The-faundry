# FS-DEC-001 — Decision Boundary v1

Status: VALIDATED REFERENCE MODEL

## Core distinction
OBS = evidence
INQ = uncertainty-resolution
DEC = authorized organizational choice

A DEC must be derived from an evidence-backed INQ resolution. It cannot bypass
the INQ boundary when material uncertainty exists.

## Required evidence
A Decision Proposal references INQ IDs, current resolution IDs and digests,
supporting work products, decision question, options, trade-offs, risks,
reversibility, requested authority, and residual uncertainty.

Superseded resolutions cannot silently serve as current evidence.

## Governance
Founder-approved rules carried forward:
- CEO has the highest decision weight.
- CEO has veto authority.
- CEO NO => final NO.
- CEO YES + CFO NO + TEAM NO => final NO.
- CFO and TEAM participate as independent governance signals.

Exact numerical CFO/TEAM weights are NOT invented here; they remain an explicit
governance parameter requiring ratification. The reference model fails closed
when a case requires those unratified weights.

## Decision integrity
Final decisions are immutable. A changed decision creates a new revision with
an explicit SUPERSEDES relation. Votes/signals, rationale, evidence basis,
risks, trade-offs, authority, and residual uncertainty remain traceable.
