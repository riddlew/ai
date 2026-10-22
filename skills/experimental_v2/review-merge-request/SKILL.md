---
name: review-merge-request
description: Review a GitLab merge request, GitHub pull request, or local branch against user-supplied Jira acceptance criteria and current repository evidence. Produce actionable findings and a read-only approve/request-changes recommendation.
disable-model-invocation: true
---

# Review Merge Request

Review the **current proposed change**, not the repository in general. Use evidence to evaluate correctness, requirements, architecture, maintainability, security, tests, performance, and regressions. Follow the project's `CLAUDE.md` and approved architectural records when present.

This is a **read-only** review. Do not edit project code or documentation, commit, push, post comments, change merge-request state, approve, or request changes on the hosting platform. The final **Approve** or **Request changes** recommendation is advisory only.

A review finding is not authorization to refactor or resolve a product/architectural decision. Do not propose extra layers or patterns merely because they could be useful later.

## 1. Establish the review inputs

Identify:

- the GitLab merge-request URL/number, GitHub pull-request URL/number, or local source branch;
- the **user-supplied Jira story and acceptance criteria**, which are the primary requirement source;
- the intended target/base branch and source/head revision;
- whether this is a **full review** (default) or a **re-review** of a previous set of findings.

If the user said they would provide a Jira story but did not include it, request it before issuing a requirement-compliance conclusion. Other independent inspection may continue. If the user explicitly establishes that no Jira story applies, proceed using the remaining evidence; do not invent acceptance criteria.

Resolve intended behavior in this order:

1. **Jira story and acceptance criteria supplied by the user.** Treat these as the primary contract for what the change must accomplish.
2. Merge/pull request description and linked issues, including relevant discussion of scope.
3. Referenced specifications, approved ADRs, domain records, and applicable repository rules.
4. Existing observable behavior, tests, interfaces, and documented contracts.

Lower-ranked sources add context; they must not silently override higher-ranked requirements. Existing architectural constraints remain relevant even when they do not restate acceptance criteria. If sources conflict materially, describe the conflict, investigate facts, and consult the user about the intended requirement rather than selecting a product or architectural decision on their behalf. Continue independent review work while that choice is unresolved.

Do not assume that satisfying the listed acceptance criteria proves every aspect of the change correct: also check relevant failure paths, regressions, and existing contracts.

## 2. Resolve the exact change set

### Remote merge/pull request

Use available GitLab/GitHub tooling (for example, `glab`, `gh`, an approved integration, or hosting API) to obtain the canonical source and target refs, current head SHA, changed files and patches, merge/pull request description, linked issues, CI results, and review discussion. Do not assume a branch is named `main` or `master`.

Use the **actual merge-request target** and source head to establish the effective merge-base change set. Check that any local checkout matches the remote head SHA before using local code as evidence. If the local checkout is stale or unrelated, obtain the correct revision or rely on the remote change set, identifying any limits. For a shallow or incomplete checkout, do not silently treat an incorrect base as authoritative.

### Local branch review

Use a base explicitly given by the user. Otherwise infer the intended target from **unambiguous** repository configuration or branch metadata. If multiple targets are plausible, ask rather than guessing. Identify the source HEAD and merge base and inspect the equivalent of:

```bash
git diff <merge-base>..HEAD
git log <merge-base>..HEAD --oneline
```

Include staged, unstaged, or untracked files **only when the user requests review of uncommitted work**; identify that scope separately so it is neither missed nor confused with the merge-request diff.

Before analyzing findings, report any material ambiguity in the comparison range. A review of the wrong revision is not a valid review.

## 3. Build an evidence-based review

Inspect changed code and only the surrounding code needed to understand ownership, callers, state/lifecycle, tests, and contracts. Read applicable `CLAUDE.md`, domain records, ADRs, specification material, and relevant tooling/CI configuration.

Evaluate as applicable:

- **Correctness:** reachable failures, edge cases, concurrency and lifecycle errors, data integrity, and regression paths.
- **Requirement fit:** trace each Jira acceptance criterion and material secondary requirement to observable implementation and tests; identify unsupported changes to product behavior.
- **Architecture and complexity:** changes to responsibility/ownership, needless indirection, new managers/interfaces without concrete need, coupling, or unexplained departures from approved design.
- **Maintainability:** clear boundaries, readable control flow, duplication with real synchronization costs, and consistency with repository conventions.
- **Security:** authorization, trust boundaries, untrusted input, credentials, sensitive-data handling, and plausible exploitation paths.
- **Tests:** whether meaningful behaviors and failure cases are verified; test quality and false confidence from mocks or assertions against internals.
- **Performance:** realistic hot paths, allocation/query complexity, blocking operations, and regressions supported by usage evidence, measurement, or clear complexity analysis.

These are lenses for investigation, **not quotas for findings**. Don't report aesthetic preferences, speculative scaling concerns, or a refactor just because another design pattern is familiar. Prefer the smallest correction consistent with established ownership.

Distinguish:

- **Introduced or materially worsened by the change:** eligible as merge-request findings.
- **Pre-existing and unchanged:** omit from MR findings, except separately flag serious defects or vulnerabilities worth alerting the user to. Don't make unrelated legacy debt a reason to reject the merge request.
- **Unverified concern:** investigate if possible, then label as uncertainty or a question, never as a confirmed defect.

