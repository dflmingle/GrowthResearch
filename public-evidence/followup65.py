from collect65 import *
if __name__=='__main__':
    targets=[
     ('obd-readme','https://raw.githubusercontent.com/st-tech/zr-obp/master/obd/README.md'),
     ('obd-files','https://api.github.com/repos/st-tech/zr-obp/contents/obd'),
     ('obd-license','https://raw.githubusercontent.com/st-tech/zr-obp/master/obd/LICENSE'),
     ('obd-random-sample','https://raw.githubusercontent.com/st-tech/zr-obp/master/obd/random/all.csv'),
     ('kuairand-record','https://zenodo.org/api/records/10439422'),
     ('mobile-ltv-readme','https://raw.githubusercontent.com/rizz045/mobile_games_LTV/main/README.md'),
     ('mobile-ltv-files','https://api.github.com/repos/rizz045/mobile_games_LTV/contents'),
     ('zenodo-game-data','https://zenodo.org/api/records?q=resource_type.type%3Adataset%20AND%20game%20AND%20revenue&size=8'),
     ('zenodo-ltv-paper-code','https://zenodo.org/api/records/23133796'),
     ('ipinyou-original','http://bunwell.cs.ucl.ac.uk/ipinyou.contest.dataset.zip'),
     ('rotate-history-page','https://rotate-rings-nebula-studio.en.aptoide.com/versions'),
     ('ads-google','https://adstransparency.google.com/?region=anywhere&search=com.nebula.rotaterings'),
     ('ads-tiktok','https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en?keyword=Meowdoku'),
     ('ads-meta','https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q=Meowdoku&search_type=keyword_unordered'),
    ]
    with ThreadPoolExecutor(max_workers=5) as pool:
        records=[f.result() for f in as_completed([pool.submit(fetch,t) for t in targets])]
    (BASE/'FOLLOWUP_LEDGER.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps([{k:x.get(k) for k in ['id','status','bytes','error']} for x in records],ensure_ascii=True,indent=2))
