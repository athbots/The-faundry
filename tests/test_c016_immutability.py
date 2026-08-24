import sys
sys.path.insert(0,".")
from canonical_obs.state_machine import CanonicalOBS

def blocked(name, fn):
    try:
        fn()
    except Exception:
        print("PASS | "+name)
        return True
    print("FAIL | "+name+" | mutation accepted")
    return False

o=CanonicalOBS("factory", {"sensor":"S1","value":80})
r=[]
r.append(blocked("object_id immutable", lambda: setattr(o,"object_id","ATTACK")))
r.append(blocked("source immutable", lambda: setattr(o,"source","attacker")))
r.append(blocked("raw_payload immutable", lambda: setattr(o,"raw_payload",{"value":0})))

# Deep-copy protection: caller mutation must not mutate captured raw telemetry.
payload={"sensor":"S1","value":{"reading":80}}
x=CanonicalOBS("factory",payload)
payload["value"]["reading"]=0
r.append(x.raw_payload["value"]["reading"]==80)
print(("PASS" if r[-1] else "FAIL")+" | source payload deep-copy isolation")

print(f"SUMMARY | {sum(r)}/{len(r)} immutability tests PASS")
raise SystemExit(0 if all(r) else 1)
