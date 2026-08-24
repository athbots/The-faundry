import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from dec_core.core import DecisionCore,GovernanceSignal,DecisionDenied

def s(r,v): return GovernanceSignal(r,v,r+" rationale")
def denied(f):
    try:f()
    except DecisionDenied:return True
    return False

def main():
    c=DecisionCore()
    p=c.create_proposal(inq_ids=("INQ-1",),resolution_ids=("RES-1",),
      resolution_digests=("D1",),work_product_ids=("WP-1",),
      question="Choose path",options=("A","B"),tradeoffs="cost/reliability",
      risks="operational",reversibility="reversible",
      requested_authority="EXECUTIVE_AUTHORITY",residual_uncertainty="minor")
    assert c.decide(p.proposal_id,(s("CEO","NO"),s("CFO","YES"),s("TEAM","YES")),
                    "CEO veto","EXECUTIVE_AUTHORITY").outcome=="NO"
    assert c.decide(p.proposal_id,(s("CEO","YES"),s("CFO","NO"),s("TEAM","NO")),
                    "joint rejection","EXECUTIVE_AUTHORITY").outcome=="NO"
    assert c.decide(p.proposal_id,(s("CEO","YES"),s("CFO","YES"),s("TEAM","YES")),
                    "consensus","EXECUTIVE_AUTHORITY").outcome=="YES"
    assert denied(lambda:c.decide(p.proposal_id,(s("CEO","YES"),s("CFO","YES")),
                    "missing","EXECUTIVE_AUTHORITY"))
    assert denied(lambda:c.decide(p.proposal_id,(s("CEO","YES"),s("CFO","ABSTAIN"),s("TEAM","YES")),
                    "abstain","EXECUTIVE_AUTHORITY"))
    assert denied(lambda:c.decide(p.proposal_id,(s("CEO","MAYBE"),s("CFO","YES"),s("TEAM","YES")),
                    "invalid","EXECUTIVE_AUTHORITY"))
    assert denied(lambda:c.create_proposal(inq_ids=("I",),resolution_ids=(),
                    resolution_digests=(),work_product_ids=("W",),question="x",
                    options=("A","B"),tradeoffs="x",risks="x",reversibility="x",
                    requested_authority="X",residual_uncertainty="x"))
    assert denied(lambda:c.create_proposal(inq_ids=("I",),resolution_ids=("R1","R2"),
                    resolution_digests=("D1",),work_product_ids=("W",),question="x",
                    options=("A","B"),tradeoffs="x",risks="x",reversibility="x",
                    requested_authority="X",residual_uncertainty="x"))
    assert denied(lambda:c.decide("UNKNOWN",(s("CEO","YES"),s("CFO","YES"),s("TEAM","YES")),
                    "x","X"))
    assert denied(lambda:c.decide(p.proposal_id,(s("CEO","ABSTAIN"),s("CFO","YES"),s("TEAM","YES")),
                    "CEO abstains","X"))
    print("PASS | DEC boundary and governance")
    print("SUMMARY | 10/10 DEC invariants PASS")
    print("NOTE | Exact CFO/TEAM numerical weights remain unratified.")

if __name__=="__main__":main()
