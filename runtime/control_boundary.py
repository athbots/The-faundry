"""Durable reference boundary for governed change and migration records.

The API is intentionally small so a later adapter can bind it to the Foundry's
G-09 persistence and G-02 audit services. This SQLite implementation is a
reference backend, not a production storage or distributed-consistency claim.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Protocol


class ControlBoundaryError(Exception):
    pass


class IdempotencyConflict(ControlBoundaryError):
    pass


class IntegrityFailure(ControlBoundaryError):
    pass


class ControlBoundaryPort(Protocol):
    """Adapter contract for a shared durable store plus audit transaction."""

    def create(self, kind: str, object_id: str, document: dict, request_key: str) -> dict: ...
    def transition(self, kind: str, object_id: str, expected_state: str, new_state: str,
                   actor: str, authority_ref: str, evidence: dict | None = None,
                   request_key: str | None = None, *, extra: dict | None = None) -> dict: ...
    def execute_migration(self, object_id: str, actor: str, authority_ref: str, request_key: str,
                          operation: Callable, verify: Callable) -> dict: ...
    def get(self, kind: str, object_id: str) -> dict: ...
    def history(self, kind: str, object_id: str) -> list[dict]: ...


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(value: Any) -> str:
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


class SQLiteControlBoundary:
    """One transaction boundary for aggregate state, immutable history and audit."""

    def __init__(self, database: str | Path):
        self.database = str(database)
        with self._session() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS control_aggregates (
                    kind TEXT NOT NULL, object_id TEXT NOT NULL, version INTEGER NOT NULL,
                    document TEXT NOT NULL, PRIMARY KEY(kind, object_id)
                );
                CREATE TABLE IF NOT EXISTS control_events (
                    kind TEXT NOT NULL, object_id TEXT NOT NULL, version INTEGER NOT NULL,
                    event TEXT NOT NULL, previous_hash TEXT NOT NULL, event_hash TEXT NOT NULL,
                    PRIMARY KEY(kind, object_id, version)
                );
                CREATE TABLE IF NOT EXISTS control_idempotency (
                    kind TEXT NOT NULL, object_id TEXT NOT NULL, request_key TEXT NOT NULL,
                    fingerprint TEXT NOT NULL, PRIMARY KEY(kind, object_id, request_key)
                );
                """
            )

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.database, timeout=10, isolation_level=None)
        db.row_factory = sqlite3.Row
        return db

    @contextmanager
    def _session(self):
        db = self._connect()
        try:
            yield db
        finally:
            db.close()

    def create(self, kind: str, object_id: str, document: dict, request_key: str) -> dict:
        fingerprint = _digest({"operation": "create", "document": document})
        with self._session() as db:
            db.execute("BEGIN IMMEDIATE")
            found = db.execute(
                "SELECT document FROM control_aggregates WHERE kind=? AND object_id=?",
                (kind, object_id),
            ).fetchone()
            if found:
                existing = json.loads(found["document"])
                prior = db.execute(
                    "SELECT fingerprint FROM control_idempotency WHERE kind=? AND object_id=? AND request_key=?",
                    (kind, object_id, request_key),
                ).fetchone()
                db.rollback()
                if prior and prior["fingerprint"] == fingerprint:
                    return existing
                raise IdempotencyConflict("identity already exists with different provenance")
            event = {
                "kind": kind, "object_id": object_id, "version": 0,
                "from": None, "to": document["state"], "actor": document["proposer"],
                "authority_ref": document["provenance"]["authority_ref"],
                "scope_digest": _digest(document["scope"]),
                "provenance_digest": _digest(document["provenance"]), "event": "CREATED",
                "audit_ref": f"AUDIT:{kind}:{object_id}:0",
            }
            db.execute("INSERT INTO control_aggregates VALUES(?,?,0,?)", (kind, object_id, _json(document)))
            self._append_event(db, kind, object_id, 0, event)
            db.execute(
                "INSERT INTO control_idempotency VALUES(?,?,?,?)",
                (kind, object_id, request_key, fingerprint),
            )
            db.commit()
            return document

    def transition(
        self, kind: str, object_id: str, expected_state: str, new_state: str,
        actor: str, authority_ref: str, evidence: dict | None = None,
        request_key: str | None = None, *, extra: dict | None = None,
    ) -> dict:
        operation = {"from": expected_state, "to": new_state, "actor": actor,
                     "authority_ref": authority_ref, "evidence": evidence or {}, "extra": extra or {}}
        fingerprint = _digest(operation)
        with self._session() as db:
            db.execute("BEGIN IMMEDIATE")
            if request_key:
                prior = db.execute(
                    "SELECT fingerprint FROM control_idempotency WHERE kind=? AND object_id=? AND request_key=?",
                    (kind, object_id, request_key),
                ).fetchone()
                if prior:
                    row = self._load_row(db, kind, object_id)
                    db.rollback()
                    if prior["fingerprint"] == fingerprint:
                        return json.loads(row["document"])
                    raise IdempotencyConflict("request key reused for a different operation")
            row = self._load_row(db, kind, object_id)
            document = json.loads(row["document"])
            if document["state"] != expected_state:
                db.rollback()
                raise ControlBoundaryError(f"expected {expected_state}, found {document['state']}")
            if (_digest(document["scope"]) != document["scope_digest"] or
                    _digest(document["provenance"]) != document["provenance_digest"] or
                    document.get("identity") != object_id):
                db.rollback()
                raise IntegrityFailure("immutable identity, scope, or provenance digest mismatch")
            document["state"] = new_state
            document["version"] = row["version"] + 1
            document.setdefault("evidence", []).append(evidence or {})
            for field in ("implementer", "authorization_ref", "verifier"):
                if field in (extra or {}):
                    document[field] = (extra or {})[field]
            event = {
                "kind": kind, "object_id": object_id, "version": document["version"],
                "from": expected_state, "to": new_state, "actor": actor,
                "authority_ref": authority_ref, "scope_digest": document["scope_digest"],
                "evidence": evidence or {}, "details": extra or {},
                "audit_ref": f"AUDIT:{kind}:{object_id}:{document['version']}:{request_key or 'transition'}",
            }
            db.execute("UPDATE control_aggregates SET version=?,document=? WHERE kind=? AND object_id=?",
                       (document["version"], _json(document), kind, object_id))
            self._append_event(db, kind, object_id, document["version"], event)
            if request_key:
                db.execute("INSERT INTO control_idempotency VALUES(?,?,?,?)",
                           (kind, object_id, request_key, fingerprint))
            db.commit()
            return document

    def execute_migration(
        self, object_id: str, actor: str, authority_ref: str, request_key: str,
        operation: Callable[[sqlite3.Connection], Any],
        verify: Callable[[sqlite3.Connection, Any], dict],
    ) -> dict:
        kind = "G06"
        fingerprint = _digest({"operation": "execute", "actor": actor, "authority_ref": authority_ref})
        db = self._connect()
        attempted: list[str] = []
        try:
            db.execute("BEGIN IMMEDIATE")
            prior = db.execute(
                "SELECT fingerprint FROM control_idempotency WHERE kind=? AND object_id=? AND request_key=?",
                (kind, object_id, request_key),
            ).fetchone()
            row = self._load_row(db, kind, object_id)
            document = json.loads(row["document"])
            if prior:
                if prior["fingerprint"] != fingerprint:
                    raise IdempotencyConflict("migration request key reused")
                db.rollback()
                return document
            if document["state"] != "AUTHORIZED":
                raise ControlBoundaryError("migration must be authorized before execution")
            if (_digest(document["scope"]) != document["scope_digest"] or
                    _digest(document["provenance"]) != document["provenance_digest"] or
                    document.get("identity") != object_id):
                raise IntegrityFailure("immutable migration scope digest mismatch")
            transitions = ["EXECUTING"]
            for state in transitions:
                attempted.append(state)
                version = document["version"] + 1
                self._record_migration_step(db, document, state, version, actor, authority_ref,
                                            {"audit_ref": f"AUDIT:G06:{object_id}:{version}"})
            result = operation(db)
            state = "POST_VERIFYING"
            attempted.append(state)
            version = document["version"] + 1
            self._record_migration_step(db, document, state, version, actor, authority_ref,
                                        {"audit_ref": f"AUDIT:G06:{object_id}:{version}"})
            verification = verify(db, result)
            if not isinstance(verification, dict) or not verification.get("passed"):
                raise IntegrityFailure("post-migration integrity verification failed")
            if not verification.get("verifier") or verification["verifier"] == actor:
                raise IntegrityFailure("migration verification must be performed by an independent verifier")
            if not verification.get("authority_ref"):
                raise IntegrityFailure("migration verification authority reference is required")
            document.setdefault("evidence", []).append({"verification": verification})
            state = "COMPLETED"
            version = document["version"] + 1
            self._record_migration_step(db, document, state, version, actor, authority_ref,
                                        {"verification": verification,
                                         "audit_ref": f"AUDIT:G06:{object_id}:{version}"})
            db.execute("INSERT INTO control_idempotency VALUES(?,?,?,?)",
                       (kind, object_id, request_key, fingerprint))
            db.commit()
            return document
        except Exception as exc:
            db.rollback()
            try:
                self.transition(kind, object_id, "AUTHORIZED", "MIGRATION_FAILED", actor,
                                authority_ref, {"error": type(exc).__name__, "message": str(exc),
                                                "attempted_states": attempted},
                                request_key=f"{request_key}:failure")
            except ControlBoundaryError:
                pass
            raise
        finally:
            db.close()

    def _record_migration_step(self, db, document, state, version, actor, authority_ref, details):
        prior_state = document["state"]
        document["state"] = state
        document["version"] = version
        event = {"kind": "G06", "object_id": document["identity"], "version": version,
                 "from": prior_state, "to": state, "actor": actor,
                 "authority_ref": authority_ref, "scope_digest": document["scope_digest"],
                 "details": details, "audit_ref": details["audit_ref"]}
        db.execute("UPDATE control_aggregates SET version=?,document=? WHERE kind='G06' AND object_id=?",
                   (version, _json(document), document["identity"]))
        self._append_event(db, "G06", document["identity"], version, event)

    def _append_event(self, db, kind, object_id, version, event):
        previous = db.execute(
            "SELECT event_hash FROM control_events WHERE kind=? AND object_id=? ORDER BY version DESC LIMIT 1",
            (kind, object_id),
        ).fetchone()
        previous_hash = previous["event_hash"] if previous else "0" * 64
        event_hash = hashlib.sha256((previous_hash + _json(event)).encode("utf-8")).hexdigest()
        db.execute("INSERT INTO control_events VALUES(?,?,?,?,?,?)",
                   (kind, object_id, version, _json(event), previous_hash, event_hash))

    @staticmethod
    def _load_row(db, kind, object_id):
        row = db.execute("SELECT version,document FROM control_aggregates WHERE kind=? AND object_id=?",
                         (kind, object_id)).fetchone()
        if not row:
            raise ControlBoundaryError("unknown control record")
        return row

    def get(self, kind: str, object_id: str) -> dict:
        with self._session() as db:
            row = self._load_row(db, kind, object_id)
            return json.loads(row["document"])

    def history(self, kind: str, object_id: str) -> list[dict]:
        with self._session() as db:
            rows = db.execute(
                "SELECT version,event,previous_hash,event_hash FROM control_events "
                "WHERE kind=? AND object_id=? ORDER BY version", (kind, object_id),
            ).fetchall()
        previous = "0" * 64
        result = []
        for row in rows:
            event = json.loads(row["event"])
            expected = hashlib.sha256((previous + _json(event)).encode("utf-8")).hexdigest()
            if row["previous_hash"] != previous or row["event_hash"] != expected:
                raise IntegrityFailure("control history hash chain failed")
            previous = row["event_hash"]
            result.append(event)
        return result

    def reconstruct(self, kind: str, object_id: str) -> dict:
        """Verify append-only events reconstruct the stored terminal snapshot."""
        events = self.history(kind, object_id)
        document = self.get(kind, object_id)
        if not events or events[0].get("version") != 0 or events[0].get("from") is not None:
            raise IntegrityFailure("control history has no valid creation event")
        state = events[0].get("to")
        for expected_version, event in enumerate(events[1:], start=1):
            if (event.get("version") != expected_version or event.get("from") != state or
                    not event.get("audit_ref")):
                raise IntegrityFailure("control event sequence cannot reconstruct state")
            state = event.get("to")
        if document.get("version") != len(events) - 1 or document.get("state") != state:
            raise IntegrityFailure("stored snapshot does not match reconstructed history")
        return document

