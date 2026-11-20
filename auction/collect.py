"""Public documentation GET only. No ad requests, credentials, cookies or SDK execution."""
from pathlib import Path
import sys,importlib.util
spec=importlib.util.spec_from_file_location('identity_public_collect',Path(__file__).resolve().parents[1]/'identity-graph/collect.py')
base=importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.R=Path(__file__).resolve().parent
base.R.mkdir(parents=True,exist_ok=True)
if __name__=='__main__':
 base.batch('protocol-initial',{
  'al-exchange':'https://support.applovin.com/en/partners/ad-exchange',
  'al-bid-request':'https://support.applovin.com/en/partners/ad-exchange/integrations/bid-request',
  'al-bid-response':'https://support.applovin.com/en/partners/ad-exchange/integrations/bid-response',
  'al-ortb':'https://support.applovin.com/en/partners/ad-exchange/openrtb-specification',
  'al-doc-index':'https://support.applovin.com/llms.txt',
  'unity-response':'https://docs.unity.com/en-us/grow/programmatic/unity-exchange/bid-responses.md',
  'unity-overview':'https://docs.unity.com/en-us/grow/programmatic/unity-exchange.md',
  'unity-macros':'https://docs.unity.com/en-us/grow/programmatic/unity-exchange/macros.md',
  'unity-errors':'https://docs.unity.com/en-us/grow/programmatic/unity-exchange/error-codes.md',
  'unity-start':'https://docs.unity.com/en-us/grow/programmatic/unity-exchange/integration-guide.md',
 })
