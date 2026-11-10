"""Bundle Draft C and handoff with local CAD libraries and attribution."""
from pathlib import Path
import zipfile,shutil
from draft_c_common import ROOT,OUT
paths=[ROOT/'ATTRIBUTION.md',ROOT/'README.md',ROOT/'AGENTS.md',ROOT/'docs/CHATGPT-HANDOFF.md',ROOT/'docs/START-HERE.md',OUT.parent/'README.md',OUT.parent/'pin-plan.json']
paths+=list((ROOT/'LICENSES').rglob('*'))
paths+=list((OUT.parent/'reference').rglob('*'))
paths+=list(OUT.rglob('*'))
paths+=list((ROOT/'analysis-tools').glob('draft_c_*.py'))
paths += [ROOT/'r4-layout/evidence/crkbd-LICENSE-MIT',ROOT/'r4-layout/evidence/kbd-LICENSE']
dest=ROOT/'docs/draft-corne.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(set(paths)):
  if p.is_file() and p.suffix not in ['.kicad_prl','.lck','.bak'] and '__pycache__' not in p.parts and p.name!='.DS_Store':z.write(p,p.relative_to(ROOT))
shutil.copy2(dest,ROOT.parent/'draft-corne.zip')
with zipfile.ZipFile(dest) as z:assert z.testzip() is None
print(dest,'valid archive',dest.stat().st_size,'bytes')
