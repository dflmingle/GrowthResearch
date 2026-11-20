"""Offline synthetic auction laboratory, NOT either vendor's production implementation.

No networking code. Notice URLs use .invalid and are only strings in local logs.
Document-derived profile differences are separated from explicit modeling choices.
"""
from dataclasses import dataclass,field
from decimal import Decimal,InvalidOperation
from typing import Optional
import json

D=Decimal

@dataclass(frozen=True)
class Profile:
    name: str
    tmax_ms: int
    strict_floor: bool
    response_currency: str='USD'
    usd_per_currency: Decimal=D('1')
    # Unity equality handling and local tie policy are laboratory choices, not proven server rules.

PROFILES={
 'applovin':Profile('applovin',500,True),
 'unity':Profile('unity',200,False), # 200 is this fixture's configured tmax, not a universal Unity limit.
}

@dataclass
class Offer:
    bidder: str
    cpm: Decimal
    latency_ms: int=40
    request_id: str='synthetic-request'
    impid: str='1'
    currency: str='USD'
    adm: str='<div>synthetic creative</div>'
    crid: str='synthetic-creative'
    domain: str='advertiser.invalid'
    seat: str='synthetic-seat'
    category: str='IAB9'
    response_bytes: int=1024
    blocked: bool=False
    load_ok: bool=True
    render: bool=True
    click: bool=False
    display_delay_s: int=2
    cache_ttl_s: int=14400 # Local fixture. Unity TTL is NOT inferred from this value.
    nurl: Optional[str]='https://dsp.invalid/win?price=${AUCTION_PRICE}'
    burl: Optional[str]='https://dsp.invalid/bill?price=${AUCTION_PRICE}'
    lurl: Optional[str]='https://dsp.invalid/loss?reason=${AUCTION_LOSS}'
    imptrackers: tuple=()

@dataclass
class Result:
    selected: Optional[str]=None
    rendered: bool=False
    clearing_cpm_usd: Decimal=D('0')
    billed_usd: Decimal=D('0')
    rejected: dict=field(default_factory=dict)
    notices: list=field(default_factory=list)

class Auction:
    def __init__(self,profile:Profile):
        self.profile=profile
        self.billed_keys=set()

    def normalized_price(self,o):
        if self.profile.name=='applovin':
            # Published AL contract ignores cur; numerical price is USD.
            return D(o.cpm)
        if o.currency!=self.profile.response_currency:
            raise ValueError('unconfigured_currency')
        return D(o.cpm)*self.profile.usd_per_currency

    def invalid(self,o,floor,tmax,request_id,budgets):
        if o.latency_ms>tmax:return 'timeout'
        if o.request_id!=request_id:return 'request_id_mismatch'
        if o.impid!='1':return 'impid_mismatch'
        try:
            price=self.normalized_price(o)
        except (ValueError,InvalidOperation):return 'unconfigured_currency'
        if not price.is_finite() or price<=0:return 'invalid_price'
        if price<floor or (self.profile.strict_floor and price==floor):return 'below_floor'
        if not o.adm or not o.crid or not o.category:return 'missing_creative_fields'
        if not o.domain or '/' in o.domain or o.domain.startswith('www.'):return 'invalid_domain'
        if o.blocked:return 'publisher_block'
        if self.profile.name=='applovin':
            if o.response_bytes>4096:return 'response_too_large'
            if not o.burl:return 'missing_billing_url'
        else:
            if not o.seat:return 'missing_seat'
            if not o.nurl and not o.burl:return 'missing_win_or_billing_url'
            if not o.burl and not o.imptrackers:return 'missing_billing_url_or_imptrackers'
        if budgets is not None and price/D('1000')>budgets.get(o.bidder,D('0')):return 'budget_limit'
        return None

    def run(self,offers,floor=D('1'),tmax_ms=None,request_id='synthetic-request',budgets=None):
        result=Result();valid=[]
        for o in offers:
            reason=self.invalid(o,floor,tmax_ms if tmax_ms is not None else self.profile.tmax_ms,request_id,budgets)
            if reason:result.rejected[o.bidder]=reason
            else:valid.append(o)
        # All latency values share one request clock. No sequential accumulated DSP waiting.
        valid.sort(key=lambda o:(-self.normalized_price(o),o.bidder))
        # Alphabetical tie handling is explicitly local; production ties are unknown.
        if not valid:
            for o in offers:
                if o.lurl:result.notices.append(dict(kind='loss',bidder=o.bidder,reason=result.rejected.get(o.bidder,'no_bid')))
            return result
        winner=valid[0];result.selected=winner.bidder
        result.clearing_cpm_usd=self.normalized_price(winner)
        if self.profile.name=='applovin' and winner.load_ok and winner.nurl:
            result.notices.append(dict(kind='win',bidder=winner.bidder,stage='load_success',
                                      clearing_cpm_usd=str(result.clearing_cpm_usd)))
        # Deliberately do not implement vendor failover/reauction after failed load.
        if not winner.load_ok or not winner.render or winner.display_delay_s>winner.cache_ttl_s:
            reason='load_failed' if not winner.load_ok else ('expired' if winner.display_delay_s>winner.cache_ttl_s else 'not_rendered')
            for o in offers:
                if o.lurl:result.notices.append(dict(kind='loss',bidder=o.bidder,reason=reason if o is winner else result.rejected.get(o.bidder,'higher_bid')))
            return result
        result.rendered=True
        for o in offers:
            if o is winner:continue
            if o.lurl:result.notices.append(dict(kind='loss',bidder=o.bidder,reason=result.rejected.get(o.bidder,'higher_bid'),
                                             clearing_cpm_usd=str(result.clearing_cpm_usd) if self.profile.name=='applovin' else None))
        if winner.nurl and self.profile.name=='unity':
            result.notices.append(dict(kind='win',bidder=winner.bidder,
                stage='render',
                clearing_cpm_usd=str(result.clearing_cpm_usd)))
        key=(request_id,winner.bidder,winner.crid)
        if key not in self.billed_keys:
            self.billed_keys.add(key)
            result.billed_usd=result.clearing_cpm_usd/D('1000')
            if budgets is not None:budgets[winner.bidder]-=result.billed_usd
            # A single accounting event even when multiple tracking callbacks exist.
            result.notices.append(dict(kind='billing',bidder=winner.bidder,stage='render',
                amount_usd=str(result.billed_usd),route='burl' if winner.burl else 'imptrackers'))
        if winner.click:result.notices.append(dict(kind='click',bidder=winner.bidder))
        return result

