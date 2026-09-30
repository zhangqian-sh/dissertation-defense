from pathlib import Path
import numpy as np
root=Path('/oscar/data/gk/qzhang64/Projects/SpikingNN/Conversion/SNN-CAACT')
paths=[root/'result/burgers/T=0064/Tanh/advanced_caa',*[root/f'bak/result/{s}/T={t:04d}/Tanh/advanced_caa' for s,t in [('burgers-seed0',64),('burgers-seed0',128),('burgers-nu0.01-T=128',128),('burgers-nu0.01-T=1024',1024)]]]
cases=[]
for path in paths:
    x=np.loadtxt(path/'snn_x.csv',delimiter=','); y=np.loadtxt(path/'snn_y.csv',delimiter=','); ref=np.loadtxt(path/'snn_y_true.csv',delimiter=',');ann=np.loadtxt(path/'ann_y.csv',delimiter=',');ax=np.loadtxt(path/'ann_x.csv',delimiter=',')
    idx=np.lexsort((x[:,1],x[:,0])); ai=np.lexsort((ax[:,1],ax[:,0]))
    cases.append((x[idx],ref[idx],ann[ai]))
    print(path, 'shape',x.shape,'unique',[len(np.unique(x[:,i])) for i in range(2)],'L2',np.linalg.norm(y-ref)/np.linalg.norm(ref),flush=True)
for i,a in enumerate(cases):
    for j,b in enumerate(cases[:i]):
        print(i,j,'same shape',a[0].shape==b[0].shape,'max diffs', [float(np.max(np.abs(v-w))) if v.shape==w.shape else None for v,w in zip(a,b)],flush=True)
