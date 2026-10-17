// Two-section library: finals.html (approved to run) and mockups.html (drafts, mockups, rejected, B-roll).
// Data: catalog/sections.json (tools/make_sections.py). manifest.json is also read so anything added after the
// last make_sections run still shows up (as a draft under its brand) instead of disappearing.
(()=>{
const VIEW=document.body.dataset.view; // 'finals' | 'mockups'
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fmt=s=>{s=Math.round(s||0);return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')};
const dt=x=>String(x.datetime||'').slice(0,19);
const byNew=(a,b)=>dt(b).localeCompare(dt(a));
const SL={final:'FINAL',draft:'DRAFT',rejected:'REJECTED'};
const schip=s=>`<span class="chip s-${s}">${SL[s]||esc(s).toUpperCase()}</span>`;
const aspect=x=>x.width&&x.height?({'1080x1920':'9:16','720x1280':'9:16','1080x1350':'4:5','720x900':'4:5','1920x1080':'16:9','1280x720':'16:9'}[x.width+'x'+x.height]||x.width+'×'+x.height):'';
const touch=matchMedia('(hover:none)').matches;
Promise.all([fetch('catalog/sections.json',{cache:'no-cache'}).then(r=>r.json()),
             fetch('manifest.json',{cache:'no-cache'}).then(r=>r.json()).catch(()=>({finals:[],clips:[]}))]).then(([S,M])=>{
  const items=S.items.slice();
  const have=new Set(items.map(x=>x.id));
  [['ad','finals'],['clip','clips']].forEach(([kind,k])=>(M[k]||[]).forEach(e=>{if(have.has(e.id))return;
    items.push({id:e.id,kind,client:e.brand||'Generic/Other',section:'mockups',status:e.status==='rejected'?'rejected':'draft',folder:'New (not sorted yet)',
      concept:e.group||e.name||e.title,title:e.title||e.name,version:e.version||'',date:e.date,datetime:e.datetime,duration:e.duration,width:e.width,height:e.height,
      video:e.video,poster:e.poster,note:e.note||'',categories:e.categories,used_in:e.used_in})}));
  const mine=items.filter(x=>x.section===VIEW);
  const order=S.client_order||[];
  const clients=[...new Set([...order,...mine.map(x=>x.client)])].filter(c=>mine.some(x=>x.client===c));
  document.getElementById('nF').textContent=items.filter(x=>x.section==='finals').length;
  document.getElementById('nM').textContent=items.filter(x=>x.section==='mockups').length;
  const tabs=document.getElementById('tabs');
  let st='all',q='',kindF='all';
  const cur=()=>{const h=decodeURIComponent((location.hash.match(/client=([^&]+)/)||[])[1]||'All');return clients.includes(h)?h:'All'};
  function drawTabs(c){tabs.innerHTML=['All',...clients].map(x=>`<a href="#client=${encodeURIComponent(x)}" class="${x===c?'on':''}">${esc(x)}<small>${x==='All'?mine.length:mine.filter(i=>i.client===x).length}</small></a>`).join('')}
  function wire(root){
    root.querySelectorAll('.v button').forEach(b=>b.onclick=()=>{const card=b.closest('.card'),v=card.querySelector('video');
      v.poster=b.dataset.p;v.src=b.dataset.v;v.style.aspectRatio=b.dataset.a;card.querySelectorAll('.v button').forEach(x=>x.classList.toggle('on',x===b));
      const n=card.querySelector('.note.cur');if(n)n.textContent=b.dataset.n||'';v.play().catch(()=>{})});
    root.querySelectorAll('.clip video').forEach(v=>{v.addEventListener('mouseenter',()=>{if(!touch)v.play().catch(()=>{})});
      v.addEventListener('mouseleave',()=>{if(!touch){v.pause();v.currentTime=0}});v.addEventListener('click',()=>v.paused?v.play().catch(()=>{}):v.pause())});
  }
  const vbtn=(x,on)=>`<button class="${on?'on':''}" data-v="${esc(x.video)}" data-p="${esc(x.poster)}" data-a="${x.width&&x.height?x.width+'/'+x.height:'9/16'}" data-n="${esc(x.note)}">▶</button>`;
  // ---------- FINALS ----------
  function finalCard(g){
    g.sort((a,b)=>(a.rank?0:1)-(b.rank?0:1)||(S.finals_rank.find(r=>r.rank===a.rank)?.asset_ids||[]).indexOf(a.id)-(S.finals_rank.find(r=>r.rank===b.rank)?.asset_ids||[]).indexOf(b.id));
    const f=g[0],rank=g.find(x=>x.rank)?.rank;
    return `<div class="card final" id="final-${esc(f.concept_id||f.id)}">
      <video controls playsinline preload="metadata" style="aspect-ratio:${f.width}/${f.height}" poster="${esc(f.poster)}" src="${esc(f.video)}"></video>
      <h4>${rank?`<span class="rk">#${rank}</span>`:''}${esc(f.concept)}</h4>
      <div>${schip('final')}<span class="chip">${esc(f.concept_id||'')}</span><span class="chip tag">${esc(f.client)}</span></div>
      <div class="meta">Approved by ${esc(f.approved_by||'Chase Fowler')} · ${esc((f.approved_at||'').slice(0,10)?new Date(f.approved_at).toLocaleString('en-US',{timeZone:'America/Denver',month:'short',day:'numeric',year:'numeric',hour:'numeric',minute:'2-digit'})+' MT':'')} · file dated ${esc(f.date)}</div>
      <div class="vers">${g.map((x,i)=>`<div class="v">${vbtn(x,!i)}<b>${esc(aspect(x))}</b>${x.rank?'':'<span class="chip">original cut (also approved)</span>'}<code style="font-size:11px;color:#aaa">${esc(x.id)}</code> · ${fmt(x.duration)} · ${esc(x.date)} · <a class="dl" href="${esc(x.video)}" download>⬇</a></div>`).join('')}</div>
    </div>`}
  function drawFinals(c){
    const el=document.getElementById('body');
    const cl=c==='All'?clients:[c];
    el.innerHTML=cl.map(cn=>{const list=mine.filter(x=>x.client===cn);const fam={};list.forEach(x=>(fam[x.concept_id||x.concept]??=[]).push(x));
      const gs=Object.values(fam).sort((a,b)=>(Math.min(...a.map(x=>x.rank||99)))-(Math.min(...b.map(x=>x.rank||99))));
      return `<section class="client"><h2>${esc(cn)}<small>${gs.length} approved ads · ${list.length} files</small></h2><p class="cnote">${esc((S.client_notes||{})[cn]||'')}</p><div class="grid">${gs.map(finalCard).join('')}</div></section>`}).join('')||'<p class="empty">Nothing approved here yet.</p>';
    wire(el)}
  // ---------- MOCKUPS ----------
  const match=x=>(st==='all'||x.status===st)&&(kindF==='all'||(kindF==='clip')===(x.kind==='clip'))&&
     (!q||[x.title,x.concept,x.folder,x.version,x.note,x.id,x.concept_id,x.client,...(x.categories||[])].join(' ').toLowerCase().includes(q));
  function conceptCard(g){
    g.sort(byNew);const f=g[0];
    if(f.kind==='placeholder')return `<div class="card"><div class="ph">🛈 ${esc(f.note)}<br><br><a href="${esc(f.link)}" target="_blank" rel="noopener">Open the concepts doc →</a></div>
      <h4>${esc(f.concept)}</h4><div>${schip(f.status)}<span class="chip">concept only</span></div><div class="meta">${esc(f.title)} · ${esc(f.version)} · ${esc(f.date)}</div></div>`;
    const rej=g.every(x=>x.status==='rejected');
    return `<div class="card${rej?' rej':''}"><video controls playsinline preload="none" style="aspect-ratio:${f.width&&f.height?f.width+'/'+f.height:'9/16'}" poster="${esc(f.poster)}" src="${esc(f.video)}"></video>
      <h4>${esc(f.concept)}${rej?' <span style="color:#ff9b9b">(rejected)</span>':''}</h4>
      <div><span class="chip tag">${esc(f.concept)}${rej?' (rejected)':''}</span>${f.concept_id?`<span class="chip">${esc(f.concept_id)}</span>`:''}<span class="chip">${g.length} version${g.length>1?'s':''}</span></div>
      <div class="note cur">${esc(f.note)}</div>
      <div class="vers">${g.map((x,i)=>`<div class="v">${vbtn(x,!i)}${schip(x.status)}<span>${esc(x.version||x.title)}</span>${aspect(x)?`<span class="meta" style="margin:0">${esc(aspect(x))}</span>`:''}<span class="meta" style="margin:0">· ${esc(x.date)} · ${fmt(x.duration)}</span><a class="dl" href="${esc(x.video)}" download>⬇</a></div>`).join('')}</div></div>`}
  const clipCard=x=>`<div class="clip"><video muted loop playsinline preload="none" poster="${esc(x.poster)}" src="${esc(x.video)}"></video><div class="i"><div class="nm">${esc(x.title)}</div>
     <div>${schip(x.status)}</div><div class="meta">${esc(x.date)} · ${fmt(x.duration)}</div>${(x.categories||[]).map(c=>`<span class="chip">${esc(c)}</span>`).join('')}
     <div class="meta">Used in: ${(x.used_in||[]).length?x.used_in.map(esc).join(', '):'not used yet'}</div>${x.note?`<div class="note">⚠ ${esc(x.note)}</div>`:''}<a class="dl" href="${esc(x.video)}" download>⬇ Download</a></div></div>`;
  function folderHTML(name,list){
    const isClips=list.every(x=>x.kind==='clip');
    const fam={};list.forEach(x=>(fam[x.concept]??=[]).push(x));
    const gs=Object.entries(fam).sort((a,b)=>byNew(a[1].slice().sort(byNew)[0],b[1].slice().sort(byNew)[0]));
    const counts=['draft','rejected'].map(s=>{const n=list.filter(x=>x.status===s).length;return n?`${n} ${s}`:''}).filter(Boolean).join(' · ');
    const tags=gs.filter(([k,g])=>g.every(x=>x.status==='rejected')).map(([k])=>`<span class="chip s-rejected">${esc(k)} (rejected)</span>`).join('');
    const open=!isClips||q||list.length<=12;
    return `<details class="folder"${open?' open':''}><summary><h3>${esc(name)}</h3><span class="cnt">${list.length} item${list.length>1?'s':''}${counts?' · '+counts:''}</span>${tags}</summary><div class="fbody">${
      isClips?gs.map(([k,g])=>`<div class="sub3">${esc(k)} (${g.length})</div><div class="clips">${g.sort(byNew).map(clipCard).join('')}</div>`).join('')
             :`<div class="grid">${gs.map(([k,g])=>conceptCard(g)).join('')}</div>`}</div></details>`}
  function drawMockups(c){
    const el=document.getElementById('body');
    const cl=c==='All'?clients:[c];
    const html=cl.map(cn=>{const list=mine.filter(x=>x.client===cn&&(x.kind==='placeholder'?(st==='all'||st==='draft')&&kindF!=='clip':true)&&(x.kind==='placeholder'?!q||match(x):match(x)));if(!list.length)return '';
      const fs={};list.forEach(x=>(fs[x.folder]??=[]).push(x));
      const fol=Object.entries(fs).sort((a,b)=>{const ca=a[1].every(x=>x.kind==='clip'),cb=b[1].every(x=>x.kind==='clip');if(ca!==cb)return ca?1:-1;
        return byNew(a[1].slice().sort(byNew)[0],b[1].slice().sort(byNew)[0])});
      return `<section class="client"><h2>${esc(cn)} <span style="color:var(--o)">›</span> Mockups<small>${list.filter(x=>x.kind!=='placeholder').length} items · ${fol.length} folders</small></h2><p class="cnote">${esc((S.client_notes||{})[cn]||'')}</p>${fol.map(([n,l])=>folderHTML(n,l)).join('')}</section>`}).join('');
    el.innerHTML=html||'<p class="empty">Nothing matches.</p>';wire(el)}
  function tools(){
    const t=document.getElementById('tools');if(!t)return;
    t.innerHTML=[['all','All statuses'],['draft','Drafts'],['rejected','Rejected']].map(([k,l])=>`<button data-s="${k}" class="${k===st?'on':''}">${l}</button>`).join('')+
      ' &nbsp; '+[['all','Ads + clips'],['ad','Ads only'],['clip','B-roll clips only']].map(([k,l])=>`<button data-k="${k}" class="${k===kindF?'on':''}">${l}</button>`).join('')+
      `<input id="q" type="search" placeholder="Search concept, version, note (e.g. planet, flagship, penguin)" value="${esc(q)}">`;
    t.querySelectorAll('button[data-s]').forEach(b=>b.onclick=()=>{st=b.dataset.s;tools();route()});
    t.querySelectorAll('button[data-k]').forEach(b=>b.onclick=()=>{kindF=b.dataset.k;tools();route()});
    const i=document.getElementById('q');i.oninput=e=>{q=e.target.value.toLowerCase();route()};
  }
  function route(){const c=cur();drawTabs(c);(VIEW==='finals'?drawFinals:drawMockups)(c);document.title=(c==='All'?'':c+' · ')+document.body.dataset.title}
  addEventListener('hashchange',route);tools();route();
  if(VIEW==='mockups'&&!document.activeElement?.id)0;
}).catch(e=>{document.getElementById('body').innerHTML='<p style="color:#f88">Could not load catalog/sections.json: '+esc(e)+'</p>'});
})();
