# Digest-only composition: physical book first, with individually sized plates.
_base_art=art
_plate_heights={9:245,12:245,14:310,17:225,19:230,21:290,28:210,31:270,35:230,37:220,39:175}
def art(kind,top,h=165):
 return _base_art(kind,top,_plate_heights.get(N,h))

_base_supporting_leaf=supporting_leaf
insertlog=[]
def reading_insert(key,bottom):
 insert=D.get('editionInserts',{}).get(key)
 if not insert:return bottom
 top=bottom-20;placements=[]
 def put(t,x,y,w,size=11.8,font='G',leading=None,color=INK,gap=9):
  p=para(t,size,leading,font,color,space=0);_,height=p.wrap(w,1000)
  placements.append((p,x,y-height));return y-height-gap
 y=put(insert['label'],44,top-10,524,8,'AB',11,RUST,12)
 y=put(insert['title'],44,y,524,22,'BD',25,INK,18)
 art_bounds=None
 if insert.get('art'):
  path=TMP/('study-'+insert['art']+'.png')
  image_y=y-130;art_bounds=image_bounds(path,44,image_y,524,130)
  y=caption(insert['caption'],art_bounds,draw=False)-16
 if insert.get('lines'):
  verse_y=y;wide=insert.get('wide');width=524 if wide else 250
  for i,line in enumerate(insert['lines']):
   if not line:verse_y-=10;continue
   if insert.get('lang')=='ar':
    p=para(insert['printLines'][i],22,29,'AR',space=0);p.style.alignment=2;_,h=p.wrap(width,1000)
    placements.append((p,44,verse_y-h));verse_y-=h+2
   else:verse_y=put(line,44,verse_y,width,13,'G',17,INK,0)
  if insert.get('translation'):
   right_y=y
   for line in insert['translation']:right_y=put(line,318,right_y,250,12,'GI',18,INK,0)
   y=min(verse_y,right_y)-12
   y=put(insert['credit'],44,y,524,8,'A',11,TEAL,14)
  elif wide:
   y=put(insert['credit'],44,verse_y-12,524,8,'A',11,TEAL,16)
  else:
   right_y=y
   for p in insert['body']:right_y=put(p,318,right_y,250,11.5,leading=15)
   y=put(insert['credit'],44,min(verse_y,right_y)-12,524,8,'A',11,TEAL,0)
  if not wide and not insert.get('translation'):
   content_bottom=y
  else:content_bottom=None
 else:content_bottom=None
 if content_bottom is None:
  paras=insert['body'];cut=(len(paras)+1)//2;ends=[]
  for x,part in [(44,paras[:cut]),(318,paras[cut:])]:
   yy=y
   for p in part:yy=put(p,x,yy,250,11.5,leading=15)
   ends.append(yy)
  content_bottom=min(ends)
 if content_bottom<70:raise Exception(f'Reading insert overflow on {N} ({key}): {content_bottom:.1f}')
 rule(top)
 if art_bounds:
  image(path,44,image_y,524,130);caption(insert['caption'],art_bounds)
 for p,x,y in placements:p.drawOn(C,x,y)
 insertlog.append({'page':N,'key':key,'bottom':round(content_bottom,2)})
 return content_bottom

def supporting_leaf(key,bottom):
 remaining=bottom if key in D.get('editionInserts',{}) else _base_supporting_leaf(key,bottom)
 return reading_insert(key,remaining if remaining is not None else bottom)
