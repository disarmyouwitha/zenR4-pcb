"""New Draft C schematics, preserving our matrix/QSPI and adding right nice!view."""
import sys,json,shutil
from pathlib import Path
from draft_c_common import *
sys.path.insert(0,str(ROOT.parent/'corneish-zen-replacement/analysis-tools/python'))
from kiutils.schematic import Schematic
links={}
for side in ['left','right']:
 name=f'draft-corne-{side}';sch=Schematic.from_file(str(ROOT/f'r4-layout/zen-r4-{side}.kicad_sch'))
 refs={}
 for s in sch.schematicSymbols:
  ps={p.key:p for p in s.properties};ref=ps['Reference'].value
  for i in s.instances:i.name=name
  if not s.onBoard:continue
  refs[ref]=s.uuid
  fp=ps['Footprint'].value
  if ref=='U1':fp='DraftC:Nano_Front_Down';ps['Value'].value='nice!nano v2 FRONT / components down'
  elif ref=='J1':fp='DraftC:Battery_Wire_SMD';ps['Value'].value='BAT+ / GND wire solder pads'
  elif ref=='SW22':fp='DraftC:Power_MSK12C02';ps['Value'].value='MSK12C02 candidate: 2 common / 3 ON'
  elif ref=='SW23':fp='DraftC:Reset_TL3342'
  elif ref.startswith('SW'):fp='DraftC:ChocSocket_Bottom'
  elif ref.startswith('D'):fp='DraftC:Diode_SOD123_Bottom'
  elif ref=='U2':fp='DraftC:SOIC-8_5.3x5.3mm_P1.27mm__NoSilk'
  elif ref=='C1':fp='DraftC:C_0603_1608Metric__NoSilk'
  elif ref=='R1':fp='DraftC:R_0603_1608Metric__NoSilk'
  ps['Footprint'].value=fp
 if side=='right':
  # Free edge pins become actual display signals; all matrix assignments remain unchanged.
  points=[(317.5,71.12),(317.5,73.66),(317.5,76.2),(363.22,68.58)]
  sch.noConnects=[n for n in sch.noConnects if not any(abs(n.position.X-x)<.001 and abs(n.position.Y-y)<.001 for x,y in points)]
 sch.titleBlock.title='Draft Corne '+side;sch.titleBlock.revision='C placement draft'
 for t in sch.texts:
  t.text=t.text.replace('Zen R4','Draft Corne').replace('carrier layout / DRAFT A','new Choc layout / DRAFT C')
  if 'Right display placement pending' in t.text:t.text='Right nice!view: CS D4 active high; MOSI D2; SCK D3. J2 included.'
  if 'Backside edge-contact' in t.text:t.text='Front-mounted nice!nano, components down. Battery wire pads, no JST.'
  if 'V2 PCB measured' in t.text:t.text='1.6 mm nominal draft; own plate/base. Not a Zen case replacement.'
  if 'Draft flash decoupling' in t.text:t.text='Left flash at former JST region; verify parts, antenna and assembly clearances.'
 path=OUT/f'{name}.kicad_sch';sch.to_file(str(path));text=path.read_text()
 if side=='right':
  sym='''(symbol "R4Review:View5" (pin_names (offset 0.7)) (in_bom yes) (on_board yes)
   (property "Reference" "J" (at 0 10 0) (effects (font (size 1 1))))
   (property "Value" "View5" (at 0 8 0) (effects (font (size 1 1))))
   (symbol "View5_0_1" (rectangle (start -2.54 7.62) (end 5.08 -7.62) (stroke (width 0.254) (type default)) (fill (type background))))
   (symbol "View5_1_1"'''
  nets=['VIEW_MOSI','VIEW_SCK','3V3_SW','GND','VIEW_CS_ACTIVE_HIGH']
  for i,n in enumerate(nets,1):sym+=f'(pin passive line (at -5.08 {7.62-2.54*i:.2f} 0) (length 2.54) (name {q(n)} (effects (font (size 1 1)))) (number "{i}" (effects (font (size 1 1)))))'
  sym+='))'
  lib=next((a,b,n) for a,b,n in nodes(text) if head(n)=='lib_symbols');text=text[:lib[1]-1]+'\n'+sym+text[lib[1]-1:]
  ident=uid();refs['J2']=ident
  more=f'(symbol (lib_id "R4Review:View5") (at 340.36 198.12 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid "{ident}")'+prop('Reference','J2',340.36,187.96)+prop('Value','nice!view front header',340.36,190.5)+prop('Footprint','DraftC:NiceView_Front_Header',340.36,198.12)+f'(instances (project "{name}" (path "/{sch.uuid}" (reference "J2") (unit 1)))))'
  def term(x,y,net,dx):
   return f'(wire (pts (xy {x} {y}) (xy {x+dx} {y})) (stroke (width 0) (type default)) (uuid "{uid()}"))(label {q(net)} (at {x+dx} {y} {0 if dx<0 else 180}) (effects (font (size 1 1)) (justify left bottom)) (uuid "{uid()}"))'
  for i,n in enumerate(nets):more+=term(335.28,193.04+2.54*i,n,-12.7)
  for x,y,n,dx in [(317.5,71.12,nets[0],-10.16),(317.5,73.66,nets[1],-10.16),(317.5,76.2,nets[4],-10.16),(363.22,68.58,'3V3_SW',10.16)]:more+=term(x,y,n,dx)
  end=text.rfind(')');text=text[:end]+more+text[end:];path.write_text(text)
 links[side]={'root':sch.uuid,'symbols':refs,'name':name}
# The local embedded symbol is authoritative. Preserve baseline library plus display connector.
symtext=(ROOT/'r4-layout/r4-review.kicad_sym').read_text()
# Add connector to the external library with the local entry name.
symtext=symtext[:symtext.rfind(')')]+sym.replace('R4Review:View5','View5',1)+')\n'
(OUT/'draft-c.kicad_sym').write_text(symtext)
(OUT/'sym-lib-table').write_text('(sym_lib_table (version 7) (lib (name "R4Review") (type "KiCad") (uri "${KIPRJMOD}/draft-c.kicad_sym") (options "") (descr "Draft Corne symbols")))\n')
(OUT/'schematic-links.json').write_text(json.dumps(links,indent=2)+'\n')
print('Draft C schematics: our matrix, left QSPI, battery pads, actual right display interface.')
