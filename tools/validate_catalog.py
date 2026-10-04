#!/usr/bin/env python3
"""Validate shared identities and approval pointers. Does not certify media QA."""
import json,re,sys
from pathlib import Path

def validate(root):
 r=json.loads((root/'catalog/registry.json').read_text());m=json.loads((root/'manifest.json').read_text())
 errors=[];ids=set();owned={};media={};records=r.get('revision_records',{})
 for a in m.get('finals',[])+m.get('clips',[]):
  k=a['id']
  if k in media: errors.append('Duplicate manifest asset: '+k)
  media[k]=a
 for c in r['concepts']:
  k=c.get('concept_id','')
  if not re.fullmatch(r'[A-Z]+-\d{3,}',k):errors.append('Invalid concept ID: '+k)
  if k in ids:errors.append('Duplicate concept ID: '+k)
  ids.add(k)
  for f in ('title','kind','collection','category'):
   if not c.get(f):errors.append(k+' missing '+f)
  if c.get('kind') not in ('ad','clip'):errors.append(k+' invalid kind')
  for a in c.get('assets',[]):
   if a in owned:errors.append('Asset assigned twice: '+a)
   owned[a]=k
   if a not in media:errors.append('Missing manifest asset: '+a)
  approved=c.get('approved_asset_id')
  if approved:
   rec=records.get(approved,{})
   if approved not in c.get('assets',[]):errors.append(k+' invalid approved pointer')
   if rec.get('status') not in ('Approved','Live'):errors.append(k+' approved pointer lacks approved record')
   proof=rec.get('approval') or {}
   if not all(proof.get(f) for f in ('by','at','sha256')):errors.append(k+' lacks approval evidence')
 for a in media:
  if a not in owned:errors.append('Unregistered manifest asset: '+a)
 for aid,v in records.items():
  if aid!=v.get('asset_id') or v.get('concept_id')!=owned.get(aid):errors.append('Revision identity mismatch: '+aid)
  for f in ('category','branch','revision','format','created_by','last_edited_by','created_at','sha256'):
   if not v.get(f):errors.append(aid+' missing '+f)
  if v.get('status') not in ('Inbox','Draft','Review','Approved','Live','Archived','Rejected'):errors.append(aid+' invalid status')
  if not isinstance(v.get('created_by'),str) or not v['created_by'].strip():errors.append(aid+' invalid creator tag')
  if not isinstance(v.get('last_edited_by'),str) or not v['last_edited_by'].strip():errors.append(aid+' invalid editor tag')
  if v.get('parent_asset_id') and v['parent_asset_id'] not in media:errors.append(aid+' missing parent asset')
  if v.get('status')=='Live' and not v.get('live_platform_ids'):errors.append(aid+' lacks live platform IDs')
 return errors
if __name__=='__main__':
 root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
 e=validate(root)
 print('\n'.join(e) if e else 'PASS: catalog identities and approval references are consistent. Media QA is separate.')
 sys.exit(bool(e))
