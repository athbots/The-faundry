import sys
sys.path.insert(0,".")
from canonical_obs.state_machine import CanonicalOBS
from canonical_obs.authority import AuthorityService, Capability, AuthorizationDenied
from runtime.canonical_runtime import CanonicalRuntime

R=[]
def T(n,f):
 try:f();print("PASS | "+n);R.append(True)
 except Exception as e:print("FAIL | "+n+" | "+type(e).__name__+": "+str(e));R.append(False)

def legitimate():
 a=AuthorityService(); c=a.issue("validator","OBS_VALIDATOR"); o=CanonicalOBS("f","x")
 o.transition("VALIDATING","capture",a.issue("capture","OBS_CAPTURE"),a)
 o.transition("ACCEPTED","valid",c,a)
 assert o.state=="ACCEPTED"

def forged_capability():
 a=AuthorityService(); legit=a.issue("validator","OBS_VALIDATOR"); o=CanonicalOBS("f","x")
 forged=Capability(legit._token,"attacker","TRIAGE_POLICY")
 try:o.transition("VALIDATING","forged",forged,a)
 except AuthorizationDenied:return
 raise AssertionError("forged capability accepted")

def foreign_service():
 a1=AuthorityService(); a2=AuthorityService()
 cap=a1.issue("capture","OBS_CAPTURE"); o=CanonicalOBS("f","x")
 try:o.transition("VALIDATING","foreign",cap,a2)
 except AuthorizationDenied:return
 raise AssertionError("foreign authority accepted capability")

def wrong_capability():
 a=AuthorityService(); cap=a.issue("validator","OBS_VALIDATOR"); o=CanonicalOBS("f","x")
 try:o.transition("VALIDATING","wrong",cap,a)
 except AuthorizationDenied:return
 raise AssertionError("wrong capability accepted")

def runtime():
 r=CanonicalRuntime(); o=r.create_obs("factory","deviation")
 r.validate(o); r.triage(o,"GRADUATED_TO_INQ"); r.close(o)
 assert o.state=="HISTORICAL"

T("C019-001 legitimate issued capability",legitimate)
T("C019-002 forged capability rejected",forged_capability)
T("C019-003 foreign authority rejected",foreign_service)
T("C019-004 wrong capability rejected",wrong_capability)
T("C019-005 runtime integration",runtime)
print(f"SUMMARY | {sum(R)}/{len(R)} capability issuance tests PASS")
raise SystemExit(0 if all(R) else 1)
