"""Generate factual handoff diagrams and rasterize direct KiCad schematic exports. Does not mutate PCB files."""
import os,sys,json,xml.etree.ElementTree as ET
from pathlib import Path
extra=os.environ.get('ZEN_DOCS_PYTHON_PATH')
if extra:sys.path.insert(0,extra)
os.environ.setdefault('MPLCONFIGDIR','/tmp/zen-r4-docs-mpl')
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Rectangle,Circle,FancyBboxPatch,FancyArrowPatch
from matplotlib.lines import Line2D
import cairosvg
ROOT=Path(__file__).resolve().parents[1];IM=ROOT/'docs/images';IM.mkdir(parents=True,exist_ok=True)
BG='#f4f6f8';INK='#152b3a';BLUE='#2268af';AMBER='#d18a17';GREEN='#146c56'
geo=json.loads((ROOT/'r4-layout/geometry.json').read_text())
fig,axs=plt.subplots(1,2,figsize=(16,8.5),facecolor=BG)
for ax,side in zip(axs,['left','right']):
 g=geo[side];d=json.loads((ROOT/f'r4-layout/checks/{side}-routing-geometry.json').read_text());ox=min(v[0] for v in g['outline']);oy=max(v[1] for v in g['outline'])
 def xy(v):return [v[0]-ox+25,oy-v[1]+25]
 outer=[xy(v) for v in g['outline']];ax.add_patch(Polygon(outer,fc='#174f46',ec=INK,lw=.7))
 cx=-14.3 if side=='left' else 24.9;bcx=cx if side=='left' else 23.8
 cut=[xy(v) for v in [(bcx-10.1,-16.5),(bcx+10.1,-16.5),(bcx+10.1,4),(bcx-10.1,4)]];ax.add_patch(Polygon(cut,fc=BG,ec=INK,lw=.8))
 for t in d['tracks']:
  if not t['via']:ax.plot([t['a'][0],t['b'][0]],[t['a'][1],t['b'][1]],color='#edba6a' if t['layer']==0 else '#74a9dc',lw=.5,alpha=.8)
 for p in d['pads']:
  if p['net']:
   x,y=p['xy'];w,h=p['size'];ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,angle=-p['angle'],rotation_point='center',fc='#e7c27b',ec='none'))
  if p['drill']:ax.add_patch(Circle(p['xy'],p['drill']/2,fc=BG,ec='none'))
 x,y=xy([cx-9,39.1]);ax.add_patch(Rectangle((x,y),18,34.2,fill=False,ls='--',ec='white',lw=1.2))
 # USB location at rear of controller, not original connector location.
 ax.annotate('USB at new location',xy=xy([cx,40]),xytext=xy([cx-12 if side=='left' else cx+13,49]),ha='center',fontsize=9,color=INK,arrowprops={'arrowstyle':'->','color':INK})
 tags={1:xy([cx,31]),3:xy([bcx,-5]),4:xy([-35 if side=='left' else 46,-17.5]),5:xy([-12 if side=='left' else 22,-20.5]),6:xy([-49 if side=='left' else 62,-32])}
 if side=='left':tags[2]=xy([-14.3,17.5])
 k=next(k for k in g['keys'] if k['row']==0 and k['col']==5);tags[7]=xy([k['xy'][0],k['xy'][1]+2])
 for n,point in tags.items():ax.text(*point,str(n),fontsize=10,fontweight='bold',ha='center',va='center',color=INK,bbox={'boxstyle':'circle,pad=.28','fc':'white','ec':BLUE,'lw':1.5},zorder=10)
 ax.set_aspect('equal');ax.set_xlim(17,166);ax.set_ylim(118,13);ax.axis('off');ax.set_title(side.upper()+' — carrier TOP view',color=INK,fontweight='bold',fontsize=14,pad=18)
fig.suptitle('Zen R4 DRAFT A · actual routing with placement callouts',fontsize=19,color=INK,y=.97)
fig.text(.5,.16,'1  nano underneath     2  left flash on front     3  battery opening     4  power switch     5  reset',ha='center',fontsize=12,color=INK)
fig.text(.5,.115,'6  Zen thumb cluster     7  top inner socket rotated 180°     Dashed: nano body; amber: front copper; blue: back copper',ha='center',fontsize=11,color=INK)
fig.text(.5,.055,'Electrical rules passed. New case cuts, assembly stack and physical V2 fit remain unverified. Right display footprint is absent.',ha='center',fontsize=11,color=INK)
fig.subplots_adjust(left=.025,right=.975,bottom=.2,top=.88,wspace=.03);fig.savefig(IM/'01-layout-annotated.png',dpi=160,facecolor=BG);plt.close(fig)

fig,ax=plt.subplots(figsize=(15,9),facecolor=BG);ax.set_xlim(0,15);ax.set_ylim(0,9);ax.axis('off')
def box(x,y,w,h,title,body,color=BLUE,dashed=False):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.13',ec=color,fc='white',lw=2,ls='--' if dashed else '-'))
 ax.text(x+w/2,y+h-.3,title,ha='center',va='top',fontsize=14,fontweight='bold',color=color)
 ax.text(x+w/2,y+h/2-.1,body,ha='center',va='center',fontsize=12,color=INK,linespacing=1.6)
def arrow(a,b,label='',color=INK):
 ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=14,color=color,lw=1.7))
 if label:ax.text((a[0]+b[0])/2,(a[1]+b[1])/2+.18,label,ha='center',fontsize=10,color=color,bbox={'fc':BG,'ec':'none','pad':1})
