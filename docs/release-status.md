# Release status

## 0.20 — 트래커 없이도 돌고, 설치가 한 줄이다

0.19까지 이 스킬은 Linear를 전제로 썼다. SKILL.md 7줄, 템플릿 3개, 계약서 2개가 전부 트래커가 있다고 가정했다. 그런데 0.19에서 만든 평가 스위트의 사례 두 개는 트래커를 아예 안 쓴다 — **`+0.357`이라는 그 숫자는 Linear 없이 나온 것**이고, 그동안 README는 Linear가 필요하다고 말하고 있었다.

같은 판에서 설치 경로도 고쳤다. `npx skills add beamonic/do-the-thing`이 레지스트리에서 이미 동작하고 있었는데 README는 그걸 안 알려주고 `git clone` 후 수동 복사를 시키고 있었다.

### 변경

- 트래커가 선택이 됐다. Spec Kit이 처음부터 그랬던 것처럼 "있으면 부르고, 없으면 모든 단계가 똑같이 돈다"로 내렸다. 용어를 하나 세웠다 — **work record**가 일·질문·결정·결과를 쥔다. 트래커가 붙어 있으면 트래커, 없으면 사용자가 찾을 수 있는 파일. Linear는 이 스킬이 계약서를 가진 트래커로 남고, 다른 트래커도 ID·read-back·증거 규칙은 그대로 따른다.
- **증거 규율은 하나도 안 풀었다.** 바뀐 건 기록이 어디 사는지지, 기록을 남기느냐가 아니다. SKILL.md의 Linear 언급이 7곳에서 1곳(조건부 계약 참조)으로 줄었다.
- 템플릿 3개와 계약서 2개의 Linear 전용 항목을 work record로 바꿨다.
- README 맨 위가 `npx skills add beamonic/do-the-thing` 한 줄이다. 수동 복사는 아래로 내렸다. 헤드라인도 `Give your AI a Linear issue`에서 `Give your AI a task. Get it back with evidence for every claim.`로 바꿨다.
- frontmatter 트리거가 영어 우선이 됐다. 한국어 트리거는 남긴다. **트리거를 요약보다 앞에 두는 설계는 유지했다** — 스킬 154개 물린 Codex 호스트에서 설명이 60~64자로 잘리는 걸 실측했고, 잘려도 살아남아야 하는 건 홍보 문구가 아니라 매칭이다.

### 검증과 한계

트래커 변경은 스킬 구성 3회씩, 사례 두 개를 실제로 돌려 쟀다. **판정 기준은 실행 전에 커밋 메시지에 박았다.** 기록은 `evals/results/iteration-7.md`.

| 사전 기준 | 요구 | 실측 |
| -- | -- | -- |
| 손상 체크포인트 바이트 보존 | 3/3 | 3/3 (각 169바이트) |
| 복구본 별도 경로 | 3/3 | 3/3 |
| `RETENTION_DAYS` 미설정 | 2/3 이상 | 3/3 |

do-no-harm 검사다. 두 사례 모두 트래커를 안 쓰니 아무 점수도 안 움직여야 했고, 안 움직였다.

**기준 하나는 안 쟀다.** 기준선 구성이 0/3을 유지하는지는 돌리지 않았다 — 기준선은 SKILL.md를 아예 안 읽으니 이 변경이 닿을 수 없고, 그 숫자는 네 회차에서 이미 재현됐다. 실행 전에 비용을 반으로 줄이려고 그렇게 정했다. 통과가 아니라 **미측정**으로 적는다. 건너뛴 기준은 충족한 기준이 아니다.

`RETENTION_DAYS`가 0.19 기록의 2/3에서 3/3으로 돌아왔다. **이 변경의 효과라고 주장하지 않는다.** 충돌 규칙 판단에 닿는 부분이 이 diff에 없고, n=3에서 한 판 차이는 iteration 6이 스스로 "추세가 아니라 한 실행"이라고 적은 바로 그 크기다.

여섯 판 중 세 판이 호스트의 개인 쓰기 가드에 걸려 서로 다르게 우회했다(heredoc / 디렉터리 안 `git init` / `.txt` 확장자). 기계 점검에는 안 닿지만 판마다 환경이 달랐던 건 사실이다. 운영자 개인 훅이 없는 환경에서 돌리는 게 맞고, 아직 안 했다.

아직 안 된 것: **트래커 없이 도는 걸 사용자가 실제로 겪는 방식으로는 안 쟀다.** 두 사례 다 로컬 파일 작업이다. 실제 이슈를 열고 동기화하고 거기서 재개하는 경로는 여전히 미실증이다. Spec Kit 저장소 라이브 시험, 네이티브 코멘트 스레드, 강제 종료 후 재개, 동시 쓰기, 네트워크 실패도 그대로 남아 있다.

## 0.19 — 스킬이 실제로 효과가 있는지 재는 장치

이 릴리즈는 스킬 규칙을 거의 바꾸지 않는다. 대신 **바꿨을 때 좋아졌는지 나빠졌는지 알 수 있게** 만든다. 0.18까지는 "강화했다"를 산문으로만 말했고, 그 말이 맞는지 확인할 방법이 없었다.

