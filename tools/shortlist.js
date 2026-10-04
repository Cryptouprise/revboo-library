/* Portable favorites: exact versions, user notes, explicit removals. No campaign actions. */
(function(root){
 const SCHEMA=1,KEY='revboo-shortlist-v1';
 function validate(raw,assets){
  if(!raw||raw.schema_version!==SCHEMA||!Array.isArray(raw.entries))throw Error('Use a RevBoo shortlist JSON (schema 1).');
  const refs=new Map(assets.map(a=>[a.id,a])),seen=new Set();
  if(raw.entries.length>assets.length)throw Error('Too many shortlist entries.');
  const entries=raw.entries.map(e=>{
   if(!e||typeof e.concept_id!=='string'||seen.has(e.concept_id))throw Error('Each concept must appear once.');
   seen.add(e.concept_id);const a=refs.get(e.asset_id);
   if(!a||a.concept_id!==e.concept_id)throw Error('Unknown or mismatched version: '+String(e.asset_id));
   if(typeof e.starred!=='boolean'||!Number.isInteger(e.rank)||e.rank<1)throw Error('Invalid star or order.');
   if(typeof e.note!=='string'||e.note.length>2000)throw Error('Notes must be text, up to 2,000 characters.');
   if(typeof e.updated_at!=='string'||!Number.isFinite(Date.parse(e.updated_at)))throw Error('A valid update timestamp is required.');
   return {concept_id:e.concept_id,asset_id:e.asset_id,starred:e.starred,rank:e.rank,note:e.note,updated_at:e.updated_at,updated_by:typeof e.updated_by==='string'?e.updated_by.slice(0,80):'Human'};
  });
  return {schema_version:SCHEMA,updated_at:raw.updated_at||null,updated_by:raw.updated_by||'Human',entries};
 }
 function merge(shared,local){
  const map=new Map((shared?.entries||[]).map(e=>[e.concept_id,{...e}]));
  (local?.entries||[]).forEach(e=>{const old=map.get(e.concept_id);if(!old||Date.parse(e.updated_at)>=Date.parse(old.updated_at))map.set(e.concept_id,{...e})});
  return [...map.values()];
 }
 function ordered(entries){return entries.filter(e=>e.starred).sort((a,b)=>a.rank-b.rank||a.concept_id.localeCompare(b.concept_id))}
 root.RevBooShortlist={SCHEMA,KEY,validate,merge,ordered};
})(typeof window!=='undefined'?window:globalThis);
