import {publicAssetUrl} from './publicAssetUrl.mjs'
const hash=async bytes=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(v=>v.toString(16).padStart(2,'0')).join('')
export async function loadAnimationIndex(name){
 if(!/^[a-z0-9-]+$/.test(name))throw Error('Invalid animation name')
 const response=await fetch(publicAssetUrl(`/data/animations/${name}/index.json`))
 if(!response.ok)throw Error('Missing animation index')
 const meta=await response.json()
 if(meta.schema_version!==1||meta.bundle?.format!=='png-concat-v1'||meta.bundle.path!==`/data/animations/${name}/frames.bin`||!Array.isArray(meta.frames)||!meta.frames.length)throw Error('Invalid animation index')
 return meta
}
export async function loadAnimationFrames(meta,{decode=false}={}){
 const response=await fetch(publicAssetUrl(meta.bundle.path));if(!response.ok)throw Error('Missing animation bundle')
 const bytes=await response.arrayBuffer()
 if(bytes.byteLength!==meta.bundle.byte_length||await hash(bytes)!==meta.bundle.sha256)throw Error('Animation bundle checksum mismatch')
 const entries=meta.frames.flatMap(f=>f.panels??[f]);let end=0
 for(const entry of entries){
  if(!Number.isSafeInteger(entry.offset)||entry.offset!==end||!Number.isSafeInteger(entry.length)||entry.length<=0||entry.offset+entry.length>bytes.byteLength)throw Error('Invalid animation slice')
  const slice=bytes.slice(entry.offset,entry.offset+entry.length)
  if(await hash(slice)!==entry.sha256)throw Error('Animation frame checksum mismatch')
  end+=entry.length
 }
 if(end!==bytes.byteLength)throw Error('Unused animation bundle bytes')
 const urls=[]
 try{
  const frames=meta.frames.map(frame=>(frame.panels??[frame]).map(entry=>{
   const url=URL.createObjectURL(new Blob([bytes.slice(entry.offset,entry.offset+entry.length)],{type:'image/png'}));urls.push(url);return url
  }))
  if(decode)await Promise.all(urls.map(async url=>{const image=new Image();image.src=url;await image.decode()}))
  return {frames,dispose:()=>urls.forEach(URL.revokeObjectURL)}
 }catch(error){urls.forEach(URL.revokeObjectURL);throw error}
}
