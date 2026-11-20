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
   fp('The plan<br/><i>has tenants.</i>',0,520,275,36,35,'G',FEATURE_BLACK)
   fp('FILM DESK / A MARGINAL DRAWING',0,431,270,6.8,9,'MONO')
   fp('Allow room<br/>for the people.',0,122,168,19,22,'GI')
  else:
   C.setFillColor(CREAM);C.rect(132,0,195,34,fill=1,stroke=0)
   fp('LÁMINA / A MUNICIPALITY OF DRAWERS,\nBALCONIES & UNFORESEEN INHABITANTS'.replace('\n','<br/>'),140,25,180,6.3,8,'MONO')
 C.restoreState()

def draw_contribution(s):
 a=s.get('a',{});t=s.get('t',a);key=s['key'];kind=s['kind'];opening=kind!='continued'
 contribution_frame();y=530
 if kind=='editorial':
  lang=s['lang'];body=s['body']
  if lang=='en' and s.get('openingpart'):
   y=fp('Fifty years from here',0,530,327.5,32,35,'GI',FEATURE_RED,gap=24)
   y=fcols(body,y,size=10.4,leading=13.5)
  elif lang=='en':
   fp('1977',0,530,327.5,47,47,'COND',FEATURE_RED,gap=0)
   y=fp('An island is <i>a beginning.</i>',0,473,327.5,27,28,'G',gap=15)
   frule(y+4,FEATURE_RED,weight=2)
   y=fcols(body,y-8)
  elif lang=='es':
   fp('LA ISLA',0,530,327.5,57,54,'COND',FEATURE_BLACK)
   y=fp('no está vacía',0,470,327.5,35,38,'GI',gap=16)
   frule(y+4,FEATURE_BLACK,weight=3)
   y=fp(t['subtitle'],0,y-8,327.5,11,14,'GB',gap=17)
   y=fcols(body,y)
   y=fp('MESA DEL TERRITORIO / LOS NOMBRES ANTES QUE LOS PLANOS',0,y-15,327.5,7,9,'MONO')
  elif lang=='fr':
   y=fp('Sans centre unique',0,530,327.5,32,34,'GI',FEATURE_BLUE,gap=24)
   y=fcols(body,y)
   y=fp(t['subtitle'],0,y-17,327.5,12.4,15.5,'GI',FEATURE_BLUE)
  elif lang=='it':
   fp('abitare',0,530,327.5,62,62,'GI',FEATURE_RED)
   y=fp('Una porta da chiudere',0,452,327.5,25,28,'GB',gap=18)
   y=fcols(body,y)
   frule(y-12,FEATURE_RED,weight=2)
   y=fp(t['subtitle'],0,y-25,327.5,13,17,'GI')
  else:
   y=fp('Unter dem\nDrachenbaum'.replace('\n','<br/>'),0,530,327.5,28,28,'G',gap=15)
   y=fcols(body,y,size=9.4,leading=12.2)
 elif kind=='assembly':
  a=s['a'];labels={'kitchen-desk':'DE LA COCINA','letters-desk':'CORREO','accounts-desk':'CAJA / 1977','closing-desk':'ÚLTIMA HORA'}
  y=fp(labels[key],0,530,327.5,34,34,'COND',FEATURE_BLACK,gap=6)
  frule(y,FEATURE_BLACK,weight=3)
  y=fp(a['title'],0,y-9,327.5,18,20,'GB',gap=8)
  y=fp(a['deck'],0,y,327.5,9.5,12,'GI',gap=10)
  y=fcols(a['body'],y,size=9.1,leading=11.5,paragraph_gap=7)
  p=Paragraph(clean(a['notice']),ParagraphStyle('notice',fontName='MONO',fontSize=8,leading=10.3))
  _,h=p.wrap(307.5,600)
  if y-h-18<0:raise Exception(f'Notice overflow {key}: y={y} h={h}')
  C.setStrokeColor(FEATURE_BLACK);C.setLineWidth(1.2);C.rect(0,y-h-18,327.5,h+12,fill=0,stroke=1)
  y=fp(a['notice'],10,y-12,307.5,8,10.3,'MONO')
 else:
  aid=a.get('id');body=s['body'];title=t['title'] if opening else t.get('continuationTitle',t['title'])
  if not opening:
   y=fp(title,0,530,327.5,24,27,'GI',gap=14)
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
   y=fp('A place for\nother lives'.replace('\n','<br/>'),0,530,327.5,39,38,'GI',gap=22)
   frule(y+6,TEAL,weight=3)
   y=fp(t['author'],0,y-8,327.5,7.5,10,'MONO',gap=22)
   y=fcols(body,y)
  elif aid=='coast':
   y=fp('The afternoon\nwithout a shore'.replace('\n','<br/>'),0,530,327.5,31,32,'G',gap=16)
   y=fcols(body,y)
   if y>150:y=fimage(ROOT/'assets/montana-amarilla-v2.png',y-12,min(200,y-38),'MONTAÑA AMARILLA / DEL CUADERNO DEL AGUA')
  elif aid=='cousteau':
   y=fimage(ROOT/'assets/ocean-observatory.png',530,130,'CARNET DE TÉLÉVISION / UNE FENÊTRE, DU TEMPS')
   y=fp(t['title'],0,y,327.5,28,28,'GI',FEATURE_BLUE,gap=16)
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
 y=fp(a['title'],0,y,327.5,34,36,'GI',gap=27)
 for i,p in enumerate(a['body']):
  y=fp(p,18 if i%2 else 0,y,300,10.4,13.7,'G',gap=15)
 C.restoreState()
