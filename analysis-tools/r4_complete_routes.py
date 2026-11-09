"""Complete explicit DRC airwires with conservative two-layer grid search; native DRC remains authoritative."""
import sys,json,math,heapq,re,time
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];OUT=BASE/'r4-layout'
sys.path[:0]=[str(BASE/'analysis-tools/render-python'),str(BASE/'analysis-tools/python')]
import numpy as np
from scipy.ndimage import binary_erosion
from PIL import Image,ImageDraw
from shapely.geometry import Polygon,Point,LineString,box
from shapely import affinity
step=.1;lo=np.array([20.,20.]);shape=(980,1400)
def idx(xy):return tuple(np.rint((np.array(xy)-lo)/step).astype(int))
def coord(x,y):return [float(lo[0]+x*step),float(lo[1]+y*step)]
def paint(draw,g,fill):
 if g.is_empty:return
 if g.geom_type=='Polygon':
  draw.polygon([idx(p) for p in g.exterior.coords],fill=fill)
  for ring in g.interiors:draw.polygon([idx(p) for p in ring.coords],fill=1-fill)
 else:
  for p in g.geoms:paint(draw,p,fill)
def padshape(a):
 x,y=a['xy'];w,h=a['size']
 if a['circle']:return Point(x,y).buffer(w/2)
 return affinity.rotate(box(x-w/2,y-h/2,x+w/2,y+h/2),-a['angle'],origin=(x,y))
def search(free,start,ends,viafree):
 sx,sy,sl=start;tx,ty,tl=ends;H,W=free.shape[1:];N=H*W
 def key(x,y,l):return l*N+y*W+x
 def decode(k):l,k=divmod(k,N);y,x=divmod(k,W);return x,y,l
 def heur(x,y,l):dx,dy=abs(tx-x),abs(ty-y);return max(dx,dy)+.41421356*min(dx,dy)+(0 if l==tl else 12)
 startid=key(sx,sy,sl);goal=key(tx,ty,tl);cost=np.full(2*N,np.inf,dtype=np.float32);prev=np.full(2*N,-1,dtype=np.int32);cost[startid]=0
 heap=[(heur(sx,sy,sl),0,startid)];iterations=0
 while heap:
  _,g,k=heapq.heappop(heap)
  if g>float(cost[k])+1e-3:continue
  if k==goal:
   path=[]
   while k!=-1:path.append(decode(k));k=int(prev[k])
   return path[::-1]
  x,y,l=decode(k);iterations+=1
  if iterations>3000000:break
  for dx,dy,w in [(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),(1,1,1.41421356),(1,-1,1.41421356),(-1,1,1.41421356),(-1,-1,1.41421356)]:
   xx,yy=x+dx,y+dy
   if not (0<=xx<W and 0<=yy<H) or not free[l,yy,xx]:continue
   if dx and dy and (not free[l,y,xx] or not free[l,yy,x]):continue
   kk=key(xx,yy,l);ng=g+w
   if ng<float(cost[kk])-1e-3:cost[kk]=ng;prev[kk]=k;heapq.heappush(heap,(ng+heur(xx,yy,l),ng,kk))
  if viafree[y,x]:
   kk=key(x,y,1-l);ng=g+35
   if ng<float(cost[kk])-1e-3:cost[kk]=ng;prev[kk]=k;heapq.heappush(heap,(ng+heur(x,y,1-l),ng,kk))
 print('search failed',iterations,flush=True);return None
side='left';data=json.loads((OUT/f'checks/{side}-routing-geometry.json').read_text());geo=json.loads((OUT/'geometry.json').read_text())[side]
aliases={(a['reference'],a['pad']):a['net'] for a in json.loads((OUT/'left-pads.json').read_text()) if a['net']}
netmap={a['net']:aliases.get((a['ref'],a['pad']),a['net']) for a in data['pads'] if a['net']}
for a in data['pads']+data['tracks']:a['net']=netmap.get(a['net'],a['net'])
ox=min(v[0] for v in geo['outline']);oy=max(v[1] for v in geo['outline'])
def xy(v):return [v[0]-ox+25,oy-v[1]+25]
solid=Polygon([xy(v) for v in geo['outline']]).buffer(-.4)
solid=solid.difference(box(*xy([-24.4,4]),*xy([-4.2,-16.5])).buffer(.4))
# Main-controller antenna: no copper underneath its central antenna tip.
antenna=Polygon([xy(v) for v in [(-20.8,4),(-7.8,4),(-7.8,10),(-20.8,10)]]).buffer(.12)
base=Image.new('1',(shape[1],shape[0]),0);paint(ImageDraw.Draw(base),solid,1);paint(ImageDraw.Draw(base),antenna,0)
airwires=json.loads((OUT/'checks/left-routed-drc.json').read_text())['unconnected_items'];result=[]
for ai,air in enumerate(airwires):
 a,b=air['items'];net=netmap.get(re.search(r'\[([^]]+)\]',a['description'])[1],re.search(r'\[([^]]+)\]',a['description'])[1]);print(ai,net,a['pos'],b['pos'],flush=True)
 masks=[]
 for layer in range(2):
  im=base.copy();draw=ImageDraw.Draw(im)
  for pad in data['pads']:
   if pad['drill'] and (pad['net']!=net or not pad['net']):paint(draw,Point(pad['xy']).buffer(pad['drill']/2+.36),0)
   if layer in pad['layers'] and pad['net'] and pad['net']!=net:paint(draw,padshape(pad).buffer(.33),0)
  for t in data['tracks']:
   if t['net']==net:continue
   if t['via']:paint(draw,Point(t['xy']).buffer(t['width']/2+.33),0)
   elif t['layer']==layer:paint(draw,LineString([t['a'],t['b']]).buffer(t['width']/2+.33),0)
  masks.append(np.array(im,dtype=bool))
 free=np.stack(masks);viafree=binary_erosion(free[0]&free[1],structure=np.ones((7,7)))
 starts=[]
 for item in [a,b]:
  x,y=idx([item['pos']['x'],item['pos']['y']]);layer=0 if 'F.Cu' in item['description'] else 1
  if 'PTH' in item['description']:layer=0
  assert free[layer,y,x],('endpoint blocked',net,item,coord(x,y))
  starts.append((x,y,layer))
 path=search(free,*starts,viafree)
 if path is None:continue
 simple=[path[0]]
 for i in range(1,len(path)-1):
  before=tuple(path[i][j]-path[i-1][j] for j in range(3));after=tuple(path[i+1][j]-path[i][j] for j in range(3))
  if before!=after:simple.append(path[i])
 simple.append(path[-1]);tracks=[]
 for u,v in zip(simple[:-1],simple[1:]):
  if u[2]!=v[2]:tracks.append({'via':True,'xy':coord(*u[:2]),'width':.6,'net':net})
  else:tracks.append({'via':False,'a':coord(*u[:2]),'b':coord(*v[:2]),'width':.2,'net':net,'layer':u[2]})
 for item,node in zip([a,b],[path[0],path[-1]]):
  tracks.append({'via':False,'a':[item['pos']['x'],item['pos']['y']],'b':coord(*node[:2]),'width':.2,'net':net,'layer':node[2]})
 data['tracks'].extend(tracks);result.extend(tracks);print('routed',len(path),'nodes',len(tracks),'items',flush=True)
(OUT/'checks/manual-routes.json').write_text(json.dumps(result,indent=2,default=lambda v:int(v)));print('saved',len(result),flush=True)
