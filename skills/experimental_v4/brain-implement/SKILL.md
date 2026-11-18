---
name: brain-implement
description: Implement approved requirements and code-level design in verified, test-first increments, using collaborative review checkpoints by default and resumable per-feature progress when needed.
---

# Implement

Implement approved requirements within the agreed architecture. Small settled changes can proceed directly; substantial or design-sensitive work needs an approved blueprint. Honor `CLAUDE.local.md` for decisions, context loading and write scope.

## Collaboration and design boundary

**Automatic skill invocation is not authorization to modify code.** Begin implementation only when the user explicitly requests implementation. Approval of a specification, blueprint, or task list does not independently authorize implementation. Preserve all existing design-approval and collaborative review checkpoints.

**Collaborative is the default**, inline execution. For substantial work, obtain explicit approval of the binding `brain-design-implementation` before editing; after **each verified, coherent increment**, show the diff and verification and **wait for user approval**. **Guided** reviews larger increments; **autonomous** skips routine checkpoints only when the user opts in. No mode waives approval for an unresolved consequential change. Subagent-driven is a separate opt-in execution mode; use `${CLAUDE_SKILL_DIR}/references/subagent-driven.md` and keep the main coordinator out of production edits.

## 1. Establish the boundary

1. Read the project core, active feature's specifications, approved implementation plans, tasks, ADRs and technical source knowledge; inspect all relevant code owners, callers, tests and current Git changes. `brain-context` is optional, not a substitute for discovery: when uncertain, **read more**. If no Brain exists, proceed from the request and mention `/brain-init` once.
2. Recheck binding plan assumptions against current source and `Design inspected at:`. If a binding design is stale, stop affected work and return to `brain-design-implementation` for revision/approval; independent authorized work may proceed.
3. Note `git status`; preserve unrelated edits. Record the **true review base before the first code change** and preserve it on resume (do not substitute the design SHA or latest HEAD). Reconcile any recorded base that no longer represents the actual work.
4. Resolve the previously chosen workspace and collaboration/execution modes without re-asking. Worktrees use a shared Brain: **do not copy brain documents into it**. Verify new worktrees against committed/uncommitted work and user authorization; never silently discard uncommitted or untracked dependencies, auto-merge, or remove worktrees.

## 2. Track execution progress separately from design

For feature tasks or multi-session work, use `.brain/features/<feature-slug>/execution.md`, **not** `04-implementation-plans/`, for checkpoints, review base, verification, blockers, rulings and deviations. Read existing history and preserve approvals. Scaffold a missing record with `brain-tool doc new --kind execution` and append verified events with `record`; preview writes and pass the real authorized scope. Do not mark a task complete from a checkbox or successful scaffold.

If that write is denied or outside the session's authorized boundaries, follow `CLAUDE.local.md` §Worktrees and brain writes. Never route around a restriction. For new/changed tracked work items, review task/plan coverage using `${CLAUDE_SKILL_DIR}/references/impl-plan-review.md`. On resume, inspect the actual diff and any user changes **since the last reviewed checkpoint** before editing.

## 3. Implement and verify

1. Choose the next unblocked requirement/example and smallest coherent behavior slice; do not introduce speculative owners, layers or dependencies.
2. When observable testing is feasible: write a spec-derived test, verify a meaningful **red** result, make the smallest change, verify **green**, and rerun affected checks. If it already passes, investigate; don't manufacture failure. When tests are impractical, use proportionate observable evidence and disclose limits.
3. Review the actual diff, requirements and approved binding design; inspect command results. Technically verified is **not** the same as approved or done. Maintain verification evidence in execution records.
4. In collaborative/guided mode, present the relevant diff, covered acceptance cases and actual test results, request approval and **wait**; a `continue` response approves only the previously reviewed increment. If the user edited files, preserve/reverify them before proceeding.
5. For consequential design deviations, stop the affected scope and consult/return to `brain-design-implementation`. Minor reversible illustrative adjustments may proceed and be reported.

Commit only upon explicit user instruction; stage only authorized files. For subagent task review and detailed test/review modes, read `${CLAUDE_SKILL_DIR}/references/implement-details.md` **when that mode or situation arises**.

## 4. Finish

Run proportionate final checks and inspect the **full diff**. Substantial or consequential work, or requested review, gets `brain-review-code` including in-scope uncommitted files and recorded Review Focus; small changes get a disclosed self-review. Address significant findings and honor any outstanding user checkpoint. Record evidence and limitations, invoke `brain-update` once when project knowledge changed, and report changed files, verification, approvals, rulings/deferred items and blockers. Never claim completion with unresolved critical failures.

**Detailed exceptions:** `${CLAUDE_SKILL_DIR}/references/implement-details.md` covers worktree creation, paused/resumed runs, subagent review packets, failed-test diagnosis, final independent review and fix-pass mechanics. The CLI contract is `${CLAUDE_SKILL_DIR}/../brain-init/references/deterministic-tooling.md`.

**Recommended next step:** End the final user-facing reply with one concise, evidence-based next action, naming the appropriate skill or command when useful. If blocked, identify the missing information, prerequisite, or approval instead of advancing; if complete, say no further action is needed. A recommendation is not authorization to execute another step. Keep it outside copy-ready deliverables.
