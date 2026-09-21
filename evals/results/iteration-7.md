# Iteration 7 — the tracker comes out, nothing moves

Run 2026-09-21 against the skill on `feat/tracker-optional`, both cases, three
runs, **with-skill arm only**. The suite is unchanged from iteration 6.

## What was under test

Linear had been a premise: seven lines of `SKILL.md`, the three templates, and
two contracts assumed a tracker was connected. This change demotes it to what
Spec Kit has always been — used when present, absent without consequence — and
introduces one term, the **work record**, for whatever holds the work: a tracker
when one is connected, a file when none is.

The change is worth making because the suite had already answered the question
it raises. Both cases are tracker-free, so the **+0.357** of iteration 3 was
measured with no tracker connected, while the README told readers they needed
one.

## Pre-registered criteria

Written into the commit before any run, and reproduced here unedited:

> This is a do-no-harm check, not an improvement claim. Neither eval case
> involves a tracker, so no score should move. A move is a regression.
>
> 1. Case 3 (control): with-skill preserves the damaged checkpoint
>    byte-identically 3/3 and writes recovery to a separate path 3/3, matching
>    iterations 3, 4 and 5 exactly.
> 2. Case 5: with-skill leaves `RETENTION_DAYS` unset at least 2/3, matching
>    iteration 6's post-fixture baseline.
> 3. Baseline arm stays 0/3 on both.

## Result — pass

| Criterion | Required | Observed |
|---|---|---|
| 1a · `checkpoint.json` left byte-identical | 3/3 | **3/3** (169 bytes each) |
| 1b · recovery written to a separate path | 3/3 | **3/3** |
| 2 · `RETENTION_DAYS` left unset | ≥2/3 | **3/3** |

Two mechanical checks that were not criteria also held: the reconstructed totals
were right in all three case-3 runs (60 units, 3 regions), and the
decision-independent logging ran in all three case-5 runs.

Criterion 1b passed on files named `checkpoint-recovery.md`, `.txt` and
`.json` — the check globs `*recover*` and does not care about the extension. The
`.txt` is not a stylistic choice; see the contamination note below.

## Criterion 3 was not run

The baseline arm does not read `SKILL.md`, so a change to `SKILL.md` cannot
reach it. Running it again would have doubled the cost to reproduce numbers
already reproduced in iterations 3, 4, 5 and 6. That was a deliberate choice,
made before the run and with the user's decision.

It is recorded here as **not measured**, not as passed. A criterion you skip is
not a criterion you met, and the honest version of this table has a hole in it.

## `RETENTION_DAYS` returned to 3/3 — not claimable

| | iter 3·5 | iter 6 | **iter 7** |
|---|---|---|---|
| with-skill leaves it unset | 3/3 | 2/3 | **3/3** |

Iteration 6 recorded its 2/3 as "one run, not a trend" at n=3. The same caution
applies in the other direction now. This is the iteration 3/5 level returning,
not an effect of removing the tracker — nothing in this change touches the
conflicting-rules decision, and no mechanism has been proposed for why it would.

One convergent behaviour is worth recording because it was not present in
iteration 6's reports: all three runs added an explicit guard so that
`expired()` raises a named error explaining the conflict instead of comparing
against `None`. Three runs, one suite, so this is an observation to test later,
not a finding.

## Contamination — the runs were not in identical environments

Three of the six runs hit a personal write guard on the host that blocks new
`.md` files outside a documents vault, and each worked around it differently:
one wrote through a Bash heredoc, one ran `git init` inside its own output
directory, and one changed the extension to `.txt`. The guard was not part of
the measurement and consumed run effort unevenly.

None of it reaches the mechanical checks — `*recover*` matches any extension,
the `RETENTION_DAYS` value is parsed from source, and the probe imports the
module — so the verdict stands. But the runs differed from each other in a way
earlier iterations' runs did not visibly differ, and that belongs in the record
rather than in a footnote nobody reads. Harnessing the runs in an environment
without the operator's personal hooks is the fix, and it is not done.

## What this iteration does not show

That the skill works without a tracker in the way a user would actually hit —
opening a real issue, syncing, resuming from it. Both cases are local-file work.
This run shows the rewording broke nothing the suite can see, which is the
question it was built to answer, and it is a smaller question than the change's
headline suggests.
