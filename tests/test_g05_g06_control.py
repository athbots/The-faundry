import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from runtime.control_boundary import (
    ChangeControl, ControlBoundaryError, IdempotencyConflict, IntegrityFailure,
    MigrationControl, SQLiteControlBoundary,
)


class ChangeMigrationControlTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "control.sqlite"
        self.boundary = SQLiteControlBoundary(self.path)
        self.grants = {("approver", "AUTH-CHANGE", "AUTHORIZED"),
                       ("reviewer", "AUTH-VERIFY", "VERIFIED"),
                       ("release", "AUTH-RELEASE", "RELEASED"),
                       ("ops", "AUTH-OPS", "IMPACT_ASSESSED"),
                       ("approver", "AUTH-CHANGE", "REJECTED"),
                       ("rollback", "AUTH-ROLLBACK", "COMPENSATED"),
                       ("engineer", "AUTH-CHANGE", "IMPLEMENTING"),
                       ("migrator", "AUTH-MIGRATION", "AUTHORIZED"),
                       ("migrator", "AUTH-MIGRATION", "EXECUTING"),
                       ("reviewer", "AUTH-VERIFY", "MIGRATION_VERIFIED"),
                       ("rollback", "AUTH-ROLLBACK", "ROLLED_BACK")}
        self.changes = ChangeControl(self.boundary, self.allowed)
        self.migrations = MigrationControl(self.boundary, self.allowed)

    def tearDown(self):
        self.temp.cleanup()

    def allowed(self, actor, authority_ref, action):
        return (actor, authority_ref, action) in self.grants

    def change(self, identity="CHG-001"):
        self.changes.propose(identity, {"systems": ["runtime"], "files": ["runtime/x.py"]},
                             "author", "AUTH-PROPOSAL", {"source": "test", "digest": "sha256:abc"},
                             "create")
        self.changes.transition(identity, "IMPACT_ASSESSED", "ops", "AUTH-OPS", "assess",
                                {"impact": "reviewed"})
        self.changes.transition(identity, "AUTHORIZED", "approver", "AUTH-CHANGE", "authorize",
                                {"decision": "approved"})
        return identity

    def migration(self, identity="MIG-001", reversible=True):
        self.migrations.prepare(identity, {"database": "records", "schema": ["v1", "v2"]},
                                "planner", "AUTH-PREPARE", {"source": "test", "digest": "sha256:def"},
                                reversible, "prepare")
        self.migrations.require_preconditions(identity, "migrator", "AUTH-MIGRATION", "precheck",
                                              lambda: True)
        return identity

    def test_unauthorized_change(self):
        identity = self.change()
        with self.assertRaises(ControlBoundaryError):
            self.changes.transition(identity, "IMPLEMENTING", "unknown", "NONE", "start")
        self.assertEqual(self.boundary.get("G05", identity)["state"], "AUTHORIZED")

    def test_implementer_cannot_self_verify(self):
        identity = self.change()
        self.changes.transition(identity, "IMPLEMENTING", "engineer", "AUTH-CHANGE", "start")
        self.changes.transition(identity, "VERIFICATION_PENDING", "engineer", "AUTH-CHANGE", "pending")
        with self.assertRaisesRegex(ControlBoundaryError, "cannot independently verify"):
            self.changes.transition(identity, "VERIFIED", "engineer", "AUTH-VERIFY", "verify-self",
                                    {"evidence_digest": "sha256:123"})

    def test_unverified_change_cannot_be_released(self):
        identity = self.change()
        with self.assertRaises(ControlBoundaryError):
            self.changes.transition(identity, "RELEASED", "release", "AUTH-RELEASE", "release")

    def test_change_release_requires_and_follows_independent_verification(self):
        identity = self.change("CHG-RELEASE")
        self.changes.transition(identity, "IMPLEMENTING", "engineer", "AUTH-CHANGE", "start")
        self.changes.transition(identity, "VERIFICATION_PENDING", "engineer", "AUTH-CHANGE", "pending")
        self.changes.transition(identity, "VERIFIED", "reviewer", "AUTH-VERIFY", "verify",
                                {"evidence_digest": "sha256:verified"})
        result = self.changes.transition(identity, "RELEASED", "release", "AUTH-RELEASE", "release")
        self.assertEqual(result["state"], "RELEASED")
        self.assertEqual(result["verifier"], "reviewer")

    def test_failed_change_reconstructs_from_durable_history(self):
        identity = self.change()
        self.changes.transition(identity, "FAILED", "engineer", "AUTH-CHANGE", "failure",
                                {"failure": "BUILD_FAILED"})
        reopened = SQLiteControlBoundary(self.path)
        self.assertEqual(reopened.reconstruct("G05", identity)["state"], "FAILED")
        self.assertEqual([e["to"] for e in reopened.history("G05", identity)],
                         ["PROPOSED", "IMPACT_ASSESSED", "AUTHORIZED", "FAILED"])

    def test_scope_mutation_is_rejected(self):
        identity = self.change()
        db = sqlite3.connect(self.path)
        try:
            row = db.execute("SELECT document FROM control_aggregates WHERE kind='G05' AND object_id=?",
                             (identity,)).fetchone()
            document = json.loads(row[0])
            document["scope"]["files"].append("runtime/unauthorized.py")
            db.execute("UPDATE control_aggregates SET document=? WHERE kind='G05' AND object_id=?",
                       (json.dumps(document), identity))
            db.commit()
        finally:
            db.close()
        with self.assertRaises(IntegrityFailure):
            self.changes.transition(identity, "IMPLEMENTING", "engineer", "AUTH-CHANGE", "start")

    def test_provenance_mutation_is_rejected(self):
        identity = self.change("CHG-PROVENANCE")
        db = sqlite3.connect(self.path)
        try:
            row = db.execute("SELECT document FROM control_aggregates WHERE kind='G05' AND object_id=?",
                             (identity,)).fetchone()
            document = json.loads(row[0])
            document["provenance"]["digest"] = "sha256:changed"
            db.execute("UPDATE control_aggregates SET document=? WHERE kind='G05' AND object_id=?",
                       (json.dumps(document), identity))
            db.commit()
        finally:
            db.close()
        with self.assertRaises(IntegrityFailure):
            self.changes.transition(identity, "IMPLEMENTING", "engineer", "AUTH-CHANGE", "start")

    def test_rejection_and_compensation_are_explicit_states(self):
        self.changes.propose("CHG-REJECT", {"files": ["x"]}, "author", "AUTH-P",
                             {"digest": "sha256:x"}, "reject-create")
        self.changes.transition("CHG-REJECT", "REJECTED", "approver", "AUTH-CHANGE", "reject",
                                {"reason": "risk unacceptable"})
        self.assertEqual(self.boundary.get("G05", "CHG-REJECT")["state"], "REJECTED")
        identity = self.change("CHG-COMPENSATE")
        self.changes.transition(identity, "FAILED", "engineer", "AUTH-CHANGE", "failed",
                                {"failure": "partial implementation"})
        self.changes.transition(identity, "COMPENSATION_REQUIRED", "engineer", "AUTH-CHANGE",
                                "compensation-required", {"reason": "restore prior state"})
        self.changes.transition(identity, "COMPENSATED", "rollback", "AUTH-ROLLBACK", "compensated",
                                {"compensation_ref": "COMP-CHG-1"})
        self.assertEqual([event["to"] for event in self.boundary.history("G05", identity)][-3:],
                         ["FAILED", "COMPENSATION_REQUIRED", "COMPENSATED"])

    def test_duplicate_change_creation_is_idempotent(self):
        first = self.changes.propose("CHG-DUP", {"files": ["a"]}, "author", "AUTH-P", {"digest": "x"}, "same")
        second = self.changes.propose("CHG-DUP", {"files": ["a"]}, "author", "AUTH-P", {"digest": "x"}, "same")
        self.assertEqual(first, second)
        with self.assertRaises(IdempotencyConflict):
            self.changes.propose("CHG-DUP", {"files": ["b"]}, "author", "AUTH-P", {"digest": "x"}, "same")

    def test_unauthorized_migration_cannot_execute(self):
        identity = self.migrations.prepare("MIG-UNAUTH", {"database": "x"}, "planner", "AUTH-P",
                                           {"digest": "x"}, True, "prepare")
        called = []
        with self.assertRaises(ControlBoundaryError):
            self.migrations.execute(identity["identity"], "intruder", "NONE", "execute",
                                    lambda _db: called.append(True), lambda _db, _r: {
                                        "passed": True, "verifier": "reviewer", "authority_ref": "AUTH-VERIFY"})
        self.assertEqual(called, [])
        self.assertEqual(self.boundary.get("G06", "MIG-UNAUTH")["state"], "PREPARED")

    def test_migration_precondition_failure_is_visible(self):
        identity = self.migrations.prepare("MIG-PRE", {"database": "x"}, "planner", "AUTH-P",
                                           {"digest": "x"}, True, "prepare")["identity"]
        with self.assertRaisesRegex(ControlBoundaryError, "precondition failed"):
            self.migrations.require_preconditions(identity, "migrator", "AUTH-MIGRATION", "check",
                                                  lambda: False)
        self.assertEqual(self.boundary.get("G06", identity)["state"], "MIGRATION_FAILED")

    def test_post_migration_integrity_failure_rolls_back_and_is_visible(self):
        identity = self.migration("MIG-INTEGRITY")
        with self.assertRaises(IntegrityFailure):
            self.migrations.execute(identity, "migrator", "AUTH-MIGRATION", "execute",
                                    lambda db: db.execute("CREATE TABLE should_rollback (id INTEGER)"),
                                    lambda _db, _result: {"passed": False, "verifier": "reviewer",
                                                          "authority_ref": "AUTH-VERIFY"})
        self.assertEqual(self.boundary.get("G06", identity)["state"], "MIGRATION_FAILED")
        db = sqlite3.connect(self.path)
        try:
            exists = db.execute("SELECT name FROM sqlite_master WHERE name='should_rollback'").fetchone()
        finally:
            db.close()
        self.assertIsNone(exists)

    def test_rollback_preserves_failure_history_and_is_distinct(self):
        identity = self.migration("MIG-ROLLBACK")
        with self.assertRaises(IntegrityFailure):
            self.migrations.execute(identity, "migrator", "AUTH-MIGRATION", "execute",
                                    lambda _db: None, lambda _db, _r: {"passed": False, "verifier": "reviewer",
                                                                      "authority_ref": "AUTH-VERIFY"})
        self.migrations.transition(identity, "ROLLBACK_REQUIRED", "migrator", "AUTH-MIGRATION",
                                   "rollback-required", {"reason": "failed verification"})
        self.migrations.transition(identity, "ROLLED_BACK", "rollback", "AUTH-ROLLBACK", "rollback",
                                   {"compensation_ref": "COMP-001"})
        history = self.boundary.history("G06", identity)
        self.assertEqual([e["to"] for e in history][-3:],
                         ["MIGRATION_FAILED", "ROLLBACK_REQUIRED", "ROLLED_BACK"])
        self.assertNotEqual(history[-1]["to"], "COMPLETED")

    def test_non_reversible_migration_cannot_claim_rollback(self):
        identity = self.migration("MIG-IRREVERSIBLE", reversible=False)
        with self.assertRaises(IntegrityFailure):
            self.migrations.execute(identity, "migrator", "AUTH-MIGRATION", "execute",
                                    lambda _db: None, lambda _db, _r: {"passed": False, "verifier": "reviewer",
                                                                      "authority_ref": "AUTH-VERIFY"})
        self.migrations.transition(identity, "ROLLBACK_REQUIRED", "migrator", "AUTH-MIGRATION",
                                   "rollback-required", {"reason": "verification failed"})
        with self.assertRaisesRegex(ControlBoundaryError, "non-reversible"):
            self.migrations.transition(identity, "ROLLED_BACK", "rollback", "AUTH-ROLLBACK", "rollback",
                                       {"compensation_ref": "COMP-002"})

    def test_migration_idempotency_does_not_repeat_operation(self):
        identity = self.migration("MIG-IDEMPOTENT")
        calls = []
        operation = lambda db: (calls.append("ran"), db.execute("CREATE TABLE once_only (id INTEGER)"))[0]
        verify = lambda _db, _result: {"passed": True, "digest": "sha256:ok", "verifier": "reviewer",
                                      "authority_ref": "AUTH-VERIFY"}
        first = self.migrations.execute(identity, "migrator", "AUTH-MIGRATION", "execute", operation, verify)
        second = self.migrations.execute(identity, "migrator", "AUTH-MIGRATION", "execute",
                                         lambda _db: calls.append("duplicate"), verify)
        self.assertEqual(first["state"], "COMPLETED")
        self.assertEqual(second["state"], "COMPLETED")
        self.assertEqual(calls, ["ran"])

    def test_migration_state_and_audit_commit_atomically(self):
        identity = self.migration("MIG-ATOMIC")
        self.migrations.execute(identity, "migrator", "AUTH-MIGRATION", "execute",
                                lambda db: db.execute("CREATE TABLE atomic_result (value TEXT)"),
                                lambda db, _r: {"passed": db.execute(
                                    "SELECT count(*) FROM sqlite_master WHERE name='atomic_result'"
                                    ).fetchone()[0] == 1, "verifier": "reviewer",
                                        "authority_ref": "AUTH-VERIFY"})
        history = self.boundary.history("G06", identity)
        self.assertEqual([e["to"] for e in history][-3:], ["EXECUTING", "POST_VERIFYING", "COMPLETED"])
        self.assertTrue(all(e.get("audit_ref") for e in history))
        self.assertEqual(self.boundary.get("G06", identity)["state"], "COMPLETED")

    def test_migration_verification_is_independent(self):
        identity = self.migration("MIG-VERIFY")
        verification_actors = []
        self.migrations.execute(identity, "migrator", "AUTH-MIGRATION", "execute",
                                lambda _db: "result",
                                lambda _db, _result: (verification_actors.append("independent-verifier") or
                                                       {"passed": True, "verifier": "reviewer",
                                                        "authority_ref": "AUTH-VERIFY"}))
        self.assertNotEqual("migrator", verification_actors[0])
        last = self.boundary.history("G06", identity)[-1]
        self.assertEqual(last["to"], "COMPLETED")
        self.assertEqual(last["details"]["verification"]["verifier"], "reviewer")

    def test_migration_self_verification_fails_and_records_failure(self):
        identity = self.migration("MIG-SELF-VERIFY")
        with self.assertRaisesRegex(IntegrityFailure, "independent authorized verifier"):
            self.migrations.execute(identity, "migrator", "AUTH-MIGRATION", "execute",
                                    lambda _db: None,
                                    lambda _db, _result: {"passed": True, "verifier": "migrator",
                                                          "authority_ref": "AUTH-MIGRATION"})
        self.assertEqual(self.boundary.get("G06", identity)["state"], "MIGRATION_FAILED")

    def test_canonical_runtime_exposes_injected_controls(self):
        from runtime.canonical_runtime import CanonicalRuntime
        runtime = CanonicalRuntime(self.boundary, self.allowed)
        self.assertIsInstance(runtime.change_control, ChangeControl)
        self.assertIsInstance(runtime.migration_control, MigrationControl)


if __name__ == "__main__":
    unittest.main()
