/* Spreads composed as inhabited places; all text remains live and searchable. */
function worldStage(family,side,body){
 const image={ocean:'ocean-inhabited-spread.png',village:'village-stair-spread.png',table:'architects-working-table.png'}[family];
 const alt={ocean:'An inhabited underwater room and passenger tram beside the volcanic Tenerife coast',village:'A stair linking modest cliffside homes, neighbours and a fisherman repairing a net',table:'Imagined architectural working table, with models, an island drawing and several participants'}[family];
 return `<div class="world-stage world-${family} world-side-${side}"><div class="world-image-window"><img src="assets/${image}" alt="${alt}" width="${family==='table'?1536:1470}" height="${family==='table'?1024:1070}"></div>${body}</div>`;
}
function worldSheet(key,title,family,side,body){addSheet(key,title,`world-page world-page-${family}`,worldStage(family,side,body));sheets.at(-1).designed=true;}
function oceanWorldBodies(a){return [
 worldStage('ocean',0,`<div class="world-heading"><small>OCEAN WORKSHOP / 02</small><h1>A ROOM IN<br>THE ATLANTIC</h1><em>Una stanza, non un impero.</em></div><div class="world-shaped"><span class="shape-occluder" aria-hidden="true"></span>${a.body.slice(0,1).map(p=>`<p>${p}</p>`).join('')}</div>`),
 worldStage('ocean',1,`<div class="world-bottom"><h2>THE EXTRAORDINARY<br><i>becomes ordinary.</i></h2><p>${a.body[1]}</p></div>`)
 ];}
function addVillageWorld(){
 const a=alexanderEssay;
 worldSheet('alexander',a.title,'village',0,`<div class="world-heading"><small>LIFE & FORM / BOCACANGREJO</small><h1>The village<br>that built us.</h1><small>CHRISTOPHER ALEXANDER</small></div><div class="world-shaped"><span class="shape-occluder" aria-hidden="true"></span><p>${a.sections[0].body[0].replace(/ (\S+)$/, '&nbsp;$1')}</p></div>`);
 worldSheet('alexander-walk',a.title,'village',1,`<div class="world-bottom"><h2><i>The way down</i></h2><p>${a.sections[0].body[1]}</p></div>`);
 a.sections.forEach((sec,i)=>{
  let ps=i===0?sec.body.slice(2):sec.body;
  const h=i===0?'A landing.<br>A bucket.<br><i>A little room for another life.</i>':sec.heading;
  const body=`<div class="contribution-heading"><small>CHRISTOPHER ALEXANDER / ${String(i+1).padStart(2,'0')}</small><h1>${h}</h1></div><div class="village-essay">${ps.map(p=>`<p class="${p==='What we build builds us in turn.'?'world-revelation':''}">${p}</p>`).join('')}</div>`+(i===2?'<aside class="world-memory">The conquest of Tenerife ended in 1496. It brought enslavement and assimilation, but Indigenous people and customs persisted. The island did not begin with the conquerors’ maps.</aside>':'');
  addSheet('alexander-'+(i+1),a.title+' / '+sec.heading,`contributed village-text village-section-${i}`,body);sheets.at(-1).designed=true;
 });
}
function addTableWorld(a){
 // This recto introduction gives the following artwork a real verso/recto pair.
 addSheet('table',a.title,'contributed table-preface',`<div class="contribution-heading"><small>ARCHITECTURE / CONVERSATIONS AT THE TABLE</small><h1>Three seats.<br><i>More than three minds.</i></h1></div>${featureBody(a.body.slice(0,2))}<p class="contribution-deck">${a.subtitle}</p>`);sheets.at(-1).designed=true;
 worldSheet('table-drawing',a.title,'table',0,`<div class="world-heading"><h1>Different drawings.</h1><small>THE SAME ISLAND</small></div><div class="world-bottom"><p>${a.body[2]}</p></div>`);
 worldSheet('table-tension',a.title,'table',1,`<div class="world-heading"><h1>Held apart.<br><i>Held together.</i></h1></div><div class="world-bottom table-relationship"><p>${a.body[3]}</p></div>`);
 addSheet('table-continued',a.title,'contributed table-voices',`<div class="contribution-heading"><h1>Leave the table open</h1></div>${featureBody(a.body.slice(4))}<p class="feature-technical">${a.note}</p>`);
 // The translation-table poem is appended by the ordinary insert compositor.
}
