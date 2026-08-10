# Repository Charter

**Version:** Genesis G-0.1  
**Status:** Active

## Purpose

Define how The Foundry repository represents, versions, validates, and releases institutional artifacts.

## Core rule

The repository is a representation layer. It is not the institution itself.

## Source-of-truth hierarchy

1. Constitutional meaning: `CONST-001`
2. Institutional behavioral invariants: `IP-001`
3. Universal object structure: `FM-001`
4. Ratified type specifications
5. Ratified object instances
6. Derived representations and exports

## Change control

Frozen foundation artifacts SHALL NOT be edited in place to conceal change.

A proposed change SHALL:
- identify the affected artifact;
- identify the contradiction or new requirement;
- describe impact on dependencies;
- preserve prior wording/history;
- receive the authority required by the affected layer;
- produce a new version.

## Git rule

Git history is part of repository provenance but SHALL NOT replace the institutional revision history defined by FM-001.

## Representation rule

A filename, directory, commit, branch, or Git tag is not an ObjectID.

## Release rule

A release is a reproducible snapshot of the repository state identified by a release identifier.

## Current release

`GENESIS-G0.1`
