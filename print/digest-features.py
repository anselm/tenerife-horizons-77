"""Individually art-directed digest pages, composed in physical points.

The surrounding legacy compositor remains intact for the rest of the issue.
These pages use actual 9.4/12.2 body type, never an automatic copy-fit reduction.
"""
pdfmetrics.registerFont(TTFont('COND',F+'NimbusSansNarrow-Bold.ttf'))
pdfmetrics.registerFont(TTFont('MONO',F+'NimbusMonoPS-Regular.ttf'))
FEATURE_BLUE=CMYKColor(.91,.58,.33,.25)
FEATURE_RED=CMYKColor(.02,.88,.89,.10)
FEATURE_BLACK=CMYKColor(0,0,0,.94)
feature_checks=[]
def feature_clean(t):
 t=clean(t).replace('<span lang="ar" dir="rtl">أُنس</span>','<font name="AR">ﺲﻧﺃُ</font>')
 return re.sub(r'<span[^>]*>|</span>','',t)

def fp(t,x,top,w,size=9.4,leading=None,font='G',color=FEATURE_BLACK,gap=8):
 # Display lettering is upright; reading emphasis and book titles remain semantic.
 if size>=16:
  t=re.sub(r'</?(?:i|em)>','',t)
  if font=='GI':font='GB'
 p=Paragraph(feature_clean(t).replace('<br>','<br/>'),ParagraphStyle('feature',fontName=font,fontSize=size,leading=leading or size*1.30,textColor=color,alignment=0,allowWidows=0,allowOrphans=0,splitLongWords=1))
 _,h=p.wrap(w,2000)
 if top-h<0 or top>535:raise Exception(f'Feature text outside page {N}: {t[:60]} / {top-h}')
 p.drawOn(C,x,top-h);feature_checks.append({'page':N,'type':'text','x':x,'top':top,'bottom':top-h,'width':w,'size':size})
 return top-h-gap

def fcols(ps,top,size=9.4,leading=12.2,paragraph_gap=9,paper=None):
 # Let a paragraph cross columns; balance measured lines at a fixed readable size.
 style=ParagraphStyle('feature-column',fontName='G',fontSize=size,leading=leading,textColor=FEATURE_BLACK,alignment=0,allowWidows=0,allowOrphans=0,splitLongWords=1,spaceAfter=paragraph_gap)
 def compose(height):
  queue=[Paragraph(feature_clean(t),style) for t in ps];positions=[]
  for x in [0,171.75]:
   yy=top;floor=top-height
   while queue:
    p=queue[0];_,h=p.wrap(155.75,max(0,yy-floor))
    if h<=yy-floor:
     positions.append((p,x,yy-h));yy-=h+paragraph_gap;queue.pop(0)
    else:
     parts=p.split(155.75,max(0,yy-floor))
     if len(parts)>1:
      part=parts[0];_,h=part.wrap(155.75,yy-floor);positions.append((part,x,yy-h));queue=parts[1:]+queue[1:]
     break
  return None if queue else positions
 lo,hi=leading,top-3
 if compose(hi) is None:raise Exception(f'Feature columns overflow on {N}; top {top}; total heights {[Paragraph(feature_clean(t),style).wrap(155.75,2000)[1] for t in ps]}')
 for _ in range(20):
  mid=(lo+hi)/2
  if compose(mid) is None:lo=mid
  else:hi=mid
 positions=compose(hi+.05)
 if paper:
  if paper=='letters':
   for j,(p,x,y) in enumerate(positions):
    C.setFillColor(CMYKColor(0,.02,.07,0) if j%2 else CMYKColor(0,0,0,.04));C.rect(x-4,y-3,163.75,p.height+6,fill=1,stroke=0)
    C.setStrokeColor(CMYKColor(0,0,0,.4));C.setLineWidth(.35);C.line(x-4,y-3,x+159.75,y-3)
  else:
   for j,x in enumerate([0,171.75]):
    bottom=min(y for p,xx,y in positions if xx==x)
    C.setFillColor(CMYKColor(0,.025,.07,0) if j==0 else CMYKColor(0,0,0,.025));C.rect(x-5,bottom-6,165.75,top-bottom+11,fill=1,stroke=0)
    C.setStrokeColor(CMYKColor(0,0,0,.38));C.setLineWidth(.4);C.line(x-5,bottom-6,x+160.75,bottom-6)
    C.line(x+160.75,bottom-6,x+160.75,top+5)
 for p,x,y in positions:
  p.drawOn(C,x,y);feature_checks.append({'page':N,'type':'text','x':x,'top':y+p.height,'bottom':y,'width':155.75,'size':size})
 return min(y for p,x,y in positions)-9

