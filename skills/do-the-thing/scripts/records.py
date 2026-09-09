#!/usr/bin/env python3
"""Validate completion evidence coverage. No network calls or issue mutations."""
import argparse
import json
import sys


def validate(record):
    errors = []
    if not isinstance(record, dict):
        return ['Record must be an object.']

    def spec(value, label):
        if not isinstance(value, dict):
            errors.append(f'{label}: expected an object.')
            return None
        if not isinstance(value.get('id'), str) or not value['id'].strip():
            errors.append(f'{label}: nonempty id required.')
        revision = value.get('revision')
        if type(revision) is not int or revision < 1:
            errors.append(f'{label}: positive integer revision required.')
        criteria = value.get('criteria')
        if not isinstance(criteria, list) or not criteria or any(
            not isinstance(c, str) or not c.strip() for c in criteria
        ):
            errors.append(f'{label}: nonempty criterion IDs required.')
            return None
        if len(set(criteria)) != len(criteria):
            errors.append(f'{label}: duplicate criterion IDs.')
        return set(criteria)

    def checks(values, criteria, revision, label):
        if not isinstance(values, list):
            errors.append(f'{label}: checks must be a list.')
            return
        seen = set()
        for check in values:
            if not isinstance(check, dict):
                errors.append(f'{label}: check must be an object.')
                continue
            cid = check.get('criterion')
            if not isinstance(cid, str) or cid not in criteria:
                errors.append(f'{label}: unknown criterion.')
                continue
            if cid in seen:
                errors.append(f'{label}: duplicate check for {cid}.')
            seen.add(cid)
            if type(check.get('revision')) is not int or check['revision'] != revision:
                errors.append(f'{label}: stale revision for {cid}.')
            if check.get('result') != 'pass':
                errors.append(f'{label}: {cid} has not passed.')
            for key in ('evidence', 'artifact_revision', 'method'):
                if not isinstance(check.get(key), str) or not check[key].strip():
                    errors.append(f'{label}: {cid} needs {key}.')
        for cid in sorted(criteria - seen):
            errors.append(f'{label}: missing check for {cid}.')

    big = record.get('big')
    big_criteria = spec(big, 'Big')
    if big_criteria is None:
        return errors
    minis = record.get('minis')
    if not isinstance(minis, list) or not minis:
        return errors + ['At least one Mini required.']
    ids, covered = set(), set()
    for index, mini in enumerate(minis):
        label = f'Mini[{index}]'
        criteria = spec(mini, label)
        if criteria is None:
            continue
        mid = mini.get('id')
        if isinstance(mid, str):
            if mid in ids:
                errors.append(f'{label}: duplicate Mini ID.')
            ids.add(mid)
        if mini.get('parent_id') != big.get('id'):
            errors.append(f'{label}: wrong Big ID.')
        if type(mini.get('parent_revision')) is not int or mini['parent_revision'] != big.get('revision'):
            errors.append(f'{label}: stale Big revision.')
        refs = mini.get('parent_criteria')
        if not isinstance(refs, list) or not refs or any(not isinstance(c, str) or c not in big_criteria for c in refs):
            errors.append(f'{label}: valid parent criteria required.')
        else:
            covered.update(refs)
        checks(mini.get('checks'), criteria, mini.get('revision'), label)
    if big_criteria - covered:
        errors.append('Some Big criteria have no responsible Mini.')
    checks(record.get('big_checks'), big_criteria, big.get('revision'), 'Big aggregate')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', help='Completion record JSON file')
    args = parser.parse_args()
    try:
        with open(args.record, encoding='utf-8') as source:
            errors = validate(json.load(source))
    except (OSError, ValueError) as error:
        print(f'Cannot read record: {error}', file=sys.stderr)
        return 2
    print(json.dumps({'valid': not errors, 'errors': errors,
                      'notice': 'Coverage only; independently inspect evidence and current source revisions.'}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
