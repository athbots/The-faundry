from dataclasses import dataclass, field
import hashlib, json

class SupersessionDenied(Exception): pass
class ConcurrencyConflict(Exception): pass

@dataclass(frozen=True)
class ResolutionRecord:
    resolution_id:str; inq_id:str; statement:str; evidence_ids:tuple
    authority:str; predecessor_id:str|None; predecessor_digest:str|None
    reason:str; digest:str

@dataclass
class VersionedINQ:
    inq_id:str; status:str="RESOLVED"; revision:int=0
    resolutions:list=field(default_factory=list); events:list=field(default_factory=list)

class INQIntegrity:
    def create_initial_resolution(self,q,statement,evidence_ids,authority):
        if authority!="RESOLUTION_AUTHORITY": raise SupersessionDenied("resolution authority required")
        if not statement or not evidence_ids: raise SupersessionDenied("resolution evidence required")
        rid="RES-"+hashlib.sha256((q.inq_id+"|"+statement+"|"+json.dumps(sorted(evidence_ids))).encode()).hexdigest()[:24]
        digest=hashlib.sha256((rid+"|"+statement+"|"+json.dumps(sorted(evidence_ids))).encode()).hexdigest()
        r=ResolutionRecord(rid,q.inq_id,statement,tuple(sorted(evidence_ids)),authority,None,None,"initial",digest)
        q.resolutions.append(r); q.events.append(("RESOLUTION_CREATED",rid,authority)); q.revision+=1
        return r

    def transition(self,q,target,authority,expected_revision):
        if expected_revision!=q.revision: raise ConcurrencyConflict("stale revision")
        if target not in {"CLOSED","CANCELLED"}: raise SupersessionDenied("unsupported transition")
        if target=="CLOSED" and authority!="CLOSURE_AUTHORITY": raise SupersessionDenied("closure authority required")
        if target=="CANCELLED" and authority not in {"TRIAGE_AUTHORITY","INVESTIGATION_AUTHORITY"}:
            raise SupersessionDenied("cancellation authority required")
        q.status=target; q.revision+=1; q.events.append(("TRANSITION",target,authority,q.revision))
        return q

    def supersede(self,q,statement,evidence_ids,reason,authority,predecessor_id,predecessor_digest,expected_revision):
        if expected_revision!=q.revision: raise ConcurrencyConflict("stale revision")
        if authority!="RESOLUTION_AUTHORITY": raise SupersessionDenied("resolution authority required")
        if q.status!="CLOSED": raise SupersessionDenied("supersession requires closed INQ")
        if not statement or not evidence_ids or not reason: raise SupersessionDenied("missing supersession basis")
        if not q.resolutions: raise SupersessionDenied("no predecessor resolution")
        prev=q.resolutions[-1]
        if predecessor_id!=prev.resolution_id or predecessor_digest!=prev.digest:
            raise SupersessionDenied("predecessor mismatch")
        rid="RES-"+hashlib.sha256((q.inq_id+"|"+statement+"|"+json.dumps(sorted(evidence_ids))+"|"+prev.digest).encode()).hexdigest()[:24]
        digest=hashlib.sha256((rid+"|"+statement+"|"+json.dumps(sorted(evidence_ids))+"|"+prev.digest).encode()).hexdigest()
        r=ResolutionRecord(rid,q.inq_id,statement,tuple(sorted(evidence_ids)),authority,prev.resolution_id,prev.digest,reason,digest)
        q.resolutions.append(r); q.events.append(("SUPERSEDES",prev.resolution_id,rid,authority)); q.revision+=1
        return r
