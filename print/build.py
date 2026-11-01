import json,re,html,math,os,tempfile
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
ROOT=Path(os.environ.get('HORIZONS_ROOT',Path(__file__).resolve().parents[1])); TMP=Path(os.environ.get('HORIZONS_PRINT_TMP',str(Path(tempfile.gettempdir())/'horizons-print')));OUT=ROOT/'output'/'pdf';OUT.mkdir(exist_ok=True,parents=True)
D=json.loads((TMP/'content.json').read_text())
F=str(ROOT/'assets'/'fonts')+'/'
for name,file in [('G','NimbusRoman-Regular.ttf'),('GI','NimbusRoman-Italic.ttf'),('GB','NimbusRoman-Bold.ttf'),('A','NimbusSans-Regular.ttf'),('AB','NimbusSans-Bold.ttf'),('BD','URWGothic-Demi.ttf'),('BL','URWBookman-Light.ttf'),('BI','URWGothic-Demi.ttf')]:pdfmetrics.registerFont(TTFont(name,F+file))
pdfmetrics.registerFont(TTFont('AR',F+'Amiri-Regular.ttf'))
pdfmetrics.registerFontFamily('G',normal='G',bold='GB',italic='GI',boldItalic='GI')
pdfmetrics.registerFontFamily('A',normal='A',bold='AB',italic='A',boldItalic='AB')
W,H=612,792;INK=CMYKColor(0,.25,.42,.78);RUST=CMYKColor(0,.66,.86,.27);TEAL=CMYKColor(.18,.06,.43,.58);GRAY=CMYKColor(0,.13,.25,.42)
C=None;N=0;fitlog=[]
def clean(t):
 t=html.unescape(t).replace('\u00a0',' ').replace('↔',' / ').replace('→',' / ').replace('↗',' / ').replace('↘',' / ').replace('☼','*').replace('□','[ ]')
 return t

def plain(t):return clean(LH.fromstring('<div>'+t+'</div>').text_content())
def para(t,size=11,leading=None,font='G',color=INK,space=10):
 # Edition notes need compact, readable leading as the acknowledgements grow.
 if N>=46 and font=='G':leading=leading or size*1.3;space=min(space,7)
 # This one Arabic word uses joined visual-order glyphs; keep the source in logical order.
 # Shaped with arabic-reshaper (harakat retained and shifted) and python-bidi.
 t=t.replace('<span lang="ar" dir="rtl">أُنس</span>','<font name="AR">ﺲﻧﺃُ</font>')
 t=clean(t);t=re.sub(r'<a\b[^>]*>(.*?)</a>',r'\1',t,flags=re.S);t=re.sub(r'<span[^>]*>|</span>','',t);t=t.replace('<br>','<br/>')
 # prevent short paragraph-final single words while preserving markup
 if '<' not in t:
  m=re.search(r'(\S+)\s+(\S+)$',t)
  if m and len(m.group())<23:t=t[:m.start()]+m.group(1)+'\u00a0'+m.group(2)
 return Paragraph(t,ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.42,textColor=color,spaceAfter=space,alignment=0,allowWidows=0,allowOrphans=0,splitLongWords=1,uriWasteReduce=0.15))
def text(t,x,y,size=10,font='A',color=INK):
 C.setFillColor(color);C.setFont(font,size);C.drawString(x,y,clean(t))
def rule(y,x=44,width=524):C.setStrokeColor(GRAY);C.setLineWidth(.7);C.line(x,y,x+width,y)
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
 size=31 if not continued else 24
 while True:
  p=para(title if continued else title.upper(),size,size*1.06,'BD',space=0);w,h=p.wrap(524,180)
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
 im=ImageReader(str(cached));iw,ih=im.getSize();s=max(w/iw,h/ih) if crop else min(w/iw,h/ih);dw,dh=iw*s,ih*s
 if crop:
  C.saveState();clip=C.beginPath();clip.rect(x,y,w,h);C.clipPath(clip,stroke=0,fill=0)
 C.drawImage(im,x+(w-dw)/2,y+(h-dh)/2,dw,dh,mask='auto')
 if crop:C.restoreState()
 return (x+(w-dw)/2 if not crop else x,y+(h-dh)/2 if not crop else y,dw if not crop else w,dh if not crop else h)
