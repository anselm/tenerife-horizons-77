"""Three inhabited spreads: real type follows the spaces left by the drawing."""
def world_background(asset,side):
 panorama(asset,side)

def shaped_copy(ps,frames,size=9.4,leading=12.2):
 style=ParagraphStyle('shaped',fontName='G',fontSize=size,leading=leading,textColor=FEATURE_BLACK,allowWidows=0,allowOrphans=0,splitLongWords=1)
 queue=[Paragraph(re.sub(r'\s+(\S+)$',r'&nbsp;\1',feature_clean(t)),style) for t in ps]
 for x,top,w,height in frames:
  y=top;floor=top-height
  while queue:
   p=queue[0];_,h=p.wrap(w,max(0,y-floor))
   if h<=y-floor:
    p.drawOn(C,x,y-h);feature_checks.append(dict(page=N,type='text',x=x,top=y,bottom=y-h,width=w,size=size));y-=h+9;queue.pop(0)
   else:
    parts=p.split(w,max(0,y-floor))
    if len(parts)>1:
     p=parts[0];_,h=p.wrap(w,y-floor);p.drawOn(C,x,y-h)
     feature_checks.append(dict(page=N,type='text',x=x,top=y,bottom=y-h,width=w,size=size));queue=parts[1:]+queue[1:]
    break
 if queue:raise Exception(f'Shaped copy overflow on {N}: {len(queue)} fragments')

def draw_ocean_world(side):
 a=A['below'];world_background('ocean-inhabited-spread.png',side);contribution_frame()
 if side==0:
  fp('OCEAN WORKSHOP / 02',0,530,270,7,9,'MONO',FEATURE_BLUE)
  fp('A ROOM IN<br/>THE ATLANTIC',0,505,327.5,43,40,'COND',FEATURE_BLUE)
  fp('Una stanza, non un impero.',0,412,270,15,18,'G',FEATURE_BLUE)
  shaped_copy(a['body'][:1],[(0,374,198,36.7),(0,337.4,177,36.7),(0,300.8,151,73.3)])
 else:
  fp('THE EXTRAORDINARY<br/>becomes ordinary.',0,130,327.5,18,18,'G',FEATURE_BLUE,gap=10)
  fp(a['body'][1],0,82,327.5,9.4,12.2)
 C.restoreState()

def draw_village_world(s):
 a=D['alexanderEssay'];i=s['part']
 if i<2:
  world_background('village-stair-spread.png',i);contribution_frame()
  if i==0:
   fp('LIFE & FORM / BOCACANGREJO',0,530,300,7,9,'MONO',RUST)
   fp('The village<br/>that built us.',0,510,300,32,31,'GB')
   fp('CHRISTOPHER ALEXANDER',0,439,220,7,9,'MONO')
   shaped_copy(a['sections'][0]['body'][:1],[(0,418,230,36.7),(0,381.4,188,36.7),(0,344.8,145,36.7),(0,308.2,101,36.7),(0,271.6,55,36.7)],9.4,12.2)
  else:
   fp('The way down',46,203,281.5,25,27,'GB',RUST)
   fp(a['sections'][0]['body'][1],46,164,281.5,10,13)
  C.restoreState();return
 contribution_frame();sec=a['sections'][i-2]
 if i==2:
  fp('01',0,530,100,64,64,'G',RUST)
  y=fp('A landing.<br/>A bucket.<br/>A little room for another life.',112,526,215.5,25,27,'GB',gap=28)
  frule(y+6,RUST)
  y=fp(sec['body'][2],0,y-12,237,11.2,15,gap=20)
  y=fp(sec['body'][3],67,y,260.5,11.2,15,gap=30)
  frule(y,RUST)
  fp('DEL CUADERNO DE LA EXCURSIÓN',0,y-13,327.5,7,9,'MONO',RUST)
 elif i==3:
  y=fp(sec['heading'],0,530,327.5,27,29,'GB',gap=24)
  y=fcols(sec['body'][:2],y,10,13)
  frule(y-6,RUST,weight=2)
  y=fp(sec['body'][2],0,y-24,327.5,32,32,'GB',RUST,gap=24)
  fcols(sec['body'][3:],y,10,13)
 else:
  y=fp(sec['heading'],0,530,327.5,31,31,'GB',gap=22)
  y=fcols(sec['body'],y,9.4,12.2)
  if i==4:
   frule(y-10,RUST)
   fp('MEMORIA DEL LUGAR / The conquest of Tenerife ended in 1496. It brought enslavement and assimilation, but Indigenous people and customs persisted. The island did not begin with the conquerors’ maps.',0,y-23,327.5,8.2,10.6,'G')

 C.restoreState()

def table_band(side):
 # A single drawing runs across the binding; captions and all prose remain type.
 C.saveState();C.scale(1.6,1.6);C.translate(-(8.5 if N%2 else 5),0)
 clip=C.beginPath();clip.rect(-9,-9,414,630);C.clipPath(clip,stroke=0,fill=0)
 C.setFillColor(CREAM);C.rect(-9,-9,414,630,fill=1,stroke=0)
 image(ROOT/'assets/architects-working-table.png',-9-side*396,210,810,300,crop=False)
 C.setFillColor(FEATURE_BLACK);C.setFont('A',6);C.drawString(32,18,'HORIZONS / 1977');C.drawRightString(364,18,str(N));C.restoreState()

def draw_table_world(s):
 a=A['table'];i=s['part']
 if i<2:table_band(i)
 contribution_frame()
 if i==0:
  fp('ARCHITECTURE / CONVERSATIONS AT THE TABLE',0,530,327.5,7,9,'MONO',RUST)
  fp('Three seats.<br/>More than three minds.',0,505,327.5,29,29,'G')
  fp(a['body'][0],0,174,327.5,10,13)
 elif i==1:
  fp('SOLERI / ROSSI / FULLER / SNELSON',0,530,327.5,7,9,'MONO',RUST)
  fp('Different drawings.<br/>The same island.',0,505,327.5,29,29,'G')
  fp(a['body'][1],0,174,155.75,9.4,12.2)
  fp(a['body'][2],171.75,174,155.75,9.4,12.2)
 elif i==2:
  fp('HELD APART.',0,530,327.5,43,42,'COND')
  y=fp('Held together.',0,478,327.5,37,40,'GB',RUST,gap=16)
  y=fimage(TMP/'study-tensegrity.png',y,125,'COMPRESSION / TENSION / A PRINCIPLE STUDY')
  y=fcols([a['body'][3]],y-12,10,13)
  frule(y-9,RUST)
  fp(a['body'][4],0,y-23,327.5,11,14,'GI')
 else:
  y=fp('Leave the table open',0,530,327.5,29,31,'G',gap=18)
  y=fcols(a['body'][5:],y,9.4,12.2)
  y=fp(a['note'],0,y-8,327.5,7.3,9.5,'MONO',gap=14)
  ins=D['editionInserts']['table-continued'];frule(y,RUST)
  y=fp(ins['label'],0,y-10,327.5,7,9,'MONO',RUST)
  y=fp(ins['title'],0,y,327.5,22,24,'GB',gap=16)
  top=y
  for line in ins['printLines']:y=fp(line,0,y,155.75,18,23,'AR',gap=2)
  z=top
  for line in ins['translation']:z=fp(line,171.75,z,155.75,9.4,12.2,'GI',gap=0)
  y=fp(ins['credit'],0,min(y,z)-12,327.5,6.7,9,'A')
  fcols(ins['body'],y-6,9.4,12.2)
 C.restoreState()
