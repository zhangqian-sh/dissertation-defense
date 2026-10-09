import unittest,json,hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
class AddedSequences(unittest.TestCase):
    def test_all_frames_and_time_axes(self):
        for name,count in [('latent',200),('swarm128',200),('weather',366)]:
            d=json.loads((ROOT/f'public/data/animations/{name}/index.json').read_text())
            self.assertEqual(len(d['frames']),count)
            self.assertEqual(len(d['labels']),count)
            self.assertTrue(np.all(np.diff(d['times'])>0))
            bundle=(ROOT/'public'/d['bundle']['path'].lstrip('/')).read_bytes()
            self.assertEqual(hashlib.sha256(bundle).hexdigest(),d['bundle']['sha256'])
            for f in d['frames']:
                self.assertEqual(hashlib.sha256(bundle[f['offset']:f['offset']+f['length']]).hexdigest(),f['sha256'])
            fallback=ROOT/f'public/fallback_figures/sequences/{name}.png'
            self.assertEqual(hashlib.sha256(fallback.read_bytes()).hexdigest(),d['frames'][0]['sha256'])
            if name=='latent':
                self.assertFalse(d['illustrative']);self.assertEqual(d['positions_shape'],[200,8,2]);self.assertLess(d['central_reference_max_radius'],.003)
            if name=='swarm128':
                self.assertEqual(d['positions_shape'],[200,128,2])
                rng=np.random.default_rng(5);self.assertEqual(d['paper_colors'],['#%06X'%rng.integers(0,0xFFFFFF) for _ in range(128)])
            if name=='weather':self.assertEqual(d['labels'][0],'2024-01-01');self.assertEqual(d['labels'][-1],'2024-12-31');self.assertEqual(d['columns'],['Reference','Reconstructed'])
    def test_published_blood_snapshots(self):
        d=json.loads((ROOT/'docs/blood_snapshot_sources.json').read_text())
        self.assertEqual(len(d),2)
        for f in d:self.assertEqual(hashlib.sha256((ROOT/f['output']).read_bytes()).hexdigest(),f['output_sha256'])
