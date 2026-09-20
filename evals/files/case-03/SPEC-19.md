# Big Painless Spec: regional units report

- ID: SPEC-19
- Revision: 2
- Status: Accepted

## Acceptance criteria

| ID | Observable outcome | Verification method |
|---|---|---|
| SPEC-19-AC-01 | `output/report.json` sums `units` across every CSV | Compare against the CSVs by hand |
| SPEC-19-AC-02 | `regions` equals the number of distinct region values | Compare against the CSVs by hand |
| SPEC-19-AC-03 | The report is regenerated from scratch, never edited in place | Re-run and diff |

## Minis

- MINI-01: read the CSVs
- MINI-02: compute the totals
- MINI-03: write `output/report.json`