def frule(y,color=FEATURE_BLACK,width=327.5,weight=.65):
 C.setStrokeColor(color);C.setLineWidth(weight);C.line(0,y,width,y)

def fimage(path,top,h,caption_text='',crop=False):
 rect=image(path,0,top-h,327.5,h,crop=crop)
 feature_checks.append({'page':N,'type':'image','x':rect[0],'top':rect[1]+rect[3],'bottom':rect[1],'width':rect[2]})
 return fp(caption_text,0,top-h-7,327.5,6.4,8.1,'A',gap=12) if caption_text else top-h

def fnotice(leaf,top):
 frule(top)
 y=fp(leaf['label'],0,top-10,327.5,6.6,8.5,'AB',RUST)
 y=fp(leaf['title'],0,y,327.5,19,20,'GB',gap=9)
 return fp(leaf['text'],0,y,327.5,9.4,12.2)

def fslips(key,top,rows=None):
 y=top
 for h,p in (D['featureMarginalia'][key] if rows is None else rows):
  frule(y,GRAY)
  yy=fp(h,0,y-8,94,7.1,9,'AB',RUST)
  yy=fp(p,107,y-8,220.5,9.1,11.7)
  y=min(y-34,yy-8)
 return y

def fhead(a,d,font,size):
 y=fp(d['label'],0,530,327.5,7.1,9,'AB',gap=15)
 y=fp('<br/>'.join(d['lines']),0,y,327.5,size,size*.91,font,FEATURE_BLUE if a['id']=='below' else FEATURE_BLACK,gap=18)
 y=fp(a['subtitle'],0,y,310,12.3,15.2,'GI',gap=12)
 return fp(a['author'],0,y,327.5,6.8,9,'A',gap=17)

def draw_feature(s):
 a=s['a'];key=a['id'];i=s['part'];d=D['featureDesigns'][key]
 if key=='below' and i<2:
  draw_ocean_world(i);return
 C.saveState();C.translate(44,76);C.scale(1.6,1.6)
 if key=='below':
  if i==0:
   y=fhead(a,d,'GB',43);y=fcols(a['body'][:3],y)
   frule(y-8,FEATURE_BLUE,weight=2)
   fp('UNA STANZA, NON UN IMPERO.',0,y-20,327.5,10.5,13,'AB',FEATURE_BLUE)
  elif i==1:
   fimage(ROOT/'assets'/d['image'],530,491,d['caption'])
  elif i==2:
   y=fp('The coast<br/>continues.',0,530,327.5,34,32,'GB',FEATURE_BLUE,gap=18)
   y=fcols(a['body'][2:],y)
   y=fnotice(D['workshopLeaves']['below'],y-8)
   # The full-page proposition supersedes the old habitat sketch; the service section follows.
  else:
   y=fp('The beautiful drawing<br/>has a reverse side.',0,530,327.5,29,29,'GB',FEATURE_BLUE,gap=14)
   leaf=D['workshopLeaves']['below-continued']
   y=fimage(TMP/'study-ocean-services.png',y,125,leaf['caption'])
   y=fp(leaf['title'],0,y,327.5,20,22,'GB')
   y=fp(leaf['text'],0,y,327.5,10.4,13.5,gap=18)
   y=fslips(key,y)
   fp(a['note'],0,y-6,327.5,7.5,9.8,'MONO')
 elif key=='slope':
  if i==0:
   y=fhead(a,d,'COND',49);y=fcols(a['body'][:3],y)
   fslips(key,y-10,D['featureMarginalia'][key][:1])
  elif i==1:
   fp('03 / SECCIÓN HABITADA',0,530,327.5,8,10,'AB',RUST)
   y=fimage(ROOT/'assets'/d['image'],500,240,d['caption'])
   y=fp(a['body'][3],0,y-12,307,18,21,'GI',RUST,gap=22)
   frule(y)
   y=fp(a['note'],0,y-12,327.5,8.4,11,'MONO');fslips(key,y-8,D['featureMarginalia'][key][1:2])
  elif i==2:
   y=fp('OUTSIDE\nTHE DOOR'.replace('\n','<br/>'),0,530,327.5,43,40,'COND',gap=18)
   y=fp(a['body'][4],0,y,327.5,14.2,18.2,'GI',RUST,gap=22)
   frule(y+3,RUST)
   y=fcols(a['body'][5:],y-13);fslips(key,y-12,D['featureMarginalia'][key][2:])
  else:
   ins=D['editionInserts']['slope-continued']
   y=fimage(ROOT/'assets/terrace-workshop.png',530,180,'LA TERRAZA / THE USE OF AN AFTERNOON')
   y=fp(ins['label'],0,y,327.5,6.8,8.5,'AB',RUST,gap=9)
   y=fp('Se hace camino<br/>al andar',0,y,327.5,27,27,'GB',gap=17)
   left=y
   for line in ins['lines']:left=fp(line,0,left,168,9.4,12,'GI',gap=1)
   left=fp(ins['credit'],0,left-12,160,6.8,8.5,'A')
   right=y
   for p in ins['body']:right=fp(p,181,right,146.5,9,11.6)
 elif key=='air':
  if i==0:
   y=fp(d['label'],0,530,327.5,7,9,'AB',FEATURE_RED,gap=10)
   y=fp('TAKE THE LIFT<br/>TO THE SKY',0,y,327.5,47,41,'COND',FEATURE_BLACK,gap=14)
   fimage(ROOT/'assets'/d['image'],y,min(370,y-26),d['caption'])
  elif i==1:
   y=fp('HEIGHT BECOMES<br/>A PUBLIC SERVICE.',0,530,327.5,34,33,'COND',FEATURE_RED,gap=15)
   y=fp(a['author'],0,y,327.5,7,9,'A',gap=17)
   y=fcols(a['body'][:4],y)
   frule(y-5,FEATURE_RED,weight=2)
   fp(a['body'][4],0,y-18,327.5,12.4,16,'GI',FEATURE_BLUE)
  elif i==2:
   y=fp('A CHAIN OF DESCENTS',0,530,327.5,29,30,'COND',gap=15)
   y=fimage(TMP/'airlift.png',y,122,'POWERED ASCENT / UNPOWERED GLIDE / PRINCIPLE ONLY')
   y=fcols(a['body'][5:],y)
   frule(y-6)
   fp(a['note'],0,y-17,327.5,7.5,9.8,'MONO')
  else:
   y=fp('THE LAST<br/>HUNDRED METRES',0,530,327.5,39,36,'COND',FEATURE_RED,gap=24)
   y=fslips(key,y)
   leaf=D['workshopLeaves']['air-continued']
   y=fimage(TMP/'study-landing.png',y-4,125,leaf['caption'])
   fnotice(leaf,y-4)
 C.restoreState()

