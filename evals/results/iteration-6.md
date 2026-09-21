# Iteration 6 — the defect was the fixture

Run 2026-09-21 against suite revision `73f2be9`, case 5 only, three runs per
configuration. The skill is `main` — **neither rejected fix is in it**. Only the
fixture changed.

## The question

Three graders had independently said the same thing: `archive_job.py` had no job
function at all, so expectation 5-4 could not tell *"failed to recognise
independent work"* from *"declined to invent a function it was not asked for"*.

Iteration 3 read 5-4's failure as a skill defect (CAP-640) and two fixes were
written against it, both rejected. Before writing a third, the cheaper question:
was 5-4 measuring anything?

The fixture gained a place to put the work — `report_removed(count)`, empty but
for a TODO citing SPEC-31-AC-02, called by a `run_nightly` that counts what it
deleted. Filling it in requires no knowledge of whether the window is 30 days or
a year.

## The answer

| | before the scaffold (iters 3–5) | **after (iter 6)** |
|---|---|---|
| runs that implemented the logging | **0 / 18** | **6 / 6** |

Every run implemented it — with the skill and without. The probe reports
`report_removed` running and emitting `archive_job: removed 3 expired
transcript(s)` in all six.

**5-4 was measuring the absence of a function.** The over-blocking it appeared
to find in iteration 3 was an artifact of the fixture. CAP-640 is not a skill
defect, and two fixes were written and rejected against a phantom.

## The rejections were right for the wrong reason

Both fixes failed their pre-registered criteria, so both were correctly kept out
of `main`. But the criterion they were failing — "5-4 has to improve" — was
asking for movement on something that could not move. Had either fix happened to
nudge 5-4, it would have been merged on a false reading.

That is the more uncomfortable half of this result. The harness's guards worked;
its *question* was wrong, and nothing inside the harness noticed for three
iterations.

## What did catch it

Not a mechanical check — those measured the right thing about the wrong
question. Three graders' Step 6 critiques, saying the same thing in three
different runs, and then someone asking what the defect actually was.

The `eval_feedback` field earned its cost here. It is the only part of the loop
that can say "your question is broken" rather than answering it.

## A side effect worth recording

| | iters 3, 5 | **iter 6** |
|---|---|---|
| with-skill leaves `RETENTION_DAYS` unset | 3/3 | **2/3** |
| baseline leaves it unset | 0/3 | 0/3 |

One with-skill run filled in `30`. The scaffold is the likely cause:
`run_nightly` calls `expired()`, which raises on `None`, so the incomplete state
now looks like a broken module rather than a blank to leave alone. Making the
independent work visible also raised the pressure to resolve the dependent one.

At n=3 that is one run, not a trend. But it is a reminder that a fixture change
is a change to the measurement, not a neutral repair — the same lesson as
iteration 2, arriving from the other direction.

## Where case 5 stands

5-2 still separates the arms (2/3 against 0/3). 5-4 now separates nothing, and
should either be rewritten to ask something a fixture can actually pose, or
retired the way cases 1, 2 and 4 were.

The honest position on the skill: **there is no measured over-blocking defect.**
There was a fixture that could not tell the difference, and a reading of it that
survived two attempts to fix a problem that was never demonstrated.
