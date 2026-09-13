# Two-axis review inside Do the Thing

Use for a requested code review or before closing a meaningful code change. This is review, not permission to fix, commit, push, or deploy. For non-code work use its acceptance checks instead of manufacturing code-style findings.

Resolve the user's comparison target, or infer the current task's verified base if unambiguous; ask only when that ambiguity changes the reviewed scope. Pin base and head revisions. Review committed changes from their merge base, and include relevant staged, unstaged, and untracked task changes when the request includes work in progress. Do not mistake `base...HEAD` for a review of uncommitted changes. An empty diff means no changes in that comparison, not proof the work is correct.

Reuse the exact accepted Big/Mini revisions and the repo's documented standards. No specific tracker file or separate setup command is required. Inspect two distinct axes:

- **Spec:** missing or partial requirements, unintended additions, incorrect behavior, and missing evidence for the promised journey. Cite the acceptance ID or requirement and the actual changed path.
- **Standards:** violations of applicable documented repo rules. Separate hard violations from maintainability suggestions; do not turn a preference for abstraction or fewer lines into a mandatory refactor. Skip issues already conclusively enforced by tooling.

Use independent reviewers when available and proportionate. Otherwise perform separate passes and state that they were not independent. A missing spec or unavailable execution check is an unreviewed area, never a pass; use the requested behavior already present in the conversation when it is sufficient, without demanding a new document.

Keep findings labeled by axis, path/line, evidence, severity, and consequence. A clean standards pass cannot offset a failed requirement. Combine only exact duplicates while retaining both labels. Respect the repo's blocking severity rules and report each axis plus remaining checks. When implementation is authorized, fix in-scope findings and recheck affected evidence; otherwise return findings only. Neither a clean review nor an agent's conclusion establishes completion without the required checks.

Adapted in original wording from Matt Pocock's `code-review` (MIT), without mandatory parallel agents, fixed setup files, or a universal smell checklist.
