# Mini Painless Spec: retry helper for the upload step

- ID: MINI-04
- Revision: 1
- Status: Accepted
- Big: SPEC-22, revision 2

## Task scenario

The upload step fails intermittently on a timeout. Wrap it so a failed attempt
is retried with a growing delay, and give up after the third attempt.

## Delegation

Owner note, 2026-09-04: "Internal naming, private helper structure, and the
delay arithmetic are yours. I care about the retry count and that the last
error surfaces. Don't ask me what to call things."

## Acceptance criteria

| ID | Observable outcome | Verification method |
|---|---|---|
| MINI-04-AC-01 | At most three attempts are made | Unit test with a always-failing stub |
| MINI-04-AC-02 | The final exception reaches the caller | Unit test asserts the raised error |
