"""Run unittest with networking blocked, persist real per-case inputs/expectations/results."""
from pathlib import Path
import argparse,csv,datetime,hashlib,io,json,platform,socket,sqlite3,sys,unittest
from unittest.mock import patch
from tests import test_acceptance as cases
R=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def csvsave(p,rows):
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
class Result(unittest.TextTestResult):
    def record(self,test,status,detail=None):
        folder=test.folder
        save(folder/'INPUT.json',dict(test_id=test.case_id,seed=cases.CONFIG['seed'],environment='LOCAL_SYNTHETIC_ONLY',
             fixture=getattr(test,'fixture_manifest',{}),operations=test.calls))
        save(folder/'EXPECTATIONS_AND_ACTUALS.json',test.checks)
        save(folder/'AUDIT_LOG.json',getattr(test,'audit_records',[]))
        save(folder/'RESULT.json',dict(test_id=test.case_id,status=status,assertions=len(test.checks),
             failed_assertions=[c for c in test.checks if not c['passed']],detail=detail))
    def addSuccess(self,test):super().addSuccess(test);self.record(test,'PASS')
    def addFailure(self,test,err):super().addFailure(test,err);self.record(test,'FAIL',self._exc_info_to_string(err,test))
    def addError(self,test,err):super().addError(test,err);self.record(test,'ERROR',self._exc_info_to_string(err,test))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,default=760078);ap.add_argument('--output',default=None);args=ap.parse_args()
    if args.output:
        output=Path(args.output);output=output if output.is_absolute() else R/output
    else:
        output=next(R/'results'/f'run-{i:03d}' for i in range(1,10000) if not (R/'results'/f'run-{i:03d}').exists())
    if output.exists():raise SystemExit('Refusing to overwrite prior test evidence: '+str(output))
    output.mkdir(parents=True);cases.CONFIG.update(seed=args.seed,output=output)
    code={p.relative_to(R).as_posix():sha(p) for p in sorted(R.rglob('*')) if p.is_file() and p.suffix in ['.py','.sql'] and not any(x in p.parts for x in ['results','development','__pycache__'])}
    save(output/'RUN_MANIFEST.json',dict(started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),seed=args.seed,
        python=sys.version,platform=platform.platform(),sqlite=sqlite3.sqlite_version,code_hashes=code,
        source_acceptance_sha256=sha(R/'contracts/ACCEPTANCE_TEST_DESIGN.csv'),network='socket creation, DNS and connections blocked during tests',
        C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP'))
    suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(cases.AcceptanceSuite),unittest.defaultTestLoader.loadTestsFromTestCase(cases.RegressionSuite)])
    log=io.StringIO();runner=unittest.TextTestRunner(stream=log,verbosity=2,resultclass=Result)
    def denied(*a,**kw):raise RuntimeError('NETWORK_DISABLED_FOR_LOCAL_SYNTHETIC_TESTS')
    with patch('socket.socket',side_effect=denied),patch('socket.create_connection',side_effect=denied),patch('socket.getaddrinfo',side_effect=denied):result=runner.run(suite)
    (output/'UNITTEST.log').write_text(log.getvalue(),encoding='utf-8')
    designs=list(csv.DictReader((R/'contracts/ACCEPTANCE_TEST_DESIGN.csv').open(encoding='utf-8-sig',newline='')))
    mapping=[]
    for row in designs:
        outcome=load_result(output,row['test_id'])
        mapping.append(dict(test_id=row['test_id'],original_test=row['test'],original_expected=row['expected'],original_rules=row['rules'],
            implementation_status=outcome['status'],assertions=outcome['assertions'],input_path=f"cases/{row['test_id']}/INPUT.json",
            expected_actual_path=f"cases/{row['test_id']}/EXPECTATIONS_AND_ACTUALS.json",result_path=f"cases/{row['test_id']}/RESULT.json",
            scope='LOCAL_SYNTHETIC_ENGINEERING_ONLY_NOT_PRODUCTION'))
    csvsave(output/'ACCEPTANCE_MAPPING_RESULTS.csv',mapping)
    allresults=[load_result(output,p.name) for p in sorted((output/'cases').iterdir()) if p.is_dir()]
    summary=dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests_run=result.testsRun,failures=len(result.failures),errors=len(result.errors),
        acceptance_passed=sum(x['implementation_status']=='PASS' for x in mapping),acceptance_total=len(mapping),
        regression_total=sum(x['test_id'].startswith('R') for x in allresults),assertions=sum(x['assertions'] for x in allresults),
        seed=args.seed,network_connections_allowed=False,scope='Real execution of synthetic local engineering tests; NOT real identity/model/platform validation',
        C_graph_Axon='UNKNOWN',C_graph_Vector='UNKNOWN',D='UNKNOWN',production_forensics='STOP')
    save(output/'SUMMARY.json',summary);save(output/'ALL_CASE_RESULTS.json',allresults)
    (R/'LATEST_RUN.txt').write_text(output.relative_to(R).as_posix()+'\n',encoding='utf-8')
    print(json.dumps(dict(output=str(output),**summary),ensure_ascii=False))
    if not result.wasSuccessful():print(log.getvalue()[-14000:])
    return 0 if result.wasSuccessful() else 1
def load_result(output,tid):
    p=output/'cases'/tid/'RESULT.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else dict(test_id=tid,status='NOT_EXECUTED',assertions=0)
if __name__=='__main__':raise SystemExit(main())
