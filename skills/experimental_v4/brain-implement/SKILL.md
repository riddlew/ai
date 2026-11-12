---
name: brain-implement
description: Implement approved requirements and code-level design in verified, test-first increments, using collaborative review checkpoints by default and resumable per-feature progress when needed.
disable-model-invocation: true
---

# Implement

**Project brain:** Follow `CLAUDE.local.md` §Project brain loading: read **all** root `.md` files once per session (again after compaction), plus the active branch's pending file when present. Inspect linked detail and verify task-critical facts against current source. Do not send the whole brain to subagents. If no brain exists, proceed and mention `/brain-init` once.

Implement an approved specification, ticket set, or well-established request **without silently changing the user's intended code structure**. Small, clear changes need no specification or separate blueprint. Follow `CLAUDE.local.md` for decision authority and consultation.

## Collaboration modes and blueprint gate

**Collaboration mode defaults to `collaborative`** unless the user or the existing impl plan selected another mode. It is independent from `Execution mode` (inline or subagent-driven):

- **Collaborative (default):** for substantial or design-sensitive work, require an explicitly approved `/brain-blueprint` first; discuss key signatures, ownership, pseudocode and patterns as needed. Implement a **small coherent testable behavior** and pause after presenting its diff, verification evidence, and design deviations. Resume only when the user approves or directs revisions. Default execution: **inline**, preserving design discussion in the same session.
- **Guided:** require the approved blueprint for substantial or design-sensitive work, but discuss fewer method-level details. Present and pause after each **larger coherent functional increment**. Default execution: inline; subagent-driven is an option after the design is settled.
- **Autonomous:** implement the approved requirements and applicable blueprint with no routine per-increment approval pause. Verify each increment and give a final diff and checks. The user may opt into subagent-driven execution. Unresolved consequential decisions **still require consultation**.

A blueprint is normally expected for a substantial feature, cross-component change, or task where the user has expressed preferences about architectural or method-level design. If absent, **handoff to `/brain-blueprint` before editing code**; this skill does not silently write or approve a blueprint itself. If the user explicitly requests direct implementation of a small, settled change, or an existing approved spec and user direction clearly make a blueprint unnecessary, record `Blueprint status: not required — <reason>` in tracked work and proceed. Never infer approval from a drafted file, an approved spec, or a prior feature request. If a blueprint is `draft` or `needs revision`, do not implement the blocked scope until its design is approved. Explicitly changing the collaboration mode or bypassing a nonessential blueprint does not authorize an unresolved consequential redesign.

## 1. Establish the boundary

Before editing production code:

1. Identify the governing specification, tickets, request, and **approved blueprint when present**; binding user design preferences, exclusions, and open consequential questions. Resolve the collaboration mode from the plan or explicit user instruction, otherwise `collaborative`.
2. Read repository guidance and applicable ADRs in `.brain/adrs/`.
3. Inspect relevant code, callers, tests, state owners, and lifecycle. Revalidate the blueprint's `Design inspected at:` assumptions against current code, staged/unstaged edits, and branch-specific changes. Do not treat the design SHA as a review base. If a **binding** blueprint design no longer fits, stop the affected work, explain what changed, and return to `/brain-blueprint` for revision and approval; independently authorized work may proceed.
4. Check `git status` and branch conventions. Do not overwrite unrelated changes or switch branches if that could endanger user work.
5. Record the review base: a verified commit taken **before the first change**. When resuming, use the base recorded in the impl plan, never the latest `HEAD`. If the recorded base is invalid or the branch or scope has materially changed, investigate and reconcile it from Git and the approved scope; consult only if the correct base cannot be established without a consequential choice.
6. **Workspace and execution mode** (before the first code change; for a newly created or expanded tracked plan, run §2 review first). Use existing `Workspace:`, `Execution mode:`, and `Collaboration mode:` values when set; do not re-ask. For a small untracked task, default to the current checkout, inline execution, and collaborative mode. For a new tracked plan, record `Collaboration mode: collaborative` by default and recommend **inline** execution in collaborative mode. Ask about a worktree (default: no) or subagent-driven execution **only if requested or the choice would materially improve execution**; otherwise record `Workspace: main checkout` and `Execution mode: inline`. If user preferences require a meaningful choice, ask the relevant questions together, not as a ritual.

   For a worktree, Claude Code isolation means a session can read but cannot edit the main checkout. If the brain is untracked (`Git: ignored`) inside the main repository, warn that the impl plan cannot be updated there from an isolated worktree; recommend moving the brain outside and `/brain-init <path>` first. `HEAD` includes **committed** local work, including unpushed commits, but **not** uncommitted edits or untracked files. Before creating a worktree identify any such work needed by the feature and agree how to preserve/access it; never silently proceed without those changes. Verify the destination and branch name are unused, then create from current HEAD with `git worktree add <repo root>/.claude/worktrees/<feature-slug> -b <feature-slug> HEAD`. Ensure `.claude/worktrees/` is listed once in `info/exclude` under `git rev-parse --git-common-dir`. Work inside it (in Claude Code, `EnterWorktree` where available). Don't create the worktree while an untracked brain is still inside this repository; never merge or remove the worktree automatically. Preserve and transfer the **entire existing impl plan including approved blueprint**, not only its execution checklist. Report path and branch at the end.

