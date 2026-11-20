"""Mixam digest: reflowed text, mirrored glue margins, separate outside cover."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'print/build.py').read_text().split('r=PdfReader(MASTER);writer=PdfWriter();order=[]')[0]
source=source.replace('W,H=612,792;','W,H=612,979.2;').replace("MASTER=OUT/'Horizons-77-print-letter.pdf'","MASTER=OUT/'Horizons-77-digest-interior.pdf'").replace('pagesize=(W,H)','pagesize=(414,630)').replace(' y=718\n',' y=905.2\n').replace('size=sz,cols=3','size=sz,cols=2').replace('if cols==3:','if leading is not None:')
# Give the self-contained coastal afternoon a larger plate on the taller digest page.
source=source.replace("165 if a['art'] in ['coast','observatory'] else 150", "310 if a['art']=='coast' else 165 if a['art']=='observatory' else 150")
source=source.replace(" t=clean(t);t=re.sub"," size=size*(1.12 if LEGACY_N>=46 or LEGACY_N in [18,20,22,29,33,36,40,42,43,44,45] else 1.20) if font in ['G','GI','GB'] else max(size,9.6)\n if leading is not None:leading=max(leading*1.10,size*1.22)\n space=min(space,8)\n t=clean(t);t=re.sub")
source=source.replace('C.setFillColor(color);C.setFont(font,size)','C.setFillColor(color);C.setFont(font,max(size,9.6))')
a=source.index('def page(');b=source.index('def titleblock(',a)
source=source[:a]+'''def page(title,section='CONFERENCE EDITION',folio=True):
 global N,LEGACY_N
 N+=1;LEGACY_N=digest_legacy.get(N,N);C.saveState();C.translate(9+(8.5 if N%2 else 5),9);C.scale(.625,.625)
 C.setFillColorCMYK(0,0,0,0);C.rect(-30,0,660,H,fill=1,stroke=0)
 if folio:
  text('HORIZONS ’77 / TENERIFE',44,H-37,7,'A')
  label=section.upper()
  while pdfmetrics.stringWidth(label,'A',9.6)>270:label=label[:-2]
  text(label,290,H-37,6.5,'A');rule(H-48)
  rule(49);text('HORIZONS / EDICIÓN DEL CONGRESO / 1977',44,34,6.8,'A')
  C.setFillColor(INK);C.setFont('G',11);C.drawRightString(568,33,str(N))
 C.bookmarkPage('p'+str(N));C.addOutlineEntry(title,'p'+str(N),0)
def finish():C.restoreState();C.showPage()
'''+source[b:]
a=source.index("page('Cover',folio=False)");b=source.index("page('Contents'",a)
source=source[:a]+'''page('Title page',folio=False)
text('HORIZONS ’77',44,840,48,'COND');rule(810)
p=para('Friendship and the art<br/>of seeing together',27,32,'GB');_,h=p.wrap(524,160);p.drawOn(C,44,735-h)
p=para('Papers, drawings, walks and conversations<br/>among friends new and old.',15,22,'GI');_,h=p.wrap(480,100);p.drawOn(C,44,610-h)
p=para('Tenerife / 1977<br/>International conference on possible futures<br/>Notes towards life in 2027 and beyond.',15,22,'G');_,h=p.wrap(480,130);p.drawOn(C,44,470-h)
text('ENGLISH / ESPAÑOL / FRANÇAIS / ITALIANO / DEUTSCH',44,230,9,'AB');text('EDICIÓN DEL CONGRESO / NÚMERO 1',44,175,10,'A');finish()
'''+source[b:]
# Use three readable note pages; the final interior page is not a redundant back cover.
a=source.index("# Choose a paragraph boundary by actual typeset fit");b=source.index("page('Back cover',folio=False)",a)
source=source[:a]+"""back=[t for t in back if not t.startswith(('The three November 2026 feature plates','The six November 2026 feature plates'))]
totals=[len(t) for t in back]
cuts=min(((i,j) for i in range(1,len(back)-1) for j in range(i+1,len(back))),key=lambda z:max(sum(totals[:z[0]]),sum(totals[z[0]:z[1]]),sum(totals[z[1]:])))
for pi,group in enumerate([back[:cuts[0]],back[cuts[0]:cuts[1]],back[cuts[1]:]]):
 page('Edition notes / '+str(pi+1),'COLOPHON / EDITION NOTES');top=titleblock('On this edition.' if pi==0 else 'Edition notes / '+str(pi+1),tag='EDITION NOTES / '+str(pi+1));prose(group,top,size=11.4);finish()
