"""Fork Draft A with new outer Edge.Cuts only; leave every electrical item intact."""
from pathlib import Path
import json,re,uuid,shutil,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'r4-layout';OUT=ROOT/'projects/nano-independent/draft-b'
G=json.loads((OUT/'geometry.json').read_text())
def nodes(text):
 depth=0;quoted=False;escaped=False;start=None
 for i,c in enumerate(text):
  if quoted:
   if escaped:escaped=False
   elif c=='\\':escaped=True
   elif c=='"':quoted=False
   continue
  if c=='"':quoted=True;continue
  if c=='(':
   if depth==1:start=i
   depth+=1
  elif c==')':
   depth-=1
   if depth==1 and start is not None:yield start,i+1,text[start:i+1];start=None
 def_unused=None

def line(a,b):
 return f'(gr_line (start {a[0]:.6f} {a[1]:.6f}) (end {b[0]:.6f} {b[1]:.6f}) (stroke (width 0.05) (type default)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))'
results={}
for side in ['left','right']:
 d=G['sides'][side];ox=d['board_xy_transform']['ox'];oy=d['board_xy_transform']['oy']
 def xy(v):return [v[0]-ox+25,oy-v[1]+25]
 original=(BASE/f'zen-r4-{side}.kicad_pcb').read_text();cx=-14.3 if side=='left' else 23.8
 low=xy([cx-10.1,4]);high=xy([cx+10.1,-16.5]);cuts=[];keep=0
 electrical=[]
 for start,end,node in nodes(original):
  head=re.match(r'\(\s*([^\s()]+)',node)[1]
  if head=='gr_line' and '(layer "Edge.Cuts")' in node:
   a=list(map(float,re.search(r'\(start ([\d.+-]+) ([\d.+-]+)\)',node).groups()));b=list(map(float,re.search(r'\(end ([\d.+-]+) ([\d.+-]+)\)',node).groups()))
   battery=all(low[0]-1e-5<=v[0]<=high[0]+1e-5 and low[1]-1e-5<=v[1]<=high[1]+1e-5 for v in [a,b])
   if battery:keep+=1
   else:cuts.append((start,end))
  elif head in ['footprint','segment','arc','via','zone','net']:electrical.append(node)
 assert keep==4,(side,keep)
 text=original
 for start,end in reversed(cuts):text=text[:start]+text[end:]
 poly=[xy(v) for v in d['outline_CAD_mm']]
 added='\n'+'\n'.join(line(a,b) for a,b in zip(poly[:-1],poly[1:]))+'\n'
 text=text.replace('DRAFT A / 1.6mm','DRAFT B / 1.6mm')
 last=text.rfind(')');text=text[:last]+added+text[last:]
 after=[n for _,_,n in nodes(text) if re.match(r'\(\s*([^\s()]+)',n)[1] in ['footprint','segment','arc','via','zone','net']]
 assert electrical==after,'Electrical payload changed'
 (OUT/f'zen-r4-{side}.kicad_pcb').write_text(text)
 for suffix in ['kicad_sch','kicad_pro']:shutil.copy2(BASE/f'zen-r4-{side}.{suffix}',OUT/f'zen-r4-{side}.{suffix}')
 results[side]={'outer_segments_removed':len(cuts),'outer_segments_added':len(poly)-1,'battery_edges_preserved':keep,'electrical_items_exactly_unchanged':len(electrical),'baseline_electrical_payload_sha256':hashlib.sha256('\n'.join(electrical).encode()).hexdigest(),'new_electrical_payload_sha256':hashlib.sha256('\n'.join(after).encode()).hexdigest()}
for name in ['r4-review.kicad_sym','sym-lib-table']:shutil.copy2(BASE/name,OUT/name)
(OUT/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "ZenR4") (type "KiCad") (uri "${KIPRJMOD}/../../../r4-layout/footprints/ZenR4.pretty") (options "") (descr "Shared checked library")))\n')
(OUT/'checks/electrical-payload-audit.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
