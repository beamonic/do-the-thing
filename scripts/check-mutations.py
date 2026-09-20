#!/usr/bin/env python3
"""Delete each validator guard in turn and require the test suite to fail.

A guard no test covers can be removed without anyone noticing, which is exactly
what happened before 0.6: every test asserted only that some error appeared, so
an unrelated guard firing on the same fixture covered for the missing one. This
runs the suite once per mutation. A mutation that leaves the suite green names an
untested guard. A mutation whose pattern is gone names a guard that was renamed
or removed, which needs the list updated on purpose rather than silently.
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGET = ROOT / 'skills/do-the-thing/scripts/records.py'
MUTATIONS = ROOT / 'tests/mutations.json'


def run_suite(root):
    result = subprocess.run(
        [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests'],
        cwd=root, capture_output=True, text=True,
    )
    match = re.search(r'Ran (\d+) tests?', result.stderr)
    count = int(match.group(1)) if match else 0
    return result.returncode, count


def main():
    mutations = json.loads(MUTATIONS.read_text(encoding='utf-8'))
    original = TARGET.read_text(encoding='utf-8')
    survived, absent = [], []
    with tempfile.TemporaryDirectory(prefix='do-the-thing-mutations-') as temporary:
        root = pathlib.Path(temporary)
        for name in ('skills', 'tests', 'examples', 'scripts', 'evals'):
            source = ROOT / name
            # A repository without one of these still runs; the baseline check
            # below catches a copy that left the suite unable to pass.
            if not source.is_dir():
                continue
            shutil.copytree(source, root / name,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        code, baseline_count = run_suite(root)
        if code != 0 or baseline_count == 0:
            print('Baseline failed or ran zero tests; fix that first.', file=sys.stderr)
            return 2
        target = root / TARGET.relative_to(ROOT)
        for mutation in mutations:
            name, find = mutation['name'], mutation['find']
            if find not in original:
                absent.append(name)
                continue
            target.write_text(original.replace(find, mutation['replace'], 1), encoding='utf-8')
            # Same-size edits within one clock tick must not reuse stale bytecode.
            shutil.rmtree(target.parent / '__pycache__', ignore_errors=True)
            code, count = run_suite(root)
            print(f'{name}: {count} tests, exit {code}')
            if code == 0 or count != baseline_count:
                survived.append(name)
    for name in absent:
        print(f'pattern gone: {name}', file=sys.stderr)
    for name in survived:
        print(f'no test covers: {name}', file=sys.stderr)
    print(f'{len(mutations)} mutations, {len(survived)} survived, {len(absent)} patterns gone')
    return 1 if survived or absent else 0


if __name__ == '__main__':
    sys.exit(main())
