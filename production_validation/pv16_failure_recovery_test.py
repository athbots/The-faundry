import sys, hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from inq_interface.interface import OBS, OBSInquiryInterface
from inq_core.core import InquiryCore
from dec_core.core import DecisionCore, GovernanceSignal
from dec_core.execution import ExecutionCore

def sig(r,v): return GovernanceSignal(r,v,r)
def denied(fn):
    try: fn(); return False
    except Exception: return True

def main():
    b=OBSInquiryInterface(); o=OBS('OBS-F16-001','ACCEPTED',hashlib.sha256(b'trigger').hexdigest()[:8],'PV16')
    c=b.create_candidate([o],'RELATED',o.evidence_digest,'op','uncertainty')
    iq=InquiryCore(); q=iq.create(c,'PV16 inquiry','resolve failure mode','scope','investigator')
    iq.transition(q.inq_id,'OPEN','TRIAGE_AUTHORITY'); iq.transition(q.inq_id,'INVESTIGATING','TRIAGE_AUTHORITY')
    iq.transition(q.inq_id,'RESOLVED','INVESTIGATION_AUTHORITY','cause established',['OBS-F16-001']); iq.transition(q.inq_id,'CLOSED','CLOSURE_AUTHORITY')
    dc=DecisionCore(); p=dc.create_proposal(inq_ids=(q.inq_id,),resolution_ids=('R',),resolution_digests=('D',),work_product_ids=('W',),question='Proceed?',options=('YES','NO'),tradeoffs='speed/risk',risks='failure',reversibility='rollback',requested_authority='EXECUTIVE_AUTHORITY',residual_uncertainty='bounded')
    d=dc.decide(p.proposal_id,(sig('CEO','YES'),sig('CFO','YES'),sig('TEAM','YES')),'approved','EXECUTIVE_AUTHORITY')
    ec=ExecutionCore(dc.decisions); dd=ec._decision_digest(d)
    assert denied(lambda:b.create_candidate([],'RELATED','x','op','bad'))
    assert denied(lambda:dc.create_proposal(inq_ids=('I',),resolution_ids=(),resolution_digests=(),work_product_ids=('W',),question='x',options=('A','B'),tradeoffs='x',risks='x',reversibility='x',requested_authority='X',residual_uncertainty='x'))
    assert denied(lambda:dc.decide(p.proposal_id,(sig('CEO','YES'),sig('CFO','ABSTAIN'),sig('TEAM','YES')),'x','X'))
    assert denied(lambda:ec.authorize(d.decision_id,'WRONG','scope','exec','EXECUTION_AUTHORITY','start','stop','expected','verify','rollback'))
    assert denied(lambda:ec.authorize(d.decision_id,dd,'scope','exec','EXECUTION_AUTHORITY','start','','expected','verify','rollback'))
    a=ec.authorize(d.decision_id,dd,'scope-A','exec-A','EXECUTION_AUTHORITY','start-A','abort','expected-A','verify-A','rollback-A'); e=ec.start(a.authorization_id)
    ec.abort(e.execution_id,'threshold exceeded','OBS-F16-FAIL','EXECUTION_AUTHORITY'); assert e.state=='ABORTED'
    assert denied(lambda:ec.verify(e.execution_id,['OBS-F16-FAIL'],'success','VERIFICATION_AUTHORITY'))
    a2=ec.authorize(d.decision_id,dd,'scope-B','exec-B','EXECUTION_AUTHORITY','start-B','stop-B','expected-B','verify-B','rollback-B'); e2=ec.start(a2.authorization_id)
    assert denied(lambda:ec.verify(e2.execution_id,[],'success','VERIFICATION_AUTHORITY'))
    assert denied(lambda:ec.verify(e2.execution_id,['OBS-F16-OUT'],'success','EXECUTION_AUTHORITY'))
    outcome=OBS('OBS-F16-RECOVERY','ACCEPTED',hashlib.sha256(b'recovery').hexdigest()[:8],'RECOVERY')
    ec.verify(e2.execution_id,[outcome.obs_id],'recovery verified','VERIFICATION_AUTHORITY')
    assert e2.state=='VERIFIED' and d.outcome=='YES' and e.execution_id in ec.executions
    print('PASS | PV-16 cross-layer failure and recovery')
    print('SUMMARY | 12/12 failure-recovery invariants PASS')
main()
