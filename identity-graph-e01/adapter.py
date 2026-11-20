"""Task/receipt binding and partitioning only; identity/policy/accounting stay in MVP."""
from common import PURPOSE,ENV,Rejected
import json

class TaskAwareAdapter:
    def __init__(self,system):self.s=system

    def _binding(self,request):
        needed={'task_ref','target_install_ref','subject_type','auth_receipt','prediction_at','since_at','purpose','authorization_context'}
        if not isinstance(request,dict) or set(request)!=needed:raise Rejected('TASK_FIELDS_INVALID_NO_RAW_ACCOUNT')
        if not isinstance(request['task_ref'],str) or not request['task_ref'].startswith('synth:task:'):raise Rejected('SYNTHETIC_TASK_REQUIRED')
        if request['subject_type']!='account':raise Rejected('UNSUPPORTED_TASK_SUBJECT')
        if request['purpose']!=PURPOSE:raise Rejected('TASK_PURPOSE_MISMATCH')
        if type(request['prediction_at']) is not int or request['prediction_at']!=self.s.clock.now:raise Rejected('BACKDATED_OR_FUTURE_TASK_FORBIDDEN')
        if type(request['since_at']) is not int or not 0<=request['since_at']<=request['prediction_at']:raise Rejected('TASK_WINDOW_INVALID')
        context=request['authorization_context']
        if not isinstance(context,dict) or set(context)!={'environment','purpose','source_app_allowlist'}:raise Rejected('AUTHORIZATION_CONTEXT_INVALID')
        if context['environment']!=ENV or context['purpose']!=request['purpose']:raise Rejected('AUTHORIZATION_CONTEXT_MISMATCH')
        allowed=context['source_app_allowlist']
        if not isinstance(allowed,list) or not allowed or any(not isinstance(x,str) or not x.startswith('synthetic-') for x in allowed):raise Rejected('SOURCE_SCOPE_INVALID')
        nonce=request['auth_receipt']
        if not isinstance(nonce,str) or not nonce.startswith('synth:'):raise Rejected('AUTH_RECEIPT_REQUIRED')
        # Inspect only the original resolver's accepted receipt. Never validate or
        # generate a parallel credential or accept an account_ref from the caller.
        receipt=self.s.store.control.execute('SELECT * FROM auth_nonces WHERE nonce=?',(nonce,)).fetchone()
        if receipt is None:raise Rejected('AUTH_RECEIPT_REQUIRED')
        receipt=dict(receipt)
        if receipt['app_ref']!=request['target_install_ref'] or receipt['purpose']!=request['purpose']:
            raise Rejected('AUTH_RECEIPT_SCOPE_MISMATCH')
        if receipt['used_at']>request['prediction_at']:raise Rejected('AUTH_RECEIPT_NOT_YET_AVAILABLE')
        account=receipt['account_ref'];target=request['target_install_ref'];purpose=request['purpose']
        a=self.s.store.entity(account);app=self.s.store.entity(target)
        if (a['entity_type'],app['entity_type'])!=('account','app_instance'):raise Rejected('TASK_ENTITY_GRAIN_MISMATCH')
        self.s.policy.require([account,target],purpose,as_of=request['prediction_at'])
        # Original policy/graph API supplies current active/known/available edges.
        active=self.s.graph.active(request['prediction_at'],purpose)
        login=[e for e in active if e['kind']=='logged_in_as' and e['src']==target and e['dst']==account and e['quality_kind']=='authenticated_account_control']
        if not login:raise Rejected('TARGET_AUTH_RELATION_NOT_ACTIVE')
        installed=[e for e in active if e['kind']=='installed_on' and e['src']==target]
        if len(installed)!=1:raise Rejected('TARGET_INSTALL_NOT_ACTIVE')
        self.s.policy.require([installed[0]['dst']],purpose,as_of=request['prediction_at'])
        ns=self.s.store.db.execute('SELECT * FROM namespaces WHERE id=?',(app['namespace_id'],)).fetchone()
        return dict(account_ref=account,receipt=receipt,target_product=ns['app'],
                    target_namespace=dict(ns),target_login_refs=[[e['id'],e['revision']] for e in login],
                    target_device_ref=installed[0]['dst'])

    def extract(self,request):
        try:
            binding=self._binding(request)
            bundle=self.s.features.compute(binding['account_ref'],as_of=request['prediction_at'],since_at=request['since_at'],purpose=request['purpose'])
            read=self.s.features.read(bundle['bundle_ref'],purpose=request['purpose'])
            if bundle['consumer_available_at']>request['prediction_at']:raise Rejected('FUTURE_FEATURE_AVAILABILITY')
            result=self._partition(request,binding,bundle,read)
            result.update(status='OK',reason='ACCOUNT_TASK_NOT_PERSON',task_ref=request['task_ref'],
                          subject_type='account',account_ref=binding['account_ref'],person_inferred=False,
                          available_at=bundle['consumer_available_at'],prediction_at=request['prediction_at'],
                          bundle_ref=bundle['bundle_ref'],feature_read_ref=read['feature_read_ref'],
                          relation_refs=bundle['lineage']['edge_revisions'],ledger_refs=bundle['lineage']['ledger_refs'],
                          original_lineage=bundle['lineage'],original_account_values=read['values'],
                          graph_version=bundle['graph_version'],policy_epoch=bundle['policy_epoch'])
            return result
        except Rejected as exc:
            reason=str(exc)
            return dict(status='UNSUPPORTED_PARTITION' if reason.startswith('UNSUPPORTED_PARTITION') else 'DENIED',reason=reason,
                        person_inferred=False,cross_app_history=None,target_app_history=None,available_at=None)

    def _partition(self,request,binding,bundle,read):
        lineage=bundle.get('lineage')
        required={'entity_refs','edge_revisions','event_refs','ledger_refs','coverage_refs'}
        if not isinstance(lineage,dict) or not required<=set(lineage):raise Rejected('UNSUPPORTED_PARTITION:MISSING_LINEAGE')
        # Reconcile the read with compute; consumers do not invent different data.
        if json.dumps(read.get('lineage'),sort_keys=True)!=json.dumps(lineage,sort_keys=True):raise Rejected('UNSUPPORTED_PARTITION:READ_LINEAGE_MISMATCH')
        needed_values={'revenue_by_currency_micros','observed_ledger_count','observation_status','currency'}
        if not isinstance(read.get('values'),dict) or not needed_values<=set(read['values']):
            raise Rejected('UNSUPPORTED_PARTITION:MISSING_ACCOUNT_VALUES')
        approved_entities=set(lineage['entity_refs']);approved_events=set(lineage['event_refs'])
        if not {tuple(r) for r in binding['target_login_refs']}<=set(tuple(r) for r in lineage['edge_revisions']):
            raise Rejected('UNSUPPORTED_PARTITION:TARGET_AUTH_NOT_IN_APPROVED_LINEAGE')
        def byref(table,ref):
            # This is the ONLY ledger read: approved exact primary-key lookup.
            if table not in ['ledger','events','coverage']:raise Rejected('UNSUPPORTED_PARTITION:TABLE')
            row=self.s.store.db.execute('SELECT * FROM '+table+' WHERE id=?',(ref,)).fetchone()
            if row is None:raise Rejected('UNSUPPORTED_PARTITION:REFERENCED_ROW_MISSING')
            return dict(row)
        edges=[]
        for ref,revision in lineage['edge_revisions']:
            row=self.s.store.db.execute('SELECT * FROM edge_revisions WHERE id=? AND revision=?',(ref,revision)).fetchone()
            if row is None:raise Rejected('UNSUPPORTED_PARTITION:EDGE_MISSING')
            edges.append(dict(row))
        apps={e['src'] for e in edges if e['kind']=='installed_on' and e['src'] in approved_entities and e['dst'] in approved_entities}
        appmeta={}
        for appref in apps:
            entity=self.s.store.entity(appref)
            ns=self.s.store.db.execute('SELECT * FROM namespaces WHERE id=?',(entity['namespace_id'],)).fetchone()
            appmeta[appref]=dict(app=ns['app'],namespace_ref=entity['namespace_id'])
        def category(appref):
            if appref not in appmeta:raise Rejected('UNSUPPORTED_PARTITION:APP_NOT_APPROVED')
            if appmeta[appref]['app']==binding['target_product']:return 'target_app_history'
            return 'cross_app_history' if appmeta[appref]['app'] in request['authorization_context']['source_app_allowlist'] else 'out_of_task_scope'
        groups={key:dict(observed_amount_by_currency_micros={},complete_amount_by_currency_micros=None,
          observation_status='UNOBSERVED',app_instance_refs=[],ledger_refs=[],event_refs=[],coverage_refs=[],missing_reasons=[])
          for key in ['cross_app_history','target_app_history','out_of_task_scope']}
        for appref in sorted(apps):groups[category(appref)]['app_instance_refs'].append(appref)
        approved_rows=[];audit_rows=[];totals={}
        for ref in lineage['ledger_refs']:
            ledger=byref('ledger',ref)
            if ledger['event_ref'] not in approved_events or ledger['account_ref']!=binding['account_ref'] or ledger['app_ref'] not in apps:
                raise Rejected('UNSUPPORTED_PARTITION:LEDGER_NOT_ACCOUNT_APPROVED')
            event=byref('events',ledger['event_ref'])
            if event['app_ref']!=ledger['app_ref'] or event['account_ref']!=binding['account_ref']:raise Rejected('UNSUPPORTED_PARTITION:EVENT_SCOPE_MISMATCH')
            for row in [ledger,event]:
                if row['deleted'] or any(row[k]>request['prediction_at'] for k in ['occurred_at','observed_at','available_at']):
                    raise Rejected('UNSUPPORTED_PARTITION:APPROVED_SOURCE_NOT_USABLE')
            key=category(ledger['app_ref']);g=groups[key];currency=ledger['currency'];amount=ledger['amount_micros']
            if type(amount) is not int:raise Rejected('UNSUPPORTED_PARTITION:AMOUNT_UNAVAILABLE')
            g['observed_amount_by_currency_micros'][currency]=g['observed_amount_by_currency_micros'].get(currency,0)+amount
            totals[currency]=totals.get(currency,0)+amount
            g['ledger_refs'].append(ref);g['event_refs'].append(ledger['event_ref']);approved_rows.append(ledger)
            audit_rows.append(dict(ledger_ref=ref,event_ref=ledger['event_ref'],app_ref=ledger['app_ref'],app_namespace=appmeta[ledger['app_ref']],
                partition=key,amount_micros=amount,currency=currency,account_ref=ledger['account_ref'],
                occurred_at=ledger['occurred_at'],observed_at=ledger['observed_at'],available_at=ledger['available_at'],
                event_occurred_at=event['occurred_at'],event_observed_at=event['observed_at'],event_available_at=event['available_at']))
        if totals!=read['values']['revenue_by_currency_micros'] or len(approved_rows)!=read['values']['observed_ledger_count']:
            raise Rejected('UNSUPPORTED_PARTITION:ACCOUNT_TOTAL_RECONCILIATION')
        cov=[byref('coverage',ref) for ref in lineage['coverage_refs']]
        for g in groups.values():
            full=bool(g['app_instance_refs'])
            for appref in g['app_instance_refs']:
                matches=[c for c in cov if c['app_ref']==appref]
                g['coverage_refs'] += [c['id'] for c in matches]
                # Reuse original query's accepted coverage; this is partition
                # presentation, never an alternative authority for completeness.
                valid=[c for c in matches if c['status']=='COMPLETE' and c['start_at']<=request['since_at'] and c['end_at']>=request['prediction_at']]
                if not valid:full=False;g['missing_reasons'].append('NO_COMPLETE_APPROVED_COVERAGE:'+appref)
            if g['app_instance_refs']:
                if full and read['values']['observation_status'] in ['OBSERVED_COMPLETE','KNOWN_ZERO']:
                    g['complete_amount_by_currency_micros']=dict(g['observed_amount_by_currency_micros'])
                    if not g['complete_amount_by_currency_micros']:g['complete_amount_by_currency_micros']={read['values']['currency']:0}
                    g['observation_status']='KNOWN_ZERO' if all(v==0 for v in g['complete_amount_by_currency_micros'].values()) else 'OBSERVED_COMPLETE'
                else:g['observation_status']='NOT_FULLY_OBSERVED';g['missing_reasons'].append('ACCOUNT_COMPLETENESS_NOT_CERTIFIED')
            else:g['missing_reasons'].append('NO_APPROVED_APP_OBSERVATION')
        return dict(**groups,observation_status=read['values']['observation_status'],
                    partition_audit=audit_rows,authorization_audit=dict(receipt_nonce=request['auth_receipt'],
                    receipt_app=binding['receipt']['app_ref'],receipt_account=binding['account_ref'],
                    target_login_refs=binding['target_login_refs'],purpose=request['purpose'],policy_epoch=self.s.store.epoch,
                    source_allowlist_scope='RESTRICTS_ORIGINAL_POLICY_ONLY_NOT_A_GRANT'))

    def reread(self,request,prior):
        """Snapshots are not reusable capabilities: recheck original read first."""
        try:
            self._binding(request)
            if prior.get('status')!='OK':raise Rejected('PRIOR_RESULT_NOT_READABLE')
            # Read the original bundle; no new query can silently replace an old
            # invalid cache. Binding at the current clock also forbids old tasks.
            self.s.features.read(prior['bundle_ref'],purpose=request['purpose'])
            if prior['task_ref']!=request['task_ref'] or prior['account_ref']!=self._binding(request)['account_ref']:
                raise Rejected('PRIOR_TASK_SCOPE_MISMATCH')
            return dict(status='READABLE',bundle_ref=prior['bundle_ref'])
        except Rejected as exc:return dict(status='DENIED',reason=str(exc))
