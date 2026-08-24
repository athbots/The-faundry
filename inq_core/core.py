from dataclasses import dataclass, field
import hashlib, json

class INQDenied(Exception): pass

STATUSES=("CANDIDATE","OPEN","INVESTIGATING","RESOLVED","CLOSED","CANCELLED")

@dataclass
class INQ:
    inq_id:str
    title:str
    question:str
    status:str
    trigger_observation_ids:tuple
    evidence_digest:str
    reason:str
    scope:str
    hypotheses:tuple
    investigation_plan:str
    owner:str
    authority:str
    schema_version:str="FS-INQ-002:v1"
    resolution_statement:str|None=None
    residual_uncertainties:tuple=()
    events:list=field(default_factory=list)

class InquiryCore:
    def __init__(self):
        self.items={}

    def create(self, candidate, title, question, scope, owner, authority="TRIAGE_AUTHORITY"):
        if candidate.state!="CANDIDATE": raise INQDenied("not a candidate")
        if not title or not question or not scope or not owner: raise INQDenied("missing required field")
        iid="INQ-"+hashlib.sha256((candidate.candidate_id+"|FS-INQ-002:v1").encode()).hexdigest()[:24]
        if iid in self.items: return self.items[iid]
        x=INQ(iid,title,question,"CANDIDATE",candidate.observation_ids,
              candidate.evidence_digest,candidate.reason,scope,(), "",owner,authority)
        x.events.append(("CREATED","CANDIDATE"))
        self.items[iid]=x
        return x

    def transition(self, iid, target, authority, resolution_statement=None, residual_uncertainties=()):
        if iid not in self.items: raise INQDenied("unknown INQ")
        x=self.items[iid]
        allowed={
            "CANDIDATE":{"OPEN"},
            "OPEN":{"INVESTIGATING","CANCELLED"},
            "INVESTIGATING":{"RESOLVED","CANCELLED"},
            "RESOLVED":{"CLOSED"},
            "CLOSED":set(),
            "CANCELLED":set(),
        }
        if target not in allowed[x.status]: raise INQDenied("invalid transition")
        if target=="OPEN" and authority!="TRIAGE_AUTHORITY": raise INQDenied("triage authority required")
        if target=="RESOLVED":
            if authority!="INVESTIGATION_AUTHORITY": raise INQDenied("resolution authority required")
            if not resolution_statement: raise INQDenied("resolution statement required")
        if target=="CLOSED" and authority!="CLOSURE_AUTHORITY": raise INQDenied("closure authority required")
        if target=="CANCELLED" and authority not in {"TRIAGE_AUTHORITY","INVESTIGATION_AUTHORITY"}:
            raise INQDenied("cancellation authority required")
        old=x.status; x.status=target
        if resolution_statement is not None: x.resolution_statement=resolution_statement
        x.residual_uncertainties=tuple(residual_uncertainties)
        x.events.append((target,authority))
        return x
