from canonical_obs.state_machine import CanonicalOBS

class GraduationDenied(Exception):
    pass

class GraduationAuthority:
    def __init__(self, authorized_actors=None):
        self.authorized_actors=set(authorized_actors or {"TRIAGE_POLICY"})
        self.graduated=set()

    def graduate(self, obs, actor, materiality, inquiry_id):
        if actor not in self.authorized_actors:
            raise GraduationDenied("actor lacks INQ graduation authority")
        if obs.state != "TRIAGE":
            raise GraduationDenied("OBS must be in TRIAGE")
        if not materiality:
            raise GraduationDenied("materiality requirement not satisfied")
        if not inquiry_id:
            raise GraduationDenied("graduation requires target INQ identity")
        if obs.object_id in self.graduated:
            raise GraduationDenied("OBS already graduated")
        obs.transition(
            "GRADUATED_TO_INQ",
            f"graduated to {inquiry_id}",
            actor
        )
        self.graduated.add(obs.object_id)
        return obs
