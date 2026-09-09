import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('records', ROOT / 'skills/do-the-thing/scripts/records.py')
records = importlib.util.module_from_spec(spec)
spec.loader.exec_module(records)


class CompletionTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT / 'examples/completion.json').read_text())

    def test_complete_record(self):
        self.assertEqual([], records.validate(self.record))

    def test_minis_alone_cannot_close_big(self):
        self.record['big_checks'] = []
        self.assertTrue(records.validate(self.record))

    def test_parent_revision_change_requires_review(self):
        self.record['big']['revision'] += 1
        self.assertTrue(records.validate(self.record))

    def test_failure_or_missing_evidence_blocks_completion(self):
        for field, value in [('result', 'fail'), ('evidence', ''), ('revision', 99)]:
            record = copy.deepcopy(self.record)
            record['minis'][0]['checks'][0][field] = value
            self.assertTrue(records.validate(record))

    def test_duplicate_mini_is_rejected(self):
        self.record['minis'].append(copy.deepcopy(self.record['minis'][0]))
        self.assertTrue(records.validate(self.record))

    def test_wrong_parent_is_rejected(self):
        self.record['minis'][0]['parent_id'] = 'OTHER'
        self.assertTrue(records.validate(self.record))

    def test_malformed_input_does_not_crash(self):
        for value in [None, [], {}, {'big': []}]:
            self.assertTrue(records.validate(value))


if __name__ == '__main__':
    unittest.main()
