from pathlib import Path
import json,zipfile,subprocess,re,sys,gc
from androguard.core.dex import DEX
from loguru import logger
logger.remove();R=Path(__file__).resolve().parent;sys.stdout.reconfigure(encoding='utf-8')
targets={
 'meowdoku':r'^com\.learnings\.(analyze\.(UUIDManager|AnalyzeManager)|unikit\.(LearningsKit|module\.(UserTagModule|AuthModule|AdModule))|auth\.(LxAuth|ServerLoginExecutor)|auth\.platform\.GuestAuthProvider)$|^com\.meevii\.(adsdk\.bridge\.Uid2PluginManager|abtest\.business\.AbAccountIdManager|adsdk\..*Uid2.*)$|^com\.learnings\.usertag\.util\.PackageUtils$',
 'rotate-rings':r'^com\.hurelax\.datareport\..*WThinkingDataAdapter$|^com\.facebook\.appevents\.gps\.pa\.PACustomAudienceClient$|^com\.unity3d\.player\.other\.model\.Admodel\$ActUserInfo$|^f8\.g$|^com\.inmobi\.unifiedId\.InMobiUnifiedIdService$',
 'jewel-coloring':r'^r9\.h$|^n9\.a$|^com\.facebook\.appevents\.b\.AdSourceUtils$|^com\.facebook\.appevents\.b\..*|^m9\.a$|^common\.platform$|^com\.inmobi\.unifiedId\.InMobiUnifiedIdService$',
}
for slug,pat in targets.items():
 base=R/slug/'static';apk=next(p for p in (base/'splits').glob('*.apk') if 'classes.dex' in zipfile.ZipFile(p).namelist());z=zipfile.ZipFile(apk)
 for dex in sorted(n for n in z.namelist() if re.fullmatch(r'classes\d*\.dex',n)):
  b=z.read(dex);d=DEX(b);matched=[c.get_name()[1:-1].replace('/','.') for c in d.get_classes() if re.search(pat,c.get_name()[1:-1].replace('/','.'))];del d;gc.collect()
  if not matched:continue
  dest=R/slug/'deep/java'/dex;dest.mkdir(parents=True,exist_ok=True);inp=R/slug/'deep/dex'/dex;inp.parent.mkdir(exist_ok=True);inp.write_bytes(b)
  with (dest/'jadx.log').open('w',encoding='utf-8') as log:
   p=subprocess.run(['java','-Xmx1000m','-cp',str(R)+';C:/Users/89trillion/game/tower-forge/tools/jadx-headless-mcp-0.7.1-all.jar','SelectJadx',str(inp),str(dest),'^(?:'+'|'.join(re.escape(n) for n in matched)+')$',str(len(matched))],stdout=log,stderr=subprocess.STDOUT,timeout=100)
  print(slug,dex,'classes',len(matched),'exit',p.returncode,flush=True)
