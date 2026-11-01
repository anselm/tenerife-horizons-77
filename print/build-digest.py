"""Mixam digest: reflowed text, mirrored glue margins, separate outside cover."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'print/build.py').read_text().split('r=PdfReader(MASTER);writer=PdfWriter();order=[]')[0]
source=source.replace('W,H=612,792;','W,H=612,979.2;').replace("MASTER=OUT/'Horizons-77-print-letter.pdf'","MASTER=OUT/'Horizons-77-digest-interior.pdf'").replace('pagesize=(W,H)','pagesize=(414,630)').replace(' y=718\n',' y=905.2\n').replace('size=sz,cols=3','size=sz,cols=2').replace('if cols==3:','if leading is not None:')
# Give the self-contained coastal afternoon a larger plate on the taller digest page.
source=source.replace("165 if a['art'] in ['coast','observatory'] else 150", "310 if a['art']=='coast' else 165 if a['art']=='observatory' else 150")
source=source.replace(" t=clean(t);t=re.sub"," size=size*1.12 if font in ['G','GI','GB'] else max(size,9.6)\n if leading is not None:leading=max(leading*1.10,size*1.22)\n space=min(space,8)\n t=clean(t);t=re.sub")
source=source.replace('C.setFillColor(color);C.setFont(font,size)','C.setFillColor(color);C.setFont(font,max(size,9.6))')
a=source.index('def page(');b=source.index('def titleblock(',a)
source=source[:a]+'''def page(title,section='CONFERENCE EDITION',folio=True):
 global N
 N+=1;C.saveState();C.translate(9+(8.5 if N%2 else 5),9);C.scale(.625,.625)
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
text('HORIZONS ’77',44,840,48,'BD');rule(810)
p=para('Friendship and the art<br/>of seeing together',27,32,'BD');_,h=p.wrap(524,160);p.drawOn(C,44,735-h)
p=para('Papers, drawings, walks and conversations<br/>among friends new and old.',15,22,'GI');_,h=p.wrap(480,100);p.drawOn(C,44,610-h)
p=para('Tenerife / 1977<br/>International conference on possible futures<br/>Notes towards life in 2027 and beyond.',15,22,'G');_,h=p.wrap(480,130);p.drawOn(C,44,470-h)
text('ENGLISH / ESPAÑOL / FRANÇAIS / ITALIANO / DEUTSCH',44,230,9,'AB');text('EDICIÓN DEL CONGRESO / NÚMERO 1',44,175,10,'A');finish()
'''+source[b:]
# Use three readable note pages; the final interior page is not a redundant back cover.
a=source.index("cut=min(range(1,len(back))");b=source.index("page('Back cover',folio=False)",a)
source=source[:a]+"""totals=[len(t) for t in back]
cuts=min(((i,j) for i in range(1,len(back)-1) for j in range(i+1,len(back))),key=lambda z:max(sum(totals[:z[0]]),sum(totals[z[0]:z[1]]),sum(totals[z[1]:])))
for pi,group in enumerate([back[:cuts[0]],back[cuts[0]:cuts[1]],back[cuts[1]:]]):
 page('Edition notes / '+str(pi+1),'COLOPHON / EDITION NOTES');top=titleblock('On this edition.' if pi==0 else 'Edition notes / '+str(pi+1),tag='EDITION NOTES / '+str(pi+1));prose(group,top,size=11.4);finish()
