"""The behavior eval suite has to stay loadable and point at files that exist.

A case whose fixture path rots is worse than a missing case: the run still
happens, the agent sees less than the case describes, and the score moves for a
reason nobody recorded.
"""
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
EVALS = ROOT / 'evals/evals.json'
BASELINE = '[기준선]'


class EvalSuite(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(EVALS.read_text(encoding='utf-8'))
        self.cases = self.data['evals']

    def test_skill_name_matches_the_skill_directory(self):
        self.assertEqual(self.data['skill_name'], 'do-the-thing')
        self.assertTrue((ROOT / 'skills' / self.data['skill_name'] / 'SKILL.md').is_file())

    def test_case_ids_are_unique(self):
        ids = [case['id'] for case in self.cases]
        self.assertEqual(sorted(ids), sorted(set(ids)), 'duplicate eval id')

    def test_every_case_has_a_prompt_and_an_expected_output(self):
        for case in self.cases:
            with self.subTest(case=case['id']):
                self.assertTrue(case['prompt'].strip())
                self.assertTrue(case['expected_output'].strip())

    def test_every_referenced_fixture_exists(self):
        for case in self.cases:
            for name in case['files']:
                with self.subTest(case=case['id'], file=name):
                    self.assertTrue((ROOT / name).is_file(), f'missing fixture: {name}')

    def test_every_case_scores_something_beyond_the_baseline(self):
        for case in self.cases:
            scoring = [e for e in case['expectations'] if BASELINE not in e]
            with self.subTest(case=case['id']):
                self.assertTrue(scoring, 'case has only baseline expectations, so it measures nothing')

    def test_the_prompt_does_not_name_the_skill(self):
        # Naming it would load it in the arm that is supposed to run without it.
        for case in self.cases:
            with self.subTest(case=case['id']):
                self.assertNotIn('do-the-thing', case['prompt'])
                self.assertNotIn('두더띵', case['prompt'])


if __name__ == '__main__':
    unittest.main()
