import {readFileSync,writeFileSync} from 'node:fs'
import {resolve} from 'node:path'
const root=resolve(import.meta.dirname,'..')
const main=readFileSync(resolve(root,'slides.md'),'utf8')
const files=['slides.md',...Array.from(main.matchAll(/^src: \.\/(.+)$/gm),m=>m[1])]
const rows=[['slide','chapter','title','source','markdown','figures','treatment']]
for(const name of files){const text=readFileSync(resolve(root,name),'utf8');for(const match of text.matchAll(/(?:^|\n)---\n([\s\S]*?)\n---\n([\s\S]*?)(?=\n---\n|$)/g)){
 const [,front,body]=match;const title=body.match(/^# (.+)$/m)?.[1];if(!title)continue
 const chapter=front.match(/^chapter: ['"]?(\d+)/m)?.[1]||'1'
 const source=front.match(/^source: (.+)$/m)?.[1].replace(/^['"]|['"]$/g,'')||'Thesis metadata'
 const figures=Array.from(body.matchAll(/src="(\/figures\/[^"\s]+)"/g),m=>m[1]).join(';')
 rows.push([String(rows.length),chapter,title.replaceAll('<br>',' '),source,name,figures,/<(SMSRollout|ConversionOverT|DroneSwarm3D|EnergyHistory|RFormerTime|RecordedSequence|SwarmExamples)/.test(body)?'required-dynamic':'static'])
}}
const quote=v=>'"'+v.replaceAll('"','""')+'"'
writeFileSync(resolve(root,'docs/slide_inventory.csv'),rows.map(row=>row.map(quote).join(',')).join('\n')+'\n')
console.log(`Indexed ${rows.length-1} slides with sources and figure references.`)
