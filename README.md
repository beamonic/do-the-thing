# Do the Thing

**Give your AI a Linear issue. Get the work back with evidence.**

Do the Thing is an installable agent skill that connects source review, interviews, Big and Mini Painless Specs, plan critique, execution, and recovery. The name comes from the Korean phrase for “do some work.”

**Available now:** an English skill package, spec/checkpoint templates, a local completion-record validator, and fictional examples. Use it with an agent that already has access to Linear. This is not a hosted app, OAuth integration, background worker, or autonomous webhook service. Live Linear execution has not yet been validated for this release.

## Install

Clone the repository and copy the skill into your agent's skills directory. For Codex:

```sh
git clone https://github.com/beamonic/do-the-thing.git
mkdir -p ~/.codex/skills
cp -R do-the-thing/skills/do-the-thing ~/.codex/skills/
```

If that destination already exists, compare it before replacing your installed copy. Other agents that support `SKILL.md` can use the same self-contained folder in their own skills directory.

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
Sources → Interview (grilling) → Big Painless Spec → Plan and critique → Split tasks
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

An interview is an explicit step. Reuse answers already present in sources and conversation; ask only questions that change the work. The Big interview delegates to [Matt Pocock's `grilling` skill](https://github.com/mattpocock/skills) when it is installed, which asks each round of settled-prerequisite questions together; install it with `npx skills add https://github.com/mattpocock/skills --skill grilling`. It is optional — without it the skill runs the same batch under its own rules — and it belongs after the source read, not before, because it requires the agent to look facts up rather than ask for them. A Mini inherits shared rules instead of asking the whole interview again. If a task uncovers a change to the overall promise, revise the Big and review affected work.

All Minis passing does not mean the Big passes. Verify the complete user journey before closing the work. A completed agent session is not a completed Linear issue.

## Check a completion record

```sh
python3 skills/do-the-thing/scripts/records.py examples/completion.json
python3 -m unittest discover -s tests -v
```

Local tests are available; GitHub Actions is not configured in this initial publication.

The example is **fictional**. The validator checks coverage, declared revisions, and evidence fields; it cannot prove that the evidence is true. It never contacts Linear or changes an issue's state. It does warn when a record still carries the example's `fictional` flag or placeholder evidence, but a warning does not fail the record: read the warnings before trusting a pass.

## Read more

- [Skill entrypoint](skills/do-the-thing/SKILL.md)
- [Product spec and implementation boundaries](docs/spec.md)
- [Method and attribution](docs/method.md)
- [Fictional demonstration](docs/demo-scenario.md)
- [Release status](docs/release-status.md)
- [References](docs/references.md)
- [Publication draft](publishing/beamonic-intro.mdx)

## Contribute

Run the tests above. For behavioral changes, include a realistic input, the expected decision, and evidence of the result. Do not include real customer issues, private documents, or credentials in examples. Report whether a result came from a fixture, a local execution, or a live integration.

## License

[MIT](LICENSE). This project is independently authored. It is not affiliated with Linear, OpenAI, or Gajae Code. No third-party skill implementation or runtime is bundled.
