from dataclasses import dataclass
import hashlib, json

class DecisionDenied(Exception): pass

@dataclass(frozen=True)
class DecisionProposal:
    proposal_id:str; inq_ids:tuple; resolution_ids:tuple; resolution_digests:tuple
    work_product_ids:tuple; question:str; options:tuple; tradeoffs:str; risks:str
    reversibility:str; requested_authority:str; residual_uncertainty:str

@dataclass(frozen=True)
class GovernanceSignal:
    role:str; signal:str; rationale:str

@dataclass(frozen=True)
class DecisionRecord:
    decision_id:str; proposal_id:str; outcome:str; signals:tuple
    rationale:str; authority:str

class DecisionCore:
    def __init__(self): self.proposals={}; self.decisions={}

    def create_proposal(self, **kw):
        required=["inq_ids","resolution_ids","resolution_digests","work_product_ids",
                  "question","options","tradeoffs","risks","reversibility",
                  "requested_authority","residual_uncertainty"]
        if any(kw.get(k) in (None,"",(),[]) for k in required):
            raise DecisionDenied("incomplete evidence basis")
        if len(kw["resolution_ids"])!=len(kw["resolution_digests"]):
            raise DecisionDenied("resolution/digest mismatch")
        m={k:(sorted(v) if isinstance(v,(tuple,list)) else v) for k,v in kw.items()}
        pid="DP-"+hashlib.sha256(json.dumps(m,sort_keys=True).encode()).hexdigest()[:24]
        p=DecisionProposal(pid,tuple(kw["inq_ids"]),tuple(kw["resolution_ids"]),
          tuple(kw["resolution_digests"]),tuple(kw["work_product_ids"]),kw["question"],
          tuple(kw["options"]),kw["tradeoffs"],kw["risks"],kw["reversibility"],
          kw["requested_authority"],kw["residual_uncertainty"])
        self.proposals[pid]=p; return p

    def decide(self,pid,signals,rationale,authority):
        if pid not in self.proposals: raise DecisionDenied("unknown proposal")
        if not signals or not rationale or not authority: raise DecisionDenied("missing governance")
        by={s.role:s.signal for s in signals}
        if not {"CEO","CFO","TEAM"}.issubset(by): raise DecisionDenied("missing governance role")
        if any(x not in {"YES","NO","ABSTAIN"} for x in by.values()): raise DecisionDenied("invalid signal")
        if "ABSTAIN" in by.values(): raise DecisionDenied("abstention requires ratified weighting rule")
        if by["CEO"]=="NO": outcome="NO"
        elif by["CEO"]=="YES" and by["CFO"]=="NO" and by["TEAM"]=="NO": outcome="NO"
        elif by["CEO"]=="YES": outcome="YES"
        else: raise DecisionDenied("unratified weighting required")
        did="DEC-"+hashlib.sha256((pid+"|"+outcome+"|"+rationale).encode()).hexdigest()[:24]
        d=DecisionRecord(did,pid,outcome,tuple(signals),rationale,authority)
        self.decisions[did]=d; return d
