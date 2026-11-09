"""Generate unrouted Zen R4 nice!nano electrical review sheets and pin contracts."""
import json
import re
import sys
import uuid
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'zen-r4-review'
FW = BASE.parent / 'zmk-javelin-steno-browser-dict'
LIB = Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols')
sys.path.insert(0, str(BASE / 'analysis-tools/python'))
from kiutils.utils import sexpr

def children(obj, key):
    return [x for x in obj if isinstance(x, list) and x and x[0] == key]

def read_dts(build):
    return (FW / 'build' / build / 'zephyr/zephyr.dts').read_text()

def array(dts, name, controller='pro_micro'):
    line = re.search(r'\b'+re.escape(name)+r' = (.*);', dts)[1]
    return [int(n, 16) for n in re.findall(r'&'+controller+r' (0x[\da-f]+)', line)]

left = read_dts('main-left-clean')
prototype_right = read_dts('main-right-nice-view')
row_names = [f'ROW{i}' for i in range(4)]
col_names = [f'COL{i}' for i in range(6)]
matrix = dict(zip(row_names + col_names, array(left,'row-gpios') + array(left,'col-gpios')))
assert list(matrix.values()) == [8,9,21,20,19,18,15,14,0,1]
maps = {'left': matrix, 'right': matrix}
pgpio = {int(n,16):f'P{port}.{int(bit,16):02}' for n,port,bit in
         re.findall(r'< (0x[\da-f]+) 0x0 &gpio([01]) (0x[\da-f]+) 0x0 >',
                    re.search(r'\bgpio-map = (.*);', left)[1])}
assert len(pgpio)==18
qspi = {'FLASH_CS_N':2,'FLASH_CLK':4,'FLASH_IO0':5,'FLASH_IO1':6,'FLASH_IO2':7,'FLASH_IO3':3}
display = {'VIEW_CS_ACTIVE_HIGH':4,'VIEW_MOSI':2,'VIEW_SCK':3}
assert set(qspi.values()).isdisjoint(maps['left'].values())
assert set(display.values()).isdisjoint(maps['right'].values())
assert 'cs-gpios = < &pro_micro 0x0 0x0 >;' in prototype_right
assert 'psels = < 0x4000014 >, < 0x5000011 >, < 0x6000019 >;' in prototype_right
qspi_block = left.split('qspi_probe_default:',1)[1].split('qspi_probe_sleep:',1)[0]
psel = [int(n,16) for match in re.findall(r'psels = (.*);', qspi_block)
        for n in re.findall(r'0x[0-9a-f]+',match)]
# nRF pinctrl PSEL encodes the physical pin in the low nine bits.
expected_qspi = [qspi[k] for k in ['FLASH_CS_N','FLASH_CLK','FLASH_IO0','FLASH_IO1','FLASH_IO2','FLASH_IO3']]
physical = [32*int(pgpio[d][1]) + int(pgpio[d][3:]) for d in expected_qspi]
assert [n & 0x1ff for n in psel] == physical, psel
assert 'flash-power-gpios = < &gpio0 0xd 0x0 >;' in left

banks = [[1,0,None,None,2,3,4,5,6,7,8,9],
         [None,None,None,None,21,20,19,18,15,14,16,10]]
# Component-face view, USB at top: 12 top-to-bottom contacts per bank.
specials = {3:('GND','GND'),4:('GND','GND'),
            13:('RAW/B+','BAT_SW'),14:('GND','GND'),
            15:('RESET','RESET_N'),16:('VCC','3V3_SW')}
module_pads = {d:i for i,d in enumerate(sum(banks,[]),1) if d is not None}
assert set(module_pads)==set(pgpio)
assert set(specials) == set(range(1,25))-set(module_pads.values())
flash_pads = {1:'FLASH_CS_N',2:'FLASH_IO1',3:'FLASH_IO2',4:'GND',
              5:'FLASH_IO0',6:'FLASH_CLK',7:'FLASH_IO3',8:'3V3_SW'}

