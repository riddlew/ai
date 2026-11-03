# Lens: Failure

Use when a decision affects what happens when operations fail, time out, partially complete, run concurrently, or repeat.

## Decisions that typically arise

- Failure semantics per failure type: fail fast, retry, degrade, defer to later, or surface to the user.
- Retry policy: which errors are retryable, limits and backoff, and whether the operation is safe to repeat.
- Partial failure in multi-step operations: roll back, compensate, or leave a resumable intermediate state.
- Timeouts and cancellation: budgets per call, cancellation propagation, cleanup on cancel.
- Concurrency control: locking, optimistic versioning, single writer, or last write wins; ordering guarantees.
- Shutdown and restart: handling in-flight work, draining, recovering incomplete operations.
- Visibility: what is logged, alerted, or shown to the user when a failure occurs.

## Evidence to gather

- Existing error-handling and retry utilities; timeouts configured on HTTP, database, and queue clients.
- Which external calls are idempotent according to their documentation; existing idempotency keys.
- Transaction boundaries, and where side effects (email, payments, external calls) happen relative to commits.
- Actual concurrency: multiple workers or instances, async tasks, multiple tabs or clients.
- Shutdown hooks, signal handling, and current treatment of in-flight work.
- Incident history, bug reports, or tests that encode past failure behavior.

## Questions that surface decisions

- If this step succeeds and the next fails, what state is left behind, and is that acceptable?
- Is it safe to run this twice? What if two run at once?
- How long may the user wait before the operation gives up, and what do they see then?
- When a dependency is down, should this feature fail, degrade, or defer?
- Which failures need a human to notice them?

## False dichotomies

- "Retry everything" vs. "never retry": retry only failures known to be transient, on operations safe to repeat.
- "Distributed transaction" vs. "accept inconsistency": an outbox, side effects after commit, or compensation often suffices.
- "Global lock" vs. "no concurrency control": optimistic versioning on the contested record is often enough.
- "Handle every failure" vs. "ignore failures": decide per failure class by likelihood and consequence.
