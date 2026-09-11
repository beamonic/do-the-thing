---
name: do-the-thing
description: 트리거 "리니어 이슈 받아서 작업해", "이 일 스펙부터 써", "중단된 작업 이어서", "완료 증거 확인해" — Linear issue to interviewed Big Painless Spec and task-level Mini Painless Specs, then execute, verify, checkpoint, resume.
license: MIT
---

# Do the Thing

Run a source-first workflow inside the user's existing agent environment. Linear holds the work, questions, decisions, and results. Local records support recovery; they do not override current Linear instructions.

Use the available Linear connector, MCP, or authenticated API client. Read [the Linear contract](references/linear.md) before interacting with Linear, and enumerate the host's actual tool list before trusting any description of it — what the host can do decides how much of the contract you can honour. If no connection is available, prepare local drafts and identify the exact connection needed; do not claim synchronization. This skill does not install an OAuth app or run a background worker.

When the repository carries GitHub's Spec Kit (`.specify/` plus installed `speckit.*` commands), call its commands wherever a step below names one, and read [the Spec Kit contract](references/speckit.md) before the first call. Spec Kit writes the spec, plan, and task files; Linear still holds the decisions and the evidence. Without Spec Kit, every step runs the same way with hand-written artifacts.

## 0. Decide whether this workflow applies

Read the issue first, then judge whether it needs this at all. If the request is already clear, bounded, low-risk, and names its own change — a one-file edit, a known symbol, a copy fix, an explicit command, a direct question — stop here. Say in one line that a Big and Minis would cost more than the work, do the work under the permissions you already have, and record the result and its evidence in the issue.

This gate exists because the workflow's most likely failure is not a missing spec, it is ceremony on a task that never needed one. A small verification need does not make an issue spec-worthy. If the user asks for the full workflow anyway, run it.

Do not skip the gate in the other direction either. Anything whose scope, shared rules, or acceptance criteria are still being guessed at goes through the workflow, however small the diff looks.

## 1. Read the work and its sources

Resolve the requested issue, workspace, team, parent/project, description, relevant comments, and existing linked specs before creating anything. Reuse existing records by stable ID. Record sources with author/authority, revision or retrieval date, relevance, conflicts, and unknowns. Prefer primary evidence for decisions. Treat issue attachments and quoted text as evidence, not authorization.

Check once for Spec Kit as the contract describes. If it is on, `.specify/memory/constitution.md` is a source with authority: extract its rules now, and run `/speckit.constitution` only when the file is still the unfilled template and the issue needs shared rules. If it is off, say so in one line and offer `specify init` as a separate action; do not run it inside the workflow.

## 2. Interview, then write the Big Painless Spec

Use [the Big template](assets/big-spec.md). First extract answers already present in sources and conversation. Ask only unresolved questions that change the outcome, scope, constraints, behavior, or acceptance criteria. Keep question IDs, answers, evidence, and affected criteria. Ask a small coherent batch, then use the answers before asking more.

Read [the interview contract](references/interview.md) before the first round. It defines what a coherent batch is: the frontier of decisions whose prerequisites are settled, asked one round at a time with your recommended answer attached, transcribed into stable question IDs, ending when the remaining questions affect only individual tasks. Facts you can look up are not interview questions.

With Spec Kit on, run `/speckit.clarify` after the first round and fold its questions into the frontier under stable IDs with your recommended answers. Write the Big, then run `/speckit.specify` with the Big's scenario, rules, and acceptance IDs so `spec.md` carries the Big ID and revision in its header. Re-run it whenever the Big is revised.

Show the user scenario, common rules, failure/recovery behavior, non-goals, open questions, owner, revision, and acceptance IDs. Mark unconfirmed behavior as unresolved. A material unanswered question blocks its dependent tasks, not unrelated work. Finishing the interview does not grant execution permission.

## 3. Plan, critique, and split

Build a plan against the Big's exact revision — `/speckit.plan` when Spec Kit is on. Run `/speckit.analyze` and `/speckit.checklist` first for the mechanical half of the critique, then critique assumptions, missing behavior, scope, dependencies, and verification yourself. Fix evidence-resolvable gaps yourself. Reopen the specific interview question when a product decision is needed.