nordic = next(s for s in children(sexpr.parse_sexp((LIB/'MCU_Nordic.kicad_sym').read_text()),'symbol') if s[1]=='nRF52840')
balls = {}
for sub in children(nordic,'symbol'):
    for pin in children(sub,'pin'):
        name = children(pin,'name')[0][1]
        gpio = re.search(r'P[01]\.\d\d',name)
        if gpio:
            balls[gpio[0]] = str(children(pin,'number')[0][1])
assert len(balls)==48 and balls['P0.22']=='AD18' and balls['P1.00']=='AD22', balls

def signal(d):
    return {'edge_label':f'D{d}','gpio':pgpio[d],
            'review_U1_pad':module_pads[d],'QIAA_ball':balls[pgpio[d]]}

contract = {
    'firmware_baseline':'cb3ccc8720a496fba8d877784345c6b120a0b999',
    'status':'schematic review; no layout, routing, fabrication or hardware fit signoff',
    'left_matrix':{n:signal(d) for n,d in maps['left'].items()},
    'left_qspi':{n:{**signal(d),'U2_pad':next(k for k,v in flash_pads.items() if v==n)} for n,d in qspi.items()},
    'left_qspi_supply':{'U1_edge_VCC_pad':16,'U2_VCC_pad':8,'U2_GND_pad':4,'net':'3V3_SW',
                        'module_internal_control':'P0.13 (not a carrier connection)',
                        'integrated_enable_candidate':{'gpio':'P0.13','QIAA_ball':balls['P0.13'],
                           'note':'Dedicated switched regulated 3.3 V, enable polarity to match selected switch and firmware.'}},
    'right_matrix':{n:signal(d) for n,d in maps['right'].items()},
    'right_display_reservation_only':{n:signal(d) for n,d in display.items()},
    'display_in_module_schematic':False,
    'mechanical_plan':{
        'original_v2_PCB_thickness_mm_user_measured':1.65,
        'replacement_thickness':'not selected; no requirement to go thinner',
        'viewing_window_mm_user_measured':[22.46,14.0],
        'original_PCB_openings':'battery only; no display cutout',
        'controller_mount':'backside on socket/component side, edge contacts only',
        'socket_and_case_fit':'user confirms Typeractive Choc sockets clear original base and case closes after PCB boss reliefs',
        'controller_fit':'user confirms underside nice!nano fits with modified plastic base',
        'custom_geometry':'Zen thumb centers, mount bosses and perimeter reliefs; Typeractive main grid reference',
        'plastic_base':'redesign permitted for controller, battery and optional display clearance',
        'optional_display':'cropped view acceptable; finalize recessed placement and solder access before adding footprint',
        'status':'physical dry-fit evidence accepted; final manufacturing stack and PCB layout remain unfinished'
    },
    'column_convention':{'left':'outside to seam','right':'outside to seam'},
    'right_firmware_scan':{'columns':col_names[::-1],'global_col_offset':6,
                           'thumb_scan_cells':['R3C0','R3C1','R3C2']},
    'populated_thumb_cells':{'left':['R3C3','R3C4','R3C5'],'right':['R3C3','R3C4','R3C5']},
    'integrated_candidate':{'package':'nRF52840-QIAA aQFN73', 'display_spi':'right SPIM0 candidate; no routed display',
                            'board_definition':'not made; clock, supply, RF, USB and bootloader review required'}
}
(OUT/'gpio-contract.json').write_text(json.dumps(contract,indent=2)+'\n')
def gpio_array(names, pull):
    flags = '(GPIO_ACTIVE_HIGH | GPIO_PULL_DOWN)' if pull else 'GPIO_ACTIVE_HIGH'
    return ',\n        '.join(f'<&pro_micro {maps["right"][n]} {flags}>' for n in names)
