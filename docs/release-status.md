# Release status

## Next — 필요할 때 먼저 쓰는 O’Reilly 맥락 학습

호스트에 `oreilly-context`가 있으면 사용자의 별도 호출 없이 그릴 전 지식 공백, 스펙의 대안·실패 조건, 낯선 구현·반복 실패에서 활용한다. 단순 수정과 확정된 실행은 건너뛰며 기존 검색은 재사용한다. 검색 후보, 실제 읽은 본문 범위, 구현·검증 반영을 구분한다. 본문을 읽지 못하면 그 한계를 기록하고 공식 문서와 로컬 근거로 진행한다. 계정·구독·외부 스킬을 패키지에 포함하거나 필수로 만들지 않는다.

검증: 저장소 테스트 40개 통과, 변이 23개 모두 검출. 별도 Codex CLI 읽기 전용 평가에서 gpt-5.6-luna가 수정 지침을 읽고 아래 6개 상황의 다음 행동을 답했다. 모두 기대 판단과 일치했다. 단일 모델·단일 실행의 지침 해석 점검이며, 이전 버전 대비 개선율이나 실제 O’Reilly 검색·본문 열람의 성공, 자동 호출률을 입증하지 않는다.

| 입력 상황 | 기대 판단과 관찰 결과 |
|---|---|
| 별도 호출 없이 낯선 재고 도메인의 그릴을 준비 | 먼저 O’Reilly로 개념·질문 관점 학습 |
| 원인과 수정이 확정된 한 글자 오타 | 검색 생략, 바로 수정 |
| 오늘 검색한 관련 후보가 있고 새 질문 없음 | 검색일·읽은 범위와 함께 재사용 |
| 검색 제목만 있고 본문은 403 | 책의 주장으로 쓰지 않고 한계 보고, 공식 문서·로컬 근거 사용 |
| 원인 불명의 동일 구현 실패 두 번 | 동일 세 번째 시도 대신 새 자료·가설 확보 |
| 선택적 스킬이 없지만 공식 문서·테스트로 진행 가능 | 설치를 강제하지 않고 사용 가능한 근거로 진행 |

## 0.16 — 기존 그릴·스펙 인수와 안전한 재개

승인된 그릴·명세·계획을 인수하면 ID, 판, 수용 기준과 실행 권한을 유지하고 첫 미완료 단계부터 진행한다. 명세를 Big 양식에 맞춰 다시 쓰거나 해결된 질문을 반복하지 않는다. 위임된 내부 구현 선택은 에이전트 선택으로 기록한다.

손상된 체크포인트는 보존하고 별도 복구 기록을 만든다. 상태 복구와 완료 검증을 구분하며, 현재 산출물과 모든 Big 수용 기준을 확인하기 전에는 검증 대기로 보고한다.

변이 검사기는 임시 사본에서 실행한다. 테스트가 0건이거나 기준 실행과 건수가 다르면 통과로 처리하지 않는다. 원본 파일 비변경, 0건 실행, 살아남은 변이를 검사하는 회귀 테스트 3개를 추가했다.

검증: 저장소 테스트 40개 통과, 변이 23개 모두 검출. 별도 Codex CLI 작업에서 승인 명세 인수, 구현, subprocess 테스트 2개, CLI 결과와 손상 기록 보존을 확인했다. 상세 범위와 제한은 [터미널 평가](terminal-evaluation.md)에 기록했다. 실제 Linear 장애, 프로세스 강제 종료와 다중 모델 평가는 이번 검증 범위에 포함하지 않았다.

## 0.15 — one question per round, and Spec Kit when it is there

