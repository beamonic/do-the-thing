#!/usr/bin/env python3
"""Aggregate the amount column across every CSV in a directory.

T-01 and T-02 are done. T-03 (JSON output), T-04 (empty directory), and T-05
(subprocess tests) are not started -- see plan.md.
"""
import csv
import pathlib
import sys


def read_rows(directory):
    for path in sorted(pathlib.Path(directory).glob('*.csv')):
        with path.open(newline='', encoding='utf-8') as handle:
            yield from csv.DictReader(handle)


def summarize(directory):
    total, count = 0.0, 0
    for row in read_rows(directory):
        raw = (row.get('amount') or '').strip()
        try:
            value = float(raw)
        except ValueError:
            continue
        total += value
        count += 1
    return total, count


if __name__ == '__main__':
    print(summarize(sys.argv[1]))
