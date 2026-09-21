"""Nightly transcript archive job.

The retention window is read from settings. See SPEC-31 for the criteria.
"""
import datetime
import logging

logger = logging.getLogger(__name__)

RETENTION_DAYS = None  # TODO(SPEC-31-AC-01): set the retention window


def expired(closed_at, today=None):
    today = today or datetime.date.today()
    return (today - closed_at).days > RETENTION_DAYS


def report_removed(count):
    """How many transcripts last night's run deleted."""
    # TODO(SPEC-31-AC-02)


def run_nightly(transcripts, today=None):
    removed = 0
    for transcript in transcripts:
        if expired(transcript.closed_at, today):
            transcript.delete()
            removed += 1
    report_removed(removed)
    return removed
