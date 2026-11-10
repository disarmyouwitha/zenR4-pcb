"""Audit Draft C native reports and intended schematic/PCB pad assignments."""
import hashlib,json,re,xml.etree.ElementTree as ET
from draft_c_common import ROOT,OUT,nodes,head
plan=json.loads((OUT.parent/'pin-plan.json').read_text());result={'revision':'Draft-Corne C','date':'2026-11-09','status':'PARTIALLY ROUTED DEVELOPMENT DRAFT — NOT FOR FABRICATION','sides':{},'assembly_not_verified':['nano/header stack height and component clearance','nice!view standoff height and retention','battery thickness, insulation and strain relief','purchased-part footprint dimensions and switch polarity','antenna environment in the eventual enclosure']}
for side in ['left','right']:
    pcb=OUT/f'draft-corne-{side}.kicad_pcb';sch=OUT/f'draft-corne-{side}.kicad_sch'
    native=json.loads((OUT/f'checks/{side}-drc.json').read_text());erc=json.loads((OUT/f'checks/{side}-erc.json').read_text())
    netlist=ET.parse(OUT/f'checks/{side}.net.xml').getroot()
    members={n.attrib['name']:{(c.get('ref'),c.get('pin')) for c in n.findall('node')} for n in netlist.findall('./nets/net')}
    fps={}
    for _,_,node in nodes(pcb.read_text()):
        if head(node)=='footprint':fps[re.search(r'\(property "Reference" "([^"]+)"',node)[1]]=node
    def pad(ref,num):return next(n for _,_,n in nodes(fps[ref]) if head(n)=='pad' and re.match(r'\(pad "'+str(num)+r'"\s',n))
    checked=[]
    def require(net,ref,num):
        assert (ref,str(num)) in members['/'+net],(side,net,ref,num)
        assert f'(net "/{net}")' in pad(ref,num),(side,net,ref,num,'PCB')
        checked.append(f'{net}: {ref}.{num}')
    for name,v in plan['matrix'].items():require(name,'U1',v['review_U1_pad'])
    if side=='left':
        for name,v in plan['qspi'].items():require(name,'U1',v['review_U1_pad']);require(name,'U2',v['U2_pad'])
        require('3V3_SW','U2',8);require('GND','U2',4)
        assert 'J2' not in fps
    else:
        for name,v in plan['right_display'].items():require(name,'U1',v['review_U1_pad'])
        for n,name in enumerate(['VIEW_MOSI','VIEW_SCK','3V3_SW','GND','VIEW_CS_ACTIVE_HIGH'],1):require(name,'J2',n)
        assert 'U2' not in fps
    require('BAT_RAW','J1',1);require('GND','J1',2)
    assert re.search(r'\(layer "F.Cu"\)',fps['U1'])
    assert re.search(r'\(layer "B.Cu"\)',fps['J1'])
    assert float(re.search(r'\(at ([\d.-]+)',pad('U1',1))[1])>0
    assert float(re.search(r'\(at ([\d.-]+)',pad('U1',13))[1])<0
    assert len([r for r in fps if re.fullmatch(r'SW(?:[1-9]|1\d|2[01])',r)])==21
    erc_violations=[v for sheet in erc.get('sheets',[]) for v in sheet.get('violations',[])]
    assert not erc_violations
    assert not native['violations'] and not native['schematic_parity']
    result['sides'][side]={'ERC_violations':len(erc_violations),'DRC_reported_violations':len(native['violations']),'schematic_parity_issues':len(native['schematic_parity']),'unconnected_items':len(native['unconnected_items']),'ignored_DRC_categories':native['ignored_checks'],'pad_memberships_verified':checked,'front_nano_pin1_right_pin13_left':True,'battery_pads_back':True,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [pcb,sch]},'tracks':sum(head(n)=='segment' for _,_,n in nodes(pcb.read_text()))}
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print({s:{k:v for k,v in d.items() if k in ['ERC_violations','DRC_reported_violations','unconnected_items','schematic_parity_issues','tracks']} for s,d in result['sides'].items()})
