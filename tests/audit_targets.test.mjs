import test from 'node:test'
import assert from 'node:assert/strict'
import {auditTargets,slideByFeature} from '../scripts/audit_targets.mjs'

test('interactive audit survives title changes, repeated titles and slide reordering',()=>{
 const results=Object.keys(auditTargets).map((feature,i)=>({slide:30-i,title:'Example',features:[feature]}))
 for(const [i,feature] of Object.keys(auditTargets).entries())assert.equal(slideByFeature(results,feature),30-i)
 results.reverse();results.forEach(row=>row.title='Renamed title')
 assert.equal(slideByFeature(results,'sms'),30)
})

test('missing, duplicated and unknown audit targets remain hard failures',()=>{
 assert.throws(()=>slideByFeature([],'sms'),/found 0/)
 assert.throws(()=>slideByFeature([{slide:1,features:['sms']},{slide:2,features:['sms']}],'sms'),/found 2/)
 assert.throws(()=>slideByFeature([],'removedSwarmTabs'),/Unknown audit feature/)
})
