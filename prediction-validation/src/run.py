"""Synthetic-only smoke runner. This first round intentionally trains no model."""
from pathlib import Path
import argparse, json, platform, hashlib, importlib.metadata
from datetime import datetime, timezone
from .synthetic_fixture import fixture
from .validation import validate, build_labels, feature_audit

BASE=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--synthetic-smoke',action='store_true',required=True)
    p.add_argument('--run-id',required=True,help='New immutable run directory; existing paths are rejected')
    args=p.parse_args()
    if not args.run_id.replace('_','').replace('-','').isalnum():p.error('Simple run-id only')
    out=BASE/'results'/args.run_id
    out.mkdir(parents=True,exist_ok=False)
    data=fixture();quality=validate(data)
    labels,_=build_labels(data)
    result=dict(conclusion_level='【合成实验支持】',scope='Accounting and time-gate smoke checks only; no fitted model or vendor performance evidence',
        provenance='synthetic',real_training_performed=False,model_training_performed=False,
        actual_platform_roas_measured=False,causal_incrementality_identified=False,
        utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),jsonschema_version=importlib.metadata.version('jsonschema'),
        input_sha256=hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest(),
        quality=quality,labels=labels,feature_coverage=feature_audit(data),
        stopped_real_work_reason='No independently verified authorized real data in local audit',
        prediction_metrics=None,auction_roas=None)
    for name,obj in [('synthetic_bundle.json',data),('smoke_result.json',result)]:
        (out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps(dict(output=str(out),quality_passed=quality['passed'],labels=len(labels),model_training_performed=False),ensure_ascii=False))

if __name__=='__main__':main()
