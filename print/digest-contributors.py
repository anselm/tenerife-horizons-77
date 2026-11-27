"""Contributions arrive in different hands. Physical-point digest compositions."""
pdfmetrics.registerFont(TTFont('BOOK',F+'URWBookman-Demi.ttf'))
CREAM=CMYKColor(0,.025,.09,0)
GOLD=CMYKColor(0,.25,.95,0)

def contribution_frame():
 C.saveState();C.translate(44,76);C.scale(1.6,1.6)

def contribution_end(y):
 C.restoreState();return 76+y*1.6

def panorama(path,side):
 # Work directly in trim coordinates, independent of mirrored text margins.
 C.saveState();C.scale(1.6,1.6);C.translate(-(8.5 if N%2 else 5),0)
 clip=C.beginPath();clip.rect(-9,-9,414,630);C.clipPath(clip,stroke=0,fill=0)
 C.setFillColor(CREAM);C.rect(-9,-9,414,630,fill=1,stroke=0)
 image(ROOT/'assets'/path,-9-side*396,3 if path.startswith('dreaming') else -9,810,630,crop=True)
 C.setFillColor(CREAM);C.rect(345,12,27,14,fill=1,stroke=0)
 if side==0:C.rect(29,12,91,14,fill=1,stroke=0)
 C.setFillColor(FEATURE_BLACK);C.setFont('A',6)
 if side==0:C.drawString(32,18,'HORIZONS / 1977')
 C.drawRightString(364,18,str(N))
 C.restoreState()

def draw_panorama(s):
 side=s['side'];family=s['family']
 panorama('dreaming-together-collage.png' if family=='fr' else 'film-desk-castle.png',side)
 contribution_frame()
 if family=='fr':
  a=D['openingFeatures']['fr']
  if side==0:
   fp('Rêver à<br/>plusieurs',0,520,327.5,40,38,'GB',FEATURE_BLUE)
   fp('FORMES VIVANTES / TENERIFE, 1977',0,430,327.5,7,9,'MONO',FEATURE_BLUE)
  C.setFillColor(CREAM);C.rect(-4,-3,335.5,72,fill=1,stroke=0)
  fp(a['body'][side],0,62,327.5,9.2,11.5,gap=0)
 else:
  if side==0:
   fp('The plan<br/>has tenants.',0,520,275,36,35,'G',FEATURE_BLACK)
   fp('FILM DESK / A MARGINAL DRAWING',0,431,270,6.8,9,'MONO')
   fp('Allow room<br/>for the people.',0,122,168,19,22,'GB')
  else:
   C.setFillColor(CREAM);C.rect(132,0,195,34,fill=1,stroke=0)
   fp('LÁMINA / A MUNICIPALITY OF DRAWERS,\nBALCONIES & UNFORESEEN INHABITANTS'.replace('\n','<br/>'),140,25,180,6.3,8,'MONO')
 C.restoreState()

def pasted_heading(words,x,top,width,size=28,font='COND',dark=False,angle=0):
 # Only a short heading slip moves; the reading columns stay square to the page.
 C.saveState();C.translate(x,top-100);C.rotate(angle)
 C.setFillColor(FEATURE_BLACK if dark else CMYKColor(0,.02,.065,0));C.rect(-5,100-size-9,width,size+14,fill=1,stroke=0)
 C.setStrokeColor(FEATURE_BLACK);C.setLineWidth(.4);C.line(-5,100-size-9,width-5,100-size-9)
 fp(words,2,99,width-14,size,size*1.04,font,CMYKColor(0,0,0,0) if dark else FEATURE_BLACK,gap=0)
 C.restoreState()

def interview_pairs(body,top):
 y=top
 style=ParagraphStyle('interview',fontName='G',fontSize=9.1,leading=11.3,textColor=FEATURE_BLACK,splitLongWords=1)
 for pair in range(0,len(body),2):
  row=[]
  for j,copy in enumerate(body[pair:pair+2]):
   p=Paragraph(feature_clean(copy),style);_,h=p.wrap(147.75,2000);row.append((p,j*171.75,h))
  h=max(h for _,_,h in row)
  if y-h-8<0:raise Exception(f'Interview overflow {N}')
  for j,(p,x,ph) in enumerate(row):
   if j==0:
    C.setFillColor(CMYKColor(0,.02,.065,0));C.rect(x-4,y-h-4,163.75,h+8,fill=1,stroke=0)
   C.setStrokeColor(FEATURE_BLACK);C.setLineWidth(.35);C.line(x,y+4,x+155.75,y+4)
   p.drawOn(C,x+4,y-ph)
   feature_checks.append(dict(page=N,type='interview',x=x+4,top=y,bottom=y-ph,width=147.75,size=9.1))
  y-=h+13
 return y

