"""Read-only hash check against the frozen historical file baseline."""
import sys
sys.dont_write_bytecode=True
from lab.common import ROOT,load,sha,save

def main():
    baseline=load(ROOT/'PRESERVATION_BASELINE.json');failures=[]
    for path,expected in baseline.items():
        target=ROOT.parent/path
        if not target.is_file() or sha(target)!=expected:failures.append(path)
    result=dict(status='FAIL' if failures else 'PASS',checked=len(baseline),failures=failures)
    save(ROOT/'results/PRESERVATION_PRECHECK.json',result);print(result)
    if failures:raise SystemExit(1)

if __name__=='__main__':main()
