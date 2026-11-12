# Impl plan review

Runs before the first **code** change, when execution work items are first created or structurally revised: work items added, split, or merged from new or changed Examples, tickets, or requirements. It also runs when `brain-implement` adds execution tracking to a plan that `brain-blueprint` already created. Never on a plain resume, a status update, fix-pass items, `Ruling:` entries, or Deferred entries. A successful blueprint review does **not** substitute for work-item coverage review.

## Order for a new plan

Do not ask the startup questions first. In this order:

1. **Reuse the existing plan and approved blueprint** when one exists, appending execution sections from `todo-template.md` without overwriting `## Implementation Design`; otherwise create the plan from the template. Set the collaboration mode to the user's prior choice or `collaborative` by default.
2. Run the self-check below, including `## Review Focus`, against the approved spec, tickets, and any blueprint constraints.
3. Run the builder review below.
4. Record the default `Workspace: main checkout` and `Execution mode: inline` unless the user requested a different arrangement or it materially matters; in that case ask the relevant workspace/execution questions **together** with any questions only the user can answer. There is no routine startup questionnaire.

A plan created before worktree selection may lack `Workspace:` or `Execution mode:` until step 4; this is expected.

If the user picks a worktree and `.brain` is tracked, transfer the **entire** existing uncommitted impl plan (including its approved blueprint and its execution sections) into the worktree's `.brain/impl_plans/` without dropping data or clobbering a different file; reconcile any existing destination. Record the startup answers there.

## Self-check

- Every governing Example, acceptance criterion, or numbered requirement (`R<n>`, for a plan tracking a request) maps to a work item; the work-item sequence respects approved blueprint constraints and exposes meaningful independently verifiable increments.
- Names match the spec and tickets.
- `## Review Focus` lists the failure cases the governing requirements imply but no Example or criterion covers. Each line takes one of two forms:
  - `RF<n>: <case> — tested in <work item>`, per §5's rule to test failure paths the Examples don't cover;
  - when no approved requirement determines the outcome, `RF<n>: <case> — blocked: <decision needed>`. List it under Blockers and Open Decisions too. Never invent its behavior.

## Builder review

Follow `${CLAUDE_SKILL_DIR}/../brain-review-code/references/builder-review.md`, with `impl plan` as `{artifact_kind}`.

- `{artifact}` is the absolute path of the impl plan file.
- `{sources}` is the spec and tickets plus any approved `## Implementation Design`, or the governing request recorded in the plan when neither exists.
- Questions only the user can answer join the startup-question message. Unanswered ones become Blockers.
- When the user answers a blocked RF's decision, record it where `CLAUDE.local.md` says (the governing spec or `09_user_decisions.md`), rewrite the line as `RF<n>: <case> — tested in <work item>`, and remove it from Blockers.
