# 네이티브 질문 터미널 실검증 — 2026-09-14

대상: PR #22 / `9819929`의 설치된 인터뷰 계약. 같은 계약을 읽도록 명시한 합성 테스트다. 자동 스킬 발견이나 전체 Linear 업무 흐름 검증은 아니다. 제품 결정 대신 검증자가 PTY 입력으로 답했다.

| 환경 | 설정 | 관측 결과 |
|---|---|---|
| Codex CLI 0.153.4 | 기존 인증 프로필, gpt-6-astra medium, read-only, `/plan` | request_user_input 2회, 선택값과 Other 메모 수신, 최종 receipt 일치 |
| Claude Code 2.1.263 | 기존 OAuth, Opus 5 xhigh, plan, Read/AskUserQuestion만 제공, MCP 제외 | AskUserQuestion 3회, 선택 수신, 자유 입력 첫 실패 감지 후 재질의 성공 |
| Codex 데스크톱 | 현재 대화 Default | 이번 blocking 입력·사이드바 라벨은 미검증. 앞선 async 응답 수신과 혼동하지 않는다 |

## 실제 왕복

- Codex Q-TEST-1: `Blue (Recommended)` 선택. 답변 전 Q-TEST-2 호출이 없었고, 실제 반환 후 다음 질문이 나타났다.
- Codex Q-TEST-2: None of the above 선택 → Tab 메모 → `terminal-freeform-20260914` → Enter. 반환은 선택값과 `user_note`를 모두 포함했고 최종 TEST_RECEIPT와 일치했다.
- Claude Q-TEST-1: `파랑` 선택. 반환 후 다음 질문으로 이동했다.
- Claude Q-TEST-2 첫 시도: 텍스트와 Enter를 한 번의 PTY 쓰기로 보냈을 때 `__other__`만 반환됐다. 본문 손실 원인은 이 실행만으로 단정하지 않는다. 모델은 답변으로 확정하지 않고 재질문했다.
- 재시도: Type something으로 이동 → 텍스트만 전송 → 입력 표시 확인 → 별도 Enter. `terminal-freeform-20260914`가 반환되고 최종 `TEST_RECEIPT: 색상=파랑; 메모=terminal-freeform-20260914`를 확인했다.

## 실행 조건과 한계

첫 Codex 실행은 TERM=dumb이라 시작을 거부했다. PTY에 TERM=xterm-256color를 지정하고 재실행했다. 저장소 신뢰를 확인했으며 Codex의 미검토 hook은 실행하지 않는 선택으로 진행했다. 이 조건은 모든 사용자 설정을 그대로 실행한 검사와 다르다. 검증용 프로세스만 종료했으며 기존 작업은 건드리지 않았다.

두 터미널의 네이티브 질문 호출·응답 대기·선택·자유 입력·다음 질문 전환은 관측했다. Claude 자유 입력은 첫 시도 실패와 재시도 성공을 함께 보존한다. 데스크톱의 선택하지 않은 작업에 표시되는 답변 요청 라벨은 별도 실검증 대상이다. 현재 대화에서는 blocking 도구가 Plan 모드 전용이므로 호출하지 않았다.

O’Reilly는 같은 대화의 `Building Applications with AI Agents` 검색 메타데이터를 재사용했다. 본문을 읽지 않았고 동작 증거로 사용하지 않았다. 로컬 context에는 codex 패키지가 없어, 앞서 읽은 공식 도구 계약·CLI 도움말·실제 도구 호출 및 응답을 근거로 삼았다.
