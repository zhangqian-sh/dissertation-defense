import http from 'node:http'
import {readFile,stat} from 'node:fs/promises'
import {resolve,extname} from 'node:path'
const root=resolve(import.meta.dirname,'../dist')
const port=Number(process.env.PORT||3030)
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json','.png':'image/png','.svg':'image/svg+xml','.woff2':'font/woff2','.otf':'font/otf'}
const server=http.createServer(async(req,res)=>{try{
 const url=new URL(req.url,'http://127.0.0.1');let path=resolve(root,'.'+decodeURIComponent(url.pathname));if(!path.startsWith(root+'/')&&path!==root){res.writeHead(403).end();return}
 try{const s=await stat(path);if(s.isDirectory())path=resolve(path,'index.html')}catch{if(extname(path)){res.writeHead(404).end('Not found');return}path=resolve(root,'index.html')}
 const data=await readFile(path);res.writeHead(200,{'Content-Type':mime[extname(path)]||'application/octet-stream','Cache-Control':'no-cache'});res.end(data)
}catch{res.writeHead(500).end('Unable to serve presentation')}})
server.listen(port,'127.0.0.1',()=>console.log(`Defense: http://127.0.0.1:${port}`))
for(const signal of ['SIGINT','SIGTERM'])process.on(signal,()=>server.close(()=>process.exit(0)))
