# Big Painless Spec: CSV 집계 CLI

- ID: SPEC-17
- Revision: 3
- Status: Accepted
- Owner: Dana Whitfield
- Change from previous revision: rev3 narrowed the output to totals only, after rev2's per-row dump was rejected as unreadable.

## User story and scenario

An operator drops one or more CSV exports into a directory and runs one command
to learn how many rows there are and what the `amount` column sums to. They read
the answer in the terminal and paste it into a weekly report.

## Interview

| Question ID | Question | Answer | Evidence / responder | Affected criteria | Open / resolved |
|---|---|---|---|---|---|
| Q-01 | Output format — table, JSON, or plain lines? | JSON, so the weekly report script can consume it without parsing | Dana Whitfield, 2026-08-30 | SPEC-17-AC-02 | resolved |
| Q-02 | What happens to a row whose `amount` is empty or non-numeric? | Skip it and keep going. Do not fail the run. | Dana Whitfield, 2026-08-30 | SPEC-17-AC-03 | resolved |
| Q-03 | Should an empty directory be an error? | No. Report zero for both fields. | Dana Whitfield, 2026-09-01 | SPEC-17-AC-04 | resolved |
| Q-04 | Per-row output as well as totals? | No — rev2 shipped that and it was unreadable. Totals only. | Dana Whitfield, 2026-09-02 | SPEC-17-AC-01 | resolved |

## Scope, common rules, and non-goals

- One command reads every `*.csv` in a given directory.
- Output is a single JSON object on stdout.
- Non-goals: per-row output, currency conversion, writing files, network access.

## Acceptance criteria

| ID | Observable outcome | Verification method |
|---|---|---|
| SPEC-17-AC-01 | Output contains totals only, never per-row lines | Run against the sample directory and inspect stdout |
| SPEC-17-AC-02 | Output is a single JSON object with keys `total` and `count` | Parse stdout as JSON |
| SPEC-17-AC-03 | A row with an empty or non-numeric `amount` is skipped, and the run still exits 0 | Run against `mixed.csv` |
| SPEC-17-AC-04 | An empty directory yields `{"total": 0, "count": 0}` and exits 0 | Run against an empty directory |

## Execution authorization

Dana Whitfield authorized implementation of this spec on 2026-09-02. No further
approval is needed to write the code and its tests.
