"""Offline integrity and temporal ordering of recorded RFormer frames."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class RFormerTimeTests(unittest.TestCase):
    def test_time_sequences_and_integrity(self):
        for case, count in [('vortex',20),('jet',40)]:
            data=json.loads((ROOT/f'public/data/ch06/time/{case}.json').read_text())
            self.assertEqual(len(data['times']),count)
            self.assertEqual(len(data['frames']),count)
            self.assertEqual(sorted(data['source_rows']),list(range(count)))
            self.assertTrue(all(a<b for a,b in zip(data['times'],data['times'][1:])))
            for frame in data['frames']:
                path=ROOT/'public'/frame['path'].lstrip('/')
                self.assertTrue(path.resolve().is_relative_to(ROOT/'public/data/ch06/time'))
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),frame['sha256'])
            self.assertGreater(len({f['sha256'] for f in data['frames']}),1)
            self.assertTrue(all(v>0 for v in data['field_limits']))
            self.assertEqual(data['columns'],['Reference','Observations','RFormer'])
            if case=='jet':
                self.assertEqual(data['rows'],['velocity'])
                self.assertEqual(data['arrow_scale'],.08)
                self.assertIn('valid.h5',data['reference_source'])
                self.assertNotEqual(data['source_rows'],list(range(count)))
            else:
                self.assertEqual(data['rows'],['u','v','p'])
                self.assertEqual(data['times'],list(range(80,100)))
