import sys
sys.path.insert(0,".")
from canonical_obs.state_machine import CanonicalOBS
from runtime.graduation_authority import GraduationAuthority, GraduationDenied
from runtime.direct_state_guard import DirectStateGuard

R=[]
def T(n,f):
    try:f(); print("PASS | "+n); R.append(True)
    except Exception as e: print("FAIL | "+n+" | "+type(e).__name__+": "+str(e)); R.append(False)

def obs_in_triage():
    o=CanonicalOBS("factory","safety deviation")
    for target in ["VALIDATING","ACCEPTED","TRIAGE"]:
        o.transition(target,"setup","TEST")
    return o

def unauthorized():
    a=GraduationAuthority()
    o=obs_in_triage()
    try:a.graduate(o,"USER",True,"INQ-1")
    except GraduationDenied:return
    raise AssertionError("unauthorized actor graduated OBS")

def no_materiality():
    a=GraduationAuthority(); o=obs_in_triage()
    try:a.graduate(o,"TRIAGE_POLICY",False,"INQ-1")
    except GraduationDenied:return
    raise AssertionError("non-material OBS graduated")

def no_inq_identity():
    a=GraduationAuthority(); o=obs_in_triage()
    try:a.graduate(o,"TRIAGE_POLICY",True,None)
    except GraduationDenied:return
    raise AssertionError("graduation without INQ identity accepted")

def duplicate():
    a=GraduationAuthority(); o=obs_in_triage()
    a.graduate(o,"TRIAGE_POLICY",True,"INQ-1")
    try:a.graduate(o,"TRIAGE_POLICY",True,"INQ-2")
    except GraduationDenied:return
    raise AssertionError("duplicate graduation accepted")

def direct_manipulation():
    o=obs_in_triage()
    assert DirectStateGuard.attempt(o,"GRADUATED_TO_INQ") is True, "current transition layer cannot distinguish authority"
    # This intentionally exposes the next architectural weakness.
    raise AssertionError("state transition itself accepts an untrusted actor; authority is only external")

def authorized():
    a=GraduationAuthority(); o=obs_in_triage()
    a.graduate(o,"TRIAGE_POLICY",True,"INQ-1")
    assert o.state=="GRADUATED_TO_INQ"

T("C017-001 unauthorized actor blocked",unauthorized)
T("C017-002 materiality required",no_materiality)
T("C017-003 INQ identity required",no_inq_identity)
T("C017-004 duplicate graduation blocked",duplicate)
T("C017-005 authorized graduation succeeds",authorized)
T("C017-006 direct state manipulation attack",direct_manipulation)
print(f"SUMMARY | {sum(R)}/{len(R)} authority tests PASS")
raise SystemExit(0 if all(R) else 1)
