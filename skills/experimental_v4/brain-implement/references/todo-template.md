# Execution record template

This file is **only** the mutable implementation history for one feature, stored at `.brain/features/<feature-slug>/execution.md`. Technical designs remain in `04-implementation-plans/` and executable definitions in `05-tasks/`. Do not copy, overwrite, or combine approved plans into this file.

```markdown
# <Feature> — Execution

Governing plans: `04-implementation-plans/<plan>.md`
Tasks: `05-tasks/` (when applicable)
Review base: <verified full HEAD SHA immediately before first code edit>
Branch: <verified branch>
Collaboration mode: collaborative
Workspace: main checkout
Execution mode: inline
Implementation workflow: brain-implement | brain-pair-program (when used)
Pair mode: AI-led | developer-led | Learning Mode (only with brain-pair-program)

## Work Items
- [ ] TASK-001 — pending
- [ ] TASK-002 — blocked by TASK-001

## Current Focus
<next actionable increment>

## Blockers and Open Decisions
- None.

## Design Deviations
- None. (Do not edit an approved technical plan to reflect implementation.)

## Rulings
- **<YYYY-MM-DD> · <actor> · <work-ID>:** Decision: <exact ruling>; scope: <constraint/exception>; basis: <source or rationale>; risk: <if known>.

## Deferred
- <item deliberately outside current scope>

## Review Focus
- RF1: <applicable failure not already covered> — tested in TASK-001

## Verification
- Passed: <command, date/revision, observed output> (one entry per actual run; do not merge distinct evidence)
- Not run: <checks and why>
- Known failures: <scope and observed evidence>
- Final review: <actual review method and outcome>

## Checkpoints
- TASK-001: verified, awaiting user review (or approved, with date/context)
```

## Rules

- Follow `${CLAUDE_SKILL_DIR}/../brain-init/references/compact-writing.md` for concise facts, stable references and complete execution evidence; never collapse distinct rulings, test runs, approvals or checkpoints.
- With `brain-pair-program`, record the explicitly selected pair mode and any dated, user-approved switch; only the user edits application source/tests in developer-led or Learning Mode. Both implementation skills append to the same history and preserve pending reviews.
- Retain the original review base, branch, collaboration mode, workspace, and execution mode across sessions; reconcile stale facts from Git and actual code, not historical text alone.
- Do not mark a task `[x]` until relevant evidence is observed and, in collaborative/guided mode, the user approved the increment. Verification without approval remains pending review.
- Record command outcomes only when actually executed. Preserve existing user changes, worktree history, blockers, deviations and checkpoints.
- Use meaningful testable behavior increments. For unticketed/direct implementations, work items may refer to verified behaviors instead of task IDs.
- A changed binding implementation plan requires renewed approval before affected work continues; execution history remains intact.
