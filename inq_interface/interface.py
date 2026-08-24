from dataclasses import dataclass
import hashlib, json

ALLOWED = {"EQUIVALENT","RELATED","CONTRADICTORY","VALUE_CONFLICT"}
BLOCKED = {"DISTINCT","UNIT_MISMATCH"}

class InterfaceDenied(Exception):
    pass

@dataclass(frozen=True)
class OBS:
    obs_id: str
    state: str
    evidence_digest: str
    provenance: str

@dataclass(frozen=True)
class InquiryCandidate:
    candidate_id: str
    observation_ids: tuple
    evidence_digest: str
    semantic_relation: str
    provenance: str
    reason: str
    requested_by: str
    schema_version: str
    state: str = "CANDIDATE"

class OBSInquiryInterface:
    ELIGIBLE = {"ACCEPTED","MERGED","SUPPRESSED"}

    def __init__(self):
        self.candidates = {}
        self.events = []

    def _id(self, ids, relation, digest, schema):
        material=json.dumps({
            "ids":list(ids),"relation":relation,
            "digest":digest,"schema":schema
        },sort_keys=True,separators=(",",":")).encode()
        return "INQC-"+hashlib.sha256(material).hexdigest()[:24]

    def create_candidate(self, observations, semantic_relation, evidence_digest,
                         requested_by, reason, schema_version="FS-INQ-001:v1"):
        if not observations:
            raise InterfaceDenied("no observations")
        if any(o.state not in self.ELIGIBLE for o in observations):
            raise InterfaceDenied("ineligible OBS state")
        if not evidence_digest or any(not o.provenance for o in observations):
            raise InterfaceDenied("missing evidence/provenance")
        if semantic_relation in BLOCKED or semantic_relation not in ALLOWED:
            raise InterfaceDenied("semantic relation not eligible")
        if not requested_by:
            raise InterfaceDenied("missing requester")
        if not reason:
            raise InterfaceDenied("missing reason")

        expected="|".join(sorted(o.evidence_digest for o in observations))
        if evidence_digest != expected:
            raise InterfaceDenied("evidence digest mismatch")

        ids=tuple(sorted(o.obs_id for o in observations))
        cid=self._id(ids,semantic_relation,evidence_digest,schema_version)

        if cid in self.candidates:
            return self.candidates[cid]

        c=InquiryCandidate(cid,ids,evidence_digest,semantic_relation,
                           "|".join(sorted(set(o.provenance for o in observations))),
                           reason,requested_by,schema_version)
        self.candidates[cid]=c
        self.events.append({
            "event":"INQUIRY_CANDIDATE_CREATED",
            "candidate_id":cid,
            "observation_ids":ids,
            "semantic_relation":semantic_relation,
            "schema_version":schema_version
        })
        return c

    def graduate(self, candidate_id, authority):
        if candidate_id not in self.candidates:
            raise InterfaceDenied("unknown candidate")
        if authority != "TRIAGE_AUTHORITY":
            raise InterfaceDenied("graduation authority denied")
        self.events.append({
            "event":"INQUIRY_GRADUATED",
            "candidate_id":candidate_id,
            "authority":authority
        })
        return {"candidate_id":candidate_id,"state":"INQ","authority":authority}
