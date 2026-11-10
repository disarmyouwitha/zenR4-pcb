"""Draft B review images and actual-size fit artifacts, derived from unchanged pad data."""
import os,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'projects/nano-independent/draft-b'
D=Path(os.environ.get('ZEN_ANALYSIS_DEPS',str(ROOT.parent/'corneish-zen-replacement/analysis-tools')))
sys.path[:0]=[str(D/'render-python'),str(D/'mesh-python'),str(D/'python')]
os.environ.setdefault('MPLCONFIGDIR','/tmp/zen-mpl-cache')
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch,Circle,Rectangle
from shapely.geometry import Polygon,Point
from shapely import affinity
import trimesh
G=json.loads((OUT/'geometry.json').read_text());OLD=json.loads((ROOT/'r4-layout/geometry.json').read_text());report={}
fig,axs=plt.subplots(1,2,figsize=(16,7.8),facecolor='#f4f6f8')
over,oa=plt.subplots(1,2,figsize=(13,6),facecolor='white')
for side,ax,oa1 in zip(['left','right'],axs,oa):
 d=G['sides'][side];ox=d['board_xy_transform']['ox'];oy=d['board_xy_transform']['oy'];data=json.loads((ROOT/f'r4-layout/checks/{side}-routing-geometry.json').read_text())
 def xy(p):return [p[0]-ox+25,oy-p[1]+25]
 def cad(p):return [p[0]+ox-25,oy-p[1]+25]
 outer=[xy(p) for p in d['outline_CAD_mm']];poly=Polygon(d['outline_CAD_mm']);cx=-14.3 if side=='left' else 24.9;bcx=cx if side=='left' else 23.8
 cut=Polygon([xy(p) for p in [(bcx-10.1,-16.5),(bcx+10.1,-16.5),(bcx+10.1,4),(bcx-10.1,4)]])
 ax.add_patch(Patch(outer,fc='#174f46',ec='#123e36',lw=1));ax.add_patch(Patch(list(cut.exterior.coords),fc='#f4f6f8',ec='#123e36',lw=1))
 for t in data['tracks']:
  if t['via']:ax.add_patch(Circle(t['xy'],t['width']/2,fc='#c4d3dc',ec='none'))
  else:ax.plot([t['a'][0],t['b'][0]],[t['a'][1],t['b'][1]],color='#edb667' if t['layer']==0 else '#70adf2',lw=.6,alpha=.9)
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="150mm" height="115mm" viewBox="15 15 150 115">','<rect x="15" y="15" width="150" height="115" fill="white"/>','<g fill="none" stroke="black" stroke-width=".15">']
 def path(p):return 'M '+' L '.join(f'{x:.4f},{y:.4f}' for x,y in p)+' Z'
 svg.append(f'<path d="{path(outer)} {path(cut.exterior.coords)}"/>');pcb=poly.difference(Polygon([cad(p) for p in cut.exterior.coords]))
 for p in data['pads']:
  x,y=p['xy'];w,h=p['size']
  if p['net']:ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,angle=-p['angle'],rotation_point='center',fc='#e3bc65',ec='none',zorder=3))
  if p['drill']:
   ax.add_patch(Circle(p['xy'],p['drill']/2,fc='#f4f6f8',ec='none',zorder=4));svg.append(f'<circle cx="{x}" cy="{y}" r="{p["drill"]/2}"/>');pcb=pcb.difference(Point(cad(p['xy'])).buffer(p['drill']/2,quad_segs=12))
 x,y=xy([cx-9,39.1]);ax.add_patch(Rectangle((x,y),18,34.2,fill=False,ec='white',lw=1,ls='--'));svg.append(f'<rect x="{x}" y="{y}" width="18" height="34.2" stroke="#276caf" stroke-dasharray="1 1"/>')
 for k in OLD[side]['keys']:
  x,y=xy(k['xy']);svg.append(f'<rect x="{x-7.5}" y="{y-7.5}" width="15" height="15" transform="rotate({-k["angle"]} {x} {y})" stroke="#aaa"/>')
 svg+=['<path d="M30 119h25 M30 117v4 M55 117v4"/>','</g>',f'<text x="30" y="125" font-size="2.5" font-family="sans-serif">{side.upper()} NANO DRAFT B - TOP - print 100%; bar = 25 mm</text>','</svg>']
 (OUT/f'mechanical/nano-b-{side}-1to1.svg').write_text('\n'.join(svg))
 mesh=trimesh.creation.extrude_polygon(pcb,height=1.6,engine='earcut');mesh.apply_translation([0,0,.05]);assert mesh.is_watertight
 mesh.export(OUT/f'mechanical/nano-b-{side}-bare-pcb-PROTOTYPE.stl')
 ax.set_aspect('equal');ax.set_xlim(20,160);ax.set_ylim(116,21);ax.axis('off');ax.set_title(side.upper()+' · nano USB-C · new case',fontsize=14,pad=12,color='#152b3a')
 old=np.array([xy(p) for p in OLD[side]['outline']]);new=np.array(outer)
 oa1.plot(old[:,0],old[:,1],color='#d1523b',lw=1.3,ls='--',label='Draft A');oa1.plot(new[:,0],new[:,1],color='#147965',lw=2,label='Draft B')
 oa1.set_xlim((108,157) if side=='left' else(21,69));oa1.set_ylim(115,78);oa1.set_aspect('equal');oa1.set_title(side.upper()+' thumb contour');oa1.legend(loc='upper left');oa1.grid(alpha=.15)
 report[side]={'bare_pcb_mesh_watertight':bool(mesh.is_watertight),'thickness_mm':1.6,'new_outer_area_mm2':poly.area,'added_area_mm2':d['added_area_mm2'],'removed_area_mm2':d['removed_area_mm2'],'electrical_parts_and_tracks':'unchanged','old_mount_holes':'retained starting references; new-case mounts not designed'}
T=G['transform_left_CAD_to_right_CAD'];lp=Polygon(G['sides']['left']['outline_CAD_mm']);rp=Polygon(G['sides']['right']['outline_CAD_mm']);mirror=affinity.translate(affinity.scale(lp,xfact=-1,yfact=1,origin=(0,0)),xoff=T['tx_mm'],yoff=T['ty_mm'])
report['mirror_outline_hausdorff_mm']=mirror.hausdorff_distance(rp);report['mirror_outline_symmetric_difference_mm2']=mirror.symmetric_difference(rp).area;assert report['mirror_outline_hausdorff_mm']<1e-9
fig.text(.5,.09,'DRAFT B · old USB reliefs removed · clean mirrored thumb outlines · electrical placement/routing unchanged',ha='center',fontsize=12,color='#283f4b')
fig.text(.5,.045,'Own case project. Right nice!view, optional RGB and artwork remain planned circuit/layout work.',ha='center',fontsize=11,color='#283f4b');fig.tight_layout(rect=[0,.12,1,1]);fig.savefig(OUT/'layout-preview.png',dpi=160);plt.close(fig)
over.tight_layout();over.savefig(OUT/'thumb-before-after.png',dpi=160);plt.close(over)
(OUT/'checks/geometry-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
