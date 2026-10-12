// Component identities survive edits to presentation titles and slide order.
export const auditTargets={
 sms:'.sms-rollout',burgers:'.burgers-example',energy:'.energy-history',
 vortex:'.vortex-matrix',hybrid:'.hybrid-rformer-time',jet:'.rformer-jet',weather:'.sequence-weather',
 latent:'.ocformer-latent-reference',scaling:'.swarm-scaling',
 perturbation:'.oc-examples.perturbation',threeD:'.oc-examples.three-d',
}
export function slideByFeature(results,feature){
 if(!Object.hasOwn(auditTargets,feature))throw Error(`Unknown audit feature "${feature}"`)
 const matches=results.filter(result=>result.features.includes(feature))
 if(matches.length!==1)throw Error(`Expected one slide containing "${feature}", found ${matches.length}`)
 return matches[0].slide
}

// Runs inside the browser, where rectangles include rotation and CSS scaling.
export function clippedPlotLabels(svgs){
 return svgs.flatMap(svg=>{
  const box=svg.getBoundingClientRect(),tolerance=.5*box.width/svg.viewBox.baseVal.width
  return [...svg.querySelectorAll('text')].filter(text=>{
   const rect=text.getBoundingClientRect()
   return rect.left<box.left-tolerance||rect.top<box.top-tolerance||rect.right>box.right+tolerance||rect.bottom>box.bottom+tolerance
  }).map(text=>text.textContent)
 })
}
