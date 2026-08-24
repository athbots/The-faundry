import sys, hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from dec_core.core import DecisionCore, GovernanceSignal
from dec_core.execution import ExecutionCore, ExecutionDenied

def s(r,v): return GovernanceSignal(r,v,r)

def denied(fn):
    try: fn()
    except ExecutionDenied: return True
    return False

def make_dec(core,outcome="YES"):
    p=core.create_proposal(
        inq_ids=("INQ-1",),resolution_ids=("RES-1",),
        resolution_digests=("RD1",),work_product_ids=("WP-1",),
        question="Choose execution",options=("A","B"),tradeoffs="cost/risk",
        risks="operational",reversibility="rollback",
        requested_authority="EXECUTIVE_AUTHORITY",residual_uncertainty="minor")
    if outcome=="YES":
        return core.decide(p.proposal_id,(s("CEO","YES"),s("CFO","YES"),s("TEAM","YES")),
                            "approved","EXECUTIVE_AUTHORITY")
    return core.decide(p.proposal_id,(s("CEO","NO"),s("CFO","YES"),s("TEAM","YES")),
                       "rejected","EXECUTIVE_AUTHORITY")

def main():
    dc=DecisionCore()
    yes=make_dec(dc,"YES")
    no=make_dec(dc,"NO")
    ec=ExecutionCore(dc.decisions)

    dd=ec._decision_digest(yes)
    a=ec.authorize(yes.decision_id,dd,"deploy service","executor-A",
                   "EXECUTION_AUTHORITY","precondition met","abort on safety threshold",
                   "service available","collect health + business metrics","rollback to prior version")
    assert a.decision_id==yes.decision_id

    # 1 final YES is executable
    e=ec.start(a.authorization_id)
    assert e.state=="EXECUTING"

    # 2 NO decision cannot execute
    assert denied(lambda:ec.authorize(no.decision_id,ec._decision_digest(no),
        "scope","executor","EXECUTION_AUTHORITY","start","stop","expected","verify","rollback"))

    # 3 digest mismatch fails closed
    assert denied(lambda:ec.authorize(yes.decision_id,"bad","scope","executor",
        "EXECUTION_AUTHORITY","start","stop","expected","verify","rollback"))

    # 4 missing stop condition fails
    assert denied(lambda:ec.authorize(yes.decision_id,dd,"scope","executor",
        "EXECUTION_AUTHORITY","start","","expected","verify","rollback"))

    # 5 verification requires evidence + verification authority
    assert denied(lambda:ec.verify(e.execution_id,["OBS-OUT-1"],"worked","EXECUTION_AUTHORITY"))

    # 6 successful verification records outcome evidence
    ec.verify(e.execution_id,["OBS-OUT-1"],"expected outcome supported","VERIFICATION_AUTHORITY")
    assert e.state=="VERIFIED" and e.outcome_evidence==("OBS-OUT-1",)

    # 7 verified execution cannot be silently re-verified
    assert denied(lambda:ec.verify(e.execution_id,["OBS-OUT-2"],"changed","VERIFICATION_AUTHORITY"))

    # 8 abort path preserves trigger/evidence
    a2=ec.authorize(yes.decision_id,dd,"second scope","executor-B",
                    "EXECUTION_AUTHORITY","start condition","stop condition",
                    "expected","verify","rollback")
    e2=ec.start(a2.authorization_id)
    ec.abort(e2.execution_id,"safety threshold exceeded","OBS-FAIL-1","EXECUTION_AUTHORITY")
    assert e2.state=="ABORTED"
    assert e2.events[-1][0]=="ABORTED"

    # 9 aborted execution cannot verify as success
    assert denied(lambda:ec.verify(e2.execution_id,["OBS-FAIL-1"],"success","VERIFICATION_AUTHORITY"))

    # 10 authorization remains tied to original decision digest
    assert a.decision_digest==dd and a.decision_id==yes.decision_id

    print("PASS | DEC execution authorization and closed-loop verification")
    print("SUMMARY | 10/10 execution-loop invariants PASS")

if __name__=="__main__": main()
