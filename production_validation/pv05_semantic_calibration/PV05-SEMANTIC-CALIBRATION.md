# PV-05 — Semantic Calibration

## Purpose

Determine whether the current semantic relation layer preserves the safety boundary required before OBS clustering or INQ graduation.

## Required safety rule

Semantic similarity must never convert:
- contradiction
- unit incompatibility
- value conflict

into `EQUIVALENT`.

## Calibration classes

- EQUIVALENT
- CONTRADICTORY
- UNIT_MISMATCH
- VALUE_CONFLICT
- DISTINCT

## Current corpus

15 adversarial synthetic cases.

## Interpretation

A passing synthetic corpus proves only that the current implementation satisfies these explicitly defined examples.

It does not establish:
- production semantic accuracy;
- false-positive rate;
- false-negative rate;
- domain-general language understanding;
- telemetry normalization quality.

Those require a representative real OBS corpus and a reviewed gold-label set.
