# REAL-SEM-01 — Representative OBS Semantic Validation

Status: MANDATORY FUTURE GATE
Authority: CISA

## Purpose

Determine whether FS-OBS-002 remains safe and useful against representative real OBS data rather than only synthetic adversarial cases.

## Required evidence

A reviewed gold-label corpus covering:
- entity resolution;
- predicate normalization;
- contradiction;
- equivalent observations;
- value conflict;
- unit normalization;
- temporal context;
- ambiguous observations;
- incomplete observations.

## Required measurements

At minimum:
- precision;
- recall;
- false-positive rate;
- false-negative rate;
- unresolved/abstention rate.

## Acceptance rule

No single aggregate accuracy score is sufficient.

Safety-critical false equivalence and false contradiction classes must be separately measured.

## Status

Not yet executed.

FS-OBS-002 remains canonical, but production semantic certification is prohibited until this gate is passed or explicitly re-scoped by a later ratified decision.
