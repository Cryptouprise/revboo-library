/* RevBoo private-import analytics. Pure functions also used by local tests. */
const RevBooMetrics=(()=>{
const fields=['spend','impressions','views_3s','thruplays','outbound_clicks','landing_page_views','meta_leads','qualified_leads','booked_calls','held_calls','new_customers','collected_revenue'];
function validate(d,assetIDs){
 if(d.schema_version!==1||!Array.isArray(d.rows))throw Error('Use schema_version 1 with rows array.');
 for(const f of ['currency','timezone','attribution','imported_at','source_updated_at'])if(typeof d[f]!=='string'||!d[f].trim()||d[f].includes('SET_ACTUAL'))throw Error('Missing or placeholder '+f);
 if(!/^[A-Z]{3}$/.test(d.currency))throw Error('Use one ISO currency code.');
 if(!Number.isFinite(Date.parse(d.imported_at))||!Number.isFinite(Date.parse(d.source_updated_at)))throw Error('Invalid import/source timestamp.');
 if(d.crm_mature_through!==null&&!dateOK(d.crm_mature_through))throw Error('Invalid maturity date.');
 if(typeof d.crm_deduped!=='boolean')throw Error('crm_deduped must be true or false.');
 const seen=new Set(),mapping=new Map();
 d.rows.forEach((r,i)=>{
  if(!dateOK(r.date))throw Error('Row '+(i+1)+': invalid date.');
  for(const f of ['account_id','ad_id','asset_id','operated_by'])if(typeof r[f]!=='string'||!r[f].trim())throw Error('Row '+(i+1)+': missing '+f);
  if(!assetIDs.has(r.asset_id))throw Error('Unknown creative '+r.asset_id+'. Register it first.');
  if(!['direct','sequence'].includes(r.strategy)||!['prospecting','retargeting'].includes(r.stage))throw Error('Invalid strategy/stage.');
  const key=JSON.stringify([r.account_id,r.ad_id,r.date]);if(seen.has(key))throw Error('Duplicate account/ad/date. Use ad-level totals, not overlapping breakdowns.');seen.add(key);
  const ad=JSON.stringify([r.account_id,r.ad_id]);if(mapping.has(ad)&&mapping.get(ad)!==r.asset_id)throw Error('An ad ID maps to multiple creatives. Reconcile before importing.');mapping.set(ad,r.asset_id);
  fields.forEach(f=>{if(!(f in r))throw Error('Missing field '+f+'; use null for unknown.');if(r[f]!==null&&(typeof r[f]!=='number'||!Number.isFinite(r[f])||r[f]<0))throw Error('Invalid nonnegative number for '+f);if(r[f]!==null&&!['spend','collected_revenue'].includes(f)&&!Number.isInteger(r[f]))throw Error('Count must be an integer: '+f)});
 });return d;
}
function dateOK(s){if(typeof s!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(s))return false;const d=new Date(s+'T00:00:00Z');return Number.isFinite(d.getTime())&&d.toISOString().slice(0,10)===s}
function sum(rows,f){return !rows.length||rows.some(r=>r[f]===null||r[f]===undefined)?null:rows.reduce((a,r)=>a+r[f],0)}
const divide=(a,b)=>a===null||b===null||b===0?null:a/b;
function aggregate(rows,dedup){let x={};fields.forEach(f=>x[f]=sum(rows,f));if(!dedup)['qualified_leads','booked_calls','held_calls','new_customers','collected_revenue'].forEach(f=>x[f]=null);return {...x,cpm:divide(x.spend,x.impressions)===null?null:divide(x.spend,x.impressions)*1000,hook:divide(x.views_3s,x.impressions),hold:divide(x.thruplays,x.views_3s),ctr:divide(x.outbound_clicks,x.impressions),arrival:divide(x.landing_page_views,x.outbound_clicks),cpql:divide(x.spend,x.qualified_leads),cac:divide(x.spend,x.new_customers),show:divide(x.held_calls,x.booked_calls),close:divide(x.new_customers,x.held_calls),cash_multiple:divide(x.collected_revenue,x.spend)}}
return {validate,aggregate,fields,dateOK};})();
if(typeof module!=='undefined')module.exports=RevBooMetrics;
