"""Append later research and synthetic engineering artifacts to the archive.

Never edits the source workspace, deletes publication files, fetches datasets,
executes SDKs, or runs historical experiments. Existing 00-67 reports are immutable.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import argparse,csv,hashlib,json,re,shutil,subprocess
from datetime import datetime,timezone

SYNTHETIC = {
    'identity-graph-mvp','identity-graph-ltv-lab','identity-graph-e01',
    'identity-graph-e02','identity-graph-capability-review','engineering76','blackbox75',
}
RESEARCH = {
    'access72','acquisition78','adjust-mechanisms','axon-vector-mechanism-gap',
    'closure70','game-industry69','identity-value74','identity72-experiments73',
    'lineage71','official-samples-audit','production77','server-identity-reference',
    'two-app-partner-readiness','identity-graph-real-data-audit',
}
TEXT = {'.md','.json','.csv','.py','.java','.txt','.sql','.diff'}
SYNTHETIC_EXTRA = {'.sqlite','.jsonl','.log','.npz','.npy'}
EXCLUDED_DIRS = {'__pycache__','.git','.pytest_cache','.venv','venv'}

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def selected(rel):
    parts=rel.parts;name=rel.name.lower();suffix=rel.suffix.lower()
    if any(p in EXCLUDED_DIRS for p in parts):return False
    if len(parts)==1:return suffix in TEXT- {'.txt'}
    if parts[0] in SYNTHETIC:
        return suffix in TEXT|SYNTHETIC_EXTRA or name=='license'
    if parts[0] in RESEARCH or parts[:2]==('public-experiments','round68'):
        # Only the explicitly MIT Adjust source extraction is redistributed.
        if parts[:2]==('adjust-mechanisms','sources'):
            return suffix=='.java' or name in {'license','license.txt'}
        if any(x in {'sources','public','raw','data','downloads','extracted'} for x in parts[1:-1]):return False
        if re.search(r'(?:evidence_(?:graph|index)\.(?:before|after)|history[_.])',name):return False
        return suffix in TEXT or name=='license'
    return False

def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--destination',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--apply',action='store_true');a=parser.parse_args()
    source=a.source.resolve();dest=a.destination.resolve()
    assert source!=dest and (dest/'.git').is_dir()
    tracked={x for x in subprocess.check_output(['git','ls-files','-z'],cwd=dest).decode('utf8').split('\0') if x}
    candidates={p.relative_to(source) for p in source.iterdir() if p.is_file() and selected(p.relative_to(source))}
    for root in SYNTHETIC|RESEARCH|{'public-experiments/round68'}:
        for p in (source/root).rglob('*'):
            if p.is_file() and selected(p.relative_to(source)):candidates.add(p.relative_to(source))
    # Refresh only already-published earlier metadata; do not broaden raw-data roots.
    for name in tracked:
        rel=Path(name)
        if (source/rel).is_file() and rel.suffix.lower() in TEXT:candidates.add(rel)
    rows=[];changes=[]
    for rel in sorted(candidates):
        src=source/rel;dst=dest/rel;digest=sha(src);key=rel.as_posix()
        if dst.is_file() and sha(dst)==digest:action='unchanged'
        else:action='update' if dst.exists() else 'add'
        if action=='update' and len(rel.parts)==1 and re.match(r'\d\d_.*\.md$',key) and int(key[:2])<=67:
            raise ValueError('Historical 00-67 report differs: '+key)
        row=dict(path=key,sha256=digest,bytes=src.stat().st_size,
            kind='local_synthetic_engineering_artifact' if rel.parts[0] in SYNTHETIC else 'research_source_or_aggregate_result')
        rows.append(row)
        if action!='unchanged':changes.append(dict(row,action=action))
    result=dict(source=str(source),destination=str(dest),selected_files=len(rows),
        added=sum(x['action']=='add' for x in changes),updated=sum(x['action']=='update' for x in changes),
        delta_bytes=sum(x['bytes'] for x in changes),largest=sorted(changes,key=lambda x:x['bytes'],reverse=True)[:5])
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if not a.apply:return
    previous_result=dest/'publication/SYNC_RESULT.json'
    if previous_result.exists():
        history=dest/'publication/sync-history';history.mkdir(exist_ok=True)
        shutil.copy2(previous_result,history/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'.json'))
    protected=read(source/'identity-graph-capability-review/HISTORY_BEFORE.json')
    for p in (source/'identity-graph-capability-review').iterdir():
        if p.is_file():protected.setdefault(p.relative_to(source).as_posix(),sha(p))
    assert all((source/p).is_file() and sha(source/p)==h for p,h in protected.items())
    for row in changes:
        src=source/row['path'];dst=dest/row['path'];dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,dst)
        assert sha(src)==row['sha256']==sha(dst)
    # Preserve the earlier publication inventory, refreshing only copied source entries.
    mf=dest/'publication/ORIGINAL_FILE_MANIFEST.csv'
    with mf.open(encoding='utf-8-sig',newline='') as f:combined={x['path']:x for x in csv.DictReader(f)}
    for row in rows:combined[row['path']]=row
    with mf.open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['path','sha256','bytes','kind'],lineterminator='\n');w.writeheader()
        w.writerows(combined[k] for k in sorted(combined))
    mismatches=[p for p,h in protected.items() if not (source/p).is_file() or sha(source/p)!=h]
    assert not mismatches,mismatches
    scope=dict(updated_utc=datetime.now(timezone.utc).isoformat(),numbered_reports=len(list(dest.glob('[0-9][0-9]_*.md'))),
        latest_numbered_round=78,includes_autonomous_MVP_lab_E01_E02_capability_review=True,
        source_workspace_modified=False,source_files_preserved=len(protected),raw_datasets_included=False,
        SDK_packages_added=0,sdk_policy='Existing 282 releases retained; all 47 audited samples already present with identical hashes',
        C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP')
    for name,value in [('CURRENT_SCOPE.json',scope),('SYNC_RESULT.json',dict(result,changes=changes)),
        ('WORKSPACE_PRESERVATION.json',dict(checked=len(protected),mismatches=mismatches,sha256_by_path=protected))]:
        (dest/'publication'/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

if __name__=='__main__':main()
