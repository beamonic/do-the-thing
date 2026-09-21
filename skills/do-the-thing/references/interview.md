# Interview contract

The Big interview is a bounded search over decisions, not a questionnaire. Model
the work as a tree: each decision branches into the decisions that only exist
once it is settled. The interview walks that tree until nothing that changes the
Big is still being guessed at.

## The frontier

First reuse accepted answers from any supplied grill or spec, with their original
IDs and evidence. Reconcile them with current sources; interview only newly
unresolved product decisions. A complete handoff can have an empty frontier at
entry. Do not rerun it just to populate this skill's template. Reversible internal
details delegated by the user are agent implementation choices; record the
delegation and choice without inventing a user answer or asking again.

The **frontier** is every decision whose prerequisites are already settled — the
questions answerable now without assuming an answer you have not heard. A
question whose answer depends on another question still open in this round
belongs to a later round, not this one.

Compute the frontier, then ask **one** question from it and stop. A round is
one question, one answer. The answer reshapes the tree, settled decisions push
the frontier outward, and you recompute it before the next question. Pick the
frontier question that unblocks the most of the tree; say how many are still
waiting behind it so the user can pace themselves.

Do not put the whole frontier in one message. A list of six questions with six
recommendations reads as a proposal, gets a one-word "as recommended", and
nothing was actually decided. One question gets an actual answer.

## Round format

Give the question a stable ID, a title, the body with its choices, and your
recommended answer. The recommendation is what makes a round cheap to answer —
the user can accept it or correct it instead of composing a decision from
nothing. Then wait for the answer using the host-specific lifecycle below.
Do not advance the interview or begin dependent work before the answer arrives.

```
Q-07 — <question title> (1 of ~4 remaining)
<question body, including any choices>
Recommended: <your answer, and why in one line>
```

### Blocking interview and host capability

For this decision interview, use a native question tool that waits for the
user's answer before returning. Ask one question with the recommended option
first. In Claude Code this is `AskUserQuestion`; in Codex it is
`request_user_input` when the current mode permits it. Discover the actual tool
contract rather than assuming availability from the host name.

Do not replace a blocking interview with `request_user_input_async` followed by
sleep or polling. A mid-turn question and an outstanding native input request
are different states; keeping a turn running does not establish the sidebar's
"Needs input" state. Do not print JSON or a prose imitation of a tool call.

If Codex exposes the blocking tool only in Plan mode and the current mode does
not permit it, stop before submitting the product question and state the exact
prerequisite: switch this conversation to Plan mode, then resume at the same
unanswered question ID. Do not claim to switch modes yourself, launch another
task, alter app flags, or invoke a restricted tool. A request to proceed is not
permission to override the host's tool restrictions.

If no supported blocking route exists, explain that limitation and preserve the
unanswered question. Use an asynchronous or plain-text interview only if the
user explicitly accepts that alternative. No answer, timeout, preselected
option, or `accepted: true` result is a decision. A native request's automatic
resolution is not evidence of a human answer: verify response provenance.

A sidebar label is rendered by the host, not by this skill. Record tool
submission, outstanding input state, user response, and observed sidebar label
separately. Some app versions hide the label on the selected task. Do not
promise that a blocking call alone makes the label visible everywhere.

After a real answer, record it and ask the next unresolved question through the
same blocking route. Do not end the turn just to claim that a question appeared.
If the user cancels or redirects the work, handle that instruction first.

Transcribe the answer into the Big template's interview table before acting on
it: the question ID, the answer, the responder, the evidence, and the acceptance
criteria the answer affects. The responder of a decision is the user. An answer
you supplied yourself is not an answer; it is an open question, and the row
stays open.

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
came back. No answer means the interview is paused, not finished: do not write
the Big, plan, split, or execute on an assumed answer, and do not report the
interview as done. If the user says to proceed without answering, record that
instruction as the answer's evidence and the recommendation as the answer — that
is the only way a recommendation becomes a decision.

## When the interview ends

Stop when the remaining frontier affects only individual tasks. Every branch that
bears on the overall promise — the user outcome, scope, shared rules, exceptions,
acceptance criteria — must be visited rather than silently assumed, but a
question that changes only one task's behavior can stay open: it blocks that
task, not the Big and not unrelated work.

Record what is still open in the Big's open-decisions section, naming for each
question both the tasks it blocks and the tasks it does not. Only the first half
is obvious to write, and a question recorded with only its blocked side tends to
be read later as blocking whatever sits near it. If a task merely looks related
— it touches the same file, the same acceptance criterion's neighbour, the same
feature — say so and keep going. An interview that ends does not grant permission to
execute, and it does not close the Big.

## Mini follow-up

A Mini inherits the Big's answers and shared rules. Do not rerun the interview
per task. Ask only what the task itself newly exposed, one question per round in the
same format, and record it in that Mini rather than the Big.

If a task's answer would change a shared rule or the scope, it is not a Mini
question. Propose a Big revision, review the Minis that depend on the affected
rule, and only then continue.

## Source

Adapted from Matt Pocock's `grilling` skill — MIT, Copyright (c) 2026 Matt
Pocock — whose design-tree frontier and recommended-answer discipline this
contract follows. The wording here is ours and three rules are deliberately
changed for this workflow: grilling asks the whole frontier per round, while this
contract asks one question per round and waits using the host-specific lifecycle, because a batched
frontier with recommendations was answered as a whole or not at all; grilling
ends when the frontier is empty, while a Big may be written with task-level
questions still open; and grilling's per-round numbering is transcribed here into
stable question IDs. See `docs/method.md` in
the repository for the full attribution.
