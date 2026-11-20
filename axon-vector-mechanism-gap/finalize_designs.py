"""Serialize planned experiments and align strict product-scoped matrix labels."""
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parent
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    if (ROOT/'EXPERIMENT_DESIGNS.json').exists():raise SystemExit('Refusing to overwrite designs')
    path=ROOT/'01_Axon_Vector机制差异矩阵.csv'
    with path.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    # Adjacent Unity products cannot confirm Vector-specific identity receipt.
    rows[0]['Vector_status']='UNKNOWN'
    rows[0]['Vector_scoped_claim']='CONFIRMED仅限邻接Unity Ads/UPA输入契约；Vector逐字段接收UNKNOWN'
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    plans=[
      dict(id='E01',candidate='C01',seed=780241,status='NOT_EXECUTED',
        hypothesis='Authenticated account/task routing preserves allowed source history without shared-device contamination or target-App duplication',
        inputs=['synthetic accounts A/B','shared device D1 and device D2','source X/target Y','existing resolver receipts and policy gates','synthetic ledger A=7/B=99/target=3 units'],
        expected_observations=['source-X account-A history=7 only when legally available','target-Y own amount=3 stays separate','no legal account proof=>unidentifiable or denied','future/expired/revoked sources excluded'],
        failure_criteria=['cross-account amount included','source/target amounts falsely called cross-App history','namespace or time leakage','scope assertion without authentication'],
        stop_conditions=['real identity/SSO/backend required','original rules or files must be changed','source partition not auditable through accepted lineage'],
        result_scope='ENGINEERING_GRAIN_AND_LINEAGE_ONLY_NOT_LTV_GAIN',actual_results=None),
      dict(id='E02',candidate='C02',seed=780241,status='NOT_EXECUTED',
        hypothesis='A local queue-to-fake-sink handoff rechecks current purpose and epoch, preventing commit after effective revocation',
        inputs=['synthetic outbox copy','unchanged independent control DB contract','existing policy.allowed','deterministic interleavings','local in-memory fake sink'],
        expected_observations=['revoke/delete/expiry cancels pending or retry','epoch change before commit aborts/revalidates','restored state cannot revive deleted use','duplicate retry has one economic effect'],
        failure_criteria=['post-prohibition commit','restored stale identity payload handed off','duplicate accounting','claim of atomicity without proven linearization point'],
        stop_conditions=['network or real ACK required','dual-store/multi-process atomicity cannot be established','claim of third-party deletion or model unlearning'],
        result_scope='LOCAL_HANDOFF_STATE_MACHINE_ONLY',actual_results=None),
      dict(id='E03',candidate='C03',seed=780241,status='NOT_EXECUTED',
        hypothesis='A positive/negative-dependency shadow invalidation planner detects all oracle-changing synthetic mutations while marking fewer unrelated dependencies',
        inputs=['synthetic independent components A/B','existing compute/read fresh oracle','shadow dependency metadata','new relationship/event, correction, expiry, revocation, restore cases'],
        expected_observations=['unrelated B changes may be marked irrelevant in plan only','new non-lineage members trigger invalidation','scheduled expiry without writes detected','unknown mutations conservatively invalidate'],
        failure_criteria=['oracle value/lineage/legal availability changes but planner predicts unaffected','planner bypasses original read or policy checks','unmeasured latency claims'],
        stop_conditions=['original global epoch check must be removed','production or distributed consistency needed','unknown dependency treated as no effect'],
        result_scope='SHADOW_PLANNER_ONLY_NOT_DEPLOYED_CACHE',actual_results=None)
    ]
    save(ROOT/'EXPERIMENT_DESIGNS.json',plans)
    print(json.dumps(dict(plans=len(plans),executed=0)))

if __name__=='__main__':main()
