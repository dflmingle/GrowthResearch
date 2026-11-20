"""Target App T:base requests;an explicit optional bridge is the leak fixture."""
import argparse
from .safety import install,mock_key
from .io import read,write

def request(spec,bridge=None):
    if set(spec)!={'request_id','device','installation','prediction_time','epoch','context','purpose'}:raise ValueError('Target schema mismatch')
    for k in ['request_id','device','installation']:mock_key(spec[k])
    if set(spec['context'])!={'country','model','placement'}:raise ValueError('Target context allowlist')
    if spec['context']!={'country':'MOCK','model':'mock-device','placement':'mock-slot'}:raise ValueError('No real advertising context accepted')
    if spec['purpose']!='mock-research':raise ValueError('Purpose mismatch')
    msg=dict(actor='target-app',operation='predict',request=dict(spec))
    msg['request']['context']=dict(spec['context'])
    if bridge is not None:
        if bridge.get('category') not in [0,1] or bridge.get('purpose')!=spec['purpose']:raise ValueError('Bridge fixture invalid')
        if bridge.get('device')!=spec['device'] or bridge.get('epoch')!=spec['epoch'] or bridge.get('valid_at')!=spec['prediction_time']:raise ValueError('Bridge scope or time invalid')
        msg['request']['context']['source_category']=bridge['category']
        msg['request']['context']['bridge_receipt']=bridge['bridge_receipt']
    return msg

def main():
    install();p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.add_argument('--bridge');a=p.parse_args()
    write(a.output,request(read(a.input),read(a.bridge) if a.bridge else None))
if __name__=='__main__':main()
