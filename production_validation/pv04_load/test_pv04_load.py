import sys,os,tempfile,time,sqlite3,statistics,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from foundry_core.persistent_transition import PersistentTransitionStore

def bench(n):
 fd,path=tempfile.mkstemp();os.close(fd); s=PersistentTransitionStore(path)
 lat=[]
 try:
  t0=time.perf_counter()
  for i in range(n):
   a=time.perf_counter();s.insert(f"O-{i}",{"sensor":"S1","value":i%100},"TRIAGE");lat.append(time.perf_counter()-a)
  insert_elapsed=time.perf_counter()-t0
  t0=time.perf_counter()
  for i in range(n):
   s.cas_transition(f"O-{i}","TRIAGE","SUPPRESSED","AUTH","load")
  trans_elapsed=time.perf_counter()-t0
  d=sqlite3.connect(path);obs=d.execute("select count(*) from obs").fetchone()[0];ev=d.execute("select count(*) from events").fetchone()[0];bad=d.execute("select count(*) from obs where state!='SUPPRESSED'").fetchone()[0];d.close()
  return {"n":n,"insert_seconds":insert_elapsed,"transition_seconds":trans_elapsed,
          "insert_ops_s":n/insert_elapsed,"transition_ops_s":n/trans_elapsed,
          "p50_insert_ms":statistics.median(lat)*1000,"obs":obs,"events":ev,"bad_states":bad}
 finally:os.remove(path)

results=[bench(n) for n in (100,1000,5000)]
for r in results:
 print(json.dumps(r))
assert all(r["obs"]==r["n"] and r["events"]==r["n"] and r["bad_states"]==0 for r in results)
print("PASS | PV04 sustained serial load | all integrity checks green")
