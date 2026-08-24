import sys,sqlite3,tempfile,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from foundry_core.persistent_transition import PersistentTransitionStore
R=[]
def T(n,f):
 try:f();print("PASS | "+n);R.append(True)
 except Exception as e:print("FAIL | "+n+" | "+type(e).__name__+": "+str(e));R.append(False)
def fresh():
 fd,p=tempfile.mkstemp();os.close(fd);s=PersistentTransitionStore(p);s.insert("OBS-1",{"v":80},"TRIAGE");return p,s
def rollback():
 p,s=fresh()
 try:
  d=sqlite3.connect(p,isolation_level=None);d.execute("BEGIN IMMEDIATE");d.execute("UPDATE obs SET state='MERGED',version=version+1 WHERE id='OBS-1'");d.execute("INSERT INTO events VALUES('E','OBS-1','TRIAGE','MERGED',1,'A','x')");d.execute("ROLLBACK");d.close();assert s.get("OBS-1")[0:2]==("TRIAGE",0);assert s.event_count("OBS-1")==0
 finally:os.remove(p)
def restart():
 p,s=fresh()
 try:
  assert s.cas_transition("OBS-1","TRIAGE","MERGED","A","commit");s2=PersistentTransitionStore(p);assert s2.get("OBS-1")[0]=="MERGED" and s2.event_count("OBS-1")==1
 finally:os.remove(p)
def recovery():
 p,s=fresh()
 try:
  d=sqlite3.connect(p,isolation_level=None);d.execute("BEGIN IMMEDIATE");d.execute("UPDATE obs SET state='MERGED',version=version+1 WHERE id='OBS-1'");d.execute("INSERT INTO events VALUES('E','OBS-1','TRIAGE','MERGED',1,'A','x')");d.execute("ROLLBACK");d.close();s2=PersistentTransitionStore(p);assert s2.cas_transition("OBS-1","TRIAGE","SUPPRESSED","A","recovery");assert s2.event_count("OBS-1")==1
 finally:os.remove(p)
for n,f in [("PV02-01 interrupted transaction rollback",rollback),("PV02-02 committed state survives reopen",restart),("PV02-03 recovery after interrupted transaction",recovery)]:T(n,f)
print(f"SUMMARY | {sum(R)}/{len(R)} PV02 failure-injection tests PASS");raise SystemExit(0 if all(R) else 1)
