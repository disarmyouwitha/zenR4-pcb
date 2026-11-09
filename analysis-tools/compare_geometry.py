from pathlib import Path
import json,numpy as np
from scipy.spatial.transform import Rotation
BASE=Path(__file__).resolve().parents[1]
MODELS=BASE/'references/typeractive-choc-3d'
def load(name):
 result=[]
 for node in json.loads((MODELS/f'{name}-decoded.json').read_text()):
  matrix=np.array(node['matrix']).reshape(4,4).T
  inst=node['instances']; count=len(next(iter(inst.values()))) if inst else 1
  for i in range(count):
   trans=np.array(inst.get('TRANSLATION',[[0,0,0]]*count)[i]) if inst else np.zeros(3)
   scale=np.array(inst.get('SCALE',[[1,1,1]]*count)[i]) if inst else np.ones(3)
   rot=Rotation.from_quat(inst.get('ROTATION',[[0,0,0,1]]*count)[i]).as_matrix() if inst else np.eye(3)
   for prim in node['primitives']:
    pts=np.array(prim['positions']); pts=(pts*scale)@rot.T+trans
    pts=(np.c_[pts,np.ones(len(pts))]@matrix.T)[:,:3]*1000
    result.append({'node':node['node'],'instance':i,'primitive':prim['primitive'],'material':prim['material'],'vertices':pts,'faces':np.array(prim['indices']).reshape(-1,3)})
 return result
if __name__=='__main__':
 for name in ['pcb','nano','battery','headers','switch']:
  objects=load(name); pts=np.concatenate([o['vertices'] for o in objects]);print(name,'bounds',pts.min(0),pts.max(0))
  if name=='pcb':
   for o in objects:
    if o['instance']==0: print(o['node'],o['primitive'],o['material'],len(o['vertices']),o['vertices'].min(0).round(3),o['vertices'].max(0).round(3))
   for node in [3,4]:
    print('node',node,'centers',[(o['vertices'].min(0)+o['vertices'].max(0)).round(3)/2 for o in objects if o['node']==node][:24])

def section(objects,z):
 segments=[]
 for obj in objects:
  tri=obj['vertices'][obj['faces']]; d=tri[:,:,2]-z
  chosen=tri[(d.min(1)<-1e-7)&(d.max(1)>1e-7)]
  for t in chosen:
   hits=[]
   for a,b in [(0,1),(1,2),(2,0)]:
    if (t[a,2]-z)*(t[b,2]-z)<0:
     hits.append(t[a,:2]+(t[b,:2]-t[a,:2])*(z-t[a,2])/(t[b,2]-t[a,2]))
   if len(hits)==2: segments.append(hits)
 seg=np.array(segments)
 from scipy.sparse import coo_matrix
 from scipy.sparse.csgraph import connected_components
 pts,inv=np.unique(np.round(seg.reshape(-1,2),3),axis=0,return_inverse=True)
 edges=inv.reshape(-1,2);g=coo_matrix((np.ones(len(edges)*2),(np.r_[edges[:,0],edges[:,1]],np.r_[edges[:,1],edges[:,0]])),shape=(len(pts),len(pts)))
 count,labels=connected_components(g)
 return [pts[labels==i] for i in range(count)]
if __name__=='__main__':
 board=[o for o in load('pcb') if o['node']==0 and o['primitive'] in [0,1]]
 loops=section(board,.8)
 print('BOARD LOOPS',len(loops))
 for i,l in enumerate(loops):
  bounds=np.ptp(l,axis=0); center=(l.min(0)+l.max(0))/2
  if center[0]<0:print(i,len(l),'center',center.round(3),'size',bounds.round(3))
 (MODELS/'pcb-section-loops.json').write_text(json.dumps([l.tolist() for l in loops]))

def section_paths(objects,z):
 segments=[]
 for obj in objects:
  tri=obj['vertices'][obj['faces']]; d=tri[:,:,2]-z
  for t in tri[(d.min(1)<-1e-7)&(d.max(1)>1e-7)]:
   hits=[]
   for a,b in [(0,1),(1,2),(2,0)]:
    if (t[a,2]-z)*(t[b,2]-z)<0: hits.append(t[a,:2]+(t[b,:2]-t[a,:2])*(z-t[a,2])/(t[b,2]-t[a,2]))
   if len(hits)==2:segments.append(hits)
 pts,inv=np.unique(np.round(np.array(segments).reshape(-1,2),3),axis=0,return_inverse=True)
 edges=np.unique(np.sort(inv.reshape(-1,2),axis=1),axis=0);edges=edges[edges[:,0]!=edges[:,1]]
 adj={}
 for a,b in edges:adj.setdefault(a,set()).add(b);adj.setdefault(b,set()).add(a)
 paths=[];unused=set(map(tuple,edges))
 while unused:
  a,b=next(iter(unused)); path=[a];start=a
  while True:
   unused.discard(tuple(sorted((a,b))));path.append(b)
   if b==start:break
   options=[v for v in adj[b] if tuple(sorted((b,v))) in unused]
   if not options:break
   a,b=b,options[0]
  paths.append(pts[path])
 return paths

def stl_objects(path):
 dtype=np.dtype([('normal','<f4',(3,)),('v','<f4',(3,3)),('attr','<u2')]); tri=np.fromfile(path,dtype=dtype,offset=84)['v'].astype(float)
 return [{'vertices':tri.reshape(-1,3),'faces':np.arange(len(tri)*3).reshape(-1,3)}]
