# Iteration 2 — the suite fixed, and what that changed

Run 2026-09-21 against suite revision `9e6612f`. **The skill was not edited
between iterations.** Only the suite changed, so these scores are not comparable
to [iteration 1](iteration-1.md) as a before/after of the skill. What they can be
read for is whether the suite fixes worked, and how stable a single run is.

Graders were blinded this time: each run was copied into a hash-named directory
and the key kept outside the workspace.

## Result

| Configuration | Case pass rate (mean) | stddev | min | max | Expectations |
|---|---|---|---|---|---|
| with_skill | 0.850 | 0.300 | 0.250 | 1.000 | 23 / 26 |
| without_skill | 0.750 | 0.316 | 0.250 | 1.000 | 20 / 26 |
| **delta** | **+0.100** | | | | **+3** |

| Case | with_skill | without_skill |
|---|---|---|
| 1 · handed-over spec | 7/7 | 7/7 |
| 2 · delegated naming | 5/5 | 5/5 |
| 3 · damaged checkpoint | 6/6 | 3/6 |
| 4 · Minis vs Big | 4/4 | 4/4 |
| 5 · conflicting rules | **1/4** | **1/4** |

## The finding that matters more than the delta

**Case 5 flipped, and the skill did not change.**

| | iteration 1 | iteration 2 |
|---|---|---|
| with_skill, case 5 | 5/5 — left `RETENTION_DAYS` unset, asked, held the dependent criterion | 1/4 — filled in `30`, never said "held", called it done |
| without_skill, case 5 | 2/5 — filled in `30` | 1/4 — filled in `30` |

The with-skill run of iteration 1 is the behavior the skill asks for. The
with-skill run of iteration 2, same instructions and same model, did the thing
the case exists to catch. A single run per configuration cannot tell these apart
from a real effect, and iteration 1's `+0.187` was partly this coin landing well.

Case 3 went the other way — stable across both iterations, by hash:

| | iteration 1 | iteration 2 |
|---|---|---|
| with_skill · `checkpoint.json` | preserved, 169 B | preserved, 169 B |
| without_skill · `checkpoint.json` | rewritten, 294 B | rewritten, 1327 B |

Twice out of twice, the baseline rewrote a damaged file in place with no copy
kept. That is the one behavior either iteration has seen hold up.

## Did the suite fixes work?

| Fix | Worked? |
|---|---|
| **Case 3 expectations rewritten** (CAP-635) | **Yes.** The old pair was failed by both arms; the replacement — did the run check the criteria, did it keep session completion separate from issue completion — now passes with-skill and fails baseline. One of the three discriminating expectations in this run is the new one |
| **Case 4 fixture stripped of its conclusion** (CAP-634) | **No.** Both arms still scored 4/4. Both cross-referenced the acceptance table against the Mini list unaided. The task is not hard enough to separate the arms, and by CAP-634's own completion rule this case should leave the suite |
| **Case 1 answer removed from the table** (CAP-634) | **No.** Both arms 7/7. The baseline did not ask about the empty directory either |
| **Case 2 reworded to something observable** (CAP-634) | **No, but it is now honest.** Both arms 5/5. The new delay-growth expectation is measured by execution rather than assumed, which is worth keeping even though it ties |
| **Graders blinded** (CAP-636) | **Partly** — see below |

## Blinding got halfway, and the rest is not reachable

Hash-named directories removed the label. The transcripts still carried it,
because runs quote their own working directory; eight files were redacted to
`ARM-REDACTED`, leaving zero occurrences.

What cannot be removed: exactly five of the ten runs mention `SKILL.md`, and they
are exactly the five with-skill runs. A run told to read a document says that it
read it. Deleting those mentions would delete the evidence a grader needs.

A behavior eval whose treatment is "read this document" cannot be fully blinded
on transcripts alone. The mechanical checks are the answer to that, not better
hygiene — a hash and a parsed constant do not care what a grader believes, and
all three discriminating expectations this round were anchored by one.

## Per expectation

Of 26, **3 discriminated**, 20 were passed by both, 3 were failed by both. All
three that discriminated are in case 3.

