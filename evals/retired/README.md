# Retired cases

These three ran in both iterations and separated the arms **zero times**. They
are kept, not deleted: the fixtures are sound, and a later version of the skill —
or a harder variant of the task — could make them discriminate again.

| Case | Subject | iteration 1 | iteration 2 |
|---|---|---|---|
| 01 | Resume a handed-over spec at the first unfinished task | 6/6 · 6/6 | 7/7 · 7/7 |
| 02 | Make a delegated naming choice without asking | 4/4 · 4/4 | 5/5 · 5/5 |
| 04 | Refuse to call a Big done when one criterion has no evidence | 4/4 · 4/4 | 4/4 · 4/4 |

Iteration 2 rewrote all three to stop them handing over their own answers —
case 4's checkpoint no longer states the conclusion, case 1's interview table no
longer answers every question, case 2 asks for something observable. They still
tied. The fixtures were not the whole problem: **an agent without the skill does
these tasks correctly anyway.** Both arms cross-reference an acceptance table
against a Mini list unaided, neither re-asks a decision the spec already states,
and neither asks what to name a function it was told to name.

A case that cannot fail for the baseline costs two agent runs per iteration to
tell you nothing.

## Reviving one

Move it back under `files/`, add its block to `evals.json`, and give it at least
one expectation the baseline could plausibly fail — ideally one
`mechanical_checks.py` can settle by fact rather than by reading.

Case 2's retry-delay check is the model for that: it imported the run's module
with a recording `sleep` bound before import and called whatever wrapper the
module defined, discovering the name rather than assuming it. That technique now
lives on in `archive_probe` for case 5. If case 2 comes back, lift it from there.
