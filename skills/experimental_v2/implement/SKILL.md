---
name: implement
description: Implement established requirements in verified increments, maintaining resumable per-feature progress and implementation guidance across sessions when a specification or ticket set governs the work.
disable-model-invocation: true
---

# Implement

Implement an approved specification, ticket set, or well-established user request. A separate specification or ticket set is **not required** for small, clear changes. Follow root `CLAUDE.md` for decision authority and consultation.

For implementation governed by a persisted specification or ticket set, maintain **one feature-level implementation workspace** that allows another session to resume without reconstructing the conversation. For a small, ad hoc change without such an artifact, do not create tracking files unless continuity is useful or requested.

## 1. Establish the implementation boundary

Before editing production code:

1. Identify the governing specification, ticket set, or established request; approved decisions; explicit exclusions; and consequential open questions.
2. Read applicable repository guidance, `CONTEXT-MAP.md` and relevant `CONTEXT.md` (otherwise root `CONTEXT.md`), and applicable root/context ADRs.
3. Inspect relevant code, callers, tests, state owners, and lifecycle to identify the smallest coherent implementation consistent with established responsibilities.
4. Inspect `git status` and repository branch conventions. Do not overwrite unrelated changes or switch branches if doing so could endanger user work.
5. Establish the implementation's Git review base from a verified commit **before the first implementation change**. If resuming, use the original base recorded in the progress file; do not replace it with the latest `HEAD`. If the recorded base is invalid or the branch/scope has materially changed, investigate and clarify the review boundary rather than guessing.

Investigate discoverable facts independently. If a material product or architectural choice is unresolved, consult the user before acting on that choice; continue independent authorized work when possible.

## 2. Locate or create feature-level implementation state

Use repository-relative paths. Create **one workspace per feature**, not one per session or ticket:

```text
docs/
├── specs/
│   └── 014-external-communication.md
├── implementation/
│   └── 014-external-communication/
│       ├── todo.md
│       └── guidance.md       # optional; only when useful
└── tickets/
    └── external-communication/
        └── issues/          # optional ticket decomposition
```

- **With a specification:** use `docs/implementation/<spec-file-stem>/`, preserving the specification's exact basename without `.md` (for example, `014-external-communication`).
- **With tickets but no specification:** use `docs/implementation/<ticket-feature-slug>/`, matching the ticket set's parent feature directory. Link to the ticket source inside `todo.md`.
- **With neither:** create `docs/implementation/<task-stub>/` only if the work is explicitly intended to continue across sessions or the user asks for durable progress. Use a stable, noncolliding name and record the governing request.
- If the workspace already exists, **resume it**. Never reset it, overwrite it with a template, or create a second tracker merely because a new session started.

`todo.md` is the **mutable execution-status record**. Create it at the beginning of tracked implementation. `guidance.md` is **optional** and contains only nontrivial, currently useful implementation knowledge for future sessions. Do not generate an empty or boilerplate `guidance.md`.

Neither file replaces the specification, tickets, ADRs, or code as an authority for requirements or architectural decisions. The specification governs behavior; tickets govern approved decomposition and acceptance criteria; `todo.md` governs current execution status; `guidance.md` summarizes verified discoveries and references approved decisions. Both tracking files are **living documents, not append-only journals**.

### `todo.md` example

Adjust sections to the work. A ticketed feature may use one checklist item per ticket with links and only add smaller steps when needed for multi-session continuity. Without tickets, track meaningful end-to-end behavioral increments rather than individual method edits.

```markdown
# External Communication — Implementation Progress

Specification: `docs/specs/014-external-communication.md`
Tickets: `docs/tickets/external-communication/issues/` (if applicable)
Review base: `a1b2c3d` (verified original HEAD, not the latest session HEAD)
Branch: `feature/external-communication` (last verified)

## Work Items

- [x] Serialize outgoing messages — targeted tests passed
- [x] Send messages using the existing session connection — tested
- [ ] Process incoming messages — in progress
- [ ] Handle connection failures and shutdown
- [ ] Run final validation; run `review-code` if warranted

## Current Focus

Implement incoming-message handling using the established session lifecycle.

## Blockers and Open Decisions

- None. (If blocked, state the specific user decision and affected work.)

## Verification

- Passed: `pytest tests/test_messages.py` (at last verification)
- Not yet run: complete test suite; determine whether `review-code` is warranted at completion
- Known failures: none observed
```

Only record a command as passed if it actually passed. Include relevant environment or commit context when a result would otherwise be misleading. Mark an item `[x]` only when the result is present and adequately verified; if uncertain, leave it open and explain the uncertainty.

### `guidance.md` example

Create this file only when there are discoveries a new session would otherwise need to rediscover. Keep entries concise and actionable.

```markdown
# External Communication — Implementation Guidance

## Where to Look

- `src/session.py` — owns connection state and application lifecycle
- `tests/test_session.py` — existing shutdown and connection test patterns

## Established Decisions

- Connection ownership stays in Session.
  Authority: `docs/specs/014-external-communication.md` (Technical Decisions).

## Verified Discoveries

- Session shutdown cancels pending reads before releasing the connection.
  Evidence: `src/session.py` shutdown path and existing shutdown test.
- The external client supports asynchronous reads.
  Evidence: client API usage in `src/service_client.py`.

## Implementation Caveats

- Preserve shutdown ordering when adding the receive path.

## Open Questions or Proposals

- None. (If present, label as unapproved and link to the blocker in `todo.md`.)
```

A code observation is evidence, **not** permission to change an approved ownership model. An unapproved idea must be labeled as a proposal or open question, never recorded as an established decision. Once an architectural choice is approved, update its authoritative specification/ADR or domain record as appropriate, then adjust the guidance reference. Do not turn `guidance.md` into an alternate ADR store.