C.save()
assert N==48,N
"""
source=source.replace("MASTER=OUT/'Horizons-77-digest-interior.pdf';C=",(ROOT/'print/digest-layout.py').read_text()+"\nMASTER=OUT/'Horizons-77-digest-interior.pdf';C=")
source=source.replace("if N>=46 and font=='G'", "if LEGACY_N>=46 and font=='G'")
source=source.replace('assert N==45,N','assert N==len(sheets)+2,N')
source=source.replace('pageCompression=1)',"pageCompression=1,initialFontName='A')")
source=source.replace(" if k in ['article','continued','editorial']:"," if k=='letters-leaf':draw_letters_leaf()\n elif k=='drago-photo':draw_drago_photo()\n elif k=='panorama':draw_panorama(s)\n elif k=='designed':draw_feature(s)\n elif k=='clarke':draw_clarke()\n elif k in ['article','continued','editorial','assembly']:bottom=draw_contribution(s)\n elif k in ['article','continued','editorial']:")
source=source.replace("C.save()\nassert N==48,N", "page('A note on the drawings','EDITION NOTES / PRODUCTION');draw_production_note();finish()\npage('Endpaper',folio=False);finish()\nC.save()\nassert N==len(sheets)+7,N")
recompose = """
# The three features are each two facing spreads. Other articles retain their copy.
old_sheets=sheets;sheets=[];digest_legacy={};LEGACY_N=0
for old_index,s in enumerate(old_sheets,3):
 key=s['key']
 if key in ['goodall','maathai','sun']:s=dict(s,body=s['a']['body'][:5])
 if key in ['goodall-continued','maathai-continued','sun-continued']:s=dict(s,body=s['a']['body'][5:])
 if key=='kitchen-desk':
  kitchen=(s,old_index);continue
 if key=='arrival/en':
  sheets.append(dict(s,body=s['body'][:4]));digest_legacy[len(sheets)+2]=old_index
  sheets.append(dict(s,key=key+'-continued',body=s['body'][4:],openingpart=1));digest_legacy[len(sheets)+2]=old_index
  continue
 if key=='arrival/it':
  sheets.append(kitchen[0]);digest_legacy[len(sheets)+2]=kitchen[1]
 if key=='arrival/de':
  sheets.append(dict(key='clarke',title=D['clarkeLeaf']['title'],kind='clarke'));digest_legacy[len(sheets)+2]=9
  sheets.append(dict(s,key=key+'-photo',kind='drago-photo'));digest_legacy[len(sheets)+2]=old_index
 if key=='arrival/fr':
  for side in range(2):
   sheets.append(dict(key=key if side==0 else key+'-plate',title=s['title'],kind='panorama',family='fr',side=side));digest_legacy[len(sheets)+2]=old_index
  s=dict(s,key=key+'-text',body=s['body'][2:])
 if key=='gilliam':
  for side in range(2):
   sheets.append(dict(key=key+'-plate-'+str(side),title=s['title'],kind='panorama',family='film',side=side));digest_legacy[len(sheets)+2]=old_index
 if key in ['below-continued','slope-continued','air-continued']:continue
 if key in ['below','slope','air']:
  for part in range(4):
   k=key if part==0 else key+'-continued' if part==3 else key+'-'+str(part)
   sheets.append(dict(key=k,title=s['title'],kind='designed',a=s['a'],part=part));digest_legacy[len(sheets)+2]=old_index
 else:
  sheets.append(s);digest_legacy[len(sheets)+2]=old_index
