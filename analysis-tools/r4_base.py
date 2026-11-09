"""Prototype-only bottom-plate pockets; preserve shell perimeter and mounting seats."""
import sys,json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis-tools/mesh-python'))
import trimesh
OUT=BASE/'r4-layout';(OUT/'mechanical').mkdir(exist_ok=True)
def box(lo,hi):
 m=trimesh.creation.box(extents=[b-a for a,b in zip(lo,hi)])
 m.apply_translation([(a+b)/2 for a,b in zip(lo,hi)])
 return m
results={}
for side,cx in [('left',-14.3),('right',24.9)]:
 src=BASE/f'references/zen-original/Corne-ish_Zen_3x6_bottomplate_{side}.stl'
 m=trimesh.load_mesh(src,process=True)
 m.merge_vertices(digits_vertex=4)
 m.update_faces(m.nondegenerate_faces());m.update_faces(m.unique_faces())
 m.fix_normals()
 # Source STL has stray open triangles. Retain its single closed structural shell.
 shells=[c for c in m.split(only_watertight=False) if c.is_watertight]
 m=max(shells,key=lambda c:abs(c.volume));m.fix_normals()
 print(side,'source watertight',m.is_watertight,'volume',m.volume)
 # Wider outer boss adds wall/floor; pocket removes stock ribs at nano position.
 # Fits inside original strip in XY but protrudes below base by ~2 mm.
 lo=[cx-10.2,2.5,-5.5];hi=[cx+10.2,42.4,-2.5]
 raised=box(lo,hi)
 joined=trimesh.boolean.union([m,raised],engine='manifold',check_volume=True)
 inner=box([cx-9.3,3.5,-4.25],[cx+9.3,44,2])
 result=trimesh.boolean.difference([joined,inner],engine='manifold',check_volume=True)
 assert result.is_watertight and result.is_volume
 result.export(OUT/f'mechanical/zen-r4-{side}-base-pocket-PROTOTYPE.stl')
 results[side]={'watertight':result.is_watertight,'volume_mm3':result.volume,'bottom_z_mm':-5.5,
 'pocket_floor_z_mm':-4.25,'local_floor_thickness_mm':1.25,'internal_nominal_width_length_mm':[18.6,38.9],
 'warning':'Prototype only: mounting underside of nano from PCB z=-0.05, solder/antenna/battery stack and V2 perimeter must be dry fitted. Not a fit certification.'}
(OUT/'mechanical/base-pocket-report.json').write_text(json.dumps(results,indent=2))
