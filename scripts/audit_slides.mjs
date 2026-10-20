import { chromium } from 'playwright'
import {auditTargets,slideByFeature,clippedPlotLabels as findClippedPlotLabels} from './audit_targets.mjs'
import { spawn } from 'node:child_process'
import { mkdir,readFile,writeFile,readdir,copyFile } from 'node:fs/promises'
import {resolve} from 'node:path'
import {execFileSync} from 'node:child_process'
const root=resolve(import.meta.dirname,'..'),out=resolve(root,'artifacts')
await mkdir(resolve(out,'slides'),{recursive:true})
const port=3137,origin=`http://127.0.0.1:${port}`,base=process.env.BASE_PATH||'/',routerMode=process.env.ROUTER_MODE||'history'
const url=origin+base.replace(/\/$/,'')
const slideUrl=(path,query='')=>routerMode==='hash'?`${url}/${query?'?'+query:''}#/${path}`:`${url}/${path}${query?'?'+query:''}`
const server=spawn(process.execPath,['scripts/serve.mjs'],{cwd:root,env:{...process.env,PORT:String(port),BASE_PATH:base},stdio:['ignore','pipe','pipe']})
const delay=ms=>new Promise(r=>setTimeout(r,ms))
let browser
const errors=[],requests=[],results=[]
try{
 for(let i=0;i<100;i++){try{if((await fetch(url+'/')).ok)break}catch{}await delay(100)}
 browser=await chromium.launch({headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']})
 const context=await browser.newContext({viewport:{width:1600,height:900},deviceScaleFactor:1})
 await context.route('**/*',route=>{const req=route.request().url();if(!req.startsWith(url+'/')&&!req.startsWith('data:')&&!req.startsWith('blob:')){requests.push(req);return route.abort()}return route.continue()})
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`HTTP ${r.status()}: ${r.url()}`)})
 // Hash-only navigation keeps components alive; each independent check opens a fresh document.
 const openSlide=async(path,query='')=>{if(routerMode==='hash')await page.goto('about:blank');await page.goto(slideUrl(path,query),{waitUntil:'domcontentloaded'})}
 const files=['slides.md',...(await readdir(resolve(root,'slides'))).filter(x=>x.endsWith('.md')).map(x=>'slides/'+x)]
 let count=0;for(const file of files)count+=((await readFile(resolve(root,file),'utf8')).match(/^# /gm)||[]).length
 for(let n=1;n<=count;n++){
  await openSlide(n,'static=1')
  await page.evaluate(()=>document.fonts.ready)
  const slide=page.locator(`.slidev-page[data-slidev-no="${n}"]:visible .academic`).first()
  await slide.waitFor({timeout:15000})
  await slide.locator('img').evaluateAll(images=>Promise.all(images.map(image=>image.decode().catch(()=>{}))))
  const measurements=await slide.evaluate((el,targets)=>{
   const body=el.querySelector('.slide-body'),footer=el.querySelector('.footer'),box=el.getBoundingClientRect(),b=body.getBoundingClientRect(),f=footer.getBoundingClientRect();const scale=box.width/1200
   const overflow=[]
   for(const child of body.querySelectorAll('h1,h2,h3,p,table,figure,.takeaway,.plot-controls,.interaction-note,.author,.affiliation,.number,.math-panel,.step-chain,.attention-mask,.connection-map,.geometry-sketch,.katex-display > .katex,math[display="block"]')){
    const r=child.getBoundingClientRect();if(!r.width||!r.height)continue
    if(r.bottom>f.top-8*scale||r.right>box.right-40*scale||r.left<box.left+38*scale)overflow.push({tag:child.tagName,text:child.textContent.slice(0,70),bottom:r.bottom,footer:f.top})
   }
   for(const math of body.querySelectorAll('.katex-error'))overflow.push({tag:'math',text:math.textContent})
   for(const paragraph of body.querySelectorAll('p,.takeaway,.protocol'))if(/\$[^$]+\$/.test(paragraph.textContent))overflow.push({tag:'raw-math',text:paragraph.textContent.slice(0,100)})
   const missing=[...body.querySelectorAll('img')].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src)
   return {features:Object.keys(targets).filter(key=>el.querySelector(targets[key])),title:el.querySelector('h1')?.textContent,divider:el.classList.contains('chapter-divider'),partDivider:el.classList.contains('part-divider'),chapter:Number(el.querySelector('.footer .page')?.textContent.match(/CH (\d+)/)?.[1]),overflow,missing,bodyScroll:body.scrollHeight,bodyHeight:body.clientHeight}
  },auditTargets)
  await slide.screenshot({path:resolve(out,'slides',`${String(n).padStart(2,'0')}.png`)})
  results.push({slide:n,...measurements});console.log(`Slide ${n}/${count}: ${measurements.title} · overflow=${measurements.overflow.length}`)
 }
 const dividers=results.filter(r=>r.divider)
 if(dividers.length!==7||dividers.some((r,i)=>r.chapter!==i+2||results[r.slide]?.chapter!==r.chapter||r.partDivider!==[2,5].includes(r.chapter)))throw Error('Chapter divider count, placement or part styling mismatch')
 const findSlide=feature=>slideByFeature(results,feature)
 const interactions=[]
 for(const [feature,label] of [['sms','SMS physical time'],['poisson','Poisson SNN T'],['energy','ET reconstruction iteration']]){
  const n=findSlide(feature)
  const loadStarted=Date.now()
  await openSlide(n)
  const slide=page.locator(`.slidev-page[data-slidev-no="${n}"]:visible .academic`).first()
  const slider=slide.getByRole('slider',{name:label});await slider.waitFor({timeout:15000})
  const readyMs=Date.now()-loadStarted
  const before=await slider.inputValue();await slider.focus();await page.keyboard.press('ArrowRight');const after=await slider.inputValue();if(before===after)throw new Error('Slider not operable: '+label)
  if(!page.url().includes('/'+n))throw new Error('Slider stole slide navigation')
  await slide.getByRole('button',{name:'Play',exact:true}).click();await delay(400);await slide.getByRole('button',{name:'Pause',exact:true}).click()
  if(label!=='Poisson SNN T'){
  const trace=slide.locator('svg').nth(label==='SMS physical time'?1:0);const traceBox=await trace.boundingBox();const traceBefore=await slider.inputValue()
  await trace.click({position:{x:traceBox.width*.8,y:traceBox.height*.5}})
  if(await slider.inputValue()===traceBefore)throw new Error('Linked trace did not seek: '+label)
  }
  if(label==='SMS physical time'){
   if(await slide.locator('.trace-svg').count()!==2||await slide.locator('select').count())throw Error('SMS must show only field/error panels without a codec selector')
   const gap=await slide.evaluate(el=>Math.min(...[...el.querySelectorAll('.trace-svg')].map(svg=>el.querySelector('.plot-controls').getBoundingClientRect().top-svg.getBoundingClientRect().bottom)))
   if(gap<8)throw Error('SMS plot labels overlap playback controls')
  }
  if(label==='Poisson SNN T'){
   await slide.getByRole('button',{name:'Reset',exact:true}).click()
   const canvases=slide.locator('.grid-field canvas')
   if(await canvases.count()!==3)throw new Error('Poisson needs exactly ANN/SNN/difference panels')
   const first=await canvases.evaluateAll(cs=>cs.map(c=>c.toDataURL()))
   const complete=await canvases.evaluateAll(cs=>cs.every(c=>c.width===102&&c.height===102&&c.getContext('2d').getImageData(0,0,102,102).data.filter((_,i)=>i%4===3).every(a=>a===255)))
   if(!complete)throw new Error('Poisson native field pixels missing')
   await slide.getByRole('button',{name:'T=64',exact:true}).click()
   const last=await canvases.evaluateAll(cs=>cs.map(c=>c.toDataURL()))
   if(first[0]!==last[0]||first[1]===last[1]||first[2]===last[2])throw new Error('Poisson T did not preserve reference and change SNN/difference')
   if(await slider.inputValue()!=='63')throw new Error('Poisson T button not linked to slider')
   await slide.getByRole('button',{name:'T=32',exact:true}).click()
   await slider.focus();await page.keyboard.press('ArrowRight')
   if(await slider.inputValue()!=='32')throw new Error('Missing actual prefix T=33')
   const intermediate=await canvases.evaluateAll(cs=>cs.map(c=>c.toDataURL()))
   if(intermediate[0]!==first[0]||intermediate[1]===first[1]||intermediate[2]===first[2])throw new Error('Intermediate prefix 33 is not linked to changed fields')
   await slide.getByRole('button',{name:'Reset',exact:true}).click()
  }
  if(label==='ET reconstruction iteration'){
   await slide.getByRole('button',{name:'Reset',exact:true}).click()
   const crisp=await slide.locator('.grid-field canvas').evaluateAll(cs=>cs.every(c=>c.width===256&&c.height===128&&!c.getContext('2d').imageSmoothingEnabled&&getComputedStyle(c).imageRendering==='pixelated'))
   if(!crisp)throw new Error('ET must retain unsmoothed native vortex-street pixels')
   const field=slide.locator('.grid-field canvas').last();const first=await field.evaluate(c=>c.toDataURL())
   await slide.locator('.energy-fields').hover();await page.mouse.wheel(0,100);await delay(150)
   if(await slider.inputValue()!=='1')throw new Error('ET wheel did not advance exactly one update')
   await slider.focus();await page.keyboard.press('End');if(first===await field.evaluate(c=>c.toDataURL()))throw new Error('ET reconstruction did not change')
   await slide.getByRole('checkbox',{name:'Show error'}).check();await slide.getByRole('checkbox',{name:'Show error'}).uncheck()
  }
  await slide.screenshot({path:resolve(out,`interactive-${n}.png`)})
  const clippedLabels=await slide.locator('.trace-svg').evaluateAll(findClippedPlotLabels)
  if(clippedLabels.length)throw new Error('Clipped plot labels: '+clippedLabels.join(', '))
  const m=await slide.evaluate(el=>{const f=el.querySelector('.footer').getBoundingClientRect();return [...el.querySelectorAll('.plot-controls,.interaction-note')].some(c=>c.getBoundingClientRect().bottom>f.top-8)})
  if(m)throw new Error('Interactive slide overflow '+n)
  // Leave through SPA navigation and check that the same cached slide pauses.
  await slide.getByRole('button',{name:'Play',exact:true}).click();await page.mouse.click(1500,80);await page.keyboard.press('ArrowRight');await delay(200);await page.keyboard.press('ArrowLeft');await delay(200)
  if(!await slide.getByRole('button',{name:'Play',exact:true}).count())throw new Error('Playback did not pause on slide leave')
  interactions.push({slide:n,readyMs,slider:true,linkedTraceSeeking:label!=='Poisson SNN T',playback:true,navigationIsolation:true,pauseOnExit:true,...(label==='Poisson SNN T'?{populatedFieldCanvases:true,referenceInvariant:true,TChangesSNNAndDifference:true,intermediate33Verified:true}:{})})
 }
 for(const [feature,kind] of [['vortex','vortex'],['jet','jet'],['hybrid','hybrid']]){
  const n=findSlide(feature)
  await openSlide(n)
  const slide=page.locator(`.slidev-page[data-slidev-no="${n}"]:visible .academic`).first()
  const slider=slide.getByRole('slider',{name:`RFormer ${kind} physical time`})
  await slider.waitFor({timeout:20000})
  if(await slide.getByRole('button',{name:'Pause',exact:true}).count())await slide.getByRole('button',{name:'Pause',exact:true}).click()
  await slide.getByRole('button',{name:'Reset',exact:true}).click()
  const img=slide.locator('.rformer-time-frame');const first=await img.getAttribute('src')
  await slider.focus();await page.keyboard.press('ArrowRight')
  if(await slider.inputValue()!=='1'||first===await img.getAttribute('src'))throw Error('RFormer physical-time seeking failed')
  await slide.getByRole('button',{name:'Play',exact:true}).click();await delay(600)
  await slide.getByRole('button',{name:'Pause',exact:true}).click()
  if(Number(await slider.inputValue())<2)throw Error('RFormer playback failed')
  await slide.screenshot({path:resolve(out,`interactive-${n}.png`)})
  const overflow=await slide.evaluate(el=>{const f=el.querySelector('.footer').getBoundingClientRect();return [...el.querySelectorAll('.plot-controls,.interaction-note,.takeaway')].some(c=>c.getBoundingClientRect().bottom>f.top-8)})
  if(overflow)throw Error('RFormer live overflow '+n)
  await slide.getByRole('button',{name:'Play',exact:true}).click();await page.mouse.click(1500,80);await page.keyboard.press('ArrowRight');await delay(200);await page.keyboard.press('ArrowLeft');await delay(200)
  if(!await slide.getByRole('button',{name:kind==='jet'?'Pause':'Play',exact:true}).count())throw Error('RFormer return playback state is incorrect')
  interactions.push({slide:n,physicalTime:true,slider:true,playback:true,autoplayOnReturn:kind==='jet'})
 }
 const addedViews=[['weather','Weather date'],['latent','Latent and optimized trajectory time']]
 for(const [feature,label] of addedViews){
  const n=findSlide(feature)
  await openSlide(n)
  const slide=page.locator(`.slidev-page[data-slidev-no="${n}"]:visible .academic`).first()
  const slider=slide.getByRole('slider',{name:label});await slider.waitFor({timeout:30000})
  const field=slide.locator('.recorded-frame');const first=await field.getAttribute('src')
  await slider.focus();await page.keyboard.press('ArrowRight');await delay(100)
  if(first===await field.getAttribute('src'))throw Error('New sequence did not seek '+label)
  await slide.getByRole('button',{name:'Play',exact:true}).click();await delay(350);await slide.getByRole('button',{name:'Pause',exact:true}).click()
  const bad=await slide.evaluate(el=>{const footer=el.querySelector('.footer').getBoundingClientRect();return [...el.querySelectorAll('.plot-controls,.interaction-note,.takeaway')].some(c=>c.getBoundingClientRect().bottom>footer.top-8)})
  if(bad)throw Error('Added sequence overflows '+label)
  await slide.screenshot({path:resolve(out,`sequence-${n}.png`)})
  await slide.getByRole('button',{name:'Play',exact:true}).click();await page.mouse.click(1500,80);await page.keyboard.press('ArrowRight');await delay(150);await page.keyboard.press('ArrowLeft');await delay(150)
  if(!await slide.getByRole('button',{name:'Play',exact:true}).count())throw Error('New sequence not paused on leave')
  interactions.push({slide:n,label,slider:true,playback:true,pauseOnExit:true})
 }
 for(const feature of ['scaling','perturbation','threeD']){
  const n=findSlide(feature);await openSlide(n)
  const slide=page.locator(`.slidev-page[data-slidev-no="${n}"]:visible .academic`).first()
  const sliders=slide.getByRole('slider');await sliders.first().waitFor({timeout:30000})
  const expected=feature==='threeD'?2:1
  if(await sliders.count()!==expected)throw Error('Drone playback control count mismatch')
  const canvases=slide.locator(feature==='scaling'?'.swarm-scaling canvas':'.oc-viewport canvas')
  if(await canvases.count()!==(feature==='scaling'?4:2))throw Error('Drone panel count mismatch')
  const first=await canvases.evaluateAll(cs=>cs.map(c=>c.toDataURL()))
  const seek=sliders.first();await seek.focus();await page.keyboard.press('End');await delay(100)
  const last=await canvases.evaluateAll(cs=>cs.map(c=>c.toDataURL()))
  if(first[0]===last[0])throw Error('Drone trajectories did not seek')
  if(feature==='threeD'&&(await sliders.nth(1).inputValue()!=='0'||first[1]!==last[1]))throw Error('Independent drone playback changed the other panel')
  const reset=slide.getByRole('button',{name:'Reset',exact:true});await reset.first().click()
  if(await seek.inputValue()!=='0')throw Error('Drone reset failed')
  await slide.getByRole('button',{name:'Play',exact:true}).first().click();await delay(200)
  await slide.getByRole('button',{name:'Pause',exact:true}).first().click()
  if(Number(await seek.inputValue())===0)throw Error('Drone playback did not advance')
  if(feature==='threeD'){
   const canvas=canvases.first(),box=await canvas.boundingBox()
   await reset.first().click();const original=await canvas.evaluate(c=>c.toDataURL())
   await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.down()
   await page.mouse.move(box.x+box.width*.7,box.y+box.height*.6,{steps:5});await page.mouse.up()
   if(original===await canvas.evaluate(c=>c.toDataURL()))throw Error('Drone camera did not rotate')
   await reset.first().click()
   if(original!==await canvas.evaluate(c=>c.toDataURL()))throw Error('Drone reset did not restore camera')
  }
  await slide.getByRole('button',{name:'Play',exact:true}).first().click()
  await page.mouse.click(1500,80);await page.keyboard.press('ArrowRight');await delay(150);await page.keyboard.press('ArrowLeft');await delay(150)
  if(await slide.getByRole('button',{name:'Play',exact:true}).count()!==expected)throw Error('Drone playback did not pause on exit')
  interactions.push({slide:n,feature,slider:true,playback:true,pauseOnExit:true,independentControls:feature==='threeD',cameraReset:feature==='threeD'})
 }
 // A fresh context has no asset cache: failed data must produce an informative fallback.
 const failure=await browser.newContext({viewport:{width:1600,height:900}})
 await failure.route('**/data/**',route=>route.abort())
 const fp=await failure.newPage();const sms=interactions[0].slide
 await fp.goto(slideUrl(sms),{waitUntil:'domcontentloaded'});await fp.getByText('Static view · interactive data unavailable').first().waitFor()
 for(const feature of ['vortex','jet','weather','latent','hybrid']){
  const n=findSlide(feature)
  await fp.goto(slideUrl(n),{waitUntil:'domcontentloaded'})
  const failedSlide=fp.locator(`.slidev-page[data-slidev-no="${n}"]:visible .academic`).first()
  await failedSlide.getByText('Static view · interactive data unavailable').waitFor()
  await failedSlide.locator('.figure-fallback').evaluate(image=>image.decode())
  if(!await failedSlide.locator('.figure-fallback').evaluate(i=>i.complete&&i.naturalWidth>0))throw Error('RFormer fallback missing')
 }
 for(const feature of ['scaling','perturbation','threeD']){
  const n=findSlide(feature);await fp.goto(slideUrl(n),{waitUntil:'domcontentloaded'})
  const failedSlide=fp.locator(`.slidev-page[data-slidev-no="${n}"]:visible .academic`).first()
  await failedSlide.getByRole('status').filter({hasText:/unavailable|missing|fetch|checksum/i}).waitFor({timeout:30000})
 }
 await failure.close()
 const noWebGL=await browser.newContext({viewport:{width:1600,height:900}})
 await noWebGL.addInitScript(()=>{const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){if(String(type).includes('webgl'))return null;return original.call(this,type,...args)}})
 const wp=await noWebGL.newPage();await wp.goto(slideUrl(findSlide('threeD')),{waitUntil:'domcontentloaded'})
 const unavailable=wp.locator('.oc-examples.three-d [role="status"]')
 await unavailable.filter({hasText:/WebGL|context/i}).waitFor({timeout:30000});await noWebGL.close()
 await openSlide('presenter/1');await page.locator('.academic').first().waitFor();const presenter=await page.locator('.academic').count();if(!presenter)throw new Error('Presenter route missing')
 const download=await fetch(`${url}/defense.pdf`)
 if(!download.ok||new TextDecoder().decode(new Uint8Array(await download.arrayBuffer()).subarray(0,5))!=='%PDF-')throw Error('PDF download unavailable')
 if(process.argv.includes('--pdf')){
  await openSlide('print','print=true&static=1');await page.evaluate(()=>document.fonts.ready)
  await page.locator('.print-slide-container').last().waitFor()
  if(await page.locator('.print-slide-container').count()!==count)throw new Error('Incomplete print route')
  // Use Slidev's build-time export as the canonical PDF. Its export server
  // applies the framework's exact slide sizing and metadata; independently
  // printing the deployed SPA can introduce an extra page from CSS rounding.
  await copyFile(resolve(root,'dist/defense.pdf'),resolve(out,'defense.pdf'))
  const info=execFileSync('pdfinfo',[resolve(out,'defense.pdf')],{encoding:'utf8'})
  if(Number(info.match(/Pages:\s+(\d+)/)?.[1])!==count)throw new Error('PDF page count mismatch')
  const pdfText=execFileSync('pdftotext',['-layout',resolve(out,'defense.pdf'),'-'],{encoding:'utf8'}).split('\f')
  const normalize=s=>s.normalize('NFKD').toLowerCase().replace(/[^a-z0-9]/g,'')
  for(const [i,slide] of results.entries())if(!normalize(pdfText[i]||'').includes(normalize(slide.title)))throw new Error('PDF title/order mismatch on page '+(i+1))
 }
 const report={basePath:base,routerMode,pdfDownload:true,generatedAt:new Date().toISOString(),slides:results,interactions,pdfPages:process.argv.includes('--pdf')?count:null,presenter:!!presenter,fallbackOnDataFailure:true,webGLFailureReported:true,externalRequests:requests,browserErrors:errors}
 await writeFile(resolve(out,'layout-audit.json'),JSON.stringify(report,null,2))
 if(results.some(r=>r.overflow.length||r.missing.length)||errors.length||requests.length)throw new Error('Slide audit failed; see artifacts/layout-audit.json')
 console.log(`PASS: ${count} slides, ${interactions.length} interactive figures, fallback, presenter, and offline requests.`)
}finally{await browser?.close();server.kill('SIGTERM')}
