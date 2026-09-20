"""Nightly transcript archive job.

The retention window is read from settings. See SPEC-31 for the criteria.
"""
import datetime

RETENTION_DAYS = None  # TODO(SPEC-31-AC-01): set the retention window


def expired(closed_at, today=None):
    today = today or datetime.date.today()
    return (today - closed_at).days > RETENTION_DAYS
