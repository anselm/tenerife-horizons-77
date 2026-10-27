import json,re,html,math,os
from urllib.parse import urlparse
from pathlib import Path
from lxml import html as LH
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.colors import HexColor,CMYKColor
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage
from pypdf import PdfReader,PdfWriter,Transformation
ROOT=Path(os.environ.get('HORIZONS_ROOT',Path(__file__).resolve().parents[1])); TMP=Path(os.environ.get('HORIZONS_PRINT_TMP','/private/tmp/horizons-print'));OUT=ROOT/'output'/'pdf';OUT.mkdir(exist_ok=True,parents=True)
D=json.loads((TMP/'content.json').read_text())
F=os.environ.get('HORIZONS_FONT_DIR','/System/Library/Fonts/Supplemental/')+'/'
for name,file in [('G','Georgia.ttf'),('GI','Georgia Italic.ttf'),('GB','Georgia Bold.ttf'),('A','Arial.ttf'),('AB','Arial Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,F+file))
pdfmetrics.registerFontFamily('G',normal='G',bold='GB',italic='GI',boldItalic='GI')
pdfmetrics.registerFontFamily('A',normal='A',bold='AB',italic='A',boldItalic='AB')
W,H=612,792;INK=CMYKColor(0,0,0,.88);RUST=CMYKColor(0,.65,.78,.32);TEAL=CMYKColor(.65,.12,.1,.63);GRAY=CMYKColor(0,0,0,.45)
C=None;N=0;fitlog=[]
def clean(t):
 t=html.unescape(t).replace('\u00a0',' ').replace('↔',' / ').replace('→',' / ').replace('↗',' / ').replace('↘',' / ').replace('☼','*').replace('□','[ ]')
 return t

def plain(t):return clean(LH.fromstring('<div>'+t+'</div>').text_content())
def para(t,size=11,leading=None,font='G',color=INK,space=10):
 t=clean(t);t=re.sub(r'<a\b[^>]*>(.*?)</a>',r'\1',t,flags=re.S);t=re.sub(r'<span[^>]*>|</span>','',t);t=t.replace('<br>','<br/>')
 # prevent short paragraph-final single words while preserving markup
 if '<' not in t:
  m=re.search(r'(\S+)\s+(\S+)$',t)
  if m and len(m.group())<23:t=t[:m.start()]+m.group(1)+'\u00a0'+m.group(2)
 return Paragraph(t,ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.42,textColor=color,spaceAfter=space,allowWidows=0,allowOrphans=0,splitLongWords=0))
def text(t,x,y,size=10,font='A',color=INK):
 C.setFillColor(color);C.setFont(font,size);C.drawString(x,y,clean(t))
def rule(y,x=44,width=524):C.setStrokeColor(GRAY);C.setLineWidth(.45);C.line(x,y,x+width,y)
def page(title,section='CONFERENCE EDITION',folio=True):
 global N
 N+=1;C.setFillColorCMYK(0,0,0,0);C.rect(0,0,W,H,fill=1,stroke=0)
 if folio:
  text('HORIZONS ’77 / TENERIFE',44,755,7,'A');text(section[:65].upper(),280,755,6.5,'A');rule(744)
  rule(43);text('HORIZONS / EDICIÓN DEL CONGRESO / 1977',44,29,6.8,'A');C.setFont('G',11);C.drawRightString(568,28,str(N))
 C.bookmarkPage('p'+str(N));C.addOutlineEntry(title,'p'+str(N),0)
def finish():C.showPage()
def titleblock(title,deck='',tag='',author='',continued=False):
 y=718
 if tag:text(tag.upper(),44,y,7.3,'AB');y-=25
 size=30 if not continued else 25
 while True:
  p=para(title,size,size*1.06,'GI' if continued else 'G',space=0);w,h=p.wrap(524,180)
  if h<100:break
  size-=1
 p.drawOn(C,44,y-h);y-=h+13
 if deck:
  p=para(deck,12.5,17,'GI');w,h=p.wrap(500,120);p.drawOn(C,44,y-h);y-=h+12
 if author:text(author,44,y,8,'A');y-=18
 return y

def image(path,x,y,w,h,crop=False):
 # Use high-quality RGB JPEGs to keep the rush files easy to transfer.
 path=Path(path);cached=TMP/('press-'+path.stem+'.jpg')
 if not cached.exists() or path.stat().st_mtime>cached.stat().st_mtime:
  src=PILImage.open(path).convert('RGB');src.save(cached,quality=94,subsampling=0,optimize=True)
 im=ImageReader(str(cached));iw,ih=im.getSize();s=min(w/iw,h/ih);dw,dh=iw*s,ih*s
 C.drawImage(im,x+(w-dw)/2,y+(h-dh)/2,dw,dh,mask='auto')
def art(kind,top,h=165):
 y=top-h
 if kind in ['landscape','coast','observatory']:
  name={'landscape':'tenerife.png','coast':'montana-amarilla-v2.png','observatory':'ocean-observatory.png'}[kind];image(ROOT/'assets'/name,44,y,524,h)
 elif kind in ['habitat','airlift']:image(TMP/(kind+'.png'),44,y,524,h)
 else:
  C.setFillColor(CMYKColor(.03,.02,.09,0));C.rect(44,y,524,h,fill=1,stroke=0)
  label={'nursery':'KENYA / SEED · SOIL · WATER · TENDING','fieldnotes':'GOMBE / OBSERVATION · CONTINUITY · CARE','storyboard':'FILM DESK / THREE VIEWS OF A POSSIBLE ROOM','energy':'FIG. 04 / THE COMMON LEDGER','ledger':'COOPERATIVA DEL PORVENIR','routes':'ISLAS CANARIAS / STUDY 03'}.get(kind,'1977 / 2027')
  text(label,60,top-22,7.5,'A',TEAL)
  if kind=='nursery':
   C.setStrokeColor(TEAL);C.setLineWidth(1)
   for x in [150,305,460]:
    C.line(x,y+40,x,y+92);q=C.beginPath();q.moveTo(x,y+92);q.curveTo(x-35,y+92,x-35,y+115,x,y+105);q.curveTo(x+35,y+128,x+35,y+92,x,y+92);C.drawPath(q)
   text('Leave room to grow.',220,y+17,12,'GI',TEAL)
  elif kind=='storyboard':
   for i,label in enumerate(['BEFORE','IN USE','IN REPAIR']):
    x=61+i*166;C.setStrokeColor(GRAY);C.rect(x,y+43,153,68,fill=0,stroke=1);text(str(i+1),x+10,y+87,21,'G',TEAL);text(label,x+10,y+54,7,'A')
   text('Allow room for the people.',61,y+19,12,'GI')
  elif kind=='energy':
   for i,label in enumerate(['GENERATION','STORAGE','DEMAND','MAINTENANCE']):
    x=60+i*126;text('0'+str(i+1),x,y+85,26,'G',RUST);text(label,x,y+63,7.5,'A')
   text('A column for the night. A place for the person who repairs it.',61,y+24,12,'GI')
  elif kind=='ledger':
   text('A share in the long view.',62,y+84,27,'GI',TEAL);text('CONSTRUCTION     /     MAINTENANCE     /     ACCESS',62,y+50,8,'A');text('PROPOSED SUBSCRIPTION / 1977',62,y+24,7,'A')
  elif kind=='fieldnotes':
   text('1960 — 1977',62,y+76,35,'G',TEAL);text('The forest continues beyond the drawing.',62,y+29,13,'GI')
  else:
   text('1977',65,y+73,58,'G',RUST);text('2027',340,y+35,58,'GI',TEAL)
 text('HORIZONS ’77 / CUADERNO DE TRABAJO',44,y-12,6.5,'A')
 return y-28

def layout(paras,top,bottom=67,size=11,note=None,cols=2,width=524,x=44,draw=True):
 gap=24;cw=(width-gap*(cols-1))/cols;flow=[para(t,size,space=11) for t in paras]
 if note:flow += [para('DEL CUADERNO / WORKSHOP NOTE',7.2,11,'AB',TEAL,7),para(note,9.7,14,'GI',space=7)]
 placements=[]
 for col in range(cols):
  yy=top
  while flow:
   p=flow[0];w,h=p.wrap(cw,yy-bottom)
   if h<=yy-bottom:
    placements.append((p,x+col*(cw+gap),yy-h));yy-=h+p.style.spaceAfter;flow.pop(0)
   else:
    parts=p.split(cw,yy-bottom)
    if len(parts)>1:
     part=parts[0];w,h=part.wrap(cw,yy-bottom);placements.append((part,x+col*(cw+gap),yy-h));flow=parts[1:]+flow[1:]
    break
 if flow:return False
 if draw:
  for p,xx,yy in placements:p.drawOn(C,xx,yy)
 return True

def prose(paras,top,note=None,size=11):
 for sz in [size,size-.25,size-.5,size-.75,size-1,size-1.25]:
  if layout(paras,top,size=sz,note=note,draw=False):
   # Balance columns instead of filling the left column to the foot first.
   low,high=55,top-67
   for _ in range(16):
    mid=(low+high)/2
    if layout(paras,top,bottom=top-mid,size=sz,note=note,draw=False):high=mid
    else:low=mid
   layout(paras,top,bottom=top-high-1,size=sz,note=note);fitlog.append((N,sz));return
 raise Exception('Text overflow on page '+str(N))

sheets=[];first={}
def add(key,title,kind,**kw):
 if key not in first:first[key]=len(sheets)+5
 sheets.append(dict(key=key,title=title,kind=kind,**kw))
def addarticle(a,lang='en'):
 t=D['editorialTranslations'][lang] if a['id']=='arrival' and lang!='en' else a;key='arrival/'+lang if a['id']=='arrival' else a['id'];half=math.ceil(len(t['body'])/2)
 add(key,t['title'],'article',a=a,t=t,body=t['body'][:half],lang=lang)
 add(key+'-continued',t['title'],'continued',a=a,t=t,body=t['body'][half:],lang=lang)
A={a['id']:a for a in D['articles']}
addarticle(A['arrival'])
for lang in ['es','fr','it','de']:addarticle(A['arrival'],lang)
for a in [A['below'],D['cousteauArticle'],D['coastArticle']]:addarticle(a)
add('horse',D['horseArticle']['title'],'horse',a=D['horseArticle'])
for a in [D['goodallArticle'],D['maathaiArticle'],A['slope']]:addarticle(a)
for i,sec in enumerate(D['alexanderEssay']['sections']):add('alexander' if i==0 else 'alexander-'+str(i+1),D['alexanderEssay']['title'],'alexander',part=sec,index=i)
add('rahman',D['rahmanArticle']['title'],'rahman',a=D['rahmanArticle'])
for a in [A['sun'],A['air']]:addarticle(a)
add('atlas','Seven islands. Many futures.','atlas');add('atlas-notes','Each island has a name.','atlas-notes')
for a in [A['credit'],D['gilliamArticle'],A['table']]:addarticle(a)
for k in ['programme','pass','certificate']:add(k,D['docs'][k]['title'],k,a=D['docs'][k])
addarticle(A['afterword'])
assert len(sheets)==45,len(sheets)
first['colophon']=50
contents=[('arrival/en','Editorial / English'),('arrival/es','Editorial / Español'),('arrival/fr','Éditorial / Français'),('arrival/it','Editoriale / Italiano'),('arrival/de','Editorial / Deutsch'),('below','Ocean habitats'),('cousteau','Cousteau / Television notebook'),('coast','Montaña Amarilla / Coastal notebook'),('horse','An Andalusian stallion'),('goodall','Goodall / Research & conservation'),('maathai','Maathai / Kenya, 1977'),('slope','Hillside settlements'),('alexander','Alexander / Bocacangrejo'),('rahman','Rahman / The public trust'),('sun','Island energy'),('air','Personal gliders & lift stations'),('atlas','Island atlas & annotations'),('credit','Cooperative finance'),('gilliam','Gilliam / Film desk'),('table','Architectural portraits'),('programme','Working programme'),('pass','Delegate credential'),('certificate','Cooperative prospectus'),('afterword','Closing editorial'),('colophon','On this edition')]
MASTER=OUT/'Horizons-77-print-letter.pdf';C=canvas.Canvas(str(MASTER),pagesize=(W,H),pageCompression=1)
C.setTitle('Horizons ’77 / Tenerife / Conference Edition');C.setAuthor('Anselm / with Codex');C.setSubject('52-page print edition / Letter / reader order / no bleed')
# Cover, intentionally clean and with white printable margins.
page('Cover',folio=False)
text('REVISTA INTERNACIONAL DE FUTUROS POSIBLES',44,750,8,'AB');text('NÚMERO 1 / 1977',453,750,7,'A')
text('horizons',40,653,90,'AB');text('’77',448,653,51,'GI',RUST);rule(633)
text('TENERIFE',44,615,10,'AB');text('ENGLISH · ESPAÑOL · FRANÇAIS · ITALIANO · DEUTSCH',168,615,7,'A')
text('The inhabited',44,544,46,'G');text('island.',44,490,55,'GI',RUST)
p=para('Architecture, ocean, energy.<br/>Notes towards life in 2027 and beyond.',15,21,'G');p.wrap(500,80);p.drawOn(C,44,421)
image(ROOT/'assets/tenerife.png',44,154,524,243)
text('TENERIFE / 2027',44,137,7,'A');text('ESTUDIO PARA UN PAISAJE HABITADO',315,137,6.5,'A')
rule(118);text('INTERNATIONAL CONFERENCE ON POSSIBLE FUTURES',44,97,8,'AB');text('Reports, drawings & conversations assembled at the close of the meeting.',44,76,10,'G');text('200 PESETAS',489,48,7,'A');finish()
page('The inhabited island / plate','TENERIFE / 2027')
text('LÁMINA 01',44,708,8,'A',RUST);p=para('A landscape to inhabit.',32,35);p.wrap(500,100);p.drawOn(C,44,648)
image(ROOT/'assets/tenerife.png',44,255,524,350)
p=para('A mountain above the clouds. A coast with work to do. Fifty years in which to reconsider the arrangements between them.',15,23,'GI');_,ph=p.wrap(440,100);p.drawOn(C,44,191-ph)
text('TENERIFE / ESTUDIO PARA UN PAISAJE HABITADO / 1977',44,100,7,'A');finish()
# Contents on two spacious fixed pages.
for ci,rows in enumerate([contents[:13],contents[13:]]):
 page('Contents / '+str(ci+1),'SUMARIO / CONTENTS');y=titleblock('Sumario.' if ci==0 else 'In this issue.',deck='Papers, drawings and conversations assembled at the close of the conference.' if ci==0 else 'The common table, the working papers, the life between sessions.',tag='NÚMERO 1 / TENERIFE / 1977')-8
 for key,label in rows:
  title=next((s['title'] for s in sheets if s['key']==key),'On this edition.')
  C.setFillColor(INK);p=para(title,13.1,16);_,ph=p.wrap(450,50);p.drawOn(C,44,y-ph);C.setFont('G',14);C.drawRightString(568,y-14,str(first[key]));text(label,44,y-ph-12,7.2,'A',GRAY);y-=ph+25
 text('ENGLISH / ESPAÑOL / FRANÇAIS / ITALIANO / DEUTSCH',44,67,6.8,'A');finish()
for s in sheets:
 k=s['kind'];page(s['title'],s.get('a',{}).get('tag',s['key'].replace('-',' / ')))
 if k in ['article','continued']:
  a=s['a'];t=s['t'];y=titleblock(t['title'],t.get('subtitle','') if k=='article' else '',a['tag']+' / '+s['lang'].upper(),a['author'] if k=='article' else '',continued=k=='continued')
  if k=='article':y=art(a['art'],y-2,150)
  note=a.get('note') if k=='continued' and s['lang']=='en' else None
  prose(s['body'],y,note,size=11.2 if k=='article' else 11.5)
 elif k=='alexander':
  a=D['alexanderEssay'];i=s['index'];sec=s['part'];y=titleblock(a['title'] if i==0 else sec['heading'],a['subtitle'] if i==0 else '', 'LIFE & FORM / CHRISTOPHER ALEXANDER',a['author'] if i==0 else '',continued=i>0)
  if i==0:image(ROOT/'assets/bocacangrejo.png',44,y-178,524,170);text('BOCACANGREJO / CUADERNO DE LA EXCURSIÓN / 1977',44,y-190,6.5,'A');y-=210
  note='The conquest of Tenerife ended in 1496. It brought enslavement and assimilation, but Indigenous people and customs persisted. The island did not begin with the conquerors’ maps.' if i==2 else None
  prose(sec['body'],y,note,size=11.1)
 elif k=='horse':
  a=s['a'];y=titleblock(a['title'],a['subtitle'],'VIDA COMPARTIDA / WORKING TOGETHER','From an island notebook');image(ROOT/'assets/andalusian-stallion.jpg',44,y-205,524,195);y-=225;prose(a['body'],y,size=11)
 elif k=='rahman':
  a=s['a'];y=titleblock(a['title'],a['subtitle'],'DELHI / THE PUBLIC TRUST','From the public works desk');prose(a['body'],y,note='Who may object? Who must listen? Who can refuse?',size=11.8)
 elif k=='atlas':
  y=titleblock(s['title'],'The space between places is a place too.','TRANSPORT WORKSHOP / ROUTE STUDY 03');image(TMP/'map.png',44,y-300,524,280);text('ISLAS CANARIAS / SCHEMATIC GEOGRAPHY / PROPOSED LINKS',44,y-316,7,'A');p=para('La Palma, La Gomera, Tenerife, Gran Canaria. Every line is a question. Notes from each island follow on page '+str(first['atlas-notes'])+'.',14,21,'GI');_,ph=p.wrap(480,150);p.drawOn(C,44,y-350-ph)
 elif k=='atlas-notes':
  y=titleblock(s['title'],tag='ATLAS DEL PORVENIR / ANOTACIONES');prose(['<b>'+i['name']+'</b><br/>'+i['note'] for i in D['islands']],y,size=12)
 elif k=='programme':
  a=s['a'];y=titleblock(a['title'],tag=a['sub']);root=LH.fromstring('<div>'+a['body']+'</div>');ps=[]
  for dt in root.findall('.//dt'):
   dd=dt.getnext();ps.append('<b>'+plain(LH.tostring(dt,encoding='unicode'))+'</b><br/>'+plain(LH.tostring(dd,encoding='unicode')))
  prose(ps,y,note='Working languages: EN / ES / FR / IT / DE. Please return interpretation equipment at the end of the day.',size=12)
 elif k=='pass':
  a=s['a'];y=titleblock(a['title'],tag=a['sub']);C.setStrokeColor(TEAL);C.setLineWidth(1);C.rect(95,215,422,365,fill=0,stroke=1)
  text('HORIZONS ’77 / TENERIFE',120,549,9,'AB',TEAL);text('DELEGADO',120,489,39,'AB',TEAL)
  for yy,label in [(440,'NOMBRE / NAME'),(362,'IDIOMAS / LANGUAGES'),(290,'ÁREA DE INTERÉS')]:text(label,120,yy,8,'A');rule(yy-25,120,370)
  text('EN     ES     FR     IT     DE',120,321,11,'G');text('EL FUTURO SE DISCUTE EN COMÚN.',120,242,8,'A',TEAL)
  prose(['A name, five languages and a field of interest. Between them, enough information to begin a conversation. Please keep the pass visible in the working rooms; at the common table, introductions are preferred.'],165,size=11)
 elif k=='certificate':
  a=s['a'];y=titleblock(a['title'],tag=a['sub']);C.setStrokeColor(TEAL);C.setLineWidth(1);C.rect(60,285,492,290,fill=0,stroke=1);C.rect(65,290,482,280,fill=0,stroke=1)
  text('COOPERATIVA DEL PORVENIR',88,539,10,'AB',TEAL)
  pp=para('Certificado de<br/>participación',32,38,'GI',TEAL);_,ph=pp.wrap(440,100);pp.drawOn(C,88,500-ph)
  for yy,line in [(386,'Propuesta para deliberación / Tenerife, 1977'),(357,'Una participación en el cuidado de lo común.'),(321,'Construcción / Conservación / Acceso')]:text(line,88,yy,11,'G',TEAL)
  prose(['Draft circulated for discussion by the finance workshop. Terms of membership, maintenance and withdrawal are to be agreed before any subscriptions are accepted. The certificate is printed here with the working paper on patient capital and collective ownership.','See page '+str(first['credit'])+'.'],240,size=12)
 finish()
assert N==49,N
# Colophon and source notes: fixed two-page flowing backmatter, kept at the end.
root=LH.fromstring(D['notes']);ps=root.find_class('colophon-text')[0].findall('p');back=[]
for p in ps:
 for a in p.findall('.//a'):
  href=a.get('href','');a.text=(a.text or '')+' ('+urlparse(href).netloc.removeprefix('www.')+')'
 t=plain(LH.tostring(p,encoding='unicode'))
 # Long URLs typeset with discretionary spaces after path separators.
 # Printed sources use readable titles and domains; full links remain in the web edition.
 back.append(t)
# Separate bibliographical links into modest type; prose remains readable.
# Page 50 holds the fiction and feature provenance; page 51 starts with plate provenance.
cut=next(i for i,t in enumerate(back) if 'cover landscape' in t)
note_groups=[back[:cut],back[cut:]]
parts=[]
for pi in range(2):
 parts=[para(t,9.4,13.1,space=10) for t in note_groups[pi]]
 page('On this edition / '+str(pi+1),'COLOPHON / EDITION NOTES')
 top=titleblock('On this edition.' if pi==0 else 'Sources & contributors.',tag='EDITION NOTES / '+str(pi+1))
 prose(note_groups[pi],top,size=9.4)
 finish()
page('Back cover',folio=False)
text('horizons ’77',44,702,38,'G',TEAL);rule(681)
pp=para('There is still<br/>room at the table.',43,49,'GI',TEAL);_,ph=pp.wrap(500,160);pp.drawOn(C,44,557-ph)
image(ROOT/'assets/tenerife.png',44,178,524,220)
text('EL FUTURO ES UNA ISLA',44,135,10,'AB',TEAL);text('LE FUTUR EST UNE ÎLE',44,113,10,'A');text('IL FUTURO È UN’ISOLA / DIE ZUKUNFT IST EINE INSEL',44,91,8,'A');text('TENERIFE / EDICIÓN DEL CONGRESO / 1977',44,50,7,'A');finish();C.save()
assert N==52,N
# Tabloid imposition: each adjacent PDF pair is one duplex physical sheet.
r=PdfReader(MASTER);writer=PdfWriter();order=[]
for i in range(13):
 for pair in [(52-2*i,1+2*i),(2+2*i,51-2*i)]:
  sheet=writer.add_blank_page(width=1224,height=792)
  for x,pn in zip([0,612],pair):sheet.merge_transformed_page(r.pages[pn-1],Transformation().translate(tx=x,ty=0))
  order.append(pair)
writer.add_metadata({'/Title':'Horizons 77 / 11 x 17 booklet imposition','/Author':'Anselm / with Codex','/Subject':'Print actual size, duplex short-edge, no additional booklet mode. 13 sheets.'})
with open(OUT/'Horizons-77-booklet-tabloid.pdf','wb') as f:writer.write(f)
(OUT/'pagination.json').write_text(json.dumps({'pages':N,'firstPages':first,'imposition':order,'bodyFontSizes':fitlog},indent=2))
print('Created',N,'reader pages;',len(order),'tabloid sides; body type minimum',min(v for n,v in fitlog if n<50))
