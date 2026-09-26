from contextlib import contextmanager
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from runtime.certification_evidence import CertificationEvidence, artifact_digest
from runtime.control_boundary import (
    ControlBoundaryError,
    IdempotencyConflict,
    IntegrityFailure,
    SQLiteControlBoundary,
    _digest,
)
from runtime.crash_recovery_boundary import CrashRecoveryBoundary
from runtime.g07_g08_evidence_gate import EvidenceResolutionGate


@contextmanager
def database(path):
    connection = sqlite3.connect(path)
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


class CrashRecoveryBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "foundry-control.sqlite"
        self.store = SQLiteControlBoundary(self.path)
        self.recovery = CrashRecoveryBoundary(self.store)
        self.grants = {
            ("reviewer", "AUTH-VERIFY", "VERIFICATION_PENDING"),
            ("reviewer", "AUTH-VERIFY", "VERIFIED"),
            ("reviewer", "AUTH-VERIFY", "INVALID"),
        }
        self.evidence = CertificationEvidence(self.recovery, self.authorized)
        self.gate = EvidenceResolutionGate(self.evidence)

    def tearDown(self):
        self.temp.cleanup()

    def authorized(self, actor, authority_ref, action):
        return (actor, authority_ref, action) in self.grants

    @staticmethod
    def document(identity="OB-001", state="OPEN"):
        scope = {"obligation": identity}
        provenance = {"source": "crash-boundary-test", "authority_ref": "AUTH-TEST"}
        return {
            "identity": identity,
            "scope": scope,
            "scope_digest": _digest(scope),
            "proposer": "originator",
            "provenance": provenance,
            "provenance_digest": _digest(provenance),
            "state": state,
            "version": 0,
            "evidence": [],
        }

    def create_record(self, identity="OB-001", state="OPEN"):
        return self.recovery.create("G07", identity, self.document(identity, state), f"create-{identity}")

    def _terminate_mid_transaction(self, operation, object_id):
        script = r'''
import os, sys
from runtime.control_boundary import SQLiteControlBoundary

class TerminateBeforeCommit(SQLiteControlBoundary):
    def _append_event(self, db, kind, object_id, version, event):
        super()._append_event(db, kind, object_id, version, event)
        os._exit(73)

store = TerminateBeforeCommit(sys.argv[1])
if sys.argv[2] == "create":
    from runtime.control_boundary import _digest
    identity = sys.argv[3]
    scope = {"obligation": identity}
    provenance = {"source": "crash-test", "authority_ref": "AUTH-TEST"}
    document = {"identity": identity, "scope": scope, "scope_digest": _digest(scope),
                "proposer": "originator", "provenance": provenance,
                "provenance_digest": _digest(provenance), "state": "OPEN",
                "version": 0, "evidence": []}
    store.create("G07", identity, document, "crash-create")
else:
    store.transition("G07", sys.argv[3], "OPEN", "RESOLUTION_PENDING", "resolver",
                     "AUTH-TEST", {"attempt": "crash"}, "crash-transition")
'''
        return subprocess.run([sys.executable, "-c", script, str(self.path), operation, object_id],
                              cwd=Path(__file__).resolve().parents[1], check=False,
                              capture_output=True, text=True)

    def register_evidence(self, identity="EV-001"):
        return self.evidence.register(identity, "artifact://test/result", artifact_digest(b"result"),
                                      "producer", "AUTH-PRODUCE", {"commit": "abc"},
                                      f"create-{identity}")

    def verify_evidence(self, identity="EV-001"):
        self.evidence.begin_verification(identity, "reviewer", "AUTH-VERIFY", f"start-{identity}")
        return self.evidence.verify(identity, "reviewer", "AUTH-VERIFY", "hash-review-v1",
                                    "PASS", f"verify-{identity}")

    def obligation(self, evidence_ids=None, **overrides):
        result = {"identity": "OB-001", "state": "RESOLUTION_PENDING",
                  "requires_evidence": True, "evidence_ids": ["EV-001"] if evidence_ids is None else evidence_ids,
                  "resolution_actor": "resolver"}
        result.update(overrides)
        return result

    def test_crash_during_creation_commits_neither_aggregate_nor_audit(self):
        result = self._terminate_mid_transaction("create", "OB-CRASH-CREATE")
        self.assertEqual(result.returncode, 73)
        with database(self.path) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM control_aggregates WHERE object_id='OB-CRASH-CREATE'").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM control_events WHERE object_id='OB-CRASH-CREATE'").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM control_idempotency WHERE object_id='OB-CRASH-CREATE'").fetchone()[0], 0)

    def test_crash_before_transition_commit_preserves_prior_state_and_audit(self):
        self.create_record("OB-CRASH-TRANSITION")
        result = self._terminate_mid_transaction("transition", "OB-CRASH-TRANSITION")
        self.assertEqual(result.returncode, 73)
        reopened = CrashRecoveryBoundary(SQLiteControlBoundary(self.path))
        recovered = reopened.recover("G07", "OB-CRASH-TRANSITION")
        self.assertEqual(recovered["state"], "OPEN")
        self.assertEqual(recovered["version"], 0)
        self.assertEqual([event["to"] for event in reopened.history("G07", "OB-CRASH-TRANSITION")], ["OPEN"])

    def test_committed_state_survives_restart_and_reconstructs(self):
        self.create_record()
        self.recovery.transition("G07", "OB-001", "OPEN", "RESOLUTION_PENDING", "resolver",
                                 "AUTH-TEST", {"change": "resolution"}, "commit-1")
        reopened = CrashRecoveryBoundary(SQLiteControlBoundary(self.path))
        self.assertEqual(reopened.recover("G07", "OB-001")["state"], "RESOLUTION_PENDING")

    def test_exact_retry_is_idempotent_after_restart(self):
        self.create_record()
        first = self.recovery.transition("G07", "OB-001", "OPEN", "RESOLUTION_PENDING", "resolver",
                                         "AUTH-TEST", {"change": "resolution"}, "same-request")
        reopened = CrashRecoveryBoundary(SQLiteControlBoundary(self.path))
        retry = reopened.transition("G07", "OB-001", "OPEN", "RESOLUTION_PENDING", "resolver",
                                    "AUTH-TEST", {"change": "resolution"}, "same-request")
        self.assertEqual(first, retry)
        self.assertEqual(len(reopened.history("G07", "OB-001")), 2)

    def test_idempotency_collision_is_rejected(self):
        self.create_record()
        self.recovery.transition("G07", "OB-001", "OPEN", "RESOLUTION_PENDING", "resolver",
                                 "AUTH-TEST", {"change": "first"}, "request-key")
        with self.assertRaises(IdempotencyConflict):
            self.recovery.transition("G07", "OB-001", "OPEN", "CLOSED", "resolver",
                                     "AUTH-TEST", {"change": "different"}, "request-key")

    def test_audit_chain_tampering_is_detected_after_restart(self):
        self.create_record()
        self.recovery.transition("G07", "OB-001", "OPEN", "RESOLUTION_PENDING", "resolver",
                                 "AUTH-TEST", {"change": "resolution"}, "commit-1")
        with database(self.path) as db:
            db.execute("UPDATE control_events SET event=? WHERE kind='G07' AND object_id='OB-001' AND version=1",
                       (json.dumps({"forged": True}),))
        with self.assertRaises(IntegrityFailure):
            CrashRecoveryBoundary(SQLiteControlBoundary(self.path)).recover("G07", "OB-001")

    def test_aggregate_state_hash_tampering_is_detected(self):
        self.create_record()
        with database(self.path) as db:
            row = db.execute("SELECT document FROM control_aggregates WHERE kind='G07' AND object_id='OB-001'").fetchone()
            document = json.loads(row[0])
            document["evidence"].append({"unrecorded": "mutation"})
            db.execute("UPDATE control_aggregates SET document=? WHERE kind='G07' AND object_id='OB-001'",
                       (json.dumps(document),))
        with self.assertRaises(IntegrityFailure):
            self.recovery.recover("G07", "OB-001")

    def test_state_hash_is_bound_into_the_audit_chain(self):
        self.create_record()
        with database(self.path) as db:
            row = db.execute("SELECT event FROM control_events WHERE kind='G07' AND object_id='OB-001' AND version=0").fetchone()
            event = json.loads(row[0])
            event["state_hash"] = "0" * 64
            db.execute("UPDATE control_events SET event=? WHERE kind='G07' AND object_id='OB-001' AND version=0",
                       (json.dumps(event),))
        with self.assertRaises(IntegrityFailure):
            self.recovery.recover("G07", "OB-001")

    def test_recovery_adapter_reconstructs_every_committed_transition(self):
        self.create_record()
        result = self.recovery.transition("G07", "OB-001", "OPEN", "RESOLUTION_PENDING", "resolver",
                                          "AUTH-TEST", {"change": "resolution"}, "commit-1")
        self.assertEqual(result["state_hash"], self.recovery.recover("G07", "OB-001")["state_hash"])

    def test_unverified_evidence_does_not_survive_as_resolution_authority(self):
        self.register_evidence()
        reopened_evidence = CertificationEvidence(CrashRecoveryBoundary(SQLiteControlBoundary(self.path)), self.authorized)
        gate = EvidenceResolutionGate(reopened_evidence)
        called = []
        with self.assertRaisesRegex(ControlBoundaryError, "not VERIFIED"):
            gate.enter_resolution_pending(self.obligation(), "resolver", lambda: called.append(True))
        self.assertEqual(called, [])

    def test_g08_verification_and_audit_reconstruct_after_restart(self):
        self.register_evidence()
        self.verify_evidence()
        reopened = CertificationEvidence(CrashRecoveryBoundary(SQLiteControlBoundary(self.path)), self.authorized)
        self.assertEqual(reopened.require_verified_and_audited("EV-001")["state"], "VERIFIED")

    def test_g08_producer_cannot_self_verify_after_recovery(self):
        self.register_evidence()
        self.evidence.begin_verification("EV-001", "reviewer", "AUTH-VERIFY", "start")
        recovered = CertificationEvidence(CrashRecoveryBoundary(SQLiteControlBoundary(self.path)), self.authorized)
        with self.assertRaisesRegex(ControlBoundaryError, "producer"):
            recovered.verify("EV-001", "producer", "AUTH-VERIFY", "hash-review-v1", "PASS", "verify")

    def test_unknown_g08_reference_blocks_g07_transition(self):
        called = []
        with self.assertRaises(ControlBoundaryError):
            self.gate.enter_resolution_pending(self.obligation(["EV-UNKNOWN"]), "resolver", lambda: called.append(True))
        self.assertEqual(called, [])

    def test_g08_audit_integrity_failure_blocks_g07_transition(self):
        self.register_evidence()
        self.verify_evidence()
        with database(self.path) as db:
            row = db.execute("SELECT event FROM control_events WHERE kind='G08' AND object_id='EV-001' AND version=1").fetchone()
            event = json.loads(row[0])
            event["evidence"]["artifact_digest"] = artifact_digest(b"forged")
            db.execute("UPDATE control_events SET event=? WHERE kind='G08' AND object_id='EV-001' AND version=1",
                       (json.dumps(event),))
        called = []
        with self.assertRaises(IntegrityFailure):
            self.gate.enter_resolution_pending(self.obligation(), "resolver", lambda: called.append(True))
        self.assertEqual(called, [])

    def test_g07_resolution_actor_cannot_verify_own_obligation(self):
        self.register_evidence()
        self.verify_evidence()
        called = []
        with self.assertRaisesRegex(ControlBoundaryError, "cannot verify own obligation"):
            self.gate.verify_resolution(self.obligation(), "resolver", "resolver", lambda: called.append(True))
        self.assertEqual(called, [])

    def test_g07_independent_verification_uses_recovered_verified_evidence(self):
        self.register_evidence()
        self.verify_evidence()
        reopened = EvidenceResolutionGate(
            CertificationEvidence(CrashRecoveryBoundary(SQLiteControlBoundary(self.path)), self.authorized)
        )
        self.assertEqual(reopened.verify_resolution(self.obligation(), "resolver", "independent",
                                                     lambda: "verified"), "verified")

    def test_evidence_gated_g07_transition_commits_and_recovers_with_audit(self):
        self.create_record()
        self.register_evidence()
        self.verify_evidence()
        result = self.gate.enter_resolution_pending(
            self.obligation(), "resolver",
            lambda: self.recovery.transition("G07", "OB-001", "OPEN", "RESOLUTION_PENDING",
                                             "resolver", "AUTH-TEST", {"evidence": "EV-001"},
                                             "g07-pending"),
        )
        recovered = CrashRecoveryBoundary(SQLiteControlBoundary(self.path)).recover("G07", "OB-001")
        self.assertEqual(result["state"], "RESOLUTION_PENDING")
        self.assertEqual(recovered["state"], "RESOLUTION_PENDING")
        self.assertEqual(self.recovery.history("G07", "OB-001")[-1]["actor"], "resolver")

    def test_independent_g07_verification_commits_and_recovers_with_audit(self):
        self.create_record()
        self.recovery.transition("G07", "OB-001", "OPEN", "RESOLUTION_PENDING", "resolver",
                                 "AUTH-TEST", {"resolution": "ready"}, "g07-pending")
        self.register_evidence()
        self.verify_evidence()
        result = self.gate.verify_resolution(
            self.obligation(), "resolver", "independent",
            lambda: self.recovery.transition("G07", "OB-001", "RESOLUTION_PENDING", "VERIFIED",
                                             "independent", "AUTH-TEST", {"check": "passed"},
                                             "g07-verify"),
        )
        recovered = CrashRecoveryBoundary(SQLiteControlBoundary(self.path)).recover("G07", "OB-001")
        self.assertEqual(result["state"], "VERIFIED")
        self.assertEqual(recovered["state"], "VERIFIED")
        self.assertEqual(self.recovery.history("G07", "OB-001")[-1]["actor"], "independent")


if __name__ == "__main__":
    unittest.main()
