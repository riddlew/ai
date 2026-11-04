# Impl Plan Template

The impl plan (`.brain/impl_plans/<feature>.md`) is the mutable execution-status record for one feature. Adjust sections to the work.

- **Ticketed feature:** one checklist item per ticket, with links; add smaller steps only when needed for multi-session continuity. Do not copy ticket acceptance criteria.
- **Without tickets:** track meaningful end-to-end behavioral increments, not individual method edits.

```markdown
# External Communication — Implementation Progress

Specification: `.brain/specs/014-external-communication.md`
Tickets: `.brain/tickets/external-communication/` (if applicable)
Review base: `a1b2c3d` (verified original HEAD, not the latest session HEAD)
Branch: `feature/external-communication` (last verified)
Workspace: main checkout (or `worktree .claude/worktrees/<slug> (branch <slug>)`)
Execution mode: inline (or `subagent-driven`)

## Work Items

- [x] Serialize outgoing messages (E1–E3) — base `a1b2c3d`, commit `d4e5f6a` — targeted tests passed
- [x] Send messages using the existing session connection (E4) — base `d4e5f6a`, commit `9f8e7d6` — tested
- [ ] Process incoming messages (E5–E7) — in progress
- [ ] Handle connection failures and shutdown (E8–E9)
- [ ] Run final validation; run `brain-review-code` if warranted

## Current Focus

Implement incoming-message handling using the established session lifecycle.

## Blockers and Open Decisions

- None. (If blocked, state the specific user decision and affected work.)

## Rulings

Format: `Ruling: <decision> — <why> — <cost if wrong>`

- Ruling: reuse the session connection for sends — avoids a second lifecycle owner — cost if wrong: rework E4

## Deferred

- E6 retry backoff tuning — out of scope for this feature

## Verification

- Passed: `pytest tests/test_messages.py` (at last verification)
- Not yet run: complete test suite; determine whether `brain-review-code` is warranted at completion
- Known failures: none observed
- Final review: fresh strongest-tier reviewer — 4/4 met, 0 findings (or `own diff inspection (small, low-risk change)`)
```

## Rules

- Record `Workspace:` and `Execution mode:` once; a resumed session reads them instead of asking.
- Record a command as passed only if it actually passed. Include environment or commit context when a result would otherwise mislead.
- Mark an item `[x]` only when the result is present and verified; if uncertain, leave it open and say why.
- Keep the next actionable item, unresolved approvals, and validation status easy to find.
- Track pre-existing failures separately from new failures when evidence permits.
