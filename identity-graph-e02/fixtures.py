"""Original resolver / events / outbox / privacy authority, synthetic only."""
from e02_common import SyntheticWorld, SEED, PURPOSE, ENV

class Fixture:
    def __init__(self,directory,*,expires=False,scheduled_revoke=False):
        self.w=w=SyntheticWorld(directory,seed=SEED);self.s=s=w.system;self.input_log=[]
        self.device=w.entity('D1','device')
        self.account=w.entity('A','account')
        self.app=w.install('X',self.device,app='synthetic-X')
        assertion,signature=w.assertion(self.account,self.app,self.device)
        login=s.resolver.login(assertion,signature)
        self.auth_receipt=assertion['nonce'];self.login_edge=login['edge_ref']
        self.input_log.append(dict(api='resolver.login',input=dict(assertion=assertion,signature=signature),actual=login))
        if expires:
            s.graph.revoke(self.login_edge)
            x=s.graph.add(self.app,self.account,'logged_in_as',source_ref='synth:expiring-login',valid_to=w.start+5,
                quality_kind='authenticated_account_control',auth_receipt=self.auth_receipt)
            self.login_edge=x['edge_ref'];self.input_log.append(dict(api='graph.add',valid_to=w.start+5,actual=x))
        if scheduled_revoke:
            s.policy.set(self.account,PURPOSE,False,effective_at=w.start+5)
            self.input_log.append(dict(api='policy.set',entity=self.account,allowed=False,effective_at=w.start+5))
        self.revenue=w.revenue(self.app,7_000_000,account=self.account,event_id='synth:e02:event:1',economic_key='synth:e02:economic:1')
        self.input_log.append(dict(api='fixture.revenue',app=self.app,account=self.account,amount_micros=7_000_000,actual=self.revenue))
        self.outbox=dict(s.store.db.execute('SELECT * FROM outbox WHERE event_ref=?',(self.revenue['event_ref'],)).fetchone())
        self.request=dict(task_ref='synth:task:E02:A:X',target_install_ref=self.app,subject_type='account',
            auth_receipt=self.auth_receipt,prediction_at=s.clock.now,since_at=w.start,purpose=PURPOSE,
            authorization_context=dict(environment=ENV,purpose=PURPOSE,source_app_allowlist=['synthetic-X']))

    def manifest(self):return dict(seed=SEED,world=self.w.manifest(),input_log=self.input_log,request=self.request,
        outbox=self.outbox,device=self.device,account=self.account,app=self.app,login_edge=self.login_edge,revenue=self.revenue)
    def close(self):self.w.close()