def value_bid(p_install,predicted_iaa_ltv,predicted_iap_ltv=D('0'),target_roas=D('1'),pacing=D('1'),shade=D('1')):
    """Illustrative economic ceiling, NOT a recovered Axon/Vector formula."""
    p=D(str(p_install));iaa=D(str(predicted_iaa_ltv));iap=D(str(predicted_iap_ltv));roas=D(str(target_roas))
    if not D('0')<=p<=D('1') or min(iaa,iap)<0 or roas<=0:raise ValueError('invalid economic assumption')
    return D('1000')*p*(iaa+iap)/roas*D(str(pacing))*D(str(shade))

def request_fixture(profile,consent=True):
    """Representative subset, not a captured or full production payload."""
    p=PROFILES[profile]
    req=dict(id='synthetic-request',at=1,tmax=p.tmax_ms,
             app=dict(id='synthetic-app',bundle='example.synthetic.publisher',publisher=dict(id='synthetic-publisher')),
             imp=[dict(id='1',bidfloor=1.0,instl=1,tagid='synthetic-placement',banner=dict(w=320,h=480))],
             device=dict(os='android',model='SYNTHETIC',lmt=0 if consent else 1))
    if consent:req['device'].update(ifa='SYNTHETIC-NOT-A-REAL-AD-ID',ip='192.0.2.10')
    if profile=='applovin':
        req['user']=dict(ext=dict(consent=int(consent)))
        if consent:req['user']['id']='synthetic-app-scoped-user'
        req['imp'][0].update(exp=14400,rwdd=0,ext=dict(ad_unit_name='synthetic-unit'))
    else:
        req['user']=dict(ext=dict(consent=str(int(consent))))
        req['source']=dict(ext=dict(header_bidding=1,fd=1))
    return req

def response_fixture(o,profile):
    """One synthetic DSP seat/bid. Not a complete vendor validator or captured response."""
    bid=dict(id='synthetic-bid-'+o.bidder,impid=o.impid,price=float(o.cpm),adm=o.adm,
             crid=o.crid,adomain=[o.domain],cat=[o.category],bundle='example.synthetic.advertiser',
             ext=dict(crtype='HTML'))
    for name in ['nurl','burl','lurl']:
        if getattr(o,name):bid[name]=getattr(o,name)
    if o.imptrackers:bid['ext']['imptrackers']=list(o.imptrackers)
    return dict(id=o.request_id,cur=o.currency,seatbid=[dict(seat=o.seat,bid=[bid])])

def offer_from_response(response,bidder,latency_ms=40,**lifecycle):
    """Parse the local one-seat/one-bid fixture; lifecycle is outside OpenRTB JSON."""
    seat=response['seatbid'][0];bid=seat['bid'][0]
    return Offer(bidder=bidder,cpm=D(str(bid['price'])),latency_ms=latency_ms,
                 request_id=response['id'],impid=bid['impid'],currency=response.get('cur','USD'),
                 adm=bid.get('adm',''),crid=bid.get('crid',''),domain=bid.get('adomain',[''])[0],
                 category=bid.get('cat',[''])[0],seat=seat.get('seat',''),
                 response_bytes=len(json.dumps(response).encode()),nurl=bid.get('nurl'),
                 burl=bid.get('burl'),lurl=bid.get('lurl'),imptrackers=tuple(bid.get('ext',{}).get('imptrackers',[])),**lifecycle)
