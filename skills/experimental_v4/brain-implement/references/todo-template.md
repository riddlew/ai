# Impl Plan Template

The impl plan (`.brain/impl_plans/<feature>.md`) is **one file per feature**: a blueprint's `## Implementation Design` and approval metadata, when present, plus mutable execution tracking. `brain-blueprint` owns the design section and blueprint metadata; `brain-implement` adds or changes execution sections **without replacing the blueprint**. Adjust sections to the work.

- **Ticketed feature:** one checklist item per ticket, with links; add smaller steps only when needed for multi-session continuity. Do not copy ticket acceptance criteria.
- **Without tickets:** track meaningful end-to-end behavioral increments, not individual method edits.

```markdown
# External Communication — Implementation Progress

Specification: `.brain/specs/014-external-communication.md`
Tickets: `.brain/tickets/external-communication/` (if applicable)
Blueprint status: approved (or `not required — <reason>` for a small direct change)
Blueprint approval: user confirmed <YYYY-MM-DD> (if approved)
Design inspected at: <full HEAD SHA> (if blueprint exists; not `Review base`)
Review base: `a1b2c3d` (verified original HEAD immediately before code edits)
Branch: `feature/external-communication` (last verified)
Collaboration mode: collaborative (default; or `guided`, `autonomous`)
Workspace: main checkout (or `worktree .claude/worktrees/<slug> (branch <slug>)`)
Execution mode: inline (default for collaborative; or `subagent-driven`)

## Implementation Design

<Preserve verbatim if brain-blueprint already wrote this section; omit for a small direct change.>

## Work Items

- [x] Serialize outgoing messages (E1–E3) — base `a1b2c3d`, commit `d4e5f6a` — targeted tests passed
- [x] Send messages using the existing session connection (E4) — base `d4e5f6a`, commit `9f8e7d6` — tested
- [ ] Process incoming messages (E5–E7) — verified, awaiting user review (collaborative/guided), or in progress
- [ ] Handle connection failures and shutdown (E8–E9)
- [ ] Run final validation; run `brain-review-code` if warranted

## Current Focus

Implement incoming-message handling using the established session lifecycle.

## Design Deviations

- None. (Record meaningful differences from illustrative sketches or user-approved deviations here; do not silently alter binding blueprint constraints.)

## Blockers and Open Decisions

- None. (If blocked, state the specific user decision and affected work.)

## Rulings

Format: `Ruling: <decision> — <why> — <cost if wrong>`

- Ruling: reuse the session connection for sends — avoids a second lifecycle owner — cost if wrong: rework E4

## Deferred

- E6 retry backoff tuning — out of scope for this feature

## Review Focus

- RF1: peer closes the connection mid-message → partial message is discarded and logged — tested in "Handle connection failures and shutdown"
- RF2: <case> — blocked: <decision needed> (also under Blockers and Open Decisions)

## Verification

- Passed: `pytest tests/test_messages.py` (at last verification)
- Not yet run: complete test suite; determine whether `brain-review-code` is warranted at completion
- Known failures: none observed
- Final review: fresh strongest-tier reviewer — 4/4 met, 0 findings (or `own diff inspection (small, low-risk change)`)
```

## Rules

- Record `Collaboration mode: collaborative` by default, independent of `Execution mode: inline`. Read recorded values on resume instead of asking again. Switch only when the user directs it.
- When a blueprint already exists, **append execution headers and sections**; never regenerate the file or replace the `Implementation Design`. The blueprint's `Design inspected at` is not the implementation's `Review base`.
- `Blueprint status: draft` or `needs revision` blocks dependent code edits; `approved` requires explicit user consent, while `not required` needs a documented small/direct-work justification.
- Record a command as passed only if it actually passed. Include environment or commit context when a result would otherwise mislead; when automated tests are inapplicable, record the actual alternative verification and its limits.
- Mark an item `[x]` only when the result is present and verified **and**, in collaborative/guided mode, the user has reviewed and approved the increment. Until then leave `[ ]` with `verified, awaiting user review`. If uncertain, leave it open and say why.
- Keep the next actionable item, unresolved approvals, and validation status easy to find.
- Track pre-existing failures separately from new failures when evidence permits.
- Review Focus lists failure cases no Example covers. It is filled in at creation and reviewed by the final review.