def caption(label,rect):
 x,y,w,h=rect
 p=para(label,6.8,9,'A',GRAY);_,hh=p.wrap(w,35);p.drawOn(C,x,y-7-hh)
 return y-7-hh

def art(kind,top,h=165):
 y=top-h;bounds=None
 if kind=='storyboard':
  bounds=image(TMP/'study-rooms.png',44,y,524,h)
 elif kind.startswith('study-'):
  bounds=image(TMP/(kind+'.png'),44,y,524,h)
 elif kind=='terrace':bounds=image(ROOT/'assets/terrace-workshop.png',44,y,524,h,crop=True)
 elif kind in ['landscape','coast','observatory']:
  name={'landscape':'terrace-workshop.png','coast':'montana-amarilla-v2.png','observatory':'ocean-observatory.png'}[kind];bounds=image(ROOT/'assets'/name,44,y,524,h,crop=True)
 elif kind in ['habitat','airlift']:bounds=image(TMP/(kind+'.png'),44,y,524,h)
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
 caption(D['plateCaptions'].get(kind,'HORIZONS ’77 / CUADERNO DE TRABAJO'),bounds or (44,y,524,h))
 return y-28

def layout(paras,top,bottom=67,size=11,note=None,cols=2,width=524,x=44,draw=True,leading=None):
 gap=24;cw=(width-gap*(cols-1))/cols;flow=[para(t,size,leading=leading,space=9 if leading else 11) for t in paras]
 if cols==3:
  for p in flow:p.style.alignment=0
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
   layout(paras,top,bottom=top-high-1,size=sz,note=note);fitlog.append((N,sz));return top-high-1
 raise Exception('Text overflow on page '+str(N))


sheets=[];first={}
def add(key,title,kind,**kw):
 if key not in first:first[key]=len(sheets)+3
 sheets.append(dict(key=key,title=title,kind=kind,**kw))
def addarticle(a,lang='en'):
 t=D['openingFeatures'][lang] if a['id']=='arrival' and lang!='en' else a;key='arrival/'+lang if a['id']=='arrival' else a['id']
 if a['id']=='arrival':add(key,t['title'],'editorial',a=a,t=t,body=t['body'],lang=lang);return
 half=math.ceil(len(t['body'])/2)
 add(key,t['title'],'article',a=a,t=t,body=t['body'][:half],lang=lang)
 add(key+'-continued',t['title'],'continued',a=a,t=t,body=t['body'][half:],lang=lang)
A={a['id']:a for a in D['articles']}
addarticle(A['arrival'])
for lang in ['es','fr','it','de']:
 addarticle(A['arrival'],lang)
 if lang=='es':
  a=next(a for a in D['assemblyPages'] if a['id']=='kitchen-desk');add(a['id'],a['title'],'assembly',a=a)
for a in [A['below'],D['cousteauArticle'],D['coastArticle']]:
 addarticle(a)
 if a['id']=='below':
  desk=next(x for x in D['assemblyPages'] if x['id']=='letters-desk');add(desk['id'],desk['title'],'assembly',a=desk)
add('horse',D['horseArticle']['title'],'horse',a=D['horseArticle'])
for a in [D['goodallArticle'],D['maathaiArticle'],A['slope']]:addarticle(a)
for i,sec in enumerate(D['alexanderEssay']['sections']):add('alexander' if i==0 else 'alexander-'+str(i+1),D['alexanderEssay']['title'],'alexander',part=sec,index=i)
add('rahman',D['rahmanArticle']['title'],'rahman',a=D['rahmanArticle'])
for a in [A['sun'],A['air']]:
 addarticle(a)
 if a['id']=='sun':
  desk=next(x for x in D['assemblyPages'] if x['id']=='accounts-desk');add(desk['id'],desk['title'],'assembly',a=desk)
