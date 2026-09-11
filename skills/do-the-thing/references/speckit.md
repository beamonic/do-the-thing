# Spec Kit contract

GitHub's [Spec Kit](https://github.com/github/spec-kit) is a spec-driven development toolkit: `specify init` drops a `.specify/` folder and a set of `speckit.*` agent commands into a repository, and each command writes one artifact under `specs/NNN-feature/`. When a repository already carries it, this skill calls those commands at every step where a Spec Kit artifact is the natural output. Spec Kit produces the files; Linear stays the record of what was asked, decided, and verified. Nothing here replaces the Big, the Minis, or the checkpoint — the Spec Kit files become their evidence.

## Detect, do not install

At step 1, check the repository root once:

- `.specify/` exists, and
- the host exposes the `speckit` commands — as command files (`.claude/commands/speckit.*.md`, `.github/prompts/speckit.*.prompt.md`, or the directory named in `.specify/init-options.json`) or as installed skills named `speckit-*`.

Both present: Spec Kit is on, and the rest of this contract applies. Note the `speckit_version` from `init-options.json` in the checkpoint's input revisions.

Either absent: Spec Kit is off. Say so in one line, offer `specify init --here --ai <agent> --offline` as a single, separate action, and continue with the plain workflow. Do not run `init` inside the workflow — it writes a template tree and can touch the agent's own config, which is the user's decision, not a step of this skill. A repository that has `.specify/` but no commands is treated as off; report the mismatch so the user can re-run `init`.

## How to call a command

Prefer the host's own slash command (`/speckit.specify …`) whenever the host exposes it as a tool or prompt. When it does not, open the command file, run the script it names from the repository root with the flags it names, and follow its instructions with the output — that is what the slash command would have done. Never paraphrase a command from memory; read the installed file, because its version is the one the repository's templates match.

The scripts are the stable interface and always accept `--json`:

| Script | Called by | Gives you |
|---|---|---|
| `.specify/scripts/bash/create-new-feature.sh --json --short-name <name> --number <n> "<description>"` | `specify` | branch, `specs/NNN-name/`, empty `spec.md` |
| `.specify/scripts/bash/setup-plan.sh --json` | `plan` | `FEATURE_SPEC`, `IMPL_PLAN`, `SPECS_DIR`, `BRANCH` |
| `.specify/scripts/bash/check-prerequisites.sh --json [--paths-only] [--require-tasks --include-tasks]` | `clarify`, `tasks`, `implement`, `analyze` | `FEATURE_DIR`, `AVAILABLE_DOCS` |

Pass the Linear identifier through `--short-name` and, when the team numbers features, `--number`, so the feature directory and branch carry the issue key. Read every path the JSON returns as absolute; do not guess a directory from the branch name.

## Where each command belongs

| Step | Command | What it is for here |
|---|---|---|
| 1 Read | read `.specify/memory/constitution.md` | The constitution is a source with authority. Extract its rules into the Big's common rules before interviewing; a rule the constitution already fixes is not an interview question. |
| 1 Read | `/speckit.constitution` | Only when the constitution is still the unfilled template and the issue needs shared rules. Fill it from the sources, then treat it as a source. |
| 2 Interview | `/speckit.clarify` | Runs once the first answers are in. Its questions join the frontier; transcribe each one into a stable question ID, attach your recommended answer, and ask them one per round like every other question. Do not let it run its own five-question loop against the user. Its answers go into `spec.md` **and** the Big's decision log. Do not let it ask a fact you can look up. |
| 2 Big | `/speckit.specify` | Produces `spec.md` from the Big's user scenario, rules, and acceptance criteria. The Big ID, revision, and acceptance IDs go into the spec's header so the two can be diffed. When the Big is revised, re-run and bump both. |
| 3 Plan | `/speckit.plan` | Produces `plan.md` against the Big's exact revision. The plan critique in step 3 runs on this file. |
| 3 Critique | `/speckit.analyze`, `/speckit.checklist` | Cross-artifact consistency and the quality checklist are the mechanical half of the critique. Run them before your own critique, fix what they surface, then critique the judgment they cannot make. |
| 3 Split | `/speckit.tasks` | Produces `tasks.md`. One Mini maps to one task group or one user-story phase in that file, never to a single line item. Each Mini's checklist cites the task IDs it covers; each task cites the Mini. |
| 3 Split | `/speckit.taskstoissues` | Off by default. Linear already holds the work; opening GitHub issues duplicates it. Use only when the user asks for GitHub issues explicitly. |
| 4 Execute | `/speckit.implement` | Runs the Mini. Scope it to that Mini's task IDs — the command wants to run every phase in `tasks.md`, so name the phase or IDs in the argument and stop when they are done. Its progress marks in `tasks.md` are a checkpoint input, not the checkpoint. |
| 5 Verify | `/speckit.analyze`, `/speckit.converge` | Re-run after the Mini's checks. A drift it reports is a failed or untested criterion until resolved. |
| 6 Close | `/speckit.converge` | Assesses the codebase against spec, plan, and tasks together. It is one input to the whole-journey verification, not a substitute for walking the Big's user scenario. |

Step 0 is unchanged. An issue that fails the gate gets no Spec Kit commands either; the same ceremony rule applies.

## Frequency

Call a command every time its artifact would otherwise be written by hand. Do not write `spec.md`, `plan.md`, or `tasks.md` yourself when the command exists, and do not re-run a command whose inputs have not changed. The trigger for a re-run is a changed revision — Big, Mini, plan, or constitution — not a new session.

Re-run `/speckit.analyze` after every artifact change. It is cheap and it is the check most likely to catch a Mini that quietly widened the Big.

## Evidence and records

- The feature directory path and the commit that holds it go into the checkpoint's "Input and output revisions".
- A completion record's `evidence` for a spec-level check is the artifact path; its `artifact_revision` is the commit hash, not the Spec Kit branch name.
- `/speckit.implement`'s `[X]` marks in `tasks.md` are not a passing check. The Mini's own check, run and recorded, is.
- When Spec Kit's numbered feature branch and the team's branch policy disagree, the team's policy wins; record the branch actually used.

## Boundaries

Spec Kit is a tool this skill calls, not a runtime it depends on. Nothing from Spec Kit is bundled here. With Spec Kit off, every step above still runs; only the artifact format changes. This project is not affiliated with GitHub or the Spec Kit maintainers.
