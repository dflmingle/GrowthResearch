"""Save real unittest output and block networking during regressions."""
import sys
sys.dont_write_bytecode=True
import datetime,io,unittest
from unittest.mock import patch
from lab.common import ROOT,save,sha

def main():
    folder=ROOT/'results/unit-tests'
    if folder.exists():raise SystemExit('Refusing to overwrite unit-test evidence')
    folder.mkdir();stream=io.StringIO()
    def deny(*args,**kwargs):raise RuntimeError('NETWORK_DISABLED_SYNTHETIC_TESTS')
    suite=unittest.defaultTestLoader.loadTestsFromName('test_lab')
    with patch('socket.socket',side_effect=deny),patch('socket.create_connection',side_effect=deny),patch('socket.getaddrinfo',side_effect=deny):
        result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    text=stream.getvalue();(folder/'UNITTEST.log').write_text(text,encoding='utf-8');print(text)
    save(folder/'SUMMARY.json',dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests=result.testsRun,
        failures=len(result.failures),errors=len(result.errors),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        sources={p:sha(ROOT/p) for p in ['test_lab.py','lab/extraction.py','lab/generator.py','lab/model.py','lab/adapter.py','lab/counterexamples.py']},network='socket entry points blocked'))
    if not result.wasSuccessful():raise SystemExit(1)

if __name__=='__main__':main()
