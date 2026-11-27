---
name: brain-implement
description: Implement requested changes with or without a Brain spec, plan, tasks or prior brainstorming; verify proportionately without routine approvals.
---

# Implement

**A direct explicit user request is sufficient authorization to implement within its established scope.** No spec, plan, task list, approved blueprint, previous brainstorm, `brain-update` or execution record is required. Use the ongoing brainstorming conversation, a concise decision record, optional handoff, or existing feature docs when available.

1. Locate the task and relevant Brain index/decisions/amendments (if present). Inspect current Git state, actual code owners, callers, tests and applicable source contracts. Use targeted context, expanding when dependencies or contradictions emerge; never treat a handoff as proof of current source.
2. Resolve consequential undecided behavior or architecture with the user. For routine reversible details, choose an appropriate implementation and proceed. Plans and specs are optional aids, not gates. Do not ask for mode: **inline is default; subagents require explicit request**.
3. Implement small coherent increments, respecting existing worktrees and user edits. Use test-first when useful, run risk-proportionate focused checks, inspect actual diffs; do not require approval between increments, a separate code-review invocation or a user confirmation to proceed. High-risk security, persistence, protocol, concurrency and compatibility changes merit deeper checks.
4. A material newly established change to a documented design may be recorded as a focused amendment with explicit `amends`/`supersedes`; do not rewrite whole original specs or require a document for minor adjustments. Conflicting authoritative decisions require consultation; no latest-document-wins shortcut.
5. Diagnose a failure before changing code again; use new evidence and different diagnostic approaches, not repeated equivalent retries. Protect modified/untracked files and explicit write boundaries. Create a compact optional `execution.md` for multi-session work; `handoff.md` only when useful. No redundant approvals or copied normative decisions.
6. Stop when requested behavior is implemented, relevant verification completed or limitations disclosed, and no material blocker remains. Do not continue with unrequested refactors, tests, docs or reviews. Only stage/commit if explicitly instructed.

Never call `brain-update` automatically. Final answer: changed files, executed verification and unresolved issues. Read `references/implement-details.md` only for specialized tests, delegated implementation or complex resume.
