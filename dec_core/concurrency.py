from dataclasses import dataclass, field

class ConcurrencyDenied(Exception): pass

@dataclass
class VersionedRecord:
    record_id: str
    version: int = 0
    state: str = "OPEN"
    history: list = field(default_factory=list)

class VersionedStore:
    def __init__(self):
        self.records={}
        self.idempotency={}

    def create(self, rid):
        if rid in self.records: raise ConcurrencyDenied("exists")
        self.records[rid]=VersionedRecord(rid)
        return self.records[rid]

    def read(self,rid):
        if rid not in self.records: raise ConcurrencyDenied("unknown")
        r=self.records[rid]
        return r.record_id,r.version,r.state

    def commit(self,rid,expected,new_state,op,key):
        r=self.records.get(rid)
        if not r: raise ConcurrencyDenied("unknown")
        old=self.idempotency.get(key)
        if old:
            if old!=(rid,op): raise ConcurrencyDenied("idempotency collision")
            return r
        if r.version!=expected: raise ConcurrencyDenied("stale")
        if r.state in {"VERIFIED","ABORTED","SUPERSEDED"}:
            raise ConcurrencyDenied("terminal")
        r.history.append((r.version,r.state,new_state,op))
        r.state=new_state; r.version+=1
        self.idempotency[key]=(rid,op)
        return r

    def supersede(self,old_id,new_id):
        old=self.records.get(old_id)
        if not old: raise ConcurrencyDenied("unknown")
        if old.state=="SUPERSEDED": raise ConcurrencyDenied("already superseded")
        self.create(new_id)
        old.history.append((old.version,old.state,"SUPERSEDED",new_id))
        old.state="SUPERSEDED"; old.version+=1
        return self.records[new_id]
