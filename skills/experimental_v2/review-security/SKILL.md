---
name: review-security
description: Examine a specific security-sensitive change, data flow, or trust boundary using current repository evidence and realistic threat scenarios. Use for authorization, credentials, untrusted input, sensitive-data processing, external integrations, or suspected vulnerabilities.
---

# Security Review

Evaluate credible threats to a **bounded, real system**. Follow root `CLAUDE.md` for decision authority. This is a focused security assessment, not a general code-quality review or permission to redesign or repair the system.

Invoke this skill when security is an explicit concern or when the relevant change materially affects authentication, authorization, tenant isolation, secret handling, untrusted input, or sensitive-data flow. Do not invoke it as a mandatory stage for ordinary low-risk edits. `review-code` continues to own general repository and requirement fit; this skill adds threat-oriented evidence and reasoning.

## 1. Establish the boundary

Identify, using the request and current repository evidence:

- the behavior, change, component, or data flow being reviewed;
- protected assets and relevant sensitive information;
- actors and their actual privileges (including unauthenticated actors when applicable);
- input and output entry points, trust boundaries, and enforcement points;
- relevant deployment assumptions, configurations, and existing controls;
- applicable approved requirements, domain records, and ADRs.

Inspect only enough adjacent code and infrastructure to follow the **complete relevant trust boundary**. If evidence shows that the requested scope ends before an important enforcement point or downstream sink, explain the necessary scope extension. Do not turn a focused review into an unrestricted repository audit.

Separate **verified facts**, **documented design claims**, **unverified assumptions**, and **security questions**. An intended safeguard is not proof that the deployed implementation enforces it. Conversely, missing documentation is not proof of a vulnerability.

## 2. Trace the relevant flows

Trace untrusted input, privilege, credentials, or sensitive data from their origin to the meaningful decision points and sinks. Depending on scope, inspect:

- authentication and session identity;
- authorization at the operation or resource boundary, including ownership and tenant isolation;
- validation, parsing, canonicalization, and output encoding;
- privilege changes, external calls, and service-to-service trust;
- logging, telemetry, persistence, caches, backups, and deletion;
- secret injection, use, rotation, and exposure;
- model, tool, and connector transmission, including untrusted instructions when relevant;
- error responses and other paths that can disclose sensitive information.

This is a set of **possible inspection points**, not a checklist of findings. Evaluate only paths that exist or matter to the selected scope. Do not assume a control is present or absent without evidence.

Do not copy raw secrets, tokens, personal data, or sensitive payloads into prompts or the review document. Redact examples; record file locations and control behavior instead. Avoid accessing production secrets or running disruptive security tests.

## 3. Develop and validate threat hypotheses

For each plausible issue, answer:

1. **Attacker or failure actor:** Who can cause it, and with what starting privileges?
2. **Entry and reachability:** How does that actor reach the relevant code or data?
3. **Failed boundary:** What authorization, isolation, validation, or other control is bypassed or missing?
4. **Consequence:** Which asset or guarantee could be compromised?
5. **Evidence and counterevidence:** What current code, tests, configuration, or platform behavior supports or weakens this scenario?
6. **Validation:** What safe observation or test would distinguish a vulnerability from an unverified concern?

Use existing tests, targeted static inspection, local fixtures, non-destructive test environments, and authoritative documentation as appropriate. When claims depend materially on library, platform, or protocol behavior, identify the actual installed version and verify the relevant behavior against primary sources when available.

Do not fabricate exploitability from a generic pattern, claim root cause from correlation, or label absent evidence as a confirmed vulnerability. A theoretically possible attack is not necessarily reachable under the actual deployment and permission model.

Classify each concern as one of:

- **Confirmed vulnerability:** Current evidence establishes a reachable security failure under stated conditions.
- **Credible unverified risk:** A realistic scenario exists, but a material premise or control cannot yet be established.
- **Assumption / missing evidence:** A security-relevant fact is unknown, without enough evidence to assert a specific risk.

Reject weak hypotheses rather than padding the report. If no material issue is supported, say so **within the inspected boundary and evidence**; never declare the system categorically secure.

## 4. Recommend proportional corrections

For each confirmed vulnerability or credible material risk, propose the **smallest mitigation** that closes the relevant boundary. Prefer using existing security ownership and project patterns instead of introducing infrastructure or abstractions by default.

Distinguish a necessary mitigation from optional defense in depth. Explain tradeoffs and how the fix should be verified, such as authorization or tenant-isolation tests, malformed-input tests, data-disclosure checks, configuration checks, or deployment verification.

This skill **does not modify production code, permissions, credentials, configuration, or deployed systems**. Recommend a change without treating the recommendation as approval. If mitigation requires a consequential product, security, or architectural decision, compare real alternatives and ask the user to choose before implementation through `implement` or another authorized workflow. Do not request approval merely to inspect evidence or perform safe, read-only investigation.

## 5. Report findings

Report findings in order of **practical risk**, considering both plausible impact and attacker prerequisites/reachability; do not rank solely by theoretical worst-case impact. State severity as Critical / High / Medium / Low when supported by evidence, and report confidence **separately**. Severity is a reasoned project assessment, not a claimed CVSS score unless one was actually calculated.

For each substantive finding record:

- **Finding and classification:** Confirmed vulnerability or credible unverified risk.
- **Severity / confidence:** With a short justification.
- **Affected asset and trust boundary:** What is protected, and where the failure occurs.
- **Evidence:** Specific code, config, tests, or documentation locations; distinguish inference from observation.
- **Scenario and prerequisites:** What an attacker or failure actor can actually do.
- **Impact:** Realistic consequence under the stated conditions.
- **Recommended mitigation:** Minimal correction and meaningful tradeoffs.
- **Verification:** Safe checks that would confirm or reject the concern and validate a fix.

Also include **Review Scope and Assumptions**, **Missing Evidence**, and **Residual Risk** as applicable. Document relevant verified controls concisely when they materially qualify a finding or explain why a suspected issue was rejected. Avoid duplicating a general code review or repeating the same issue at several levels.

If a relevant approval is unresolved, end with **Decisions Requiring Approval**, including the decision, alternatives, recommendation, and what remains blocked. Do not represent a recommended mitigation as an approved decision.

## 6. Persist only when useful

Provide the review in the current response by default. Write a durable artifact when the user requests one, the review finds consequential risks or decisions worth revisiting, or the investigation is substantial enough that future work would otherwise have to repeat it.

For a durable review, create a new append-only Markdown file under:

```text
docs/security/<NN>-<short-slug>-review.md
```

Inspect existing names and increment the highest numeric prefix, retaining existing padding (or using two digits if none exist). Create the directory only when required. Never overwrite a previous review. Keep the record evidence-based, redact sensitive values, and include sources, assessment date when relevant to version-dependent claims, scope limitations, and the findings above. The review documents evidence **at the time it was inspected**; subsequent corrections belong in the implementation record or a new review, not silent retroactive edits.

Report the saved path when a file is created. Otherwise give the actionable result without generating documentation for its own sake.
