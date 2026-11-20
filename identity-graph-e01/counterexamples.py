"""Deliberately incorrect output mutations; NEVER an alternative data path."""
from copy import deepcopy

def faulty(result, mode):
    x=deepcopy(result)
    if mode=='account_contamination':
        x['cross_app_history']['observed_amount_by_currency_micros']['USD']+=99_000_000
    elif mode=='source_target_mix':
        x['cross_app_history']['observed_amount_by_currency_micros']['USD']+=3_000_000
    elif mode=='late_information_leak':
        x['cross_app_history']['observed_amount_by_currency_micros']['USD']+=41_000_000
    else:raise ValueError(mode)
    return x

def partition_violations(result, *, source=7_000_000, target=3_000_000, excluded_refs=()):
    """Independent fixture oracle; no resolver/policy/accounting implementation."""
    failures=[]
    if result.get('status')!='OK':return ['EXPECTED_APPROVED_PARTITION']
    if result['cross_app_history']['observed_amount_by_currency_micros'].get('USD',0)!=source:failures.append('SOURCE_AMOUNT_MISMATCH')
    if result['target_app_history']['observed_amount_by_currency_micros'].get('USD',0)!=target:failures.append('TARGET_AMOUNT_MISMATCH')
    if set(excluded_refs)&set(result['ledger_refs']):failures.append('EXCLUDED_LEDGER_LEAK')
    audit_source=sum(r['amount_micros'] for r in result['partition_audit'] if r['partition']=='cross_app_history' and r['currency']=='USD')
    if audit_source!=result['cross_app_history']['observed_amount_by_currency_micros'].get('USD',0):failures.append('AUDIT_RECONCILIATION_FAILED')
    if result['person_inferred']:failures.append('ACCOUNT_UPGRADED_TO_PERSON')
    return failures
