"""Import experimental router sessions; native DRC is required afterwards."""
from pathlib import Path
import wx
app=wx.App(False)
import pcbnew as p
OUT=Path(__file__).resolve().parents[1]/'projects/choc-corne-flash/draft-c'
for side in ['left','right']:
    name=f'draft-corne-{side}'
    if not (OUT/f'{name}.ses').exists():
        raise RuntimeError(f'Missing {side} router session')
    board=p.LoadBoard(str(OUT/f'{name}.kicad_pcb'))
    if not p.ImportSpecctraSES(board,str(OUT/f'{name}.ses')):
        raise RuntimeError(f'Import failed: {side}')
    p.SaveBoard(str(OUT/f'{name}.kicad_pcb'),board)
    print(side,'session imported',flush=True)
