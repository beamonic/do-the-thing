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
import hashlib
import json
import pathlib
import sys

WS = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
REPO = pathlib.Path(__file__).resolve().parents[2]
ARMS = ('with_skill', 'without_skill')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def out(case, arm):
    return WS / case / arm / 'outputs'


def checks():
    yield 'case 3 · checkpoint.json left byte-identical', 'eval-3-damaged-checkpoint', lambda d: {
        'identical': digest(d / 'checkpoint.json') == digest(REPO / 'evals/files/case-03/checkpoint.json'),
        'bytes': (d / 'checkpoint.json').stat().st_size if (d / 'checkpoint.json').is_file() else None,
    }
    yield 'case 3 · recovery evidence written to a separate path', 'eval-3-damaged-checkpoint', lambda d: {
        'separate_files': sorted({p.name for p in d.glob('*recover*')}),
    }
    yield 'case 1 · SPEC-17.md left unmodified', 'eval-1-spec-handover', lambda d: {
        'identical': digest(d / 'SPEC-17.md') == digest(REPO / 'evals/files/case-01/SPEC-17.md'),
    }
    yield 'case 1 · summary.py actually changed', 'eval-1-spec-handover', lambda d: {
        'changed': digest(d / 'summary.py') != digest(REPO / 'evals/files/case-01/summary.py'),
    }
    yield 'case 2 · uploader.py actually changed', 'eval-2-delegated-naming', lambda d: {
        'changed': digest(d / 'uploader.py') != digest(REPO / 'evals/files/case-02/uploader.py'),
    }
    yield 'case 5 · RETENTION_DAYS filled in anyway', 'eval-5-conflicting-rules', lambda d: {
        'value': retention_value(d / 'archive_job.py'),
    }
    yield 'case 1 · SPEC-17 rev 3 cited in files the run itself wrote', 'eval-1-spec-handover', lambda d: cited(
        d, REPO / 'evals/files/case-01')
    yield 'case 2 · retry delay actually grows between attempts', 'eval-2-delegated-naming', lambda d: backoff(d)


def authored(out, fixtures):
    """Files the run created or changed -- an untouched fixture is not its work."""
    names = []
    for path in sorted(out.rglob('*')):
        if not path.is_file() or '__pycache__' in path.parts or '.git' in path.parts:
            continue
        original = fixtures / path.name
        if not original.is_file() or digest(original) != digest(path):
            names.append(path)
    return names


def cited(out, fixtures):
    hits = []
    for path in authored(out, fixtures):
        try:
            text = path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            continue
        if 'SPEC-17' in text and ('revision 3' in text or 'rev 3' in text or 'rev3' in text):
            hits.append(path.name)
    return {'files_the_run_wrote': [p.name for p in authored(out, fixtures)], 'citing': hits}


BACKOFF_PROBE = '''
import importlib.util, inspect, json, sys, time
calls = []
time.sleep = lambda s: calls.append(s)            # bound before import, so defaults capture it
spec = importlib.util.spec_from_file_location('probe_uploader', sys.argv[1])
module = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(module)
except Exception as error:
    print(json.dumps({'error': f'import failed: {error!r}'})); raise SystemExit


class Boom(Exception):
    pass


class Client:
    def put(self, payload):
        raise Boom('always fails')


result = {'error': 'no retry wrapper found'}
for name, fn in vars(module).items():
    if name.startswith('_') or name == 'perform_upload' or not inspect.isfunction(fn):
        continue
    if fn.__module__ != module.__name__:
        continue
    calls.clear()
    try:
        fn('payload', Client())
    except Boom:
        pass
    except Exception as error:
        result = {'error': f'{name} raised {error!r} instead of the upload error'}
        continue
    else:
        result = {'error': f'{name} swallowed the failure instead of re-raising'}
        continue
    result = {'callable': name, 'sleep_calls': calls[:],
              'grows': len(calls) >= 2 and all(b > a for a, b in zip(calls, calls[1:]))}
    break
print(json.dumps(result))
'''


def backoff(out):
    target = out / 'uploader.py'
    if not target.is_file():
        return {'error': 'uploader.py missing'}
    import subprocess
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as handle:
        handle.write(BACKOFF_PROBE)
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
    for arm in ARMS:
        d = out(case, arm)
        report[label][arm] = fn(d) if d.is_dir() else 'run directory missing'

print(json.dumps(report, ensure_ascii=False, indent=2))
(WS / 'mechanical_checks.json').write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
