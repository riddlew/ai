# Execution coverage review

This review applies when `brain-implement` first creates or structurally changes the work items in `.brain/features/<feature-slug>/execution.md`, **before production code edits**. It does not run on every resume, status change, or review fix-pass item. An approved blueprint review does not replace this coverage review.

## Order

1. Read governing specifications, approved component plans and tasks, and existing execution history. Preserve any prior execution record and approved plans; never conflate them.
2. Draft work items by task ID or coherent behavior, preserving genuine task dependencies.
3. Verify coverage and `Review Focus` below.
4. Run builder review with the task set and plans as sources; when unavailable, identify weaker self-review.
5. Choose default `Workspace: main checkout`, `Execution mode: inline`, and collaborative review checkpoints unless user preferences or the project environment require otherwise.
6. If working in a separate worktree, carry forward the complete `execution.md` and all referenced approved feature documents without overwriting project-specific changes; preserve `Review base`.

## Coverage check

- Every approved task and applicable requirement/example maps to an actionable work item; unresolved consequential choices block only their affected scope.
- Dependencies are genuine and acyclic; work items remain small, independently verifiable behavioral increments.
- Every uncovered approved failure path appears in `Review Focus` with a concrete test target; if behavior is not decided, identify the blocking question instead of inventing a test result.
- Work-item titles and traceability agree with qualified requirement IDs, approved plan constraints, and the project glossary.
- No plan or task definition is silently changed to align with implementation convenience.
- Keep recorded verification and user approvals across resumes; a completed checkbox is not evidence without code/test verification.
