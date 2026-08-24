from dataclasses import dataclass, field
from uuid import uuid4
from copy import deepcopy
from .authority import AuthorityService, Capability

T={
"RAW":{"VALIDATING"},
"VALIDATING":{"ACCEPTED","SUPPRESSED"},
"ACCEPTED":{"TRIAGE"},
"TRIAGE":{"CLUSTERED","MERGED","SUPPRESSED","GRADUATED_TO_INQ"},
"CLUSTERED":{"TRIAGE"},
"MERGED":{"HISTORICAL"},
"SUPPRESSED":{"HISTORICAL"},
"GRADUATED_TO_INQ":{"HISTORICAL"},
"HISTORICAL":set()
}
_IMMUTABLE={"object_id","source","raw_payload"}

@dataclass
class CanonicalOBS:
    source: str
    raw_payload: object
    state: str="RAW"
    object_id: str=field(default_factory=lambda:str(uuid4()))
    history: list=field(default_factory=list)
    _sealed: bool=field(default=False,init=False,repr=False)

    def __post_init__(self):
        object.__setattr__(self,"source",deepcopy(self.source))
        object.__setattr__(self,"raw_payload",deepcopy(self.raw_payload))
        object.__setattr__(self,"_sealed",True)

    def __setattr__(self,name,value):
        if getattr(self,"_sealed",False) and name in _IMMUTABLE:
            raise AttributeError(f"{name} is immutable")
        object.__setattr__(self,name,value)

    def transition(self,target,reason,capability,authority_service):
        if not isinstance(authority_service, AuthorityService):
            raise TypeError("transition requires AuthorityService")
        authority_service.require(capability,target)
        if target not in T[self.state]:
            raise ValueError(f"forbidden transition {self.state}->{target}")
        self.history.append({
            "from":self.state,"to":target,"reason":reason,
            "actor":capability.actor,"capability":capability.capability
        })
        object.__setattr__(self,"state",target)