For each candidate finding, verify the affected path and conditions against the current head, check relevant tests and surrounding behavior, and try to disprove the concern before reporting it. Point to precise file/line locations, preferably lines in the current proposed diff. If a problem lies outside changed lines, explain how the new code exposes or worsens it.

## 4. Use specialist reviews selectively

This skill **owns the final merge-request assessment**. Use other review skills only when their additional analysis materially improves confidence; do not invoke them all mechanically.

- `review-code`: reuse its repository-fit and requirement-fit checks **when its comparison-base contract can be met**. Its standalone skill requires a user-supplied base or a base recorded before implementation began; **do not fabricate such a record** from merge-request metadata. Otherwise apply equivalent relevant checks directly in this skill.
- `review-security`: request focused threat analysis when a change materially crosses an authentication, authorization, credential, or sensitive-data boundary, or a credible issue needs attacker-path validation.
- `review-architecture`: request focused assessment when an identified ownership, dependency, or structural concern needs more investigation than an ordinary diff review provides.

Pass each specialist a **bounded scope**, authoritative requirements, and concrete repository evidence. Keep the overall review read-only and conversation-based, even if a specialist would normally create a durable report. Incorporate relevant findings into one consolidated result, recheck them, and remove duplicates. A specialist's recommendation is not permission to redesign or change scope.

## 5. Verification and external evidence

Read existing reviewer comments, open and resolved threads, and CI results as **evidence**, not as substitutes for independent assessment. Check whether reported issues remain in the current head. Do not repeat a resolved concern simply because an old comment exists. Distinguish failed, skipped, pending, and unavailable checks, and determine whether failures are attributable to this change before treating them as findings.

Run relevant tests, static checks, or non-destructive reproductions when safe and practical. Prefer targeted checks that distinguish a concrete hypothesis. If deeper verification is warranted, use an isolated temporary checkout/worktree or disposable fixtures; do not change reviewed source files or persistent repository state.

Before executing code from an untrusted contribution, assess its side effects and exposure to credentials, networks, or production resources. Do not execute destructive operations, intrusive security tests, or commands against production systems without separate explicit authorization. Never expose secrets in findings. If validation is unsafe or unavailable, explain exactly what remains unverified.

A test passing does not prove the absence of defects; a test failing does not by itself establish a change-introduced defect.

## 6. Full review versus re-review

**Full review (default):** Review the complete current diff against its target/base and assess the applicable acceptance criteria.

**Re-review (when requested):** Obtain the previous review's head SHA and findings when available. Compare that head to the new head; verify each prior finding as **resolved**, **partially resolved**, **unresolved**, or **no longer applicable**. Examine the new changes for regressions and recheck relevant acceptance criteria, CI, and security-sensitive paths. If the previous head or findings are unavailable, say so and perform a full review rather than pretending to assess resolution.

The final recommendation must reflect the **current complete merge-request state**, not merely whether the newest patch looks reasonable. Force pushes, target changes, or changed requirements may warrant a full re-review.

## 7. Report findings and recommendation

Present findings in descending practical severity. Include only substantiated, actionable problems. For each finding, use a compact structure:

```markdown
### [High] Short, concrete finding title

- **Location:** `path/to/file.ext:line` (at current head SHA)
- **Category:** Correctness | Requirements | Architecture | Maintainability | Security | Tests | Performance
- **Evidence and failure scenario:** What the code does, when it fails, and why it matters.
- **Impact:** Concrete consequence.
- **Confidence:** High | Medium | Low, with the missing evidence if not high.
- **Recommended correction:** Smallest practical fix; mark consequential design alternatives as requiring user approval.
- **Merge blocking:** Yes | No, with a short rationale.
```

Use **Critical / High / Medium / Low** severity independently of confidence:

- **Critical:** Catastrophic or broadly exploitable security/data-loss failure under credible conditions; normally blocking.
- **High:** Significant correctness, security, reliability, or requirement failure; normally blocking.
- **Medium:** Material but bounded defect or maintainability consequence; block when impact is meaningful and evidence is sufficient, not automatically.
- **Low:** Minor but actionable issue; normally non-blocking.

Do not block merging solely on unverified speculation, missing aesthetic polish, or unrelated pre-existing issues. If an essential security/requirements boundary cannot be evaluated, explain that limitation and why it does or does not prevent a confident approval recommendation.

Conclude with:

1. **Requirements coverage:** status of each Jira acceptance criterion (met / unmet / unverifiable), with brief evidence; mention any consequential secondary requirements.
2. **Verification:** relevant tests/checks and CI status actually observed, including failures or gaps.
3. **Pre-existing serious concerns / open questions:** only when applicable; do not mislabel them as introduced findings.
4. **Recommendation: Approve** or **Recommendation: Request changes** — a reasoned assessment based on blocking findings and material unresolved risk. If critical evidence is missing, say why the recommendation is provisional and what would resolve it.

If no material findings are supported, state: **No material issues found within the reviewed scope and available evidence.** Do not claim the change is bug-free, secure, or fully verified if that has not been established.

Never post the review to the hosting platform, set its review state, or change files as part of this skill.
