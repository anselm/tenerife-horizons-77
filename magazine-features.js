/* Shared editorial material for individually composed features. */
const featureDesigns = {
 below: {title:'The sea between us',lines:['THE SEA','BETWEEN','US.'],caption:'LÁMINA 02 / A ROOM IN THE ATLANTIC / TENERIFE, 2027',image:'ocean-room-1977.png',alt:'Speculative underwater common room and submarine tram beside the volcanic Tenerife coast',label:'OCEAN WORKSHOP / PROPOSAL 02',accent:'blue'},
 slope: {title:'A town that learns the slope',lines:['A TOWN','THAT LEARNS','THE SLOPE'],caption:'SECCIÓN HABITADA / SHADE, WATER, ROOMS AND THE PATH BETWEEN',image:'hillside-section-1977.png',alt:'Ink and two-colour sectional perspective of communal homes stepping down a volcanic hillside',label:'ARCHITECTURE WORKSHOP / PROPOSAL 03',accent:'rust'},
 air: {title:'Take the lift to the sky',lines:['TAKE THE','LIFT TO','THE SKY'],caption:'ESTACIÓN DE ALTURA / THE CLIMB IS HELD IN COMMON',image:'glider-station-1977.png',alt:'Personal glider raised in a tall mechanical lift station above a Tenerife town',label:'TRANSPORT WORKSHOP / PROPOSAL 05',accent:'red'}
};
const clarkeLeaf = {
 title:'Another island, another horizon', label:'COLOMBO / TENERIFE · A CONVERSATION BETWEEN SESSIONS',
 deck:'Arthur C. Clarke brings the sea into a discussion of distance.',
 body:[
 'Clarke has come from Sri Lanka with a writer’s habit of keeping the apparently irrelevant detail. His new collection, The View from Serendip, puts recollection, diving and speculation within reach of one another. At our table, somebody has made much the same arrangement with a chart, a coffee cup and a wet towel.',
 'The ocean group has been discussing a window. The communications group is discussing a satellite. Clarke sits between them, and for a while neither group is certain which meeting he is attending. A diver and a writer inhabit different distances from the same island; one returns with a story the other could not have invented at a desk.',
 'A young delegate asks whether a view from orbit might finally make the world comprehensible. Before anyone answers, a draught lifts the route drawings. Two people catch opposite corners. The coffee has already reached La Gomera.',
 'Clarke helps lay the sheets out to dry. The conversation resumes over the unmarked part of the table. For a few minutes, the distance between two islands has become the distance at which a friend can hear you.'
 ],
 note:'AL MARGEN: las distancias se miden también por la gente que nos espera.'
};
const featureMarginalia = {
 below:[
 ['THE INVITATION','A room, a lamp, a visitor. The proposal begins with the wish to stay long enough to notice another life.'],
 ['THE OBJECTION','The maintenance group asks that the beautiful window remain on the drawing while someone explains how it will be cleaned.'],
 ['THE AMENDMENT','A second route home is pencilled in. The draughtsman has to move the elegant title to make room for it.']
 ],
 air:[
 ['01 / ASCENDER','The tower supplies the climb. Record the electricity, the machinery and the person who maintains it.'],
 ['02 / PLANEAR','The aircraft spends height. Draw the headwind as well as the fine afternoon.'],
 ['03 / VOLVER A SUBIR','For the longer journey, land, fold the wings and take another lift. The connection begins on the ground.']
 ],
 slope:[
 ['REVISIÓN A LÁPIZ','Do not erase the contour to improve the perspective.'],
 ['REVISIÓN EN ROJO','A door may close without closing the household out of the town.'],
 ['SIN RESOLVER','Who changes the calendar when the people change?']
 ]
};
function featureFigure(path,caption,alt){return `<figure class="feature-figure"><img src="assets/${path}" alt="${alt}" ${path.endsWith(".png")?`width="${path.includes("section")||path.includes("terrace")?1536:1024}" height="${path.includes("section")||path.includes("terrace")?1024:1536}"`:""} loading="lazy"><figcaption>${caption}</figcaption></figure>`;}
function featureNotice(leaf){return `<aside class="feature-notice"><span class="eyebrow">${leaf.label}</span><h3>${leaf.title}</h3><p>${leaf.text}</p></aside>`;}
function featureBody(ps){return `<div class="feature-prose">${ps.map(p=>`<p>${p}</p>`).join('')}</div>`;}
function featureSlips(id){return `<div class="feature-slips">${featureMarginalia[id].map(([h,p])=>`<section><h3>${h}</h3><p>${p}</p></section>`).join('')}</div>`;}
function addDesignedFeature(a){
 const d=featureDesigns[a.id];const id=a.id;
 const head=`<span class="eyebrow">${d.label}</span><h1 class="feature-headline">${d.lines.join('<br>')}</h1><p class="feature-deck">${a.subtitle}</p><p class="feature-byline">${a.author}</p>`;
 const plate=featureFigure(d.image,d.caption,d.alt);
 const bodies=id==='below'?[
  head+featureBody(a.body.slice(0,3)),
  plate+`<p class="plate-thought">Una stanza, non un impero.</p>`,
  `<h2 class="feature-subhead">The coast continues.</h2>`+featureBody(a.body.slice(3))+featureNotice(workshopLeaves.below),
  `<h2 class="feature-subhead">The beautiful drawing<br>has a reverse side.</h2>`+featureFigure('study-ocean-services.svg',workshopLeaves['below-continued'].caption,'Service section of a small underwater room')+featureNotice(workshopLeaves['below-continued'])+featureSlips(id)+`<p class="feature-technical">${a.note}</p>`
 ]:id==='slope'?[
  head+featureBody(a.body.slice(0,3))+featureSlips(id),
  plate+`<p class="feature-callout" lang="es">${a.body[3]}</p><p class="feature-technical">${a.note}</p>`,
  `<h2 class="feature-subhead">Outside the door</h2><p class="feature-callout" lang="it">${a.body[4]}</p>`+featureBody(a.body.slice(5)),
  featureFigure('terrace-workshop.png','LA TERRAZA / THE USE OF AN AFTERNOON','An inhabited shared terrace with a kitchen and workbench')+`<div class="feature-poem"><span class="eyebrow">${editionInserts['slope-continued'].label}</span><h2>Se hace camino<br>al andar</h2><p lang="es">${editionInserts['slope-continued'].lines.join('<br>')}</p><small>${editionInserts['slope-continued'].credit}</small></div>`+featureBody(editionInserts['slope-continued'].body)
 ]:[
  head+plate,
  `<h2 class="feature-subhead">Height becomes<br>a public service.</h2>`+featureBody(a.body.slice(0,4))+`<p class="feature-callout" lang="fr">${a.body[4]}</p>`,
  `<h2 class="feature-subhead">A chain of descents</h2><figure class="feature-figure">${airlift}<figcaption>POWERED ASCENT / UNPOWERED GLIDE / PRINCIPLE ONLY</figcaption></figure>`+featureBody(a.body.slice(5))+`<p class="feature-technical">${a.note}</p>`,
  `<h2 class="feature-subhead">The last hundred metres</h2>`+featureSlips(id)+featureFigure('study-landing.svg',workshopLeaves['air-continued'].caption,'Landing court and onward footpath')+featureNotice(workshopLeaves['air-continued'])
 ];
 bodies.forEach((body,i)=>{addSheet(i===0?id:i===3?id+'-continued':id+'-'+i,d.title,'designed-feature feature-'+id+' feature-part-'+i,body);sheets[sheets.length-1].designed=true;});
}
function addClarkeLeaf(){addSheet('clarke',clarkeLeaf.title,'clarke-leaf',`<span class="eyebrow">${clarkeLeaf.label}</span><h1>Another island,<br><i>another horizon.</i></h1><p class="feature-deck">${clarkeLeaf.deck}</p>${featureBody(clarkeLeaf.body)}<p class="feature-callout" lang="es">${clarkeLeaf.note}</p>`);}
