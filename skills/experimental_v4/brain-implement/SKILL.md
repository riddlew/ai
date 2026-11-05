---
name: brain-implement
description: Implement established requirements in verified, test-first increments, maintaining resumable per-feature progress when a specification or ticket set governs the work.
disable-model-invocation: true
---

# Implement

**Project brain:** If `.brain/00_index.md` exists (at this worktree's root, or in the main checkout when working in a linked git worktree) and you have not read its root files in this session (or they were lost to context compaction), read every root `.md` file in that `.brain/` now. Read subfolders only when a root file links to them or the task needs them. Do not load `.brain` into subagents wholesale; pass only what their task needs. Write any `.brain/` document into that same `.brain/`. If no brain exists, proceed without one and mention once that `/brain-update` can create it.

Implement an approved specification, ticket set, or well-established request. Small, clear changes need no specification. Follow root `CLAUDE.md` for decision authority and consultation.

## 1. Establish the boundary

Before editing production code:

1. Identify the governing specification, tickets, or request; approved decisions; exclusions; and open consequential questions.
2. Read repository guidance and applicable ADRs in `.brain/adrs/`.
3. Inspect the relevant code, callers, tests, state owners, and lifecycle. Identify the smallest coherent implementation within existing responsibilities.
4. Check `git status` and branch conventions. Do not overwrite unrelated changes or switch branches if that could endanger user work.
5. Record the review base: a verified commit taken **before the first change**. When resuming, use the base recorded in the impl plan, never the latest `HEAD`. If the recorded base is invalid or the branch or scope has materially changed, investigate and clarify instead of guessing.
6. **Startup questions** (before the first change, every run). If the impl plan header records `Workspace:` and `Execution mode:`, use them without asking. Otherwise ask both in one message:
   - **Worktree:** work in a git worktree for this feature? Default: no.
   - **Execution mode:** subagent-driven or inline? Recommend subagent-driven for several tasks with few shared interfaces; inline for one or two tasks, tightly coupled tasks, or untracked work.

   Record the answers in the impl plan header when one exists (untracked work asks every run). If worktree: create it from the current HEAD so unpushed work is included: `git worktree add <repo root>/.claude/worktrees/<feature-slug> -b <feature-slug> HEAD`. Ensure `.claude/worktrees/` is listed in `info/exclude` under `git rev-parse --git-common-dir`. Work inside it (in Claude Code, `EnterWorktree` with that path when available). An untracked `.brain` is still found in the main checkout. Never merge or remove the worktree; at the end, report its path and branch.

**Mode switch.**
- **Subagent-driven:** follow `${CLAUDE_SKILL_DIR}/references/subagent-driven.md` for each task. The main session coordinates and does not edit code.
- **Inline:** implement each task yourself per §4–§5. There is no task reviewer.
- **Both modes:** proof before done, the commit pause, and §7.

If a consequential choice is unresolved, consult before acting on it and continue independent authorized work meanwhile.

## 2. Track progress for governed work

Track progress when a persisted specification or ticket set governs the work, or when the user asks for multi-session continuity. Otherwise create no tracking files.

Use one impl plan per feature, never one per session or ticket:

- **With a specification:** `.brain/impl_plans/<spec-file-stem>.md` (for example, `014-external-communication.md`).
- **With tickets only:** `.brain/impl_plans/<ticket-feature-slug>.md`, linking the ticket source.
- **With neither:** `.brain/impl_plans/<task-stub>.md`, only when continuity is requested; record the governing request.

If the impl plan exists, resume it. Never reset it, overwrite it with a template, or create a second tracker. Create it when tracked work begins, following `${CLAUDE_SKILL_DIR}/references/todo-template.md`.

The impl plan is the execution-status record: a living document, not a log, and not an authority. The specification governs behavior, tickets govern decomposition and acceptance criteria, and ADRs govern architecture. Discoveries a future session would otherwise rediscover go into the `.brain` root files through `brain-update`, not into the impl plan.

## 3. Resume from evidence, not notes

At the start of every resumed session:

1. Read the specification or tickets, the impl plan, and applicable ADRs.
2. Inspect the branch, Git history and status, relevant source, and tests. Check completed items against actual code and validation evidence; a checked box is not proof.
3. Reconcile: correct stale status, branch information, blockers, and verification notes, and note discrepancies concisely. Defer to verified repository state and approved requirements; consult only if a discrepancy raises a consequential decision.
4. Select the next unblocked, authorized behavioral increment, respecting genuine ticket dependencies.

## 4. Implement within the agreed design

Extend existing owners and code paths before introducing managers, services, interfaces, dependencies, layers, or migrations. Avoid pass-through indirection, speculative extensibility, extra configuration, and unrelated refactoring.

If the agreed design cannot support a requirement, explain the concrete problem and compare the smallest correction within existing ownership with any broader alternative before making a consequential change. Testing inconvenience or familiarity with a pattern does not justify a new abstraction.

## 5. Test-first increments

Use red-green cycles for new or changed observable behavior when a reliable test surface exists. Do not request approval per test.

**Start from the specification's Examples.** Each Example is a candidate first test. Then add tests for the stated invariants and failure paths the Examples do not cover; examples are not exhaustive.

Choose test boundaries:

- Prefer stable or public interfaces through which callers observe behavior.
- Exercise real project-owned components together where practical; fake genuine external boundaries (network, time, randomness, expensive infrastructure).
- Do not test private implementation or mock project-owned internals for convenience.
- Derive expected results independently from the specification, its Examples, or manually worked cases, never from the implementation's current output.
- If meaningful testing requires a consequential change to public contracts or ownership, consult first.

For each increment:

1. Write one targeted test for the observable behavior.
2. Run it and confirm it fails for the intended reason. Fix invalid red states (environment, fixtures, syntax) before counting it.
3. If it already passes, investigate whether the behavior already exists or the test is inadequate. Do not force a failing test or manufacture changes.
4. Make the smallest coherent production change across the layers needed.
5. Rerun the test and confirm it passes. Simplify the affected code where useful and rerun relevant checks.
6. **Proof before done.** A task is done only when, in this session: (a) its tests ran and passed and you read the output; (b) each Example or acceptance criterion it covers was compared against real output; (c) a self-review of the task diff passed (in scope, no unrelated edits, no debug leftovers, consistent with the spec); (d) the impl plan (when tracked) records the test command and result. "Should pass" is not evidence. If tests cannot run, the task stays open with the reason recorded; never check it off.

Work in behavioral slices, not layer batches. Where no practical automated test exists (configuration, documentation, some UI, production-only faults), use characterization tests, static checks, manual reproduction, or diff inspection, and disclose coverage limits. Never fabricate red-green history.

### Commit pause

After each task, and after the final fix pass if it changed anything: report the task, the test command and its result, propose a Conventional Commits message (e.g. `fix(parser): reject empty input lines`), ask the user to commit, and wait. Never run `git commit` yourself. Once the user confirms, check HEAD moved and record the sha in the impl plan. The next task starts only after the commit; if the user says to continue without committing, do so and note that the next task's review covers both tasks' changes.

## 6. Keep state accurate

Update the impl plan after verified progress, when blockers change, and before ending a session, not after every edit. Keep unresolved user choices visible and do not proceed through blocked work.

Before ending a session, record its state in the impl plan. Then invoke `brain-update` with a one-line summary of what changed.

If `brain-update` already ran in this session and nothing has changed since (no code, tests, impl plan, or user decisions), skip both steps: the impl plan and the brain are already current. The usual case is a session that ends right after the completion step in §7.

## 7. Finish

Do not run the full suite or `brain-review-code` as a ritual while work remains.

When all required behavior is implemented:

1. Run relevant static checks and targeted tests. For substantial work, run the full suite once where feasible. For small, low-risk changes, use proportionate checks and say what was skipped.
2. Inspect the complete diff for missed requirements, scope creep, unnecessary abstraction, duplicated ownership, and regressions. Simplify within scope.
3. Judge by what the diff changes, not by how the defect arose. Small, low-risk changes need only your own diff inspection and checks; substantial or consequential changes (ownership, public contracts, persistence, security, broad cross-component behavior, or a small diff with material consequences), or any change when requested, get a full review covering the full scope including in-scope uncommitted files: dispatch a fresh strongest-tier subagent that runs `brain-review-code` inline, given the impl plan's `Review base`, the governing spec or tickets, and the impl plan's Rulings and Deferred lists. If no subagent tool is available, run `brain-review-code` yourself and report `Final review: self-review (no fresh reviewer) — weaker than an independent review`. Critical, High, and Medium findings enter one fix pass (each fix test-first, then the full suite, then the commit pause); list Low findings for the user. No second review pass.
4. Address in-scope findings by applying `${CLAUDE_SKILL_DIR}/references/review-feedback.md`, rerun affected checks, and consult before any new consequential decision.
5. Report, and record in the impl plan, only checks actually performed and whether `brain-review-code` ran or was skipped as disproportionate. Do not claim completion with unexplained failures.

When the work is complete, record it in the impl plan. Then invoke `brain-update` with a one-line summary of what changed.

At session end, give a concise status: completed increments, checks run and their results, coverage summary, every `Ruling:` line, deferred findings, the impl plan path if present, the worktree path and branch if one was used, blockers, and the next authorized step.