(OUT/'zen-r4-right-matrix-review.overlay').write_text(f'''/* Review overlay for nice_nano//zmk + corne_right at the pinned baseline.
 * Both PCBs use the tested left pinout, with C0 at the outside on each half.
 * ZMK scans the right columns seam to outside, so reverse the PCB net order.
 * No display enabled. D2, D3 and D4 are reserved in the pin contract.
 */
#include <zephyr/dt-bindings/gpio/gpio.h>

&kscan0 {{
    diode-direction = "col2row";
    row-gpios = {gpio_array(row_names, True)};
    col-gpios = {gpio_array(col_names[::-1], False)};
}};

&pro_micro_i2c {{ status = "disabled"; }};
&uart0 {{ status = "disabled"; }};
&spi1 {{ status = "disabled"; }};
/ {{
    chosen {{
        /delete-property/ zephyr,display;
    }};
}};
''')
(OUT/'zen-r4-right-display-review.overlay').write_text(f'''/* Build check only: use corne_right nice_view_adapter nice_view with the
 * baseline right-nice-view.conf. Do not use on the stock Ultralight.
 * Use this overlay by itself; it includes the custom right matrix.
 */
#include "zen-r4-right-matrix-review.overlay"

&nice_view_spi {{
    cs-gpios = <&pro_micro {display["VIEW_CS_ACTIVE_HIGH"]} GPIO_ACTIVE_HIGH>;
}};

/ {{
    chosen {{
        zephyr,display = &nice_view;
    }};
    behaviors {{
        zrst: zrst {{
            compatible = "zmk,behavior-zen-r4-status";
            #binding-cells = <2>;
        }};
    }};
}};
''')

def uid(s):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'zen-r4-review/'+s))
def q(s):
    return json.dumps(str(s), ensure_ascii=False)
def xy(x,y):
    return f'{x:.4f} {y:.4f}'
def effects(size=1, extra=''):
    return f'(effects (font (size {size} {size})) {extra})'
def prop(name,value,x=0,y=0,hide=False):
    return f'(property {q(name)} {q(value)} (at {xy(x,y)} 0) {effects(extra="hide" if hide else "")})'
def pin(num,name,x,y,angle,length=2.54,kind='passive'):
    return (f'(pin {kind} line (at {xy(x,y)} {angle}) (length {length})'
            f' (name {q(name)} {effects(.9)}) (number {q(num)} {effects(.9)}))')
def line(points):
    return '(polyline (pts '+''.join(f'(xy {xy(*p)})' for p in points)+') (stroke (width 0.25) (type default)) (fill (type none)))'
def box(x,y):
    return f'(rectangle (start {-x} {y}) (end {x} {-y}) (stroke (width 0.25) (type default)) (fill (type background)))'

symbols = {}
def define(name,ref,graphics,pins,hide_names=False,on_board=True):
    desc = f'(pin_names (offset 0.7) {"hide" if hide_names else ""})'
    if hide_names:
        desc += ' (pin_numbers hide)'
    yn = 'yes' if on_board else 'no'
    symbols[name] = (f'(symbol "R4Review:{name}" {desc} (in_bom {yn}) (on_board {yn}) '
                     + prop('Reference',ref)+prop('Value',name)
                     + f'(symbol "{name}_0_1" {graphics}) (symbol "{name}_1_1" {"".join(pins)}))')

# All listed contacts are at module edges; numbers are our explicit review convention.
m_pins = []
for i,d in enumerate(sum(banks,[]),1):
    name = specials[i][0] if d is None else f'D{d} {pgpio[d]}'
    m_pins.append(pin(i,name,-22.86 if i<=12 else 22.86,
                      13.97-2.54*((i-1)%12),0 if i<=12 else 180,
                      kind='power_out' if i==16 else 'passive'))
define('Nano_v2_edge','U',box(20.32,16.51),m_pins)
two = [pin(1,'1',-5.08,0,0),pin(2,'2',5.08,0,180)]
define('Switch','SW',line([(-2.54,0),(2.54,1.27)]),two,True)
define('Diode','D',line([(-1.27,-1.27),(1.27,0),(-1.27,1.27),(-1.27,-1.27)])+
       line([(1.27,-1.27),(1.27,1.27)])+line([(-2.54,0),(-1.27,0)])+line([(1.27,0),(2.54,0)]),
       [pin(2,'A',-5.08,0,0),pin(1,'K',5.08,0,180)],True)
define('Battery','J',box(2.54,3.81),
       [pin(1,'+',-5.08,1.27,0),pin(2,'-',-5.08,-1.27,0)])
define('Resistor','R',box(2.54,.85),two,True)
define('Capacitor','C',line([(-2.54,0),(-.65,0)])+line([(-.65,-1.45),(-.65,1.45)])+
       line([(.65,-1.45),(.65,1.45)])+line([(.65,0),(2.54,0)]),two,True)
