import unittest
from dataclasses import replace
from auction_model import Auction,Offer,Profile,PROFILES,D,value_bid,request_fixture,response_fixture,offer_from_response

class AuctionChecks(unittest.TestCase):
 def test_first_price_is_not_runner_up(self):
  for p in PROFILES.values():
   r=Auction(p).run([Offer('a',D('12')),Offer('b',D('8'))])
   self.assertEqual((r.selected,r.billed_usd),('a',D('.012')))
 def test_response_fixture_round_trip(self):
  for name,p in PROFILES.items():
   response=response_fixture(Offer('a',D('12.125')),name)
   o=offer_from_response(response,'a')
   self.assertEqual(Auction(p).run([o]).billed_usd,D('.012125'))
 def test_floor_difference_is_explicit(self):
  for p in PROFILES.values():
   r=Auction(p).run([Offer('a',D('3'))],floor=D('3'))
   self.assertEqual(r.rendered,not p.strict_floor)
 def test_parallel_timeout_on_shared_clock(self):
  r=Auction(PROFILES['unity']).run([Offer('a',D('99'),latency_ms=201),Offer('b',D('5'),latency_ms=199)])
  self.assertEqual(r.selected,'b');self.assertEqual(r.rejected['a'],'timeout')
 def test_tmax_is_request_configurable(self):
  r=Auction(PROFILES['unity']).run([Offer('a',D('9'),latency_ms=450)],tmax_ms=500)
  self.assertTrue(r.rendered)
 def test_loaded_unseen_ad_not_billed(self):
  for p in PROFILES.values():
   for override in [dict(load_ok=False),dict(render=False),dict(display_delay_s=14401)]:
    r=Auction(p).run([Offer('a',D('12'),**override)])
    self.assertEqual(r.billed_usd,0);self.assertFalse(r.rendered)
 def test_invalid_higher_bid_does_not_win(self):
  for p in PROFILES.values():
   for bad in [dict(cpm=D('NaN')),dict(cpm=D('-1')),dict(crid=''),dict(adm=''),dict(blocked=True),dict(impid='other'),dict(request_id='wrong')]:
    o=replace(Offer('a',D('99')),**bad)
    r=Auction(p).run([o,Offer('b',D('5'))]);self.assertEqual(r.selected,'b')
 def test_budget_and_duplicate_billing(self):
  for p in PROFILES.values():
   a=Auction(p);b={'a':D('.1')};o=Offer('a',D('12'))
   first=a.run([o],budgets=b);second=a.run([o],budgets=b)
   self.assertEqual(first.billed_usd,D('.012'));self.assertEqual(second.billed_usd,0)
   self.assertEqual(b['a'],D('.088'))
 def test_insufficient_budget_rejects_offer(self):
  r=Auction(PROFILES['unity']).run([Offer('a',D('12'))],budgets={'a':D('.005')})
  self.assertEqual(r.rejected['a'],'budget_limit')
 def test_win_notice_stage_differs_without_display(self):
  for p in PROFILES.values():
   r=Auction(p).run([Offer('a',D('12'),render=False)])
   self.assertEqual(any(x['kind']=='win' for x in r.notices),p.name=='applovin')
   self.assertEqual(r.billed_usd,0)
 def test_notifications_do_not_multiply_spend(self):
  for p in PROFILES.values():
   r=Auction(p).run([Offer('a',D('12'),imptrackers=('https://track.invalid/imp',))])
   self.assertEqual(sum(x['kind']=='billing' for x in r.notices),1)
 def test_currency_normalization_not_blind_comparison(self):
  p=Profile('unity',200,False,response_currency='CNY',usd_per_currency=D('.14'))
  r=Auction(p).run([Offer('a',D('100'),currency='CNY')])
  self.assertEqual(r.billed_usd,D('.014'))
  self.assertEqual(Auction(PROFILES['unity']).run([Offer('a',D('100'),currency='CNY')]).rejected['a'],'unconfigured_currency')
 def test_al_currency_is_usd_contract(self):
  r=Auction(PROFILES['applovin']).run([Offer('a',D('12'),currency='CNY')])
  self.assertEqual(r.billed_usd,D('.012'))
 def test_required_notice_routes(self):
  self.assertEqual(Auction(PROFILES['applovin']).run([Offer('a',D('5'),burl=None)]).rejected['a'],'missing_billing_url')
  self.assertTrue(Auction(PROFILES['unity']).run([Offer('a',D('5'),burl=None,imptrackers=('https://track.invalid/imp',))]).rendered)
 def test_value_and_roas_direction(self):
  self.assertEqual(value_bid('.02','1'),D('20'))
  self.assertEqual(value_bid('.02','2'),D('40'))
  self.assertEqual(value_bid('.02','1',target_roas='2'),D('10'))
 def test_privacy_fixture_no_linking_id_when_declined(self):
  for p in PROFILES:
   r=request_fixture(p,False);self.assertNotIn('ifa',r['device']);self.assertNotIn('ip',r['device'])
 def test_al_response_size_limit(self):
  self.assertEqual(Auction(PROFILES['applovin']).run([Offer('a',D('5'),response_bytes=4097)]).rejected['a'],'response_too_large')

if __name__=='__main__':unittest.main(verbosity=2)
