from dataclasses import dataclass, field
import hashlib, json

class ExecutionDenied(Exception): pass

@dataclass(frozen=True)
class ExecutionAuthorization:
    authorization_id:str
    decision_id:str
    decision_digest:str
    scope:str
    executor:str
    authority:str
    start_conditions:str
    stop_conditions:str
    expected_outcome:str
    verification_plan:str
    rollback_plan:str
    schema_version:str="FS-DEC-002:v1"

@dataclass
class Execution:
    execution_id:str
    authorization_id:str
    state:str="AUTHORIZED"
    events:list=field(default_factory=list)
    outcome_evidence:tuple=()
    verification_statement:str|None=None

class ExecutionCore:
    def __init__(self, decisions):
        self.decisions=decisions
        self.authorizations={}
        self.executions={}

    def authorize(self, decision_id, decision_digest, scope, executor, authority,
                  start_conditions, stop_conditions, expected_outcome,
                  verification_plan, rollback_plan):
        d=self.decisions.get(decision_id)
        if d is None: raise ExecutionDenied("unknown decision")
        if d.outcome!="YES": raise ExecutionDenied("only YES decisions may execute")
        if not decision_digest or decision_digest != self._decision_digest(d):
            raise ExecutionDenied("decision digest mismatch")
        required=[scope,executor,authority,start_conditions,stop_conditions,
                  expected_outcome,verification_plan,rollback_plan]
        if any(not x for x in required):
            raise ExecutionDenied("incomplete execution authorization")
        material=json.dumps({
            "decision":decision_id,"digest":decision_digest,"scope":scope,
            "executor":executor,"authority":authority,
            "expected":expected_outcome
        },sort_keys=True)
        aid="EXAUTH-"+hashlib.sha256(material.encode()).hexdigest()[:24]
        a=ExecutionAuthorization(aid,decision_id,decision_digest,scope,executor,
             authority,start_conditions,stop_conditions,expected_outcome,
             verification_plan,rollback_plan)
        self.authorizations[aid]=a
        return a

    def start(self, authorization_id):
        a=self.authorizations.get(authorization_id)
        if not a: raise ExecutionDenied("unknown authorization")
        eid="EXEC-"+hashlib.sha256(authorization_id.encode()).hexdigest()[:24]
        if eid in self.executions: return self.executions[eid]
        e=Execution(eid,authorization_id)
        e.events.append(("AUTHORIZED","EXECUTION_AUTHORITY"))
        e.state="EXECUTING"
        e.events.append(("EXECUTING",a.executor))
        self.executions[eid]=e
        return e

    def verify(self, execution_id, evidence_ids, statement, authority):
        e=self.executions.get(execution_id)
        if not e: raise ExecutionDenied("unknown execution")
        if e.state!="EXECUTING": raise ExecutionDenied("execution not active")
        if not evidence_ids or not statement or authority!="VERIFICATION_AUTHORITY":
            raise ExecutionDenied("verification evidence/authority required")
        e.outcome_evidence=tuple(sorted(evidence_ids))
        e.verification_statement=statement
        e.state="VERIFIED"
        e.events.append(("VERIFIED",authority,tuple(sorted(evidence_ids))))
        return e

    def abort(self, execution_id, trigger, evidence_id, authority):
        e=self.executions.get(execution_id)
        if not e: raise ExecutionDenied("unknown execution")
        if e.state!="EXECUTING": raise ExecutionDenied("execution not active")
        if not trigger or not evidence_id or authority!="EXECUTION_AUTHORITY":
            raise ExecutionDenied("abort evidence/authority required")
        e.state="ABORTED"
        e.events.append(("ABORTED",authority,trigger,evidence_id))
        return e

    @staticmethod
    def _decision_digest(d):
        # Deterministic digest of the immutable decision record.
        raw=json.dumps({
            "decision_id":d.decision_id,
            "proposal_id":d.proposal_id,
            "outcome":d.outcome,
            "rationale":d.rationale,
            "authority":d.authority
        },sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()
