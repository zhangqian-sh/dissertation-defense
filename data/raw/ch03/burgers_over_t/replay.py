"""Fresh source-code CAA calibration and actual emitted-output prefix capture."""
import os,sys,json,hashlib,copy,subprocess
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import h5py
import torch
ROOT=Path(__file__).resolve().parents[4]
CODE=Path('/users/qzhang64/Projects/SpikingNN/Conversion/SNN-CAACT')
SOURCE=Path('/oscar/data/gk/qzhang64/Projects/SpikingNN/Conversion/SNN-CAACT')
assert os.environ.get('SLURM_JOB_ID') and torch.cuda.is_available()
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'-prefix-'+os.environ['SLURM_JOB_ID']
raw=Path(__file__).parent/'runs'/stamp;raw.mkdir(parents=True)
os.environ.update(ACTIVATION='Tanh',CAACT='True',SAVE_PATH=str(raw)+'/')
sys.path.insert(0,str(CODE))
from src.conversion.models.mlp import MLP
from src.conversion.models.spiking_layer import SpikeModel,SpikeModule,get_maximum_activation
from src.conversion.models.calibration import weights_cali_model
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
torch.manual_seed(0);np.random.seed(0);torch.set_num_threads(4)
torch.backends.cuda.matmul.allow_tf32=False
checkpoint=SOURCE/'saved_model/burgers/burgers-seed0.h5'
ann=MLP([2,40,40,40,40,40,40,1],activation='Tanh',use_bn=False)
with h5py.File(checkpoint) as f:
    params=[]
    for _,layer in f['params'].items():params.extend([layer['kernel'][()].T,layer['bias'][()]])
sd=ann.state_dict();assert len(params)==len(sd)
ann.load_state_dict({k:torch.tensor(v) for k,v in zip(sd,params)},strict=True)
ann=ann.cuda().eval()
folder=SOURCE/'bak/result/burgers-seed0/T=0128/Tanh/advanced_caa'
x=np.loadtxt(folder/'ann_x.csv',delimiter=',').astype(np.float32)
saved_ann=np.loadtxt(folder/'ann_y.csv',delimiter=',').astype(np.float32)
reference=np.loadtxt(folder/'ann_y_true.csv',delimiter=',').reshape(201,300)
time=np.unique(x[:,0]);space=np.unique(x[:,1])
np.testing.assert_allclose(reference[0],np.sin(space),atol=3e-7)
np.testing.assert_allclose(reference[:,[0,-1]],0,atol=1e-7)
order=np.lexsort((x[:,1],x[:,0]));x=x[order];saved_ann=saved_ann[order]
with torch.no_grad():ann_output=ann(torch.tensor(x,device='cuda')).cpu().numpy().ravel()
if not np.allclose(ann_output,saved_ann,atol=2e-6,rtol=2e-5):
    probe=np.linspace(0,len(x)-1,1024,dtype=int);best=(float('inf'),checkpoint)
    for candidate in [SOURCE/'saved_model/burgers.h5',*sorted((SOURCE/'saved_model/burgers').glob('*.h5'))]:
        with h5py.File(candidate) as f:
            params=[]
            for _,layer in f['params'].items():params.extend([layer['kernel'][()].T,layer['bias'][()]])
        try:ann.load_state_dict({k:torch.tensor(v,device='cuda') for k,v in zip(sd,params)},strict=True)
        except RuntimeError:continue
        with torch.no_grad():prediction=ann(torch.tensor(x[probe],device='cuda')).cpu().numpy().ravel()
        discrepancy=float(np.max(np.abs(prediction-saved_ann[probe])))
        print('ANN candidate',candidate.name,'max discrepancy',discrepancy,flush=True)
        if discrepancy<best[0]:best=(discrepancy,candidate)
    checkpoint=best[1]
    with h5py.File(checkpoint) as f:
        params=[]
        for _,layer in f['params'].items():params.extend([layer['kernel'][()].T,layer['bias'][()]])
    ann.load_state_dict({k:torch.tensor(v,device='cuda') for k,v in zip(sd,params)},strict=True)
    with torch.no_grad():ann_output=ann(torch.tensor(x,device='cuda')).cpu().numpy().ravel()
