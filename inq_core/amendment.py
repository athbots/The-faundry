from dataclasses import dataclass, field
import hashlib, json

class AmendmentDenied(Exception): pass

@dataclass(frozen=True)
class Amendment:
    amendment_id:str
    inq_id:str
    evidence_ids:tuple
    assessment:str
    statement:str
    authority:str
    state:str="OPEN"

@dataclass
class ResolutionConflict:
    conflict_id:str
    inq_id:str
    amendment_id:str
    original_resolution_digest:str
    conflict_statement:str
    authority:str
    state:str="OPEN"
    events:list=field(default_factory=list)

class AmendmentManager:
    def __init__(self):
        self.amendments={}
        self.conflicts={}

    def amend(self, inq, evidence_ids, assessment, statement, authority):
        if inq.status!="CLOSED":
            raise AmendmentDenied("amendment mechanism is for closed INQ")
        if not evidence_ids or not statement or not authority:
            raise AmendmentDenied("missing amendment evidence/statement/authority")
        if assessment not in {"CORROBORATES","INSUFFICIENT","CONFLICTS"}:
            raise AmendmentDenied("invalid assessment")
        digest=hashlib.sha256(
            json.dumps({"inq":inq.inq_id,"evidence":sorted(evidence_ids),
                        "assessment":assessment,"statement":statement},
                       sort_keys=True).encode()).hexdigest()
        aid="AMND-"+digest[:24]
        if aid in self.amendments: return self.amendments[aid]
        a=Amendment(aid,inq.inq_id,tuple(sorted(evidence_ids)),
                    assessment,statement,authority)
        self.amendments[aid]=a
        return a

    def open_conflict(self, inq, amendment, conflict_statement, authority):
        if amendment.assessment!="CONFLICTS":
            raise AmendmentDenied("only conflicting amendment creates conflict")
        if inq.status!="CLOSED":
            raise AmendmentDenied("original INQ must remain closed")
        if not conflict_statement or not authority:
            raise AmendmentDenied("missing conflict statement/authority")
        digest=hashlib.sha256((inq.resolution_statement or "").encode()).hexdigest()
        cid="RC-"+hashlib.sha256(
            (inq.inq_id+"|"+amendment.amendment_id+"|"+digest).encode()
        ).hexdigest()[:24]
        if cid in self.conflicts: return self.conflicts[cid]
        c=ResolutionConflict(cid,inq.inq_id,amendment.amendment_id,
                             digest,conflict_statement,authority)
        c.events.append(("OPEN",authority))
        self.conflicts[cid]=c
        return c

    def resolve_conflict(self, conflict, authority, decision):
        if conflict.state!="OPEN":
            raise AmendmentDenied("conflict is not open")
        if authority!="RESOLUTION_AUTHORITY":
            raise AmendmentDenied("resolution authority required")
        if decision not in {"UPHOLD","SUPERSEDE","ESCALATE"}:
            raise AmendmentDenied("invalid conflict decision")
        conflict.state="RESOLVED" if decision!="ESCALATE" else "ESCALATED"
        conflict.events.append((conflict.state,authority,decision))
        return conflict
