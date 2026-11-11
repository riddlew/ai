---
name: brain-review-merge-request
description: Review a GitLab merge request, GitHub pull request, or local branch against user-supplied Jira acceptance criteria and current repository evidence, producing findings and an advisory approve/request-changes recommendation. Read-only.
disable-model-invocation: true
---

# Review Merge Request

**Project brain:** Follow `CLAUDE.local.md` §Project brain loading: read **all** root `.md` files once per session (again after compaction), plus the active branch's pending file when present. Inspect linked detail and verify task-critical facts against current source. Do not send the whole brain to subagents. If no brain exists, proceed and mention `/brain-init` once.

Produce one advisory assessment of the **current proposed change**. The analysis comes from `brain-review-code`; this skill owns the inputs, acceptance-criteria coverage, merge-specific checks, and the recommendation. Follow `CLAUDE.local.md`.

## Read-only

Do not edit project code or documentation, commit, push, post comments, change merge-request state, or approve or request changes on the hosting platform. The recommendation is advisory.

Deeper verification may use a disposable checkout or isolated temporary worktree; never change reviewed files. A temporary worktree changes Git administrative state until removed: clean it up safely after review and verify it is gone, or do not create it if cleanup is uncertain. Before executing code from an untrusted contribution, assess its side effects and exposure to credentials, networks, and production resources. Do not run destructive operations, intrusive security tests, or commands against production without separate explicit authorization. Never expose secrets in findings.

## 1. Inputs

Identify:

- the GitLab MR or GitHub PR URL/number, or the local source branch;
- the **user-supplied Jira story and acceptance criteria**, the primary requirement source;
- whether this is a **full review** (default) or a **re-review**.

If the user said they would provide a Jira story but did not, ask for it before concluding on requirement compliance, and continue other work meanwhile. If the user says no story applies, proceed without inventing acceptance criteria.

Requirement sources, highest first:

1. Jira story and acceptance criteria supplied by the user.
2. MR/PR description and linked issues.
3. Referenced specifications, approved ADRs, `.brain` root files, and repository rules.
4. Existing observable behavior, tests, interfaces, and documented contracts.

Lower sources add context but do not override higher ones. If sources conflict materially, describe the conflict and ask the user which requirement is intended; continue independent review work meanwhile. Meeting the listed criteria does not prove the change correct.

## 2. Resolve the change set

**Remote MR/PR:** use `gh`, `glab`, or an approved integration to obtain the source and target refs, head SHA, changed files and patches, description, linked issues, CI results, and review threads. Do not assume the target is `main` or `master`. Verify that a local checkout matches the head SHA before using it as evidence; otherwise fetch the correct revision or rely on the remote change set and state the limits.

**Local branch:** use a base the user gives; otherwise unambiguous repository evidence; otherwise ask. Never treat the upstream tracking branch as the target. Include uncommitted work only when the user requests it, and identify it separately.

Report any material ambiguity in the comparison range before analyzing. A review of the wrong revision is not a valid review.

## 3. Analyze

Invoke `brain-review-code` with:

- **Base:** the merge base with the verified MR/PR target (or the resolved local base). This satisfies `brain-review-code`'s base rule.
- **Requirements:** the Jira acceptance criteria and the secondary sources above.

Then add the merge-specific checks `brain-review-code` does not cover:

- **Tests:** whether meaningful behaviors and failure cases are verified; false confidence from mocks or assertions against internals.
- **Performance:** realistic hot paths touched by the change (query or allocation complexity, blocking operations), supported by usage evidence, measurement, or clear complexity analysis.

Add a specialist only when it materially improves confidence:

- `brain-review-security` when the change crosses an authentication, authorization, credential, or sensitive-data boundary, or a credible issue needs attacker-path validation.
- `brain-review-architecture` (focused review) when an ownership, dependency, or structural concern needs more than diff-level analysis.

Give each specialist a bounded scope, the requirements, and concrete evidence. Keep their output in the conversation.

Classify every candidate:

- **Introduced or materially worsened by the change** — eligible as a finding.
- **Pre-existing and unchanged** — omit, except serious defects or vulnerabilities flagged separately.
- **Unverified concern** — investigate if possible; otherwise report as a question, never as a defect.

Consolidate: re-check each finding against the current head, drop disproven findings, and merge duplicates across `brain-review-code` and specialists.

## 4. CI and prior review

Treat CI results and review threads as evidence, not substitutes for independent assessment. Check whether reported issues remain at the current head; do not repeat resolved concerns. Distinguish failed, skipped, pending, and unavailable checks, and determine whether failures are attributable to this change. A passing test does not prove absence of defects; a failing test does not by itself establish a change-introduced defect.

## 5. Re-review

When requested, obtain the previous review's head SHA and findings. Classify each prior finding as **resolved**, **partially resolved**, **unresolved**, or **no longer applicable**; review the new changes for regressions; recheck acceptance criteria, CI, and security-sensitive paths. If the previous head or findings are unavailable, say so and perform a full review.

The recommendation reflects the complete current change, not just the newest patch. Force pushes, target changes, or changed requirements may warrant a full review.

## 6. Report

Format findings per `${CLAUDE_SKILL_DIR}/../brain-review-code/references/findings.md`, in descending severity, with:

- **Category:** Correctness | Requirements | Architecture | Maintainability | Security | Tests | Performance
- **Location** at the current head SHA, preferably on changed lines. For a problem outside changed lines, explain how the change exposes or worsens it.
- An added field, **Merge blocking:** Yes | No — with a short rationale. Critical and High are normally blocking; Medium blocks when its impact is meaningful and the evidence sufficient; Low normally does not. Do not block on unverified speculation, polish, or unrelated pre-existing issues.

Conclude with:

1. **Requirements coverage:** each Jira acceptance criterion as met / unmet / unverifiable, with brief evidence; note consequential secondary requirements.
2. **Verification:** tests, checks, and CI status actually observed, including failures and gaps.
3. **Pre-existing serious concerns / open questions:** only when applicable.
4. **Recommendation: Approve** or **Recommendation: Request changes**, reasoned from blocking findings and unresolved risk. If critical evidence is missing, say why the recommendation is provisional and what would resolve it.

If no material findings are supported, state: **No material issues found within the reviewed scope and available evidence.** Do not claim the change is bug-free, secure, or fully verified.