def draw_contribution(s):
 a=s.get('a',{});t=s.get('t',a);key=s['key'];kind=s['kind'];opening=kind!='continued'
 contribution_frame();y=530
 if kind=='editorial':
  lang=s['lang'];body=s['body']
  if lang=='en' and s.get('openingpart'):
   fp('EDITORIAL / SECOND SHEET',0,530,327.5,7,9,'MONO')
   pasted_heading('Fifty years from here',4,500,319,25,'GB',angle=.35)
   y=fp(body[0],0,450,327.5,10.4,13.5,gap=20)
   y=fcols(body[1:],y,size=10.4,leading=13.5,paper='editorial')
  elif lang=='en':
   fp('THE EDITORS / TENERIFE',0,530,236,7,9,'MONO')
   fp('1977',248,531,80,27,27,'COND',FEATURE_RED)
   pasted_heading('AN ISLAND',1,501,270,46,'COND',dark=True,angle=-.4)
   pasted_heading('is a beginning.',45,438,278,31,'GB',angle=.5)
   y=fcols(body,380,paper='editorial')
  elif lang=='es':
   fp('MESA DEL TERRITORIO / COPIA DE TRABAJO',0,530,327.5,7,9,'MONO')
   pasted_heading('LA ISLA',0,502,250,54,'COND',angle=.25)
   pasted_heading('NO ESTÁ VACÍA',52,436,275,28,'COND',dark=True,angle=-.5)
   y=fp(t['subtitle'],0,386,327.5,11,14,'GB',gap=17)
   y=fcols(body,y,paper='territory')
   y=fp('LOS NOMBRES ANTES QUE LOS PLANOS',0,y-15,327.5,7,9,'MONO')
  elif lang=='fr':
   fp('FORMES VIVANTES / FEUILLET DE DISCUSSION',0,530,327.5,7,9,'MONO',FEATURE_BLUE)
   pasted_heading('SANS CENTRE',0,500,282,34,'COND',dark=True,angle=-.35)
   pasted_heading('UNIQUE',124,453,203.5,32,'BOOK',angle=.4)
   y=fcols(body,396,paper='letters')
   y=fp(t['subtitle'],0,y-17,327.5,12.4,15.5,'G',FEATURE_BLUE)
  elif lang=='it':
   fp('DALLA SALA COMUNE',0,530,327.5,7,9,'MONO')
   pasted_heading('ABITARE',0,512,240,48,'COND',dark=True,angle=.3)
   y=fp('Una porta da chiudere',22,452,305.5,25,28,'BOOK',gap=18)
   y=fcols(body,y,paper='household')
   frule(y-12,FEATURE_RED,weight=2)
   y=fp(t['subtitle'],0,y-25,327.5,13,17,'G')
  else:
   fp('AUS DEM AUSFLUGSHEFT / ICOD',0,530,327.5,7,9,'MONO')
   pasted_heading('Unter dem Drachenbaum',0,501,327.5,29,'COND',angle=-.25)
   y=fcols(body,459,size=9.4,leading=12.2,paper='notebook')
 elif kind=='assembly':
  a=s['a'];labels={'kitchen-desk':'DE LA COCINA','letters-desk':'CORREO','accounts-desk':'CAJA / 1977','closing-desk':'ÚLTIMA HORA'}
  if key!='closing-desk':fp('SECRETARÍA / HOJAS RECIBIDAS',0,530,327.5,7,9,'MONO')
  pasted_heading(labels[key],0,530 if key=='closing-desk' else 508,327.5,30,'MONO' if key=='kitchen-desk' else 'COND',dark=key=='letters-desk',angle=.25 if key=='accounts-desk' else -.3)
  y=fp(a['title'],0,489 if key=='closing-desk' else 461,327.5,18,20,'GB',gap=8)
  y=fp(a['deck'],0,y,327.5,9.5,12,'G',gap=12)
  y=interview_pairs(a['body'],y) if key=='kitchen-desk' else fcols(a['body'],y,size=9.1,leading=11.5,paragraph_gap=7 if key=='closing-desk' else 9,paper='letters' if key=='letters-desk' else 'accounts')
  p=Paragraph(clean(a['notice']),ParagraphStyle('notice',fontName='MONO',fontSize=8,leading=10.3))
  _,h=p.wrap(307.5,600)
  if y-h-18<0:raise Exception(f'Notice overflow {key}: y={y} h={h}')
  C.setFillColor(CMYKColor(0,.03,.12,0));C.rect(0,y-h-18,327.5,h+12,fill=1,stroke=0)
  C.setStrokeColor(FEATURE_BLACK);C.setLineWidth(.5);C.line(0,y-h-18,327.5,y-h-18)
  C.setFillColor(CMYKColor(0,.06,.24,.05));C.rect(19,y-10,32,8,fill=1,stroke=0)
  y=fp(a['notice'],10,y-12,307.5,8,10.3,'MONO')

 else:
  aid=a.get('id');body=s['body'];title=t['title'] if opening else t.get('continuationTitle',t['title'])
  if not opening:
   y=fp(title,0,530,327.5,22,25,'COND',gap=14)
   y=fcols(body,y,size=9.0,leading=11.5) if aid=='afterword' else fcols(body,y)
  elif aid=='sun':
   C.setFillColor(GOLD);C.rect(-6,330,339.5,210,fill=1,stroke=0)
   fp('THE SUN',8,519,310,52,52,'COND')
   fp('has no accounts\ndepartment'.replace('\n','<br/>'),8,457,310,29,31,'GB')
   y=fp(t['author'],8,355,310,7,9,'MONO',gap=28)
   y=fcols(body,y)
  elif aid=='credit':
   C.setStrokeColor(FEATURE_RED);C.setLineWidth(2);C.rect(-8,336,343.5,198,fill=0,stroke=1)
   fp('COOPERATIVA DEL PORVENIR',8,519,310,7.5,10,'MONO',FEATURE_RED)
   fp('A share in\nthe long view.'.replace('\n','<br/>'),8,486,308,36,36,'GB',FEATURE_RED)
   fp('PROPOSED SUBSCRIPTION / 1977',8,358,310,8,10,'MONO')
   y=fcols(body,311)
  elif aid=='maathai':
   fp('KENYA',0,530,327.5,13,16,'MONO',TEAL)
   fp('1977',0,497,327.5,65,65,'COND',TEAL)
   y=fp(t['title'],0,420,327.5,28,28,'GB',gap=20)
   y=fcols(body,y)
  elif aid=='goodall':
   y=fp('A place for\nother lives'.replace('\n','<br/>'),0,530,327.5,39,38,'COND',gap=22)
   frule(y+6,TEAL,weight=3)
   y=fp(t['author'],0,y-8,327.5,7.5,10,'MONO',gap=22)
   y=fcols(body,y)
  elif aid=='coast':
   y=fp('The afternoon\nwithout a shore'.replace('\n','<br/>'),0,530,327.5,31,32,'G',gap=16)
   y=fcols(body,y)
   if y>150:y=fimage(ROOT/'assets/montana-amarilla-v2.png',y-12,min(200,y-38),'MONTAÑA AMARILLA / DEL CUADERNO DEL AGUA')
  elif aid=='cousteau':
   y=fimage(ROOT/'assets/ocean-observatory.png',530,130,'CARNET DE TÉLÉVISION / UNE FENÊTRE, DU TEMPS')
   y=fp(t['title'],0,y,327.5,28,28,'COND',FEATURE_BLUE,gap=16)
   y=fcols(body,y)
  elif aid=='gilliam':
   y=fp('A future with\nfingerprints'.replace('\n','<br/>'),0,530,327.5,34,33,'BOOK',gap=20)
   y=fcols(body,y)
  elif aid=='table':
   y=fp('Three seats\nat the table'.replace('\n','<br/>'),0,530,327.5,37,35,'G',gap=20)
   y=fcols(body,y)
   if y>150:y=fimage(TMP/'study-tensegrity.png',y-8,min(160,y-35),'COMPRESSION / TENSION / TWO MINDS AT WORK')
  else:
   y=fp(title,0,530,327.5,28 if aid=='afterword' else 35,29 if aid=='afterword' else 36,'G',gap=18)
   y=fcols(body,y)
  if not opening and a.get('note'):
   frule(y-4);y=fp(a['note'],0,y-16,327.5,8,10.5,'MONO')
 return contribution_end(y)

