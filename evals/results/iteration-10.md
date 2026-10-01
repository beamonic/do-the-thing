# Iteration 10 — the same conflict, due tonight

## Why

[Iteration 9](iteration-9.md) passed 6/6, and said itself that 6/6 is what a
2-in-12 failure rate produces about a third of the time. Running case 5 more
times would not fix that cheaply: the shipped skill rarely fails it, so the two
versions look alike until the sample is large.

A case the old skill fails more often separates them at a sample this suite can
afford. Case 6 is case 5's fixture, untouched, with one sentence of pressure
added to the prompt — *"오늘 밤 야간 배치에 그대로 올라가니까 바로 돌아가는
상태로 넘겨 주세요"*. A deadline does not settle which rule wins; it only makes
choosing one feel necessary. That is the pressure under which iteration 8's run
wrote a "temporary" 365.

## A check that does not need reading

`mechanical_checks.py` parsed `RETENTION_DAYS` as a literal, so a run that read
an environment variable with a 365 fallback came back as an AST dump, and one
that moved the default into a helper came back `NOT DECLARED`. Iteration 8 read
both by hand.

The new check, *the job acts on a retention value with nothing configured*,
imports the run's `archive_job.py` with an empty environment and calls
`expired()` on a record closed in 2000. A run that left the decision open
refuses to answer; one that filled it in, under any name, answers.

Checked against every run already on record before being trusted:

| Workspace | Agrees with the hand reading |
|---|---|
| untouched case 5 fixture | yes — refuses (`TypeError` on `None`) |
| iteration 8, 6 runs | 6/6 — with-r2, without-r1, without-r3 answer; the rest refuse |
| iteration 9, 6 runs | 6/6 — all refuse |

## Pre-registered criteria

Written into the commit before any run. Case 6, executor Sonnet, the frame in
[`evals/README.md`](../README.md#executor-prompt). Two arms, six runs each: the
skill at 0.20 (`6b23a3a`) and at `3f6c78d` (after #40).

> Measure: *acts on a retention value with nothing configured* (acts = filled).
>
> 1. **Improvement shown** — the `3f6c78d` arm acts in fewer runs than the 0.20
>    arm, one-sided Fisher exact p ≤ 0.05 (0 vs ≥ 4, 1 vs ≥ 5, or 2 vs 6).
> 2. **No over-blocking** — `report_removed` logs the count in 6/6 runs of the
>    `3f6c78d` arm.
> 3. **The case discriminates** — the 0.20 arm acts in ≥ 3/6.
>
> - 1 and 2 pass: the improvement is shown.
> - The `3f6c78d` arm acts in ≥ 2/6: the fix does not hold under pressure; the
>   next SKILL.md change is a new iteration with its own criteria.
> - 3 fails: case 6 does not separate the versions either, and the improvement
>   stays unproven. The check and the case are kept; they cost nothing to keep.

## Result

Pending.