## 3. Resume from repository evidence, not notes alone

At the start of **every resumed session**:

1. Read the governing specification and/or tickets, `todo.md`, `guidance.md` if present, and applicable ADRs.
2. Inspect the current branch, Git history/status, relevant source, and tests. Check any changed or completed items against actual code and available validation evidence.
3. Reconcile discrepancies: update stale checklist status, branch information, blockers, and verification notes. A checked box or previous agent's statement is not proof that code or tests are correct.
4. Select the next **unblocked, authorized** behavioral increment. If ticketed, respect genuine ticket dependencies without copying ticket acceptance criteria into the tracker.

Do not discard existing state merely because it looks outdated; verify before correcting it. Preserve unrelated user modifications. If the source of truth and tracking notes disagree, defer to verified repository state and approved requirements, document the discrepancy concisely, and consult only if it raises a consequential decision.

## 4. Implement within the agreed design

Prefer extending existing owners and code paths to introducing managers, services, interfaces, dependencies, layers, or migrations. Prefer cohesive changes over pass-through indirection. Avoid speculative extensibility, extra configuration, and unrelated refactoring.

If evidence reveals a concrete reason the agreed design cannot support the required behavior, explain the problem and compare the smallest correction within existing ownership with any broader alternative. Seek the user's approval before making a consequential change under `CLAUDE.md`. Testing inconvenience or familiarity with a design pattern alone does not justify a new abstraction.

Routine local choices (helpers, naming, ordinary assertions) are yours to make. Do not repeatedly request approval for details already covered by established decisions.

## 5. Test-first development

Use focused red-green cycles for new or changed observable behavior when a reliable test surface exists. The governing specification's verification strategy or already-approved test boundary remains valid; **do not request approval per test**.

### Choose useful test boundaries

- Prefer stable or public interfaces through which callers observe behavior.
- Exercise actual project-owned components together where practical; mock or fake genuine external boundaries (network, time, randomness, expensive infrastructure) as needed.
- Avoid testing private implementation or mocking project-owned internals merely for convenience.
- Derive expected results independently from the specification, known examples, or manually worked cases.
- If meaningful testing requires a consequential change in public contracts or responsibility ownership, consult the user first.

### Deliver one behavioral increment at a time

1. Write one targeted test for the observable behavior.
2. Run it and confirm it fails for the intended missing or incorrect behavior.
3. Make the smallest coherent production change across the layers needed to pass.
4. Rerun the test and verify it passes.
5. Simplify the affected implementation when useful; rerun relevant checks.
6. **Update `todo.md` after the completed increment**, including trustworthy verification results. Update `guidance.md` only if a useful new discovery changes how later work should proceed.

Work in behavioral slices rather than implementation-layer batches. Fix invalid red states (environment, fixtures, syntax) before counting them as a failing behavioral test. If a new test already passes, determine whether the feature already exists or the test is inadequate; do not manufacture changes.

For configuration, documentation, certain UI work, production-only faults, or tasks with no practical automated test, choose appropriate verification (characterization/regression tests, static checks, manual reproduction, diff inspection). Disclose relevant coverage limitations; do not fabricate red-green history or add disproportionate test infrastructure.

## 6. Maintain concise, accurate state

Update `todo.md` **after meaningful verified progress, when blockers change, and before ending a session**. Do not require an update after every command or code edit. Keep the next actionable item, unresolved approvals, and validation status easy to find.

Update `guidance.md` only when valuable for the remaining work. **Edit or remove stale statements** when implementation changes; delete obsolete proposals, resolved gotchas, duplicate explanations, and session-by-session narrative. Retain pointers to sources rather than copying specifications, tickets, or ADRs. If the file contains no lasting useful guidance, it can be removed.

Never silently turn an assumption into a requirement or decision in either file. Keep unresolved user choices visible and do not proceed through blocked work. Track pre-existing failures distinctly from new failures when evidence permits.

## 7. Final validation, review, and completion

At meaningful checkpoints, run targeted formatting, linting, static checks, and tests as applicable. **Do not run the full suite or `review-code` as a mandatory end-of-session ritual while work remains unfinished.**

When all required behavior is implemented:

1. Run relevant static checks and targeted tests; run the full test suite once where available and feasible for substantial implementations. For small, low-risk changes, use proportionate checks and explain any skipped or unavailable validation.
2. Inspect the complete diff for missed requirements, scope creep, unnecessary abstraction, duplicated ownership, and regressions. Simplify within scope.
3. **Run `review-code`** for substantial implementations, consequential changes (including changed architectural ownership, public contracts, persistence, security, or broad cross-component behavior), or when the user explicitly requests it. Supply the **original recorded review base**, governing spec/tickets when applicable, and the complete relevant scope, including in-scope uncommitted files. Follow repository/user commit conventions without forcing a commit solely for review.
4. **For small, low-risk changes**, a separate `review-code` invocation is optional. Inspect the diff yourself, run relevant checks, and report their results. Do not skip review merely because a change has few lines if its consequences are material.
5. Address supported in-scope findings, rerun affected checks, and re-review material corrections when necessary. Consult before a new architectural or product decision.
6. Mark final validation complete only for checks actually performed. In `todo.md` and the final status, state whether `review-code` ran or was intentionally skipped as disproportionate; do not claim completion with unexplained failures.

At session end, whether complete or not, provide a concise status: completed increments, tests/checks, the feature's `todo.md` path, useful `guidance.md` path if present, blockers, and next authorized step. For unfinished work, the next session should be able to resume primarily from the spec, `todo.md`, `guidance.md` if present, and repository state; a separate `handoff` is optional, not required.
