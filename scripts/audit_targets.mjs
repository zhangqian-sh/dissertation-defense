// Component identities survive edits to presentation titles and slide order.
export const auditTargets={
 sms:'.sms-rollout',burgers:'.burgers-example',energy:'.energy-history',
 vortex:'.vortex-matrix',jet:'.rformer-jet',weather:'.sequence-weather',
 latent:'.ocformer-latent-reference',scaling:'.swarm-scaling',
 perturbation:'.oc-examples.perturbation',threeD:'.oc-examples.three-d',
}
export function slideByFeature(results,feature){
 if(!Object.hasOwn(auditTargets,feature))throw Error(`Unknown audit feature "${feature}"`)
 const matches=results.filter(result=>result.features.includes(feature))
 if(matches.length!==1)throw Error(`Expected one slide containing "${feature}", found ${matches.length}`)
 return matches[0].slide
}