ann_discrepancy=float(np.linalg.norm(ann_output-saved_ann)/np.linalg.norm(saved_ann))
assert ann_discrepancy<1e-5, 'No matching original ANN checkpoint found'
print('Selected ANN',checkpoint,'archived relative discrepancy',ann_discrepancy,'GPU',torch.cuda.get_device_name(),flush=True)
selection=np.random.default_rng(0).choice(len(x),8192,replace=False)
calib=torch.utils.data.TensorDataset(torch.tensor(x[selection]),torch.zeros(8192))
loader=torch.utils.data.DataLoader(calib,batch_size=1024,shuffle=False,num_workers=0)
snn=SpikeModel(copy.deepcopy(ann),sim_length=128).cuda()
with torch.no_grad():get_maximum_activation(loader,snn,momentum=.9,iters=5,mse=True,sim_length=128,channel_wise=False)
weights_cali_model(snn,loader,learning_rate=1e-3,optimize_iter=5000,batch_size=1024,num_cali_samples=8192)
snn.set_spike_state(True);snn.eval()
modules={name:m for name,m in snn.named_modules() if isinstance(m,SpikeModule)}
state=dict(state_dict=snn.state_dict(),thresholds={name:(m.threshold_positive,m.threshold_negative,m.mem_pot_init) for name,m in modules.items()},calibration_T=128)
torch.save(state,raw/'snn_checkpoint.pt')
spikes=np.empty((128,len(x)),dtype=np.float32)
with torch.no_grad():
    for start in range(0,len(x),4096):
        inp=torch.tensor(x[start:start+4096],device='cuda');snn.init_membrane_potential();total=torch.zeros((len(inp),1),device='cuda')
        for step in range(128):
            emitted=snn.model(inp);total+=emitted;spikes[step,start:start+len(inp)]=emitted.cpu().numpy().ravel()
        ordinary=snn(inp)
        torch.testing.assert_close(total/128,ordinary,atol=2e-6,rtol=2e-5)
        print('Captured nodes',start+len(inp),'/',len(x),flush=True)
frames=(np.cumsum(spikes.astype(np.float64),axis=0)/np.arange(1,129)[:,None]).astype(np.float32).reshape(128,201,300)
relative=np.linalg.norm((frames-reference).reshape(128,-1),axis=1)/np.linalg.norm(reference)
print('Relative errors k=1,16,32,64,96,128:',relative[[0,15,31,63,95,127]],flush=True)
assert np.isfinite(frames).all() and relative[-1]<.25, 'Do not publish a failed conversion'
arrays=dict(T=np.arange(1,129,dtype=np.int32),frames=frames,reference=reference,relative_error=relative,time=time,space=space,ann_output=ann_output.reshape(201,300),step_spikes=spikes.reshape(128,201,300),calibration_indices=selection)
np.savez_compressed(raw/'payload.npz',**arrays)
files=[checkpoint,folder/'ann_x.csv',folder/'ann_y.csv',folder/'ann_y_true.csv',CODE/'src/conversion/models/spiking_layer.py',CODE/'src/conversion/models/calibration.py',Path(__file__)]
meta=dict(schema_version=2,case_id='burgers_seed0_fresh_prefix',run_id=stamp,source_repository=str(CODE),
 source_commit=subprocess.check_output(['git','-C',str(CODE),'rev-parse','HEAD'],text=True).strip(),source_dirty_state=subprocess.check_output(['git','-C',str(CODE),'status','--short'],text=True),
 configuration_sha256=sha(__file__),checkpoint_sha256=sha(checkpoint),converted_checkpoint_sha256=sha(raw/'snn_checkpoint.pt'),
 environment=dict(torch=torch.__version__,numpy=np.__version__,gpu=torch.cuda.get_device_name()),slurm={k:v for k,v in os.environ.items() if k.startswith('SLURM_')},
 sample_ids=['entire 201x300 grid'],split='original PINN residual grid; no held-out generalization claim',normalization='none; restored time-major reference layout',
 units=dict(field='u, benchmark units',space='x in [0,2π]',time='physical t in [0,4]',T='cumulative emitted-output prefix length; calibration horizon fixed at 128'),
 shapes={k:list(v.shape) for k,v in arrays.items()},command='python data/raw/ch03/burgers_over_t/replay.py',payload_sha256=sha(raw/'payload.npz'),input_files=[dict(path=str(p),sha256=sha(p)) for p in files],
 protocol='Fresh source-code advanced CAA calibration at fixed horizon 128; 8192 seeded calibration nodes, minibatch 1024, 5000 weight iterations per layer. All 128 frames are measured cumulative means of actual emitted outputs; no temporal interpolation and no per-prefix recalibration.',
 archived_calibration_reproduced=False,ann_archived_relative_discrepancy=ann_discrepancy,calibration_T=128,relative_error_at_128=float(relative[-1]))
(raw/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
print('READY_RAW',raw,flush=True)
