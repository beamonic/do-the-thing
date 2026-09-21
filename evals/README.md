# Behavior evals

These cases measure whether an agent carrying this skill **follows its rules**,
not whether the skill's description gets it loaded. Trigger accuracy is a
different measurement and is not covered here.

Each case is run **three times per configuration** — with the skill available and
without — and the two are compared. A case's value is the difference between the
arms, so an expectation that both arms satisfy measures nothing.

Three runs, not one. Iteration 2 found the same case scoring 5/5 and then 1/4
across iterations with **no change to the skill**; one run per arm cannot tell a
coin from an effect. Before reading any delta as an effect, check that it is
larger than the spread within a configuration.

[Iteration 3](results/iteration-3.md) is the first run where it was: delta
**+0.357** against a largest within-arm stddev of **0.094**, roughly four times
the noise. It also produced the first finding about the skill rather than about
the suite — every with-skill run refused to decide a question that was the
user's to answer, and then held work that did not depend on that answer.

The suite is two cases and 12 expectations. It was five and 26 until iteration 2
measured three of them separating the arms zero times twice running — those live
in [`retired/`](retired/README.md) with the reasoning and how to bring one back.

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

Two steps sit between the runs and the graders:

```
python evals/scripts/mechanical_checks.py <workspace>/iteration-N
python evals/scripts/blind_runs.py <workspace>/iteration-N --mapping <path outside it>
```

`mechanical_checks.py` settles by hash, parsed constant, and — for the retry
case — by actually executing the run's code with a recording `sleep`, the
expectations a grader would otherwise take a transcript's word for. Hand its
output to every grader so nobody re-derives them and no verdict drifts from the
bytes.

`blind_runs.py` copies each run into a hash-named directory, redacts the arm
label out of the copies — runs quote their own working directory, so the hash
alone does not hide it — and writes the key outside the workspace. Point each
grader at one `run-<hash>` and nothing else, and give it only its own slice of
the mechanical results; the keys in `mechanical_checks.json` name the arms.

Blinding stops there. A run that read the skill cites it, and removing those
citations would delete the evidence a grader needs. Lean on the mechanical
checks for the expectations that decide the outcome.

Its `aggregate_benchmark` did not read this layout in iteration 1 and reported a
zero delta over zero runs; the figures in the results file were aggregated
directly from each `grading.json`.

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
it. The table below was written 2026-09-20, **before** any run. It has since been
scored: see [iteration 1](results/iteration-1.md) for what each expectation
actually did.

**It was wrong.** Of the 15 expectations graded "strong", 5 separated the two
arms, 8 were passed by both, and 2 were failed by both. Cases 1, 2, and 4
produced no signal at all. The table is kept as written, unedited, because a
prediction that is quietly corrected after the fact teaches nothing — the gap
between this column and the results file is the useful part.

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

Predicted: 15 strong, 6 moderate, 2 weak, 2 baseline. The two baseline items are
deliberate sanity gates and are excluded from the discrimination score.

Observed in iteration 1: **5 discriminated, 18 tied on a pass, 2 tied on a
fail.** All five that discriminated live in cases 3 and 5. Three fixtures were
found to hand over their own answer, which is why so much tied; the fixes are
listed in the results file and belong to iteration 2.

## Changes made for iteration 2

Iteration 1 found the problems in this suite before it found any in the skill.
The fixes, tracked as CAP-634, CAP-635 and CAP-636:

- **Case 4's fixture no longer states its own conclusion.** The line
  "SPEC-23-AC-04 has no Mini assigned and no recorded evidence" is gone from
  `checkpoint.md`, and the acceptance table no longer carries a "Responsible
  Minis" column. The Minis are listed separately with their scope; the gap has
  to be found by reading one against the other.
- **Case 1 no longer answers every question in its table.** The empty-directory
  decision was removed from SPEC-17's interview table and now lives only in
  `SPEC-17-AC-04`. Asking about it is asking about a fact the spec already
  states. The citation expectation was narrowed to files the run itself wrote —
  leaving the fixture untouched used to satisfy it.
- **Case 2 asks something observable.** "Does not ask" became "does not record
  that it needs a decision", since a single-turn run has no channel to ask
  through. A new expectation checks that the delay between retries actually
  grows, which nothing checked before.
- **Case 3 splits the completion boundary.** The two expectations both arms
  failed were replaced by the distinction SKILL.md itself draws: did the run
  actually check the criteria, and did it keep session completion separate from
  issue completion. The old pair asked a run to withhold a conclusion it had
  earned.
- **Case 5 merges two correlated expectations.** Filling the value in and
  failing to ask were one failure counted twice.

26 expectations, up from 25.

**Two of the five fixes worked.** [Iteration 2](results/iteration-2.md) ran the
fixed suite: case 3's rewritten expectations now discriminate, and the blinding
helped. Cases 1, 2 and 4 still tied at 100% in both arms — two iterations with no
signal — and have since been retired.

It also found something larger. Case 5 flipped between iterations with **no
change to the skill**: the with-skill run scored 5/5 in iteration 1 and 1/4 in
iteration 2. One run per configuration is not a measurement, which is why the
suite now runs three.

Both surviving cases gained an expectation that checks the *outcome* rather than
the process — whether the reconstructed totals are actually right, and whether
the work claimed as decision-independent actually runs. A grader pointed out that
every expectation in the retired cases watched how a run behaved and none watched
whether it produced the correct thing, so a broken implementation could have
passed them all.

## What these cases do not cover

They are behavior-selection checks run against fixtures. They do not exercise a
live Linear connection, a real crash, a concurrent writer, a network failure, or
a repository carrying Spec Kit. Those need real environments and are tracked
separately.