C.save()
assert N==48,N
"""
ns={'__file__':str(ROOT/'print/build.py')};exec(compile(source,str(ROOT/'print/build-digest.py'),'exec'),ns)
from pypdf import PdfReader,PdfWriter,Transformation
from pypdf.generic import RectangleObject
OUT=ROOT/'output/pdf';interior=OUT/'Horizons-77-digest-interior.pdf'
r=PdfReader(interior);w=PdfWriter()
for page in r.pages:
 page.trimbox=RectangleObject([9,9,405,621]);page.bleedbox=RectangleObject([0,0,414,630]);w.add_page(page)
w.add_metadata({'/Title':'Horizons 77 / Mixam digest interior','/Subject':'48 interior pages; 5.5 x 8.5 trim; 0.125 bleed; 50lb uncoated; PUR'})
with interior.open('wb') as f:w.write(f)
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
INK=ns['INK'];RUST=ns['RUST'];TEAL=ns['TEAL']
cover=OUT/'Horizons-77-digest-cover.pdf';spine=10.08;cw=820.08;ch=630
c=canvas.Canvas(str(cover),pagesize=(cw,ch),pageCompression=1)
def line(t,x,y,size=10,font='A',color=INK):
 c.setFillColor(color);c.setFont(font,size);c.drawString(x,y,t)
def paragraph(t,x,y,width,size=12,font='G',leading=None,color=INK):
 p=Paragraph(t,ParagraphStyle('cover',fontName=font,fontSize=size,leading=leading or size*1.3,textColor=color));_,h=p.wrap(width,500);p.drawOn(c,x,y-h);return y-h
c.saveState();c.translate(9,9)
line('HORIZONS ’77',25,555,29,'BD');c.setStrokeColor(INK);c.line(25,540,371,540)
paragraph('There is still<br/>room at the table.',25,475,340,30,'BD',34,RUST)
line('LAS PREGUNTAS VIAJAN',25,290,10,'AB',TEAL)
paragraph('Correspondence, drawings and corrections for the next issue are welcome. Please include the name of the place, the scale of the drawing and the address to which a reply may be sent.',25,260,315,12,'G',17)
line('EL FUTURO ES UNA ISLA',25,108,10,'AB');line('LE FUTUR EST UNE ÎLE',25,88,10);line('TENERIFE / EDICIÓN DEL CONGRESO / 1977',25,40,7,'A');c.restoreState()
c.saveState();c.translate(9+396+spine,9)
line('REVISTA INTERNACIONAL DE FUTUROS POSIBLES',36,578,6.7,'AB');line('HORIZONS ’77',34,522,43,'BD');c.setStrokeColor(INK);c.setLineWidth(1);c.line(25,505,371,505)
line('TENERIFE / NÚMERO 1 / 1977',36,489,8,'AB');paragraph('THE INHABITED<br/>ISLAND.',36,455,335,29,'BD',30)
paragraph('Architecture, ocean, energy.<br/>Notes towards life in 2027 and beyond.',36,375,335,12.5,'G',16)
c.drawImage(ImageReader(str(ROOT/'assets/tenerife.png')),36,159,width=335,height=148,preserveAspectRatio=True,anchor='c',mask='auto')
line('ESTUDIO PARA UN PAISAJE HABITADO / 2027',36,144,6.5);c.line(25,124,371,124)
paragraph('Reports, drawings &amp; conversations<br/>assembled at the close of the meeting.',36,110,335,10,'G',13)
line('ENGLISH · ESPAÑOL · FRANÇAIS · ITALIANO · DEUTSCH',36,57,6.2);line('200 PESETAS',36,34,7,'AB');c.restoreState();c.showPage();c.save()
r=PdfReader(cover);page=r.pages[0];page.trimbox=RectangleObject([9,9,cw-9,ch-9]);page.bleedbox=RectangleObject([0,0,cw,ch]);w=PdfWriter();w.add_page(page)
w.add_metadata({'/Title':'Horizons 77 / Digest outside cover','/Subject':'11.39 x 8.75 with bleed; 0.14 inch spine; 80lb uncoated; inside covers blank'})
with cover.open('wb') as f:w.write(f)
proof=PdfWriter();wrap=PdfReader(cover).pages[0]
pg=proof.add_blank_page(width=396,height=612);pg.merge_transformed_page(wrap,Transformation().translate(tx=-(9+396+spine),ty=-9))
proof.add_blank_page(width=396,height=612)
for p in PdfReader(interior).pages:
 pg=proof.add_blank_page(width=396,height=612);pg.merge_transformed_page(p,Transformation().translate(tx=-9,ty=-9))
proof.add_blank_page(width=396,height=612);pg=proof.add_blank_page(width=396,height=612);pg.merge_transformed_page(wrap,Transformation().translate(tx=-9,ty=-9))
proof.add_metadata({'/Title':'Horizons 77 / Digest reading proof','/Subject':'52 reader pages including two blank inside covers; not for production upload'})
with (OUT/'Horizons-77-digest-proof.pdf').open('wb') as f:proof.write(f)
(OUT/'digest-pagination.json').write_text(json.dumps({'interiorPages':48,'trimInches':[5.5,8.5],'bleedInches':.125,'spineInches':.14,'outsideCoverWithBleedInches':[11.39,8.75],'firstPages':ns['first'],'virtualBodySizes':ns['fitlog'],'scale':.625},indent=2))
print('Digest: 48 interior pages, 0.14-inch outside cover wrap, 52-page reading proof.')