add('atlas','Seven islands. Many futures.','atlas');add('atlas-notes','Each island has a name.','atlas-notes')
for a in [A['credit'],D['gilliamArticle'],A['table']]:addarticle(a)
a=next(a for a in D['assemblyPages'] if a['id']=='closing-desk');add(a['id'],a['title'],'assembly',a=a)
add('programme',D['docs']['programme']['title'],'programme',a=D['docs']['programme'])
add('pass','The life between sessions','documents');first['certificate']=first['pass']
addarticle(A['afterword'])
assert len(sheets)==43,len(sheets)
first['colophon']=46
contents=[('arrival/en','Editorial / English'),('arrival/es','Territorio / Español'),('arrival/fr','Formes vivantes / Français'),('arrival/it','Abitare / Italiano'),('arrival/de','Natur & Freundschaft / Deutsch'),('below','Ocean habitats'),('cousteau','Cousteau / Television notebook'),('coast','Montaña Amarilla / Coastal notebook'),('horse','An Andalusian stallion'),('goodall','Goodall / Research & conservation'),('maathai','Maathai / Kenya, 1977'),('slope','Hillside settlements'),('alexander','Alexander / Bocacangrejo'),('rahman','Rahman / The public trust'),('sun','Island energy'),('air','Personal gliders & lift stations'),('atlas','Island atlas & annotations'),('credit','Cooperative finance'),('gilliam','Gilliam / Film desk'),('table','Architectural portraits'),*[(a['id'],'Conference desk / '+a['title']) for a in D['assemblyPages']],('programme','Working programme'),('pass','Delegate pass & cooperative certificate'),('afterword','Closing editorial'),('colophon','On this edition')]

def supporting_leaf(key,bottom):
 leaf=D['workshopLeaves'].get(key)
 if not leaf or bottom-70<50:return
 available=bottom-70;top=bottom-10
 if not leaf.get('art') or available<145:
  rule(top);text(leaf['label'],44,top-14,6.5,'AB',RUST)
  heading=para(leaf['title'],12,14,'BD');_,hh=heading.wrap(155,50)
  note=para(leaf['text'],9.3,12,'G');_,nh=note.wrap(350,100)
  if max(hh,nh)>available-25:return
  C.setStrokeColor(GRAY);C.setLineWidth(.7);C.rect(40,top-34-max(hh,nh),532,max(hh,nh)+38,fill=0,stroke=1)
  heading.drawOn(C,44,top-28-hh);note.drawOn(C,218,top-28-nh);return
 height=min(available,230)
 if leaf['art']=='screening':height=min(available,265)
 if available>300 and leaf['art']!='screening':
  rule(top,44,524);text(leaf['label'],44,top-16,7,'AB',RUST)
  pp=para(leaf['title'],20,23,'BD');_,hh=pp.wrap(524,65);pp.drawOn(C,44,top-32-hh)
  bounds=image(TMP/('study-'+leaf['art']+'.png'),44,top-205,524,140);caption(leaf.get('caption',leaf['title'].upper()),bounds)
  pp=para(leaf['text'],11.5,15);_,hh=pp.wrap(524,100);pp.drawOn(C,44,top-223-hh)
  return
 if height<145:return
 rule(top,44,524);text(leaf['label'],44,top-15,7,'AB',RUST)
 path=ROOT/'assets/evening-screening.png' if leaf['art']=='screening' else TMP/('study-'+leaf['art']+'.png')
 bounds=image(path,44,top-height+23,250,height-48)
 caption(leaf.get('caption',leaf['title'].upper()),bounds)
 pp=para(leaf['title'],18,19,'BD');_,hh=pp.wrap(250,70);pp.drawOn(C,318,top-34-hh);yy=top-44-hh
 for size in [10.5,10,9.5]:
  pp=para(leaf['text'],size,size*1.3);_,hh=pp.wrap(250,height-55)
  if yy-hh>top-height:pp.drawOn(C,318,yy-hh);return
 raise Exception('Supplement overflow on '+str(N))

def pattern_leaf(bottom,index):
 if bottom<205:return
 kind='threshold-plan' if index==1 else 'shared-path'
 cap='UMBRAL, ASIENTO Y PASO / ESQUEMA DE RELACIONES' if index==1 else 'EL CAMINO / DESCANSO Y RECORRIDO ALTERNATIVO'
 top=bottom-20;rule(top);text('DEL CUADERNO / '+str(index+1),44,top-15,7,'AB',RUST)
 h=min(150,top-115);bounds=image(TMP/('study-'+kind+'.png'),44,top-35-h,524,h);caption(cap,bounds)

