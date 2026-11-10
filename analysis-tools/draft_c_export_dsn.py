"""Export placed Draft C to local autorouter input; no firmware or baseline changes."""
import wx
app=wx.App(False)
import pcbnew as p
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'projects/choc-corne-flash/draft-c'
for side in ['left','right']:
 b=p.LoadBoard(str(OUT/f'draft-corne-{side}.kicad_pcb'))
 p.ExportSpecctraDSN(b,str(OUT/f'draft-corne-{side}.dsn'))
 f=OUT/f'draft-corne-{side}.dsn';f.write_text(f.read_text().replace('(clearance 50 (type smd_smd))','(clearance 200 (type smd_smd))\n      (clearance 350 (type default_area))'))
 print('Exported',side)
