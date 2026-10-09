import test from 'node:test'
import assert from 'node:assert/strict'
import {chromium} from 'playwright'
import {clippedPlotLabels} from '../scripts/audit_targets.mjs'

test('plot label audit accounts for rotation and scaling while detecting clipping',async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']})
 try{
  const page=await browser.newPage()
  for(const width of [250,500,1000]){
   await page.setContent(`<svg width="${width}" viewBox="0 0 500 250">
    <text x="14" y="118" transform="rotate(-90 14 118)" text-anchor="middle" font-size="12">relative L₂</text>
    <text x="30" y="26" font-size="16">training end</text>
    <text x="-10" y="50" font-size="12">actually clipped</text>
   </svg>`)
   assert.deepEqual(await page.locator('svg').evaluateAll(clippedPlotLabels),['actually clipped'])
  }
 }finally{await browser.close()}
})
