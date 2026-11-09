"""Import local routing session and link board footprints to their matching schematics."""
import wx
app=wx.App(False)
import pcbnew as p
from pathlib import Path
import json
import xml.etree.ElementTree as E
BASE=Path(__file__).resolve().parents[1];OUT=BASE/'r4-layout'
links=json.loads((OUT/'schematic-links.json').read_text())
for side in ['left','right']:
 board=p.LoadBoard(str(OUT/f'zen-r4-{side}.kicad_pcb'))
 # Session files use the original engineering net aliases; restore before re-import.
 aliases={(a['reference'],a['pad']):a['net'] for a in json.loads((OUT/f'{side}-pads.json').read_text()) if a['net']}
 restore={}
 for fp in board.GetFootprints():
  for pad in fp.Pads():
   old=aliases.get((fp.GetReference(),pad.GetNumber()))
   if old and pad.GetNetname():restore[pad.GetNetname()]=old
 for old,new in restore.items():board.FindNet(old).SetNetname(new)
 p.SaveBoard(str(OUT/f'zen-r4-{side}.kicad_pcb'),board)
 board=p.LoadBoard(str(OUT/f'zen-r4-{side}.kicad_pcb'))
 ok=p.ImportSpecctraSES(board,str(OUT/f'zen-r4-{side}.ses'));print(side,'import',ok)
 assert ok
 if side=='left' and (OUT/'checks/manual-routes.json').exists():
  for t in json.loads((OUT/'checks/manual-routes.json').read_text()):
   if t['via']:
    a=p.PCB_VIA(board);a.SetPosition(p.VECTOR2I(p.FromMM(t['xy'][0]),p.FromMM(t['xy'][1])));a.SetWidth(p.FromMM(.6));a.SetDrill(p.FromMM(.3));a.SetViaType(p.VIATYPE_THROUGH);a.SetLayerPair(p.F_Cu,p.B_Cu)
   else:
    a=p.PCB_TRACK(board);a.SetStart(p.VECTOR2I(p.FromMM(t['a'][0]),p.FromMM(t['a'][1])));a.SetEnd(p.VECTOR2I(p.FromMM(t['b'][0]),p.FromMM(t['b'][1])));a.SetWidth(p.FromMM(t['width']));a.SetLayer(p.F_Cu if t['layer']==0 else p.B_Cu)
   a.SetNet(board.FindNet(t['net']));board.Add(a)
 for fp in board.GetFootprints():
  ref=fp.GetReference()
  if ref in links[side]['symbols']:
   path=p.KIID_PATH();path.push_back(p.KIID(links[side]['root']));path.push_back(p.KIID(links[side]['symbols'][ref]));fp.SetPath(path)
 if side=='left':
  r=next(f for f in board.GetFootprints() if f.GetReference()=='R1');q=r.GetPosition();r.SetPosition(p.VECTOR2I(q.x,p.FromMM(56.616552)))
 seen=set();via_centers=[]
 pth=[a for f in board.GetFootprints() for a in f.Pads() if a.GetDrillSize().x and a.GetNetname()]
 for t in list(board.GetTracks()):
  if isinstance(t,p.PCB_VIA):
   key=(t.GetPosition().x,t.GetPosition().y,t.GetNetname())
   redundant=any(a.GetNetname()==t.GetNetname() and (a.GetPosition().x-t.GetPosition().x)**2+(a.GetPosition().y-t.GetPosition().y)**2<p.FromMM(.30)**2 for a in pth)
   close=any(n==key[2] and (x-key[0])**2+(y-key[1])**2<p.FromMM(.35)**2 for x,y,n in via_centers)
   if key in seen or redundant or close:board.Remove(t)
   else:seen.add(key);via_centers.append(key)
 xml=E.parse(OUT/f'checks/{side}.net.xml')
 comps={c.attrib['ref']:c for c in xml.findall('.//components/comp')}
 assigned={(n.attrib['ref'],n.attrib['pin']):net.attrib['name'] for net in xml.findall('.//nets/net') for n in net.findall('node')}
 rename={}
 for fp in board.GetFootprints():
  ref=fp.GetReference()
  if ref not in comps:
   fp.SetAttributes(fp.GetAttributes() | p.FP_BOARD_ONLY);continue
  c=comps[ref]
  desired=c.findtext('footprint')
  if desired.endswith('__NoSilk') and not (OUT/'footprints/ZenR4.pretty'/(desired.split(':',1)[1]+'.kicad_mod')).exists():
   name=desired.split(':',1)[1];source=name[:-8]
   lib={'D_SOD-123':'Diode_SMD','R_0603_1608Metric':'Resistor_SMD','C_0603_1608Metric':'Capacitor_SMD','SOIC-8_5.3x5.3mm_P1.27mm':'Package_SO','SW_SPDT_PCM12':'Button_Switch_SMD','SW_SPST_TL3342':'Button_Switch_SMD'}[source]
   plugin=p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP)
   f=plugin.FootprintLoad('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/'+lib+'.pretty',source)
   for graphic in list(f.GraphicalItems()):
    if graphic.GetLayer() in [p.F_SilkS,p.B_SilkS]:f.Remove(graphic)
   f.Reference().SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)));f.Reference().SetTextThickness(p.FromMM(.12));f.Reference().SetVisible(False);f.Value().SetVisible(False)
   f.SetFPID(p.LIB_ID('ZenR4',name));plugin.FootprintSave(str(OUT/'footprints/ZenR4.pretty'),f)
  fp.SetValue(c.findtext('value'));lib,item=c.findtext('footprint').split(':',1);fp.SetFPID(p.LIB_ID(lib,item))
  for pad in fp.Pads():
   if not pad.GetNumber():continue
   new=assigned.get((ref,pad.GetNumber()))
   if new:rename[pad.GetNetname()]=new
   elif ref=='SW22' and pad.GetNumber()=='1':pad.SetNetCode(0)
 for old,new in rename.items():
  info=board.FindNet(old)
  if info:info.SetNetname(new)
 p.SaveBoard(str(OUT/f'zen-r4-{side}.kicad_pcb'),board)
 print(side,'tracks',len(list(board.GetTracks())))
 data={'tracks':[],'pads':[]}
 for t in board.GetTracks():
  if isinstance(t,p.PCB_VIA):data['tracks'].append({'via':True,'xy':[p.ToMM(t.GetPosition().x),p.ToMM(t.GetPosition().y)],'width':p.ToMM(t.GetWidth(p.F_Cu)),'net':t.GetNetname()})
  else:data['tracks'].append({'via':False,'a':[p.ToMM(t.GetStart().x),p.ToMM(t.GetStart().y)],'b':[p.ToMM(t.GetEnd().x),p.ToMM(t.GetEnd().y)],'width':p.ToMM(t.GetWidth()),'net':t.GetNetname(),'layer':0 if t.GetLayer()==p.F_Cu else 1})
 for fp in board.GetFootprints():
  for a in fp.Pads():
   data['pads'].append({'ref':fp.GetReference(),'pad':a.GetNumber(),'xy':[p.ToMM(a.GetPosition().x),p.ToMM(a.GetPosition().y)],'size':[p.ToMM(a.GetSize().x),p.ToMM(a.GetSize().y)],'drill':p.ToMM(a.GetDrillSize().x),'angle':a.GetOrientationDegrees(),'net':a.GetNetname(),'circle':a.GetShape()==p.PAD_SHAPE_CIRCLE,'layers':[i for i,l in enumerate([p.F_Cu,p.B_Cu]) if a.IsOnLayer(l)]})
 (OUT/f'checks/{side}-routing-geometry.json').write_text(json.dumps(data))
 p.ExportSpecctraDSN(board,str(OUT/f'zen-r4-{side}-continue.dsn'))
