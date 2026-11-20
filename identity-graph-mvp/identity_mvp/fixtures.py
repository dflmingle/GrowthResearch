"""Seeded local fixture generator. Public key; never use for real authentication."""
import hashlib,hmac,json,random
from .system import IdentitySystem,ManualClock,PURPOSE,canonical
class SyntheticWorld:
    def __init__(self,directory,seed=760078):
        self.seed=seed;self.rng=random.Random(seed);self.key=hashlib.sha256(f'public-fixture-{seed}'.encode()).digest()
        self.system=IdentitySystem(directory,clock=ManualClock(),fixture_key=self.key)
        self.entities={};self.counter=0;self.start=self.system.clock.now
    def entity(self,name,kind,*,app='synthetic-app-a',issuer='synthetic:first-party',sector='first-party',scope='first-party-organization',token=None):
        ns=self.system.namespaces.register(tenant='synthetic-tenant',issuer=issuer,app=app,sector=sector,entity_type=kind,scope=scope)
        eid=self.system.namespaces.create(ns,token or f'syn:{name}:{self.rng.getrandbits(48):012x}')
        self.system.policy.set(eid,PURPOSE,True);self.entities[name]=eid;return eid
    def install(self,name,device,*,app='synthetic-app-a'):
        aid=self.entity(name,'app_instance',app=app)
        self.system.graph.add(aid,device,'installed_on',source_ref='synth:install')
        return aid
    def assertion(self,account,app_instance,device,**changes):
        self.counter+=1;s=self.system
        an=s.store.db.execute('SELECT n.* FROM namespaces n JOIN entities e ON n.id=e.namespace_id WHERE e.id=?',(account,)).fetchone()
        pn=s.store.db.execute('SELECT n.* FROM namespaces n JOIN entities e ON n.id=e.namespace_id WHERE e.id=?',(app_instance,)).fetchone()
        assertion=dict(issuer=an['issuer'],audience=pn['app'],account=account,app_instance=app_instance,device=device,
            nonce=f'synth:nonce:{self.seed}:{self.counter}',issued_at=s.clock.now,expires_at=s.clock.now+60,purpose=PURPOSE,source_ref='synth:fixture-auth')
        assertion.update(changes);signature=hmac.new(self.key,canonical(assertion).encode(),hashlib.sha256).hexdigest()
        return assertion,signature
    def login(self,account,app_instance,device,**changes):return self.system.resolver.login(*self.assertion(account,app_instance,device,**changes))
    def revenue(self,app,amount,*,account=None,event_id=None,economic_key=None,**kw):
        self.counter+=1
        return self.system.events.ingest(app=app,source_name='synth:revenue-source',event_id=event_id or f'synth:event:{self.counter}',event_type='revenue',
            occurred_at=kw.pop('occurred_at',self.system.clock.now),account=account,amount_micros=amount,
            economic_key=economic_key or f'synth:economic:{self.counter}',economic_kind=kw.pop('economic_kind','IAP'),**kw)
    def pair(self):
        d=self.entity('device-a','device');a=self.install('app-a',d);account=self.entity('account-a','account');self.login(account,a,d)
        return d,a,account
    def manifest(self):return dict(seed=self.seed,environment='LOCAL_SYNTHETIC_ONLY',start_utc_epoch=self.start,entities=self.entities)
    def close(self):self.system.close()
