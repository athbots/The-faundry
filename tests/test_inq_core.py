import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from inq_interface.interface import OBS,OBSInquiryInterface
from inq_core.core import InquiryCore,INQDenied
import hashlib

def o(i):
    return OBS(i,"ACCEPTED",hashlib.sha256(i.encode()).hexdigest()[:8],"P1")

def main():
    bridge=OBSInquiryInterface()
    a,b=o("O1"),o("O2")
    digest="|".join(sorted([a.evidence_digest,b.evidence_digest]))
    c=bridge.create_candidate([a,b],"CONTRADICTORY",digest,"operator","conflict")

    core=InquiryCore()
    q=core.create(c,"Motor temperature conflict",
                  "Which observation reflects the supported motor state?",
                  "motor-A / temperature / incident window","analyst")
    assert q.status=="CANDIDATE"

    # Candidate cannot skip triage.
    try: core.transition(q.inq_id,"OPEN","operator")
    except INQDenied: pass
    else: raise AssertionError("unauthorized opening")

    core.transition(q.inq_id,"OPEN","TRIAGE_AUTHORITY")
    core.transition(q.inq_id,"INVESTIGATING","TRIAGE_AUTHORITY")

    # Resolution requires explicit statement and authority.
    try: core.transition(q.inq_id,"RESOLVED","TRIAGE_AUTHORITY","resolved")
    except INQDenied: pass
    else: raise AssertionError("weak resolution authority accepted")

    core.transition(q.inq_id,"RESOLVED","INVESTIGATION_AUTHORITY",
                    "OBS-002 is supported by calibrated sensor evidence",
                    ["sensor calibration residual"])
    assert q.status=="RESOLVED"
    assert q.residual_uncertainties==("sensor calibration residual",)

    # Closure remains separate.
    try: core.transition(q.inq_id,"CLOSED","INVESTIGATION_AUTHORITY")
    except INQDenied: pass
    else: raise AssertionError("unauthorized closure")

    core.transition(q.inq_id,"CLOSED","CLOSURE_AUTHORITY")
    assert q.status=="CLOSED"

    # No transition after closure.
    try: core.transition(q.inq_id,"OPEN","TRIAGE_AUTHORITY")
    except INQDenied: pass
    else: raise AssertionError("closed INQ reopened")

    # Every transition is retained.
    assert [e[0] for e in q.events]==["CREATED","OPEN","INVESTIGATING","RESOLVED","CLOSED"]
    print("PASS | INQ core lifecycle and authority boundary")
    print("SUMMARY | 8/8 INQ invariants PASS")

if __name__=="__main__": main()
