"""Each guard gets a test that names the error it must raise.

A test that only asserts "some error appeared" passes even when the guard it is
named after has been deleted, because an unrelated guard fires on the same
fixture. Assert the message so removing a guard fails its own test.
"""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('records', ROOT / 'skills/do-the-thing/scripts/records.py')
records = importlib.util.module_from_spec(spec)
spec.loader.exec_module(records)


def base():
    return {
        'big': {'id': 'BIG-001', 'revision': 1, 'criteria': ['BIG-AC-01']},
        'minis': [{
            'id': 'MINI-001', 'revision': 1, 'criteria': ['MINI-AC-01'],
            'parent_id': 'BIG-001', 'parent_revision': 1, 'parent_criteria': ['BIG-AC-01'],
            'checks': [{'criterion': 'MINI-AC-01', 'revision': 1, 'result': 'pass',
                        'method': 'Ran the page check', 'evidence': 'reports/mini-001.txt',
                        'artifact_revision': 'a1b2c3d'}],
        }],
        'big_checks': [{'criterion': 'BIG-AC-01', 'revision': 1, 'result': 'pass',
                        'method': 'Walked the whole journey', 'evidence': 'reports/big-001.txt',
                        'artifact_revision': 'a1b2c3d'}],
    }


class GuardTests(unittest.TestCase):
    def assertRaisesError(self, record, fragment):
        errors = records.validate(record)
        self.assertTrue(
            any(fragment in error for error in errors),
            f'expected an error containing {fragment!r}, got {errors}',
        )

    def test_valid_record_has_no_errors(self):
        self.assertEqual([], records.validate(base()))

    def test_shipped_example_is_valid(self):
        self.assertEqual([], records.validate(json.loads((ROOT / 'examples/completion.json').read_text())))

    def test_wrong_parent_id(self):
        record = base()
        record['minis'][0]['parent_id'] = 'OTHER'
        self.assertRaisesError(record, 'wrong Big ID')

    def test_stale_parent_revision(self):
        record = base()
        record['minis'][0]['parent_revision'] = 99
        self.assertRaisesError(record, 'stale Big revision')

    def test_big_criterion_without_a_responsible_mini(self):
        record = base()
        record['big']['criteria'].append('BIG-AC-02')
        record['big_checks'].append(dict(record['big_checks'][0], criterion='BIG-AC-02'))
        self.assertRaisesError(record, 'no responsible Mini')

    def test_duplicate_mini_id(self):
        record = base()
        record['minis'].append(copy.deepcopy(record['minis'][0]))
        self.assertRaisesError(record, 'duplicate Mini ID')

    def test_failed_check(self):
        record = base()
        record['minis'][0]['checks'][0]['result'] = 'fail'
        self.assertRaisesError(record, 'has not passed')

    def test_missing_evidence_fields(self):
        for key in ('evidence', 'method', 'artifact_revision'):
            with self.subTest(field=key):
                record = base()
                record['minis'][0]['checks'][0][key] = '   '
                self.assertRaisesError(record, f'needs {key}')

    def test_stale_check_revision(self):
        record = base()
        record['minis'][0]['checks'][0]['revision'] = 99
        self.assertRaisesError(record, 'stale revision for MINI-AC-01')

    def test_criterion_without_a_check(self):
        record = base()
        record['minis'][0]['criteria'].append('MINI-AC-02')
        self.assertRaisesError(record, 'missing check for MINI-AC-02')

    def test_check_against_unknown_criterion(self):
        record = base()
        record['minis'][0]['checks'][0]['criterion'] = 'NOT-A-CRITERION'
        self.assertRaisesError(record, 'unknown criterion')

    def test_duplicate_criterion_ids(self):
        record = base()
        record['minis'][0]['criteria'].append('MINI-AC-01')
        self.assertRaisesError(record, 'duplicate criterion IDs')

    def test_duplicate_check_for_one_criterion(self):
        record = base()
        record['minis'][0]['checks'].append(copy.deepcopy(record['minis'][0]['checks'][0]))
        self.assertRaisesError(record, 'duplicate check for MINI-AC-01')

    def test_minis_alone_cannot_close_the_big(self):
        record = base()
        record['big_checks'] = []
        self.assertRaisesError(record, 'Big aggregate: missing check for BIG-AC-01')

    def test_parent_criteria_must_exist_on_the_big(self):
        record = base()
        record['minis'][0]['parent_criteria'] = ['NOT-A-CRITERION']
        self.assertRaisesError(record, 'valid parent criteria required')

    def test_empty_spec_id(self):
        record = base()
        record['big']['id'] = '  '
        self.assertRaisesError(record, 'Big: nonempty id required')

    def test_non_positive_revision(self):
        record = base()
        record['big']['revision'] = 0
        self.assertRaisesError(record, 'positive integer revision required')

    def test_boolean_is_not_a_revision(self):
        record = base()
        record['big']['revision'] = True
        self.assertRaisesError(record, 'positive integer revision required')

    def test_no_minis(self):
        record = base()
        record['minis'] = []
        self.assertRaisesError(record, 'At least one Mini required')

    def test_malformed_input_does_not_crash(self):
        for value in [None, [], {}, {'big': []}, {'big': base()['big'], 'minis': 'nope'}]:
            with self.subTest(value=value):
                self.assertTrue(records.validate(value))


class AdvisoryTests(unittest.TestCase):
    def test_clean_record_has_no_warnings(self):
        self.assertEqual([], records.advisories(base()))

    def test_fictional_flag_is_reported(self):
        record = dict(base(), fictional=True)
        self.assertTrue(any('flagged fictional' in note for note in records.advisories(record)))

    def test_placeholder_evidence_is_counted(self):
        record = base()
        record['minis'][0]['checks'][0]['evidence'] = 'fictional://demo/check'
        self.assertTrue(any('1 check(s)' in note for note in records.advisories(record)))

    def test_shipped_example_warns_but_stays_structurally_valid(self):
        record = json.loads((ROOT / 'examples/completion.json').read_text())
        self.assertEqual([], records.validate(record))
        self.assertTrue(records.advisories(record))

    def test_advisories_tolerate_malformed_input(self):
        for value in [None, [], 'x', {'minis': 'nope'}, {'big_checks': [None]}]:
            with self.subTest(value=value):
                self.assertEqual([], records.advisories(value))


if __name__ == '__main__':
    unittest.main()
