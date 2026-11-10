"""Small text helpers for Draft Corne; no pcbnew GUI runtime required."""
import re,uuid,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'projects/choc-corne-flash/draft-c'
def uid():return str(uuid.uuid4())
def q(v):return json.dumps(str(v))
def nodes(text):
 depth=0;quoted=False;escape=False;start=None
 for i,c in enumerate(text):
  if quoted:
   if escape:escape=False
   elif c=='\\':escape=True
   elif c=='"':quoted=False
   continue
  if c=='"':quoted=True;continue
  if c=='(':
   if depth==1:start=i
   depth+=1
  elif c==')':
   depth-=1
   if depth==1 and start is not None:yield start,i+1,text[start:i+1];start=None

def head(n):return re.match(r'\(\s*([^\s()]+)',n)[1]
def prop(key,value,x=0,y=0):return f'(property {q(key)} {q(value)} (at {x} {y} 0) (effects (font (size 1 1)) hide))'
def replace_top(text,replacements):
 for start,end,new in sorted(replacements,reverse=True):text=text[:start]+new+text[end:]
 return text