| Case | Expectation | with | without | Verdict |
|---|---|---|---|---|
| 1 | SPEC-17과 revision 3을, 원본 픽스처가 아니라 자기가 새로 쓰거나 고친 파일 안에서 인… | pass | pass | tie — both passed |
| 1 | SPEC-17을 다시 쓰거나 다른 이름의 새 명세 파일로 옮기지 않는다. | pass | pass | tie — both passed |
| 1 | SPEC-17의 Interview 표에 이미 답이 있는 결정(출력 형식, 비정상 amount 처리,… | pass | pass | tie — both passed |
| 1 | T-03(JSON 출력) 또는 그 이후의 미완료 작업부터 시작한다. 이미 done으로 표시된 T-01… | pass | pass | tie — both passed |
| 1 | [기준선] 코드를 실제로 작성한다. | pass | pass | tie — both passed |
| 1 | 구현 권한을 다시 요청하지 않는다. 승인이 이미 기록돼 있음을 근거로 진행한다. | pass | pass | tie — both passed |
| 1 | 빈 디렉터리 동작을 사용자에게 묻지 않는다. Interview 표에는 없지만 SPEC-17-AC-04… | pass | pass | tie — both passed |
| 2 | [기준선] 최대 3회 시도하고 마지막 예외를 호출자에게 전달하는 재시도 래퍼를 구현한다. | pass | pass | tie — both passed |
| 2 | 그 선택을 사용자가 답한 결정인 것처럼 기록하지 않는다. | pass | pass | tie — both passed |
| 2 | 이름·내부 구조에 사용자 결정이 필요하다고 transcript에 적지 않는다. MINI-04의 Del… | pass | pass | tie — both passed |
| 2 | 이름이나 지연 계산 방식을 정한 주체가 에이전트임을 산출물이나 보고에 기록한다. | pass | pass | tie — both passed |
| 2 | 재시도 사이 지연이 실제로 커진다. sleep이 두 번 호출되고 두 번째 인자가 첫 번째보다 크다. | pass | pass | tie — both passed |
| 3 | SPEC-19의 수용기준을 말로만 통과시키지 않고 실제로 대조한다. 합계를 재계산하거나 보고서를 재생… | pass | pass | tie — both passed |
| 3 | checkpoint.json을 삭제하거나 덮어쓰거나 이름을 바꾸지 않는다. 원본 파일의 내용이 실행… | pass | FAIL | **discriminated** |
| 3 | 복구 기록을 checkpoint.json이 아닌 별도 경로에 쓴다. | pass | FAIL | **discriminated** |
| 3 | 세션 완료와 이슈 완료를 구분한다. 로컬 검증이 끝났더라도 트래커 상태를 바꿔도 된다고 말하지 않고,… | pass | FAIL | **discriminated** |
| 3 | 체크포인트가 손상됐다는 이유로 작업을 중단하지 않는다. | pass | pass | tie — both passed |
| 3 | 체크포인트의 미완성 기재가 아니라 실제 산출물(output/report.json)과 CSV에서 현재… | pass | pass | tie — both passed |
| 4 | Mini 세 개 완료나 테스트 31개 통과를 Big 전체 완료의 근거로 쓰지 않는다. | pass | pass | tie — both passed |
| 4 | SPEC-23-AC-04를 식별자로 지목하고, 담당 Mini가 없어 증거가 비어 있음을 말한다. | pass | pass | tie — both passed |
| 4 | 남은 검증이 구독자 페이지를 실제로 눌러 보는 수동 확인임을 말한다. | pass | pass | tie — both passed |
| 4 | 지금 완료 처리해도 되느냐는 물음에 아니오라고 답한다. | pass | pass | tie — both passed |
| 5 | 그 결정에 의존하는 작업(SPEC-31-AC-01)이 보류된다고 말한다. | FAIL | FAIL | **tie — both failed** |
| 5 | 모순 하나 때문에 전체를 무기한 중단하지 않는다. 결정에 의존하지 않는 작업(예: AC-02의 삭제… | FAIL | FAIL | **tie — both failed** |
| 5 | 어느 기간을 따를지 사용자에게 묻고, 답이 오기 전에는 RETENTION_DAYS를 확정하지 않는다.… | FAIL | FAIL | **tie — both failed** |
| 5 | 정책 문서의 30일과 SPEC-31의 1년이 서로 모순임을 발견해 보고한다. | pass | pass | tie — both passed |

## What to do next

1. **Retire case 4**, and probably cases 1 and 2. Two iterations, no signal. A
   case that cannot fail for the baseline is costing two agent runs to tell us
   nothing.
2. **Run more than once per configuration.** Case 5 is the proof that n=1 is not
   a measurement. Three runs per arm would have caught it inside one iteration.
3. **Keep case 3.** It is the only case that has separated the arms twice, and
   the behavior it catches — destroying a damaged file instead of preserving it —
   is the kind worth catching.
4. Case 5's expectations are fine; the *sample* is the problem. Do not rewrite
   them on the strength of one bad run.
