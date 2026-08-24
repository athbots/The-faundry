import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from dec_core.concurrency import VersionedStore,ConcurrencyDenied
def denied(f):
    try:f()
    except ConcurrencyDenied:return True
    return False
def main():
    s=VersionedStore(); r=s.create("DEC-17-001")
    assert s.read("DEC-17-001")[1]==0
    s.commit("DEC-17-001",0,"AUTHORIZED","A","K-A")
    assert s.read("DEC-17-001")[1]==1
    assert denied(lambda:s.commit("DEC-17-001",0,"EXECUTING","B","K-B"))
    x=s.commit("DEC-17-001",1,"EXECUTING","B","K-B")
    assert s.commit("DEC-17-001",1,"EXECUTING","B","K-B") is x
    assert denied(lambda:s.commit("DEC-17-001",2,"VERIFYING","C","K-B"))
    s.commit("DEC-17-001",2,"VERIFIED","C","K-C")
    assert denied(lambda:s.commit("DEC-17-001",3,"ABORTED","D","K-D"))
    assert len(r.history)==3
    new=s.supersede("DEC-17-001","DEC-17-002")
    assert new.record_id=="DEC-17-002"
    assert s.read("DEC-17-001")[2]=="SUPERSEDED"
    assert denied(lambda:s.commit("DEC-17-001",4,"OPEN","E","K-E"))
    assert s.read("DEC-17-002")[1]==0
    assert denied(lambda:s.commit("UNKNOWN",0,"AUTHORIZED","X","K-X"))
    print("PASS | PV-17 concurrency and persistence reference model")
    print("SUMMARY | 12/12 concurrency invariants PASS")
if __name__=="__main__":main()
