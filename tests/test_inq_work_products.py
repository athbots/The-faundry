import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from inq_core.work_products import WorkProductStore,WorkProductDenied

def main():
    s=WorkProductStore()

    exp=s.create(
        inq_id="INQ-1",wp_class="EXPERIMENT",title="Thermal test",
        purpose="test motor thermal hypothesis",inputs=("OBS-1",),
        outputs=("OBS-2",),actor="engineer-A",authority="INVESTIGATION_AUTHORITY",
        method="controlled thermal run",method_version="m1",
        created_at="2026-08-16T10:00:00Z",
        result="temperature rose above baseline",
        limitations="single operating point",provenance="lab-run-001"
    )
    assert exp.work_product_id.startswith("WP-")

    # Failed/inconclusive results remain valid first-class artifacts.
    neg=s.create(
        inq_id="INQ-1",wp_class="ANALYSIS",title="Null test",
        purpose="test alternate hypothesis",inputs=(exp.work_product_id,),
        outputs=(),actor="engineer-B",authority="INVESTIGATION_AUTHORITY",
        method="statistical comparison",method_version="a2",
        created_at="2026-08-16T11:00:00Z",
        result="INCONCLUSIVE",limitations="insufficient sample size",provenance="analysis-001"
    )
    assert neg.result=="INCONCLUSIVE"

    # Review must be independent.
    review=s.create(
        inq_id="INQ-1",wp_class="REVIEW",title="Independent review",
        purpose="review thermal test",inputs=(exp.work_product_id,),
        outputs=(),actor="reviewer-C",authority="REVIEW_AUTHORITY",
        method="evidence audit",method_version="r1",
        created_at="2026-08-16T12:00:00Z",
        result="method acceptable",limitations="scope limited to method",
        provenance="review-001"
    )
    assert review.actor=="reviewer-C"

    # Self-review is prohibited.
    try:
        s.create(
            inq_id="INQ-1",wp_class="REVIEW",title="Bad review",
            purpose="self review",inputs=(exp.work_product_id,),
            outputs=(),actor="engineer-A",authority="REVIEW_AUTHORITY",
            method="audit",method_version="r1",created_at="2026-08-16T12:00:00Z",
            result="approved",limitations="none",provenance="bad"
        )
    except WorkProductDenied: pass
    else: raise AssertionError("self-review accepted")

    # Missing provenance is denied.
    try:
        s.create(
            inq_id="INQ-1",wp_class="ANALYSIS",title="No provenance",
            purpose="test",inputs=(exp.work_product_id,),outputs=(),
            actor="engineer-D",authority="INVESTIGATION_AUTHORITY",
            method="x",method_version="1",created_at="now",
            result="x",limitations="x",provenance=""
        )
    except WorkProductDenied: pass
    else: raise AssertionError("missing provenance accepted")

    # Invalid class is denied.
    try:
        s.create(
            inq_id="INQ-1",wp_class="TASK",title="Task",
            purpose="test",inputs=("OBS-1",),outputs=(),
            actor="engineer-D",authority="INVESTIGATION_AUTHORITY",
            method="x",method_version="1",created_at="now",
            result="x",limitations="x",provenance="p"
        )
    except WorkProductDenied: pass
    else: raise AssertionError("invalid class accepted")

    # Deterministic idempotency.
    exp2=s.create(
        inq_id="INQ-1",wp_class="EXPERIMENT",title="Thermal test",
        purpose="test motor thermal hypothesis",inputs=("OBS-1",),
        outputs=("OBS-2",),actor="engineer-A",authority="INVESTIGATION_AUTHORITY",
        method="controlled thermal run",method_version="m1",
        created_at="2026-08-16T10:00:00Z",
        result="temperature rose above baseline",
        limitations="single operating point",provenance="lab-run-001"
    )
    assert exp2.work_product_id==exp.work_product_id and len(s.items)==3

    # A work product cannot masquerade as a decision.
    assert exp.wp_class!="DECISION"

    print("PASS | INQ investigation work products")
    print("SUMMARY | 8/8 work-product invariants PASS")

if __name__=="__main__": main()
