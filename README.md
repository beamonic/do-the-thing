# Do the Thing

**Give your AI a Linear issue. Get the work back with evidence.**

Do the Thing is an installable agent skill that connects source review, interviews, Big and Mini Painless Specs, plan critique, execution, and recovery. The name comes from the Korean phrase for “do some work.”

**Available now:** the skill package with its interview contract, Big/Mini/checkpoint templates, a completion-record validator whose suite is mutation-tested in CI, and fictional examples. Use it with an agent that already has access to Linear. This is not a hosted app, OAuth integration, background worker, or autonomous webhook service. Five runs so far, two of them on live Linear issues — one closed to Done with the whole journey verified and resume exercised, one still in progress. Native comment threads and crash-simulated resume are untested. See [release status](docs/release-status.md).

## Install

Clone the repository and copy the skill into your agent's skills directory. For Codex:

```sh
git clone https://github.com/beamonic/do-the-thing.git
mkdir -p ~/.codex/skills
cp -R do-the-thing/skills/do-the-thing ~/.codex/skills/
```

If that destination already exists, compare it before replacing your installed copy. Other agents that support `SKILL.md` can use the same self-contained folder in their own skills directory. The frontmatter deliberately stays inside the six keys the Agent Skills spec allows, so a Claude Code extension such as `when_to_use` is not used and `tests/test_skill_frontmatter.py` fails if one appears.

The description opens with a one-word label and the Korean trigger phrases, one per branch the skill handles, and the English summary follows. The label is there because a YAML value that begins with a quote is a quoted scalar, and strict loaders reject what comes after its closing quote — `tests/test_skill_frontmatter.py` now fails on that shape. The order is deliberate: a host with many skills shortens every description to its first sixty or so characters — measured at 60–64 on a Codex host carrying 154 skills — so whatever must survive goes first. The English still matches an English request.

Connect Linear through your agent's supported connector, MCP, or API client. The skill discovers the available operations; it does not bundle credentials or assume a specific tool name. Python 3.9+ is needed only for the optional record validator; it is tested on 3.9 and 3.13.

## Use

```text
Use $do-the-thing on Linear issue TEAM-123.
Read its sources, interview me about unresolved decisions, and create a Big
Painless Spec. Split it into task-level Mini Painless Specs, then execute
work within the permissions I have given you. Keep evidence and checkpoints
in the same work context so we can resume later.
```

`TEAM-123` is a placeholder. Start with a non-sensitive trial issue. If Linear is not connected, the agent can prepare drafts locally but must not report them as synchronized.

## The workflow

```text
Does this issue need a spec at all? → no: do the work, record it, stop
  yes:
Sources → Interview → Big Painless Spec → Plan and critique → Split tasks
  For each task:
  Mini Painless Spec → Focused follow-up interview → Plan and critique
    → Execute → Verify Mini → Checkpoint → Next task
  Then:
  Verify the whole Big user journey → Deliver and read back in Linear
```

| Spec | Responsibility |
|---|---|
| Big Painless Spec | Overall user outcome, scope, shared rules, exceptions, and acceptance criteria |
| Mini Painless Spec | One verifiable task, its behavior and evidence, linked to the Big revision and criteria |

The first step is deciding whether to run the rest. An issue that is already clear, bounded, low-risk, and names its own change gets done directly, with the result recorded in the issue — no Big, no Minis. The workflow's likeliest failure is ceremony on a task that never needed one, not a missing spec.

An interview is an explicit step, and [its contract](skills/do-the-thing/references/interview.md) ships with the skill. Questions are asked one frontier at a time — every decision whose prerequisites are already settled, together, each with the agent's recommended answer — and the round is transcribed into stable question IDs before anything is acted on. Facts the agent can look up are not interview questions. The interview may end with questions still open when they affect only individual tasks. That discipline is adapted from Matt Pocock's `grilling` skill; nothing needs to be installed alongside this one. A Mini inherits shared rules instead of asking the whole interview again. If a task uncovers a change to the overall promise, revise the Big and review affected work.

If the repository already carries GitHub's Spec Kit, the agent calls its `speckit.*` commands at each of those steps — `clarify` feeds the interview, `specify`, `plan`, and `tasks` write the artifacts, `implement` runs one Mini at a time, `analyze` and `converge` feed verification — as [the Spec Kit contract](skills/do-the-thing/references/speckit.md) maps them. Nothing is installed for you, and the workflow is the same without it.

All Minis passing does not mean the Big passes. Verify the complete user journey before closing the work. A completed agent session is not a completed Linear issue.

## Check a completion record

```sh
python3 skills/do-the-thing/scripts/records.py examples/completion.json
python3 -m unittest discover -s tests -v
```

GitHub Actions runs both on every push and pull request: the suite on Python 3.9 and 3.13, and a mutation gate.

```sh
python3 scripts/check-mutations.py
```

The gate deletes each of the validator's guards in turn and requires the suite to fail. A guard no test covers is a guard that can be removed without anyone noticing, which is what happened here before 0.6 — every test asserted only that some error appeared, so an unrelated guard firing on the same fixture covered for the missing one. `tests/mutations.json` lists the guards; renaming one without updating that list fails the gate rather than passing quietly.

The example is **fictional**. Each Mini criterion names the Big criterion it serves, and a Big criterion counts as covered only when a Mini criterion aimed at it actually passes. The validator checks coverage, declared revisions, and evidence fields; it cannot prove that the evidence is true. It never contacts Linear or changes an issue's state. It does warn when a record still carries the example's `fictional` flag or placeholder evidence, but a warning does not fail the record: read the warnings before trusting a pass.

## Read more

- [Skill entrypoint](skills/do-the-thing/SKILL.md)
- [Interview contract](skills/do-the-thing/references/interview.md)
- [Spec Kit contract](skills/do-the-thing/references/speckit.md)
- [Product spec and implementation boundaries](docs/spec.md)
- [Method and attribution](docs/method.md)
- [Fictional demonstration](docs/demo-scenario.md)
- [Release status](docs/release-status.md)
- [References](docs/references.md)
- [Publication draft](publishing/beamonic-intro.mdx)

## Contribute

Run the tests above. For behavioral changes, include a realistic input, the expected decision, and evidence of the result. Do not include real customer issues, private documents, or credentials in examples. Report whether a result came from a fixture, a local execution, or a live integration.

## License

[MIT](LICENSE). This project is independently authored. It is not affiliated with Linear, OpenAI, GitHub, Gajae Code, or Matt Pocock. No third-party skill implementation or runtime is bundled or invoked. The interview contract adapts the frontier discipline of the `grilling` skill (MIT, Copyright (c) 2026 Matt Pocock), rewritten here; see [method and attribution](docs/method.md).
