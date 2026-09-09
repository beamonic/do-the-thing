# Product specification

Status: Skill implementation available; live Linear trial pending.
Version: 0.5. Owner: Unassigned.
Change: Package the approved Big/Mini workflow as an English agent skill with templates and a completion-record validator. The earlier hosted-runtime design remains future work, not an implemented capability.

## User and outcome

A person managing work in Linear delegates an issue to an agent. They answer material questions in the same work context and receive artifacts with verification evidence. When the session stops, the next session reads the records and actual outputs before resuming.

For example, Morgan asks for a password-reset help page. The agent reads the source requirements, discovers that missing-email behavior is unspecified, and asks about that behavior. It writes the agreed user journey into a Big, critiques the plan, and defines a Mini for the bounded page change. After implementation, it checks the Mini and then the full journey. A working link alone does not prove that a visitor can find and understand the instructions.

## Current implementation

The distributable object is `skills/do-the-thing`: a self-contained skill with referenced templates and a Python validator. The host agent supplies reasoning, execution tools, and authenticated Linear access. The skill controls the procedure through instructions, not a deterministic execution scheduler.

The validator checks completion-record structure and coverage. It rejects missing or failing checks, duplicate Mini IDs, wrong or stale parent references, missing Big coverage, and absent aggregate verification. Separately it warns, without failing the record, when a record still carries the sample's `fictional` flag or placeholder evidence. It does not authenticate sources, inspect artifacts, fetch current revisions, or enforce concurrency. Human and agent review must establish evidence truth and current inputs.

One coverage rule is weaker than it looks. A Mini declares which Big criteria it serves, and the checks it must pass are its own; nothing ties an individual Mini check to an individual parent criterion. A Mini may therefore claim several Big criteria while passing one check of its own. The aggregate `big_checks` exist because of that gap, and they are themselves self-declared. Treat both as bookkeeping, not proof.

## Big and Mini contracts

| Property | Big Painless Spec | Mini Painless Spec |
|---|---|---|
| Unit | Overall work or project | Independently verifiable task |
| Content | Full user scenario, common rules, scope/non-goals, exceptions, open decisions, acceptance IDs | Task scenario, inputs/outputs, inherited and local rules, exceptions, acceptance IDs and methods |
| Parent link | Lists responsible Minis | Big ID, exact revision, parent acceptance IDs |
| Interview | Establish purpose, constraints, behavior, and success/failure examples | Reuse answers; ask only newly discovered material questions |
| Completion | Whole-journey and all-criteria verification | Actual task evidence and checkpoint |

Keep mechanical actions as checklist items within a Mini. Do not create a new spec for every click or command. Mini completion is necessary but insufficient for Big completion.

## Workflow contract

1. Read sources, revisions, authority, conflicts, and existing Linear records.
2. Interview explicitly. Preserve questions, answers, evidence, and dependent criteria. Unknown behavior remains unknown.
3. Write the Big with owner, revision, user scenario, shared rules, non-goals, exceptions, and acceptance IDs.
4. Plan and critique. Resolve factual gaps; return product decisions to the relevant interview question.
5. Split tasks and write Minis referencing the Big. Ask focused follow-up questions, then critique each task plan.
6. Execute authorized, ready work against current instructions and revisions.
7. Verify the Mini, record output revisions and evidence, and checkpoint.
8. Resume from current records and actual artifacts. Repeat only checks whose inputs or evidence changed.
9. Verify the Big journey independently, deliver the results in Linear, and read them back.

A material unresolved question blocks its dependent tasks, not every task. Interview completion does not grant execution permission. Existing authorization remains usable within its scope. New shared-rule or scope decisions return to the Big; a Mini must not silently override them.

## Linear mapping

A Big may live in a project-linked document or parent issue body. A Mini lives in its task issue body. A one-task trial can store separate Big and Mini sections in the same issue. Preserve stable spec IDs, source links, and actual Linear IDs in checkpoints.

Read viewer/workspace and target identity before writes. Inspect existing records to avoid duplicate tasks. Preserve unrelated content and reread before editing. Read back successful changes. An uncertain response requires reconciliation before retrying. Use actual team states; never hard-code a status ID.

## Records and future runtime objects

| Object | Purpose | Current form |
|---|---|---|
| InterviewRecord | Questions, answers, evidence, affected criteria | Template section |
| FunctionalSpec | `level: big/mini`, ID, revision, behavior, criteria, parent references | Markdown; completion JSON subset |
| PlanRevision | Spec inputs, plan, critique, ready conditions | Template section |
| GoalRecord | Task/Mini, dependencies, execution and verification state | Mini and checkpoint |
| WorkflowDefinition | Ordered contracts and reusable guidance | SKILL.md and references |
| ExecutionAttempt | Attempt, input/output revisions, state, next condition | Checkpoint |
| Verification | Criterion, output revision, method, evidence, result | Completion JSON and narrative evidence |
| DeliveryRecord | External request, confirmed/uncertain result, read-back | Checkpoint |

A future service could enforce leases, event deduplication, webhook verification, activity streaming, and persisted state transitions. None of those are implemented by this package. No exactly-once network execution guarantee is made.

## Verification and open work

Automated tests cover completion validation, including rejecting Mini-only closure and stale parent revisions. Each test asserts the specific error its guard must produce, because a test that only asserts "some error appeared" still passes when its guard is deleted and an unrelated guard fires on the same fixture. Deleting any one of the validator's eighteen guards fails at least one test. They still do not prove that an agent follows the skill or that Linear writes work.

Before claiming live integration success, run a permitted trial: interview, store Big/Mini, execute an actual task, stop/resume, inspect evidence, and read back Linear results. Keep the issue ID, artifact revision, and actual observations. Hosted executor selection, OAuth, event recovery, retention, and any automatic deployment remain open decisions.