The interview contract now asks one frontier question per round and ends the turn on it. A live run on 2026-09-11 batched six questions with recommended answers into one message and then proceeded as if they were decided; the user never answered one. The contract already said to wait, but a batched list with recommendations reads as a proposal. No answer now pauses the interview — no Big, plan, Minis, or execution on an assumed answer — and a self-supplied answer is recorded as open. "Proceed without answering" is the only way a recommendation becomes a decision, with that instruction as its evidence. This is the third deliberate departure from `grilling`, recorded in `docs/method.md`. (#14)

When a repository already carries GitHub's Spec Kit — `.specify/` plus installed `speckit.*` commands or `speckit-*` skills — the skill calls those commands wherever a step produces the artifact they write: constitution as a source, `clarify` into the frontier one question at a time, `specify`/`plan`/`tasks` for the artifacts, `implement` scoped to one Mini, `analyze` after checks, `converge` as one input to whole-journey verification. `specify init` is never run inside the workflow. Spec Kit's `[X]` marks are not proof; the Mini's own check is. Mapping is in `references/speckit.md`. (#13)

Not yet exercised: a live run under the one-question rule, and any run in a repository with Spec Kit on. Both are the next trials.

## 0.14 — the description parses again

0.13 moved the Korean triggers to the front of the description, which made the value begin with a double quote. To YAML that is a quoted scalar, and the English text after its closing quote is a parse error in any strict loader; the lenient loaders in use did not object, and the regex-based frontmatter test did not look. A one-word label now precedes the first quote so the value is a plain scalar, and the test asserts the three shapes a plain scalar cannot take: opening quote, colon-space, space-hash. The triggers still sit inside the first 60 characters.


## 0.13 — live trials, what they reached and what they did not

Five runs to date. Three on 2026-09-09, recorded in the project's private trial ledger outside this repository: two local, and one on a live Linear issue that went from creation through a question and answer stored in the issue, Big/Mini storage, implementation, browser-verified acceptance criteria, an artifact hash, and a Done transition read back. One of the local runs exercised fresh-context resume from saved records. Two on 2026-09-10 on real work: one whose evidence stays in its own private ledger, and one on this project's own host, CAP-515 — step 0 admitted the task, six sources were measured, two interview rounds ran (one question rephrased when the user did not understand it; one chosen criterion found unmeasurable from the host's logs and re-grounded on another data source without re-asking), four Minis were written into the issue body under `do-the-thing:` markers, one was verified, one completed, one classified blocked with its dependency named, one left open. One gateway write was refused by the gateway's content scan and corrected rather than routed around.

Still not exercised: a native comment thread — every question and answer so far lived in issue-description sections, and the official MCP's `save_comment` is now permitted on this host but untested; crash-simulated resume; a concurrent writer; a no-skill control; forced network failure. CAP-515's two remaining acceptance criteria wait on its host's quota. One live description reached 7,957 of a gateway's 8,000-character limit, so larger work needs linked documents or child tasks — the contract names both, neither is validated yet.

An earlier draft of this note called CAP-515 the first live trial and listed resume and closure as unreached. Both were wrong; the 2026-09-09 ledger had already covered them.

## 0.12 — the Linear contract follows measured capability

Changed: `references/linear.md` no longer assumes one shape of Linear access. It tells the agent to enumerate the host's tool list first, then names the capability each rule needs and the fallback when the host lacks it — a project-linked document or the parent issue body for a Big, a comment thread or the Big's interview table for questions, a parent reference or a shared project for grouping Minis. Rule 4 now prefers an anchored partial edit, since the official MCP's `patch` requires each anchor to match exactly once and therefore fails a save that would silently overwrite a concurrent change; the `do-the-thing: BIG-001` marker is that anchor. A closing paragraph covers hosts that route writes through a gateway with its own required labels, limits, or content scans: satisfy them, record that you did, and report a genuine block rather than switching to an unguarded path.

Evidence: the official Linear MCP's tool list was enumerated rather than read about — 73 tools, `save_*` shaped, create and update in one call. A widely installed third-party skill still documents `create_comment`, `create_issue`, and `update_issue`, none of which exist. That is why the contract now says a tool list you did not enumerate yourself is a guess.


## 0.11 — a gate for not running this at all

Changed: step 0 asks whether the issue needs a spec before anything else happens. An issue that is already clear, bounded, low-risk, and names its own change is done directly and recorded, with no Big and no Minis. Blockers are now classified before being acted on — resolvable by default, human-blocked only for a credential, manual step, external approval, or missing access — and an attempt whose blocker and evidence are unchanged across two consecutive tries is not repeated a third time. On resume, an unreadable or contradicted local record falls back to Linear and the artifacts instead of stopping, and a record holding interview answers, spec revisions, or evidence is never discarded without asking.

Adapted from Gajae Code's deep-interview suitability gate, ultragoal blocker triage, bounded zero-progress escalation, and safe-degradation property; see `docs/method.md`, which also records why its risk-proportional validation was reviewed and left out.


## 0.10 — triggers in the description, portability tested

Changed: the description now carries one Korean trigger per branch the skill handles — delegating an issue, writing the spec, resuming stopped work, checking completion evidence — after the English sentence that already described it. The official field for trigger phrases is `when_to_use`, but that is a Claude Code extension and not among the six keys the Agent Skills spec allows, so using it would break the README's promise that any `SKILL.md` host can run this folder. `license: MIT` was added, which the spec does allow.

`tests/test_skill_frontmatter.py` enforces that: only spec keys, name matching the directory, a description within the 1,536-character listing cap, one distinct trigger per branch, and no broken relative links out of SKILL.md.


## 0.9 — the interview contract ships with the skill

Changed: `references/interview.md` now carries the interview method — the decision tree and its frontier, one round per frontier with a recommended answer attached, transcription into stable question IDs, the rule that the agent finds facts while the user decides, and an ending condition that permits task-level questions to stay open. Earlier revisions called an installed `grilling` skill by name, which meant the method silently degraded to a vague "small coherent batch" wherever that skill was absent. Nothing external is invoked now.

Adapted from Matt Pocock's `grilling` (MIT, Copyright (c) 2026 Matt Pocock) with attribution in the contract, `docs/method.md`, `docs/references.md`, and the README. The text is rewritten, not copied.


## 0.8 — CI and a mutation gate

Implemented: GitHub Actions on push and pull request, running the suite on Python 3.9 and 3.13 plus `scripts/check-mutations.py`, which deletes each of the twenty-three validator guards in turn and requires the suite to fail. The gate was itself verified by deleting one test, which left `unittest` green and the gate red, and by renaming a guard pattern, which the gate reports rather than skipping. The `workflow` token scope that blocked 0.5 was granted on 2026-09-10.

Not implemented: live Linear execution is still untested. That remains the only claim in this repository with no evidence behind it. (Corrected in 0.13: the 2026-09-09 ledger already held one live trial and two local runs when this was written.)

## 0.7 — coverage runs through individual criteria

Changed: a Mini's `criteria` are now objects that each name the Big criterion they serve, replacing the separate `parent_criteria` list. A Big criterion is covered only when a Mini criterion aimed at it passes a check, so a failed or unevidenced check uncovers its parent. The previous shape let one Mini claim several Big criteria while passing a single check of its own; that record now fails with a message naming the change.

This breaks the completion-record format. The package has no released consumers, so no migration path is provided beyond the rejection message.

Still not implemented: everything listed under 0.5. Live Linear execution remains untested. CI arrived in 0.8.

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
