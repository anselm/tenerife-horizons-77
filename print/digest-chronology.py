"""A conference file assembled in the voice of 1977. Live type, measured slips, no raster essays."""
def draw_chronology(side):
 d=D['conferenceTimeline'];contribution_frame()
 frule(532,FEATURE_BLACK,weight=3)
 if side==0:
  fp('FROM THE CONFERENCE FILE / 1967–1976',0,523,327.5,6.5,8,'MONO')
  fp('People kept',0,507,327.5,35,35,'COND')
  fp('meeting.',179,475,148.5,32,32,'GI',FEATURE_RED)
  fp(d['intro'],0,437,327.5,9.4,11,'G',gap=0)
  rows=d['events'][:8];y=393
 else:
  fp('THE HINGE / HERE & AFTER',0,523,327.5,7,9,'MONO')
  fp('1977',0,505,327.5,72,70,'COND',FEATURE_RED)
  fp('and the rooms still to come.',0,428,327.5,23,25,'GI')
  fp('From this year’s festivals and assemblies to the meetings now being prepared: the conversation travels on.',0,391,327.5,10,12,'G')
  rows=d['events'][8:];y=358
 for i,e in enumerate(rows):
  if side and i==2:
   C.setStrokeColor(FEATURE_RED);C.setLineWidth(1);C.line(0,y-1,327.5,y-1);y-=8
  label=f"{e['year']} / {e['city']}"
  copy=f"<b>{e['title']}.</b> {e['body']}"
  p=Paragraph(copy,ParagraphStyle('chronology',fontName='G',fontSize=9.4,leading=11,textColor=FEATURE_BLACK,alignment=0,splitLongWords=1))
  _,h=p.wrap(315.5,600);height=h+18;bottom=y-height
  if bottom<49:raise Exception(f'Chronology slip overflow {label}: {bottom}')
  C.setFillColor(CMYKColor(0,.015,.055,0) if i%3 else CMYKColor(0,0,0,.035))
  C.rect(0,bottom,327.5,height,fill=1,stroke=0)
  C.setStrokeColor(CMYKColor(0,0,0,.43));C.setLineWidth(.35)
  C.line(0,bottom,327.5,bottom);C.line(327.5,bottom,327.5,y)
  fp(label,6,y-4,315.5,7.1,8,'MONO',gap=0)
  p.drawOn(C,6,y-14-h)
  feature_checks.append({'page':N,'type':'chronology-slip','top':y,'bottom':bottom,'x':0,'width':327.5,'size':9.4,'year':e['year']})
  y=bottom-4
 if side:
  note=Paragraph(d['note'],ParagraphStyle('chronology-note',fontName='MONO',fontSize=8,leading=10,textColor=FEATURE_BLACK))
  _,h=note.wrap(307.5,300);bottom=y-h-19
  if bottom<49:raise Exception(f'Chronology note overflow: {bottom}')
  C.setFillColor(CMYKColor(0,.04,.19,0));C.rect(0,bottom,327.5,h+12,fill=1,stroke=0)
  note.drawOn(C,10,bottom+6)
  C.setFillColor(CMYKColor(0,.06,.24,.06));C.rect(21,y-11,36,7,fill=1,stroke=0)
 frule(43,FEATURE_BLACK,weight=.5)
 fp('PRÓXIMAS REUNIONES / DATES TO KEEP IN THE DIARY' if side else 'DEL ARCHIVO DE TRABAJO / PAPERS PASSED FROM HAND TO HAND',0,37,327.5,6.5,8,'MONO',gap=0)
 contribution_end(0)


def draw_future_plans():
 d=D['conferenceTimeline']['plans'];contribution_frame()
 frule(532,FEATURE_BLACK,weight=3)
 fp('PROPOSALS / NOT PROPHECIES',0,523,327.5,7,9,'MONO')
 fp('Already on',0,513,327.5,31,32,'COND')
 fp('the drawing board.',0,478,327.5,28,29,'GI',FEATURE_RED)
 y=fp(d['intro'],0,439,327.5,10,12,'G',gap=10)
 for i,item in enumerate(d['items']):
  # Different kinds of paper: a short report, an exhibition prospectus, a notice.
  copy=item['body']
  if i==1:
   measure=Paragraph(feature_clean(copy),ParagraphStyle('measure',fontName='G',fontSize=9.4,leading=11.6))
   _,body_h=measure.wrap(327.5,1000)
   panel_h=57+body_h
   C.setFillColor(CMYKColor(0,.035,.13,0));C.rect(-5,y+7-panel_h,337.5,panel_h,fill=1,stroke=0)
  frule(y+4,FEATURE_BLACK,weight=.5 if i!=2 else 1.3)
  y=fp(item['label'],0,y-4,327.5,6.7,8,'MONO',gap=7)
  y=fp(item['title'],0,y,327.5,17 if i!=1 else 20,20,'GB' if i!=1 else 'COND',gap=7)
  y=fp(copy,0,y,327.5,9.4,11.6,'G',gap=10)
 y=fp(d['later'],0,y,327.5,7.2,9,'MONO',gap=12)
 if y<38:raise Exception(f'Plans page source clearance: {y}')
 frule(y+3,FEATURE_BLACK,weight=.5)
 fp('TENERIFE / CONFERENCE FILE / 1977',0,y-4,327.5,6.3,7.7,'MONO',gap=0)
 contribution_end(0)
