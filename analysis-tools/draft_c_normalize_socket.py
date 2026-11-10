"""Save one actual B socket as native-normalized F library source for exact library comparison."""
import wx
app=wx.App(False)
import pcbnew as p
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'projects/choc-corne-flash/draft-c'
b=p.LoadBoard(str(OUT/'draft-corne-left.kicad_pcb'))
f=next(f for f in b.GetFootprints() if f.GetReference()=='SW1')
f.SetOrientationDegrees(0);f.SetPosition(p.VECTOR2I(0,0));f.Flip(p.VECTOR2I(0,0),p.FLIP_DIRECTION_LEFT_RIGHT)
f.SetReference('REF**');f.SetValue('ChocSocket_Bottom');f.SetPath(p.KIID_PATH());f.SetFPID(p.LIB_ID('DraftC','ChocSocket_Bottom'))
plugin=p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP);plugin.FootprintSave(str(OUT/'footprints/DraftC.pretty'),f)
print('Saved native front-normalized socket library footprint.')
