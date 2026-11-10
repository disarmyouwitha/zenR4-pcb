"""Place Draft Corne with nominal production footprints and our schematic netlist; initially unrouted."""
import math,csv,json,re,shutil,xml.etree.ElementTree as ET
from draft_c_common import *
LIB=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints');FP=OUT/'footprints/DraftC.pretty';links=json.loads((OUT/'schematic-links.json').read_text())
def parts(text):return [(head(n),n) for _,_,n in nodes(text)]
def load_embedded(ref):
 return next(n for k,n in parts((ROOT/'r4-layout/zen-r4-left.kicad_pcb').read_text()) if k=='footprint' and f'(property "Reference" "{ref}"' in n)
def lib_clean(text,name):
 # Normalize an embedded footprint to a standalone library footprint at angle zero.
 at=next((n for k,n in parts(text) if k=='at'),None);baseangle=float(at.rstrip(')').split()[-1]) if at and len(at.split())>3 else 0.
 edits=[]
 for a,b,n in nodes(text):
  k=head(n)
  if k in ['version','generator','generator_version','at','uuid','tstamp','path']:edits.append((a,b,''))
  elif k=='pad':
   n=re.sub(r'\(net\s+\d+\s+"[^"]*"\)','',n)
   def angle(m):return f'(at {m[1]} {m[2]} {float(m[3] or 0)-baseangle:.6f})'
   n=re.sub(r'\(at ([\d.e+-]+) ([\d.e+-]+)(?: ([\d.e+-]+))?\)',angle,n,count=1);edits.append((a,b,n))
  elif k=='property' and ('"Reference"' in n or '"Value"' in n):
   if '(hide yes)' not in n:n=n[:-1]+' (hide yes))'
   edits.append((a,b,n))
  elif k.startswith('fp_') and ('"F.SilkS"' in n or '"B.SilkS"' in n):edits.append((a,b,''))
 text=replace_top(text,edits);text=re.sub(r'^\(footprint "[^"]+"',f'(footprint "{name}"',text)
 # Each reference has its own symbol value; library values are not circuit values.
 text=re.sub(r'\(property "Reference" "[^"]*"','(property "Reference" "REF**"',text)
 return text.strip()

def pad(num,x,y,w,h,layer='F',drill=None,kind=None):
 if drill:
  return f'(pad "{num}" {kind or "thru_hole"} circle (at {x} {y}) (size {w} {h}) (drill {drill}) (layers "*.Cu" "*.Mask"))'
 return f'(pad "{num}" smd rect (at {x} {y}) (size {w} {h}) (layers "{layer}.Cu" "{layer}.Paste" "{layer}.Mask"))'
def fline(a,b,layer,w=.1):return f'(fp_line (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (stroke (width {w}) (type default)) (layer "{layer}"))'
def rect(x1,y1,x2,y2,layer):
 p=[(x1,y1),(x2,y1),(x2,y2),(x1,y2),(x1,y1)];return ''.join(fline(a,b,layer) for a,b in zip(p[:-1],p[1:]))
def custom(name,items,layer='F',attr='smd'):
 return f'(footprint "{name}" (version 20260206) (generator "pcbnew") (layer "{layer}.Cu") (property "Reference" "REF**" (at 0 -3) (layer "{layer}.SilkS") (hide yes) (effects (font (size .8 .8) (thickness .12))))(property "Value" "{name}" (at 0 3) (layer "{layer}.Fab") (hide yes) (effects (font (size .8 .8) (thickness .12))))(attr {attr}){items})'
libs={}
libs['ChocSocket_Bottom']=lib_clean(load_embedded('SW1'),'ChocSocket_Bottom')
libs['Diode_SOD123_Bottom']=lib_clean(load_embedded('D1'),'Diode_SOD123_Bottom')
for name in ['SOIC-8_5.3x5.3mm_P1.27mm__NoSilk','C_0603_1608Metric__NoSilk','R_0603_1608Metric__NoSilk']:
 libs[name]=lib_clean((ROOT/'r4-layout/footprints/ZenR4.pretty'/f'{name}.kicad_mod').read_text(),name)
