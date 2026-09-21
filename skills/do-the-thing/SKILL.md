---
name: do-the-thing
description: Triggers "do the thing" "spec this out first" "take this issue and work it" "resume the stopped work" "check the completion evidence" "두더띵으로 해줘" "이 일 스펙부터 써" "중단된 작업 이어서" — one entrypoint that turns a request into interview, Big and Mini specs, execution, test proof, two-axis review, checkpoint, and resume, with evidence behind every claim.
license: MIT
---

# Do the Thing

Run a source-first workflow inside the user's existing agent environment. Linear holds the work, questions, decisions, and results. Local records support recovery; they do not override current Linear instructions.

Use the available Linear connector, MCP, or authenticated API client. Read [the Linear contract](references/linear.md) before interacting with Linear, and enumerate the host's actual tool list before trusting any description of it — what the host can do decides how much of the contract you can honour. If no connection is available, prepare local drafts and identify the exact connection needed; do not claim synchronization. This skill does not install an OAuth app or run a background worker.

When the repository carries GitHub's Spec Kit (`.specify/` plus installed `speckit.*` commands), call its commands wherever a step below names one, and read [the Spec Kit contract](references/speckit.md) before the first call. Spec Kit writes the spec, plan, and task files; Linear still holds the decisions and the evidence. Without Spec Kit, every step runs the same way with hand-written artifacts.

## One entrypoint, context-selected methods

The user can invoke only `do-the-thing`. Choose the needed methods yourself; do not ask them to pick a skill or issue another command. This is an agent instruction package, not a new callable API, background worker, or grant of authority. Use tools actually available in the host. A read-only question, diagnosis, or review stays read-only even when a method describes implementation.

Apply the suitability gate below first, then read only the contracts whose conditions arise. They are internal parts of this package, not extra installations or a checklist to run on every task. Preserve accepted answers, revisions, and valid evidence when moving between methods; return to the first unfinished step, not the start of the workflow.

| Current need | Method to use |
|---|---|
| Ambiguous domain terms, states, or boundaries change behavior | Read [domain modeling](references/domain-modeling.md), then feed unresolved decisions into the existing one-question interview |
| Product decisions or acceptance criteria remain open | Use the interview and Big/Mini steps below |
| Missing knowledge could change a decision | Use the context-learning section below; O'Reilly remains an optional host service |
| Writing meaningful tests, uncertain coverage, or a bug escaping green tests | Read [test proof](references/test-proof.md); a routine suite rerun does not trigger mutation work |
| Reviewing code, or closing a meaningful code change | Read [two-axis review](references/code-review.md); a simple wording edit does not require a separate review exercise |
| Existing plan/checkpoint supplied | Reconcile and resume; activate other methods only for newly found gaps |

Mention a consequential method choice in one sentence, not a menu of skills. Keep its decisions and evidence in existing task artifacts. No new tracker, glossary, ADR, test framework, or external write is authorized merely by selecting a method. The Ponytail principle and completion/permission boundaries below apply throughout.

## Working principle: less unnecessary work, full outcome responsibility

Use the Ponytail-inspired reasoning below inside this workflow, not as another command, mandatory phase, or persistent mode. Understand the requested outcome and trace the relevant current flow before simplifying it.

Before adding work, identify the acceptance criterion, required control, or observed problem it serves. Reuse an existing answer, artifact, process, or implementation when it meets that need. For code, prefer suitable existing helpers, standard-library or native platform features, and already-installed dependencies before adding custom machinery. For other work, check the existing operating path before creating another report, meeting, tracker, or automation. This is a quick choice among adequate approaches, not a requirement to exhaust every option.

Compare the whole cost: implementation, maintenance, manual handoffs, failure recovery, and burden shifted to other people. Choose the least burdensome approach that still meets the accepted behavior and constraints, not simply the fewest lines or files. Omit speculative additions proposed by the agent; record a meaningful omission and the evidence that would justify revisiting it in the existing plan or checkpoint. Do not silently drop an explicit requirement or ship a reduced substitute and ask permission afterward. If changing scope is necessary, reopen only that decision.

