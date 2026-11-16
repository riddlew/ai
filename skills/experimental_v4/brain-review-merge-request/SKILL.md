---
name: brain-review-merge-request
description: Review a GitLab merge request, GitHub pull request, or local branch against user-supplied Jira acceptance criteria and current repository evidence, producing findings and an advisory approve/request-changes recommendation. Read-only.
disable-model-invocation: true
---

# Review Merge Request

Review a specific PR/MR or local branch **read-only**. Do not edit code, push, comment, approve, request changes or alter the hosting service's state.

## Workflow

1. Resolve the actual target/source revisions and Git comparison base, head SHA, changes and PR/MR context. Never assume `@{upstream}` is the target. Include uncommitted files only if scope explicitly requires them.
2. Read applicable requirements, source, approvals and review history. Treat CI and review comments as **evidence**, not independent proof or authority.
3. Inspect correctness, intended behavior, security/repository fit and regressions across changed code plus the necessary callers/tests. Verify concerns against current head and mark stale/review-resolved comments accordingly.
4. Report evidence-based findings with severity, locations and `Merge blocking: Yes | No` rationale. Distinguish open questions from supported defects. If none, say `No material issues found within the reviewed scope and available evidence.` Never claim comprehensive safety.
5. Deliver in the conversation. Save a durable report only when requested or needed at `.brain/reviews/merge-request/<NN>-<short-slug>/review.md`, using `${CLAUDE_SKILL_DIR}/../brain-review-code/references/report-storage.md` and the deterministic `doc new --kind review --report-type merge-request` scaffold.

**Read when needed:** `${CLAUDE_SKILL_DIR}/references/mr-review-details.md` for remote CI/review thread evidence, specialized subreviews, local temporary worktree cleanup, coverage and complete report structure. A temporary worktree must be cleaned up; reviewed files remain unchanged.
