import { ref, watch, onBeforeUnmount, type Ref } from 'vue'
import { useIsSlideActive } from '@slidev/client'
export function usePlayback(count:Ref<number>,initial=0,ms=100){
  const index=ref(initial); const playing=ref(false); const active=useIsSlideActive()
  let timer:ReturnType<typeof setInterval>|undefined
  const pause=()=>{playing.value=false; if(timer)clearInterval(timer);timer=undefined}
  const toggle=()=>{if(playing.value){pause();return} if(!active.value)return; if(index.value>=count.value-1)index.value=0; playing.value=true;timer=setInterval(()=>{if(index.value>=count.value-1)pause();else index.value++},ms)}
  const seek=(n:number)=>{pause();index.value=Math.max(0,Math.min(count.value-1,Math.round(n)))}
  const reset=()=>seek(initial)
  const hidden=()=>{if(document.hidden)pause()}
  document.addEventListener('visibilitychange',hidden)
  watch(active,v=>{if(!v)pause()})
  onBeforeUnmount(()=>{pause();document.removeEventListener('visibilitychange',hidden)})
  return {index,playing,active,toggle,pause,seek,reset}
}