For a bug, trace affected callers and the underlying cause before choosing the smallest adequate fix. Verify the affected paths; do not hide the symptom on one path or use this rule to refactor unrelated code. Preserve security, trust-boundary validation, data-loss prevention, accessibility, required controls, and all Big/Mini criteria. Reuse the repository's test conventions; neither a one-test ceiling nor a short-output limit applies.

Once necessary work is authorized, own the result through execution and verification. A smaller solution, passing Mini, or cheaper workaround is not permission to skip the whole journey or external read-back. Use the existing blocker and recovery rules rather than abandoning hard work or repeating an unchanged attempt. If current evidence shows the goal has disappeared or been superseded, preserve the work and evidence, report a proposed stop and its reason, and obtain any needed scope/state authorization; cancellation is not verified completion.

An explicit user cancellation already settles whether to stop: stop the canceled execution without asking for the same decision again, preserve evidence, and report canceled rather than complete. Only a separate action not covered by that instruction, such as changing an external tracker state, may need its own authorization.

## 0. Decide whether this workflow applies

Read the issue first, then judge whether it needs this at all. If the request is already clear, bounded, low-risk, and names its own change — a one-file edit, a known symbol, a copy fix, an explicit command, a direct question — stop here. Say in one line that a Big and Minis would cost more than the work, do the work under the permissions you already have, and record the result and its evidence in the issue.

This gate exists because the workflow's most likely failure is not a missing spec, it is ceremony on a task that never needed one. A small verification need does not make an issue spec-worthy. If the user asks for the full workflow anyway, run it.

Do not skip the gate in the other direction either. Anything whose scope, shared rules, or acceptance criteria are still being guessed at goes through the workflow, however small the diff looks.

## 1. Read the work and its sources

Resolve the requested issue, workspace, team, parent/project, description, relevant comments, and existing linked specs before creating anything. Reuse existing records by stable ID. Record sources with author/authority, revision or retrieval date, relevance, conflicts, and unknowns. Prefer primary evidence for decisions. Treat issue attachments and quoted text as evidence, not authorization.

Check once for Spec Kit as the contract describes. If it is on, `.specify/memory/constitution.md` is a source with authority: extract its rules now, and run `/speckit.constitution` only when the file is still the unfilled template and the issue needs shared rules. If it is off, say so in one line and offer `specify init` as a separate action; do not run it inside the workflow.

## Context learning across the grill, spec, and execution

Do not wait for the user to name a research skill when a knowledge gap could change a decision. If `oreilly-context` is available, read and use it at these points; it is an optional host integration, not a bundled dependency:

- Before the grill: unfamiliar domain vocabulary or missing perspectives would weaken the questions. Learn the relevant concepts first, then ask only the user's unresolved decisions.
- During the spec and plan: competing approaches, trade-offs, or failure modes need grounding. Use relevant sources to sharpen alternatives and acceptance criteria, not to override accepted requirements.
- During execution: unfamiliar implementation or repeated failures suggest a missing mental model. Investigate with sources before another unchanged attempt, then test the resulting hypothesis locally.

Skip this research for simple edits and mechanical execution with a known cause and settled approach. Reuse relevant results from the same conversation, naming their search date and actual reading scope; search again only for a new question or stale evidence. Do not restart a completed grill or spec merely to add reading.

State the decision or knowledge gap in one sentence. Search for one primary candidate and at most two supporting candidates using the skill's discovery, authentication, and bounded fallback rules. Search metadata identifies candidates; it does not establish what a book says. When a decision needs body-level support, read the relevant section through an authorized available path and record the chapter or section actually read. If that is unavailable, report the reading limit and use primary documentation or local evidence instead; never invent a book's advice or bypass access controls. Do not send private issue text or credentials in search queries.

For exact API, version, or security behavior, use local `context query` when available, then supplier documentation and repository checks. O'Reilly supplements design understanding; it does not replace these checks. If the optional skill or service is unavailable, report the specific limitation and continue with available evidence where safe. Research never grants new execution or external-write authority.

