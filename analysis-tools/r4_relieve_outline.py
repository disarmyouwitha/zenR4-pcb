"""Locally extend draft PCB contour only where native DRC finds socket-land edge conflicts."""
import sys,json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis-tools/python'))
from shapely.geometry import Polygon,Point
OUT=BASE/'r4-layout';g=json.loads((OUT/'geometry.json').read_text())
for side in ['left','right']:
 d=g[side];raw=d.get('original_outline',d['outline']);d['original_outline']=raw
 ox=min(p[0] for p in raw);oy=max(p[1] for p in raw)
 poly=Polygon(raw);drc=json.loads((OUT/f'checks/{side}-placement-drc.json').read_text())
 changes=[]
 pads=json.loads((OUT/f'{side}-pads.json').read_text())
 for v in drc['violations']:
  if v['type']!='copper_edge_clearance':continue
  item=next(i for i in v['items'] if i['description'].startswith('Pad'))
  x,y=item['pos']['x'],item['pos']['y'];cx,cy=x+ox-25,oy-(y-25)
  land=min(pads,key=lambda p:(p['xy'][0]-x)**2+(p['xy'][1]-y)**2)
  radius=(land['size'][0]**2+land['size'][1]**2)**.5/2+.35
  bump=Point(cx,cy).buffer(radius,quad_segs=12)
  if poly.intersects(bump):
   poly=poly.union(bump);changes.append({'cad_xy':[cx,cy],'clearance_envelope_radius':radius,'ref':land['reference']})
 assert poly.geom_type=='Polygon' and poly.is_valid
 d['outline']=list(map(list,poly.exterior.coords))
 d['local_outline_extensions']=changes
(OUT/'geometry.json').write_text(json.dumps(g,indent=2))
print({s:d['local_outline_extensions'] for s,d in g.items()})
