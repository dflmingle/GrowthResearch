"""Source App S process. No target storage,service truth or network dependencies."""
import argparse
from .safety import install,mock_key
from .io import read,write

def emit(spec):
    allowed={'event_id','device','installation','event_time','available_at','category','purpose','epoch'}
    if set(spec)!=allowed:raise ValueError('Source schema mismatch')
    for k in ['event_id','device','installation']:mock_key(spec[k])
    if spec['purpose']!='mock-research' or spec['category'] not in [0,1]:raise ValueError('Invalid mock event')
    if any(type(spec[k]) is not int for k in ['event_time','available_at','epoch']):raise ValueError('Integer logical times required')
    return dict(actor='source-app',operation='collect',event=spec)

def main():
    install();p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    write(a.output,emit(read(a.input)))
if __name__=='__main__':main()
