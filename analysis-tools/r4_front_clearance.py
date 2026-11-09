"""Sample front component envelopes against archived metal shell, not a V2 fit certificate."""
from compare_geometry import *
OUT=BASE/'r4-layout'
o=stl_objects(BASE/'references/zen-original/Corne-ish_Zen_3x6_main_case_left.stl')[0]
tri=o['vertices'][o['faces']];mn=tri[:,:,:2].min(1);mx=tri[:,:,:2].max(1)
def hits(x,y):
 pt=np.array([x,y]);t=tri[((mn<=pt+1e-6)&(mx>=pt-1e-6)).all(1)];a,b=t[:,1]-t[:,0],t[:,2]-t[:,0];d=a[:,0]*b[:,1]-a[:,1]*b[:,0];m=abs(d)>1e-8;t,a,b,d=t[m],a[m],b[m],d[m];xx,yy=(pt-t[:,0,:2]).T;u,v=(xx*b[:,1]-yy*b[:,0])/d,(yy*a[:,0]-xx*a[:,1])/d;good=(u>=-1e-6)&(v>=-1e-6)&(u+v<=1+1e-6);return np.unique(np.round((t[:,0,2]+u*a[:,2]+v*b[:,2])[good],3))
result={}
for ref,cx,cy,w,h,height in [('U2',-14.3,17.5,8.2,5.3,2.16),('C1',-14.3,22,2.2,1.1,1.0),('R1',-14.3,11.28,2.2,1.1,.65)]:
 samples=[]
 for x in np.linspace(cx-w/2,cx+w/2,19):
  for y in np.linspace(cy-h/2,cy+h/2,13):
   above=hits(x,y);above=above[above>1.65]
   if len(above):samples.append(float(min(above)-1.65-height))
 result[ref]={'samples':247,'nominal_height_assumed_mm':height,'minimum_sampled_headroom_mm':min(samples) if samples else None,'all_samples_in_open_window':not samples,'interference_at_sample':bool(samples and min(samples)<0)}
assert not any(r['interference_at_sample'] for r in result.values()),result
result['scope']='Grid sample of early archived shell only. Exact part height, solder and physical V2 remain to verify.'
(OUT/'checks/front-component-clearance.json').write_text(json.dumps(result,indent=2));print(result)
