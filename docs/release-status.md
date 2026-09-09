# Release status

## 0.7 — coverage runs through individual criteria

Changed: a Mini's `criteria` are now objects that each name the Big criterion they serve, replacing the separate `parent_criteria` list. A Big criterion is covered only when a Mini criterion aimed at it passes a check, so a failed or unevidenced check uncovers its parent. The previous shape let one Mini claim several Big criteria while passing a single check of its own; that record now fails with a message naming the change.

This breaks the completion-record format. The package has no released consumers, so no migration path is provided beyond the rejection message.

Still not implemented: everything listed under 0.5. Live Linear execution remains untested, and CI is still unpublished — the GitHub token in use carries `gist`, `read:org` and `repo`, but not `workflow`.

## 0.6 — hardened checks and delegated interview

Changed: tests assert the specific error each guard raises, verified by deleting each of the eighteen guards in turn; the validator now reports non-blocking warnings for `fictional` flags and placeholder evidence; the Big interview delegates to Matt Pocock's `grilling` skill when installed, with its completion condition narrowed and its rounds transcribed into stable question IDs. The documented Python floor moved from 3.10 to 3.9 after running the suite on 3.9.6; no 3.10-only syntax was in use.

Still not implemented: everything listed under 0.5. Live Linear execution remains untested.

## 0.5 — English skill package

Implemented: self-contained SKILL.md, Big/Mini/checkpoint templates, Linear interaction contract, completion-record validator, unit tests. A CI workflow was prepared locally but is not published: the current GitHub authorization lacks workflow scope.

Not implemented: hosted executor, Linear OAuth app, webhook worker, automatic task scheduling, automatic merge/deploy, and integrations with other work-management systems.

Live Linear execution has not been tested. The Beamonic article remains an unpublished draft. GitHub publication is tracked by the repository's actual remote state and CI results, not inferred from this file.

## Design history

- 0.2: Integrated Painless Spec and Gajae Code concepts; selected Do the Thing as the name.
- 0.3: Made interviews an independent stage with question/answer and reopening rules.
- 0.4: Defined Big as overall work and Mini as a task; linked criteria, revisions, and aggregate verification.
- 0.5: Implemented the portable skill and record validator in English.
