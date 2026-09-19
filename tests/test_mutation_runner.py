"""Exercise the mutation command in a disposable miniature repository."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MutationRunnerTests(unittest.TestCase):
    def run_fixture(self, test_source):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ('scripts', 'skills/do-the-thing/scripts', 'tests', 'examples'):
                (root / name).mkdir(parents=True)
            shutil.copy2(ROOT / 'scripts/check-mutations.py', root / 'scripts/check-mutations.py')
            target = root / 'skills/do-the-thing/scripts/records.py'
            target.write_text('VALUE = 1\n', encoding='utf-8')
            before = target.stat().st_mtime_ns
            (root / 'tests/mutations.json').write_text(json.dumps([
                {'name': 'value', 'find': 'VALUE = 1', 'replace': 'VALUE = 2'}
            ]), encoding='utf-8')
            (root / 'tests/test_value.py').write_text(test_source, encoding='utf-8')
            result = subprocess.run([sys.executable, 'scripts/check-mutations.py'],
                                    cwd=root, capture_output=True, text=True)
            self.assertEqual('VALUE = 1\n', target.read_text(encoding='utf-8'))
            self.assertEqual(before, target.stat().st_mtime_ns, 'original must never be rewritten')
            return result

    def test_killed_mutation_never_touches_original(self):
        result = self.run_fixture(
            'import unittest\nfrom pathlib import Path\n'
            'class ValueTest(unittest.TestCase):\n'
            ' def test_value(self):\n'
            '  self.assertEqual("VALUE = 1\\n", Path("skills/do-the-thing/scripts/records.py").read_text())\n')
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('value: 1 tests, exit 1', result.stdout)

    def test_zero_tests_is_not_success(self):
        result = self.run_fixture('')
        self.assertEqual(2, result.returncode)
        self.assertIn('zero tests', result.stderr)

    def test_surviving_mutation_fails_gate(self):
        result = self.run_fixture(
            'import unittest\nclass ValueTest(unittest.TestCase):\n'
            ' def test_irrelevant(self):\n  self.assertTrue(True)\n')
        self.assertEqual(1, result.returncode)
        self.assertIn('no test covers: value', result.stderr)