MASTER=OUT/'Horizons-77-print-letter.pdf';C=canvas.Canvas(str(MASTER),pagesize=(W,H),pageCompression=1)
C.setTitle('Horizons ’77 / the 1977 design edition');C.setAuthor('Anselm / with Codex');C.setSubject('48-page print edition / Letter / reader order / no bleed')
page('Cover',folio=False)
text('REVISTA INTERNACIONAL DE FUTUROS POSIBLES',44,750,8,'AB');text('NÚMERO 1 / 1977',453,750,7,'A')
# Geometric display capitals; fit the wordmark to the printed measure.
mark='HORIZONS ’77';fs=72
while pdfmetrics.stringWidth(mark,'BD',fs)>524:fs-=.5
text(mark,40,660,fs,'BD');rule(638)
text('TENERIFE',44,618,10,'AB');text('ENGLISH · ESPAÑOL · FRANÇAIS · ITALIANO · DEUTSCH',168,618,7,'A')
text('THE INHABITED',44,550,39,'BD');text('ISLAND.',44,493,55,'BD',RUST)
p=para('Architecture, ocean, energy.<br/>Notes towards life in 2027 and beyond.',16,21,'G');p.wrap(500,80);p.drawOn(C,44,427)
image(ROOT/'assets/tenerife.png',44,154,524,250)
text('TENERIFE / 2027',44,137,7,'A');text('ESTUDIO PARA UN PAISAJE HABITADO',315,137,6.5,'A')
rule(118);text('INTERNATIONAL CONFERENCE ON POSSIBLE FUTURES',44,97,8,'AB');text('Reports, drawings & conversations assembled at the close of the meeting.',44,76,11,'G');text('200 PESETAS',489,48,7,'A');finish()
page('Contents','SUMARIO / CONTENTS');y=titleblock('Sumario.',deck='Friendship and the art of seeing together.<br/>Papers, drawings, walks and conversations among friends new and old.',tag='NÚMERO 1 / TENERIFE / 1977')-7
contents.sort(key=lambda row:first[row[0]])
for col,rows in enumerate([contents[:14],contents[14:]]):
 yy=y;x=44+col*274
 for key,label in rows:
  title=next((s['title'] for s in sheets if s['key']==key),'On this edition.')
  p=para(title,11.3,13,'BL');_,hh=p.wrap(219,60);p.drawOn(C,x,yy-hh);C.setFillColor(RUST);C.setFont('BD',12);C.drawRightString(x+250,yy-12,str(first[key]));text(label,x,yy-hh-10,6.7,'A',GRAY);yy-=hh+20
 if yy<65:raise Exception('Contents overflow')
