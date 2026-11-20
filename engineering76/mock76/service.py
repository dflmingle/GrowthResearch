"""Deterministic local evidence-chain mock. All IDs are generated fixture labels."""
import argparse,random
from .io import Ledger,read,write,digest
from .safety import install,mock_key

PURPOSE='mock-research'

class Service:
    def __init__(self,root):
        from pathlib import Path
        self.root=Path(root);self.path=self.root/'private/service_state.json';self.log=Ledger(self.root/'audit/ledger.jsonl')
        self.s=read(self.path) if self.path.exists() else None
    def flush(self):write(self.path,self.s)
    def record(self,kind,**data):return self.log.append(kind,self.s['clock'],**data)
    def clock(self,t):
        if type(t) is not int or t<self.s['clock']:raise ValueError('Logical clock cannot go backwards')
        self.s['clock']=t
    def init(self,route,seed):
        if self.s is not None:raise ValueError('Run exists')
        if route not in ['D0','D1','LEAK']:raise ValueError('Unknown fixture route')
        self.s=dict(clock=0,route=route,seed=seed,permissions=[],events=[],epoch={},seen=[],requests=[])
        self.record('run_open',environment='offline-mock',seed=seed,namespace='mock76',no_network=True,
                    model_version='mock-model-v1',aggregate_version='frozen-v1',inventory_version='fixed-v1')
        self.flush();return dict(ok=True)
    def gate(self,app,device,t):
        matches=[p for p in self.s['permissions'] if p['app']==app and p['device']==device and p['effective_at']<=t]
        return bool(matches and max(matches,key=lambda p:(p['effective_at'],p['version']))['allow'])
    def permit(self,app,device,allow,effective_at):
        mock_key(device)
        if app not in ['source-app','target-app'] or type(allow) is not bool or type(effective_at) is not int or effective_at<self.s['clock']:raise ValueError('No retroactive or foreign permission')
        p=dict(app=app,device=device,allow=allow,effective_at=effective_at,purpose=PURPOSE,version=len(self.s['permissions'])+1)
        self.s['permissions'].append(p);self.record('permission_changed',**p);return dict(ok=True)
    def collect(self,event):
        required={'event_id','device','installation','event_time','available_at','category','purpose','epoch'}
        if set(event)!=required or any(type(event[k]) is not int for k in ['event_time','available_at','epoch','category']) or event['category'] not in [0,1]:raise ValueError('Invalid source-event schema')
        for k in ['device','installation','event_id']:mock_key(event[k])
        if event['purpose']!=PURPOSE:raise ValueError('Foreign purpose')
        eid=event['event_id'];now=self.s['clock'];device=event['device']
        if eid in self.s['seen']:
            self.record('event_deduplicated',event_id=eid);return dict(status='DUPLICATE')
        if not (0<=event['event_time']<=now<=event['available_at']):
            self.record('event_rejected',event_id=eid,reason='INVALID_TIME');return dict(status='INVALID_TIME')
        if event['epoch']!=self.s['epoch'].get(device,0):
            self.record('event_rejected',event_id=eid,reason='STALE_EPOCH');return dict(status='STALE_EPOCH')
        if not self.gate('source-app',device,event['event_time']) or not self.gate('source-app',device,now):
            self.record('event_rejected',event_id=eid,reason='SOURCE_COLLECTION_DENIED');return dict(status='DENIED')
        self.s['seen'].append(eid)
        seq=self.record('event_received',event_id=eid,source_app='source-app',device=device,installation=event['installation'],
                        event_time=event['event_time'],received_at=now,available_at=event['available_at'],category=event['category'],epoch=event['epoch'],purpose=PURPOSE)
        self.s['events'].append(dict(event,receipt=seq));return dict(status='RECEIVED',receipt=seq)
    def usable(self,device):
        if not self.gate('source-app',device,self.s['clock']) or not self.gate('target-app',device,self.s['clock']):return None,'PURPOSE_DENIED'
        valid=[e for e in self.s['events'] if e['device']==device and e['epoch']==self.s['epoch'].get(device,0) and e['available_at']<=self.s['clock']]
        if not valid:return None,'NO_AVAILABLE_HISTORY'
        return max(valid,key=lambda e:(e['event_time'],e['receipt'])),None
    def bridge(self,device):
        e,reason=self.usable(device)
        if reason:
            self.record('bridge_denied',device=device,reason=reason);return dict(status=reason)
        seq=self.record('context_bridge',event_receipt=e['receipt'],device=device,category=e['category'],purpose=PURPOSE,
                        source_app='source-app',destination='target-current-context',source_available_at=e['available_at'])
        return dict(category=e['category'],bridge_receipt=seq,purpose=PURPOSE,device=device,epoch=e['epoch'],valid_at=self.s['clock'])
    def predict(self,q):
        device=mock_key(q['device']);rid=mock_key(q['request_id'])
        if rid in self.s['requests']:raise ValueError('Request ID reuse rejected')
        if q['prediction_time']!=self.s['clock'] or q['purpose']!=PURPOSE:raise ValueError('Prediction time/purpose mismatch')
        if q['epoch']!=self.s['epoch'].get(device,0):raise ValueError('Target epoch stale')
        allowed={'country','model','placement','source_category','bridge_receipt'}
        mock_key(q['installation'])
        if set(q['context'])-allowed or any(q['context'].get(k)!=v for k,v in dict(country='MOCK',model='mock-device',placement='mock-slot').items()):raise ValueError('Unexpected target context')
        permitted=self.gate('target-app',device,self.s['clock']) and self.gate('source-app',device,self.s['clock'])
        if not permitted and ('source_category' in q['context'] or 'bridge_receipt' in q['context']):
            # Drop unauthorized contextual history before writing the target request log.
            q=dict(q,context={k:v for k,v in q['context'].items() if k not in ['source_category','bridge_receipt']})
            self.record('context_sanitized',request_id=rid,reason='PURPOSE_DENIED_STALE_BRIDGE',dropped_fields=['source_category','bridge_receipt'])
        self.s['requests'].append(rid)
        req=self.record('request_received',request_id=rid,device=device,installation=q['installation'],epoch=q['epoch'],
                        prediction_time=q['prediction_time'],context=q['context'],purpose=PURPOSE)
        gate=self.record('use_gate',request_id=rid,device=device,allow=permitted,purpose=PURPOSE)
        features=[];category=None
        # On gate denial no lookup at all,including stale cached events or bridge data.
        if permitted and self.s['route']=='D1':
            self.record('lookup_attempt',request_id=rid,device=device,scope='same-device',purpose=PURPOSE)
            e,reason=self.usable(device)
            if e:
                seq=self.record('history_read',request_id=rid,event_receipt=e['receipt'],device=device,source_app='source-app',
                                scope='same-device',category=e['category'],source_available_at=e['available_at'],purpose=PURPOSE)
                f=self.record('feature_read',request_id=rid,family='cross-app-device-history',provenance=seq,actual_read=True,
                              nonnull=True,value=e['category'],model_version='mock-model-v1',materialized_at=self.s['clock'])
                features.append(f);category=e['category']
            else:self.record('lookup_empty',request_id=rid,reason=reason)
        if permitted and 'source_category' in q['context']:
            b=q['context'].get('bridge_receipt');logs=self.log.records()
            br=next((x for x in logs if x['seq']==b and x['kind']=='context_bridge'),None)
            if not br or br['data']['device']!=device or br['data']['category']!=q['context']['source_category']:raise ValueError('Unattested bridge')
            e=next((x for x in self.s['events'] if x['receipt']==br['data']['event_receipt']),None)
            if not e or e['epoch']!=q['epoch'] or e['available_at']>self.s['clock']:raise ValueError('Stale bridge')
            f=self.record('feature_read',request_id=rid,family='current-context',provenance=b,actual_read=True,nonnull=True,
                          value=e['category'],model_version='mock-model-v1',materialized_at=self.s['clock'])
            features.append(f);category=e['category']
        # Equal responses for D1 and LEAK deliberately:response is not a route fingerprint.
        score=.2 if category is None else (.8 if category else .2)
        rng=random.Random(self.s['seed']+len(self.s['requests']))
        filled=rng.random()>=.1
        choice=('mock-creative-high' if score>.5 else 'mock-creative-base') if filled else None
        response=dict(request_id=rid,score=score,creative=choice,filled=filled,model_version='mock-model-v1')
        decision=self.record('decision',request_id=rid,request_receipt=req,gate_receipt=gate,feature_receipts=features,
                             response=response,model_version='mock-model-v1',inventory_version='fixed-v1',cap_version='fixed-v1')
        self.record('request_closed',request_id=rid,decision_receipt=decision,feature_log_complete=True)
        return response
    def reset(self,device):
        mock_key(device);self.s['epoch'][device]=self.s['epoch'].get(device,0)+1
        purged=[e['event_id'] for e in self.s['events'] if e['device']==device]
        self.s['events']=[e for e in self.s['events'] if e['device']!=device]
        self.record('scope_reset',device=device,epoch=self.s['epoch'][device],purged_events=purged,relink_attempted=False)
        return dict(epoch=self.s['epoch'][device])
    def apply(self,command):
        if command['operation']=='init':return self.init(command['route'],command['seed'])
        if self.s is None:raise ValueError('Initialize first')
        if self.log.records()[-1]['kind']=='run_closed':raise ValueError('Run already closed')
        self.clock(command['time']);op=command['operation']
        if op=='permit':out=self.permit(command['app'],command['device'],command['allow'],command.get('effective_at',self.s['clock']))
        elif op=='collect':out=self.collect(command['event'])
        elif op=='predict':out=self.predict(command['request'])
        elif op=='bridge':out=self.bridge(command['device'])
        elif op=='reset':out=self.reset(command['device'])
        elif op=='close':self.record('run_closed',requests=len(self.s['requests']),events=len(self.s['events']),complete=True);out=dict(closed=True)
        else:raise ValueError('Unsupported operation')
        self.flush();return out

def main():
    install();p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    service=Service(a.root)
    try:out=service.apply(read(a.input))
    except Exception as e:
        if service.s is not None:service.record('command_failed',error_type=type(e).__name__,message=str(e));service.flush()
        write(a.output,dict(error=type(e).__name__,message=str(e)));raise
    write(a.output,out)
if __name__=='__main__':main()
