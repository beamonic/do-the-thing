# Iteration 5 — the second attempt is safe and useless

Run 2026-09-21 against suite revision `0d7c28b`, three runs per configuration.
Same suite as [iteration 3](iteration-3.md) and [iteration 4](iteration-4.md),
so all three are directly comparable.

The change under test is on `fix/record-both-halves` at `38a240e`. It is the
half of the rejected [iteration 4](iteration-4.md) fix that had actually been
asked for: logging an open question must name the criteria that wait on the
answer **and** the criteria that do not. The sentence that governed what gets
*done* — "anything that does not rest on the missing answer carries on" — was
left out this time.

## The criterion, written before the run

> 5-4 has to improve while 5-2 and 5-3 hold at 3/3. If nothing moves, wording is
> not the lever and the next attempt has to be something else.

## The result

| Expectation | iter 3 | iter 4 (1st attempt) | **iter 5 (2nd attempt)** |
|---|---|---|---|
| 5-2 · value not decided before the answer | 3/3 | **0/3** | **3/3** |
| 5-3 · dependent criterion named as held | 3/3 | 0/3 | **3/3** |
| **5-4 · unrelated work not blocked with it** | 1/3 | — | **0/3** |

Case 3, the untouched control, reproduced exactly: with-skill preserved the
damaged checkpoint 3/3 and wrote recovery elsewhere 3/3; the baseline rewrote it
3/3 and wrote nothing separate 3/3. Byte-identical to iteration 3.

Case 5 overall: with-skill **0.800 ± 0.000**, baseline **0.467 ± 0.094**,
delta **+0.333**.

## What this settles

**The confound is confirmed.** Isolating the "carries on" sentence restored 5-2
and 5-3 from 0/3 to 3/3. Iteration 4's damage came from that clause, not from
the recording requirement. The guess recorded in iteration 4 was right.

**And the recording requirement does nothing for the problem it was written
for.** 5-4 did not improve — 1/3 to 0/3, which at n=3 is no movement rather than
a decline. All three with-skill runs still folded the logging criterion into the
blocked set. One transcript put it plainly: building the logging first "would be
speculative work premised on a value that has not been decided." That is exactly
the misclassification, stated as if it were reasoning.

Two wording attempts, zero movement on the target. **Wording is not the lever
here.**

## So it is not merged either

The recording requirement is safe — it broke nothing, and the control held. It
is also, by the only measurement available, inert. Adding text to a skill that
measurably does nothing is the thing the skill's own working principle warns
against: identify the criterion a piece of work serves before adding it.

`fix/record-both-halves` stays pushed and unmerged beside
`fix/open-question-blast-radius`. Two attempts, two records, `main` unchanged.

## What is left to try

Not a third rewording. The rule has been present, then emphasised, then made
mandatory to record, and a run in a hard case still treats "related-looking" as
"blocked". Candidates that are not wording:

- **Make the classification a step with an output**, the way the interview has
  rounds and the blocker triage has categories. A question the run has to answer
  per criterion — does this one need the missing answer? — rather than a
  sentence it can agree with and then not apply.
- **Change the fixture instead.** Two graders noted that `archive_job.py` has no
  job function at all, so "failed to recognise independent work" and "declined to
  invent a function" are indistinguishable here. A fixture with a logging stub
  already present would separate them. It is possible the skill is being blamed
  for a case that cannot tell the difference.

The second should probably come first. It is cheaper, and if it turns out 5-4
was never measuring what it claimed, two rejected fixes were spent on a
phantom.

## Method note

Only case 5 was graded this round — six runs, not twelve. Case 3 is the control
and its three mechanical checks reproduced iteration 3 exactly, so the six runs
that could not have moved were not re-graded. Overall pass rates across both
cases are therefore not recomputed here; the case 5 figures above are the
comparable ones.
