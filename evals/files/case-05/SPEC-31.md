# Big Painless Spec: transcript archive

- ID: SPEC-31
- Revision: 2
- Status: Accepted

## Common rules

Support transcripts are retained for **one year** so that the quality team can
sample them for coaching reviews. The archive job runs nightly.

## Acceptance criteria

| ID | Observable outcome | Verification method |
|---|---|---|
| SPEC-31-AC-01 | A transcript older than the retention window is removed from the archive | Run the job against seeded data |
| SPEC-31-AC-02 | The nightly job logs how many transcripts it removed | Read the job log |
| SPEC-31-AC-03 | The coaching sample page lists transcripts within the retention window | Load the page |
