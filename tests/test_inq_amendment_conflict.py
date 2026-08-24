import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from inq_interface.interface import OBS,OBSInquiryInterface
from inq_core.core import InquiryCore,INQDenied
from inq_core.amendment import AmendmentManager,AmendmentDenied
import hashlib

def setup():
    bridge=OBSInquiryInterface()
    o=OBS("O1","ACCEPTED",hashlib.sha256(b"O1").hexdigest()[:8],"P")
    c=bridge.create_candidate([o],"RELATED",o.evidence_digest,"operator","investigation")
    core=InquiryCore(); q=core.create(c,"Test","Resolve uncertainty","bounded","analyst")
    core.transition(q.inq_id,"OPEN","TRIAGE_AUTHORITY")
    core.transition(q.inq_id,"INVESTIGATING","TRIAGE_AUTHORITY")
    core.transition(q.inq_id,"RESOLVED","INVESTIGATION_AUTHORITY","original resolution")
    core.transition(q.inq_id,"CLOSED","CLOSURE_AUTHORITY")
    return core,q

def deny(fn):
    try: fn()
    except AmendmentDenied: return True
    return False

def main():
    _,q=setup(); m=AmendmentManager()
    old=q.resolution_statement

    # New evidence never mutates the closed INQ.
    a=m.amend(q,["O2"],"CORROBORATES","new evidence supports original","INVESTIGATION_AUTHORITY")
    assert q.status=="CLOSED" and q.resolution_statement==old

    # Idempotency.
    a2=m.amend(q,["O2"],"CORROBORATES","new evidence supports original","INVESTIGATION_AUTHORITY")
    assert a2.amendment_id==a.amendment_id and len(m.amendments)==1

    # Insufficient evidence is represented explicitly.
    b=m.amend(q,["O3"],"INSUFFICIENT","evidence is inconclusive","INVESTIGATION_AUTHORITY")
    assert b.state=="OPEN" and q.resolution_statement==old

    # Conflict creates a separate object, not a reopened INQ.
    c=m.amend(q,["O4"],"CONFLICTS","new evidence challenges original","INVESTIGATION_AUTHORITY")
    conflict=m.open_conflict(q,c,"Calibration evidence contradicts the original conclusion","RESOLUTION_AUTHORITY")
    assert q.status=="CLOSED" and conflict.state=="OPEN"

    # Unauthorized conflict resolution is denied.
    assert deny(lambda:m.resolve_conflict(conflict,"INVESTIGATION_AUTHORITY","SUPERSEDE"))

    # Conflict may be upheld without mutating original INQ.
    m.resolve_conflict(conflict,"RESOLUTION_AUTHORITY","UPHOLD")
    assert conflict.state=="RESOLVED" and q.resolution_statement==old

    # A second conflicting amendment creates a distinct conflict.
    d=m.amend(q,["O5"],"CONFLICTS","independent contradiction","INVESTIGATION_AUTHORITY")
    c2=m.open_conflict(q,d,"Independent evidence remains contradictory","RESOLUTION_AUTHORITY")
    assert c2.conflict_id!=conflict.conflict_id

    # Invalid mutation paths are rejected.
    assert deny(lambda:m.amend(q,[],"CONFLICTS","x","x"))
    assert deny(lambda:m.amend(q,["O6"],"INVALID","x","x"))

    print("PASS | INQ amendment/conflict safety")
    print("SUMMARY | 8/8 amendment/conflict invariants PASS")

if __name__=="__main__": main()
