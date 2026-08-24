# PV-05 v1-r3 Decision

The calibration corpus was corrected to distinguish:

- compatible units with different physical values -> VALUE_CONFLICT;
- compatible units with equal physical values -> EQUIVALENT;
- incompatible/unresolvable measurement families -> UNIT_MISMATCH;
- timestamp-only difference -> RELATED.

This preserves semantic correctness instead of treating unit labels themselves as contradictions.
