"""E01 fixtures built exclusively through the original synthetic MVP APIs."""
from common import SyntheticWorld, SEED, PURPOSE, ENV

class Scenario:
    def __init__(self, directory, *, source_amount=7_000_000, source_coverage='COMPLETE', expiry=False):
        self.w = w = SyntheticWorld(directory, seed=SEED)
        self.s = s = w.system
        self.calls = []
        self.d1 = w.entity('D1', 'device')
        self.d2 = w.entity('D2', 'device')
        self.a = w.entity('A', 'account', token='syn:account:A')
        self.b = w.entity('B', 'account', token='syn:account:B')
        self.xa = w.install('X_A', self.d1, app='synthetic-X')
        self.xb = w.install('X_B', self.d1, app='synthetic-X')
        self.y = w.install('Y_A', self.d2, app='synthetic-Y')
        self.login_refs = {}
        self.receipts = {}
        for name, account, app, device in [('xa',self.a,self.xa,self.d1),('xb',self.b,self.xb,self.d1),('y',self.a,self.y,self.d2)]:
            assertion, signature = w.assertion(account, app, device)
            result = s.resolver.login(assertion, signature)
            self.calls.append(dict(api='resolver.login', input=dict(assertion=assertion,signature=signature), actual=result))
            self.login_refs[name] = result['edge_ref']
            self.receipts[name] = assertion['nonce']
        if expiry:
            s.graph.revoke(self.login_refs['xa'])
            result=s.graph.add(self.xa,self.a,'logged_in_as',source_ref='synth:expiring-login',
                valid_to=w.start+5,quality_kind='authenticated_account_control',auth_receipt=self.receipts['xa'])
            self.login_refs['xa']=result['edge_ref']
            self.calls.append(dict(api='graph.add', input=dict(valid_to=w.start+5,auth_receipt=self.receipts['xa']),actual=result))
        for app, account, amount in [(self.xa,self.a,source_amount),(self.xb,self.b,99_000_000),(self.y,self.a,3_000_000)]:
            if amount is not None:
                result=w.revenue(app, amount, account=account)
                self.calls.append(dict(api='fixture.revenue',input=dict(app=app,account=account,amount_micros=amount),actual=result))
        for app in [self.xa,self.xb,self.y]:
            status=source_coverage if app==self.xa else 'COMPLETE'
            result=s.events.coverage(app,start_at=w.start,end_at=w.start,status=status)
            self.calls.append(dict(api='events.coverage',input=dict(app=app,start_at=w.start,end_at=w.start,status=status),actual=result))

    def request(self, **changes):
        result=dict(task_ref='synth:task:E01:A:Y',target_install_ref=self.y,subject_type='account',
            auth_receipt=self.receipts['y'],prediction_at=self.s.clock.now,since_at=self.w.start,
            purpose=PURPOSE,authorization_context=dict(environment=ENV,purpose=PURPOSE,source_app_allowlist=['synthetic-X']))
        result.update(changes)
        return result

    def manifest(self):
        return dict(fixture=self.w.manifest(),calls=self.calls,login_refs=self.login_refs,receipts=self.receipts,
                    shared_device_accounts=[self.a,self.b],source_app='synthetic-X',target_app='synthetic-Y')

    def close(self):self.w.close()
