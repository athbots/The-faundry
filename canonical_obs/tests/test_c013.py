import sys
sys.path.insert(0,".")
from state_machine import CanonicalOBS
from semantic_relation import rel
R=[]
def T(n,f):
 try:f();print("PASS | "+n);R.append(True)
 except Exception as e:print("FAIL | "+n+" | "+str(e));R.append(False)
def path():
 o=CanonicalOBS("factory","x")
 for s in [("VALIDATING","capture"),("ACCEPTED","valid"),("TRIAGE","triage"),("GRADUATED_TO_INQ","material"),("HISTORICAL","closed")]:
  o.transition(s[0],s[1],"AUTH")
 assert o.state=="HISTORICAL"
T("canonical lifecycle",path)
def legacy():
 o=CanonicalOBS("f","x")
 try: o.transition("VALIDATED","legacy","legacy")
 except ValueError: return
 raise AssertionError("legacy state accepted")
T("legacy VALIDATED rejected",legacy)
T("negation contradiction",lambda: (_ for _ in ()).throw(AssertionError()) if rel("motor temperature high","motor temperature not high")!="CONTRADICTORY" else None)
T("unit mismatch",lambda: (_ for _ in ()).throw(AssertionError()) if rel("temperature 80 c","temperature 80 f")!="UNIT_MISMATCH" else None)
T("value conflict",lambda: (_ for _ in ()).throw(AssertionError()) if rel("temperature 80 c","temperature 20 c")!="VALUE_CONFLICT" else None)
T("exact equivalent",lambda: (_ for _ in ()).throw(AssertionError()) if rel("motor temperature high","motor temperature high")!="EQUIVALENT" else None)
T("paraphrase related",lambda: (_ for _ in ()).throw(AssertionError()) if rel("motor temperature high","motor thermal temperature elevated")!="EQUIVALENT" else None)
print(f"SUMMARY | {sum(R)}/{len(R)} tests PASS")
raise SystemExit(0 if all(R) else 1)
