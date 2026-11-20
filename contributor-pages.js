/* Different desks brought different paper objects; no universal article opener. */
function contributorHeading(t,lang='en') { return `<div class="contribution-heading"><small>${t.author||t.tag||''}</small><h1 lang="${lang}">${t.title}</h1></div>`; }
function panoramaHalf(family,side,title,copy='') {
 const asset=family==='dream'?'dreaming-together-collage.png':'film-desk-castle.png';
 return `<div class="panorama-window panorama-${family} panorama-${side}"><img src="assets/${asset}" width="1424" height="1104" alt="${side?'Right':'Left'} half of ${family==='dream'?'a coastal photomontage of homes, terraces and Atlantic lives':'an ink fantasy of a municipal tower overflowing with life'}">${title?`<h1>${title}</h1>`:''}${copy?`<p class="panorama-copy">${copy}</p>`:''}</div>`;
}
function addContributorPaper(a,lang='en') {
 const t=a.id==='arrival'&&lang!=='en'?openingFeatures[lang]:a;
 const key=a.id==='arrival'?`arrival/${lang}`:a.id;
 const voice=a.id==='arrival'?lang:a.id;
 const half=t.pageBreak??Math.ceil(t.body.length/2);
 const prose=ps=>`<div class="sheet-prose" lang="${lang}">${bodyParagraphs(ps,lang,false)}</div>`;
 if(voice==='fr') {
  ['Rêver à<br>plusieurs',''].forEach((title,i)=>{addSheet(i?key+'-plate':key,t.title,`contributed panorama-page panorama-page-${i}`,panoramaHalf('dream',i,title,t.body[i]));sheets.at(-1).designed=true;});
  addSheet(key+'-text',t.title,'contributed voice-fr',contributorHeading({...t,title:'Sans centre unique'},lang)+prose(t.body.slice(2,5)));
  addSheet(key+'-continued',t.title,'contributed voice-fr continuation',prose(t.body.slice(5))+`<p class="contribution-deck">${t.subtitle}</p>`);
  return;
 }
 let figure='';
 if(voice==='de')figure=featureFigure('drago-excursion-halftone.png','ICOD / AUS DEM AUSFLUGSHEFT / 1977','Imagined halftone excursion photograph of the Drago and two people with a notebook');
 if(voice==='coast')figure=featureFigure('montana-amarilla-v2.png','MONTAÑA AMARILLA / DEL CUADERNO DEL AGUA','Barracuda beside submerged volcanic rock');
 if(voice==='cousteau')figure=featureFigure('ocean-observatory.png','CARNET DE TÉLÉVISION / UNE FENÊTRE, DU TEMPS','Imagined underwater observation room');
 if(voice==='table')figure=featureFigure('study-tensegrity.svg','COMPRESSION / TENSION / TWO MINDS AT WORK','A tensegrity study');
 const stamp=voice==='en'?'<div class="contribution-year">1977</div>':voice==='maathai'?'<div class="contribution-year">KENYA<br>1977</div>':voice==='it'?'<div class="contribution-word">abitare</div>':voice==='credit'?'<div class="contribution-stamp">COOPERATIVA DEL PORVENIR<br>PROPOSED SUBSCRIPTION / 1977</div>':'';
 const opening=stamp+contributorHeading(t,lang)+(voice==='cousteau'||voice==='de'?figure:'')+prose(t.body.slice(0,half))+(voice==='coast'||voice==='table'?figure:'')+`<p class="contribution-deck" lang="${lang}">${t.subtitle}</p>`;
 addSheet(key,t.title,`contributed voice-${voice}`,opening);
 if(voice==='gilliam') {
  // The introductory sheet is a recto; the drawing then occupies an actual verso/recto pair.
  ['The plan<br><i>has tenants.</i>',''].forEach((title,i)=>{addSheet(key+'-plate-'+i,t.title,`contributed panorama-page panorama-page-${i}`,panoramaHalf('film',i,title,i?'':'Allow room for the people.'));sheets.at(-1).designed=true;});
 }
 addSheet(key+'-continued',t.title,`contributed voice-${voice} continuation`,`<h2 class="contribution-continuation">${t.continuationTitle||t.title}</h2>`+prose(t.body.slice(half))+(lang==='en'&&a.note?`<aside class="workshop-note"><p>${a.note}</p></aside>`:''));
}
