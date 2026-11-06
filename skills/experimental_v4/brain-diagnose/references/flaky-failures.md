# Flaky and Suite-Only Failures

Use this for failures that depend on timing, or that appear only when other tests run first. First establish how often it fails and under what conditions; a failure you cannot repeat cannot be confirmed fixed.

## Condition-based waiting

If a test or script waits with a fixed sleep or delay, the failure is often a race: the wait is sometimes too short. Replace the guess with a check of the actual condition.

- Poll for the condition you need (a file exists, a status changes, an event arrives) at a short interval, such as every 10 ms.
- Set a timeout and fail with a clear message naming what was awaited, so a hang becomes a diagnosable error.
- Read fresh state on every poll; do not cache the value outside the loop.
- A fixed delay is correct only when the test is about timing itself, such as a debounce or an interval. Then wait for the triggering condition first, base the delay on a known duration, and add a comment explaining why.

Changing waiting behavior in production code, rather than in a test, may alter timing semantics. Consult the user first.

## Finding a polluting test

When a test passes alone but fails in the full suite, another test is leaving behind state: a file, an environment variable, a global, a database row, a registered handler.

1. Confirm the failure: run the full suite, and note the order.
2. List the candidate tests that run before it.
3. Split the candidates in half. Run the first half followed by the failing test, using your test runner's file or name selection and its option to preserve order.
4. If the failing test fails, the polluter is in that half. Otherwise it is in the other half. Repeat until one candidate remains.
5. Run that single candidate and then the failing test to confirm. Then inspect what the candidate leaves behind.

If the runner randomizes order, fix the seed first so the result is repeatable.

Fix the pollution at its source, usually by having the polluting test clean up after itself, not by reordering tests.
