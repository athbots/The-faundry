import sys
sys.path.insert(0,".")
from runtime.canonical_runtime import CanonicalRuntime
from canonical_obs.state_machine import CanonicalOBS
from canonical_obs.semantic_relation import rel
from canonical_obs.authority import AuthorityService, Capability, AuthorizationDenied

R=[]
def T(n,f):
    try:f();print("PASS | "+n);R.append(True)
    except Exception as e:print("FAIL | "+n+" | "+type(e).__name__+": "+str(e));R.append(False)

def lifecycle():
    r=CanonicalRuntime(); o=r.create_obs("factory","motor temperature high")
    r.validate(o); r.triage(o,"GRADUATED_TO_INQ"); r.close(o)
    assert o.state=="HISTORICAL"

def cluster_merge():
    r=CanonicalRuntime(); o=r.create_obs("factory","motor temperature high")
    r.validate(o); r.triage(o,"CLUSTERED")
    o.transition("TRIAGE","re-evaluate",r.engine,r.authority)
    r.triage(o,"MERGED"); r.close(o)
    assert o.state=="HISTORICAL"

def suppression():
    r=CanonicalRuntime(); o=r.create_obs("factory","malformed")
    r.validate(o,False)
    o.transition("HISTORICAL","archive",r.history,r.authority)
    assert o.state=="HISTORICAL"

def forbidden():
    r=CanonicalRuntime(); o=r.create_obs("factory","x")
    try:o.transition("GRADUATED_TO_INQ","attack",r.policy,r.authority)
    except ValueError:return
    raise AssertionError("RAW graduation accepted")

def legacy():
    r=CanonicalRuntime(); o=r.create_obs("factory","x")
    try:o.transition("VALIDATED","legacy",r.policy,r.authority)
    except Exception:return
    raise AssertionError("legacy state accepted")

def semantic():
    assert rel("motor temperature high","motor thermal temperature elevated")=="EQUIVALENT"
    assert rel("motor temperature high","motor temperature not high")=="CONTRADICTORY"
    assert rel("temperature 80 c","temperature 80 f")=="UNIT_MISMATCH"
    assert rel("temperature 80 c","temperature 20 c")=="VALUE_CONFLICT"

def immutability():
    o=CanonicalOBS("factory",{"value":80}); oid=o.object_id
    try:o.object_id="ATTACK"
    except AttributeError: pass
    else: raise AssertionError("object_id mutable")
    assert o.object_id==oid

def forged():
    a=AuthorityService(); legit=a.issue("validator","OBS_VALIDATOR")
    forged=Capability(legit._token,"attacker","TRIAGE_POLICY")
    o=CanonicalOBS("factory","x")
    try:o.transition("VALIDATING","forged",forged,a)
    except AuthorizationDenied:return
    raise AssertionError("forged capability accepted")

T("C019-R01 lifecycle",lifecycle)
T("C019-R02 cluster re-entry and merge",cluster_merge)
T("C019-R03 suppression",suppression)
T("C019-R04 forbidden transition",forbidden)
T("C019-R05 legacy vocabulary rejection",legacy)
T("C019-R06 semantic safety",semantic)
T("C019-R07 immutability",immutability)
T("C019-R08 capability forgery rejection",forged)
print(f"SUMMARY | {sum(R)}/{len(R)} full regression tests PASS")
raise SystemExit(0 if all(R) else 1)
