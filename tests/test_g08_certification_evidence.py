import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from runtime.certification_evidence import CertificationEvidence, artifact_digest
from runtime.control_boundary import (
    ControlBoundaryError,
    IdempotencyConflict,
    IntegrityFailure,
    SQLiteControlBoundary,
)
from runtime.g07_g08_evidence_gate import EvidenceResolutionGate
from runtime.canonical_runtime import CanonicalRuntime


class G08EvidenceBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "foundry.sqlite"
        self.boundary = SQLiteControlBoundary(self.path)
        self.grants = {
            ("reviewer", "AUTH-VERIFY", "VERIFICATION_PENDING"),
            ("reviewer", "AUTH-VERIFY", "VERIFIED"),
            ("reviewer", "AUTH-VERIFY", "INVALID"),
            ("reviewer", "AUTH-VERIFY", "FAILED"),
        }
        self.evidence = CertificationEvidence(self.boundary, self.authorized)
        self.gate = EvidenceResolutionGate(self.evidence)

    def tearDown(self):
        self.temp.cleanup()

    def authorized(self, actor, authority_ref, action):
        return (actor, authority_ref, action) in self.grants

    def register(self, identity="EV-001", producer="builder"):
        return self.evidence.register(
            identity, "artifact://build/1", artifact_digest(b"artifact bytes"), producer,
            "AUTH-PRODUCE", {"source_commit": "abc123", "run_id": "run-1"},
            f"create-{identity}",
        )

    def verify(self, identity="EV-001", result="PASS"):
        self.evidence.begin_verification(identity, "reviewer", "AUTH-VERIFY", f"start-{identity}")
        return self.evidence.verify(identity, "reviewer", "AUTH-VERIFY", "digest-review-v1",
                                    result, f"verify-{identity}")

    def obligation(self, evidence_ids=None, **overrides):
        value = {"identity": "OB-001", "requires_evidence": True,
                 "evidence_ids": ["EV-001"] if evidence_ids is None else evidence_ids,
                 "state": "IN_PROGRESS", "resolution_actor": "resolver"}
        value.update(overrides)
        return value

    def test_artifact_digest_is_required_and_bound(self):
        with self.assertRaises(ControlBoundaryError):
            self.evidence.register("EV-BAD", "artifact://bad", "sha256:short", "builder",
                                   "AUTH-P", {"source": "test"}, "create-bad")
        record = self.register()
        self.assertEqual(record["scope"]["artifact_digest"], artifact_digest(b"artifact bytes"))

    def test_producer_cannot_verify_own_evidence(self):
        self.register()
        self.evidence.begin_verification("EV-001", "reviewer", "AUTH-VERIFY", "start")
        with self.assertRaisesRegex(ControlBoundaryError, "producer"):
            self.evidence.verify("EV-001", "builder", "AUTH-VERIFY", "digest-review-v1",
                                 "PASS", "verify")

    def test_evidence_verification_requires_authority_and_pending_state(self):
        self.register()
        with self.assertRaises(ControlBoundaryError):
            self.evidence.verify("EV-001", "reviewer", "AUTH-VERIFY", "digest-review-v1",
                                 "PASS", "verify-before-pending")
        with self.assertRaises(ControlBoundaryError):
            self.evidence.begin_verification("EV-001", "reviewer", "NONE", "start-unauthorized")

    def test_pass_becomes_verified_and_audit_reconstructs(self):
        self.register()
        result = self.verify()
        self.assertEqual(result["state"], "VERIFIED")
        self.assertEqual(self.evidence.require_verified_and_audited("EV-001")["verifier"], "reviewer")
        self.assertEqual(self.boundary.reconstruct("G08", "EV-001")["state"], "VERIFIED")

    def test_fail_result_becomes_invalid_and_blocks_resolution(self):
        self.register()
        self.verify(result="FAIL")
        with self.assertRaisesRegex(ControlBoundaryError, "not VERIFIED"):
            self.gate.enter_resolution_pending(self.obligation(), "resolver", lambda: "committed")

    def test_failed_verification_blocks_resolution(self):
        self.register()
        self.evidence.begin_verification("EV-001", "reviewer", "AUTH-VERIFY", "start")
        self.evidence.fail("EV-001", "reviewer", "AUTH-VERIFY", "tool error", "fail")
        with self.assertRaisesRegex(ControlBoundaryError, "not VERIFIED"):
            self.evidence.require_verified_and_audited("EV-001")

    def test_unverified_evidence_blocks_resolution_without_side_effect(self):
        self.register()
        called = []
        with self.assertRaisesRegex(ControlBoundaryError, "not VERIFIED"):
            self.gate.enter_resolution_pending(self.obligation(), "resolver", lambda: called.append(True))
        self.assertEqual(called, [])

    def test_unknown_evidence_blocks_resolution_without_side_effect(self):
        called = []
        with self.assertRaises(ControlBoundaryError):
            self.gate.enter_resolution_pending(self.obligation(["EV-UNKNOWN"]), "resolver",
                                               lambda: called.append(True))
        self.assertEqual(called, [])

    def test_any_explicit_unknown_evidence_reference_blocks_even_when_not_required(self):
        called = []
        obligation = self.obligation(["EV-UNKNOWN"], requires_evidence=False)
        with self.assertRaises(ControlBoundaryError):
            self.gate.enter_resolution_pending(obligation, "resolver", lambda: called.append(True))
        self.assertEqual(called, [])

    def test_explicit_non_evidence_obligation_can_use_transition_without_evidence_ids(self):
        obligation = {"identity": "OB-NO-EVIDENCE", "requires_evidence": False}
        self.assertEqual(self.gate.enter_resolution_pending(obligation, "resolver", lambda: "ok"), "ok")

    def test_missing_required_evidence_reference_blocks_resolution(self):
        called = []
        with self.assertRaisesRegex(ControlBoundaryError, "no evidence references"):
            self.gate.enter_resolution_pending(self.obligation([]), "resolver", lambda: called.append(True))
        self.assertEqual(called, [])

    def test_all_verified_evidence_allows_one_delegated_g07_transition(self):
        self.register()
        self.verify()
        calls = []
        result = self.gate.enter_resolution_pending(
            self.obligation(), "resolver", lambda: calls.append("RESOLUTION_PENDING") or "ok"
        )
        self.assertEqual(result, "ok")
        self.assertEqual(calls, ["RESOLUTION_PENDING"])

    def test_audit_tampering_blocks_verified_evidence(self):
        self.register()
        self.verify()
        db = sqlite3.connect(self.path)
        try:
            row = db.execute(
                "SELECT event FROM control_events WHERE kind='G08' AND object_id='EV-001' AND version=1"
            ).fetchone()
            event = json.loads(row[0])
            event["evidence"]["artifact_digest"] = "sha256:" + "0" * 64
            db.execute(
                "UPDATE control_events SET event=? WHERE kind='G08' AND object_id='EV-001' AND version=1",
                (json.dumps(event),),
            )
            db.commit()
        finally:
            db.close()
        with self.assertRaises(IntegrityFailure):
            self.gate.enter_resolution_pending(self.obligation(), "resolver", lambda: "must-not-run")

    def test_scope_mutation_blocks_record_use(self):
        self.register()
        self.verify()
        db = sqlite3.connect(self.path)
        try:
            row = db.execute(
                "SELECT document FROM control_aggregates WHERE kind='G08' AND object_id='EV-001'"
            ).fetchone()
            document = json.loads(row[0])
            document["scope"]["artifact_uri"] = "artifact://substituted"
            db.execute(
                "UPDATE control_aggregates SET document=? WHERE kind='G08' AND object_id='EV-001'",
                (json.dumps(document),),
            )
            db.commit()
        finally:
            db.close()
        with self.assertRaises(IntegrityFailure):
            self.gate.enter_resolution_pending(self.obligation(), "resolver", lambda: "must-not-run")

    def test_duplicate_registration_is_idempotent_and_conflicting_retry_rejected(self):
        first = self.register()
        second = self.register()
        self.assertEqual(first, second)
        with self.assertRaises(IdempotencyConflict):
            self.evidence.register("EV-001", "artifact://different", artifact_digest(b"different"),
                                  "builder", "AUTH-PRODUCE", {"source_commit": "abc123"},
                                  "create-EV-001")

    def test_duplicate_verification_retry_is_idempotent_after_terminal_state(self):
        self.register()
        self.evidence.begin_verification("EV-001", "reviewer", "AUTH-VERIFY", "start")
        first = self.evidence.verify("EV-001", "reviewer", "AUTH-VERIFY", "digest-review-v1",
                                     "PASS", "verify")
        retry = self.evidence.verify("EV-001", "reviewer", "AUTH-VERIFY", "digest-review-v1",
                                     "PASS", "verify")
        self.assertEqual(first, retry)
        self.assertEqual(len(self.boundary.history("G08", "EV-001")), 3)

    def test_g07_resolution_actor_cannot_verify_own_obligation(self):
        self.register()
        self.verify()
        obligation = self.obligation(state="RESOLUTION_PENDING")
        with self.assertRaisesRegex(ControlBoundaryError, "cannot verify own obligation"):
            self.gate.verify_resolution(obligation, "resolver", "resolver", lambda: "must-not-run")

    def test_independent_g07_verifier_can_use_verified_evidence(self):
        self.register()
        self.verify()
        obligation = self.obligation(state="RESOLUTION_PENDING")
        self.assertEqual(self.gate.verify_resolution(obligation, "resolver", "independent",
                                                     lambda: "verified"), "verified")

    def test_resolution_gate_requires_explicit_evidence_requirement(self):
        with self.assertRaisesRegex(ControlBoundaryError, "must be explicit"):
            self.gate.enter_resolution_pending({"identity": "OB-1"}, "resolver", lambda: None)

    def test_canonical_runtime_exposes_g08_and_boundary_adapter(self):
        runtime = CanonicalRuntime(self.boundary, self.authorized)
        self.assertIsInstance(runtime.certification_evidence, CertificationEvidence)
        self.assertIsInstance(runtime.evidence_resolution_gate, EvidenceResolutionGate)


if __name__ == "__main__":
    unittest.main()
