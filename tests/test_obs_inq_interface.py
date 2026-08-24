import sys,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from inq_interface.interface import OBS,OBSInquiryInterface,InterfaceDenied

def obs(i,state="ACCEPTED",p="P1"):
    return OBS(i,state,hashlib.sha256(i.encode()).hexdigest()[:8],p)

def digest(*xs): return "|".join(sorted(x.evidence_digest for x in xs))

def expect_denied(fn):
    try: fn()
    except InterfaceDenied: return
    raise AssertionError("expected denial")

def main():
    api=OBSInquiryInterface()
    a,b=obs("O1"),obs("O2")

    c=api.create_candidate([a,b],"CONTRADICTORY",digest(a,b),"triage-operator","conflicting evidence")
    assert c.state=="CANDIDATE"
    assert c.observation_ids==("O1","O2")
    assert len(api.events)==1

    # Idempotency
    c2=api.create_candidate([b,a],"CONTRADICTORY",digest(a,b),"triage-operator","same evidence")
    assert c2.candidate_id==c.candidate_id and len(api.candidates)==1

    # DISTINCT and UNIT_MISMATCH must fail closed.
    expect_denied(lambda: api.create_candidate([a,b],"DISTINCT",digest(a,b),"x","x"))
    expect_denied(lambda: api.create_candidate([a,b],"UNIT_MISMATCH",digest(a,b),"x","x"))

    # Bad state cannot enter the interface.
    bad=obs("O3","RAW")
    expect_denied(lambda: api.create_candidate([bad,b],"RELATED",digest(bad,b),"x","x"))

    # Evidence/provenance is mandatory.
    no_prov=OBS("O4","ACCEPTED",obs("O4").evidence_digest,"")
    expect_denied(lambda: api.create_candidate([no_prov],"RELATED",no_prov.evidence_digest,"x","x"))
    expect_denied(lambda: api.create_candidate([a,b],"RELATED","wrong","x","x"))

    # Candidate cannot self-graduate.
    expect_denied(lambda: api.graduate(c.candidate_id,"candidate"))
    result=api.graduate(c.candidate_id,"TRIAGE_AUTHORITY")
    assert result["state"]=="INQ"

    # Audit events preserve the two-stage boundary.
    assert [e["event"] for e in api.events]==[
        "INQUIRY_CANDIDATE_CREATED","INQUIRY_GRADUATED"
    ]

    print("PASS | OBS→INQ interface | all boundary invariants")
    print("SUMMARY | 8/8 interface invariants PASS")

if __name__=="__main__":
    main()
