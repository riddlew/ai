# `todo.md` Template

`todo.md` is the mutable execution-status record for one feature. Adjust sections to the work.

- **Ticketed feature:** one checklist item per ticket, with links; add smaller steps only when needed for multi-session continuity. Do not copy ticket acceptance criteria.
- **Without tickets:** track meaningful end-to-end behavioral increments, not individual method edits.

```markdown
# External Communication — Implementation Progress

Specification: `docs/specs/014-external-communication.md`
Tickets: `docs/tickets/external-communication/issues/` (if applicable)
Review base: `a1b2c3d` (verified original HEAD, not the latest session HEAD)
Branch: `feature/external-communication` (last verified)

## Work Items

- [x] Serialize outgoing messages (E1–E3) — targeted tests passed
- [x] Send messages using the existing session connection (E4) — tested
- [ ] Process incoming messages (E5–E7) — in progress
- [ ] Handle connection failures and shutdown (E8–E9)
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

## Rules

- Record a command as passed only if it actually passed. Include environment or commit context when a result would otherwise mislead.
- Mark an item `[x]` only when the result is present and verified; if uncertain, leave it open and say why.
- Keep the next actionable item, unresolved approvals, and validation status easy to find.
- Track pre-existing failures separately from new failures when evidence permits.
