from dataclasses import dataclass
import secrets

class AuthorizationDenied(Exception):
    pass

CAPABILITIES = {
    "OBS_CAPTURE": {"VALIDATING"},
    "OBS_VALIDATOR": {"ACCEPTED", "SUPPRESSED"},
    "TRIAGE_ENGINE": {"TRIAGE"},
    "TRIAGE_POLICY": {"CLUSTERED", "MERGED", "SUPPRESSED", "GRADUATED_TO_INQ"},
    "HISTORY_ENGINE": {"HISTORICAL"},
}

@dataclass(frozen=True)
class Capability:
    _token: str
    actor: str
    capability: str

class AuthorityService:
    def __init__(self):
        self._tokens = {}

    def issue(self, actor, capability):
        if capability not in CAPABILITIES:
            raise AuthorizationDenied("unknown capability")
        token=secrets.token_urlsafe(32)
        cap=Capability(token,actor,capability)
        self._tokens[token]=cap
        return cap

    def require(self, capability, target):
        if not isinstance(capability, Capability):
            raise AuthorizationDenied("transition requires issued capability")
        issued=self._tokens.get(capability._token)
        if issued is not capability:
            raise AuthorizationDenied("capability was not issued by AuthorityService")
        if target not in CAPABILITIES.get(capability.capability,set()):
            raise AuthorizationDenied(
                f"{capability.actor} with {capability.capability} cannot perform {target}"
            )
