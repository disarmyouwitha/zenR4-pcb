"""Derive layout-linked sheets from reviewed electrical sheets; preserve GPIOs."""
import sys,copy,json,shutil
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];OUT=BASE/'r4-layout';SRC=BASE/'zen-r4-review'
sys.path.insert(0,str(BASE/'analysis-tools/python'))
from kiutils.schematic import Schematic
from kiutils.symbol import SymbolLib
library=SymbolLib.from_file(str(SRC/'r4-review.kicad_sym'))
power=copy.deepcopy(next(s for s in library.symbols if s.entryName=='Switch'));power.libId='Power23'
for sub in power.units:
 sub.entryName='Power23'
 for p in sub.pins:p.number=str(int(p.number)+1)
library.symbols.append(power);library.to_file(str(OUT/'r4-review.kicad_sym'))
shutil.copyfile(SRC/'sym-lib-table',OUT/'sym-lib-table')
links={}
for side in ['left','right']:
 name='zen-r4-'+side;sch=Schematic.from_file(str(SRC/f'{name}-nano.kicad_sch'))
 embedded=copy.deepcopy(power);embedded.libId='R4Review:Power23';sch.libSymbols.append(embedded)
 links[side]={'root':sch.uuid,'symbols':{}}
 for s in sch.schematicSymbols:
  props={p.key:p for p in s.properties};ref=props['Reference'].value
  for instance in s.instances:instance.name=name
  if not s.onBoard:continue
  links[side]['symbols'][ref]=s.uuid
  fp=''
  if ref=='U1':fp='ZenR4:NiceNano_v2_edges'
  elif ref=='J1':fp='ZenR4:Battery_wire_pads'
  elif ref=='SW22':
   s.libId='R4Review:Power23';fp='Button_Switch_SMD:SW_SPDT_PCM12'
   props['Value'].value='PCM12: 2 common, 3 ON; 1 NC'
  elif ref=='SW23':fp='Button_Switch_SMD:SW_SPST_TL3342'
  elif ref.startswith('SW'):fp='ZenR4:Choc_PG1350_bottom'
  if fp:props['Footprint'].value=fp
  current=props['Footprint'].value
  if current and not current.startswith('ZenR4:'):props['Footprint'].value='ZenR4:'+current.split(':',1)[1]+'__NoSilk'
 sch.titleBlock.revision='DRAFT A layout review'
 for t in sch.texts:
  t.text=t.text.replace('electrical review / before layout','carrier layout / DRAFT A')
 sch.to_file(str(OUT/f'{name}.kicad_sch'))
(OUT/'schematic-links.json').write_text(json.dumps(links,indent=2))
