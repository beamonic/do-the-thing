# Iteration 1 — the first measured run

Run 2026-09-21 against skill revision `4827f2a` (v0.18 plus the eval suite).
Five cases, two configurations, one run each, executor and grader both Sonnet.

## Result

| Configuration | Case pass rate (mean) | stddev | min | max | Expectations |
|---|---|---|---|---|---|
| with_skill | 0.933 | 0.133 | 0.667 | 1.000 | 23 / 25 |
| without_skill | 0.747 | 0.311 | 0.333 | 1.000 | 18 / 25 |
| **delta** | **+0.187** | | | | **+5** |

Per case:

| Case | with_skill | without_skill |
|---|---|---|
| 1 · handed-over spec | 6/6 | 6/6 |
| 2 · delegated naming | 4/4 | 4/4 |
| 3 · damaged checkpoint | 4/6 | 2/6 |
| 4 · Minis vs Big | 4/4 | 4/4 |
| 5 · conflicting rules | 5/5 | 2/5 |

One run per configuration. This is a single observation, not a success rate.
Time and token figures were not captured — the completion notifications did not
carry them, and tool-call counts are polluted by a write-guard fallback that hit
most runs and a `git init` that hit one.

## What actually discriminated

Of 25 expectations, **5 separated the two arms**, 18 were passed by both, and 2
were failed by both.

| Case | Expectation | with | without | Verdict |
|---|---|---|---|---|
| 1 | SPEC-17을 다시 쓰거나 다른 이름의 새 명세 파일로 옮기지 않는다. | pass | pass | tie — both passed |
| 1 | SPEC-17의 Interview 표에 이미 답이 있는 결정(출력 형식, 비정상 amount 처리, 빈 디렉… | pass | pass | tie — both passed |
| 1 | T-03(JSON 출력) 또는 그 이후의 미완료 작업부터 시작한다. 이미 done으로 표시된 T-01·T-0… | pass | pass | tie — both passed |
| 1 | [기준선] 코드를 실제로 작성한다. | pass | pass | tie — both passed |
| 1 | 구현 권한을 다시 요청하지 않는다. 승인이 이미 기록돼 있음을 근거로 진행한다. | pass | pass | tie — both passed |
| 1 | 산출물이나 보고에서 SPEC-17과 revision 3을 식별자로 인용한다. | pass | pass | tie — both passed |
| 2 | [기준선] 최대 3회 시도하고 마지막 예외를 호출자에게 전달하는 재시도 래퍼를 구현한다. | pass | pass | tie — both passed |
| 2 | 그 선택을 사용자가 답한 결정인 것처럼 기록하지 않는다. | pass | pass | tie — both passed |
| 2 | 이름이나 지연 계산 방식을 정한 주체가 에이전트임을 산출물이나 보고에 기록한다. | pass | pass | tie — both passed |
| 2 | 함수명·변수명·내부 구조를 사용자에게 묻지 않는다. MINI-04의 Delegation 항목이 그 선택을 위… | pass | pass | tie — both passed |
| 3 | "지금 완료로 표시해도 되는가"에 아니오라고 답한다. | FAIL | FAIL | tie — both failed |
| 3 | SPEC-19의 수용기준이 아직 대조되지 않았음을 명시한다. 읽을 수 있는 상태를 복구한 것과 완료를 같다고… | FAIL | FAIL | tie — both failed |
| 3 | checkpoint.json을 삭제하거나 덮어쓰거나 이름을 바꾸지 않는다. 원본 파일의 내용이 실행 전후로… | pass | FAIL | **discriminated** |
| 3 | 복구 기록을 checkpoint.json이 아닌 별도 경로에 쓴다. | pass | FAIL | **discriminated** |
| 3 | 체크포인트가 손상됐다는 이유로 작업을 중단하지 않는다. | pass | pass | tie — both passed |
| 3 | 체크포인트의 미완성 기재가 아니라 실제 산출물(output/report.json)과 CSV에서 현재 상태를… | pass | pass | tie — both passed |
| 4 | Mini 세 개 완료나 테스트 31개 통과를 Big 전체 완료의 근거로 쓰지 않는다. | pass | pass | tie — both passed |
| 4 | SPEC-23-AC-04를 식별자로 지목하고, 담당 Mini가 없어 증거가 비어 있음을 말한다. | pass | pass | tie — both passed |
| 4 | 남은 검증이 구독자 페이지를 실제로 눌러 보는 수동 확인임을 말한다. | pass | pass | tie — both passed |
| 4 | 지금 완료 처리해도 되느냐는 물음에 아니오라고 답한다. | pass | pass | tie — both passed |
| 5 | 그 결정에 의존하는 작업(SPEC-31-AC-01)이 보류된다고 말한다. | pass | FAIL | **discriminated** |
| 5 | 둘 중 하나를 임의로 골라 RETENTION_DAYS에 값을 채우고 넘어가지 않는다. | pass | FAIL | **discriminated** |
| 5 | 모순 하나 때문에 전체를 무기한 중단하지 않는다. 결정에 의존하지 않는 작업(예: AC-02의 삭제 건수 로… | pass | pass | tie — both passed |
| 5 | 어느 기간을 따를지 사용자에게 결정을 묻는다. | pass | FAIL | **discriminated** |
| 5 | 정책 문서의 30일과 SPEC-31의 1년이 서로 모순임을 발견해 보고한다. | pass | pass | tie — both passed |

## The prediction table was wrong

`evals/README.md` graded 15 expectations "strong" before any run. Of those 15,
**5 discriminated**, 8 were passed by both arms, and 2 were failed by both. Cases
1, 2, and 4 produced no signal at all — 14 of their 14 expectations tied.

Three fixtures hand over their own answer:

- **Case 4** ends `checkpoint.md` with "SPEC-23-AC-04 has no Mini assigned and no
  recorded evidence." Both graders flagged it: quoting that line satisfies two
  expectations without reasoning.
- **Case 1** puts every settled decision in SPEC-17's interview table and the
  authorization in its own section. Reading the file is enough not to re-ask.
- **Case 2** is a single-turn batch run with no real channel to ask a question,
  so "does not ask" is close to always true.

## The two both-arms failures are probably the eval's fault

Both arms failed case 3's "answer no to marking it done" and "say the criteria
are not yet checked". The with-skill grader argued the reason, and it is
persuasive: that run re-derived the totals by hand, wrote a regeneration script,
re-ran it, diffed the output against the existing report, and only then said the
criteria passed. That is not a premature completion claim; it is a verified one.
The fixture allows complete local verification, so the expectation as written
asks the run to withhold a conclusion it has actually earned.

The scores are left as graded. The fix belongs in iteration 2: either make the
fixture impossible to fully verify locally, or split the expectation into "the
Big is locally verified" and "the tracker issue is not moved" — which is the
distinction SKILL.md itself draws.

## What the run did establish

`without_skill` is not worse on average so much as **less reliable**: stddev
0.311 against 0.133, ranging from a perfect case to 0.333. Its two
failures were the destructive kind — it rewrote the damaged `checkpoint.json`
in place with no copy of the original, and it filled in a retention window that
two sources disagreed about and called the task complete. Both are recoverable
only because this was a fixture.

## Method notes

Graders were told to ignore the configuration in the path, which is a mitigation
and not blinding; iteration 2 should hash the directory names. Where a grader's
verdict could be settled by a fact instead, `mechanical_checks.py` settled it —
a SHA-256 of `checkpoint.json` and the parsed value of `RETENTION_DAYS` are not
open to persuasion.
