# PV-05 Corpus Revision — v1 semantics

Three earlier expectations were corrected because the first v1 specification changed the meaning of the relation classes:

- compatible units normalize to `EQUIVALENT`, not `UNIT_MISMATCH`;
- timestamp difference alone is temporal metadata and yields `RELATED`, not `VALUE_CONFLICT`;
- entity mismatch remains `DISTINCT`.

This is a specification correction, not a test weakening.