text('ENGLISH / ESPAÑOL / FRANÇAIS / ITALIANO / DEUTSCH',44,67,6.8,'A');finish()
for s in sheets:
 k=s['kind'];page(s['title'],s.get('a',{}).get('tag',s['key'].replace('-',' / ')));bottom=None
 if k in ['article','continued','editorial']:
  a=s['a'];t=s['t'];opening=k!='continued';y=titleblock(t['title'],t.get('subtitle','') if opening else '',t.get('tag',a['tag'])+' / '+s['lang'].upper(),t.get('author',a['author']) if opening else '',continued=not opening)
  if opening:
   kind='study-'+dict(en='section',es='territory',fr='reef-village',it='privacy',de='drago')[s['lang']] if k=='editorial' else 'terrace' if a['id']=='slope' else 'study-scales' if a['id']=='table' else 'study-calendar' if a['id']=='afterword' else a['art']
   if a['id']!='afterword':y=art(kind,y-2,105 if k=='editorial' else 185 if a['id']=='slope' else 165 if a['art'] in ['coast','observatory'] else 150)
  note=a.get('note') if not opening and s['lang']=='en' else None
  bottom=prose(s['body'],y,note,size=11.3 if opening else 11.7)
 elif k=='alexander':
  a=D['alexanderEssay'];i=s['index'];sec=s['part'];y=titleblock(a['title'] if i==0 else sec['heading'],a['subtitle'] if i==0 else '', 'LIFE & FORM / CHRISTOPHER ALEXANDER',a['author'] if i==0 else '',continued=i>0)
  if i==0:
   bounds=image(ROOT/'assets/bocacangrejo.png',44,y-178,524,170);caption('BOCACANGREJO / CUADERNO DE LA EXCURSIÓN / 1977',bounds);y-=210
  note='The conquest of Tenerife ended in 1496. It brought enslavement and assimilation, but Indigenous people and customs persisted. The island did not begin with the conquerors’ maps.' if i==2 else None
  bottom=prose(sec['body'],y,note,size=11.3)
  if i in [1,2]:pattern_leaf(bottom,i)
 elif k=='horse':
  a=s['a'];y=titleblock(a['title'],a['subtitle'],'VIDA COMPARTIDA / WORKING TOGETHER','From an island notebook');bounds=image(ROOT/'assets/andalusian-stallion.jpg',44,y-205,524,195);caption('EL CABALLO / TENERIFE',bounds);y-=230;bottom=prose(a['body'],y,size=11.5)
 elif k=='rahman':
  a=s['a'];y=titleblock(a['title'],a['subtitle'],'DELHI / THE PUBLIC TRUST','From the public works desk');bottom=prose(a['body'],y,note='Who may object? Who must listen? Who can refuse?',size=12)
 elif k=='atlas':
  y=titleblock(s['title'],'The space between places is a place too.','TRANSPORT WORKSHOP / ROUTE STUDY 03');image(TMP/'map.png',44,y-310,524,300);text('ISLAS CANARIAS / SCHEMATIC GEOGRAPHY / PROPOSED LINKS',44,y-326,7,'A');bottom=prose(['La Palma, La Gomera, Tenerife, Gran Canaria. Every line is a question. Notes from each island follow on page '+str(first['atlas-notes'])+'.'],y-350,size=14)

 elif k=='atlas-notes':
  y=titleblock(s['title'],tag='ATLAS DEL PORVENIR / ANOTACIONES');bottom=prose(['<b>'+i['name']+'</b><br/>'+i['note'] for i in D['islands']],y,size=12.5)

 elif k=='assembly':
  a=s['a'];y=titleblock(a['title'],a['deck'],a['tag'])
  # A three-column newspaper measure, with a dedicated plate and boxed notice.
  bounds=image(TMP/('study-'+a['art']+'.png'),44,y-95,524,85);caption(a['caption'],bounds);y-=125
  note=para(a['notice'],9.3,12,'A');_,nh=note.wrap(500,80)
  C.setStrokeColor(INK);C.setLineWidth(1.3);C.rect(44,62,524,nh+20,fill=0,stroke=1);note.drawOn(C,56,72)
  floor=nh+99
  for sz in [11,10.75,10.5,10.25]:
   if layout(a['body'],y,bottom=floor,size=sz,cols=3,draw=False,leading=sz*1.28):
    layout(a['body'],y,bottom=floor,size=sz,cols=3,leading=sz*1.28);fitlog.append((N,sz));break
  else:raise Exception('Assembly overflow on '+str(N))
 elif k=='programme':
  a=s['a'];y=titleblock(a['title'],tag=a['sub']);root=LH.fromstring('<div>'+a['body']+'</div>');ps=[]
  for dt in root.findall('.//dt'):
   dd=dt.getnext();ps.append('<b>'+plain(LH.tostring(dt,encoding='unicode'))+'</b><br/>'+plain(LH.tostring(dd,encoding='unicode')))
  bottom=prose(ps,y,note='Working languages: EN / ES / FR / IT / DE. Please return interpretation equipment at the end of the day.',size=12)

 elif k=='documents':
  y=titleblock('The life between sessions',tag='DOCUMENTOS / CREDENCIAL / COOPERATIVA')
  C.setStrokeColor(TEAL);C.rect(44,y-280,250,260,fill=0,stroke=1);C.rect(318,y-280,250,260,fill=0,stroke=1)
  text('HORIZONS ’77 / TENERIFE',60,y-45,8,'AB',TEAL);text('DELEGADO',60,y-82,24,'AB',TEAL)
  for yy,label in [(y-120,'NOMBRE / NAME'),(y-175,'IDIOMAS / LANGUAGES'),(y-230,'ÁREA DE INTERÉS')]:text(label,60,yy,7,'A');rule(yy-20,60,216)
  text('EN    ES    FR    IT    DE',60,y-210,9,'G')
  text('COOPERATIVA DEL PORVENIR',334,y-45,8,'AB',TEAL);pp=para('Certificado de<br/>participación',22,27,'BI',TEAL);_,hh=pp.wrap(210,90);pp.drawOn(C,334,y-78-hh)
  ps=['Propuesta para deliberación / Tenerife, 1977','Una participación en el cuidado de lo común.','Construcción / Conservación / Acceso']
  yy=y-175
  for txt in ps:
   pp=para(txt,10.5,14,'G',TEAL);_,hh=pp.wrap(216,60);pp.drawOn(C,334,yy-hh);yy-=hh+12
  bottom=prose(['A name, five languages and a field of interest. Between them, enough information to begin a conversation. At the common table, introductions are preferred.','Draft circulated for discussion. Terms of membership, maintenance and withdrawal are to be agreed before any subscriptions are accepted. See page '+str(first['credit'])+'.','Los derechos de uso, las obligaciones de mantenimiento y las condiciones de salida deberán acordarse antes de emitir cualquier participación.'],y-315,size=12)

 if bottom is not None:supporting_leaf(s['key'],bottom)
 finish()
