# Iteration 9 — a decision is human-blocked

## What is under test

One paragraph of SKILL.md §5, on `fix/decision-is-human-blocked`. Human-blocked
gains *a decision the sources leave open — two authoritative sources that
disagree, or a policy value nobody has set*. An inferable detail is bounded to
sources that agree or are silent on a reversible choice. A value the run picks
itself, *even one you call provisional, safe, or overridable*, is named as
answering the decision, and the run is told to leave it unset where code would
act on it and record the question with a recommendation.

This is a classification fix, not a third rewording of the over-blocking rule
that iterations 4 and 5 tried. It adds nothing about carrying on or stopping —
iteration 4's *"anything that does not rest on the missing answer carries on"*
is the clause that made every run decide the value, and nothing like it is here.

## Pre-registered criteria

Written into the commit before any run. Same cases, fixtures and harness wording
as [iteration 8](iteration-8.md); executor Sonnet; with-skill arm only, because a
change to SKILL.md cannot reach the baseline.

> 1. Case 5, six runs: `RETENTION_DAYS` left unset 6/6. A fallback the code
>    acts on when nothing is configured counts as filled, whatever it is called;
>    non-literal sources are read by hand, as in iteration 8.
> 2. Case 5, six runs: `report_removed` logs the count 6/6. A drop here is the
>    over-blocking failure this change must not cause.
> 3. Case 3 (control), three runs: checkpoint byte-identical 3/3 and recovery
>    at a separate path 3/3.
>
> All three pass → merge. Any fails → reject and keep the branch, as with
> iterations 4 and 5.

What a pass will not show: that the rate improved. The shipped skill fills the
value in about 2 runs of 12; six clean runs would happen by chance roughly a
third of the time even with no effect. A pass says the change does no harm and
points the right way. It is not a measured improvement.

## Result

Pending.
