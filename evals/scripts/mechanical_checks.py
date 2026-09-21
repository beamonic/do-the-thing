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
