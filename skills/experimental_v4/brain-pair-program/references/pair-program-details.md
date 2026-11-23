# Pair programming — pacing, review and continuity

Use this when implementation modes or checkpoint behavior need more detail. **Do not replace** shared Brain approval, authority, documentation ownership or inline/subagent rules. The two choices are independent:

| Choice | Modes | Controls |
|---|---|---|
| Pair programming | **AI-led (recommended)** or **developer-led** | Who edits production code/tests |
| Execution | **Inline (recommended)** or **subagents** | Who carries out Claude's research/review |

Ask for any missing choice at the beginning (both can be asked in one message), wait, and record the selection. In developer-led Claude may read code, propose snippets, inspect actual diffs, and perform authorized non-editing checks; it must not write application code, tests or database migrations. Updating the authorized `execution.md` record is permitted. Explicitly confirm a switch before Claude takes over edits; subagents do not change authorship or waive review checkpoints.

## Dependency-aware Spring Boot example

Assume `Order`, `OrderStatus`, `OrderRepository`, `OrderService` and `OrderController` already exist. **Inspect those first**, along with approved order-cancellation behavior, concurrency expectations and existing exception handling. An illustration is **not** permission to invent cancellation eligibility, HTTP status or lock strategy.

**Overview:** Show the planned responsibility and request flow, concrete class structure, and missing dependencies. Explain why a cancellation service is warranted by actual complexity, not hypothetical future patterns.

**Possible sequence (adapt to repository and approved plan):**

1. **Prerequisites:** Check existing entity and repository contracts. Introduce missing `OrderNotFoundException`, `OrderCannotBeCancelledException` and any agreed status eligibility behavior **before** the service calls them. Verify the slice, pause for review.
2. **Service:** Explain the outline, constructor injection and cancellation orchestration, then present a coherent implementation and focused unit tests. Explain transactions, idempotency, `@Transactional`, and JPA dirty checking rather than calling `save()` unnecessarily. Verify, review and wait.
3. **Concurrency:** If approved, establish version field, schema migration, other-writer compatibility and transaction-conflict tests before claiming optimistic locking works. `@Transactional` alone cannot prevent lost updates. Changing persistence or HTTP 409 policy needs explicit design approval.
4. **HTTP:** Prefer an existing central exception handler over another competing one. Add a controller endpoint only when its service contract exists; verify response codes. Pause at coherent boundaries.
5. **Integration:** Verify persistence, rollback, endpoint errors and conflicting updates. Use the production database engine/Testcontainers where necessary, and distinguish executed tests from proposed coverage.

A test-first red stage is normal **during** an increment; finish with a buildable, verified boundary (or mark blocked) before treating it as complete. A conceptual overview may name future types, but **ready-to-paste code cannot depend on missing types** at a checkpoint. Group connected dependencies rather than inventing one-method-per-turn bureaucracy.

## Shared checkpoint dialogue

**Start:** `Next: add the two exceptions that the cancellation service will use. They're domain exceptions, not HTTP handlers. Verify compilation and the related failure-path tests.`

**Developer-led:** Give file path and relevant code, then explain decisions without walking through trivial lines. Ask user to implement. When they say "done", inspect real files and the actual diff; don't assume the snippet was copied. Verify the observed behavior and show `verified, awaiting review`. Ask for approval or revisions; **stop**.

**AI-led:** Explain the same increment, edit only that increment, show actual diff and executed checks, then ask `Approve, request changes, or challenge the approach?` **Stop**. A response of "continue" approves only that checkpoint.

**Feedback:** Prefer small local corrections to unrelated refactors. If a suggested change contradicts the approved spec, ADR or binding plan, explain the impact and return to owning producer for renewed approval; do not silently update approvals or `parent_hashes`. No new code on affected scope until approved.

## Reuse existing execution history

Use `.brain/features/<feature-slug>/execution.md` and `brain-implement/references/todo-template.md`, not `pair-progress.md` or another checklist. Retain original `Review base`, branch/workspace, collaboration and execution modes, approvals, verification and decisions. For a feature record, optional fields can distinguish the implementation workflow without changing the template contract:

```markdown
Implementation workflow: brain-pair-program
Pair mode: developer-led
Execution mode: inline

## Checkpoints
- INC-2 · developer-led: user wrote service; observed compilation at <revision>, awaiting user review
- INC-2: user approved on <date>; next dependency: HTTP adapter
```

If switching modes, log actor, date and scope; don't retroactively relabel earlier source authors. If switching between `brain-implement` and `brain-pair-program`, inspect the **same** pending checkpoint and real changes before resuming. Never reset review base or mark unapproved work done. Use the shared `brain-tool doc new --kind execution` / `record` operations when authorized; don't bypass workspace restrictions. After owner changes, use `brain-update` for durable knowledge, **not** to reapprove feature docs.

## Verification and handoff

- For AI-led, tests may follow test-first red/green; do not fabricate a red result where a test already passes.
- For developer-led, source review and tests may reveal deviations; discuss the user's actual implementation rather than overwrite it.
- Verification alone is not user acceptance. Show the evidence and wait after every incremental change regardless of mode.
- For final review, follow proportionate `brain-review-code` rules and the confirmed inline/subagent selection. Committing requires separate explicit authorization.
