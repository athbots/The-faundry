import sys,os,sqlite3,tempfile,shutil,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from foundry_core.persistent_transition import PersistentTransitionStore
R=[]
def T(n,f):
 try:f();print("PASS | "+n);R.append(True)
 except Exception as e:print("FAIL | "+n+" | "+type(e).__name__+": "+str(e));R.append(False)
def fresh():
 fd,p=tempfile.mkstemp();os.close(fd);s=PersistentTransitionStore(p);s.insert("OBS-1",{"v":80},"TRIAGE");s.insert("OBS-2",{"v":81},"TRIAGE");s.cas_transition("OBS-1","TRIAGE","MERGED","AUTH","seed");return p,s
def backup():
 p,s=fresh();b=p+".bak";r=p+".restore"
 try:
  s.cas_transition("OBS-2","TRIAGE","SUPPRESSED","AUTH","seed");shutil.copy2(p,b);shutil.copy2(b,r);x=PersistentTransitionStore(r)
  assert x.get("OBS-1")[0]=="MERGED" and x.get("OBS-2")[0]=="SUPPRESSED" and x.event_count("OBS-1")==1 and x.event_count("OBS-2")==1
 finally:
  for x in(p,b,r):
   if os.path.exists(x):os.remove(x)
def lineage():
 p,s=fresh()
 try:
  s.cas_transition("OBS-2","TRIAGE","SUPPRESSED","AUTH","seed");d=sqlite3.connect(p);rows=d.execute("select obs_id,state_from,state_to,version from events order by rowid").fetchall();d.close()
  assert rows==[("OBS-1","TRIAGE","MERGED",1),("OBS-2","TRIAGE","SUPPRESSED",1)]
 finally:os.remove(p)
def replay():
 p,s=fresh()
 try:
  before=s.event_count("OBS-1");assert s.cas_transition("OBS-1","MERGED","HISTORICAL","AUTH","close");assert s.cas_transition("OBS-1","MERGED","HISTORICAL","AUTH","replay") is False;assert s.event_count("OBS-1")==before+1
 finally:os.remove(p)
def integrity():
 p,s=fresh()
 try:
  d=sqlite3.connect(p);a=d.execute("select id,state,version,payload from obs order by id").fetchall();b=d.execute("select obs_id,state_from,state_to,version,authority,reason from events order by rowid").fetchall();d.close();h=hashlib.sha256(repr((a,b)).encode()).hexdigest()
  x=PersistentTransitionStore(p);d=sqlite3.connect(p);a2=d.execute("select id,state,version,payload from obs order by id").fetchall();b2=d.execute("select obs_id,state_from,state_to,version,authority,reason from events order by rowid").fetchall();d.close();assert hashlib.sha256(repr((a2,b2)).encode()).hexdigest()==h
 finally:os.remove(p)
for n,f in [("PV03-01 backup/restore preserves state and events",backup),("PV03-02 event lineage reconstructs history",lineage),("PV03-03 replay cannot create duplicate event",replay),("PV03-04 recovered state is integrity-stable",integrity)]:T(n,f)
print(f"SUMMARY | {sum(R)}/{len(R)} PV03 recovery tests PASS");raise SystemExit(0 if all(R) else 1)
