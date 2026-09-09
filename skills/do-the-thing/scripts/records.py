#!/usr/bin/env python3
"""Validate completion evidence coverage. No network calls or issue mutations."""
import argparse
import json
import sys


def validate(record):
    errors = []
    if not isinstance(record, dict):
        return ['Record must be an object.']

    def header(value, label):
        """Check id and revision. Return the revision, or None if unusable."""
        if not isinstance(value, dict):
            errors.append(f'{label}: expected an object.')
            return None
        if not isinstance(value.get('id'), str) or not value['id'].strip():
            errors.append(f'{label}: nonempty id required.')
        revision = value.get('revision')
        if type(revision) is not int or revision < 1:
            errors.append(f'{label}: positive integer revision required.')
            return None
        return revision

    def big_criteria_of(value, label):
        criteria = value.get('criteria')
        if not isinstance(criteria, list) or not criteria or any(
            not isinstance(c, str) or not c.strip() for c in criteria
        ):
            errors.append(f'{label}: nonempty criterion IDs required.')
            return None
        if len(set(criteria)) != len(criteria):
            errors.append(f'{label}: duplicate criterion IDs.')
        return set(criteria)

    def mini_criteria_of(value, label, parents):
        """Map each Mini criterion to the Big criterion it serves."""
        criteria = value.get('criteria')
        if not isinstance(criteria, list) or not criteria:
            errors.append(f'{label}: nonempty criterion list required.')
            return None
        if any(isinstance(entry, str) for entry in criteria):
            errors.append(
                f'{label}: each criterion must be an object with id and parent; '
                'a bare list of IDs is the pre-0.7 format.'
            )
            return None
        mapping = {}
        for entry in criteria:
            if not isinstance(entry, dict):
                errors.append(f'{label}: criterion must be an object.')
                continue
            cid = entry.get('id')
            if not isinstance(cid, str) or not cid.strip():
                errors.append(f'{label}: nonempty criterion id required.')
                continue
            if cid in mapping:
                errors.append(f'{label}: duplicate criterion IDs.')
            parent = entry.get('parent')
            if not isinstance(parent, str) or parent not in parents:
                errors.append(f'{label}: criterion {cid} needs a parent drawn from the Big.')
                continue
            mapping[cid] = parent
        return mapping or None

    def checks(values, criteria, revision, label):
        """Return the criteria whose checks actually passed."""
        passed = set()
        if not isinstance(values, list):
            errors.append(f'{label}: checks must be a list.')
            return passed
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
            sound = True
            if type(check.get('revision')) is not int or check['revision'] != revision:
                errors.append(f'{label}: stale revision for {cid}.')
                sound = False
            if check.get('result') != 'pass':
                errors.append(f'{label}: {cid} has not passed.')
                sound = False
            for key in ('evidence', 'artifact_revision', 'method'):
                if not isinstance(check.get(key), str) or not check[key].strip():
                    errors.append(f'{label}: {cid} needs {key}.')
                    sound = False
            if sound:
                passed.add(cid)
        for cid in sorted(criteria - seen):
            errors.append(f'{label}: missing check for {cid}.')
        return passed

    big = record.get('big')
    big_revision = header(big, 'Big')
    big_criteria = None if big_revision is None else big_criteria_of(big, 'Big')
    if big_criteria is None:
        return errors
    minis = record.get('minis')
    if not isinstance(minis, list) or not minis:
        return errors + ['At least one Mini required.']
    ids, covered = set(), set()
    for index, mini in enumerate(minis):
        label = f'Mini[{index}]'
        revision = header(mini, label)
        if revision is None:
            continue
        mid = mini.get('id')
        if isinstance(mid, str):
            if mid in ids:
                errors.append(f'{label}: duplicate Mini ID.')
            ids.add(mid)
        if mini.get('parent_id') != big.get('id'):
            errors.append(f'{label}: wrong Big ID.')
        if type(mini.get('parent_revision')) is not int or mini['parent_revision'] != big_revision:
            errors.append(f'{label}: stale Big revision.')
        if 'parent_criteria' in mini:
            errors.append(f'{label}: parent_criteria was replaced by a parent on each criterion.')
        mapping = mini_criteria_of(mini, label, big_criteria)
        if mapping is None:
            continue
        passed = checks(mini.get('checks'), set(mapping), revision, label)
        covered.update(mapping[cid] for cid in passed)
    for cid in sorted(big_criteria - covered):
        errors.append(f'No Mini criterion passed for {cid}.')
    checks(record.get('big_checks'), big_criteria, big_revision, 'Big aggregate')
    return errors


def advisories(record):
    """Non-blocking notices about placeholder content. Structure is checked by validate()."""
    notes = []
    if not isinstance(record, dict):
        return notes
    if record.get('fictional') is True:
        notes.append('Record is flagged fictional; replace every check with an actual observation.')
    groups = [record.get('big_checks')]
    minis = record.get('minis')
    if isinstance(minis, list):
        groups.extend(mini.get('checks') for mini in minis if isinstance(mini, dict))
    placeholder = 0
    for group in groups:
        if not isinstance(group, list):
            continue
        for check in group:
            if isinstance(check, dict) and any(
                isinstance(check.get(key), str) and 'fictional' in check[key].lower()
                for key in ('evidence', 'artifact_revision', 'method')
            ):
                placeholder += 1
    if placeholder:
        notes.append(f'{placeholder} check(s) cite placeholder evidence naming "fictional".')
    return notes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', help='Completion record JSON file')
    args = parser.parse_args()
    try:
        with open(args.record, encoding='utf-8') as source:
            record = json.load(source)
    except (OSError, ValueError) as error:
        print(f'Cannot read record: {error}', file=sys.stderr)
        return 2
    errors = validate(record)
    print(json.dumps({'valid': not errors, 'errors': errors, 'warnings': advisories(record),
                      'notice': 'Coverage only; independently inspect evidence and current source revisions.'}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
