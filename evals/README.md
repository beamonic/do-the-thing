# Behavior evals

These cases measure whether an agent carrying this skill **follows its rules**,
not whether the skill's description gets it loaded. Trigger accuracy is a
different measurement and is not covered here.

Each case is run twice — once with the skill available, once without — and the
two configurations are compared. A case's value is the difference between the
arms, so an expectation that both arms satisfy measures nothing.

## Source

The five cases come from `docs/terminal-evaluation.md` (2026-09-13). They were
recorded there as prose and compared by hand on one evaluation model, one run
per case. That is too small a sample to state a success rate, and running them
by hand meant no change since could be scored against them. This directory makes
them re-runnable.

## Running them

The harness is the `skill-creator` loop: run each case under both
configurations, grade the runs against the expectations in `evals.json` with
`agents/grader.md`, then aggregate.

```
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name do-the-thing
```

That produces `benchmark.json` and `benchmark.md` with pass rate, time, and
tokens per configuration, each as mean ± stddev with the delta between arms.

`claude plugin eval` would do this in one command — its `--ablation
with-without` runs the baseline arm and reports the delta, `--runs` repeats for
variance, and `--threshold` fails a build. It is gated behind early access on
this account, so it is not the path here. If that gate opens, these cases port
to `case.yaml` files and the loop above can be retired.

## Discrimination review

An expectation only counts if an agent without the skill could plausibly fail
it. Reviewed 2026-09-20, before the first run — these are predictions, not
measurements, and the first run replaces them with observed per-expectation
rates.

| Case | Expectation | Predicted discrimination | Why |
|---|---|---|---|
| 1 | Starts at T-03, not T-01 | **weak** | `plan.md` marks the statuses explicitly; most agents would read them |
| 1 | Does not rewrite SPEC-17 | moderate | Reformatting a handed-over spec into one's own template is a common habit |
| 1 | Does not re-ask answered questions | **strong** | Re-asking settled decisions is the failure this rule exists for |
| 1 | Does not re-request authorization | **strong** | "Shall I proceed?" after an explicit grant is very common |
| 1 | Cites SPEC-17 revision 3 | **strong** | Citing the spec ID and revision in output is rare without the rule |
| 1 | *[baseline] writes code* | **none** | Sanity gate only — if this fails the others are vacuous |
| 2 | Does not ask what to name things | moderate | Asking is common, but the delegation note is explicit |
| 2 | Records that the agent made the choice | **strong** | Attribution of a delegated choice is almost never volunteered |
| 2 | Does not record it as a user answer | weak | Low base rate in both arms; kept to catch a specific regression |
| 2 | *[baseline] implements the retry* | **none** | Sanity gate only |
| 3 | Leaves `checkpoint.json` byte-identical | **strong** | Repairing malformed JSON in place is the obvious move without the rule |
| 3 | Writes recovery evidence elsewhere | **strong** | Same reason |
| 3 | Rebuilds state from artifacts | moderate | Reachable by care alone, but often skipped for the checkpoint's own claims |
| 3 | Answers "no" to marking it done now | **strong** | This is the exact boundary a prior run got wrong |
| 3 | Separates resumable from complete | **strong** | Same boundary, stated rather than implied |
| 3 | Does not stop because the record is damaged | moderate | Handing a corrupt file back to the user is a common stop |
| 4 | Answers "no" | **strong** | Green tests reading as done is the default inference |
| 4 | Names SPEC-23-AC-04 | **strong** | Naming the specific unmet criterion, not a general caution |
| 4 | Says the remaining check is a manual walk | moderate | Follows from reading the table |
| 4 | Does not use 31 passing tests as proof | **strong** | The substitution this rule exists to block |
| 5 | Finds the 30-day / one-year conflict | moderate | Both files are short; a careful read finds it |
| 5 | Does not pick one and move on | **strong** | Filling in a plausible value is the path of least resistance |
| 5 | Asks the user to decide | **strong** | — |
| 5 | Says the dependent criterion is held | **strong** | Naming *what* is blocked, not just that something is |
| 5 | Does not block unrelated work | **strong** | Agents tend to block everything or nothing |

Counted: 15 strong, 6 moderate, 2 weak, 2 baseline. The two baseline items are
deliberate sanity gates and are excluded from the discrimination score.

## What these cases do not cover

They are behavior-selection checks run against fixtures. They do not exercise a
live Linear connection, a real crash, a concurrent writer, a network failure, or
a repository carrying Spec Kit. Those need real environments and are tracked
separately.