ax.text(7.5,8.6,'Zen R4: tested firmware architecture, unbuilt carrier boards',ha='center',fontsize=18,fontweight='bold',color=INK)
box(.6,5.1,4.1,2.5,'LEFT nice!nano v2','21 Choc keys · shared matrix\nJavelin + Plover modes\nCentral half → host USB / BLE')
box(10.3,5.1,4.1,2.5,'RIGHT nice!nano v2','21 Choc keys · same GPIOs\nRight scan columns reversed\nPeripheral half over BLE')
arrow((4.9,6.5),(10.1,6.5),'BLE split; left sends active mode',BLUE)
box(.6,2.65,4.1,1.55,'LEFT QSPI flash','W25Q128 candidate · 3V3_SW\nD2 / D4 / D5 / D6 / D7 / D3',AMBER)
arrow((2.65,5),(2.65,4.35),'tested wiring kept',AMBER)
box(10.3,2.65,4.1,1.55,'FUTURE right nice!view','No footprint or routes in Draft A\nCS D4 active HIGH · MOSI D2 · SCK D3',BLUE,True)
arrow((12.35,5),(12.35,4.35),'mounting gate',BLUE)
box(5.5,2.65,4,1.55,'POWER — on each half','1S LiPo → SW22 → nano RAW/B+\nUSB charger / regulator on module',GREEN)
arrow((6.3,4.4),(4.6,5.1),color=GREEN);arrow((8.7,4.4),(10.4,5.1),color=GREEN)
ax.text(7.5,1.7,'Switched VCC on LEFT powers flash. P0.13 controls that rail inside the module; no carrier P0.13 connection.',ha='center',fontsize=11,color=INK)
ax.text(7.5,1.1,'Mode display and reconnect behavior were hardware-tested on the existing Ultralight right.',ha='center',fontsize=11,color=INK)
ax.text(7.5,.65,'The custom right matrix and D4-CS display overlays compiled. New boards / new display pin have not been hardware-tested.',ha='center',fontsize=11,color=INK)
fig.tight_layout();fig.savefig(IM/'02-system-and-power.png',dpi=160,facecolor=BG);plt.close(fig)

fig,ax=plt.subplots(figsize=(14,10),facecolor=BG);ax.set_xlim(-11,11);ax.set_ylim(-1.5,15);ax.axis('off')
ax.text(0,14.4,'nice!nano edge holes in carrier TOP view',ha='center',fontsize=20,fontweight='bold',color=INK)
ax.text(0,13.7,'Module components face DOWN toward plastic base · USB toward rear',ha='center',fontsize=12,color=INK)
ax.add_patch(FancyBboxPatch((-3.3,.4),6.6,12.5,boxstyle='round,pad=.08',ec=BLUE,fc='#e4edf5',lw=2))
ax.add_patch(Rectangle((-1.3,12.35),2.6,1.05,ec=INK,fc='#bcc7d0'));ax.text(0,12.8,'USB',ha='center',va='center',fontsize=12,color=INK)
left=['13  RAW / B+','14  GND','15  RESET_N','16  VCC switched','17  D21 → ROW2','18  D20 → ROW3','19  D19 → COL0','20  D18 → COL1','21  D15 → COL2','22  D14 → COL3','23  D16 unused','24  D10 unused']
right=['1  D1 → COL5','2  D0 → COL4','3  GND','4  GND','5  D2 → flash CS / reserved MOSI','6  D3 → flash IO3 / reserved SCK','7  D4 → flash CLK / reserved CS','8  D5 → flash IO0','9  D6 → flash IO1','10  D7 → flash IO2','11  D8 → ROW0','12  D9 → ROW1']
for i,(l,r) in enumerate(zip(left,right)):
 y=11.9-i*.98
 for x in [-2.85,2.85]:ax.add_patch(Circle((x,y),.16,fc='white',ec=BLUE,lw=1.2))
 ax.text(-3.6,y,l,ha='right',va='center',fontsize=11,color=INK);ax.text(3.6,y,r,ha='left',va='center',fontsize=10.5,color=INK)
ax.text(0,7.3,'1–24 are THIS PROJECT\'S\nedge-hole numbers,\nnot MCU package pins.',ha='center',va='center',fontsize=12,color=INK,linespacing=1.6)
ax.text(0,4.35,'D1 / pad 1 is RIGHT\nin this top view.',ha='center',fontsize=12,fontweight='bold',color=BLUE,linespacing=1.6)
ax.text(0,-.55,'Flash functions apply to LEFT only. Display functions are reserved on RIGHT; no display footprint exists.',ha='center',fontsize=11,color=INK)
ax.text(0,-1.05,'Looking directly at the module component face reverses the two banks. Check the physical module before soldering.',ha='center',fontsize=11,color=INK)
fig.subplots_adjust(left=.015,right=.985,bottom=.02,top=.98);fig.savefig(IM/'03-nano-top-view-pinmap.png',dpi=160,facecolor=BG);plt.close(fig)

for side in ['left','right']:
 source=ROOT/f'docs/schematics/zen-r4-{side}.svg'
 cairosvg.svg2png(url=str(source),write_to=str(IM/f'{side}-schematic-full.png'),output_width=5000,background_color='white')
 root=ET.fromstring(source.read_text())
 # Focus on module, battery/reset/power, and left flash, preserving exact KiCad graphics.
 root.set('viewBox','285 42 125 205');root.set('width','125mm');root.set('height','205mm')
 cairosvg.svg2png(bytestring=ET.tostring(root),write_to=str(IM/f'{side}-controller-detail.png'),output_width=2100,background_color='white')
print('Created annotated layout, system/power, pin-orientation and four native schematic PNGs.')
