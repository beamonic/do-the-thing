# Completion record format

Run `python3 <skill-path>/scripts/records.py <record.json>` using Python 3.9 or newer. Exit 0 means structurally complete coverage; 1 means incomplete or invalid coverage; 2 means unreadable input. The helper never calls Linear or marks work done. The repository's `examples/completion.json` is a sample input; it ships outside the skill folder, so write your own record when only the skill is installed.

Top-level fields:

- `big`: `id`, positive integer `revision`, nonempty list of `criteria` IDs.
- `minis`: nonempty list of objects with `id`, `revision`, `criteria`, `parent_id`, `parent_revision`, and `checks`.
- `big_checks`: independent aggregate checks covering all Big criteria.

Each entry in a Mini's `criteria` is an object naming the criterion and the Big criterion it serves: `{"id": "MINI-AC-01", "parent": "BIG-AC-01"}`. A Big criterion counts as covered only when some Mini criterion pointing at it has a check that actually passed, so a failed or unevidenced check leaves its parent uncovered. The pre-0.7 shape — a bare list of Mini criterion IDs plus a separate `parent_criteria` list — is rejected with a message naming the change; it let one Mini claim several Big criteria while passing a single check of its own.

Each check contains `criterion`, the exact spec `revision`, `result` (`pass` to satisfy completion), `method`, `evidence` (path or URL), and `artifact_revision` (commit, file digest, or other immutable output revision).

The helper rejects missing checks, duplicate IDs/checks, failed checks, stale declared parent/spec revisions, unknown criteria, missing evidence fields, a Mini criterion whose parent is not a Big criterion, and any Big criterion left without a passing Mini criterion. It also returns a `warnings` list, which does not change the exit code: it names a record still flagged `fictional` and counts checks whose method, evidence, or artifact revision still says `fictional`. Read the warnings before trusting a pass. It does not fetch Linear, open evidence, execute tests, or detect dishonest results. A structurally valid fictional example is not evidence of a real run. Update the Big revision from the actual source before evaluating a record.

Keep working checkpoints using the checkpoint template even when a completion record cannot yet pass. Preserve prior records when inputs change; do not rewrite history to make an old result appear current.
