import test from 'node:test'
import assert from 'node:assert/strict'
import {createHash} from 'node:crypto'
import {readFileSync} from 'node:fs'
import {loadAnimationIndex,loadAnimationFrames} from '../composables/animationBundle.mjs'
const png=readFileSync(new URL('../public/figures/ch06/blood-u-0.png',import.meta.url))
const sha=bytes=>createHash('sha256').update(bytes).digest('hex')
const bytes=Buffer.concat([png,png])
const meta={schema_version:1,bundle:{format:'png-concat-v1',path:'/data/animations/blood/frames.bin',byte_length:bytes.length,sha256:sha(bytes)},frames:[{panels:[0,1].map(i=>({offset:i*png.length,length:png.length,sha256:sha(png)}))}]}
test('index validation, image slices, explicit decoding, cleanup and corruption',async()=>{
 const originalFetch=globalThis.fetch,OriginalImage=globalThis.Image,originalCreate=URL.createObjectURL,originalRevoke=URL.revokeObjectURL
 let decoded=0,created=[],revoked=[]
 globalThis.Image=class{async decode(){decoded++}}
 URL.createObjectURL=blob=>{const url=`blob:${created.length}`;created.push(blob);return url}
 URL.revokeObjectURL=url=>revoked.push(url)
 try{
  globalThis.fetch=async path=>path.endsWith('index.json')?Response.json(meta):new Response(bytes)
  assert.deepEqual(await loadAnimationIndex('blood'),meta)
  await assert.rejects(loadAnimationIndex('../blood'),/Invalid animation name/)
  const loaded=await loadAnimationFrames(meta)
  assert.equal(loaded.frames[0].length,2);assert.equal(decoded,0)
  assert.deepEqual(Buffer.from(await created[0].arrayBuffer()),png)
  loaded.dispose();assert.equal(revoked.length,2)
  const ready=await loadAnimationFrames(meta,{decode:true});assert.equal(decoded,2);ready.dispose()
  globalThis.fetch=async()=>new Response(Buffer.from('corrupt'))
  await assert.rejects(loadAnimationFrames(meta),/checksum/)
  globalThis.fetch=async()=>new Response(bytes)
  const invalid=structuredClone(meta);invalid.frames[0].panels[1].offset++
  await assert.rejects(loadAnimationFrames(invalid),/slice/)
  const badHash=structuredClone(meta);badHash.frames[0].panels[0].sha256='bad'
  await assert.rejects(loadAnimationFrames(badHash),/frame checksum/)
  globalThis.Image=class{async decode(){throw Error('decode failed')}}
  const before=revoked.length
  await assert.rejects(loadAnimationFrames(meta,{decode:true}),/decode failed/)
  assert.equal(revoked.length-before,2)
 }finally{globalThis.fetch=originalFetch;globalThis.Image=OriginalImage;URL.createObjectURL=originalCreate;URL.revokeObjectURL=originalRevoke}
})