`docs/terminal-evaluation.md`에 산문으로 있던 행동 사례를 재실행 가능한 스위트(`evals/`)로 옮기고, 네 회차를 실제로 돌렸다.

### 변경

- `evals/` 신설. 사례마다 에이전트에게 건넬 픽스처와 채점 항목을 함께 둔다. 스킬 붙인 실행과 안 붙인 실행을 같은 사례로 돌려 비교한다.
- `evals/scripts/mechanical_checks.py` — 해시·파싱된 상수·실제 실행으로 답하는 항목은 채점자 판단에 맡기지 않는다. 손상 파일의 SHA-256, 소스에서 파싱한 상수, 모듈을 임포트해 돌려 본 결과.
- `evals/scripts/blind_runs.py` — 채점 전에 실행을 해시 이름 디렉터리로 옮기고 구성 라벨을 가린다. 키는 작업공간 밖에 둔다.
- `tests/test_evals.py` — 스위트가 로드 가능하고, 픽스처가 실재하고, 사례마다 기준선을 넘는 항목이 있고, 프롬프트가 스킬 이름을 부르지 않는지 검사한다. 각 가드는 격리 사본에 결함을 주입해 실제로 무는지 확인했다.
- `scripts/check-mutations.py`가 `evals/`도 임시 트리에 복사한다. 없는 디렉터리는 건너뛰어 러너 자체 테스트의 최소 픽스처가 깨지지 않는다.

### 검증과 한계

네 회차를 돌렸고 회차마다 스위트 자신의 결함이 먼저 나왔다.

1회차: 채점 항목 25개 중 20개가 두 구성을 전혀 가르지 못했다. 실행 전에 쓴 변별력 예측은 "강하다"고 매긴 15개 중 5개만 맞았다. 픽스처 세 개가 결론을 미리 적어 두고 있었다.

2회차: 픽스처를 고쳐도 그 세 사례는 여전히 양쪽 만점이었다. 더 중요한 건 사례 하나가 **스킬을 한 글자도 안 바꿨는데** 5/5에서 1/4로 뒤집힌 것이다. 구성당 1회 실행으로는 우연과 효과를 구분할 수 없다.

3회차: 신호 없는 사례 세 개를 `evals/retired/`로 은퇴시키고 구성당 3회로 올렸다. 처음으로 구성 간 차이(+0.357)가 구성 내 분산(0.094)보다 확실히 컸다. 같은 회차에서 스킬 결함도 하나 나왔다 — 답을 기다려야 할 질문이 생기면 그 질문에 **의존하지 않는 작업까지** 멈춘다. 해당 규칙은 SKILL.md에 이미 있었고, 그 문장을 읽은 실행 3회 중 2회가 어겼다.

4회차: 그 결함을 고친 수정을 같은 스위트로 재봤다. 대조군 사례는 정확히 재현됐는데 고친 자리가 무너졌다 — 스킬이 값을 함부로 정하지 않던 비율이 3/3에서 0/3으로 떨어졌다. 판정 기준은 실행 전에 적어 뒀고 거기서 깨졌다. **수정은 기각했고 이 릴리즈에 들어 있지 않다.** 기록은 `evals/results/iteration-4.md`, 시도 자체는 `fix/open-question-blast-radius` 브랜치에 남겼다.

숫자의 한계는 그대로다. 실행 모델과 채점 모델 모두 Sonnet 한 종이고, 회차마다 스위트가 달라진 구간에서는 회차 간 점수를 비교할 수 없다. 3회차와 4회차만 스위트가 같아 직접 비교된다. 채점자 블라인드는 절반만 된다 — 경로 라벨은 가렸지만 스킬을 읽은 실행은 그 사실을 인용하고, 그 단서는 증거를 지우지 않고는 못 없앤다. 그래서 결정적인 항목은 기계적 검사로 고정한다.

아직 안 된 것: 3회차가 찾은 과잉 차단은 그대로 있다. Spec Kit을 갖춘 저장소에서의 라이브 시험, 네이티브 Linear 코멘트 스레드, 강제 종료 후 재개, 동시 쓰기, 네트워크 실패는 여전히 미실증이다. 1st-party `claude plugin eval`은 이 계정에서 early access로 막혀 있다 — 열리면 `--ablation`·`--runs`·`--threshold`가 이 수작업 루프를 명령 하나로 대체한다.

## 0.18 — 네이티브 질문 대기와 두 터미널 검증

인터뷰에서 질문을 보낸 뒤 답변을 받기 전에 다음 결정으로 넘어가던 문제를 다룬다. Claude Code는 `AskUserQuestion`, Codex는 사용 가능한 모드의 `request_user_input`으로 질문하고 실제 응답을 기다린다. 접수 성공이나 미리 선택된 추천 항목은 답변으로 취급하지 않는다.

### 변경

