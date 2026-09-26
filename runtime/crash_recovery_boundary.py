"""Crash-recovery adapter over the shared Foundry persistence/audit port.

The adapter adds restart reconstruction checks without creating a second
storage, history, audit, or idempotency model.
"""

from __future__ import annotations

from typing import Callable

from runtime.control_boundary import ControlBoundaryPort


class CrashRecoveryBoundary:
    """Verify committed snapshots by rebuilding them from the shared event log."""

    def __init__(self, boundary: ControlBoundaryPort):
        self.boundary = boundary

    def create(self, kind: str, object_id: str, document: dict, request_key: str) -> dict:
        self.boundary.create(kind, object_id, document, request_key)
        return self.recover(kind, object_id)

    def transition(self, kind: str, object_id: str, expected_state: str, new_state: str,
                   actor: str, authority_ref: str, evidence: dict | None = None,
                   request_key: str | None = None, *, extra: dict | None = None) -> dict:
        self.boundary.transition(kind, object_id, expected_state, new_state, actor,
                                 authority_ref, evidence, request_key, extra=extra)
        return self.recover(kind, object_id)

    def execute_migration(self, object_id: str, actor: str, authority_ref: str,
                          request_key: str, operation: Callable, verify: Callable) -> dict:
        self.boundary.execute_migration(object_id, actor, authority_ref, request_key,
                                        operation, verify)
        return self.recover("G06", object_id)

    def get(self, kind: str, object_id: str) -> dict:
        return self.recover(kind, object_id)

    def history(self, kind: str, object_id: str) -> list[dict]:
        return self.boundary.history(kind, object_id)

    def reconstruct(self, kind: str, object_id: str) -> dict:
        return self.boundary.reconstruct(kind, object_id)

    def recover(self, kind: str, object_id: str) -> dict:
        """Reconstruct the durable state and verify its audit and state hashes."""
        return self.boundary.reconstruct(kind, object_id)
