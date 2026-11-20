"""Execute finite engineering cases;no Monte Carlo expansion or external requests."""
from pathlib import Path
import argparse,copy,csv,importlib,json,sys,unittest,subprocess,hashlib,platform,os
from mock76.io import read,write,Ledger
from mock76.auditor import audit,assess_observable,hypothesis_verdict
from mock76.safety import install
from run_demo import execute_case
from build_acceptance import compile_cases

D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    install(allow_child=True);p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--seed',type=int,default=760031);args=p.parse_args()
    out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=False)
    code_manifest={p.relative_to(D).as_posix():sha(p) for p in list((D/'mock76').glob('*.py'))+list((D/'tests').glob('*.py'))+[D/'run_demo.py',D/'run_acceptance.py',D/'build_acceptance.py']}
    write(out/'CODE_AT_RUN.json',code_manifest)
    cases=compile_cases();write(out/'CASES.json',cases);(D/'acceptance').mkdir(exist_ok=True);write(D/'acceptance/CASES.json',cases)
    fixture={}
    for route in ['D0','D1','LEAK']:
        x=execute_case(out/'process_runs'/route,route,args.seed);fixture[route]=read(Path(x['root'])/'audit/packet.json')
    rows=[]
    for case in cases['cases']:
        packet=dict(observation_level=case['observation_level'])
        if case['observation_level'] in ['feature','score']:packet['audit_packet']=fixture[case['fixture_route']]
        elif case['observation_level']=='audience':packet['audience']=dict(scope_attested=True,namespace='mock-audience',receiver='mock-service',member=True)
        elif case['observation_level']=='match':packet['match']=dict(scope_attested=True,namespace='mock-provider',entity_granularity='account',result_type='maintained',matchConfidence='cascade-step-8')
        else:packet['observations']=[dict(creative='mock-creative-high',frequency=2,category=1)]
        verdict=assess_observable(packet);claims=set(verdict['claims'])
        hypothesis_observed=hypothesis_verdict(case['original_row']['hypothesis'],verdict)
        ok=verdict['status']==case['expected_status'] and set(case['required_claims'])<=claims and not claims&set(case['forbidden_claims']) and hypothesis_observed==case['hypothesis_outcome']
        # Evidence loss must not strengthen a conclusion.
        weakened=copy.deepcopy(packet)
        if case['observation_level'] in ['feature','score']:weakened['audit_packet']=dict(view='redacted',observations=[])
        elif case['observation_level']=='audience':weakened['audience']['scope_attested']=False
        elif case['observation_level']=='match':weakened['match']['scope_attested']=False
        weak=assess_observable(weakened)
        if case['observation_level'] in ['feature','score','audience','match']:ok=ok and weak['status']=='UNIDENTIFIABLE' and not weak['claims']
        derived=None
        if case['observation_level']=='match':
            d=copy.deepcopy(packet);d['match']['result_type']='derived';derived=assess_observable(d)
            ok=ok and 'provider_maintained_status' not in derived['claims']
        write(out/'matrix_cases'/f"{case['case_id']}.json",dict(case=case,input=packet,verdict=verdict,hypothesis_observed=hypothesis_observed,weakened_input=weakened,weakened_verdict=weak,derived_variant_verdict=derived,passed=ok))
        rows.append(dict(case_id=case['case_id'],hypothesis=case['original_row']['hypothesis'],observation_id=case['original_row']['observation_id'],fixture=case['fixture_route'],expected_status=case['expected_status'],actual_status=verdict['status'],passed=ok,hypothesis_outcome=hypothesis_observed,claim_count=len(claims)))
    with (out/'MATRIX_RESULTS.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    regressions=[]
    def reg(name,ok,details):regressions.append(dict(name=name,passed=bool(ok),details=details))
    d1=audit(fixture['D1']);leak=audit(fixture['LEAK']);d0=audit(fixture['D0'])
    response1=d1['requests'][0]['response'];response2=leak['requests'][0]['response']
    reg('equal_outputs_different_routes',response1==response2 and d1['routes']!=leak['routes'],dict(D1=d1,LEAK=leak))
    reg('ads_only_unidentifiable_both',all(audit(dict(view='external_only',observations=[x]))['status']=='UNIDENTIFIABLE' for x in [response1,response2]),dict(response=response1))
    reg('D0_no_H0_vs_H3_training_inference','training_origin_H0_vs_H3' in d0['not_identified'],d0)
    for name,options,expected in [
      ('not_yet_available',dict(available_at=80),'NO_INDIVIDUAL_HISTORY_READ_OBSERVED'),
      ('source_denied',dict(source_denied=True),'GATE_BLOCKED'),
      ('revoke_after_collect',dict(revoke=True),'GATE_BLOCKED'),
      ('reset_no_relink',dict(reset=True),'NO_INDIVIDUAL_HISTORY_READ_OBSERVED'),
      ('different_device',dict(other_device=True),'GATE_BLOCKED'),
      ('duplicate_event',dict(duplicate=True),'SAME_DEVICE_HISTORY_READ')]:
        x=execute_case(out/'process_runs'/name,'D1',args.seed,**options);v=x['verdict']
        reg(name,v['status']=='IDENTIFIED_LOCAL_CHAIN' and v['routes']==[expected],v)
    # Determinism checks all ledger and response bytes,not paths in process launch logs.
    x=execute_case(out/'process_runs/replay_D1','D1',args.seed)
    reg('fixed_seed_ledger_replay',read(Path(x['root'])/'audit/packet.json')==fixture['D1'],dict(seed=args.seed,comparison='all ledger records byte-equivalent JSON;absolute process paths excluded'))
    # Auditor independence:copy only the public packet and run without any service root.
    isolated=out/'auditor_isolated';isolated.mkdir();write(isolated/'packet.json',fixture['D1'])
    cp=subprocess.run([sys.executable,'-X','utf8','-m','mock76.auditor','--input',str(isolated/'packet.json'),'--output',str(isolated/'verdict.json')],cwd=D,capture_output=True,text=True,timeout=20)
    reg('auditor_no_private_truth',cp.returncode==0 and read(isolated/'verdict.json')==d1,dict(command='auditor with public packet only',stdout=cp.stdout,stderr=cp.stderr))
    # Actual socket creation and child spawning are denied inside the runtime guard.
    probe="from mock76.safety import install; install(); import socket; socket.socket()"
    cp=subprocess.run([sys.executable,'-X','utf8','-c',probe],cwd=D,capture_output=True,text=True,timeout=20)
    reg('socket_creation_denied',cp.returncode!=0 and 'Round76 forbids all sockets' in cp.stderr,dict(returncode=cp.returncode,stdout=cp.stdout,stderr=cp.stderr))
    probe="from mock76.safety import install; install(); import subprocess; subprocess.run(['unused-mock-command'])"
    cp=subprocess.run([sys.executable,'-X','utf8','-c',probe],cwd=D,capture_output=True,text=True,timeout=20)
    reg('app_child_spawn_denied',cp.returncode!=0 and 'cannot spawn children' in cp.stderr,dict(returncode=cp.returncode,stdout=cp.stdout,stderr=cp.stderr))
    write(out/'REGRESSION_RESULTS.json',regressions)
    suite=unittest.defaultTestLoader.discover(str(D/'tests'))
    os.environ['MOCK76_UNIT_LOG_ROOT']=str(out/'unit_cases')
    with (out/'UNITTEST.txt').open('w',encoding='utf-8') as stream:result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    del os.environ['MOCK76_UNIT_LOG_ROOT']
    unit=dict(tests_run=result.testsRun,failures=[dict(test=str(t),trace=s) for t,s in result.failures],errors=[dict(test=str(t),trace=s) for t,s in result.errors],skipped=len(result.skipped),passed=result.wasSuccessful())
    write(out/'UNITTEST.json',unit)
    summary=dict(status='PASS' if all(x['passed'] for x in rows+regressions) and unit['passed'] else 'FAIL',seed=args.seed,
                 matrix_cases=len(rows),matrix_passed=sum(x['passed'] for x in rows),process_regressions=len(regressions),regressions_passed=sum(x['passed'] for x in regressions),unit_tests=unit['tests_run'],unit_passed=unit['passed'],
                 python=platform.python_version(),scope='offline engineering fixtures only;not new statistical efficacy experiment',
                 apps='separate Python CLI processes via local JSON files;not Android/iOS APKs',no_external_calls=True,real_platform_claims=False)
    write(out/'SUMMARY.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    if summary['status']!='PASS':raise SystemExit(1)

if __name__=='__main__':main()