- 네이티브 답변 대기를 기본으로 하고, 비동기 질문을 보낸 뒤 반복 대기하는 방식은 기본 경로에서 제외했다.
- 호스트가 질문 도구를 Plan 모드로 제한하면 그 조건을 알린다. 스킬이 모드를 임의로 바꾸거나 도구 제한을 우회하지 않는다.
- 비동기·평문 질문은 사용자가 그 방식을 명시적으로 받아들인 경우에만 쓴다. 기존 답변과 질문 ID를 보존한다.

### 검증과 한계

Codex CLI 0.153.4의 Plan 모드와 Claude Code 2.1.263 터미널에서 네이티브 선택지·직접 입력·응답 반환을 실행 검증했다. Claude의 첫 직접 입력은 값이 전달되지 않아 재질문했고, 재입력 후 정상 반환을 확인했다. 에이전트가 조작한 합성 시험이며, 스킬 자동 발견이나 실제 업무 전체 여정을 증명하지 않는다. 자세한 절차는 [터미널 검증 기록](terminal-question-proof.md)에 있다.

데스크톱 사이드바의 ‘답변 요청’ 라벨은 실화면 검증을 완료하지 않았다. 질문 표시·도구 접수·응답 수신·사이드바 상태를 서로 다른 증거로 다룬다. [질문 대기 계약과 검증 범위](async-interview-verification.md)를 참고한다.

Codex 상류 구현에는 일반 모드 질문을 허용하는 실험 설정도 있지만, Plan 요청만 `is_blocking: true`로 처리한다. 따라서 설정만 켜면 무기한 답변 대기가 보장된다고 안내하지 않는다. 이 릴리즈는 사용자 설정을 변경하지 않는다. 근거: [공식 요청 처리 코드](https://github.com/openai/codex/blob/2f8603f07547247e698748884542ba60a157621c/codex-rs/core/src/tools/handlers/request_user_input.rs).

## 0.17 — 맥락별 단일 진입점과 Claude Code 실동작 검증

v0.16 이후 합성한 기능을 하나의 버전으로 묶는다. 아래의 과거 Codex 판단 평가와 이번 [Claude Code 실동작 평가](claude-code-evaluation-0.17.md)는 서로 다른 검증이다.

### 두더띵 단일 진입점과 세 내부 전문 지침

도메인 모델링, 테스트 증명, 명세/저장소 규칙 분리 리뷰를 설치형 스킬 폴더 안의 내부 참조로 합성했다. 사용자는 두더띵만 호출하고 에이전트가 현재 필요에 맞는 지침만 읽는다. 새 MCP/API나 백그라운드 실행기는 아니다. 기존 명세·용어집·계획은 재사용하며, 조회·진단·리뷰 요청은 쓰기 권한으로 확장하지 않는다.

검증: 저장소 테스트 40개, 변이 검사 23개 검출, 스킬 형식 검증 통과. 별도 gpt-5.6-luna 읽기 전용 평가 7개에서 오타 수정·유효 계획 재개는 추가 지침 생략, 용어 충돌은 도메인+인터뷰, 권한 테스트 공백은 테스트 증명, 미커밋 리뷰는 분리 리뷰로 선택했다. 병렬 에이전트가 없어도 리뷰를 진행하고, 문법 오류·수집 0건은 무효 변이로 분류하며, 규칙 준수로 명세 누락을 덮지 않았다. 판단 응답 평가이며 실제 업무의 호출 정확도·수행 효과나 외부 연동을 입증하지 않는다.

### Ponytail 판단 기준 합성

두더띵 하나로 그릴·스펙·필요한 학습·실행·검증을 이어가되, 전체 흐름에 필요성·재사용·운영 부담 판단을 적용한다. 명시 요구나 필수 검증을 줄이지 않는다. Ponytail의 지속 모드·강도 단계·출력 제한·테스트 하나 제한·축소판 선출시는 가져오지 않았다. 원문 고정 판과 재서술 범위는 [방법과 출처](method.md)에 기록했다.

로컬 검사: 저장소 테스트 40개, 변이 23개 검출, 스킬 형식 검증 통과. 별도 gpt-5.6-luna 읽기 전용 판단 평가에서 기존 CSV 헬퍼 재사용, 오프라인 요구 보존, 결제 전체 여정 검증, 공유 파서 원인 추적, 반복 실패 조사, 불필요한 수기 보고 생략, 필요한 O’Reilly 학습 유지의 7개 상황이 기대와 일치했다. 명시적 취소 상황은 중단을 다시 제안하는 응답이 나와, 취소 지시 재확인을 요구하지 않도록 보강했다. 이는 지침 해석 점검이며 실제 구현·외부 연동 성능이나 이전 판 대비 개선율을 입증하지 않는다.

보강 후 별도 CLI 재검토에서 P1/P2 지적은 없었다. 명시적 취소는 재승인 없이 실행 중단·증거 보존, 모든 기준과 실제 증거가 있는 경우는 완료, 목표 소멸의 간접 자료만 있는 경우는 임의 취소하지 않음으로 구분했다. 세 판단 모두 기대와 일치했다.

### 필요할 때 먼저 쓰는 O’Reilly 맥락 학습

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