class ChangeControl:
    KIND = "G05"
    TRANSITIONS = {
        "PROPOSED": {"IMPACT_ASSESSED", "REJECTED"},
        "IMPACT_ASSESSED": {"AUTHORIZED", "REJECTED"},
        "AUTHORIZED": {"IMPLEMENTING", "FAILED"},
        "IMPLEMENTING": {"VERIFICATION_PENDING", "FAILED", "COMPENSATION_REQUIRED"},
        "VERIFICATION_PENDING": {"VERIFIED", "FAILED", "COMPENSATION_REQUIRED"},
        "VERIFIED": {"RELEASED"},
        "FAILED": {"COMPENSATION_REQUIRED"},
        "COMPENSATION_REQUIRED": {"COMPENSATED", "COMPENSATION_FAILED"},
        "REJECTED": set(), "RELEASED": set(), "COMPENSATED": set(), "COMPENSATION_FAILED": set(),
    }

    def __init__(self, boundary: ControlBoundaryPort, authorize: Callable[[str, str, str], bool]):
        self.boundary, self.authorize = boundary, authorize

    def propose(self, identity, scope, proposer, authority_ref, provenance, request_key):
        if not identity or not scope or not proposer or not authority_ref or not provenance:
            raise ControlBoundaryError("change identity, explicit scope and provenance are required")
        prov = {**provenance, "authority_ref": authority_ref}
        document = {"identity": identity, "scope": scope, "scope_digest": _digest(scope),
                    "proposer": proposer, "provenance": prov, "provenance_digest": _digest(prov),
                    "state": "PROPOSED", "version": 0, "evidence": [], "implementer": None,
                    "verifier": None}
        return self.boundary.create(self.KIND, identity, document, request_key)

    def transition(self, identity, target, actor, authority_ref, request_key, evidence=None, **details):
        current = self.boundary.get(self.KIND, identity)
        if target not in self.TRANSITIONS.get(current["state"], set()):
            raise ControlBoundaryError(f"transition {current['state']} -> {target} is prohibited")
        if target == "REJECTED" and not (evidence or {}).get("reason"):
            raise ControlBoundaryError("rejection requires a recorded rationale")
        if target == "FAILED" and not ((evidence or {}).get("failure") or (evidence or {}).get("reason")):
            raise ControlBoundaryError("failed change requires failure evidence")
        if target == "VERIFIED" and actor == current.get("implementer"):
            raise ControlBoundaryError("implementer cannot independently verify own change")
        if target in {"IMPACT_ASSESSED", "AUTHORIZED", "IMPLEMENTING", "REJECTED", "VERIFIED",
                      "RELEASED", "COMPENSATED", "COMPENSATION_FAILED"} and not self.authorize(actor, authority_ref, target):
            raise ControlBoundaryError("required authority was not established")
        if target == "IMPLEMENTING":
            return self._transition_with_document(current, target, actor, authority_ref, request_key,
                                                  evidence, {**details, "implementer": actor})
        if target == "VERIFIED":
            if not evidence or not evidence.get("evidence_digest"):
                raise ControlBoundaryError("verification requires evidence digest")
        if target == "RELEASED" and current["state"] != "VERIFIED":
            raise ControlBoundaryError("unverified change cannot be released")
        if target in {"COMPENSATED", "COMPENSATION_FAILED"} and current["state"] != "COMPENSATION_REQUIRED":
            raise ControlBoundaryError("compensation outcome requires COMPENSATION_REQUIRED")
        if target == "COMPENSATED" and not (evidence or {}).get("compensation_ref"):
            raise ControlBoundaryError("compensation requires a distinct compensation record")
        if target == "COMPENSATION_FAILED" and not (evidence or {}).get("failure"):
            raise ControlBoundaryError("failed compensation requires failure evidence")
        if target == "AUTHORIZED":
            details = {**details, "authorization_ref": authority_ref}
        if target == "VERIFIED":
            details = {**details, "verifier": actor}
        return self._transition_with_document(current, target, actor, authority_ref, request_key,
                                              evidence, details)

    def _transition_with_document(self, current, target, actor, authority_ref, request_key, evidence, details):
        result = self.boundary.transition(self.KIND, current["identity"], current["state"], target,
                                          actor, authority_ref, evidence, request_key, extra=details)
        return result


