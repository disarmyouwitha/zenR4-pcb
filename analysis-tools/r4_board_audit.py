"""Check layout net memberships against native schematic XML, ignoring NC nets."""
import json,xml.etree.ElementTree as E
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];OUT=BASE/'r4-layout'
result={}
for side in ['left','right']:
 xml=E.parse(OUT/f'checks/{side}.net.xml');want={}
 for net in xml.findall('.//nets/net'):
  members=frozenset((n.attrib['ref'],n.attrib['pin']) for n in net.findall('node') if not n.attrib['ref'].startswith('#'))
  if len(members)>1:want[net.attrib['name']]=members
 actual={}
 for p in json.loads((OUT/f'checks/{side}-routing-geometry.json').read_text())['pads']:
  if p['net']:actual.setdefault(p['net'],set()).add((p['ref'],p['pad']))
 unmatched={n:sorted(m) for n,m in want.items() if m not in [frozenset(a) for a in actual.values()]}
 result[side]={'schematic_net_memberships_checked':len(want),'mismatches':unmatched}
 assert not unmatched,unmatched
(OUT/'checks/net-membership-audit.json').write_text(json.dumps(result,indent=2));print(result)
