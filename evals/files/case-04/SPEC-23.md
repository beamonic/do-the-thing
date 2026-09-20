# Big Painless Spec: subscriber export

- ID: SPEC-23
- Revision: 1
- Status: Accepted

## User story and scenario

An operator clicks Export on the subscribers page, waits, and downloads a CSV
that opens cleanly in Excel with the columns in the agreed order.

## Acceptance criteria

| ID | Observable outcome | Verification method | Responsible Minis |
|---|---|---|---|
| SPEC-23-AC-01 | The export endpoint returns a CSV for a valid request | Unit test | MINI-01 |
| SPEC-23-AC-02 | Columns appear in the agreed order | Unit test | MINI-02 |
| SPEC-23-AC-03 | Non-ASCII names survive the round trip into Excel | Unit test | MINI-03 |
| SPEC-23-AC-04 | Clicking Export on the subscribers page downloads that file | **Manual walk of the page** | none — integration |
