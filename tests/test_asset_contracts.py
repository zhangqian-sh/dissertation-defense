"""Meaningful corruption tests against the actual exported evidence."""
import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from collection_common import ROOT
from validate_defense_assets import validate_envelope, validate_manifest


class Contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=ROOT/'public/data/manifest.json'
        m=json.loads(cls.manifest.read_text())
        cls.assets={a['chapter']:json.loads((cls.manifest.parent/a['path']).read_text()) for a in m['assets']}

    def test_complete_bundle(self): validate_manifest(self.manifest)

    def reject(self, chapter, edit):
        e=copy.deepcopy(self.assets[chapter]); edit(e)
        with self.assertRaises((AssertionError,ValueError,KeyError)):
            validate_envelope(e)

    def test_old_schema_rejected(self):
        self.reject('ch02',lambda e:e.update(schema_version=1))

    def test_missing_case_rejected(self):
        self.reject('ch02',lambda e:e['data']['states'][0].pop('case_id'))

    def test_bad_time_alignment_rejected(self):
        self.reject('ch02',lambda e:e['data']['states'][0]['payload']['time']['values'].__setitem__(1,0))

    def test_corrupted_burgers_difference_rejected(self):
        self.reject('ch03',lambda e:e['data']['states'][0]['payload']['relative_error']['values'].__setitem__(0,123))

    def test_corrupted_binary_checksum_rejected(self):
        self.reject('ch03',lambda e:e['data']['states'][0]['payload']['frames'].update(sha256='0'*64))

    def test_missing_intermediate_step_rejected(self):
        self.reject('ch03',lambda e:e['data']['states'][0]['payload']['T']['values'].__setitem__(65,65))

    def test_wrong_event_agent_rejected(self):
        self.reject('ch07',lambda e:e['data']['states'][0]['payload']['critical_events'][0].update(agent_ids=[0,0]))

    def test_wrong_event_time_rejected(self):
        self.reject('ch07',lambda e:e['data']['states'][0]['payload']['critical_events'][0].update(time=-1))

    def test_nonfinite_rejected(self):
        self.reject('ch03',lambda e:e['data']['states'][0]['payload']['ann_output']['values'].__setitem__(0,float('nan')))

    def test_et_iteration_order_rejected(self):
        self.reject('ch05',lambda e:e['data']['states'][0]['payload']['iteration']['values'].__setitem__(1,1))

    def test_et_inconsistent_error_rejected(self):
        self.reject('ch05',lambda e:e['data']['states'][0]['payload']['relative_error']['values'].__setitem__(0,0))

    def test_et_material_replay_mismatch_rejected(self):
        self.reject('ch05',lambda e:e['data']['states'][0]['payload']['metadata'].update(final_relative_l2_difference_from_saved=.5))


if __name__=='__main__': unittest.main()
