"""Inventory metadata and known research artifacts; never read device/user IDs."""
from pathlib import Path
from collections import Counter
import csv, datetime, hashlib, json, re

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / 'prediction-validation'
DATA_EXTENSIONS = {'.csv', '.parquet', '.jsonl', '.ndjson', '.sqlite', '.db', '.duckdb',
    '.xlsx', '.xls', '.feather', '.arrow', '.npz', '.npy', '.avro', '.orc', '.h5', '.hdf5'}

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''): h.update(b)
    return h.hexdigest()

def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', 'utf-8')

def csv_profile(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        rows = list(reader)
    seen, missing, duplicates = set(), Counter(), 0
    for row in rows:
        key = tuple(row.get(k) for k in fields)
        duplicates += key in seen
        seen.add(key)
        for k in fields: missing[k] += row.get(k) in ('', None)
    return dict(rows=len(rows), fields=[dict(name=k, storage_type='CSV string; semantic types need contract') for k in fields],
        exact_duplicate_rows=duplicates, duplicate_rate=duplicates/len(rows) if rows else None,
        missing_rate={k: missing[k]/len(rows) if rows else None for k in fields})

def main():
    files = [p for p in ROOT.rglob('*') if p.is_file() and WORK not in p.parents]
    known = {
        'vector/FINANCIAL_COMPARISON.csv': ('public_aggregate', 'Company quarterly financial comparison, not users/cohorts', 'Unity/AppLovin official financial publications; local compilation'),
        'axon/deep/event-callsite-catalog.csv': ('static_reverse_engineering', 'DEX callsite index, not event observations', 'Original game/SDK publishers; local static analysis'),
        'jewel-coloring/deep/adworth-method-inventory.csv': ('static_reverse_engineering', '524 method records, not 524 users', 'Original publisher; local static analysis'),
        'jewel-coloring/deep/rule-catalog.csv': ('static_reverse_engineering', '90 default rules, not production user outcomes', 'Original publisher; local static analysis'),
    }
    assets = []
    for p in files:
        if p.suffix.lower() not in DATA_EXTENSIONS: continue
        rel = p.relative_to(ROOT).as_posix()
        kind, desc, owner = known.get(rel, ('synthetic', 'Existing explicitly synthetic simulation output/template', 'Locally authored research simulation')) if '/model/output/' in rel or rel in known else ('unclassified', 'Needs owner/provenance verification before use', 'Unknown')
        a = dict(path=rel, sha256=digest(p), bytes=p.stat().st_size, data_kind=kind, description=desc,
            owner=owner, authorization='Public/static analysis or authored synthetic use only; no operational-data authorization established',
            eligible_real_training=False, eligible_preinstall_prediction=False, eligible_postinstall_prediction=False,
            time_range='No observed user-level time range established', cohort_maturity='not applicable / not observed',
            event_available_received_times='No complete observed event/available/received timeline',
            revenue_currency_precision='No verified user-level actual revenue ledger',
            identity_scope_and_join='No authorized user-level or cross-app join contract',
            profile=csv_profile(p) if p.suffix.lower()=='.csv' else None)
        assets.append(a)
    reports=[]
    for i in range(56):
        p=next(ROOT.glob(f'{i:02}_*.md'), None)
        if p: reports.append(dict(number=i,path=p.relative_to(ROOT).as_posix(),sha256=digest(p)))
    # Read JSON structure only for discovery; never export values or identifier samples.
    shapes, unread, candidate_shapes = [], [], []
    timeline_keys={'bid_time','bid_at','install_time','install_at','available_at','received_at','event_time','event_at'}
    for p in files:
        if p.suffix.lower()!='.json': continue
        if p.stat().st_size>12*1024*1024:
            unread.append(dict(path=p.relative_to(ROOT).as_posix(),reason='over bounded metadata inspection limit')); continue
        try: obj=json.loads(p.read_text('utf-8-sig'))
        except (ValueError,UnicodeError,OSError): continue
        keys=set()
        def walk(x, depth=0):
            if depth>3:return
            if isinstance(x,dict):
                keys.update(x)
                for v in x.values():
                    if isinstance(v,(dict,list)):walk(v,depth+1)
            elif isinstance(x,list):
                for v in x[:3]:walk(v,depth+1)
        walk(obj)
        row=dict(path=p.relative_to(ROOT).as_posix(),top_level_type=type(obj).__name__,
            timeline_keys=sorted(keys & timeline_keys), classification='structure only; SDK schemas are not event samples')
        shapes.append(row)
        if len(keys & timeline_keys)>=3:candidate_shapes.append(row)
    result=dict(audit_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        scope='D:/GrowthResearch only; file metadata, CSV profiles, bounded JSON keys; no SDK initialization or device access',
        limitations='Archives, binary payloads, arbitrary text/log bodies and files outside research root not inspected as telemetry; no claim that no data exist elsewhere',
        files_scanned=len(files),extension_counts=dict(Counter(p.suffix.lower() for p in files)),
        reports=reports,tabular_candidates=assets,json_structures_inspected=len(shapes),
        json_timeline_candidates=candidate_shapes,json_too_large=unread,
        verified_authorized_real_cohort_datasets=0,real_training_gate='STOP_NO_VERIFIED_AUTHORIZED_DATA')
    save(WORK/'results/asset_audit.json',result)
    save(WORK/'results/json_structure_inventory.json',shapes)
    baseline=WORK/'results/prior_artifacts.before56.json'
    if not baseline.exists():
        protected=[ROOT/x['path'] for x in reports]+[ROOT/'prediction-system/EVIDENCE_GRAPH.json']
        for d in ['ltv/model','auction/model','vector/model','core-insights']:
            protected += [p for p in (ROOT/d).rglob('*') if p.is_file() and '__pycache__' not in str(p)]
        save(baseline,[dict(path=p.relative_to(ROOT).as_posix(),sha256=digest(p)) for p in dict.fromkeys(protected)])
    print(json.dumps({k:result[k] for k in ['files_scanned','json_structures_inspected','verified_authorized_real_cohort_datasets','real_training_gate']}))
    print('Tabular candidates:',len(assets),'timeline-key candidates:',len(candidate_shapes))

if __name__=='__main__':main()
