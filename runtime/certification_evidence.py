"""G-08 certification evidence reference service.

Evidence records use the existing control boundary so aggregate state, event
history, idempotency, and audit linkage share the G-05/G-06 reference store.
This module does not define certification thresholds or production authority.
"""

from __future__ import annotations

import hashlib
import re
from typing import Callable

from runtime.control_boundary import (
    ControlBoundaryError,
    ControlBoundaryPort,
    IntegrityFailure,
    _digest,
)


class CertificationEvidence:
    KIND = "G08"
    TRANSITIONS = {
        "REGISTERED": {"VERIFICATION_PENDING"},
        "VERIFICATION_PENDING": {"VERIFIED", "INVALID", "FAILED"},
        "VERIFIED": set(),
        "INVALID": set(),
        "FAILED": set(),
    }
    _SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")

    def __init__(self, boundary: ControlBoundaryPort,
                 authorize: Callable[[str, str, str], bool]):
        self.boundary = boundary
        self.authorize = authorize

    def register(self, identity: str, artifact_uri: str, artifact_digest: str,
                 producer: str, authority_ref: str, provenance: dict,
                 request_key: str) -> dict:
        if not all((identity, artifact_uri, producer, authority_ref, request_key)):
            raise ControlBoundaryError("evidence identity, artifact, producer and provenance are required")
        if not isinstance(provenance, dict) or not provenance:
            raise ControlBoundaryError("evidence provenance is required")
        if not isinstance(artifact_digest, str) or not self._SHA256.fullmatch(artifact_digest):
            raise ControlBoundaryError("evidence requires a SHA-256 artifact digest")
        scope = {"artifact_uri": artifact_uri, "artifact_digest": artifact_digest,
                 "producer": producer}
        immutable_provenance = {**provenance, "authority_ref": authority_ref}
        document = {
            "identity": identity,
            "scope": scope,
            "scope_digest": _digest(scope),
            "proposer": producer,
            "producer": producer,
            "provenance": immutable_provenance,
            "provenance_digest": _digest(immutable_provenance),
            "state": "REGISTERED",
            "version": 0,
            "evidence": [],
            "verifier": None,
        }
        return self.boundary.create(self.KIND, identity, document, request_key)

    def begin_verification(self, identity: str, actor: str, authority_ref: str,
                           request_key: str) -> dict:
        current = self.record(identity)
        self._require_authority(actor, authority_ref, "VERIFICATION_PENDING")
        return self.boundary.transition(
            self.KIND, identity, "REGISTERED", "VERIFICATION_PENDING", actor,
            authority_ref, {"event": "verification_started"}, request_key,
        )

    def verify(self, identity: str, verifier: str, authority_ref: str,
               verification_method: str, result: str, request_key: str) -> dict:
        current = self.record(identity)
        if result not in {"PASS", "FAIL"}:
            raise ControlBoundaryError("verification result must be PASS or FAIL")
        if not verification_method:
            raise ControlBoundaryError("verification method is required")
        if verifier == current["producer"]:
            raise ControlBoundaryError("evidence producer cannot independently verify own evidence")
        target = "VERIFIED" if result == "PASS" else "INVALID"
        self._require_authority(verifier, authority_ref, target)
        return self.boundary.transition(
            self.KIND, identity, "VERIFICATION_PENDING", target, verifier,
            authority_ref,
            {"verification_method": verification_method, "result": result,
             "artifact_digest": current["scope"]["artifact_digest"]},
            request_key,
            extra={"verifier": verifier},
        )

    def fail(self, identity: str, actor: str, authority_ref: str,
             failure: str, request_key: str) -> dict:
        current = self.record(identity)
        if not failure:
            raise ControlBoundaryError("verification failure requires a recorded reason")
        self._require_authority(actor, authority_ref, "FAILED")
        return self.boundary.transition(
            self.KIND, identity, "VERIFICATION_PENDING", "FAILED", actor,
            authority_ref, {"failure": failure}, request_key,
        )

    def record(self, identity: str) -> dict:
        document = self.boundary.reconstruct(self.KIND, identity)
        if (document.get("identity") != identity or
                _digest(document.get("scope")) != document.get("scope_digest") or
                _digest(document.get("provenance")) != document.get("provenance_digest") or
                document.get("producer") != document.get("scope", {}).get("producer")):
            raise IntegrityFailure("evidence identity or immutable provenance failed integrity")
        return document

    def require_verified_and_audited(self, identity: str) -> dict:
        document = self.record(identity)
        if document.get("state") != "VERIFIED":
            raise ControlBoundaryError("evidence is not VERIFIED")
        verifier = document.get("verifier")
        if not verifier or verifier == document.get("producer"):
            raise IntegrityFailure("verified evidence lacks an independent verifier")
        events = self.boundary.history(self.KIND, identity)
        if not events or any(not event.get("audit_ref") for event in events):
            raise IntegrityFailure("evidence audit linkage is incomplete")
        verification_events = [event for event in events if event.get("to") == "VERIFIED"]
        if len(verification_events) != 1:
            raise IntegrityFailure("evidence verification audit is missing or ambiguous")
        verification_event = verification_events[0]
        if (verification_event.get("actor") != verifier or
                verification_event.get("evidence", {}).get("result") != "PASS" or
                not verification_event.get("evidence", {}).get("verification_method") or
                not verification_event.get("authority_ref") or
                verification_event.get("evidence", {}).get("artifact_digest") !=
                document["scope"]["artifact_digest"]):
            raise IntegrityFailure("evidence verification audit does not match the record")
        return document

    def _require_authority(self, actor: str, authority_ref: str, action: str) -> None:
        if not actor or not authority_ref or not self.authorize(actor, authority_ref, action):
            raise ControlBoundaryError("required evidence authority was not established")


def artifact_digest(payload: bytes) -> str:
    """Return the canonical G-08 SHA-256 digest representation."""
    return "sha256:" + hashlib.sha256(payload).hexdigest()
