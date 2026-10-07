import { onMounted, onBeforeUnmount, type Ref } from 'vue'

// Keep axis labels at the requested slide-space size despite SVG viewBox scaling.
export function useSvgAxisText(root: Ref<HTMLElement | SVGSVGElement | undefined>, size=12, selector='svg') {
  let observer: ResizeObserver | undefined
  const update=()=>{
    const element=root.value
    if(!element)return
    const svgs=element instanceof SVGSVGElement?[element]:Array.from(element.querySelectorAll<SVGSVGElement>(selector))
    for(const svg of svgs){
      const box=svg.viewBox.baseVal
      const scale=Math.min(svg.clientWidth/box.width,svg.clientHeight/box.height)
      if(scale>0)svg.style.setProperty('--axis-text-size',`${size/scale}px`)
    }
  }
  onMounted(()=>{update();observer=new ResizeObserver(update);if(root.value)observer.observe(root.value)})
  onBeforeUnmount(()=>observer?.disconnect())
}
