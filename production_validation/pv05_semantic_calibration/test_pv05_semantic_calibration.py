import sys,csv
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from canonical_obs.semantic_relation import rel

p=Path(__file__).with_name("PV05-adversarial-corpus.csv")
rows=list(csv.DictReader(p.open(encoding="utf8")))
results=[]
for r in rows:
    got=rel(r["a"],r["b"])
    ok=got==r["expected"]
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'} | {r['id']} | {r['class']} | got={got} | expected={r['expected']}")

assert all(results), f"{sum(results)}/{len(results)} semantic cases passed"

# Safety gate: contradiction/incompatibility must not collapse into equivalence.
for r in rows:
    if r["expected"] in {"CONTRADICTORY","UNIT_MISMATCH","VALUE_CONFLICT"}:
        assert rel(r["a"],r["b"]) != "EQUIVALENT"

print(f"SUMMARY | PV05 semantic calibration | {sum(results)}/{len(results)} PASS")
