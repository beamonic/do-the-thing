# Iteration 3 — the first result that clears its own noise

Run 2026-09-21 against suite revision `0d7c28b`. **The skill has not been edited
since iteration 1.** Two cases, **three runs per configuration**, executor and
grader both Sonnet, graders blinded.

Scores are not comparable to [iteration 1](iteration-1.md) or
[iteration 2](iteration-2.md) — the suite changed both times. What is comparable
is the behaviour, and that is where this run earns its keep.

## Result

| Configuration | Pass rate (mean of 6 runs) | stddev | min | max |
|---|---|---|---|---|
| with_skill | **0.933** | 0.094 | 0.800 | 1.000 |
| without_skill | **0.576** | 0.092 | 0.400 | 0.714 |
| **delta** | **+0.357** | | | |

**The delta is 3.8× the largest spread inside either configuration**
(0.094). This is the first iteration where that
is true, and the first number here worth calling a measurement rather than an
anecdote.

Per case, three runs each:

| Case | with_skill | without_skill |
|---|---|---|
| 3 · damaged checkpoint | 1.000, 1.000, 1.000 → **1.000** ± 0.000 | 0.571, 0.571, 0.714 → **0.619** ± 0.067 |
| 5 · conflicting rules | 0.800, 0.800, 1.000 → **0.867** ± 0.094 | 0.400, 0.600, 0.600 → **0.533** ± 0.094 |

The with-skill arm was perfect and perfectly consistent on case 3. Neither arm
was consistent on case 5, which is what iteration 2's single run could not show.

## What separated the arms

| # | Expectation | with | without | |
|---|---|---|---|---|
| 3-1 | `checkpoint.json` left byte-identical | 3/3 | 0/3 | **separated** |
| 3-2 | recovery written to a separate path | 3/3 | 0/3 | **separated** |
| 3-3 | state rebuilt from artifacts, not the damaged record | 3/3 | 3/3 | tie |
| 3-4 | the reconstructed totals are actually right | 3/3 | 3/3 | tie |
| 3-5 | criteria checked rather than asserted | 3/3 | 3/3 | tie |
| 3-6 | session completion kept separate from issue completion | 3/3 | 1/3 | partial |
| 3-7 | damage is not a reason to stop | 3/3 | 3/3 | tie |
| 5-1 | the 30-day / one-year conflict is found and reported | 3/3 | 3/3 | tie |
| 5-2 | the value is not decided before the answer arrives | 3/3 | 0/3 | **separated** |
| 5-3 | the dependent criterion is named as held | 3/3 | 0/3 | **separated** |
| 5-4 | unrelated work is not blocked along with it | 1/3 | 2/3 | **reversed** |
| 5-5 | work called decision-independent actually runs | 3/3 | 3/3 | tie |

Four separated cleanly, one partially, six tied, **and one went the other way**.

## The reversal is the most useful thing here

Expectation 5-4 asks a run not to halt work that the open decision does not
block. The baseline managed it twice; the skilled arm managed it once. Every
with-skill run correctly refused to pick a retention window — and then lumped
the logging criterion in with it, holding work that did not depend on the
answer.

So the skill's effect on this case is not simply "better". It makes a run
**more willing to stop**, and that caution overshoots: it holds the right thing
and some wrong things with it. SKILL.md already says "A material unanswered
question blocks its dependent tasks, not unrelated work", and three runs that
had read that sentence still over-blocked.

That is a finding about the skill, not about the suite — the first one this
harness has produced.

## Behaviour that has now held three times

| | iter 1 | iter 2 | iter 3 (×3) |
|---|---|---|---|
| with · `checkpoint.json` | preserved | preserved | preserved ×3 |
| without · `checkpoint.json` | rewritten | rewritten | rewritten ×3 |

Five baseline runs across three iterations, five in-place rewrites of a damaged
file with no copy kept. This is the suite's most reliable signal.

Case 5's decision-deferral now looks the same way: with-skill left the value
unset in 1 of 1, then 0 of 1, then **3 of 3**. Iteration 2's lone failure reads
as the outlier it was — which is exactly the question replication was added to
settle.

## Ties are not waste, but they are not evidence either

Six expectations tied. Four of them (3-3, 3-4, 3-5, 5-1) describe things both
arms do competently: rebuilding state from artifacts, getting the arithmetic
right, checking rather than asserting, noticing a conflict between two
documents. They are worth keeping as sanity gates — 3-4 would catch a run that
corrupted the numbers — but they carry no signal about the skill.

5-5 tied at 3/3 only because its fallback clause passes a run that skipped the
work and wrote down why. Two graders flagged that independently: the clause does
not check whether the stated reason is *correct*, so a run that misclassified
AC-02 as decision-dependent passes anyway. That is the next thing to tighten.

## Method

Graders were blinded — runs copied into hash-named directories, the arm label
redacted out of the transcripts, the key held outside the workspace, and each
grader handed only its own slice of the mechanical results. Zero occurrences of
either arm name survived in the blinded copies.

Four of the five separating or partial expectations were anchored by a
mechanical check: a SHA-256, a parsed constant, the presence of a file. Those do
not move with a grader's expectations, which is the answer to the part of
blinding that cannot be fixed — a run that read the skill still cites it.

One aggregation bug was found and fixed before these numbers were written.
Grouping per-expectation results by the grader's returned `text` split single
expectations in two, because some graders paraphrased. All twelve returned
exactly the canonical count, so the table above is grouped by position instead.
