#!/usr/bin/env python3
"""Hide which arm a run belongs to before it is graded.

Usage:
  python evals/scripts/blind_runs.py <workspace>/iteration-N --mapping <path outside the workspace>

Iteration 1 graded runs whose own path said `with_skill` or `without_skill`.
Every grader was told to ignore it, which is a mitigation and not blinding: the
thing being measured is the difference between those two arms, so a grader that
expects one to win can grade toward that expectation.

This copies each run to a directory named by a hash and writes the mapping
somewhere the graders are never pointed at. Blinding is still not complete — a
run that read the skill tends to quote it — but the label is gone from the path,
which is the cheap half of the problem.
"""
import argparse
import hashlib
import json
import pathlib
import shutil
import sys

ARMS = ('with_skill', 'without_skill')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('workspace', type=pathlib.Path)
    parser.add_argument('--mapping', type=pathlib.Path, required=True,
                        help='where to write the key; put it outside the workspace')
    parser.add_argument('--salt', default='iteration',
                        help='changes the hashes, so a grader cannot reuse a remembered one')
    args = parser.parse_args()

    ws = args.workspace.resolve()
    blind = ws / 'blind'
    if blind.exists():
        sys.exit(f'{blind} already exists; remove it or pick another workspace')
    if args.mapping.resolve().is_relative_to(ws):
        sys.exit('the mapping must live outside the workspace, or blinding is theatre')

    mapping = {}
    for case in sorted(p for p in ws.glob('eval-*') if p.is_dir()):
        for arm in ARMS:
            source = case / arm
            if not source.is_dir():
                continue
            token = hashlib.sha256(f'{args.salt}:{case.name}:{arm}'.encode()).hexdigest()[:8]
            target = blind / f'run-{token}'
            shutil.copytree(source, target,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            mapping[f'run-{token}'] = {'case': case.name, 'configuration': arm}

    if not mapping:
        sys.exit(f'no runs found under {ws}')

    args.mapping.parent.mkdir(parents=True, exist_ok=True)
    args.mapping.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding='utf-8')
    for token in sorted(mapping):
        print(token)
    print(f'\n{len(mapping)} runs blinded into {blind}', file=sys.stderr)
    print(f'key written to {args.mapping} -- do not give this path to a grader', file=sys.stderr)


if __name__ == '__main__':
    main()
