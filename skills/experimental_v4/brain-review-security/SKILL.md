---
name: brain-review-security
description: Examine a specific security-sensitive change, data flow, or trust boundary using current repository evidence and realistic threat scenarios. Use for authorization, credentials, untrusted input, sensitive-data processing, external integrations, or suspected vulnerabilities.
---

# Security Review

**Project brain:** If `.brain/00_index.md` exists (at this worktree's root, or in the main checkout when working in a linked git worktree) and you have not read its root files in this session (or they were lost to context compaction), read every root `.md` file in that `.brain/` now. Read subfolders only when a root file links to them or the task needs them. Do not load `.brain` into subagents wholesale; pass only what their task needs. If no brain exists, proceed without one and mention once that `/brain-update` can create it.

Evaluate credible threats to a **bounded, real system**. Follow root `CLAUDE.md`. This is a focused security assessment, not a general code review (`brain-review-code` owns that) and not permission to modify code, permissions, credentials, configuration, or deployed systems.

Use it when security is an explicit concern or a change materially affects authentication, authorization, tenant isolation, secret handling, untrusted input, or sensitive-data flow, not as a mandatory stage for low-risk edits.

## 1. Establish the boundary

From the request and current repository evidence, identify:

- the behavior, change, component, or data flow under review;
- protected assets and sensitive information;
- actors and their actual privileges, including unauthenticated actors;
- entry points, trust boundaries, and enforcement points;
- deployment assumptions, configuration, and existing controls;
- applicable requirements, `.brain` root files, and ADRs.

Inspect only enough adjacent code and infrastructure to follow the **complete relevant trust boundary**. If the requested scope ends before an important enforcement point or sink, explain the needed extension rather than auditing the whole repository.

Separate **verified facts**, **documented design claims**, **unverified assumptions**, and **security questions**. An intended safeguard is not proof of enforcement; missing documentation is not proof of a vulnerability.

## 2. Trace the relevant flows

Trace untrusted input, privilege, credentials, and sensitive data from origin to decision points and sinks. Inspection points, as they apply:

- authentication and session identity;
- authorization at the operation or resource boundary, including ownership and tenant isolation;
- validation, parsing, canonicalization, and output encoding;
- privilege changes, external calls, and service-to-service trust;
- logging, telemetry, persistence, caches, backups, and deletion;
- secret injection, use, rotation, and exposure;
- model, tool, and connector transmission, including untrusted instructions;
- error responses and other disclosure paths.

These are places to look, not a checklist of findings. Do not assume a control is present or absent without evidence.

Do not copy raw secrets, tokens, personal data, or sensitive payloads into prompts or reports; record locations and control behavior instead. Do not access production secrets or run disruptive tests.

## 3. Develop and validate threat hypotheses

For each plausible issue, answer:

1. **Actor:** who can cause it, with what starting privileges?
2. **Reachability:** how does that actor reach the code or data?
3. **Failed boundary:** which control is bypassed or missing?
4. **Consequence:** which asset or guarantee is compromised?
5. **Evidence and counterevidence:** what supports or weakens the scenario?
6. **Validation:** what safe observation or test would confirm or reject it?

Use existing tests, targeted static inspection, local fixtures, non-destructive environments, and authoritative documentation. When a claim depends on library, platform, or protocol behavior, identify the installed version and verify against primary sources when available.

Classify each concern:

- **Confirmed vulnerability** — current evidence establishes a reachable security failure under stated conditions.
- **Credible unverified risk** — a realistic scenario exists, but a material premise or control cannot yet be established.
- **Assumption / missing evidence** — a security-relevant fact is unknown, without enough evidence to assert a specific risk.

Reject weak hypotheses rather than padding the report. If nothing material is supported, say so **within the inspected boundary and evidence**; never declare the system categorically secure.

## 4. Recommend proportional mitigations

For each confirmed vulnerability or credible material risk, propose the **smallest mitigation** that closes the boundary, using existing security ownership and project patterns. Distinguish necessary mitigation from optional defense in depth, and say how to verify the fix (authorization or tenant-isolation tests, malformed-input tests, disclosure checks, configuration or deployment verification). If mitigation requires a consequential product, security, or architectural decision, compare the real alternatives and ask the user to choose.

## 5. Report

Order findings by **practical risk**: plausible impact weighed against attacker prerequisites and reachability, not theoretical worst case. Severity is a reasoned project assessment, not a CVSS score unless one was calculated.

Format findings per `${CLAUDE_SKILL_DIR}/../brain-review-code/references/findings.md`, with:

- **Category:** Confirmed vulnerability | Credible unverified risk
- **Evidence and failure scenario:** include the actor, prerequisites, and reachability; distinguish observation from inference.
- Added fields: **Asset and trust boundary** (what is protected and where the failure occurs) and **Verification** (safe checks that would confirm the concern and validate a fix).

List assumptions and missing evidence separately, not as findings. Also include **Review Scope and Assumptions**, **Missing Evidence**, and **Residual Risk** as applicable. Mention verified controls only when they qualify a finding or explain a rejected hypothesis. If an approval is outstanding, end with **Decisions Requiring Approval**: the decision, alternatives, recommendation, and what remains blocked.

## Output

Deliver the review in the conversation. Write a durable report only when the user requests one or a workflow needs it for continuation.

A durable report goes in `.brain/reviews/security/<NN>-<short-slug>.md`: increment the highest existing number, matching its padding (two digits by default), and create the directory only when needed. Never overwrite a previous review. Redact sensitive values; include sources, scope limits, and the assessment date when claims are version-dependent. The report records evidence at the time of inspection; later fixes belong in the implementation record or a new review.

When you save a durable report, it is the only file you write. Then invoke `brain-update` with a one-line summary of what changed.

Report the saved path when a file is created.
