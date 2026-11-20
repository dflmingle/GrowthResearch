"""Local process orchestration only;file IPC,no servers,sockets or production SDKs."""
from pathlib import Path
import argparse,sys,subprocess,json,random
from mock76.io import Ledger,read,write
from mock76.safety import install

def execute_case(root,route,seed=760031,*,available_at=20,predict_at=30,source_denied=False,revoke=False,reset=False,other_device=False,duplicate=False):
    root=Path(root);root.mkdir(parents=True,exist_ok=False);transcript=Ledger(root/'process_transcript.jsonl');counter=0
    def child(module,args):
        nonlocal counter
        counter+=1;cmd=[sys.executable,'-X','utf8','-m',module,*map(str,args)]
        cp=subprocess.run(cmd,cwd=Path(__file__).resolve().parent,capture_output=True,text=True,encoding='utf-8',timeout=20)
        transcript.append('child_exit',counter,module=module,args=list(map(str,args)),returncode=cp.returncode,stdout=cp.stdout,stderr=cp.stderr)
        if cp.returncode:raise RuntimeError(module+' failed:'+cp.stderr)
    def service(command):
        nonlocal counter
        label=f'{counter+1:03d}';inp=root/'ipc'/f'{label}_service_input.json';out=root/'ipc'/f'{label}_service_output.json';write(inp,command)
        child('mock76.service',['--root',root,'--input',inp,'--output',out]);return read(out)
    service(dict(operation='init',route=route,seed=seed))
    service(dict(operation='permit',time=0,app='source-app',device='mock-device-A',allow=not source_denied))
    service(dict(operation='permit',time=0,app='target-app',device='mock-device-A',allow=True))
    if other_device:service(dict(operation='permit',time=0,app='target-app',device='mock-device-B',allow=True))
    source_input=root/'ipc/source_input.json';source_out=root/'ipc/source_envelope.json'
    write(source_input,dict(event_id='mock-event-1',device='mock-device-A',installation='mock-install-S1',event_time=10,available_at=available_at,category=1,purpose='mock-research',epoch=0))
    child('mock76.app_source',['--input',source_input,'--output',source_out])
    envelope=read(source_out);service(dict(operation='collect',time=12,event=envelope['event']))
    if duplicate:service(dict(operation='collect',time=13,event=envelope['event']))
    if revoke:service(dict(operation='permit',time=14,app='source-app',device='mock-device-A',allow=False))
    epoch=0
    if reset:epoch=service(dict(operation='reset',time=15,device='mock-device-A'))['epoch']
    bridge_path=None
    if route=='LEAK':
        b=service(dict(operation='bridge',time=predict_at,device='mock-device-A'))
        if 'bridge_receipt' in b:bridge_path=root/'ipc/bridge.json';write(bridge_path,b)
    target_in=root/'ipc/target_input.json';target_out=root/'ipc/target_envelope.json'
    write(target_in,dict(request_id='mock-request-1',device='mock-device-B' if other_device else 'mock-device-A',installation='mock-install-T1',prediction_time=predict_at,epoch=0 if other_device else epoch,purpose='mock-research',context=dict(country='MOCK',model='mock-device',placement='mock-slot')))
    args=['--input',target_in,'--output',target_out]
    if bridge_path:args+=['--bridge',bridge_path]
    child('mock76.app_target',args);target=read(target_out)
    response=service(dict(operation='predict',time=predict_at,request=target['request']))
    service(dict(operation='close',time=predict_at+1))
    packet=dict(view='complete_local_audit',records=Ledger(root/'audit/ledger.jsonl').records());write(root/'audit/packet.json',packet)
    child('mock76.auditor',['--input',root/'audit/packet.json','--output',root/'audit/verdict.json'])
    external=dict(view='external_only',observations=[response]);write(root/'audit/external_packet.json',external)
    child('mock76.auditor',['--input',root/'audit/external_packet.json','--output',root/'audit/external_verdict.json'])
    write(root/'private/truth.json',dict(route=route,seed=seed,fixture_only=True))
    return dict(root=str(root),response=response,verdict=read(root/'audit/verdict.json'),external_verdict=read(root/'audit/external_verdict.json'))

def main():
    install(allow_child=True);p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--seed',type=int,default=760031);a=p.parse_args()
    root=Path(a.output).resolve();root.mkdir(parents=True,exist_ok=False)
    # Hidden fixture routing is randomized only for operator labels;auditor receives no truth.
    routes=['D0','D1','LEAK'];random.Random(a.seed).shuffle(routes);summary=[]
    for i,route in enumerate(routes):
        x=execute_case(root/f'run-{i+1}',route,a.seed)
        summary.append(dict(run=f'run-{i+1}',response=x['response'],verdict=x['verdict'],external_verdict=x['external_verdict']))
    write(root/'summary.json',dict(seed=a.seed,runs=summary,fixture_truth_location='each run private/truth.json;not passed to auditor',scope='Offline CLI mock only;not Android/iOS binaries'))
    print(json.dumps(dict(status='PASS_LOCAL_DEMO',runs=len(summary),output=str(root)),ensure_ascii=False))

if __name__=='__main__':main()
