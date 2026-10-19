// Piecewise-linear scalar interpolation on the native mesh, not triangle fills
// or post-hoc blur. Cache geometry weights; playback only updates scalar colors.
export function meshRaster(coordinates,cells,size=256){
 const xs=Array.from(coordinates).filter((_,i)=>i%2===0),ys=Array.from(coordinates).filter((_,i)=>i%2===1)
 const xmin=Math.min(...xs),xmax=Math.max(...xs),ymin=Math.min(...ys),ymax=Math.max(...ys)
 const ids=new Int32Array(size*size*3).fill(-1),weights=new Float32Array(ids.length)
 const x=i=>(coordinates[2*i]-xmin)/(xmax-xmin)*size-.5
 const y=i=>(ymax-coordinates[2*i+1])/(ymax-ymin)*size-.5
 for(let t=0;t<cells.length;t+=3){
  const a=cells[t],b=cells[t+1],c=cells[t+2],ax=x(a),ay=y(a),bx=x(b),by=y(b),cx=x(c),cy=y(c)
  const det=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy);if(Math.abs(det)<1e-12)continue
  for(let py=Math.max(0,Math.ceil(Math.min(ay,by,cy)));py<=Math.min(size-1,Math.floor(Math.max(ay,by,cy)));py++){
   for(let px=Math.max(0,Math.ceil(Math.min(ax,bx,cx)));px<=Math.min(size-1,Math.floor(Math.max(ax,bx,cx)));px++){
    const u=((by-cy)*(px-cx)+(cx-bx)*(py-cy))/det,v=((cy-ay)*(px-cx)+(ax-cx)*(py-cy))/det,w=1-u-v
    if(Math.min(u,v,w)<-1e-6)continue
    const k=(py*size+px)*3;ids.set([a,b,c],k);weights.set([u,v,w],k)
   }
  }
 }
 return {size,ids,weights}
}
export function interpolateRaster(raster,values){
 const out=new Float64Array(raster.size**2).fill(NaN)
 for(let i=0;i<out.length;i++){const k=i*3;if(raster.ids[k]>=0)out[i]=values[raster.ids[k]]*raster.weights[k]+values[raster.ids[k+1]]*raster.weights[k+1]+values[raster.ids[k+2]]*raster.weights[k+2]}
 return out
}
export function scalarColors(values,limit){
 const rgba=new Uint8ClampedArray(values.length*4),neutral=[247,246,237]
 for(let i=0;i<values.length;i++){
  const v=values[i];if(!Number.isFinite(v))continue
  const s=Math.max(-1,Math.min(1,v/Math.max(limit,1e-30))),end=s<0?[35,68,107]:[164,46,56]
  for(let c=0;c<3;c++)rgba[4*i+c]=Math.round(neutral[c]+(end[c]-neutral[c])*Math.abs(s))
  rgba[4*i+3]=255
 }
 return rgba
}

// Matplotlib jet's channel breakpoints and 256-entry sampling.
const jetChannels=[[[0,0],[.35,0],[.66,1],[.89,1],[1,.5]],[[0,0],[.125,0],[.375,1],[.64,1],[.91,0],[1,0]],[[0,.5],[.11,1],[.34,1],[.65,0],[1,0]]]
const jetTable=Array.from({length:256},(_,i)=>jetChannels.map(stops=>{
 const t=i/255,j=Math.max(1,stops.findIndex(([x])=>x>=t)),[x0,c0]=stops[j-1],[x1,c1]=stops[j]
 return Math.round(255*(c0+(c1-c0)*(t-x0)/(x1-x0)))
}))
export const jetGradient=`linear-gradient(90deg,${jetTable.map(rgb=>`rgb(${rgb.join(',')})`).join(',')})`
export function jetColors(values,min,max){
 const rgba=new Uint8ClampedArray(values.length*4)
 for(let i=0;i<values.length;i++){
  if(!Number.isFinite(values[i]))continue
  const t=Math.max(0,Math.min(1,(values[i]-min)/Math.max(max-min,1e-30)))
  rgba.set(jetTable[Math.min(255,Math.floor(t*256))],4*i);rgba[4*i+3]=255
 }
 return rgba
}
