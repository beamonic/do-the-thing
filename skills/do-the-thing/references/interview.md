# Interview contract

The Big interview is a bounded search over decisions, not a questionnaire. Model
the work as a tree: each decision branches into the decisions that only exist
once it is settled. The interview walks that tree until nothing that changes the
Big is still being guessed at.

## The frontier

The **frontier** is every decision whose prerequisites are already settled — the
questions answerable now without assuming an answer you have not heard. A
question whose answer depends on another question still open in this round
belongs to a later round, not this one.

Ask the whole frontier at once, then wait. Do not trickle one question at a time:
the user answers a set, that set reshapes the tree, settled decisions push the
frontier outward, and you recompute it for the next round.

## Round format

Number each question, give it a title, and state your own recommended answer.
The recommendation is what makes a round cheap to answer — the user can accept it
or correct it instead of composing a decision from nothing.

```
Q1 — <question title>: <question body, including any choices>
    Recommended: <your answer, and why in one line>

Q2 — <question title>: <question body>
    Recommended: <your answer>
```

Transcribe each round into the Big template's interview table before acting on
it: a stable question ID, the answer, the responder, the evidence, and the
acceptance criteria the answer affects. A round's own numbering is positional and
does not survive the next round; a question ID must. `Q1` in round two is not
`Q1` in round one, but `Q-07` stays `Q-07`.

## Facts are yours, decisions are the user's

Finding facts is your job, never the user's. Step 1 of this skill — the issue,
its sources, existing Linear records — is that fact-finding, which is why the
interview runs after it and not before. A question the environment can answer is
not an interview question; look it up.

When a frontier question needs a fact you do not have yet, go get it, and do not
block the round on it. A running lookup is an unsettled prerequisite, so only the
questions downstream of it wait; ask the rest of the frontier now.

The decisions themselves are the user's. Put each one to them and wait. Do not
resolve a product decision by picking your own recommendation when no answer
came back.

## When the interview ends

Stop when the remaining frontier affects only individual tasks. Every branch that
bears on the overall promise — the user outcome, scope, shared rules, exceptions,
acceptance criteria — must be visited rather than silently assumed, but a
question that changes only one task's behavior can stay open: it blocks that
task, not the Big and not unrelated work.

Record what is still open in the Big's open-decisions section, naming the tasks
each open question blocks. An interview that ends does not grant permission to
execute, and it does not close the Big.

## Mini follow-up

A Mini inherits the Big's answers and shared rules. Do not rerun the interview
per task. Ask only what the task itself newly exposed, as one small round in the
same format, and record it in that Mini rather than the Big.

If a task's answer would change a shared rule or the scope, it is not a Mini
question. Propose a Big revision, review the Minis that depend on the affected
rule, and only then continue.

## Source

Adapted from Matt Pocock's `grilling` skill — MIT, Copyright (c) 2026 Matt
Pocock — whose design-tree frontier and one-round-per-frontier discipline this
contract follows. The wording here is ours and two rules are deliberately
changed for this workflow: grilling ends when the frontier is empty, while a Big
may be written with task-level questions still open, and grilling's per-round
numbering is transcribed here into stable question IDs. See `docs/method.md` in
the repository for the full attribution.
