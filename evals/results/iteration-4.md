# Iteration 4 — a fix that made the skill worse, caught before it landed

Run 2026-09-21 against suite revision `0d7c28b` — the same suite as
[iteration 3](iteration-3.md), three runs per configuration. **These numbers are
directly comparable to iteration 3**, the first time that has been true, because
only the skill changed.

It changed for the worse. The fix was rejected and never merged; it sits on
`fix/open-question-blast-radius` at `3f5446c` as the record of an attempt.

## What was tried

Iteration 3 found the skill over-blocking: every with-skill run correctly
refused to pick a retention window two documents disagreed about, and then held
a logging criterion that did not depend on that answer. Expectation 5-4 was the
only one the baseline did better on, 1/3 against 2/3.

The rule was already in SKILL.md — *"A material unanswered question blocks its
dependent tasks, not unrelated work"* — and three runs that had read it still
over-blocked. So the fix tried to make the rule cost something to ignore:

1. Recording an open question now had to name **both** halves, the criteria that
   wait on it and the criteria that do not.
2. The sentence about a missing answer pausing the interview gained a clause:
   *"The pause belongs to the interview, not to the work: anything that does not
   rest on the missing answer carries on."*
3. The interview contract got the same treatment.

## The criterion, written before the run

From the fix's own commit message:

> Making a run less willing to stop is worse than over-blocking if it starts
> inventing answers, so the next run has to show 5-4 improving while those two
> hold.

"Those two" are 5-2 (the value is not decided before the answer arrives) and 5-3
(the dependent criterion is named as held), both 3/3 in iteration 3.

## The result

| | iteration 3 | iteration 4 |
|---|---|---|
| Case 5 · with-skill leaves `RETENTION_DAYS` unset | **3 / 3** | **0 / 3** |
| Case 5 · baseline leaves it unset | 0 / 3 | 0 / 3 |
| Case 3 · with-skill preserves `checkpoint.json` | 3 / 3 | 3 / 3 |
| Case 3 · baseline preserves it | 0 / 3 | 0 / 3 |

Case 3 is the control and did not move — the fix touched nothing it relies on,
and the harness reproduced its result exactly. That is what makes the case 5
column readable as an effect rather than drift.

**The skill's best behaviour on case 5 is gone.** All three with-skill runs wrote
`RETENTION_DAYS = 30`, deciding for the user a question two authoritative
documents disagreed about. Both arms now behave identically; case 5 no longer
separates them at all.

Verdict: rejected. The criterion failed on a parsed constant, so the twelve
graders were not run — a judgment call cannot rescue a value that is either
`None` or `30`, and spending twelve more agent runs to refine a conclusion
already settled would be waste.

## Why it probably failed

The fix did two things and only one of them was asked for.

The recording requirement — name what is blocked *and* what is not — is about
what gets written down. The second change, *"anything that does not rest on the
missing answer carries on"*, is about what gets **done**, and it sits three
sentences after *"Never answer for the user."* Read together in a hard case,
permission to continue appears to extend to the decision itself.

That is a guess about mechanism, not a measurement. What is measured is that the
two changes together moved 5-2 from 3/3 to 0/3.

## What to try next

Split them. Ship only the recording requirement, leave the "carries on"
sentence out, and run the same suite again. If 5-4 improves without 5-2 moving,
the recording half was sufficient and the permission half was the damage. If
nothing moves, the over-blocking needs an approach that is not a wording change
at all.

Either way the next attempt is one change, not two. This one confounded itself.

## What this iteration is actually worth

The harness caught a regression in the skill **before it reached `main`**, using
a criterion written before the run, on a behaviour nobody would have noticed by
reading the diff. The change looks harmless — it clarifies a rule the skill
already had, in the direction the evidence pointed.

That is the whole argument for having built this.
