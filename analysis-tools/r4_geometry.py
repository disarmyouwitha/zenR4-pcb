"""Recover both Zen halves' mechanical geometry in matched case coordinates."""
from compare_geometry import *
from scipy.optimize import linear_sum_assignment
from scipy.spatial import ConvexHull
def rdp(p,eps=.03):
 if len(p)<3:return p
 v=p[-1]-p[0];n=np.linalg.norm(v);d=np.linalg.norm(p-p[0],axis=1) if n<1e-9 else abs(v[0]*(p-p[0])[:,1]-v[1]*(p-p[0])[:,0])/n
 i=int(d.argmax())
 return np.vstack([rdp(p[:i+1],eps)[:-1],rdp(p[i:],eps)]) if d[i]>eps else p[[0,-1]]

OUT=BASE/'r4-layout'
paths=section_paths(stl_objects(BASE/'references/zen-original/Corne-ish_Zen_-_PCBs_v1.stl'),1.3)
result={}
for side,sign in [('left',-1),('right',1)]:
 loops=section_paths(stl_objects(BASE/f'references/zen-original/Corne-ish_Zen_3x6_main_case_{side}.stl'),2)
 apertures=[l for l in loops if np.all((np.ptp(l,axis=0)>13)&(np.ptp(l,axis=0)<21))]
 assert len(apertures)==21
 centers=np.array([(l.min(0)+l.max(0))/2 for l in apertures])
 holes=[l for l in paths if sign*l[:,0].mean()>0 and np.all((np.ptp(l,axis=0)>3.3)&(np.ptp(l,axis=0)<3.5))]
 source=np.array([(l.min(0)+l.max(0))/2 for l in holes]);assert len(source)==21
 a=source[source[:,1]>-10];b=centers[centers[:,1]>-10]
 t=b.mean(0)-a.mean(0)
 i,j=linear_sum_assignment(np.linalg.norm((a+t)[:,None]-b[None,:],axis=2))
 a,b=a[i],b[j];u,s,v=np.linalg.svd((a-a.mean(0)).T@(b-b.mean(0)));R=u@v;t=b.mean(0)-a.mean(0)@R
 aligned=source@R+t
 i,j=linear_sum_assignment(np.linalg.norm(aligned[:,None]-centers[None,:],axis=2))
 err=np.linalg.norm(aligned[i]-centers[j],axis=1)
 assert max(err)<.15,max(err)
 outline=next(l for l in paths if sign*l[:,0].mean()>0 and np.ptp(l,axis=0).max()>100)
 outline=rdp(outline@R+t)
 mounts=[((l.min(0)+l.max(0))/2)@R+t for l in paths if sign*l[:,0].mean()>0 and np.all((np.ptp(l,axis=0)>4.2)&(np.ptp(l,axis=0)<4.4))]
 assert len(mounts)==5
 keys=[]
 main=sorted([l for l in apertures if l[:,1].mean()>-10],key=lambda l:-sign*l[:,0].mean())
 for c in range(6):
  for r,l in enumerate(sorted(main[c*3:c*3+3],key=lambda l:-l[:,1].mean())):
   keys.append(dict(row=r,col=c,xy=((l.min(0)+l.max(0))/2).tolist(),angle=0.))
 for c,l in enumerate(sorted([l for l in apertures if l[:,1].mean()<-10],key=lambda l:-sign*l[:,0].mean()),3):
  v=l[ConvexHull(l).vertices];dif=np.roll(v,-1,axis=0)-v
  # dominant edge closest to horizontal gives rotation of switch body.
  edge=dif[np.argmax(np.linalg.norm(dif,axis=1))]
  angle=np.degrees(np.arctan2(edge[1],edge[0]));angle=(angle+45)%90-45
  keys.append(dict(row=3,col=c,xy=((l.min(0)+l.max(0))/2).tolist(),angle=float(angle)))
 result[side]=dict(outline=outline.tolist(),mounts=np.array(mounts).tolist(),keys=keys,
                   registration_max_error_mm=float(max(err)),source='early Zen CAD registered to case switch apertures')
(OUT/'geometry.json').write_text(json.dumps(result,indent=2))
for s,d in result.items():print(s,'registration max',d['registration_max_error_mm'],'mounts',d['mounts'],'thumbs',d['keys'][-3:])
