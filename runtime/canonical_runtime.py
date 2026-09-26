from canonical_obs.state_machine import CanonicalOBS
from canonical_obs.authority import AuthorityService
from canonical_obs.semantic_relation import rel
from runtime.control_boundary import ChangeControl, MigrationControl

class CanonicalRuntime:
    def __init__(self, control_boundary=None, control_authorizer=None):
        self.authority=AuthorityService()
        self.capture=self.authority.issue("capture","OBS_CAPTURE")
        self.validator=self.authority.issue("validator","OBS_VALIDATOR")
        self.engine=self.authority.issue("triage-engine","TRIAGE_ENGINE")
        self.policy=self.authority.issue("triage-policy","TRIAGE_POLICY")
        self.history=self.authority.issue("history","HISTORY_ENGINE")
        self.change_control=None
        self.migration_control=None
        if control_boundary is not None:
            if control_authorizer is None:
                raise ValueError("control_authorizer is required with a control boundary")
            self.change_control=ChangeControl(control_boundary, control_authorizer)
            self.migration_control=MigrationControl(control_boundary, control_authorizer)

    def create_obs(self, source, raw_payload):
        return CanonicalOBS(source,raw_payload)

    def validate(self,obs,valid=True):
        obs.transition("VALIDATING","capture envelope accepted",self.capture,self.authority)
        if not valid:
            obs.transition("SUPPRESSED","validation failed",self.validator,self.authority)
            return obs
        obs.transition("ACCEPTED","schema/provenance validation passed",self.validator,self.authority)
        return obs

    def triage(self,obs,decision):
        if obs.state=="ACCEPTED":
            obs.transition("TRIAGE","triage initiated",self.engine,self.authority)
        elif obs.state!="TRIAGE":
            raise ValueError("OBS must be ACCEPTED or TRIAGE")
        obs.transition(decision,"triage policy decision",self.policy,self.authority)
        return obs

    def close(self,obs):
        if obs.state not in {"MERGED","SUPPRESSED","GRADUATED_TO_INQ"}:
            raise ValueError("only terminal outcome states can become HISTORICAL")
        obs.transition("HISTORICAL","terminal outcome preserved",self.history,self.authority)
        return obs

    def compare(self,a,b): return rel(a,b)
