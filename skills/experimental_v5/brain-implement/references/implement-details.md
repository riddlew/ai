# Implementation details (v5)

## Objective, scope and context

Implement the explicit user's requested behavior; brainstorming decisions and code can provide scope without formal specs, plans or tasks. If present, read applicable authoritative requirements, focused amendments, technical contracts and concise handoff/optional execution state. Verify current Git changes and actual source. Recheck uncertain or stale assumptions against code; load more relevant files when needed.

## Execution

Default inline, no execution-mode question. Subagents require explicit opt-in. Protect unrelated staged, unstaged, untracked and worktree changes. Never silently merge, drop dependencies or commit. For a multi-session feature, optional `execution.md` records review base, objective, completed/remaining work, tests, active amendments and blockers, not every conversational step.

Choose meaningful coherent behavior slices rather than arbitrary layer order. Write failing tests first when useful; if a test already passes, investigate rather than manufacture a red state. Implement minimal code under existing ownership, test appropriate normal/edge/failure and unchanged behavior, inspect actual diff. High-risk security, protocol, persistence, concurrency and backwards compatibility require deeper checks.

No mandatory user checkpoint after each increment and no default final specialist-review skill. Ask only for genuinely unresolved consequential choices. Routine internal design details may be selected and implemented. A significant newly settled design change may be recorded as a focused plan/spec amendment; no wholesale reapproval of original documents. Without a plan, a focused durable record is optional.

## Failures

Investigate actual symptoms, logs, test outputs and causes before retrying. Do not repeat essentially identical failing tests or speculative edits without new evidence; change the diagnostic approach. If blocked, report completed work and the specific evidence or decision needed.

## Completion

Stop when the requested behavior is implemented, meaningful tests/verification completed (or limitations disclosed), and no material blocker remains. Inspect final diff for scope and regressions. Do not automatically refactor, create unrelated tests/docs, add abstractions, invoke `brain-update`, run expensive blanket reviews or stage/commit. Final response: changed files, actual verification, unresolved issues. Use `references/subagent-driven.md` only when opted into delegated work.
