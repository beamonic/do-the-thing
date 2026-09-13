# Domain modeling inside Do the Thing

Use when competing meanings of a domain term, state, or relationship could change behavior. Skip when consuming an already accepted vocabulary without a conflict.

Read the project's existing glossary, relevant spec, examples, and actual behavior first. Reuse their location and authority; a file named `CONTEXT.md` is not required. Distinguish an observed implementation from the intended rule: code can reveal a contradiction but cannot settle a product decision by itself.

For an overloaded term, propose precise alternatives and a concrete boundary example. For example, an order can be canceled while a refund is still pending; do not silently collapse those states. Extract existing answers before asking. Route only a material unresolved decision into the Big's stable question IDs, one question per round, and wait for its answer. Do not reopen accepted terms just to prefer a different name.

When authorized to write, record the resolved term, meaning, example/counterexample, source, and revision in the existing glossary or spec. Create a small glossary only if none exists and a resolved concept needs durable reuse. Keep implementation details in the plan, not the vocabulary. A review-only request produces proposed corrections, not file edits.

Suggest an ADR only when a decision is costly to reverse, surprising without its rationale, and involved real alternatives. Otherwise use the existing decision record. If a changed meaning affects acceptance criteria, propose a Big revision and identify affected Minis; no automatic mass rename or scope change.

Adapted in original wording from Matt Pocock's `domain-modeling` (MIT); reviewed source and deliberate differences are in the repository's `docs/method.md` and `docs/references.md`.
