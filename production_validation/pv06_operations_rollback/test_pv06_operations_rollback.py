import json, hashlib, tempfile, os

class DeploymentError(Exception): pass

class DeploymentController:
    def __init__(self):
        self.releases={}
        self.active=None
        self.known_good=None
        self.history=[]
        self.evidence=[{"id":"OBS-1","state":"ACCEPTED","version":1}]
    def publish(self, rid, artifact):
        digest=hashlib.sha256(artifact.encode()).hexdigest()
        self.releases[rid]={"digest":digest,"artifact":artifact}
        return digest
    def activate(self,rid):
        if rid not in self.releases: raise DeploymentError("unknown release")
        if self.active is not None:
            self.known_good=self.active
        self.active=rid
        self.history.append({"action":"ACTIVATE","release":rid})
    def rollback(self):
        if not self.known_good: raise DeploymentError("no known-good release")
        failed=self.active
        self.active=self.known_good
        self.history.append({"action":"ROLLBACK","from":failed,"to":self.active})
    def snapshot(self):
        return json.dumps(self.evidence,sort_keys=True), list(self.history)

def T(name,fn,R):
    try: fn(); print("PASS | "+name); R.append(True)
    except Exception as e: print("FAIL | "+name+" | "+type(e).__name__+": "+str(e)); R.append(False)

R=[]
def test_release_identity():
    c=DeploymentController()
    d1=c.publish("R1","known-good")
    d2=c.publish("R2","defective")
    assert d1!=d2 and c.releases["R1"]["digest"]==d1

def test_known_good_recorded():
    c=DeploymentController(); c.publish("R1","good"); c.activate("R1")
    c.publish("R2","new"); c.activate("R2")
    assert c.known_good=="R1" and c.active=="R2"

def test_rollback():
    c=DeploymentController(); c.publish("R1","good"); c.activate("R1")
    c.publish("R2","defective"); c.activate("R2"); c.rollback()
    assert c.active=="R1"
    assert c.history[-1]["action"]=="ROLLBACK"

def test_evidence_preserved():
    c=DeploymentController(); before,_=c.snapshot()
    c.publish("R1","good"); c.activate("R1"); c.publish("R2","bad"); c.activate("R2"); c.rollback()
    after,_=c.snapshot()
    assert before==after

def test_rollback_missing_good_fails_closed():
    c=DeploymentController(); c.publish("R1","first"); c.activate("R1")
    c.known_good=None
    try: c.rollback()
    except DeploymentError: return
    raise AssertionError("rollback succeeded without known-good release")

def test_rollback_is_audited():
    c=DeploymentController(); c.publish("R1","good"); c.activate("R1")
    c.publish("R2","bad"); c.activate("R2"); c.rollback()
    assert c.history[-1]=={"action":"ROLLBACK","from":"R2","to":"R1"}

def test_no_mixed_authoritative_version():
    c=DeploymentController(); c.publish("R1","good"); c.activate("R1")
    c.publish("R2","bad"); c.activate("R2"); c.rollback()
    assert c.active=="R1"
    assert c.known_good=="R1"

def test_history_not_rewritten():
    c=DeploymentController(); c.publish("R1","good"); c.activate("R1")
    c.publish("R2","bad"); c.activate("R2"); c.rollback()
    actions=[x["action"] for x in c.history]
    assert actions==["ACTIVATE","ACTIVATE","ROLLBACK"]

tests=[
("PV06-01 immutable release identity",test_release_identity),
("PV06-02 known-good release recorded",test_known_good_recorded),
("PV06-03 rollback restores known-good",test_rollback),
("PV06-04 evidence survives rollback",test_evidence_preserved),
("PV06-05 missing known-good fails closed",test_rollback_missing_good_fails_closed),
("PV06-06 rollback is audited",test_rollback_is_audited),
("PV06-07 no mixed authoritative version",test_no_mixed_authoritative_version),
("PV06-08 deployment history is preserved",test_history_not_rewritten),
]
for n,f in tests:T(n,f,R)
print(f"SUMMARY | PV06 operations/rollback | {sum(R)}/{len(R)} PASS")
raise SystemExit(0 if all(R) else 1)