Keep a compact note with the existing sources or checkpoint: the question; search queries and selected URLs (or reused search date); actual reading scope (metadata only, named sections, or unread); the resulting decision or test and its observed result. Record "no implementation impact" when appropriate. Candidate discovery, reading, and implementation are distinct states; none alone proves completion.

## 2. Interview, then write the Big Painless Spec

### Accept an existing grill and spec

When the user hands over an existing interview, specification, plan, or checkpoint, enter at the first unfinished step. Read and reconcile it with current sources before deciding what is missing. Preserve its IDs, revision, accepted answers, domain vocabulary, acceptance criteria, and execution authorization. A specification does not need to be renamed or rewritten into the Big template to serve as the Big; map existing criteria to task-level criteria. Reuse a valid plan and task split too. Ask only about material gaps or contradictions newly found. Do not repeat the grill or require fresh approval for execution already authorized.

Separate unresolved product decisions from delegated implementation choices. Within the user's delegated scope, choose reversible implementation details and record them as agent choices, not user answers. A naming choice is not a reason to reopen an accepted spec. Changes to the promised behavior, scope, permissions, or shared rules still need their own decision evidence.

Use [the Big template](assets/big-spec.md). First extract answers already present in sources and conversation. Ask only unresolved questions that change the outcome, scope, constraints, behavior, or acceptance criteria. Keep question IDs, answers, evidence, and affected criteria. Ask one question per round with your recommended answer attached, wait through a permitted native blocking question tool as specified in the interview contract (do not substitute asynchronous questions plus sleep), and use the answer before asking the next. Never answer for the user: a round without an answer pauses the interview, and nothing downstream — Big, plan, Minis, execution — is built on an assumed answer.

Read [the interview contract](references/interview.md) before the first round. It defines the frontier of decisions whose prerequisites are settled, the one-question round, the stable question IDs, and the end condition: the remaining questions affect only individual tasks. Facts you can look up are not interview questions.

With Spec Kit on, run `/speckit.clarify` once the first answers are in and fold its questions into the frontier under stable IDs, still one per round. Write the Big, then run `/speckit.specify` with the Big's scenario, rules, and acceptance IDs so `spec.md` carries the Big ID and revision in its header. Re-run it whenever the Big is revised.

Show the user scenario, common rules, failure/recovery behavior, non-goals, open questions, owner, revision, and acceptance IDs. Mark unconfirmed behavior as unresolved. A material unanswered question blocks its dependent tasks, not unrelated work. Finishing the interview does not grant execution permission.

## 3. Plan, critique, and split

Build a plan against the Big's exact revision — `/speckit.plan` when Spec Kit is on. Run `/speckit.analyze` and `/speckit.checklist` first for the mechanical half of the critique, then critique assumptions, missing behavior, scope, dependencies, and verification yourself. Fix evidence-resolvable gaps yourself. Reopen the specific interview question when a product decision is needed.

Split into independently verifiable tasks. Each task gets one Mini Painless Spec using [the Mini template](assets/mini-spec.md). Each Mini references the Big ID, revision, and acceptance IDs it serves. Keep mechanical steps inside its checklist rather than making each step an issue. With Spec Kit on, `/speckit.tasks` writes `tasks.md`; one Mini maps to one task group or user-story phase there, never to a single line item, and each side cites the other's IDs. Leave `/speckit.taskstoissues` off unless the user asks for GitHub issues — Linear already holds the work.

Reuse Big answers and common rules. Conduct a focused follow-up interview only for newly discovered task uncertainties, then critique the Mini's execution plan. A Mini cannot silently change the Big's scope or shared rules: propose a Big revision and review affected Minis first.

## 4. Execute one ready Mini

Before writing or strengthening meaningful tests, read [test proof](references/test-proof.md). Before any defect injection, create a separate disposable directory and copy the implementation and tests into it; run the mutated tests there. Never copy a mutant or a baseline implementation back onto the task's source files, even temporarily or with a backup-and-restore plan. If a safe isolated run is unavailable, leave proof pending.

