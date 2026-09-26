"""Narrow G-07/G-08 evidence gate adapter.

This module guards a caller-owned G-07 transition callback. It does not own or
redefine G-07 obligation lifecycle, resolution semantics, or G-10 consistency.
"""

from __future__ import annotations

from typing import Callable

from runtime.certification_evidence import CertificationEvidence
from runtime.control_boundary import ControlBoundaryError


class EvidenceResolutionGate:
    def __init__(self, evidence: CertificationEvidence):
        self.evidence = evidence

    def enter_resolution_pending(self, obligation: dict, resolution_actor: str,
                                 commit_transition: Callable[[], object]):
        """Run the supplied G-07 transition only after every required record passes."""
        self._validate_obligation(obligation)
        if not resolution_actor:
            raise ControlBoundaryError("G-07 resolution actor is required")
        self._validate_evidence_refs(obligation)
        return commit_transition()

    def verify_resolution(self, obligation: dict, resolution_actor: str,
                          verifier: str, commit_verification: Callable[[], object]):
        """Enforce independent G-07 obligation verification before delegated commit."""
        self._validate_obligation(obligation)
        if obligation.get("state") != "RESOLUTION_PENDING":
            raise ControlBoundaryError("G-07 obligation must be RESOLUTION_PENDING before verification")
        if not resolution_actor or not verifier or verifier == resolution_actor:
            raise ControlBoundaryError("G-07 resolution actor cannot verify own obligation")
        if obligation.get("resolution_actor") not in {None, resolution_actor}:
            raise ControlBoundaryError("G-07 resolution actor does not match recorded resolution")
        self._validate_evidence_refs(obligation)
        return commit_verification()

    def _validate_evidence_refs(self, obligation: dict) -> None:
        evidence_ids = obligation.get("evidence_ids", [])
        if obligation["requires_evidence"] and not evidence_ids:
            raise ControlBoundaryError("evidence-required obligation has no evidence references")
        for evidence_id in evidence_ids:
            self.evidence.require_verified_and_audited(evidence_id)

    @staticmethod
    def _validate_obligation(obligation: dict) -> None:
        if not isinstance(obligation, dict) or not obligation.get("identity"):
            raise ControlBoundaryError("G-07 obligation identity is required")
        if not isinstance(obligation.get("requires_evidence"), bool):
            raise ControlBoundaryError("G-07 evidence requirement must be explicit")
        evidence_ids = obligation.get("evidence_ids", [])
        if not isinstance(evidence_ids, list) or any(not isinstance(item, str) or not item for item in evidence_ids):
            raise ControlBoundaryError("G-07 evidence references must be explicit identifiers")
