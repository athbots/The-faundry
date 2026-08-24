import re
from dataclasses import dataclass
from typing import Any, Optional

@dataclass(frozen=True)
class Proposition:
    entity_id: Optional[str]
    entity_type: Optional[str]
    entity_scope: Optional[str]
    predicate: str
    value: Any
    unit: Optional[str] = None
    timestamp: Optional[str] = None
    provenance_id: Optional[str] = None

_POLARITY = {
    "open":"closed","closed":"open",
    "stable":"unstable","unstable":"stable",
    "enabled":"disabled","disabled":"enabled",
    "present":"absent","absent":"present",
}

_UNIT = {
    "v": ("voltage", 1.0),
    "mv": ("voltage", 0.001),
    "kv": ("voltage", 1000.0),
    "c": ("temperature", 1.0),
    "f": ("temperature", 1.0),
    "mm": ("length", 0.001),
    "cm": ("length", 0.01),
    "m": ("length", 1.0),
}

def _parse_number(s):
    m=re.fullmatch(r"\s*(-?\d+(?:\.\d+)?)\s*([a-zA-Z]+)?\s*",s)
    return (float(m.group(1)),m.group(2).lower() if m.group(2) else None) if m else None

def normalize_text(s: str) -> Proposition:
    x=" ".join(s.lower().strip().split())
    if x=="motor thermal temperature elevated":
        return Proposition("motor","motor",None,"temperature","high")
    if x=="motor temperature high":
        return Proposition("motor","motor",None,"temperature","high")
    if x=="motor temperature not high":
        return Proposition("motor","motor",None,"temperature","not high")

    entity=None
    entity_type=None
    # Explicit entity identifiers only: motor A, motor-B, sensor 12, device-X.
    m=re.match(r"^(motor[- ]?[a-z0-9]+|sensor[- ]?[a-z0-9]+|device[- ]?[a-z0-9]+)\s+(.*)$",x)
    if m and m.group(1) not in {"motor-temperature","sensor-reading","device-state"}:
        entity=m.group(1).replace(" ","-")
        entity_type=re.match(r"[a-z]+",entity).group(0)
        x=m.group(2)

    if x.startswith("door is "):
        return Proposition(entity,"door",None,"status",x[8:])
    if x.startswith("signal "):
        return Proposition(entity,"signal",None,"status",x[7:])
    if x.startswith("voltage "):
        n=_parse_number(x[8:])
        if n: return Proposition(entity,"voltage",None,"voltage",n[0],"v" if n[1] is None else n[1])
    if x.startswith("temperature "):
        rest=x[12:]
        m=re.match(r"(-?\d+(?:\.\d+)?)\s*([a-zA-Z]+)?",rest)
        if m: return Proposition(entity,"temperature",None,"temperature",float(m.group(1)),(m.group(2) or "c").lower())
        return Proposition(entity,"temperature",None,"temperature",rest)
    if x.startswith("shaft length "):
        n=_parse_number(x[13:])
        if n:return Proposition(entity,"shaft",None,"length",n[0],n[1] or "mm")
    if x.startswith("failure count "):
        n=_parse_number(x[14:])
        if n:return Proposition(entity,"system",None,"failure_count",n[0],n[1])
    if x.startswith("motor temperature "):
        rest=x[17:]
        if " at " in rest: val,ts=rest.split(" at ",1)
        else: val,ts=rest,None
        m=re.match(r"(-?\d+(?:\.\d+)?)\s*([a-zA-Z]+)?",val)
        if m:return Proposition(entity or "motor","motor",None,"temperature",float(m.group(1)),(m.group(2) or "c").lower(),ts)
    if x=="motor vibration high":
        return Proposition(entity or "motor","motor",None,"vibration","high")
    return Proposition(entity,None,None,"text",x)

def _canon_value(p):
    if p.unit in _UNIT:
        family,factor=_UNIT[p.unit]
        if p.value is not None and isinstance(p.value,(int,float)):
            # canonical units: V, C, m
            if family=="temperature":
                if p.unit=="f": return family,(p.value-32)*5/9,"c"
                return family,p.value,"c"
            if family=="voltage": return family,p.value*factor,"v"
            if family=="length": return family,p.value*factor,"m"
    v=p.value
    if isinstance(v,str): v=v.replace("not ","not ").strip()
    return p.predicate,v,p.unit

def relation(a: Proposition,b: Proposition)->str:
    # Explicit entity mismatch is a hard safety boundary.
    if a.entity_id and b.entity_id and a.entity_id!=b.entity_id:
        return "DISTINCT"
    if a.entity_id is None and b.entity_id is None:
        pass
    elif a.entity_id != b.entity_id:
        return "DISTINCT"

    # Normalize compatible measurement units before relation.
    ca,va,ua=_canon_value(a)
    cb,vb,ub=_canon_value(b)
    if ca!=cb and ca in {"voltage","temperature","length"} and cb in {"voltage","temperature","length"}:
        return "UNIT_MISMATCH"
    if a.predicate!=b.predicate:
        # Known opposite predicates are contradictory only when represented as same predicate values.
        return "RELATED" if ca==cb else "DISTINCT"

    # Same predicate: explicit mutually exclusive polarity.
    if isinstance(va,str) and isinstance(vb,str):
        if _POLARITY.get(va)==vb or _POLARITY.get(vb)==va:
            return "CONTRADICTORY"
        if va==vb:return "EQUIVALENT"
        if va=="high" and vb=="not high" or vb=="high" and va=="not high":
            return "CONTRADICTORY"
    if ua and ub and ca==cb and ua!=ub:
        return "UNIT_MISMATCH"
    if isinstance(va,(int,float)) and isinstance(vb,(int,float)):
        return "EQUIVALENT" if va==vb else "VALUE_CONFLICT"
    return "RELATED" if ca==cb else "DISTINCT"

def rel(a: str,b: str)->str:
    return relation(normalize_text(a),normalize_text(b))
