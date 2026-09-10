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
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGET = ROOT / 'skills/do-the-thing/scripts/records.py'
MUTATIONS = ROOT / 'tests/mutations.json'


def run_suite():
    return subprocess.run(
        [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests'],
        cwd=ROOT, capture_output=True, text=True,
    ).returncode


def main():
    mutations = json.loads(MUTATIONS.read_text(encoding='utf-8'))
    original = TARGET.read_text(encoding='utf-8')
    if run_suite() != 0:
        print('The suite fails before any mutation; fix that first.', file=sys.stderr)
        return 2
    survived, absent = [], []
    try:
        for mutation in mutations:
            name, find = mutation['name'], mutation['find']
            if find not in original:
                absent.append(name)
                continue
            TARGET.write_text(original.replace(find, mutation['replace'], 1), encoding='utf-8')
            if run_suite() == 0:
                survived.append(name)
    finally:
        TARGET.write_text(original, encoding='utf-8')
    for name in absent:
        print(f'pattern gone: {name}', file=sys.stderr)
    for name in survived:
        print(f'no test covers: {name}', file=sys.stderr)
    print(f'{len(mutations)} mutations, {len(survived)} survived, {len(absent)} patterns gone')
    return 1 if survived or absent else 0


if __name__ == '__main__':
    sys.exit(main())
