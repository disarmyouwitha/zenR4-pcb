"""Produce review previews and 1:1 physical fit templates from final board geometry."""
import sys,json,math,os
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];OUT=BASE/'r4-layout'
sys.path[:0]=[str(BASE/'analysis-tools/render-python'),str(BASE/'analysis-tools/mesh-python'),str(BASE/'analysis-tools/python')]
os.environ.setdefault('MPLCONFIGDIR','/tmp/zen-mpl-cache')
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPolygon,Circle,Rectangle
from shapely.geometry import Polygon,Point,box
import trimesh
geo=json.loads((OUT/'geometry.json').read_text());fig,axs=plt.subplots(1,2,figsize=(16,7),facecolor='#f4f5f7')
report={}
for ax,side in zip(axs,['left','right']):
 g=geo[side];data=json.loads((OUT/f'checks/{side}-routing-geometry.json').read_text());ox=min(v[0] for v in g['outline']);oy=max(v[1] for v in g['outline'])
 def xy(c):return [c[0]-ox+25,oy-c[1]+25]
 def cad(c):return [c[0]+ox-25,oy-c[1]+25]
 outer=np.array([xy(v) for v in g['outline']]);cx=-14.3 if side=='left' else 24.9
 bcx=cx if side=='left' else 23.8
 ax.add_patch(MPolygon(outer,fc='#174f46',ec='#153930',lw=1))
 cut=Polygon([xy(v) for v in [(bcx-10.1,-16.5),(bcx+10.1,-16.5),(bcx+10.1,4),(bcx-10.1,4)]])
 ax.add_patch(MPolygon(list(cut.exterior.coords),fc='#f4f5f7',ec='#153930',lw=1))
 for layer,col in [(1,'#70adf2'),(0,'#edb667')]:
  for t in data['tracks']:
   if t['via']:continue
   if t['layer']==layer:ax.plot([t['a'][0],t['b'][0]],[t['a'][1],t['b'][1]],color=col,lw=.65,alpha=.85)
 for t in data['tracks']:
  if t['via']:ax.add_patch(Circle(t['xy'],t['width']/2,fc='#cbd5df',ec='#222',lw=.25))
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="150mm" height="115mm" viewBox="15 15 150 115">','<rect x="15" y="15" width="150" height="115" fill="white"/>','<g fill="none" stroke="black" stroke-width=".15">']
 def path(poly):return 'M '+' L '.join(f'{x:.4f},{y:.4f}' for x,y in poly)+' Z'
 svg.append(f'<path d="{path(outer)} {path(cut.exterior.coords)}"/>')
 pcb=Polygon(g['outline']).difference(Polygon([cad(v) for v in cut.exterior.coords]))
 for pad in data['pads']:
  if pad['net']:
   x,y=pad['xy'];w,h=pad['size'];ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,fc='#e3bc65',ec='none',angle=-pad['angle'],rotation_point='center',zorder=3))
  if pad['drill']:
   ax.add_patch(Circle(pad['xy'],pad['drill']/2,fc='#f4f5f7',ec='#263a35',lw=.25,zorder=4));x,y=pad['xy'];svg.append(f'<circle cx="{x}" cy="{y}" r="{pad["drill"]/2}"/>')
   pcb=pcb.difference(Point(cad(pad['xy'])).buffer(pad['drill']/2,quad_segs=12))
 # Non-electrical physical outlines shown in final carrier top view.
 x,y=xy([cx-9,39.1]);ax.add_patch(Rectangle((x,y),18,34.2,fill=False,ec='#fff',lw=1,ls='--'))
 svg.append(f'<rect x="{x}" y="{y}" width="18" height="34.2" stroke="#276caf" stroke-dasharray="1 1"/>')
 for k in g['keys']:
  x,y=xy(k['xy']);svg.append(f'<rect x="{x-7.5}" y="{y-7.5}" width="15" height="15" transform="rotate({-k["angle"]} {x} {y})" stroke="#aaa"/>')
 svg+=['<path d="M30 119h25 M30 117v4 M55 117v4"/>','</g>',f'<text x="30" y="125" font-size="2.5" font-family="sans-serif">{side.upper()} DRAFT A — TOP VIEW — print 100%; bar = 25 mm</text>','</svg>']
 (OUT/f'mechanical/zen-r4-{side}-fit-1to1.svg').write_text('\n'.join(svg))
 assert pcb.is_valid and pcb.geom_type=='Polygon'
 mesh=trimesh.creation.extrude_polygon(pcb,height=1.6,engine='earcut');mesh.apply_translation([0,0,.05]);assert mesh.is_watertight and mesh.is_volume
 mesh.export(OUT/f'mechanical/zen-r4-{side}-bare-pcb-fit-PROTOTYPE.stl')
 ax.set_aspect('equal');ax.set_xlim(20,160);ax.set_ylim(116,21);ax.axis('off');ax.set_title(f'{side.upper()} · 21 Choc keys · nice!nano underneath',fontsize=14,color='#17222b',pad=12)
 report[side]={'pcb_fit_mesh_watertight':mesh.is_watertight,'pcb_fit_mesh_thickness_mm':1.6,'track_segments':sum(not t['via'] for t in data['tracks']),'vias':sum(t['via'] for t in data['tracks']),'min_track_width_mm':min(t['width'] for t in data['tracks'] if not t['via']), 'outline_change_area_mm2':Polygon(g['outline']).difference(Polygon(g['original_outline'])).area}
fig.text(.5,.05,'DRAFT A · amber: front copper · blue: back copper · dashed white: nano body · display omitted',ha='center',fontsize=12,color='#374650')
fig.tight_layout(rect=[0,.08,1,1]);fig.savefig(OUT/'layout-preview.png',dpi=160,facecolor=fig.get_facecolor());plt.close(fig)
(OUT/'checks/artifact-report.json').write_text(json.dumps(report,indent=2));print(report)