Split into independently verifiable tasks. Each task gets one Mini Painless Spec using [the Mini template](assets/mini-spec.md). Each Mini references the Big ID, revision, and acceptance IDs it serves. Keep mechanical steps inside its checklist rather than making each step an issue. With Spec Kit on, `/speckit.tasks` writes `tasks.md`; one Mini maps to one task group or user-story phase there, never to a single line item, and each side cites the other's IDs. Leave `/speckit.taskstoissues` off unless the user asks for GitHub issues — Linear already holds the work.

Reuse Big answers and common rules. Conduct a focused follow-up interview only for newly discovered task uncertainties, then critique the Mini's execution plan. A Mini cannot silently change the Big's scope or shared rules: propose a Big revision and review affected Minis first.

## 4. Execute one ready Mini

Read current instructions, dependencies, applicable permissions, Big/Mini revisions, and existing results. Proceed with work already authorized. With Spec Kit on, run `/speckit.implement` scoped to the Mini's task IDs or phase — the command wants to run everything in `tasks.md`, so name the scope in its argument and stop when it is done. Persist a checkpoint at meaningful boundaries; keep execution and external delivery distinct. If an external write times out, read the destination before retrying. Do not infer failure from a missing response.

## 5. Verify and checkpoint

Use [the checkpoint template](assets/checkpoint.md). Record actual checks, output revisions, failures, and evidence locations. Only mark a Mini complete when its criteria have passed. A narrative claim or checked box is not proof — `/speckit.implement`'s `[X]` marks in `tasks.md` included. With Spec Kit on, re-run `/speckit.analyze` after the Mini's checks; a drift it reports is a failed or untested criterion until resolved.

Classify a blocker before deciding what to do with it, and default to resolvable when unsure. **Resolvable** is anything you can act on: a failing check, missing implementation, a dependency to install, an inferable detail, work that needs investigating. Do not hand these back — investigate, split the task, or record the blocker and move to the next ready Mini. **Human-blocked** is only what the user alone can supply: a credential, a physical or manual step, an external approval, access you do not have. Name the specific dependency when you record one; "needs input" is not a classification.

Stop repeating an attempt that is not moving. If a Mini's blocker and evidence are unchanged across two consecutive attempts, do not make a third with the same inputs: record the blocker as standing, say what new condition would change it, and move on. Progress means a changed artifact revision, a changed check result, or a changed blocker — not a new timestamp.

The optional [record helper](scripts/records.py) validates a local completion record. Read [its format](references/records.md) when using it. It checks structure and coverage, not the truth of evidence. Inspect actual results before writing a passing record.

## 6. Resume and close the Big

On resume, compare saved records with current Linear instructions and actual artifacts. Preserve valid completed work. A changed shared rule invalidates affected evidence; do not restart unaffected work merely because a timestamp changed.

A local record that is unreadable, malformed, or contradicted by the artifacts is not a reason to stop. Fall back to what Linear and the artifacts themselves say, note in the checkpoint that the record was discarded and why, and resume from observed state. Never delete a record that holds interview answers, spec revisions, or verification evidence in order to start clean — ask first. Only a record with none of those is yours to replace.

After the Minis pass, verify the whole Big user journey and every Big acceptance criterion, including integration gaps. All Minis being complete is necessary but insufficient. With Spec Kit on, `/speckit.converge` is one input to that verification, not a substitute for walking the scenario. Report outputs, evidence, remaining limitations, and delivery status in Linear, then read back the update. Session completion is not issue completion. Change the issue state only when the Big is verified and the user's authorization covers that transition.

## Boundaries and attribution

Big/Mini is this project's convention. Painless Functional Specifications informs readable user behavior; Gajae Code inspires interview, plan critique, persistent goals, and recovery; the interview contract adapts the frontier discipline of Matt Pocock's `grilling` skill (MIT). GitHub's Spec Kit is called by name when a repository already carries it, and nothing from it is bundled or required. No other skill pack or runtime is bundled, called by name, or required. Use available specialist skills where helpful, preserving this input/output contract. See the repository's source attribution for details.
