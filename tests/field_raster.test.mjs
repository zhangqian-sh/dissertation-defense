import test from 'node:test'
import assert from 'node:assert/strict'
import {meshRaster,interpolateRaster,scalarColors} from '../composables/fieldRaster.mjs'
const xy=[0,0,1,0,1,1,0,1],tri=[0,1,2,0,2,3]
test('native triangle raster covers the square without seams',()=>{
 const raster=meshRaster(xy,tri,32),values=interpolateRaster(raster,[1,1,1,1])
 for(const v of values)assert.ok(Math.abs(v-1)<1e-6)
 const rgba=scalarColors(values,1);for(let i=3;i<rgba.length;i+=4)assert.equal(rgba[i],255)
})
test('barycentric interpolation reproduces a linear scalar field',()=>{
 const size=32,values=interpolateRaster(meshRaster(xy,tri,size),[0,1,3,2])
 for(let r=0;r<size;r++)for(let c=0;c<size;c++)assert.ok(Math.abs(values[r*size+c]-((c+.5)/size+2*(1-(r+.5)/size)))<1e-6)
})
test('fixed color scale exposes changing signed error without geometry artifacts',()=>{
 const raster=meshRaster(xy,tri,16)
 const first=scalarColors(interpolateRaster(raster,[-1,1,1,-1]),1)
 const last=scalarColors(interpolateRaster(raster,[-.01,.01,.01,-.01]),1)
 assert.notDeepEqual(first,last)
 for(let i=3;i<first.length;i+=4)assert.equal(first[i],last[i])
})
