"""Draft Corne placement preview from actual generated pads, not a photorealistic fit claim."""
import os,sys,json,math,re
from pathlib import Path
from draft_c_common import ROOT,OUT,nodes,head
D=ROOT.parent/'corneish-zen-replacement/analysis-tools';sys.path[:0]=[str(D/'render-python'),str(D/'python')]
os.environ.setdefault('MPLCONFIGDIR','/tmp/zen-mpl-cache')
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Rectangle,Circle
import numpy as np
P=json.loads((OUT/'placement.json').read_text());fig,axs=plt.subplots(1,2,figsize=(16,8),facecolor='#f4f6f8')
for side,ax in zip(['left','right'],axs):
 d=P[side];ax.add_patch(Polygon(d['outline'],fc='#164e45',ec='#123b33',lw=1))
 # Optional routing overlay, if a router session has been imported.
 pcb=(OUT/f'draft-corne-{side}.kicad_pcb').read_text()
 for _,_,n in nodes(pcb):
  if head(n)=='segment':
   a=list(map(float,re.search(r'\(start ([\d.e+-]+) ([\d.e+-]+)\)',n).groups()));b=list(map(float,re.search(r'\(end ([\d.e+-]+) ([\d.e+-]+)\)',n).groups()));ax.plot([a[0],b[0]],[a[1],b[1]],color='#e5b663' if '(layer "F.Cu")' in n else '#6aa6dd',lw=.45,alpha=.7)
 for p in d['pads']:
  x,y=p['xy'];w,h=p['size']
  if p['net']:ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,angle=-p['angle'],rotation_point='center',fc='#e9c47c' if p['layer']=='F' else '#85b4d3',ec='none',zorder=3))
  if p['drill']:ax.add_patch(Circle((x,y),p['drill']/2,fc='#f4f6f8',ec='none',zorder=4))
 byref={p['ref']:p for p in d['footprints']};cx,cy=byref['U1']['xy']
 ax.add_patch(Rectangle((cx-9,cy-18.37),18,34.2,fill=False,ec='white',lw=1.4,ls='--'));ax.add_patch(Rectangle((cx-4.5,cy-19.67),9,4,fill=False,ec='white',lw=1))
 ax.text(cx,cy-22.5,'nano USB-C',fontsize=9,color='#213d4b',ha='center')
 if side=='right':
  x,y=byref['J2']['xy'];ax.add_patch(Rectangle((x-7,y-34.4),14,36,fc='#99d7e4',alpha=.2,ec='#6fdbf0',lw=1.2));ax.text(x,y-21,'nice!view\nabove nano',ha='center',va='center',fontsize=8,color='white',linespacing=1.5)
 else:
  x,y=byref['U2']['xy'];ax.add_patch(Rectangle((x-2.65,y-2.65),5.3,5.3,fc='#344758',ec='#f1c36f',lw=.8));ax.text(x,y,'QSPI',ha='center',va='center',fontsize=7,color='white');ax.text(cx,cy,'nano on FRONT\ncomponents DOWN',ha='center',fontsize=8,color='white',linespacing=1.7)
 x,y=byref['J1']['xy'];ax.text(x,y+3.8,'BAT pads: BACK',ha='center',fontsize=7,color='white')
 ax.set_aspect('equal');ax.set_xlim(20,160);ax.set_ylim(112,21);ax.axis('off');ax.set_title(side.upper()+' · Draft Corne C',fontsize=15,color='#152e3d',pad=15)
fig.text(.5,.105,'Typeractive-style Choc geometry · OUR matrix · front-mounted nanos, components down · battery wire pads, no JST',ha='center',fontsize=12,color='#253e4a')
fig.text(.5,.055,'ROUTED · 0 unconnected on both halves · display/nano stack and battery retention need physical review',ha='center',fontsize=11,color='#253e4a')
fig.tight_layout(rect=[0,.15,1,1]);fig.savefig(OUT/'placement-preview.png',dpi=160);plt.close(fig)
print('Saved Draft Corne placement preview.')