**Execution mode switch.**
- **Subagent-driven:** follow `${CLAUDE_SKILL_DIR}/references/subagent-driven.md` for each task. The main session coordinates and does not edit code. In collaborative/guided mode, it must return control for user review **after each task**, not dispatch the next one immediately.
- **Inline:** implement each task yourself per §4–§5. There is no task reviewer.
- **Both modes:** proof before done, the collaboration checkpoint where required, optional commits, and §7. Subagent execution is not a substitute for user design approval.

If a consequential choice is unresolved, consult before acting on it and continue independent authorized work meanwhile.

## 2. Track progress for governed work

Track progress when a persisted specification, ticket set, **or blueprint** governs the work, or when the user asks for multi-session continuity. Otherwise create no tracking files.

Use one impl plan per feature, never one per session or ticket:

- **With a specification:** `.brain/impl_plans/<spec-file-stem>.md` (for example, `014-external-communication.md`).
- **With tickets only:** `.brain/impl_plans/<ticket-feature-slug>.md`, linking the ticket source.
- **With neither:** `.brain/impl_plans/<task-stub>.md`, only when continuity is requested; record the governing request.

If the impl plan exists, **reuse it**. It may already contain an approved `## Implementation Design` written by `brain-blueprint` without execution tasks. Never reset it, overwrite it with a template, duplicate the blueprint, or create a second tracker. Add missing execution headers, work items and verification sections following `${CLAUDE_SKILL_DIR}/references/todo-template.md`; **preserve** blueprint status, approval, design details, and existing progress. If none exists and tracking is warranted, create it from the template. When execution tasks are first created or structurally revised, follow `${CLAUDE_SKILL_DIR}/references/impl-plan-review.md` before the first code change; the blueprint builder review does **not** replace this coverage review.

The impl plan is an execution-status record **and optional approved code-level blueprint**, not an independent authority. The specification governs behavior, tickets govern decomposition and acceptance criteria, and ADRs and durable recorded decisions govern architecture. `brain-blueprint` owns the `Implementation Design` section and its approval metadata; `brain-implement` owns execution tracking, including a separate `## Design Deviations` section; it does not rewrite the blueprint to match code or silently change binding design. Discoveries a future session would otherwise rediscover go into `.brain` root files through `brain-update`, not into the progress checklist.

## 3. Resume from evidence, not notes

At the start of every resumed session:

1. Read the specification or tickets, the **approved blueprint** (if any) in the impl plan, and applicable ADRs.
2. Inspect branch, Git history and status, relevant code, and tests. Check completed items against code and observed verification; a checked box is not proof. **Compare the current diff and relevant file contents against the last reviewed checkpoint before touching code:** the user may have edited code between sessions or increments.
3. Reconcile stale status, branch information, design assumptions, blockers, and verification notes. Preserve user edits and rerun affected verification before building on them. If source changes invalidate a binding blueprint constraint, return to `brain-blueprint`; do not silently repair the blueprint to match code.
4. Select the next unblocked, authorized behavioral increment, respecting real ticket dependencies and the collaboration-mode review boundary.

## 4. Implement within the agreed design

Follow **binding approved implementation constraints** (ownership, patterns, important signatures, negative constraints) in the blueprint and governing decisions. Treat explicitly **illustrative** snippets and suggested private helpers as flexible. Extend existing owners and code paths before introducing managers, services, interfaces, dependencies, layers, or migrations unless an approved design explicitly requires one. Avoid pass-through indirection, speculative extensibility, extra configuration, and unrelated refactoring. Preserve manual user changes, even when they differ from an earlier illustrative sketch; verify their effect rather than overwriting them.

