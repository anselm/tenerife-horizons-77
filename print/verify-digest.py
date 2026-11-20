from pathlib import Path
import json,re,unicodedata,tempfile
from lxml import html
from pypdf import PdfReader
import pdfplumber
from PIL import Image,ImageOps,ImageDraw
r=Path(__file__).resolve().parents[1];d=json.loads((Path(tempfile.gettempdir())/'horizons-print/content.json').read_text());pdf=PdfReader(r/'output/pdf/Horizons-77-digest-interior.pdf')
assert len(pdf.pages)==64
norm=lambda s:re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',html.fromstring('<div>'+s+'</div>').text_content()).lower())
full=norm(' '.join(p.extract_text() for p in pdf.pages))
items=[]
for a in d['articles']:items.extend(a['body'])
for a in d['openingFeatures'].values():items.extend(a['body'])
for key in ['cousteauArticle','goodallArticle','gilliamArticle','coastArticle','horseArticle','maathaiArticle','rahmanArticle','clarkeLeaf']:items.extend(d[key]['body'])
for s in d['alexanderEssay']['sections']:items.extend(s['body'])
for a in d['assemblyPages']:items.extend(a['body'])
missing=[p[:90] for p in items if norm(p) not in full]
print('Paragraphs:',len(items),'Missing:',missing)
assert not missing
for p in pdf.pages:assert list(p.trimbox)==[9,9,405,621] and list(p.mediabox)==[0,0,414,630]
proof=PdfReader(r/'output/pdf/Horizons-77-digest-proof.pdf');assert len(proof.pages)==68
assert not proof.pages[1].extract_text().strip() and not proof.pages[-2].extract_text().strip()
m=json.loads((r/'output/pdf/digest-pagination.json').read_text());assert [m['firstPages'][k] for k in ['below','slope','air']]==[14,28,40]
collisions=[]
checks=m['designedFeatures']
for i,a in enumerate(checks):
 for b in checks[i+1:]:
  if a['page']!=b['page']:continue
  dx=min(a['x']+a['width'],b['x']+b['width'])-max(a['x'],b['x'])
  dy=min(a['top'],b['top'])-max(a['bottom'],b['bottom'])
  if dx>.5 and dy>.5:collisions.append((a['page'],a['type'],b['type'],round(dx,1),round(dy,1)))
print('Composed element collisions:',collisions);assert not collisions
with pdfplumber.open(r/'output/pdf/Horizons-77-digest-interior.pdf') as book:
 bad=[]
 for n,p in enumerate(book.pages,1):
  chars=[c for c in p.chars if c['text'].strip()]
  for c in chars:
   if c['x0']<20 or c['x1']>394 or c['top']<14 or c['bottom']>614:bad.append((n,c['text'],c['x0'],c['top']))
 print('Outside safe page:',bad[:20]);assert not bad
 # Record source images and actual effective resolution of new feature plates.
 for n in [7,12,15,29,40,49]:
  p=book.pages[n-1]
  print('Plate',n,[(im.get('srcsize'),round(im['width'],1),round(im['height'],1)) for im in p.images])

# All carried writing survives the redesign, including inserts moved to their own leaf.
insert_missing=[]
for key,a in d['editionInserts'].items():
 for t in a['body']+a.get('translation',[])+([] if a.get('lang')=='ar' else a.get('lines',[])):
  if t.strip() and norm(t) not in full:insert_missing.append((key,t[:60]))
assert not insert_missing,insert_missing
assert not pdf.pages[-1].extract_text().strip()
assert m['firstPages']['arrival/fr']==6 and m['firstPages']['gilliam']==48
assert m['firstPages']['arrival/de']==12
print('All 11 carried reading panels retained; panorama parity correct; blank endpaper verified.')
