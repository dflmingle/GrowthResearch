"""Adaptive static follow-up, reuse public artifacts without SDK execution."""
from pathlib import Path
import importlib.util, concurrent.futures, json
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('collect',R/'collect.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
tasks=[('max-history-cache','AppLovin/MAX/13.6.4',r'^com\.applovin\.impl\.(?:g5|y3|w3|x3|c5)$',8),
       ('lp-follow','Unity/LevelPlay/9.5.0',r'^com\.ironsource\.(?:C0118g2|g2|C0318q3|q3|C0263n3|n3)$',8)]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(m.decompile,tasks))
m.save(R/'DECOMPILE_FOLLOWUP.json',rows)
print([(x['name'],x['exit_code'],len(x['source_files'])) for x in rows])
