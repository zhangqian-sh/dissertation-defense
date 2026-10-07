import {readFileSync,existsSync,readdirSync} from 'node:fs'
import {resolve,dirname} from 'node:path'
import {createHash} from 'node:crypto'
const root=resolve(import.meta.dirname,'..'),pub=resolve(root,'public')
const hash=p=>createHash('sha256').update(readFileSync(p)).digest('hex')
function binaries(v){if(!v||typeof v!=='object')return;if(v.binary_path){const p=resolve(pub,v.binary_path.replace(/^\//,''));if(!p.startsWith(pub+'/')||hash(p)!==v.sha256||readFileSync(p).byteLength!==v.shape.reduce((a,b)=>a*b,1)*4)throw new Error('Invalid binary tensor');return}for(const child of Object.values(v))binaries(child)}
const manifest=JSON.parse(readFileSync(resolve(pub,'data/manifest.json')))
if(manifest.schema_version!==2||!['ch02/sms_longtime_rollout','ch03/conversion_over_t','ch05/energy_history','ch07/ocformer_swarm_3d'].every(id=>manifest.assets.some(a=>a.asset_id===id)))throw new Error('Four schema-v2 assets required')
for(const a of manifest.assets){const path=resolve(pub,'data',a.path);const fallback=resolve(pub,a.fallback_path.replace(/^\//,''));if(!path.startsWith(pub+'/')||!fallback.startsWith(pub+'/'))throw new Error('Path escapes public');if(hash(path)!==a.sha256||hash(fallback)!==a.fallback_sha256)throw new Error('Checksum mismatch');const e=JSON.parse(readFileSync(path));if(e.asset_id!==a.asset_id||e.schema_version!==2)throw new Error('Invalid asset');binaries(e)}
let images=0
for(const file of ['slides.md',...readdirSync(resolve(root,'slides')).filter(n=>n.endsWith('.md')).map(n=>'slides/'+n)]){
 const text=readFileSync(resolve(root,file),'utf8')
 for(const [,path] of text.matchAll(/(?:src|fallback)="(\/[^"\s]+)"/g)){if(!existsSync(resolve(pub,path.slice(1))))throw new Error(`Missing ${path} in ${file}`);images++}
}
for(const ch of ['ch02/sms_longtime_rollout','ch03/conversion_over_t','ch05/energy_history','ch07/ocformer_swarm_3d'])if(!existsSync(resolve(pub,'fallback_figures',ch+'.png')))throw new Error('Missing print fallback')
for(const font of ['NotoSerif-Regular.ttf', 'NotoSerif-Medium.ttf', 'NotoSerif-SemiBold.ttf', 'NotoSerif-Bold.ttf', 'NotoSerif-Italic.ttf', 'NotoSerif-SemiBoldItalic.ttf', 'NotoSerif-BoldItalic.ttf'])if(!existsSync(resolve(pub,'fonts',font)))throw new Error('Missing local font: '+font)
console.log(`Validated ${manifest.assets.length} data assets, their checksums, ${images} slide image references, and local fallbacks/fonts.`)