# Ordinary illustrations no longer fill every unused rectangle. Notes survive.
def supporting_leaf(key,bottom):
 if key=='afterword-continued':return bottom
 if key in D.get('editionInserts',{}):return reading_insert(key,bottom)
 leaf=D['workshopLeaves'].get(key)
 if not leaf:return bottom
 contribution_frame();top=(bottom-76)/1.6-16
 title=Paragraph(clean(leaf['title']),ParagraphStyle('leafh',fontName='GB',fontSize=16,leading=18))
 body=Paragraph(clean(leaf['text']),ParagraphStyle('leafp',fontName='G',fontSize=9,leading=11.5))
 _,hh=title.wrap(327.5,1000);_,bh=body.wrap(327.5,1000)
 if top-hh-bh-35>0:
  frule(top);y=fp(leaf['label'],0,top-8,327.5,6.5,8,'MONO',RUST)
  y=fp(leaf['title'],0,y,327.5,16,18,'GB');y=fp(leaf['text'],0,y,327.5,9,11.5)
 C.restoreState()
 return bottom


def draw_drago_photo():
 contribution_frame()
 fimage(ROOT/'assets/drago-excursion-halftone.png',530,492,'ICOD DE LOS VINOS / AUS DEM AUSFLUGSHEFT / 1977')
 C.restoreState()


def draw_letters_leaf():
 contribution_frame();a=D['editionInserts']['afterword-continued']
 y=fp('CORRESPONDANCE',0,530,327.5,8,10,'MONO',FEATURE_RED,gap=24)
 y=fp(a['title'],0,y,327.5,34,36,'GB',gap=27)
 for i,p in enumerate(a['body']):
  y=fp(p,18 if i%2 else 0,y,300,10.4,13.7,'G',gap=15)
 C.restoreState()
