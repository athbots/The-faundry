import sys, hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from inq_interface.interface import OBS, OBSInquiryInterface, InterfaceDenied
from inq_core.core import InquiryCore, INQDenied

def make_candidate(bridge, ids=("O1","O2"), relation="CONTRADICTORY"):
    obs=[OBS(i,"ACCEPTED",hashlib.sha256(i.encode()).hexdigest()[:8],"P") for i in ids]
    digest="|".join(sorted(o.evidence_digest for o in obs))
    return bridge.create_candidate(obs,relation,digest,"operator","investigation trigger")

def denied(fn):
    try: fn()
    except (INQDenied,InterfaceDenied): return True
    return False

def setup():
    b=OBSInquiryInterface()
    c=make_candidate(b)
    core=InquiryCore()
    q=core.create(c,"Test INQ","Resolve conflicting evidence","bounded scope","analyst")
    return b,core,q

def t01_competing_investigators():
    _,core,q=setup()
    core.transition(q.inq_id,"OPEN","TRIAGE_AUTHORITY")
    core.transition(q.inq_id,"INVESTIGATING","TRIAGE_AUTHORITY")
    assert denied(lambda: core.transition(q.inq_id,"RESOLVED","TRIAGE_AUTHORITY","bad"))
    core.transition(q.inq_id,"RESOLVED","INVESTIGATION_AUTHORITY","supported by evidence")
    assert q.status=="RESOLVED"

def t02_resolution_cannot_be_overwritten():
    _,core,q=setup()
    core.transition(q.inq_id,"OPEN","TRIAGE_AUTHORITY")
    core.transition(q.inq_id,"INVESTIGATING","TRIAGE_AUTHORITY")
    core.transition(q.inq_id,"RESOLVED","INVESTIGATION_AUTHORITY","first resolution")
    assert denied(lambda: core.transition(q.inq_id,"RESOLVED","INVESTIGATION_AUTHORITY","second resolution"))
    assert q.resolution_statement=="first resolution"

def t03_conflicting_resolutions_require_new_state():
    _,core,q=setup()
    core.transition(q.inq_id,"OPEN","TRIAGE_AUTHORITY")
    core.transition(q.inq_id,"INVESTIGATING","TRIAGE_AUTHORITY")
    core.transition(q.inq_id,"RESOLVED","INVESTIGATION_AUTHORITY","hypothesis A supported")
    # A resolved INQ cannot be reopened just to replace its conclusion.
    assert denied(lambda: core.transition(q.inq_id,"OPEN","TRIAGE_AUTHORITY"))
    assert q.status=="RESOLVED"

def t04_evidence_after_resolution_is_not_silently_absorbed():
    b,core,q=setup()
    core.transition(q.inq_id,"OPEN","TRIAGE_AUTHORITY")
    core.transition(q.inq_id,"INVESTIGATING","TRIAGE_AUTHORITY")
    core.transition(q.inq_id,"RESOLVED","INVESTIGATION_AUTHORITY","resolution based on initial evidence")
    old_digest=q.evidence_digest
    # New evidence must not mutate the historical resolution.
    c2=make_candidate(b,("O3","O4"),"VALUE_CONFLICT")
    assert q.evidence_digest==old_digest
    assert c2.candidate_id != q.inq_id

def t05_cancel_requires_authority_and_preserves_history():
    _,core,q=setup()
    core.transition(q.inq_id,"OPEN","TRIAGE_AUTHORITY")
    assert denied(lambda: core.transition(q.inq_id,"CANCELLED","random"))
    core.transition(q.inq_id,"CANCELLED","TRIAGE_AUTHORITY")
    assert q.status=="CANCELLED"
    assert [e[0] for e in q.events]==["CREATED","OPEN","CANCELLED"]

def t06_no_reopen_after_cancel():
    _,core,q=setup()
    core.transition(q.inq_id,"OPEN","TRIAGE_AUTHORITY")
    core.transition(q.inq_id,"CANCELLED","TRIAGE_AUTHORITY")
    assert denied(lambda: core.transition(q.inq_id,"OPEN","TRIAGE_AUTHORITY"))

def t07_no_recursive_self_generation():
    # The core model contains no operation that turns an INQ into another INQ.
    _,core,q=setup()
    assert not hasattr(core,"create_from_inq")

def t08_residual_uncertainty_preserved():
    _,core,q=setup()
    core.transition(q.inq_id,"OPEN","TRIAGE_AUTHORITY")
    core.transition(q.inq_id,"INVESTIGATING","TRIAGE_AUTHORITY")
    core.transition(q.inq_id,"RESOLVED","INVESTIGATION_AUTHORITY",
                    "primary hypothesis supported",["sensor drift unresolved"])
    assert q.residual_uncertainties==("sensor drift unresolved",)

def t09_closure_cannot_change_resolution():
    _,core,q=setup()
    core.transition(q.inq_id,"OPEN","TRIAGE_AUTHORITY")
    core.transition(q.inq_id,"INVESTIGATING","TRIAGE_AUTHORITY")
    core.transition(q.inq_id,"RESOLVED","INVESTIGATION_AUTHORITY","resolved")
    core.transition(q.inq_id,"CLOSED","CLOSURE_AUTHORITY")
    assert denied(lambda: core.transition(q.inq_id,"RESOLVED","INVESTIGATION_AUTHORITY","changed"))
    assert q.resolution_statement=="resolved"

def t10_history_is_append_only():
    _,core,q=setup()
    core.transition(q.inq_id,"OPEN","TRIAGE_AUTHORITY")
    core.transition(q.inq_id,"INVESTIGATING","TRIAGE_AUTHORITY")
    before=list(q.events)
    core.transition(q.inq_id,"CANCELLED","INVESTIGATION_AUTHORITY")
    assert q.events[:len(before)]==before

tests=[
("PV09-01 competing investigators cannot bypass authority",t01_competing_investigators),
("PV09-02 resolution cannot be overwritten",t02_resolution_cannot_be_overwritten),
("PV09-03 conflicting resolution cannot reopen INQ",t03_conflicting_resolutions_require_new_state),
("PV09-04 post-resolution evidence cannot mutate history",t04_evidence_after_resolution_is_not_silently_absorbed),
("PV09-05 cancellation requires authority",t05_cancel_requires_authority_and_preserves_history),
("PV09-06 cancelled INQ cannot reopen",t06_no_reopen_after_cancel),
("PV09-07 recursive INQ generation is absent",t07_no_recursive_self_generation),
("PV09-08 residual uncertainty is preserved",t08_residual_uncertainty_preserved),
("PV09-09 closure cannot alter resolution",t09_closure_cannot_change_resolution),
("PV09-10 INQ event history is append-only",t10_history_is_append_only),
]

R=[]
for name,fn in tests:
    try:
        fn(); print("PASS | "+name); R.append(True)
    except Exception as e:
        print("FAIL | "+name+" | "+type(e).__name__+": "+str(e)); R.append(False)
print(f"SUMMARY | PV09 INQ stress validation | {sum(R)}/{len(R)} PASS")
raise SystemExit(0 if all(R) else 1)
