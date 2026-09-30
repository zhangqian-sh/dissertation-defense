import { shallowRef, ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useNav } from '@slidev/client'
export interface Tensor { dtype:string; shape:number[]; order:'C'; values:Float64Array|Float32Array }
export interface DefenseAsset { schema_version:2; asset_id:string; units:Record<string,string>; data:{states:Array<{id:string;status:string;payload:any}>} }
const cache=new Map<string,Promise<DefenseAsset>>()
let manifest:Promise<any>|undefined
const local=(path:string,base=location.origin+'/data/manifest.json')=>{
  const url=new URL(path,base)
  if(url.origin!==location.origin) throw new Error('Nonlocal data URL')
  return url.href
}
async function fetchChecked(url:string){ const r=await fetch(url); if(!r.ok) throw new Error(`Data unavailable (${r.status})`); return r }
async function decode(value:any):Promise<any> {
  if(value && typeof value==='object') {
    if('dtype' in value){
      if(value.binary_path){
        if(value.dtype!=='float32'||value.byte_order!=='little'||value.order!=='C'||!Array.isArray(value.shape)||!value.shape.every((n:number)=>Number.isInteger(n)&&n>0))throw new Error('Invalid binary tensor')
        const r=await fetchChecked(local(value.binary_path));const bytes=await r.arrayBuffer()
        const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(v=>v.toString(16).padStart(2,'0')).join('')
        if(hash!==value.sha256||bytes.byteLength!==value.shape.reduce((a:number,b:number)=>a*b,1)*4)throw new Error('Binary tensor checksum/size mismatch')
        const values=new Float32Array(bytes)
        if(!values.every(Number.isFinite))throw new Error('Nonfinite binary tensor')
        return {...value,values}
      }
      if(value.order!=='C' || !Array.isArray(value.shape) || !Array.isArray(value.values) || value.shape.reduce((a:number,b:number)=>a*b,1)!==value.values.length || !value.values.every(Number.isFinite)) throw new Error('Invalid tensor')
      return {...value,values:new Float64Array(value.values)}
    }
    if(Array.isArray(value)) return Promise.all(value.map(decode))
    return Object.fromEntries(await Promise.all(Object.entries(value).map(async([k,v])=>[k,await decode(v)])))
  }
  return value
}
export function loadAsset(id:string){
  if(!cache.has(id)) cache.set(id,(async()=>{
    manifest ||= fetchChecked('/data/manifest.json').then(r=>r.json())
    const m=await manifest
    if(m.schema_version!==2) throw new Error('Unsupported manifest')
    const entry=m.assets.find((a:any)=>a.asset_id===id)
    if(!entry) throw new Error('Required asset missing')
    const r=await fetchChecked(local(entry.path)); const bytes=await r.arrayBuffer()
    const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(v=>v.toString(16).padStart(2,'0')).join('')
    if(hash!==entry.sha256) throw new Error('Asset checksum mismatch')
    const e=JSON.parse(new TextDecoder().decode(bytes))
    if(e.schema_version!==2 || e.asset_id!==id || !e.data?.states?.length) throw new Error('Invalid asset envelope')
    return decode(e)
  })())
  return cache.get(id)!
}
export function useDefenseAsset(id:string){
  const nav=useNav()
  const staticMode=computed(()=>nav.isPrintMode.value || ['static','print'].some(key=>new URLSearchParams(location.search).has(key)))
  const data=shallowRef<DefenseAsset>(); const error=ref(''); let disposed=false
  onMounted(async()=>{ if(staticMode.value)return; try{const d=await loadAsset(id);if(!disposed)data.value=d}catch(e){if(!disposed)error.value=String(e)} })
  onBeforeUnmount(()=>{disposed=true})
  const payload=computed(()=>data.value?.data.states[0].payload)
  return {data,payload,error,staticMode}
}

export const values=(t:Tensor)=>t.values
export const row=(t:Tensor,index:number)=>t.values.subarray(index*t.shape[1],(index+1)*t.shape[1])