class MigrationControl:
    KIND = "G06"
    TRANSITIONS = {
        "PREPARED": {"VALIDATING", "MIGRATION_FAILED"},
        "VALIDATING": {"AUTHORIZED", "MIGRATION_FAILED"},
        "AUTHORIZED": {"EXECUTING", "MIGRATION_FAILED"},
        "EXECUTING": {"POST_VERIFYING", "MIGRATION_FAILED"},
        "POST_VERIFYING": {"COMPLETED", "MIGRATION_FAILED"},
        "MIGRATION_FAILED": {"ROLLBACK_REQUIRED"},
        "ROLLBACK_REQUIRED": {"ROLLED_BACK"},
        "COMPLETED": set(), "ROLLED_BACK": set(),
    }

    def __init__(self, boundary: ControlBoundaryPort, authorize: Callable[[str, str, str], bool]):
        self.boundary, self.authorize = boundary, authorize

    def prepare(self, identity, scope, proposer, authority_ref, provenance, reversible, request_key):
        if not identity or not scope or not proposer or not authority_ref or not provenance:
            raise ControlBoundaryError("migration identity, explicit scope and provenance are required")
        prov = {**provenance, "authority_ref": authority_ref}
        document = {"identity": identity, "scope": scope, "scope_digest": _digest(scope),
                    "proposer": proposer, "provenance": prov, "provenance_digest": _digest(prov),
                    "state": "PREPARED", "version": 0, "evidence": [], "reversible": bool(reversible)}
        return self.boundary.create(self.KIND, identity, document, request_key)

    def transition(self, identity, target, actor, authority_ref, request_key, evidence=None, **details):
        current = self.boundary.get(self.KIND, identity)
        if target not in self.TRANSITIONS.get(current["state"], set()):
            raise ControlBoundaryError(f"transition {current['state']} -> {target} is prohibited")
        if target in {"EXECUTING", "POST_VERIFYING", "COMPLETED"}:
            raise ControlBoundaryError("execution and completion phases are recorded only by execute()")
        if target == "MIGRATION_FAILED" and not ((evidence or {}).get("failure") or
                                                    (evidence or {}).get("error")):
            raise ControlBoundaryError("migration failure requires durable failure evidence")
        if target == "ROLLBACK_REQUIRED" and not ((evidence or {}).get("reason") or
                                                   (evidence or {}).get("failure")):
            raise ControlBoundaryError("rollback request requires a recorded reason")
        if target in {"AUTHORIZED", "ROLLED_BACK"} and not self.authorize(actor, authority_ref, target):
            raise ControlBoundaryError("required authority was not established")
        if target == "ROLLED_BACK":
            if not current["reversible"]:
                raise ControlBoundaryError("non-reversible migration cannot claim rollback")
            if not evidence or not evidence.get("compensation_ref"):
                raise ControlBoundaryError("rollback requires compensation evidence")
        return self.boundary.transition(self.KIND, identity, current["state"], target, actor,
                                        authority_ref, evidence, request_key, extra=details)

    def execute(self, identity, actor, authority_ref, request_key, operation, verify):
        current = self.boundary.get(self.KIND, identity)
        if current["state"] == "COMPLETED":
            return self.boundary.execute_migration(identity, actor, authority_ref, request_key, operation,
                                                   lambda _db, _result: {})
        if current["state"] != "AUTHORIZED":
            raise ControlBoundaryError("migration must be authorized before execution")
        if not self.authorize(actor, authority_ref, "EXECUTING"):
            raise ControlBoundaryError("required migration execution authority was not established")
        def independently_verify(db, result):
            evidence = verify(db, result)
            if not isinstance(evidence, dict):
                raise IntegrityFailure("post-migration verification evidence must be a record")
            verifier = evidence.get("verifier")
            verification_authority = evidence.get("authority_ref")
            if (not verifier or verifier == actor or not verification_authority or
                    not self.authorize(verifier, verification_authority, "MIGRATION_VERIFIED")):
                raise IntegrityFailure("migration verification requires independent authorized verifier")
            return evidence
        return self.boundary.execute_migration(identity, actor, authority_ref, request_key, operation,
                                               independently_verify)

    def require_preconditions(self, identity, actor, authority_ref, request_key, check):
        self.transition(identity, "VALIDATING", actor, authority_ref, request_key)
        try:
            passed = bool(check())
        except Exception as exc:
            self.transition(identity, "MIGRATION_FAILED", actor, authority_ref,
                            f"{request_key}:precondition-error",
                            {"failure": "PRECONDITION_ERROR", "error": type(exc).__name__,
                             "message": str(exc)})
            raise ControlBoundaryError("migration precondition evaluation failed") from exc
        if not passed:
            self.transition(identity, "MIGRATION_FAILED", actor, authority_ref,
                            f"{request_key}:precondition-failed", {"failure": "PRECONDITION_FAILED"})
            raise ControlBoundaryError("migration precondition failed")
        return self.transition(identity, "AUTHORIZED", actor, authority_ref,
                               f"{request_key}:authorize", {"preconditions": "passed"})
