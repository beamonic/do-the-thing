# Linear interaction contract

This is an agent-operated integration through tools supplied by the host, not an installed Linear agent service. Tool names differ by host; discover the available operations rather than inventing calls.

1. Read viewer/workspace identity and the target issue, team, current status, relevant comments, and linked project or parent. Match the user's intended destination.
2. Locate an existing Big and Minis before creating records. Search the issue's actual relationships and stable spec markers, not titles alone.
3. Store a Big in a project-linked document or parent issue body. Store a Mini in its task issue body. For a single-task trial, use separate Big/Mini sections in the same issue. Keep local IDs and resulting Linear IDs/URLs mapped in checkpoints.
4. Preserve unrelated user content when editing. Read the latest body before writing. Use a unique marker such as `do-the-thing: BIG-001` to find the managed section; do not overwrite the whole description from a stale copy.
5. Put material questions in the relevant issue, then consume the answer from that same scope. Record the responder and decision; an unrelated comment does not resolve a question.
6. Before creating child issues, inspect existing children and dependencies. Create only the authorized scope. After each mutation, read back its ID, parent relationship, body, and status as relevant. If the response is uncertain, reconcile before retrying; do not promise exactly-once delivery.
7. Select statuses from the team's actual configured states. Never hard-code a status UUID or equate an agent session ending with a completed issue.
8. Record failed or incomplete synchronization explicitly. Keep a local checkpoint until remote results are verified. Do not place credentials or private source contents in public examples.

For implementations that add a background service later, consult current official API documentation for OAuth, webhooks, signatures, activities, and signals. This package does not implement those capabilities.
