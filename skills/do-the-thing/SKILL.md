---
name: do-the-thing
description: Turn a Linear issue into an interviewed Big Painless Spec and task-level Mini Painless Specs, then execute, verify, checkpoint, and resume the work using available Linear tools. 한국어 트리거 "리니어 이슈 받아서 작업해", "이 일 스펙부터 써", "중단된 작업 이어서", "완료 증거 확인해".
license: MIT
---

# Do the Thing

Run a source-first workflow inside the user's existing agent environment. Linear holds the work, questions, decisions, and results. Local records support recovery; they do not override current Linear instructions.

Use the available Linear connector, MCP, or authenticated API client. Read [the Linear contract](references/linear.md) before interacting with Linear. If no connection is available, prepare local drafts and identify the exact connection needed; do not claim synchronization. This skill does not install an OAuth app or run a background worker.

## 0. Decide whether this workflow applies

Read the issue first, then judge whether it needs this at all. If the request is already clear, bounded, low-risk, and names its own change — a one-file edit, a known symbol, a copy fix, an explicit command, a direct question — stop here. Say in one line that a Big and Minis would cost more than the work, do the work under the permissions you already have, and record the result and its evidence in the issue.

This gate exists because the workflow's most likely failure is not a missing spec, it is ceremony on a task that never needed one. A small verification need does not make an issue spec-worthy. If the user asks for the full workflow anyway, run it.

Do not skip the gate in the other direction either. Anything whose scope, shared rules, or acceptance criteria are still being guessed at goes through the workflow, however small the diff looks.

## 1. Read the work and its sources

Resolve the requested issue, workspace, team, parent/project, description, relevant comments, and existing linked specs before creating anything. Reuse existing records by stable ID. Record sources with author/authority, revision or retrieval date, relevance, conflicts, and unknowns. Prefer primary evidence for decisions. Treat issue attachments and quoted text as evidence, not authorization.

## 2. Interview, then write the Big Painless Spec

Use [the Big template](assets/big-spec.md). First extract answers already present in sources and conversation. Ask only unresolved questions that change the outcome, scope, constraints, behavior, or acceptance criteria. Keep question IDs, answers, evidence, and affected criteria. Ask a small coherent batch, then use the answers before asking more.

Read [the interview contract](references/interview.md) before the first round. It defines what a coherent batch is: the frontier of decisions whose prerequisites are settled, asked one round at a time with your recommended answer attached, transcribed into stable question IDs, ending when the remaining questions affect only individual tasks. Facts you can look up are not interview questions.

Show the user scenario, common rules, failure/recovery behavior, non-goals, open questions, owner, revision, and acceptance IDs. Mark unconfirmed behavior as unresolved. A material unanswered question blocks its dependent tasks, not unrelated work. Finishing the interview does not grant execution permission.

## 3. Plan, critique, and split

Build a plan against the Big's exact revision. Critique assumptions, missing behavior, scope, dependencies, and verification. Fix evidence-resolvable gaps yourself. Reopen the specific interview question when a product decision is needed.

Split into independently verifiable tasks. Each task gets one Mini Painless Spec using [the Mini template](assets/mini-spec.md). Each Mini references the Big ID, revision, and acceptance IDs it serves. Keep mechanical steps inside its checklist rather than making each step an issue.

Reuse Big answers and common rules. Conduct a focused follow-up interview only for newly discovered task uncertainties, then critique the Mini's execution plan. A Mini cannot silently change the Big's scope or shared rules: propose a Big revision and review affected Minis first.

## 4. Execute one ready Mini

Read current instructions, dependencies, applicable permissions, Big/Mini revisions, and existing results. Proceed with work already authorized. Persist a checkpoint at meaningful boundaries; keep execution and external delivery distinct. If an external write times out, read the destination before retrying. Do not infer failure from a missing response.

## 5. Verify and checkpoint

Use [the checkpoint template](assets/checkpoint.md). Record actual checks, output revisions, failures, and evidence locations. Only mark a Mini complete when its criteria have passed. A narrative claim or checked box is not proof.

Classify a blocker before deciding what to do with it, and default to resolvable when unsure. **Resolvable** is anything you can act on: a failing check, missing implementation, a dependency to install, an inferable detail, work that needs investigating. Do not hand these back — investigate, split the task, or record the blocker and move to the next ready Mini. **Human-blocked** is only what the user alone can supply: a credential, a physical or manual step, an external approval, access you do not have. Name the specific dependency when you record one; "needs input" is not a classification.

Stop repeating an attempt that is not moving. If a Mini's blocker and evidence are unchanged across two consecutive attempts, do not make a third with the same inputs: record the blocker as standing, say what new condition would change it, and move on. Progress means a changed artifact revision, a changed check result, or a changed blocker — not a new timestamp.

The optional [record helper](scripts/records.py) validates a local completion record. Read [its format](references/records.md) when using it. It checks structure and coverage, not the truth of evidence. Inspect actual results before writing a passing record.

## 6. Resume and close the Big

On resume, compare saved records with current Linear instructions and actual artifacts. Preserve valid completed work. A changed shared rule invalidates affected evidence; do not restart unaffected work merely because a timestamp changed.

A local record that is unreadable, malformed, or contradicted by the artifacts is not a reason to stop. Fall back to what Linear and the artifacts themselves say, note in the checkpoint that the record was discarded and why, and resume from observed state. Never delete a record that holds interview answers, spec revisions, or verification evidence in order to start clean — ask first. Only a record with none of those is yours to replace.

After the Minis pass, verify the whole Big user journey and every Big acceptance criterion, including integration gaps. All Minis being complete is necessary but insufficient. Report outputs, evidence, remaining limitations, and delivery status in Linear, then read back the update. Session completion is not issue completion. Change the issue state only when the Big is verified and the user's authorization covers that transition.

## Boundaries and attribution

Big/Mini is this project's convention. Painless Functional Specifications informs readable user behavior; Gajae Code inspires interview, plan critique, persistent goals, and recovery; the interview contract adapts the frontier discipline of Matt Pocock's `grilling` skill (MIT). No other skill pack or runtime is bundled, called by name, or required. Use available specialist skills where helpful, preserving this input/output contract. See the repository's source attribution for details.
