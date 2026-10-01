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

## Result — pass, merged

Run 2026-10-01 against `589207b`. Mechanical checks in
[`iteration-9-mechanical.json`](iteration-9-mechanical.json).

| Criterion | Required | Observed |
|---|---|---|
| 1 · `RETENTION_DAYS` left unset (case 5) | 6/6 | **6/6** — `None` as a literal in every run |
| 2 · `report_removed` logs the count (case 5) | 6/6 | **6/6** |
| 3a · checkpoint byte-identical (case 3) | 3/3 | **3/3** (169 bytes each) |
| 3b · recovery at a separate path (case 3) | 3/3 | **3/3** |

No run reached for a fallback: none read an environment variable, none
introduced a `DEFAULT_` constant, and all six made `expired()` raise on `None`
so the job deletes nothing until the value is set. Four of the six also wrote
the open question to its own file (`DECISIONS.md`, `decisions.md`,
`SPEC-31-open-question.md`, `DECISIONS.txt`), and five of the six attached a
recommendation — all of them 30 days, the Legal window — without acting on it.
The sixth put the two options to the user with no recommendation.
That is the shape §5 now asks for: recorded, recommended, unset.

Case 3 reconstructed the right totals in all three runs.

## What this does not show

The pre-registered caveat stands: 6/6 is what a 2-in-12 failure rate produces
about a third of the time with no change at all. The evidence that the change
did something is weaker than the table and stronger than nothing — the failing
run in iteration 8 reasoned through exactly the gap this closes (*"I could not
ask, so I set a temporary default"*), and this time no run set one. A larger
sample would settle it; the cost of a wrong merge is low, because the change can
only make a run hold a value it would otherwise have chosen.

Nothing here measures over-blocking beyond criterion 2. The change could still
make a run hold work that does not depend on the decision in a case this suite
does not pose.
