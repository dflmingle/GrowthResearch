"""MVP feature query adapter; no duplicated identity-resolution implementation."""
import math
from .common import PURPOSE,Rejected,guard_feature
class GraphAdapter:
    def __init__(self,system):self.s=system
    def extract(self,device,predicted_at,since_at):
        try:
            bundle=self.s.features.compute(device,as_of=predicted_at,since_at=since_at)
            read=self.s.features.read(bundle['bundle_ref'])
        except Rejected as exc:return dict(eligible=False,reason=str(exc),value=None,bundle=None)
        if guard_feature(bundle['as_of'],bundle['consumer_available_at'],predicted_at)!='ALLOW':
            return dict(eligible=False,reason='FUTURE_INFORMATION_BLOCKED',value=None,bundle=bundle)
        active=self.s.graph.active(predicted_at,PURPOSE);byref={(e['id'],e['revision']):e for e in active}
        edges=[byref.get(tuple(ref)) for ref in bundle['lineage']['edge_revisions']]
        if any(e is None or e['quality_kind']=='uncalibrated_score' or e['status']!='ACTIVE' for e in edges):
            return dict(eligible=False,reason='RELATION_QUALITY_NOT_ESTABLISHED',value=None,bundle=bundle)
        # This is task eligibility, not a person graph: a device with multiple
        # known account owners cannot provide account-specific installation value.
        apps={e['src'] for e in edges if e and e['kind']=='installed_on'}
        accounts={e['dst'] for e in active if e['kind']=='logged_in_as' and e['src'] in apps}
        if len(accounts)>1:return dict(eligible=False,reason='SHARED_DEVICE_ACCOUNT_AMBIGUITY',value=None,bundle=bundle)
        if read['values']['observed_ledger_count']==0:return dict(eligible=False,reason='NO_OBSERVED_HISTORICAL_LEDGER',value=None,bundle=bundle)
        if read['values']['currency']!='USD':return dict(eligible=False,reason='CURRENCY_NOT_SUPPORTED',value=None,bundle=bundle)
        amount=read['values']['observed_revenue_micros']
        if amount is None or amount<0:return dict(eligible=False,reason='HISTORY_VALUE_NOT_USABLE',value=None,bundle=bundle)
        return dict(eligible=True,reason='ALLOW_DEVICE_SCOPED_HISTORY_NOT_PERSON_TRUTH',value=math.log1p(amount/1e6),bundle=bundle)