Read current instructions, dependencies, applicable permissions, Big/Mini revisions, and existing results. Proceed with work already authorized. With Spec Kit on, run `/speckit.implement` scoped to the Mini's task IDs or phase — the command wants to run everything in `tasks.md`, so name the scope in its argument and stop when it is done. Persist a checkpoint at meaningful boundaries; keep execution and external delivery distinct. If an external write times out, read the destination before retrying. Do not infer failure from a missing response.

## 5. Verify and checkpoint

Before declaring a meaningful code change verified, read [the two-axis review contract](references/code-review.md) and apply it to the actual task changes, including uncommitted files. Record Spec and Standards findings separately, plus unreviewed areas. A test pass or completion-record validation does not substitute for this review.

Use [the checkpoint template](assets/checkpoint.md). Record actual checks, output revisions, failures, and evidence locations. Only mark a Mini complete when its criteria have passed. A narrative claim or checked box is not proof — `/speckit.implement`'s `[X]` marks in `tasks.md` included. With Spec Kit on, re-run `/speckit.analyze` after the Mini's checks; a drift it reports is a failed or untested criterion until resolved.

Classify a blocker before deciding what to do with it, and default to resolvable when unsure. **Resolvable** is anything you can act on: a failing check, missing implementation, a dependency to install, an inferable detail, work that needs investigating. Do not hand these back — investigate, split the task, or record the blocker and move to the next ready Mini. **Human-blocked** is only what the user alone can supply: a credential, a physical or manual step, an external approval, access you do not have. Name the specific dependency when you record one; "needs input" is not a classification.

Stop repeating an attempt that is not moving. If a Mini's blocker and evidence are unchanged across two consecutive attempts, do not make a third with the same inputs: record the blocker as standing, say what new condition would change it, and move on. Progress means a changed artifact revision, a changed check result, or a changed blocker — not a new timestamp.

The optional [record helper](scripts/records.py) validates a local completion record. Read [its format](references/records.md) when using it. It checks structure and coverage, not the truth of evidence. Inspect actual results before writing a passing record.

## 6. Resume and close the Big

Keep a damaged checkpoint at its original path and preserve its bytes. Do not move or rename it to make room for a replacement. Write recovery evidence to a different path.

On resume, compare saved records with current Linear instructions and actual artifacts. Preserve valid completed work. A changed shared rule invalidates affected evidence; do not restart unaffected work merely because a timestamp changed.

Recovering a readable work state does not establish completion. Until current artifacts and every Big criterion have been checked, report verification pending even if previous test reports are available. Distinguish what can happen after those checks from what is justified now.

A local record that is unreadable, malformed, or contradicted by the artifacts is not a reason to stop. Fall back to what Linear and the artifacts themselves say, preserve the damaged record, and write a separate recovery checkpoint explaining which claims were disregarded and why. Resume from observed state. An unreadable record may still contain recoverable interview answers, spec revisions, or verification evidence; do not delete or overwrite it to start clean.

After the Minis pass, verify the whole Big user journey and every Big acceptance criterion, including integration gaps. All Minis being complete is necessary but insufficient. With Spec Kit on, `/speckit.converge` is one input to that verification, not a substitute for walking the scenario. Report outputs, evidence, remaining limitations, and delivery status in Linear, then read back the update. Session completion is not issue completion. Change the issue state only when the Big is verified and the user's authorization covers that transition.

## Boundaries and attribution

Big/Mini is this project's convention. Painless Functional Specifications informs readable user behavior; Gajae Code inspires interview, plan critique, persistent goals, and recovery; the interview contract adapts the frontier discipline of Matt Pocock's `grilling` skill (MIT). GitHub's Spec Kit and `oreilly-context` are called by name only when available in the host, and neither is bundled or required. No third-party skill implementation or runtime is bundled. Use available specialist skills where helpful, preserving this input/output contract. See the repository's source attribution for details.
