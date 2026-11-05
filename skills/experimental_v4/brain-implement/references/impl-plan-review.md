# Impl plan review

Runs before the first change, when a plan is created or structurally revised: work items added, split, or merged from new or changed Examples, tickets, or requirements. Never on a plain resume, a status update, fix-pass items, `Ruling:` entries, or Deferred entries.

## Order for a new plan

Do not ask the startup questions first. In this order:

1. Create the plan from `todo-template.md`.
2. Run the self-check below, including `## Review Focus`.
3. Run the builder review below.
4. Only then send ONE message: the startup questions (SKILL.md §1 step 6) plus any questions only the user can answer. Record the startup answers in the plan header.

Until step 4, the plan exists with no `Workspace:` or `Execution mode:` recorded. That is expected.

If the user picks a worktree and `.brain` is tracked, move the new, uncommitted plan into the worktree's `.brain/impl_plans/` so it isn't left in the main checkout. Record the startup answers there.

## Self-check

- Every governing Example, acceptance criterion, or numbered requirement (`R<n>`, for a plan tracking a request) maps to a work item.
- Names match the spec and tickets.
- `## Review Focus` lists the failure cases the governing requirements imply but no Example or criterion covers. Each line takes one of two forms:
  - `RF<n>: <case> — tested in <work item>`, per §5's rule to test failure paths the Examples don't cover;
  - when no approved requirement determines the outcome, `RF<n>: <case> — blocked: <decision needed>`. List it under Blockers and Open Decisions too. Never invent its behavior.

## Builder review

Follow `${CLAUDE_SKILL_DIR}/../brain-review-code/references/builder-review.md`, with `impl plan` as `{artifact_kind}`.

- `{artifact}` is the absolute path of the impl plan file.
- `{sources}` is the spec and tickets, or the governing request recorded in the plan when neither exists.
- Questions only the user can answer join the startup-question message. Unanswered ones become Blockers.
- When the user answers a blocked RF's decision, record it where root `CLAUDE.md` says (the governing spec or `09_user_decisions.md`), rewrite the line as `RF<n>: <case> — tested in <work item>`, and remove it from Blockers.
