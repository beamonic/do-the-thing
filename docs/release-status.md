# Release status

## 0.5 — English skill package

Implemented: self-contained SKILL.md, Big/Mini/checkpoint templates, Linear interaction contract, completion-record validator, unit tests. A CI workflow was prepared locally but is not published: the current GitHub authorization lacks workflow scope.

Not implemented: hosted executor, Linear OAuth app, webhook worker, automatic task scheduling, automatic merge/deploy, and integrations with other work-management systems.

Live Linear execution has not been tested. The Beamonic article remains an unpublished draft. GitHub publication is tracked by the repository's actual remote state and CI results, not inferred from this file.

## Design history

- 0.2: Integrated Painless Spec and Gajae Code concepts; selected Do the Thing as the name.
- 0.3: Made interviews an independent stage with question/answer and reopening rules.
- 0.4: Defined Big as overall work and Mini as a task; linked criteria, revisions, and aggregate verification.
- 0.5: Implemented the portable skill and record validator in English.