assert N==45,N
root=LH.fromstring(D['notes']);ps=root.find_class('colophon-text')[0].findall('p');back=[]
for p in ps:
 for a in p.findall('.//a'):
  href=a.get('href','');a.text=(a.text or '')+' ('+urlparse(href).netloc.removeprefix('www.')+')'
 back.append(plain(LH.tostring(p,encoding='unicode')))
# Keep the provenance whole, with a clean chapter break between pages.
cut=min(range(1,len(back)),key=lambda i:abs(sum(map(len,back[:i]))-sum(map(len,back[i:]))))
for pi,group in enumerate([back[:cut],back[cut:]]):
 page('On this edition / '+str(pi+1),'COLOPHON / EDITION NOTES');top=titleblock('On this edition.' if pi==0 else 'Sources & contributors.',tag='EDITION NOTES / '+str(pi+1));prose(group,top,size=9.8);finish()
page('Back cover',folio=False)
text('HORIZONS ’77',44,710,42,'BD');rule(684)
pp=para('There is still<br/>room at the table.',42,47,'BI',RUST);_,hh=pp.wrap(520,180);pp.drawOn(C,44,575-hh)
text('LAS PREGUNTAS VIAJAN / THE QUESTIONS TRAVEL',44,340,11,'AB',TEAL)
pp=para('Correspondence, drawings and corrections for the next issue are welcome. Please include the name of the place, the scale of the drawing and the address to which a reply may be sent.',17,23,'G');_,hh=pp.wrap(420,130);pp.drawOn(C,44,300-hh)
text('EL FUTURO ES UNA ISLA',44,124,10,'AB');text('LE FUTUR EST UNE ÎLE',44,103,10,'A');text('IL FUTURO È UN’ISOLA / DIE ZUKUNFT IST EINE INSEL',44,82,8,'A');text('TENERIFE / EDICIÓN DEL CONGRESO / 1977',44,49,7,'A');finish();C.save()
assert N==48,N
r=PdfReader(MASTER);writer=PdfWriter();order=[]
for i in range(N//4):
 for pair in [(N-2*i,1+2*i),(2+2*i,N-1-2*i)]:
  sheet=writer.add_blank_page(width=1224,height=792)
  for x,pn in zip([0,612],pair):sheet.merge_transformed_page(r.pages[pn-1],Transformation().translate(tx=x,ty=0))
  order.append(pair)
writer.add_metadata({'/Title':'Horizons 77 / 11 x 17 booklet imposition','/Author':'Anselm / with Codex','/Subject':'48 pages / 12 sheets / actual size / short-edge duplex / no additional booklet mode'})
with open(OUT/'Horizons-77-booklet-tabloid.pdf','wb') as f:writer.write(f)
# Reader spreads: screen reading, not the printer's imposition.
reader=PdfWriter()
pairs=[(None,1)]+[(i,i+1) for i in range(2,N,2)]+[(N,None)]
for pair in pairs:
 sheet=reader.add_blank_page(width=1224,height=792)
 for x,pn in zip([0,612],pair):
  if pn:sheet.merge_transformed_page(r.pages[pn-1],Transformation().translate(tx=x,ty=0))
reader.add_metadata({'/Title':'Horizons 77 / facing reader spreads','/Subject':'Screen reading only; use reader-order PDF for printing'})
with open(OUT/'Horizons-77-reader-spreads.pdf','wb') as f:reader.write(f)
(OUT/'pagination.json').write_text(json.dumps({'pages':N,'firstPages':first,'imposition':order,'readerSpreads':pairs,'bodyFontSizes':fitlog},indent=2))
print('Created',N,'reader pages;',len(order),'tabloid sides;',len(pairs),'reader spreads. Minimum article type:',min(v for n,v in fitlog if n<46))