define('Ground_ref','PWR',line([(0,0),(0,2.54),(-1.25,3.1),(0,3.65),(1.25,3.1),(0,2.54)]),
       [pin(1,'REF',0,0,90,0,kind='power_out')],True,False)
flash_names={1:'CS#',2:'IO1',3:'IO2',4:'GND',5:'IO0',6:'CLK',7:'IO3',8:'VCC'}
define('W25Q128JV','U',box(12.7,7.62),
       [pin(i,flash_names[i],-15.24 if i<=4 else 15.24, 3.81-2.54*((i-1)%4),
            0 if i<=4 else 180,kind=('power_in' if i in (4,8) else 'input' if i in (1,6) else 'bidirectional'))
        for i in range(1,9)])
(OUT/'r4-review.kicad_sym').write_text('(kicad_symbol_lib (version 20231120) (generator kicad_symbol_editor)\n'+
    '\n'.join(s.replace('"R4Review:','"',1) for s in symbols.values())+'\n)\n')
(OUT/'sym-lib-table').write_text('(sym_lib_table (version 7) (lib (name "R4Review") (type "KiCad") (uri "${KIPRJMOD}/r4-review.kicad_sym") (options "") (descr "")))\n')

def generate(side):
    name = f'zen-r4-{side}-nano'
    root = uid(name)
    parts, refs, used, net_expect = [], [], set(), {}
    def sym(ref,tag,value,x,y,foot='',offset=3.81,on_board=True):
        ident = uid(name+'/'+ref)
        yn='yes' if on_board else 'no'
        parts.append(f'(symbol (lib_id "R4Review:{tag}") (at {xy(x,y)} 0) (unit 1)'
                     f' (in_bom {yn}) (on_board {yn}) (dnp no) (uuid {ident})'
                     +prop('Reference',ref,x,y-offset,hide=not on_board)+prop('Value',value,x,y-offset+1.4,hide=not on_board)
                     +prop('Footprint',foot,x,y,True)
                     +f'(instances (project {q(name)} (path "/{root}" (reference {q(ref)}) (unit 1)))))')
        used.add(tag)
    def wire(x,y,xx,yy):
        parts.append(f'(wire (pts (xy {xy(x,y)}) (xy {xy(xx,yy)})) (stroke (width 0) (type default))'
                     f' (uuid {uid(name+str((x,y,xx,yy,len(parts))))}))')
    def label(net,x,y,angle=0):
        parts.append(f'(label {q(net)} (at {xy(x,y)} {angle}) {effects(.92,"(justify left bottom)")}'
                     f' (uuid {uid(name+net+str((x,y,len(parts))))}))')
    def term(ref,num,net,x,y,dx):
        net_expect[f'{ref}:{num}']=net
        wire(x,y,x+dx,y);label(net,x+dx,y,0 if dx<0 else 180)
    def nc(x,y):
        parts.append(f'(no_connect (at {xy(x,y)}) (uuid {uid(name+str((x,y)))}))')
    def note(s,x,y,size=1.25):
        parts.append(f'(text {q(s)} (at {xy(x,y)} 0) {effects(size,"(justify left)")} (uuid {uid(name+s)}))')

    for row in range(4):
        cols=range(6) if row<3 else range(3,6)
        for index,c in enumerate(cols if side=='left' else reversed(cols)):
            i=row*6+index+1 if row<3 else 19+index
            x=31.75+(c if side=='left' else 5-c)*43.18;y=57.15+row*35.56
            sr,dr=f'SW{i}',f'D{i}'
            sym(sr,'Switch','Choc socket',x,y)
            sym(dr,'Diode','1N4148W',x+12.7,y,'Diode_SMD:D_SOD-123')
            wire(x+5.08,y,x+7.62,y)
            term(sr,1,f'COL{c}',x-5.08,y,-6.35)
            term(dr,1,f'ROW{row}',x+17.78,y,5.08)
            net_expect[f'{sr}:2']=net_expect[f'{dr}:2']=f'internal_pair_{i}'
    x,y=340.36,74.93
    sym('U1','Nano_v2_edge','nice!nano v2 (edge only)',x,y,offset=22.86)
    signals={d:n for n,d in (maps[side]|(qspi if side=='left' else {})).items()}
    for num,d in enumerate(sum(banks,[]),1):
        pinx=x+(-22.86 if num<=12 else 22.86)
        piny=y-13.97+2.54*((num-1)%12)
        net=specials[num][1] if d is None else signals.get(d)
        # Switched VCC is unused on the right without the display.
        if net and not (side=='right' and num==16):
            term('U1',num,net,pinx,piny,-10.16 if num<=12 else 10.16)
        else:
            nc(pinx,piny)
    for ref,val,x,y,leftnet,rightnet in [
        ('SW22','Battery switch',340.36,124.46,'BAT_RAW','BAT_SW'),
        ('SW23','Reset switch',340.36,142.24,'RESET_N','GND'),
    ]:
        sym(ref,'Switch',val,x,y)
        term(ref,1,leftnet,x-5.08,y,-7.62)
        term(ref,2,rightnet,x+5.08,y,7.62)
    sym('J1','Battery','1S LiPo connection',340.36,165.1,offset=7.62)
    term('J1',1,'BAT_RAW',335.28,163.83,-7.62)
    term('J1',2,'GND',335.28,166.37,-7.62)
    sym('#FLG01','Ground_ref','PWR_FLAG',373.38,166.37,on_board=False)
    term('#FLG01',1,'GND',373.38,166.37,-5.08)

    if side=='left':
        fx,fy=340.36,200.66
        sym('U2','W25Q128JV','W25Q128JVSIQ (candidate)',fx,fy,
            'Package_SO:SOIC-8_5.3x5.3mm_P1.27mm',offset=13.97)
        for n,net in flash_pads.items():
            term('U2',n,net,fx+(-15.24 if n<=4 else 15.24),fy-3.81+2.54*((n-1)%4),-12.7 if n<=4 else 12.7)
        sym('C1','Capacitor','100 nF',330.2,220.98,'Capacitor_SMD:C_0603_1608Metric')
        term('C1',1,'3V3_SW',325.12,220.98,-10.16);term('C1',2,'GND',335.28,220.98,7.62)
        sym('R1','Resistor','10k',330.2,233.68,'Resistor_SMD:R_0603_1608Metric')
        term('R1',1,'3V3_SW',325.12,233.68,-10.16);term('R1',2,'FLASH_CS_N',335.28,233.68,7.62)
    note(f'Zen R4 — {side} electrical review / before layout',25.4,25.4,2.2)
    note('21 Choc switches; column drives switch then diode anode; diode stripe toward row.',25.4,40.64)
    note('C0 is outside; C5 is at the seam on both halves.',25.4,185.42)
    note('Tested left matrix and QSPI assignments kept. IO2 and IO3 are data; do not strap them.',25.4,195.58) if side=='left' else note('Same matrix pins as left. D2/D3/D4 are free for optional display.',25.4,195.58)
    note('No left display.' if side=='left' else 'Right display placement pending: CS D4, MOSI D2, SCK D3. No footprint yet.',25.4,205.74)
    note('Backside edge-contact nano; modified plastic base. Zen thumb centers and boss reliefs.',25.4,215.9)
    note('V2 PCB measured 1.65 mm; replacement thickness pending. Physical dry fit reported.',25.4,246.38)
    note('3V3_SW is the module edge VCC; P0.13 controls it inside the module.',25.4,226.06) if side=='left' else None
    note('Draft flash decoupling and CS pull-up require placement and power-on review.',25.4,236.22) if side=='left' else None
    (OUT/f'{name}.kicad_sch').write_text(f'(kicad_sch (version 20250114) (generator eeschema) (uuid {root})'
        f' (paper "A3") (title_block (title {q(name)}) (rev "electrical review"))\n(lib_symbols\n'
        +'\n'.join(symbols[s] for s in sorted(used))+')\n'+'\n'.join(parts)
        +'\n(sheet_instances (path "/" (page "1"))))\n')
    return net_expect

expected = {s:generate(s) for s in maps}
(OUT/'expected-schematic-nets.json').write_text(json.dumps(expected,indent=2)+'\n')
print('Generated two review sheets and two right firmware review overlays; no display footprint or routes.')
