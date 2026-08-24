import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from canonical_obs.state_machine import CanonicalOBS
from canonical_obs.authority import AuthorityService, Capability, AuthorizationDenied
from runtime.canonical_runtime import CanonicalRuntime

R=[]
def T(n,f):
    try:f(); print("PASS | "+n); R.append(True)
    except Exception as e: print("FAIL | "+n+" | "+type(e).__name__+": "+str(e)); R.append(False)

def forge():
    a=AuthorityService(); legit=a.issue("validator","OBS_VALIDATOR")
    o=CanonicalOBS("factory","x")
    try:o.transition("VALIDATING","forged",Capability(legit._token,"attacker","TRIAGE_POLICY"),a)
    except AuthorizationDenied:return
    raise AssertionError("forged capability accepted")

def foreign():
    a=AuthorityService(); b=AuthorityService(); cap=a.issue("capture","OBS_CAPTURE"); o=CanonicalOBS("factory","x")
    try:o.transition("VALIDATING","foreign",cap,b)
    except AuthorizationDenied:return
    raise AssertionError("foreign authority accepted")

def replay_scope():
    a=AuthorityService(); cap=a.issue("capture","OBS_CAPTURE"); o=CanonicalOBS("factory","x")
    o.transition("VALIDATING","first",cap,a)
    try:o.transition("ACCEPTED","replay",cap,a)
    except AuthorizationDenied:return
    raise AssertionError("wrong-scope replay accepted")

def no_cap():
    a=AuthorityService(); o=CanonicalOBS("factory","x")
    try:o.transition("VALIDATING","direct",None,a)
    except AuthorizationDenied:return
    raise AssertionError("unauthorized direct transition accepted")

def evidence():
    p={"sensor":"S1","reading":{"value":80}}; o=CanonicalOBS("factory",p); p["reading"]["value"]=0
    assert o.raw_payload["reading"]["value"]==80
    for k,v in [("object_id","ATTACK"),("source","ATTACK"),("raw_payload",{})]:
        try:setattr(o,k,v)
        except AttributeError:continue
        raise AssertionError(k+" mutation accepted")

def audit():
    r=CanonicalRuntime(); o=r.create_obs("factory","x"); r.validate(o); r.triage(o,"GRADUATED_TO_INQ")
    h=o.history[-1]; assert h["actor"]=="triage-policy" and h["capability"]=="TRIAGE_POLICY"

def bad_type():
    a=AuthorityService(); o=CanonicalOBS("factory","x")
    try:o.transition("VALIDATING","bad","OBS_CAPTURE",a)
    except (AuthorizationDenied,TypeError):return
    raise AssertionError("invalid capability type accepted")

for n,f in [
("PV01-01 capability forgery",forge),
("PV01-02 foreign authority substitution",foreign),
("PV01-03 wrong-scope replay",replay_scope),
("PV01-04 direct transition bypass",no_cap),
("PV01-05 immutable evidence",evidence),
("PV01-06 audit provenance",audit),
("PV01-07 invalid capability type",bad_type)]:
    T(n,f)
print(f"SUMMARY | {sum(R)}/{len(R)} PV01 security tests PASS")
raise SystemExit(0 if all(R) else 1)