for name,src in [('Power_MSK12C02','SW_SPDT_Shouhan_MSK12C02'),('Reset_TL3342','SW_SPST_TL3342')]:libs[name]=lib_clean((LIB/'Button_Switch_SMD.pretty'/f'{src}.kicad_mod').read_text(),name)
items=''
for bank in range(2):
 for i in range(12):items+=pad(bank*12+i+1,(1 if bank==0 else -1)*7.62,-13.97+2.54*i,1.65,1.65,drill=1.)
items+=rect(-9,-18.37,9,15.83,'F.Fab')+rect(-9.25,-18.62,9.25,16.08,'F.CrtYd')+rect(-4.5,-19.67,4.5,-11,'F.Fab')
libs['Nano_Front_Down']=custom('Nano_Front_Down',items,attr='through_hole')
items=pad(1,-1.8,0,2,2.5,layer='B')+pad(2,1.8,0,2,2.5,layer='B')+rect(-3.05,-1.5,3.05,1.5,'B.CrtYd')
items+='(fp_text user "BAT+" (at -1.8 2.4) (layer "B.SilkS") (effects (font (size .8 .8) (thickness .12)) (justify mirror)))(fp_text user "GND" (at 1.8 2.4) (layer "B.SilkS") (effects (font (size .8 .8) (thickness .12)) (justify mirror)))'
libs['Battery_Wire_SMD']=custom('Battery_Wire_SMD',items,layer='B')
items=''.join(pad(i+1,-5.08+2.54*i,0,1.7,1.7,drill=1) for i in range(5))+rect(-6.18,-1.1,6.18,1.1,'F.CrtYd')+rect(-7,-34.4,7,1.6,'F.Fab')
libs['NiceView_Front_Header']=custom('NiceView_Front_Header',items,attr='through_hole')
for name,diam in [('Mount_4p3',4.3),('Mount_2p2',2.2)]:libs[name]=custom(name,pad('',0,0,diam,diam,drill=diam,kind='np_thru_hole'),attr='board_only exclude_from_bom exclude_from_pos_files')
for name,text in libs.items():
 saved=text
 if '(layer "B.Cu")' in saved:
  def refl(m):return f'({m[1]} {m[2]} {-float(m[3]):.6f}'+(f' {-float(m[4]):.6f}' if m[4] else '')+')'
  saved=re.sub(r'\((at|start|end|mid|center|xy) ([\d.e+-]+) ([\d.e+-]+)(?: ([\d.e+-]+))?\)',refl,saved)
  for layer in ['Cu','Paste','Mask','SilkS','Fab','CrtYd']:saved=saved.replace('"B.'+layer+'"','"F.'+layer+'"')
  saved=saved.replace('(justify mirror)','')
 (FP/f'{name}.kicad_mod').write_text(saved+'\n')
(OUT/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "DraftC") (type "KiCad") (uri "${KIPRJMOD}/footprints/DraftC.pretty") (options "") (descr "Draft Corne local footprints")))\n')

