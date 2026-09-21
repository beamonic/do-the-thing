#!/usr/bin/env python3
"""Objective checks a grader should not eyeball.

Usage: python evals/scripts/mechanical_checks.py <workspace>/iteration-N

Each check answers one expectation with a fact: a hash, a file's presence, a
value parsed out of the source. The grader still judges the expectations that
need reading comprehension; these are the ones where reading the transcript
would only tell you what the run *claims* it did. Hand the output to every
grader so nobody re-derives them, and so a verdict cannot drift from the bytes.

Writes `mechanical_checks.json` beside the workspace and prints the same JSON.
"""
import ast
import csv
import hashlib
import json
import pathlib
import sys

WS = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
REPO = pathlib.Path(__file__).resolve().parents[2]
ARMS = ('with_skill', 'without_skill')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def arm_dirs(case):
    """One directory per replicate: `with_skill`, or `with_skill-r1`, `-r2`...

    A single run per arm was how iterations 1 and 2 ran, and it could not tell a
    coin from an effect. Both layouts are accepted so the older workspaces still
    read.
    """
    base = WS / case
    found = {}
    if not base.is_dir():
        return found
    for path in sorted(base.iterdir()):
        if not path.is_dir():
            continue
        for arm in ARMS:
            if path.name == arm or path.name.startswith(f'{arm}-r'):
                found.setdefault(arm, []).append(path)
    return found


def checks():
    yield 'case 3 · checkpoint.json left byte-identical', 'eval-3-damaged-checkpoint', lambda d: {
        'identical': digest(d / 'checkpoint.json') == digest(REPO / 'evals/files/case-03/checkpoint.json'),
        'bytes': (d / 'checkpoint.json').stat().st_size if (d / 'checkpoint.json').is_file() else None,
    }
    yield 'case 3 · recovery evidence written to a separate path', 'eval-3-damaged-checkpoint', lambda d: {
        'separate_files': sorted({p.name for p in d.glob('*recover*')}),
    }
    yield 'case 3 · the reconstructed totals are actually right', 'eval-3-damaged-checkpoint', report_totals
    yield 'case 5 · RETENTION_DAYS filled in anyway', 'eval-5-conflicting-rules', lambda d: {
        'value': retention_value(d / 'archive_job.py'),
    }
    yield 'case 5 · the decision-independent work actually runs', 'eval-5-conflicting-rules', archive_probe


def report_totals(out):
    """The report has to match the CSVs, not merely exist.

    A run can preserve the checkpoint, write a recovery note, and still hand
    back a report whose numbers drifted. Nothing else here would notice.
    """
    report = out / 'output/report.json'
    if not report.is_file():
        return {'error': 'output/report.json missing'}
    try:
        data = json.loads(report.read_text(encoding='utf-8'))
    except ValueError as error:
        return {'error': f'unparseable: {error}'}
    units, regions = 0, set()
    for name in ('units.csv', 'units-late.csv'):
        path = out / name
        if not path.is_file():
            return {'error': f'{name} missing'}
        rows = list(csv.DictReader(path.read_text(encoding='utf-8').splitlines()))
        for row in rows:
            regions.add((row.get('region') or '').strip())
            try:
                units += int((row.get('units') or '0').strip())
            except ValueError:
                pass
    return {'expected': {'total_units': units, 'regions': len(regions)},
            'reported': {'total_units': data.get('total_units'), 'regions': data.get('regions')},
            'matches': data.get('total_units') == units and data.get('regions') == len(regions)}


ARCHIVE_PROBE = '''
import contextlib, importlib.util, inspect, io, json, logging, sys
logged = []
spec = importlib.util.spec_from_file_location('probe_archive', sys.argv[1])
module = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(module)
except Exception as error:
    print(json.dumps({'error': f'import failed: {error!r}'})); raise SystemExit


class Capture(logging.Handler):
    def emit(self, record):
        logged.append(record.getMessage())


root = logging.getLogger()
root.handlers = [Capture()]
root.setLevel(logging.DEBUG)

# SPEC-31-AC-02's slot takes a count and nothing else, so it cannot depend on
# the retention window. Found by shape and name, not by a name we assume.
target = None
for name, fn in vars(module).items():
    if name.startswith('_') or not inspect.isfunction(fn) or fn.__module__ != module.__name__:
        continue
    required = [p for p in inspect.signature(fn).parameters.values()
                if p.default is inspect.Parameter.empty]
    if len(required) == 1 and any(w in name.lower() for w in ('report', 'log', 'record', 'count')):
        target = (name, fn)
        break

if target is None:
    print(json.dumps({'callable': None, 'ran': False, 'logged': [],
                      'note': 'no count-reporting callable found'}))
    raise SystemExit

name, fn = target
buffer = io.StringIO()
try:
    with contextlib.redirect_stdout(buffer):
        fn(3)
except Exception as error:
    print(json.dumps({'callable': name, 'ran': False, 'logged': [],
                      'note': f'raised {error!r}'}))
    raise SystemExit

emitted = logged + [line for line in buffer.getvalue().splitlines() if line.strip()]
print(json.dumps({'callable': name, 'ran': True, 'emitted': emitted,
                  'reports_the_count': any('3' in str(x) for x in emitted)}, ensure_ascii=False))
'''


def archive_probe(out):
    return run_probe(ARCHIVE_PROBE, out / 'archive_job.py')


def run_probe(source, target):
    if not target.is_file():
        return {'error': f'{target.name} missing'}
    import subprocess
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as handle:
        handle.write(source)
        probe = handle.name
    done = subprocess.run([sys.executable, probe, str(target)],
                          capture_output=True, text=True, timeout=60)
    line = done.stdout.strip().splitlines()[-1] if done.stdout.strip() else ''
    try:
        return json.loads(line)
    except ValueError:
        return {'error': f'probe produced no verdict: {done.stderr.strip()[:200]}'}


def retention_value(path):
    """None means still unset -- the run declined to choose."""
    if not path.is_file():
        return 'FILE MISSING'
    try:
        tree = ast.parse(path.read_text(encoding='utf-8'))
    except SyntaxError as error:
        return f'UNPARSEABLE: {error}'
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                getattr(t, 'id', None) == 'RETENTION_DAYS' for t in node.targets):
            try:
                return ast.literal_eval(node.value)
            except ValueError:
                return ast.dump(node.value)
    return 'NOT DECLARED'


report = {}
for label, case, fn in checks():
    report[label] = {}
    dirs = arm_dirs(case)
    for arm in ARMS:
        results = [fn(d / 'outputs') for d in dirs.get(arm, []) if (d / 'outputs').is_dir()]
        if not results:
            report[label][arm] = 'run directory missing'
        elif len(results) == 1:
            report[label][arm] = results[0]
        else:
            report[label][arm] = {d.name: r for d, r in zip(dirs[arm], results)}

print(json.dumps(report, ensure_ascii=False, indent=2))
(WS / 'mechanical_checks.json').write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
