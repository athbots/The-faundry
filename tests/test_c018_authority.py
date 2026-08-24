import sys
sys.path.insert(0,".")
from canonical_obs.state_machine import CanonicalOBS
from canonical_obs.authority import Capability, AuthorizationDenied
from runtime.canonical_runtime import CanonicalRuntime

R=[]
def T(n,f):
 try:f();print("PASS | "+n);R.append(True)
 except Exception as e:print("FAIL | "+n+" | "+type(e).__name__+": "+str(e));R.append(False)

def obs(state="RAW"):
 return CanonicalOBS("factory","x",state=state)

def allowed():
 o=obs()
 o.transition("VALIDATING","capture",Capability("capture","OBS_CAPTURE"))
 o.transition("ACCEPTED","valid",Capability("validator","OBS_VALIDATOR"))
 o.transition("TRIAGE","triage",Capability("engine","TRIAGE_ENGINE"))
 o.transition("GRADUATED_TO_INQ","material",Capability("policy","TRIAGE_POLICY"))
 assert o.state=="GRADUATED_TO_INQ"

def spoof():
 o=obs()
 try:o.transition("VALIDATING","spoof",Capability("attacker","TRIAGE_POLICY"))
 except AuthorizationDenied:return
 raise AssertionError("attacker spoofed capability name")

def wrong_capability():
 o=obs()
 try:o.transition("VALIDATING","wrong",Capability("validator","OBS_VALIDATOR"))
 except AuthorizationDenied:return
 raise AssertionError("wrong capability permitted transition")

def raw_direct():
 o=obs()
 try:o.transition("GRADUATED_TO_INQ","direct",Capability("attacker","TRIAGE_POLICY"))
 except ValueError: # capability valid, state transition invalid
     return
 except AuthorizationDenied:
     raise AssertionError("TRIAGE_POLICY should be capable, but RAW state must block")
 raise AssertionError("RAW graduation accepted")

def all_protected():
 paths=[
 ("VALIDATING","OBS_CAPTURE","RAW"),
 ("ACCEPTED","OBS_VALIDATOR","VALIDATING"),
 ("TRIAGE","TRIAGE_ENGINE","ACCEPTED"),
 ("SUPPRESSED","OBS_VALIDATOR","VALIDATING"),
 ("MERGED","TRIAGE_POLICY","TRIAGE"),
 ("GRADUATED_TO_INQ","TRIAGE_POLICY","TRIAGE"),
 ("HISTORICAL","HISTORY_ENGINE","MERGED"),
 ]
 for target,cap,state in paths:
  o=obs(state)
  o.transition(target,"policy",Capability("actor",cap))
  assert o.state==target

def runtime():
 r=CanonicalRuntime(); o=r.create_obs("factory","deviation")
 r.validate(o); r.triage(o,"GRADUATED_TO_INQ"); r.close(o)
 assert o.state=="HISTORICAL"

T("C018-001 authorized transition path",allowed)
T("C018-002 capability spoof rejected",spoof)
T("C018-003 wrong capability rejected",wrong_capability)
T("C018-004 direct RAW graduation blocked",raw_direct)
T("C018-005 protected transition matrix",all_protected)
T("C018-006 runtime integration",runtime)
print(f"SUMMARY | {sum(R)}/{len(R)} capability tests PASS")
raise SystemExit(0 if all(R) else 1)