def draw_clarke():
 C.saveState();C.translate(44,76);C.scale(1.6,1.6)
 a=D['clarkeLeaf'];y=fp('BETWEEN SESSIONS / COLOMBO — TENERIFE',0,530,327.5,7,9,'AB',RUST,gap=25)
 y=fp('Another island,<br/><i>another horizon.</i>',0,y,327.5,33,34,'G',gap=20)
 y=fp(a['deck'],0,y,327.5,12,15,'GI',gap=22)
 frule(y+7)
 y=fcols(a['body'],y-6,size=9.4,leading=12.2)
 y=fp(a['note'],0,y-22,327.5,14,18,'GI',RUST)
 # A small compositor's correction, attached to this conversation.

 C.restoreState()

def draw_production_note():
 C.saveState();C.translate(44,76);C.scale(1.6,1.6)
 y=fp('A NOTE ON THE DRAWINGS',0,530,327.5,28,29,'COND',gap=23)
 notes=[
 'This edition continues the imagined conference. The new plates — including the inhabited ocean, village stair and architectural gathering — are generated artwork made with OpenAI’s image-generation tool in November 2026. They are not recovered drawings, photographs or designs by the historical contributors. The working-table picture is an imagined gathering; its thread model illustrates a conversation, not a verified engineering structure.',
 'The new Arthur C. Clarke conversation is original fiction. His residence in Sri Lanka, his interest in diving and the 1977 publication of The View from Serendip supply the historical setting; his Tenerife visit, the coffee spill and all exchanges here are invented. No passage is quoted from that book. Reference: the Smithsonian National Air and Space Museum’s Arthur C. Clarke Collection of Sri Lanka, “The View from Serendip” manuscript catalogue (si.edu).',
 'The design takes lessons from the coexistence of enormous headlines, narrow reporting columns, notices and images in Jericho, the Habitat newspaper, 1 June 1976 (Habitat Archive, University of British Columbia). Its historical pages are references, not material reproduced in this magazine.',
 'The body text, personal recollections and friendships remain. This pass lets the contributions arrive in different visual hands. Their systems are incomplete; the lives around them will always exceed the drawing.',
 'Conceived and edited by Anselm. Writing, layout and production in collaboration with Codex. Digital font revivals are listed in the repository; all font files used here are embedded. The imaginary date inside the magazine remains 1977.'
 ]
 for p in notes:y=fp(p,0,y,327.5,10,13.2,gap=14)
 frule(y-10)
 fp('HORIZONS ’77 / DESIGN PROOF / NOVEMBER 2026',0,y-25,327.5,7,9,'MONO')
 C.restoreState()
