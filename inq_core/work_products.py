from dataclasses import dataclass
import hashlib, json

CLASSES={"OBSERVATION","EXPERIMENT","ANALYSIS","SIMULATION","REVIEW","DECISION_EVIDENCE"}

class WorkProductDenied(Exception): pass

@dataclass(frozen=True)
class WorkProduct:
    work_product_id:str
    inq_id:str
    wp_class:str
    title:str
    purpose:str
    inputs:tuple
    outputs:tuple
    actor:str
    authority:str
    method:str
    method_version:str
    created_at:str
    result:str
    limitations:str
    provenance:str
    schema_version:str="FS-INQ-004:v1"
    supersedes:str|None=None

class WorkProductStore:
    def __init__(self):
        self.items={}

    def create(self, *, inq_id, wp_class, title, purpose, inputs, outputs,
               actor, authority, method, method_version, created_at,
               result, limitations, provenance, supersedes=None):
        if wp_class not in CLASSES: raise WorkProductDenied("invalid class")
        required=[inq_id,title,purpose,actor,authority,method,method_version,
                  created_at,result,limitations,provenance]
        if any(x is None or x=="" for x in required):
            raise WorkProductDenied("missing mandatory provenance")
        if not inputs: raise WorkProductDenied("inputs required")
        if wp_class=="REVIEW":
            if len(inputs)!=1: raise WorkProductDenied("review must identify one reviewed work product")
            reviewed=self.items.get(inputs[0])
            if reviewed is None: raise WorkProductDenied("reviewed work product must exist")
            if reviewed.actor==actor: raise WorkProductDenied("reviewer cannot review own artifact")
        material={
            "inq_id":inq_id,"class":wp_class,"title":title,"purpose":purpose,
            "inputs":list(inputs),"outputs":list(outputs),"actor":actor,
            "method":method,"method_version":method_version,"created_at":created_at,
            "result":result,"limitations":limitations,"provenance":provenance,
            "supersedes":supersedes
        }
        wid="WP-"+hashlib.sha256(json.dumps(material,sort_keys=True).encode()).hexdigest()[:24]
        if wid in self.items: return self.items[wid]
        wp=WorkProduct(wid,inq_id,wp_class,title,purpose,tuple(inputs),tuple(outputs),
                       actor,authority,method,method_version,created_at,result,
                       limitations,provenance,supersedes=supersedes)
        self.items[wid]=wp
        return wp
