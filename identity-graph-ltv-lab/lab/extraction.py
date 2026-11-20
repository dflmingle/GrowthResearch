"""Query the read-only imported MVP on lab-owned synthetic databases only."""
from .common import BASE,DAY,LabWorld,save,to_time,csvsave
from .adapter import GraphAdapter

def schedule_actions(rows):
    """Independent installations may overlap; the shared clock never rewinds."""
    return sorted([(r['install_at'],0,i) for i,r in enumerate(rows)]+
                  [(r['prediction_at'],1,i) for i,r in enumerate(rows)])
def extract(rows,seed,world,out,protocol,progress):
    result=[];audit=[];start=BASE-120*DAY
    for shard,offset in enumerate(range(0,len(rows),protocol['shard_size'])):
        chunk=rows[offset:offset+protocol['shard_size']];folder=out/'graphs'/world/str(seed)/f'shard-{shard:03d}'
        w=LabWorld(folder,seed+shard,start);s=w.system;adapter=GraphAdapter(s);refs=[]
        try:
            for i,row in enumerate(chunk):
                d=w.entity(f'device-{i}','device');account=w.entity(f'account-{i}','account')
                oldapp=w.install(f'history-app-{i}',d,app='synthetic-history-game');w.login(account,oldapp,d)
                other=None
                if row['shared_device']:
                    other=w.entity(f'shared-account-{i}','account');w.login(other,oldapp,d)
                refs.append(dict(device=d,account=account,history_app=oldapp,other=other))
            to_time(s.clock,start+DAY)
            gross=[]
            for row,ref in zip(chunk,refs):
                gross.append(w.revenue(ref['history_app'],row['history_gross_micros'],account=ref['account'],economic_key='synth:history-order'))
                if ref['other']:w.revenue(ref['history_app'],5000000,account=ref['other'],economic_key='synth:shared-other-order')
            to_time(s.clock,start+2*DAY)
            for row,ref,first in zip(chunk,refs,gross):
                if row['history_refund_micros']:
                    w.revenue(ref['history_app'],row['history_gross_micros']-row['history_refund_micros'],account=ref['account'],
                        economic_key='synth:history-order',revision=2,correction_of=first['ledger_ref'])
            snapshots=[];records={};traces={};apps={}
            for action_at,kind,index in schedule_actions(chunk):
                row,ref=chunk[index],refs[index]
                to_time(s.clock,action_at)
                if kind==0:
                    app=w.install('current-'+row['sample_id'],ref['device'],app='synthetic-target-game');w.login(ref['account'],app,ref['device'])
                    apps[index]=app
                    continue
                app=apps[index]
                early=s.events.ingest(app=app,source_name='synth:early-summary',event_id='synth:'+row['sample_id'],event_type='early_summary',
                    occurred_at=row['early_observed_at'],account=ref['account'])
                feature=adapter.extract(ref['device'],row['prediction_at'],start)
                b=feature['bundle'];epochs=dict(policy_epoch=s.store.epoch,graph_version=s.store.graph_version)
                trace=dict(sample_id=row['sample_id'],world=world,seed=seed,shard=shard,entity_grain='device-not-person',
                    prediction_at=row['prediction_at'],early_observed_at=row['early_observed_at'],early_available_at=row['early_available_at'],
                    graph_eligible=feature['eligible'],gate_reason=feature['reason'],bundle_ref=b['bundle_ref'] if b else None,
                    bundle_as_of=b['as_of'] if b else None,feature_actual_available_at=b['consumer_available_at'] if b else None,
                    graph_relation_max_observed=None,graph_relation_max_available=None,event_max_observed=None,event_max_available=None,
                    early_event_ref=early['event_ref'],**epochs)
                if b:
                    edge_refs=b['lineage']['edge_revisions'];event_refs=b['lineage']['event_refs']
                    ed=[dict(s.store.db.execute('SELECT observed_at,available_at FROM edge_revisions WHERE id=? AND revision=?',tuple(x)).fetchone()) for x in edge_refs]
                    ev=[dict(s.store.db.execute('SELECT observed_at,available_at FROM events WHERE id=?',(x,)).fetchone()) for x in event_refs]
                    for prefix,values in [('graph_relation',ed),('event',ev)]:
                        trace[prefix+'_max_observed']=max([x['observed_at'] for x in values],default=None)
                        trace[prefix+'_max_available']=max([x['available_at'] for x in values],default=None)
                for key in ['early_observed_at','early_available_at','feature_actual_available_at','graph_relation_max_observed','graph_relation_max_available','event_max_observed','event_max_available']:
                    if trace[key] is not None and trace[key]>row['prediction_at']:raise RuntimeError('Feature leakage: '+key)
                record=dict(row,graph_log_history=feature['value'],graph_available=int(feature['eligible']),graph_gate_reason=feature['reason'])
                records[index]=record;traces[index]=trace
                snapshots.append(dict(sample_id=row['sample_id'],extracted_before_any_lifecycle_intervention=True,
                    synthetic_only=True,decision_at=row['prediction_at'],adapter_result=feature))
            result.extend(records[i] for i in range(len(chunk)))
            audit.extend(traces[i] for i in range(len(chunk)))
            save(folder/'FEATURE_QUERY_SNAPSHOTS.json',snapshots)
            save(folder/'MVP_AUDIT_LOG.json',s.audit.records())
            if not s.audit.verify():raise RuntimeError('Imported MVP audit chain invalid')
        finally:w.close()
        progress(dict(stage='MVP_EXTRACTION',world=world,seed=seed,completed=min(offset+len(chunk),len(rows)),total=len(rows)))
    return result,audit
