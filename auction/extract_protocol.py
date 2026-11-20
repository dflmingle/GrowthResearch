"""Extract every documented field row, with source heading and exact description."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,re,hashlib
R=Path(__file__).resolve().parent;ROOT=R.parent
rows=[]
sources=[('AppLovin','request',R/'al-request.raw'),('AppLovin','response',R/'al-response.raw'),
 ('Unity','request',ROOT/'identity-graph/unity-exchange-identity.raw'),('Unity','response',R/'unity-response.raw'),
 ('Unity','privacy',ROOT/'identity-graph/unity-exchange-privacy.raw'),('Unity','skan',R/'unity-ios.raw'),('Unity','loss',R/'unity-loss.raw')]
for vendor,kind,p in sources:
 s=p.read_text(encoding='utf-8');sha=hashlib.sha256(p.read_bytes()).hexdigest()
 if vendor=='AppLovin':
  soup=BeautifulSoup(s,'html.parser');heading='';table_index=0
  for node in soup.find_all(['h1','h2','h3','h4','table']):
   if node.name!='table':heading=node.get_text(' ',strip=True);continue
   table_index+=1
   for ri,tr in enumerate(node.find_all('tr')):
    cells=[x.get_text(' ',strip=True) for x in tr.find_all(['th','td'])]
    if ri==0 or len(cells)<2:continue
    field=cells[0]
    if not field:continue
    rows.append(dict(vendor=vendor,kind=kind,section=heading,field=field,cells=cells,
      source=p.relative_to(ROOT).as_posix(),sha256=sha,table_index=table_index,row=ri))
 else:
  heading=''
  # Markdown includes fenced multiline examples INSIDE cells; do not stop at their newlines.
  lines=s.splitlines();i=0
  while i<len(lines):
   l=lines[i]
   if l.startswith('#'):heading=l.lstrip('# ').split('##')[0]
   if l.startswith('|'):
    if re.match(r'^\|[ :\-|]+\|',l) or re.match(r'^\|\s*\*\*',l):i+=1;continue
    j=i;parts=[l]
    while not parts[-1].rstrip().endswith('|') and i+1<len(lines) and not lines[i+1].startswith(('|','#')):
     i+=1;parts.append(lines[i])
    full=' '.join(parts)
    cells=[x.strip() for x in re.split(r'(?<!\\)\|',full)[1:-1]]
    if len(cells)>=2:
     rows.append(dict(vendor=vendor,kind=kind,section=heading,field=cells[0].strip('` '),cells=cells,
      source=p.relative_to(ROOT).as_posix(),sha256=sha,start_line=j+1,end_line=i+1))
   i+=1
(R/'PROTOCOL_FIELDS.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
md='# 官方协议逐字段目录\n\n自动提取表格的全部行，不代表全部行均为生产启用字段。原始描述/条件保留，非表格限制仍须读正文。AppLovin为HTML原表；Unity为Markdown原表；宏和tracking表单列保留。\n'
for vendor,kind,_ in sources:
 subset=[x for x in rows if x['vendor']==vendor and x['kind']==kind]
 md+=f'\n## {vendor} / {kind}（{len(subset)}行）\n\n| 原始章节 | 字段/项 | 原始表格其他单元 | 来源位置 |\n|---|---|---|---|\n'
 for x in subset:
  clean=lambda v:v.replace('|','\\|').replace('\n',' ')
  loc=f'table {x["table_index"]}, row {x["row"]}' if 'table_index'in x else f'line {x["start_line"]}'
  md+=f'| {clean(x["section"])} | {clean(x["field"])} | {clean(" / ".join(x["cells"][1:]))} | [{loc}](../{x["source"]}) |\n'
(R/'PROTOCOL_FIELDS.md').write_text(md,encoding='utf-8')
print('Rows',len(rows))
for v,k,_ in sources: print(v,k,len([x for x in rows if x['vendor']==v and x['kind']==k]))
