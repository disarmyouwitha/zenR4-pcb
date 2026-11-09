"""KiCad 10 pcbnew: create placed Zen R4 carrier boards. Run with bundled KiCad Python."""
import wx
app=wx.App(False)
import pcbnew as p
import json,math,os,uuid
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];OUT=BASE/'r4-layout'
LIB=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints')
geo=json.loads((OUT/'geometry.json').read_text())
contract=json.loads((BASE/'zen-r4-review/gpio-contract.json').read_text())
FP=OUT/'footprints/ZenR4.pretty'
def layers(*ids):
 s=p.LSET()
 for i in ids:s.AddLayer(i)
 return s
def mm(v):return p.FromMM(v)
def pt(x,y):return p.VECTOR2I(mm(x),mm(y))
def pos(x):return p.ToMM(x.x),p.ToMM(x.y)
def newfp(name,layer=p.F_Cu):
 f=p.FOOTPRINT(None);f.SetFPID(p.LIB_ID('ZenR4',name));f.SetValue(name);f.SetLayer(layer);return f
def line(board,a,b,layer=p.Edge_Cuts,w=.05,parent=None):
 s=p.PCB_SHAPE(parent or board);s.SetShape(p.SHAPE_T_SEGMENT);s.SetStart(pt(*a));s.SetEnd(pt(*b));s.SetLayer(layer);s.SetWidth(mm(w));(parent or board).Add(s)
 return s
def pad(f,num,xy,size,net=None,drill=None,kind=None):
 a=p.PAD(f);a.SetNumber(str(num));a.SetPosition(pt(*xy));a.SetSize(pt(*size))
 if drill:
  a.SetAttribute(p.PAD_ATTRIB_NPTH if kind=='npth' else p.PAD_ATTRIB_PTH);a.SetShape(p.PAD_SHAPE_CIRCLE);a.SetDrillSize(pt(drill,drill));a.SetLayerSet(p.LSET.AllCuMask())
 else:
  a.SetAttribute(p.PAD_ATTRIB_SMD);a.SetShape(p.PAD_SHAPE_RECT);a.SetLayerSet(layers(p.F_Cu,p.F_Paste,p.F_Mask))
 if net:a.SetNet(net)
 f.Add(a);return a
def rect(f,x1,y1,x2,y2,layer=p.F_Fab):
 for a,b in [((x1,y1),(x2,y1)),((x2,y1),(x2,y2)),((x2,y2),(x1,y2)),((x1,y2),(x1,y1))]:line(None,a,b,layer,.1,f)
def make_socket():
 f=newfp('Choc_PG1350_bottom')
 # Final B-side holes in key-side plan: x=-5,y=+3.7 and x=0,y=+5.9.
 # KiCad Flip here negates Y. Source compensation is Y-only.
 for xy,d in [((0,0),3.4),((-5.5,0),1.9),((5.5,0),1.9),((0,-5.9),3),((-5,-3.7),3)]:pad(f,'',xy,(d,d),drill=d,kind='npth')
 pad(f,1,(3.1,-5.9),(2.3,2.6));pad(f,2,(-8.1,-3.7),(2.3,2.6))
 rect(f,-7.5,-7.5,7.5,7.5)
 court=json.loads((OUT/'socket-courtyard.json').read_text())
 for a,c in zip(court[:-1],court[1:]):line(None,a,c,p.F_CrtYd,.05,f)
 return f
def make_nano():
 f=newfp('NiceNano_v2_edges')
 # Source F-side pattern; flipped for actual bottom mounting.
 # Final top-of-carrier plan: component face points down, USB to rear.
 # Thus D1 is RIGHT in carrier top view (LEFT when looking at module components).
 # Flip + orientation reset negates source Y only; pre-reflect source X here.
 rows=[[1,0,None,None,2,3,4,5,6,7,8,9],[None,None,None,None,21,20,19,18,15,14,16,10]]
 for bank in range(2):
  for i in range(12):pad(f,bank*12+i+1,((1 if bank==0 else -1)*7.62,13.97-2.54*i),(1.65,1.65),drill=1.)
 rect(f,-9,-17.1,9,17.1);rect(f,-4.5,-18.4,4.5,-10)
 return f
def mount():
 f=newfp('Zen_mount_4p4')
 pad(f,'',(0,0),(4.4,4.4),drill=4.4,kind='npth');return f

