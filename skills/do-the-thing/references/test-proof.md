# Test proof inside Do the Thing

Use for writing meaningful tests or investigating missing coverage, flaky tests, or a defect that escaped a passing suite. Skip mutation work for a routine rerun or a trivial wording change. Diagnosing coverage alone does not authorize fixing production code.

Read actual tests and the code path before declaring a gap. Tests may live under another component's filename. Prioritize failure behavior, authorization boundaries, repeat/irreversible transitions, and integration responsibilities. Reuse the repository's existing test files and framework, with real objects or isolated local storage when safe; stub only the external boundary that cannot safely run.

For a changed guard or behavior under test:

1. Run an unmodified baseline and record command, revision, collected/executed count, and result. Zero tests or a broken baseline establishes nothing.
2. In an isolated disposable copy with no production credentials or live side effects, disable or alter one relevant guard/behavior at a time. Do not mutate the user's working tree or shared runtime.
3. Run the relevant tests. Require a failure attributable to that behavioral change; syntax/import failure, missing dependencies, and zero tests are not proof that the assertion catches the defect. If a storage constraint catches it instead, record that actual defense rather than claiming the intended assertion did.
4. Reset only the disposable copy between cases. Check that the original is unchanged, rerun the normal checks, and report killed/surviving/invalid mutations separately. A survivor calls for investigation, not automatic success.

Bound the experiment to the requested behavior. If safe isolation or execution is unavailable, report test proof pending; do not weaken gates or run destructive live experiments. Distinguish partial runs from the complete repo-required checks. Review and mutation evidence do not replace whole-Big verification.

For flaky tests, record failures/attempts and the observed failure separately for isolated and suite runs. A successful retry does not erase the failure; do not stress shared resources without scope and isolation.

This package's original adaptation of `test-and-prove` preserves failure-sensitivity checks while separating invalid mutations from useful behavioral evidence.
