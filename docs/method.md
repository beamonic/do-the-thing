# Method and attribution

Painless Functional Specifications informs readable descriptions of user behavior. Gajae Code inspires explicit interviews, plan critique, persistent goals, verification, and recovery. The interview contract adapts the frontier discipline of Matt Pocock's grilling skill. Linear is the shared work surface.

**Big Painless Spec** for overall work and **Mini Painless Spec** for a task are this project's conventions. They are not terms attributed to Joel Spolsky or Gajae Code.

## Interview first, then refine

Read available sources and extract prior answers. Interview only for unresolved decisions that change the result. Store question IDs, answers, evidence, and affected criteria. Write the Big, critique the plan, and split into Minis. Each Mini reuses shared answers and asks focused follow-up questions only where needed.

A plan critique may uncover a product decision. Reopen that particular question rather than restarting the interview. If the answer changes a shared rule, revise the Big and review affected Minis and evidence.

## Durable execution

A task has a verifiable outcome, not just a list of actions. Record actual outputs, input revisions, verification results, and the next condition in checkpoints. Resume by comparing those records with current instructions and actual artifacts. Stop repeating an attempt when it cannot make progress without a new condition.

Verify the full Big user journey after the Minis pass. Individual outputs can each look correct while their integration fails.

## Source boundaries

Joel Spolsky's essays inform user scenarios, non-goals, open issues, ownership, revision, and readable specifications. The design used a previously reviewed source summary; it does not claim a new full reading during packaging.

Story/Rules/Examples/Questions and Given/When/Then belong to BDD and Cucumber-related practice, not Joel's original method. Spec IDs, Big/Mini references, and evidence linkage are our implementation choices.

The reviewed Gajae Code material includes portions of the pinned ultragoal skill and its recovery documentation. No Gajae Code runtime or third-party skill code is copied or invoked by this package. Symphony is a reference for issue-driven execution, not a dependency.

The `grilling` skill by Matt Pocock (MIT, Copyright (c) 2026 Matt Pocock) is the source of the interview method in `references/interview.md`. Its design tree, its frontier of questions whose prerequisites are settled, its one-round-per-frontier discipline, and its rule that the agent finds facts while the user makes decisions are its ideas, not ours.

Earlier revisions called that skill by name and required it to be installed. It is now adapted into this package instead, so nothing has to be installed alongside it. The wording in `references/interview.md` is ours, and two of grilling's rules are deliberately changed: grilling ends when the frontier is empty, whereas a Big may be written while questions affecting only individual tasks stay open, and grilling's per-round numbering is transcribed into stable question IDs rather than used as one. Its text is not reproduced; the ideas are credited here and in that file.

O'Reilly's *Specification by Example* and *Building Applications with AI Agents* were discovered through search metadata. Their full texts were not read for this implementation, and no specific book claim is used as an implementation requirement. See [references](references.md).