for name,f in [('Choc_PG1350_bottom',make_socket()),('NiceNano_v2_edges',make_nano()),('Zen_mount_4p4',mount())]:
 p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(FP),f)
for side in os.environ.get('ZEN_R4_SIDE','left,right').split(','):
 g=geo[side];b=p.BOARD();b.SetCopperLayerCount(2);b.GetDesignSettings().SetBoardThickness(mm(1.6))
 ds=b.GetDesignSettings();ds.m_MinClearance=mm(.2);ds.m_CopperEdgeClearance=mm(.25)
 ds.m_TrackMinWidth=mm(.2);ds.m_ViasMinSize=mm(.6);ds.m_MinThroughDrill=mm(.3)
 ox=min(v[0] for v in g['outline']);oy=max(v[1] for v in g['outline'])
 def xy(v):return v[0]-ox+25,oy-v[1]+25
 nets={}
 def net(n):
  if n not in nets:
   a=p.NETINFO_ITEM(b,n);b.Add(a);nets[n]=a
  return nets[n]
 def add(f,ref,where,ang=0,back=False,netsmap=None):
  b.Add(f)
  if back:f.Flip(pt(0,0),p.FLIP_DIRECTION_LEFT_RIGHT)
  f.SetReference(ref);f.SetPosition(pt(*xy(where)));f.SetOrientationDegrees(ang)
  f.Reference().SetTextSize(pt(.8,.8));f.Reference().SetTextThickness(mm(.12))
  f.Reference().SetVisible(False);f.Value().SetVisible(False)
  for graphic in list(f.GraphicalItems()):
   if graphic.GetLayer() in [p.F_SilkS,p.B_SilkS]:f.Remove(graphic)
  for a in f.Pads():
   if netsmap and a.GetNumber() in netsmap:a.SetNet(net(netsmap[a.GetNumber()]))
  return f
 def std(lib,name):return p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP).FootprintLoad(str(LIB/(lib+'.pretty')),name)
 # Source outline inherently includes the Zen thumb silhouette and correct boss holes.
 outline=[xy(v) for v in g['outline']]
 for a,c in zip(outline[:-1],outline[1:]):line(b,a,c)
 for i,c in enumerate(g['mounts'],1):add(mount(),'H'+str(i),c)
 # Keys are mirrored physically but both use C0 outside and C5 at split.
 for k in g['keys']:
  r,c=k['row'],k['col'];i=r*6+(c if side=='left' else 5-c)+1 if r<3 else 19+(c-3 if side=='left' else 5-c)
  # The side-swap pattern must be mirrored for the opposite physical board.
  angle=k['angle']+(180 if (r==0 and c==5) else 0);keysocket=make_socket()
  f=add(keysocket,'SW'+str(i),k['xy'],angle,True,{'1':f'COL{c}','2':f'KEY{i}'})
  rad=math.radians(angle);sx=1
  # Diode above switch, offset toward inner edge; socket is on lower side.
  dx,dy=(-3.3 if side=='left' and i==20 else sx*3.3),3.8
  off=(dx*math.cos(rad)-dy*math.sin(rad),dx*math.sin(rad)+dy*math.cos(rad))
  dc=[k['xy'][0]+off[0],k['xy'][1]+off[1]]
  d=std('Diode_SMD','D_SOD-123')
  add(d,'D'+str(i),dc,angle-90,True,{'1':f'ROW{r}','2':f'KEY{i}'})
 # Registered original board interior strip; USB faces the rear edge y≈43.
 cx=-14.3 if side=='left' else 24.9
 nano=add(make_nano(),'U1',[cx,22.0],0,True)
 # pth pin numbers follow actual component face after bottom flip, not original top view.
 used={}
 for name,e in contract[side+'_matrix'].items():used[e['review_U1_pad']]=name
 if side=='left':
  for n,e in contract['left_qspi'].items():used[e['review_U1_pad']]=n
 used.update({3:'GND',4:'GND',13:'BAT_SW',14:'GND',15:'RESET_N'})
 if side=='left':used[16]='3V3_SW'
 for a in nano.Pads():
  n=int(a.GetNumber())
  if n in used:a.SetNet(net(used[n]))
  else:
   # Mark electrically unused edge pads to avoid ambiguous floating annuli.
   a.SetNet(net('NC_U1_'+str(n)))
 # Explicit custom battery wire pads and footprint; connector choice is not presumed.
 bat=newfp('Battery_wire_pads')
 pad(bat,1,(-1.25,0),(2,2),drill=1.0);pad(bat,2,(1.25,0),(2,2),drill=1.0)
 p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(FP),bat)
 add(bat,'J1',[cx+(-6 if side=='left' else 6),-18.0],0,False,{'1':'BAT_RAW','2':'GND'})
 # Bottom slide power switch and reset footprint from standard library.
 power=std('Button_Switch_SMD','SW_SPDT_PCM12')
 add(power,'SW22',[(-35 if side=='left' else 46),-17.5],0,True,{'1':'NC_POWER','2':'BAT_RAW','3':'BAT_SW'})
 reset=std('Button_Switch_SMD','SW_SPST_TL3342')
 add(reset,'SW23',[(-12 if side=='left' else 22), -20.5],0,True,{'1':'RESET_N','2':'GND'})
 # Rectangular battery opening (source outline retains its exact outer profile).
 bcx=cx if side=='left' else 23.8
 x1,x2=bcx-10.1,bcx+10.1;y1,y2=-16.5,4.0
 cut=[xy(v) for v in [(x1,y1),(x1,y2),(x2,y2),(x2,y1),(x1,y1)]]
 for a,c in zip(cut[:-1],cut[1:]):line(b,a,c)
 if side=='left':
  flash=std('Package_SO','SOIC-8_5.3x5.3mm_P1.27mm')
  add(flash,'U2',[cx,17.5],0,False,{str(k):v for k,v in {1:'FLASH_CS_N',2:'FLASH_IO1',3:'FLASH_IO2',4:'GND',5:'FLASH_IO0',6:'FLASH_CLK',7:'FLASH_IO3',8:'3V3_SW'}.items()})
  add(std('Capacitor_SMD','C_0603_1608Metric'),'C1',[cx,22.0],0,False,{'1':'3V3_SW','2':'GND'})
  add(std('Resistor_SMD','R_0603_1608Metric'),'R1',[cx,11.28],0,False,{'1':'3V3_SW','2':'FLASH_CS_N'})
 # Antenna end of module. Keep tracks/vias/pours off the region on all copper.
 # Boundary deliberately outside battery opening, surrounding the antenna end.
 zone=p.ZONE(b);zone.SetLayerSet(p.LSET.AllCuMask());zone.SetIsRuleArea(True)
 zone.SetDoNotAllowTracks(True);zone.SetDoNotAllowVias(True);zone.SetDoNotAllowZoneFills(True)
 poly=zone.Outline();poly.NewOutline()
 for v in [(cx-6.5,4.0),(cx+6.5,4.0),(cx+6.5,10.0),(cx-6.5,10.0)]:
  x,y=xy(v);poly.Append(mm(x),mm(y))
 b.Add(zone)
 # Engineering note is documentation, never copper.
 text=p.PCB_TEXT(b);text.SetText('ZEN R4 '+side.upper()+' / DRAFT A / 1.6mm\nShared matrix / edge-only nano / BLE\nNO DISPLAY FOOTPRINT - placement pending')
 text.SetPosition(pt(90,15));text.SetLayer(p.Dwgs_User);text.SetTextSize(pt(1,1));text.SetTextThickness(mm(.15));b.Add(text)
 p.SaveBoard(str(OUT/f'zen-r4-{side}.kicad_pcb'),b)
 p.ExportSpecctraDSN(b,str(OUT/f'zen-r4-{side}.dsn'))
 dsn=OUT/f'zen-r4-{side}.dsn';dsn.write_text(dsn.read_text().replace('(clearance 50 (type smd_smd))','(clearance 200 (type smd_smd))\n      (clearance 350 (type default_area))'))
 print(side,'footprints',len(list(b.GetFootprints())),'outline created')
 # Export absolute pad positions for collision analysis and downstream review.
 pdata=[]
 for fp in b.GetFootprints():
  for a in fp.Pads():
   pdata.append(dict(reference=fp.GetReference(),pad=a.GetNumber(),xy=pos(a.GetPosition()),net=a.GetNetname(),
                     hole=p.ToMM(a.GetDrillSize().x),size=pos(a.GetSize())))
 (OUT/f'{side}-pads.json').write_text(json.dumps(pdata,indent=2))