sheets.append(dict(key='afterword-letters',title='Write before it is finished',kind='letters-leaf'));digest_legacy[len(sheets)+2]=45
first={s['key']:i for i,s in enumerate(sheets,3)}
first['gilliam']=first['gilliam-plate-0'];first['arrival/de']=first['arrival/de-photo']
first['certificate']=first['pass'];first['colophon']=len(sheets)+3
for i in range(3):digest_legacy[first['colophon']+i]=46+i
contents.append(('clarke','Arthur C. Clarke / Between sessions'))
"""
source=source.replace("MASTER=OUT/'Horizons-77-digest-interior.pdf';C=",recompose+(ROOT/'print/digest-features.py').read_text()+'\n'+(ROOT/'print/digest-contributors.py').read_text()+"\nMASTER=OUT/'Horizons-77-digest-interior.pdf';C=")
source=source.replace("title if continued else title.upper(),size,size*1.06,'BD'","title,size,size*1.06,'GB'")
source=source.replace("if i in [1,2]:pattern_leaf(bottom,i)","# Repeated generic path studies retired.")
ns={'__file__':str(ROOT/'print/build.py')};exec(compile(source,str(ROOT/'print/build-digest.py'),'exec'),ns)
from pypdf import PdfReader,PdfWriter,Transformation
from pypdf.generic import RectangleObject
OUT=ROOT/'output/pdf';interior=OUT/'Horizons-77-digest-interior.pdf'
r=PdfReader(interior);page_count=len(r.pages);w=PdfWriter()
for page in r.pages:
 page.trimbox=RectangleObject([9,9,405,621]);page.bleedbox=RectangleObject([0,0,414,630]);w.add_page(page)
w.add_metadata({'/Title':'Horizons 77 / Mixam digest interior','/Subject':f'{page_count} interior pages; 5.5 x 8.5 trim; 0.125 bleed; 50lb uncoated; PUR'})
with interior.open('wb') as f:w.write(f)
# The old wrap is retained only to extract front and back for the reading proof.
# A revised PUR spine must come from the printer after the new page count is selected.
cover=OUT/'Horizons-77-digest-cover-48pp.pdf';spine=10.08
proof=PdfWriter();wrap=PdfReader(cover).pages[0]
pg=proof.add_blank_page(width=396,height=612);pg.merge_transformed_page(wrap,Transformation().translate(tx=-(9+396+spine),ty=-9))
proof.add_blank_page(width=396,height=612)
for p in PdfReader(interior).pages:
 pg=proof.add_blank_page(width=396,height=612);pg.merge_transformed_page(p,Transformation().translate(tx=-9,ty=-9))
proof.add_blank_page(width=396,height=612);pg=proof.add_blank_page(width=396,height=612);pg.merge_transformed_page(wrap,Transformation().translate(tx=-9,ty=-9))
proof.add_metadata({'/Title':'Horizons 77 / Digest reading proof','/Subject':f'{page_count+4} reader pages including two blank inside covers; not for production upload'})
with (OUT/'Horizons-77-digest-proof.pdf').open('wb') as f:proof.write(f)
(OUT/'digest-pagination.json').write_text(json.dumps({'interiorPages':page_count,'trimInches':[5.5,8.5],'bleedInches':.125,'spineInches':None,'coverStatus':'New printer template required; old 48-page wrap is not suitable','firstPages':ns['first'],'virtualBodySizes':ns['fitlog'],'scale':.625,'readingInserts':ns['insertlog'],'designedFeatures':ns['feature_checks']},indent=2))
print(f'Digest: {page_count} interior pages, {page_count+4}-page reading proof. New printer spine required.')

reader=PdfWriter();r=PdfReader(interior)
pairs=[(None,1)]+[(i,i+1 if i+1<=page_count else None) for i in range(2,page_count+1,2)]
for pair in pairs:
 pg=reader.add_blank_page(width=792,height=612)
 for x,pn in zip([0,396],pair):
  if pn:pg.merge_transformed_page(r.pages[pn-1],Transformation().translate(tx=x-9,ty=-9))
reader.add_metadata({'/Title':'Horizons 77 / Designed digest spreads','/Subject':'Facing pages for review; not printer imposition'})
with (OUT/'Horizons-77-digest-spreads.pdf').open('wb') as f:reader.write(f)