rows=list(csv.DictReader((ROOT/'projects/choc-corne-flash/reference/component-placement.csv').open()));metadata={}
baseparts=parts((ROOT/'r4-layout/zen-r4-left.kicad_pcb').read_text());preamble='\n'.join(n for k,n in baseparts if k in ['version','generator','generator_version','general','paper','layers','setup'])
for side in ['left','right']:
 xml=ET.parse(OUT/f'checks/{side}.net.xml');comps={c.attrib['ref']:c for c in xml.findall('.//components/comp')};assigned={(n.attrib['ref'],n.attrib['pin']):net.attrib['name'] for net in xml.findall('.//nets/net') for n in net.findall('node')};names=sorted(set(assigned.values()));netcodes={n:i+1 for i,n in enumerate(names)};fps=[];pads=[];placed=[]
 def add(ref,lib,where,angle=0,value=None):
  c=comps.get(ref);value=value or (c.findtext('value') if c is not None else lib);fp=libs[lib].strip();edits=[]
  for a,b,n in nodes(fp):
   k=head(n)
   if k in ['version','generator','generator_version']:edits.append((a,b,''))
   elif k=='property':
    if '(property "Reference"' in n:n=re.sub(r'^\(property "Reference" "[^"]*"',f'(property "Reference" "{ref}"',n)
    elif '(property "Value"' in n:n=re.sub(r'^\(property "Value" "[^"]*"',f'(property "Value" {q(value)}',n)
    edits.append((a,b,n))
   elif k=='pad':
    n=re.sub(r'\(uuid "[^"]*"\)','',n)
    num=re.match(r'\(pad "([^"]*)"',n)[1];m=re.search(r'\(at ([\d.e+-]+) ([\d.e+-]+)(?: ([\d.e+-]+))?\)',n);lx,ly,pa=float(m[1]),float(m[2]),float(m[3] or 0)
    n=n[:m.start()]+f'(at {lx} {ly} {pa+angle:.6f})'+n[m.end():];net=assigned.get((ref,num))
    if net:n=n[:-1]+f' (net {netcodes[net]} {q(net)}) (uuid "{uid()}"))'
    else:n=n[:-1]+f' (uuid "{uid()}"))'
    edits.append((a,b,n));ang=math.radians(angle);size=list(map(float,re.search(r'\(size ([\d.e+-]+) ([\d.e+-]+)\)',n).groups()));hole=re.search(r'\(drill ([\d.e+-]+)\)',n)
    pads.append({'ref':ref,'pad':num,'net':net or'','xy':[where[0]+math.cos(ang)*lx+math.sin(ang)*ly,where[1]-math.sin(ang)*lx+math.cos(ang)*ly],'size':size,'angle':pa+angle,'drill':float(hole[1]) if hole else 0,'layer':'B' if '"B.Cu"' in n else 'F'})
  fp=replace_top(fp,edits);fp=re.sub(r'^\(footprint "[^"]*"',f'(footprint "DraftC:{lib}" (at {where[0]} {where[1]} {angle}) (uuid "{uid()}")',fp)
  if ref in links[side]['symbols']:fp=fp[:-1]+f'(path "/{links[side]["root"]}/{links[side]["symbols"][ref]}")'+')'
  fp=re.sub(r'\(uuid "[^"]*"\)',lambda m:f'(uuid "{uid()}")',fp)
  fps.append(fp);placed.append({'ref':ref,'library':lib,'xy':where,'angle':angle,'layer':'B' if lib in ['ChocSocket_Bottom','Diode_SOD123_Bottom','Battery_Wire_SMD'] else'F','value':value})
 # Switch and diode placements follow the Typeractive reference, with our existing reference/net convention.
 for row in [r for r in rows if r['side']==side and re.fullmatch(r'SW\d+',r['reference'])]:
  i=int(row['reference'][2:]);rr=(i-1)//6 if i<=18 else 3;cc=(i-1)%6 if i<=18 else i-16
  j=i if side=='left' else(rr*6+6-cc if rr<3 else 24-cc)
  p=[round(float(row['x_mm']),4),round(float(row['y_mm']),4)];angle=round(float(row['angle_deg'])/15)*15
  if side=='left' and i==6:angle+=180
  add('SW'+str(j),'ChocSocket_Bottom',p,angle)
  d=next(r for r in rows if r['side']==side and r['reference']=='D'+str(i));dxy=[round(float(d['x_mm']),4),round(float(d['y_mm']),4)]
  if side=='left' and i==6:dxy[1]=41.6
  add('D'+str(j),'Diode_SOD123_Bottom',dxy,round(float(d['angle_deg'])/15)*15)
 nano=next(r for r in rows if r['side']==side and r['reference']=='U1');cx,cy=round(float(nano['x_mm']),4),round(float(nano['y_mm']),4);add('U1','Nano_Front_Down',[cx,cy])
 add('J1','Battery_Wire_SMD',[cx,79.5]);add('SW22','Power_MSK12C02',[151.0 if side=='left' else 27.2,76],90 if side=='left' else -90);add('SW23','Reset_TL3342',[cx,79.5],0)
 if side=='left':
  add('U2','SOIC-8_5.3x5.3mm_P1.27mm__NoSilk',[cx,71]);add('C1','C_0603_1608Metric__NoSilk',[cx+3,66.9]);add('R1','R_0603_1608Metric__NoSilk',[cx,75.5])
 else:
  view=next(r for r in rows if r['side']==side and r['reference']=='J_VIEW');add('J2','NiceView_Front_Header',[round(float(view['x_mm']),4),round(float(view['y_mm'])+1.8,4)])
 reftext=(ROOT/f'projects/choc-corne-flash/reference/typeractive-model-{side}.kicad_pcb').read_text();outline=[];mountcount=0
 for k,n in parts(reftext):
  if k=='gr_line' and '(layer "Edge.Cuts")' in n:
   a=list(map(float,re.search(r'\(start ([\d.e+-]+) ([\d.e+-]+)\)',n).groups()));b=list(map(float,re.search(r'\(end ([\d.e+-]+) ([\d.e+-]+)\)',n).groups()));outline.append(a)
  if k=='footprint' and 'MODEL_HOLE' in n:
   dr=float(re.search(r'\(drill ([\d.e+-]+)\)',n)[1])
   if dr>2:
    pp=list(map(float,re.search(r'\(at ([\d.e+-]+) ([\d.e+-]+)',n).groups()));mountcount+=1;add('H'+str(mountcount),'Mount_4p3' if dr>3 else'Mount_2p2',pp)
 outline.append(outline[0]);edge='\n'.join(f'(gr_line (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (stroke (width .05) (type default)) (layer "Edge.Cuts") (uuid "{uid()}"))' for a,b in zip(outline[:-1],outline[1:]))
 keep=[(cx-6.5,cy+10),(cx+6.5,cy+10),(cx+6.5,cy+18.5),(cx-6.5,cy+18.5)]
 zone=f'(zone (net 0) (net_name "") (layers "F.Cu" "B.Cu") (uuid "{uid()}") (hatch edge .5) (keepout (tracks not_allowed) (vias not_allowed) (pads allowed) (copperpour not_allowed) (footprints allowed)) (polygon (pts '+''.join(f'(xy {x} {y})' for x,y in keep)+')))'
 title=f'(gr_text "DRAFT CORNE C {side.upper()} - INITIAL PLACEMENT / UNROUTED\\nFront nano, components down / battery wire pads" (at 90 17) (layer "Dwgs.User") (effects (font (size 1 1) (thickness .15))))'
 board='(kicad_pcb\n'+preamble+'\n'+'\n'.join(f'(net {i} {q(n)})' for n,i in netcodes.items())+'\n'+'\n'.join(fps)+'\n'+edge+'\n'+zone+'\n'+title+'\n)\n';(OUT/f'draft-corne-{side}.kicad_pcb').write_text(board)
 pro=json.loads((ROOT/f'r4-layout/zen-r4-{side}.kicad_pro').read_text());pro['meta']['filename']=f'draft-corne-{side}.kicad_pro';pro['schematic']={};(OUT/f'draft-corne-{side}.kicad_pro').write_text(json.dumps(pro,indent=2)+'\n')
 metadata[side]={'outline':outline,'footprints':placed,'pads':pads,'nano_keepout':keep,'routing_status':'unrouted initial placement'}
(OUT/'placement.json').write_text(json.dumps(metadata,indent=2)+'\n');print({s:len(v['footprints']) for s,v in metadata.items()})
