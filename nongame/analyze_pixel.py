"""Static string-table recovery only. Does not execute any downloaded JavaScript."""
from pathlib import Path
import re,ast,json,hashlib
from fractions import Fraction
R=Path(__file__).resolve().parent
p=R/'pixel-source.raw';s=p.read_text(encoding='utf-8')
body=s.split('function a0_0x3f86(){let e=[',1)[1].split('];return(a0_0x3f86=',1)[0]
tokens=re.findall(r'"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27',body)
table=[ast.literal_eval(t) for t in tokens]
def num(index,shift):
 v=table[(index-174+shift)%len(table)]
 m=re.match(r'^[+-]?\d+',v)
 if not m:raise ValueError(v)
 return Fraction(int(m.group()))
matches=[]
for shift in range(len(table)):
 try:
  n=lambda i:num(i,shift)
  x=n(603)*(n(217)/2)+n(311)/3+n(317)/4*(n(646)/5)+n(227)/6-n(494)/7-n(369)/8*(n(617)/9)-n(244)/10*(n(238)/11)
  if x==915260:matches.append(shift)
 except ValueError:pass
assert len(matches)==1,matches
shift=matches[0]
mapping={str(i+174):table[(i+shift)%len(table)] for i in range(len(table))}
(R/'pixel-string-table.json').write_text(json.dumps({'source':'pixel-source.raw','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'scope':'static table recovery by reproducing bounded array rotation arithmetic; no JS execution','rotation':shift,'mapping':mapping},ensure_ascii=False,indent=2),encoding='utf-8')
# Only the named decoder and its global w alias, not ambiguous local aliases.
resolved=re.sub(r'\b(?:a0_0x5ab4|w)\((\d+)\)',lambda m:json.dumps(mapping[m[1]],ensure_ascii=False),s)
(R/'pixel-partial-static.js').write_text('// STATIC DERIVATIVE; DO NOT EXECUTE. Only global decoder references replaced.\n'+resolved,encoding='utf-8')
terms=['https://b.applovin.com/v1/pixel','https://cm.g.doubleclick.net','autoEmailCapture','autoCapture','page_view','user_data','dedupe_id','sendBeacon','operationQueue','SHA-256','_axwrt','page_click','page_session','setTimeout']
snips=[]
for term in terms:
 for m in list(re.finditer(re.escape(term),s))[-3:]:
  snips.append({'term':term,'character_offset':m.start(),'original':s[max(0,m.start()-180):m.end()+260]})
(R/'PIXEL_STATIC_EVIDENCE.json').write_text(json.dumps({'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'limitations':'Literal presence and bounded excerpts; optional configuration branches are not production enabled proof. No downloaded code executed.','excerpts':snips},ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS unique rotation',shift,'strings',len(table),'excerpts',len(snips))