If the agreed design cannot support a requirement, explain the concrete problem and compare the smallest correction within existing ownership with any broader alternative before making a consequential change. Return to `/brain-blueprint` to revise **binding design** and secure approval before implementing the affected scope; change governing specs or ADRs first when required. **Routine, reversible** adjustments to illustrative details can proceed, but identify meaningful deviations at the next review checkpoint. Testing inconvenience or familiarity with a pattern does not justify a new abstraction.

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
   - If a red test fails for a reason other than the missing behavior (not step 2's invalid states), or it still fails after step 4 (failed attempt 1), investigate per `brain-diagnose` §1–§2 before another change; its three-failed-fixes rule applies.
6. **Proof before done.** A task is technically verified only when, in this session: (a) applicable tests or other **meaningful verification** ran and you inspected results; (b) each Example or acceptance criterion it covers was checked against the strongest available evidence (real execution when feasible); (c) a self-review of the task diff passed (in scope, no unrelated edits, no debug leftovers, consistent with the spec **and approved blueprint**); (d) the impl plan (when tracked) records commands, outcomes, and limitations. "Should pass" is not evidence. If essential behavior cannot be verified, the task remains open with the reason recorded. In collaborative or guided mode, **verified but awaiting user review is not approved/done**; do not start the next increment until the user approves it or directs revisions.

Work in behavioral slices, not layer batches. Where no practical automated test exists (configuration, documentation, some UI, production-only faults), use characterization tests, static checks, manual reproduction, or diff inspection, and disclose coverage limits. Never fabricate red-green history or claim a static inspection demonstrated runtime behavior.

### User review and optional commit

After **each verified behavioral increment** in **collaborative** mode, present the concrete changed files and meaningful diff (or focused excerpts with a way to inspect the full diff), covered Examples/criteria, test commands and observed results, what remains unchanged, and **any deviation** from the approved blueprint. Ask the user to approve, request edits, or adjust the next increment; **wait**. In **guided** mode do the same with a concise functional-level review after each larger coherent increment. Do not batch multiple unreviewed increments. Do not interpret silence, a passing test, or blueprint approval as increment approval. If the user edits code before answering or between increments, re-inspect the actual changed files and diff, preserve those edits, and rerun impacted verification; no blind restoration of the previous blueprint. A "continue" reply to the reviewed increment can count as approval of **that increment only**, not future ones.

When the increment is approved and verified, mark its work item done. Suggest a Conventional Commits message (e.g. `fix(parser): reject empty input lines`) **without requiring a commit**. The user may commit, request that you commit, or continue uncommitted. Run `git commit` only upon explicit user instruction; stage only authorized task files, check that `HEAD` moved, and record the SHA when there is one. If no commit is made, record the uncommitted cumulative scope and ensure subsequent reviews distinguish earlier approved work and user edits from new changes. **Autonomous** mode records verified increment status and continues without routine user checkpoints or commits; offer a commit suggestion at the end. Final fix-pass edits in collaborative/guided mode get a corresponding user review before declaring completion.

## 6. Keep state accurate

Update the impl plan after verified progress, when blockers change, and before ending a session, not after every edit. Keep unresolved user choices visible and do not proceed through blocked work.

Before ending a session, record its state in the impl plan. Then invoke `brain-update` with a one-line summary of what changed.

If `brain-update` already ran in this session and nothing has changed since (no code, tests, impl plan, or user decisions), skip both steps: the impl plan and the brain are already current. The usual case is a session that ends right after the completion step in §7.

## 7. Finish

Do not run the full suite or `brain-review-code` as a ritual while work remains.

When all required behavior is implemented **and each collaborative/guided increment has been approved**:

1. Run relevant static checks and targeted tests. For substantial work, run the full suite once where feasible. For small, low-risk changes, use proportionate checks and say what was skipped.
2. Inspect the complete diff for missed requirements, scope creep, unnecessary abstraction, duplicated ownership, and regressions. Simplify within scope.
3. Judge by what the diff changes, not by how the defect arose. Small, low-risk changes need only your own diff inspection and checks; substantial or consequential changes (ownership, public contracts, persistence, security, broad cross-component behavior, or a small diff with material consequences), or any change when requested, get a full review covering the full scope including in-scope uncommitted files: dispatch a fresh strongest-tier subagent that runs `brain-review-code` inline, given the impl plan's `Review base`, the governing spec or tickets, and the impl plan's Rulings, Deferred, and Review Focus lists (one coverage row per Review Focus item). When the final check is your own diff inspection, report one row per RF item: met, unmet, or unverifiable. If no subagent tool is available, run `brain-review-code` yourself and report `Final review: self-review (no fresh reviewer) — weaker than an independent review`. Critical, High, and Medium findings enter one fix pass (each fix test-first, then relevant/full verification, then a user review checkpoint in collaborative/guided mode); list Low findings for the user. No second review pass.
4. Address in-scope findings by applying `${CLAUDE_SKILL_DIR}/references/review-feedback.md`, rerun affected checks, and consult before any new consequential decision.
5. Report, and record in the impl plan, only checks actually performed and whether `brain-review-code` ran or was skipped as disproportionate. Do not claim completion with unexplained failures.

When the work is complete, record it in the impl plan. Then invoke `brain-update` with a one-line summary of what changed.

At session end, give a concise status: collaboration mode, blueprint status, completed and awaiting-review increments, checks run and their results, coverage summary, every `Ruling:` line, deferred findings, the impl plan path if present, the worktree path and branch if one was used, blockers, and the next authorized step.
