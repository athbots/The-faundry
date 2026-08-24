import sys
sys.path.insert(0,".")
from runtime.canonical_runtime import CanonicalRuntime

R=[]
def T(n,f):
 try:f();print("PASS | "+n);R.append(True)
 except Exception as e:print("FAIL | "+n+" | "+str(e));R.append(False)

def happy():
 r=CanonicalRuntime(); o=r.create_obs("factory","motor temperature high"); r.validate(o); r.triage(o,"GRADUATED_TO_INQ"); r.close(o)
 assert o.state=="HISTORICAL"
 assert [x["to"] for x in o.history]==["VALIDATING","ACCEPTED","TRIAGE","GRADUATED_TO_INQ","HISTORICAL"]

def cluster_merge():
 r=CanonicalRuntime(); o=r.create_obs("factory","motor temperature high"); r.validate(o); r.triage(o,"CLUSTERED")
 o.transition("TRIAGE","new evidence","TRIAGE_ENGINE"); r.triage(o,"MERGED"); r.close(o); assert o.state=="HISTORICAL"

def suppression():
 r=CanonicalRuntime(); o=r.create_obs("factory","malformed"); r.validate(o,False); o.transition("HISTORICAL","archived","HISTORY_ENGINE"); assert o.state=="HISTORICAL"

def shortcut():
 r=CanonicalRuntime(); o=r.create_obs("factory","x")
 try:o.transition("GRADUATED_TO_INQ","shortcut","BAD_ACTOR")
 except ValueError:return
 raise AssertionError("forbidden shortcut accepted")

def semantics():
 r=CanonicalRuntime()
 assert r.compare("motor temperature high","motor temperature not high")=="CONTRADICTORY"
 assert r.compare("temperature 80 c","temperature 80 f")=="UNIT_MISMATCH"
 assert r.compare("temperature 80 c","temperature 20 c")=="VALUE_CONFLICT"
 assert r.compare("motor temperature high","motor thermal temperature elevated")=="EQUIVALENT"

T("C014-001 canonical happy path",happy)
T("C014-002 cluster re-entry and merge",cluster_merge)
T("C014-003 suppression path",suppression)
T("C014-004 forbidden shortcut blocked",shortcut)
T("C014-005 semantic safety regression",semantics)
print(f"SUMMARY | {sum(R)}/{len(R)} regression tests PASS")
raise SystemExit(0 if all(R) else 1)
