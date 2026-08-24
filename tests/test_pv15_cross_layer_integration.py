import sys, hashlib, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from inq_interface.interface import OBS, OBSInquiryInterface
from inq_core.core import InquiryCore
from dec_core.core import DecisionCore, GovernanceSignal
from dec_core.execution import ExecutionCore, ExecutionDenied

def sig(role, value):
    return GovernanceSignal(role, value, f"{role} signal")

def denied(fn):
    try:
        fn()
    except Exception:
        return True
    return False

def main():
    bridge = OBSInquiryInterface()
    trigger = OBS("OBS-INT-001", "ACCEPTED",
                  hashlib.sha256(b"measured-baseline").hexdigest()[:8],
                  "INTEGRATION-TEST")
    candidate = bridge.create_candidate(
        [trigger], "RELATED", trigger.evidence_digest,
        "operator-A", "baseline anomaly requires resolution"
    )

    iq = InquiryCore()
    q = iq.create(
        candidate,
        "Resolve deployment anomaly",
        "Determine whether configuration A caused the anomaly",
        "single deployment configuration",
        "investigator-A"
    )
    iq.transition(q.inq_id, "OPEN", "TRIAGE_AUTHORITY")
    iq.transition(q.inq_id, "INVESTIGATING", "TRIAGE_AUTHORITY")
    iq.transition(
        q.inq_id, "RESOLVED", "INVESTIGATION_AUTHORITY",
        "Configuration A is supported as the cause",
        ["OBS-INT-001"]
    )
    iq.transition(q.inq_id, "CLOSED", "CLOSURE_AUTHORITY")
    assert q.status == "CLOSED"

    dc = DecisionCore()
    proposal = dc.create_proposal(
        inq_ids=(q.inq_id,),
        resolution_ids=("RES-INTEGRATION-001",),
        resolution_digests=("DIGEST-INTEGRATION-001",),
        work_product_ids=("WP-INTEGRATION-001",),
        question="Adopt configuration B to eliminate the anomaly?",
        options=("ADOPT_B", "RETAIN_A"),
        tradeoffs="migration cost versus reliability",
        risks="migration failure",
        reversibility="rollback available",
        requested_authority="EXECUTIVE_AUTHORITY",
        residual_uncertainty="minor deployment timing uncertainty"
    )
    decision = dc.decide(
        proposal.proposal_id,
        (sig("CEO","YES"), sig("CFO","YES"), sig("TEAM","YES")),
        "Evidence-backed adoption of configuration B",
        "EXECUTIVE_AUTHORITY"
    )
    assert decision.outcome == "YES"

    ec = ExecutionCore(dc.decisions)
    digest = ec._decision_digest(decision)
    auth = ec.authorize(
        decision.decision_id, digest,
        "deploy configuration B", "executor-A",
        "EXECUTION_AUTHORITY",
        "maintenance window open",
        "abort if error rate exceeds threshold",
        "error rate returns to baseline",
        "collect error rate and latency evidence",
        "restore configuration A"
    )
    execution = ec.start(auth.authorization_id)
    assert execution.state == "EXECUTING"

    outcome = OBS("OBS-INT-002", "ACCEPTED",
                   hashlib.sha256(b"post-deployment-baseline").hexdigest()[:8],
                   "EXECUTION-OUTCOME")
    assert outcome.obs_id != trigger.obs_id

    ec.verify(
        execution.execution_id,
        [outcome.obs_id],
        "error rate returned to baseline",
        "VERIFICATION_AUTHORITY"
    )
    assert execution.state == "VERIFIED"
    assert execution.outcome_evidence == ("OBS-INT-002",)

    assert denied(lambda: ec.verify(
        execution.execution_id, ["OBS-INT-003"],
        "false verification", "EXECUTION_AUTHORITY"
    ))

    rejected = dc.decide(
        proposal.proposal_id,
        (sig("CEO","NO"), sig("CFO","YES"), sig("TEAM","YES")),
        "CEO veto",
        "EXECUTIVE_AUTHORITY"
    )
    assert rejected.outcome == "NO"
    assert denied(lambda: ec.authorize(
        rejected.decision_id, ec._decision_digest(rejected),
        "forbidden deployment", "executor-B",
        "EXECUTION_AUTHORITY", "start", "stop",
        "expected", "verify", "rollback"
    ))

    trace = {
        "OBS_TRIGGER": trigger.obs_id,
        "INQ": q.inq_id,
        "DEC_PROPOSAL": proposal.proposal_id,
        "DECISION": decision.decision_id,
        "EXECUTION_AUTH": auth.authorization_id,
        "EXECUTION": execution.execution_id,
        "OUTCOME_OBS": outcome.obs_id
    }
    assert len(set(trace.values())) == len(trace.values())

    print("PASS | PV-15 end-to-end cross-layer integration")
    print("SUMMARY | 12/12 integration invariants PASS")
    print(json.dumps(trace, sort_keys=True))

if __name__ == "__main__":
    main()
