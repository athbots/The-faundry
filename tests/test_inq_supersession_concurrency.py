import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from inq_core.supersession import INQIntegrity, VersionedINQ, SupersessionDenied, ConcurrencyConflict

def denied(fn):
    try: fn()
    except (SupersessionDenied,ConcurrencyConflict): return True
    return False

def main():
    api=INQIntegrity(); q=VersionedINQ("INQ-1")
    r1=api.create_initial_resolution(q,"R1 supported",["WP-1"],"RESOLUTION_AUTHORITY")
    rev=q.revision
    api.transition(q,"CLOSED","CLOSURE_AUTHORITY",rev)
    assert denied(lambda: api.transition(q,"CANCELLED","TRIAGE_AUTHORITY",rev))
    assert q.status=="CLOSED" and q.revision==2

    r2=api.supersede(q,"R2 supersedes R1",["WP-2"],"new calibrated evidence",
                     "RESOLUTION_AUTHORITY",r1.resolution_id,r1.digest,q.revision)
    assert r2.predecessor_id==r1.resolution_id and r2.predecessor_digest==r1.digest
    assert r1.statement=="R1 supported" and q.resolutions[0].digest==r1.digest

    oldrev=q.revision
    assert denied(lambda: api.supersede(q,"stale",["WP-3"],"reason","RESOLUTION_AUTHORITY",
                                        r2.resolution_id,r2.digest,oldrev-1))
    assert q.revision==oldrev and len(q.resolutions)==2
    assert denied(lambda: api.supersede(q,"bad digest",["WP-4"],"reason","RESOLUTION_AUTHORITY",
                                        r2.resolution_id,"wrong",q.revision))
    assert denied(lambda: api.supersede(q,"unauthorized",["WP-5"],"reason","INVESTIGATION_AUTHORITY",
                                        r2.resolution_id,r2.digest,q.revision))

    r3=api.supersede(q,"R3 supersedes R2",["WP-6"],"new evidence",
                     "RESOLUTION_AUTHORITY",r2.resolution_id,r2.digest,q.revision)
    assert [r.predecessor_id for r in q.resolutions]==[None,r1.resolution_id,r2.resolution_id]
    assert [e[0] for e in q.events]==["RESOLUTION_CREATED","TRANSITION","SUPERSEDES","SUPERSEDES"]
    print("PASS | INQ supersession and optimistic concurrency")
    print("SUMMARY | 10/10 integrity invariants PASS")

if __name__=="__main__": main()
