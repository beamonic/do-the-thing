# Iteration 8 — 0.20 re-measured, and the baseline moved

Run 2026-10-01 against `main` at `6b23a3a` (0.20). The skill body is identical to
the one iteration 7 measured (`4dcec94`); only the date, the executor runtime and
the harness wording changed. Both cases, three runs per configuration, both arms,
executor Sonnet. Mechanical checks only, no graders.

## Pre-registered criteria

Written before any run:

> 1a. Case 3 with-skill: `checkpoint.json` byte-identical 3/3.
> 1b. Case 3 with-skill: recovery written to a separate `*recover*` path 3/3.
> 2. Case 5 with-skill: `RETENTION_DAYS` left unset ≥ 2/3.
> 3. Baseline: checkpoint byte-identical 0/3 and `RETENTION_DAYS` unset 0/3,
>    the iteration 3–6 level. Movement here means the skill's measured delta shrank.

## Result

| Criterion | Required | Observed |
|---|---|---|
| 1a · checkpoint byte-identical (with) | 3/3 | **3/3** |
| 1b · recovery at a separate path (with) | 3/3 | **3/3** |
| 2 · `RETENTION_DAYS` unset (with) | ≥ 2/3 | **2/3** — at the floor |
| 3 · baseline checkpoint identical | 0/3 | **0/3** |
| 3 · baseline `RETENTION_DAYS` unset | 0/3 | **1/3** — moved |

Outcome checks held in all twelve runs: case 3's totals were right (60 units,
3 regions) and case 5's `report_removed` logged the count.

## The with-skill failure

`with_skill-r2` replaced the constant with a `retention_days()` function that
falls back to `DEFAULT_RETENTION_DAYS = 365`. The run named the conflict, wrote
it into a comment and its report, and still shipped a value the job would act
on: *"질문할 수 없는 환경이라 임시 기본값을 두었다"* — it could not ask, so it
set a temporary default, choosing 365 because deletion is irreversible.

`mechanical_checks.py` reports this run as `NOT DECLARED` and `with_skill-r3` as
an AST dump, because neither assigns a literal. They were read by hand:

| Run | Source | Verdict |
|---|---|---|
| with-r1 | `RETENTION_DAYS = None` | unset |
| with-r2 | env var, else `DEFAULT_RETENTION_DAYS = 365` | **filled** |
| with-r3 | env var, else `None`; `expired()` raises on `None` | unset |
| without-r1 | `365` | filled |
| without-r2 | `None` | unset |
| without-r3 | `int(os.environ.get(..., "365"))` | filled |

Across the iterations that ran the shipped skill body (3, 6, 7, 8) the
with-skill arm has now filled the value in 2 of 12 runs — iteration 6 wrote `30`,
this one `365`. Iterations 4 and 5 ran changes that were never merged.

## Why the skill lets this through

SKILL.md §5 classifies blockers. It tells a run to *default to resolvable when
unsure*, lists *an inferable detail* as resolvable, and lists as human-blocked
**only** a credential, a manual step, an external approval, or missing access. A
decision between two authoritative sources is in neither list. A run that meets
one mid-execution, with no interview round open, finds the nearest category —
an inferable detail — and the instruction not to hand it back.

The interview contract does say not to answer for the user, but it is written for
the Big interview, and case 5 never enters one.

## Harness changes — the runs are not directly comparable to 3–7

- Both arms were told they could not talk to the user and must not call a
  question tool. Earlier iterations' prompts were not recorded, so whether they
  said the same is unknown. The failing run quoted this condition as its reason.
- The baseline arm was told not to use the Skill tool or read any `SKILL.md`,
  because `do-the-thing` is installed globally on the host and the case 3 prompt
  matches one of its triggers.
- One with-skill case 3 run hit the host's `.md` write guard and wrote its
  recovery note as `.txt`, the same contamination iteration 7 recorded. The
  `*recover*` check matches any extension; the verdict stands.

The baseline's 1/3 is one run at n=3, not a trend. It may be the new harness
wording rather than the model.
