---
name: brain-review-security
description: Examine a specific security-sensitive change, data flow, or trust boundary using current repository evidence and realistic threat scenarios. Use for authorization, credentials, untrusted input, sensitive-data processing, external integrations, or suspected vulnerabilities.
---

# Security Review

Assess an explicit security concern or a change affecting trust boundaries, authentication/authorization, secrets, untrusted input or sensitive data. Review the **complete relevant data/control flow**, not an arbitrary filename boundary.

## Workflow

1. Identify entry points, trusted/untrusted actors, data stores, sinks, enforcement points, failure conditions and applicable requirements. Inspect relevant code, configuration, tests and existing decisions.
2. Develop concrete threat hypotheses and trace exploit preconditions through validation, authority checks, canonicalization, output encoding, persistence, external interactions and sensitive-data flow. Try to disprove each; **do not invent vulnerabilities**.
3. Report actionable supported findings with evidence, impact, confidence and proportional mitigation. Clearly identify missing evidence, assumptions and residual risk; no categorical safety claim.
4. Never access production secrets, run disruptive tests or copy raw secrets/personal data into prompts or reports. Changes that alter security boundaries or contracts require approval.
5. Deliver findings in the conversation. Save only if requested/required at `.brain/reviews/security/<NN>-<short-slug>/review.md` using `${CLAUDE_SKILL_DIR}/../brain-review-code/references/report-storage.md` and `brain-tool doc new --kind review --report-type security`; invoke `brain-update` when saved.

**Read when needed:** `${CLAUDE_SKILL_DIR}/references/security-review-details.md` for detailed threat modeling, vulnerability classes and report shape. Do not report an unverified hypothesis as a defect.
