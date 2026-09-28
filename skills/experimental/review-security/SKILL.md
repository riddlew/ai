---
name: review-security
description: Review security, trust, authorization, secret, and sensitive-data boundaries, then write a durable review artifact. Use for authentication or authorization changes, untrusted input, logging and persistence, connector or model transmission, credential handling, or threat-focused review.
---

# Security Review

Trace credible threats and sensitive-data flows across the actual system boundary.

Do not infer safety from missing evidence. Do not broaden the review beyond the stated scope unless the evidence shows that the boundary is incomplete, and explain why expansion is necessary.

## Establish the review boundary

Before evaluating security, determine:

- assets requiring protection;
- relevant actors;
- trust boundaries;
- entry points;
- authentication and authorization rules;
- sensitive or untrusted data involved;
- the system boundary under review.

Inspect current code, configuration, deployment assumptions, tests, and documentation as needed to understand that boundary.

Recheck security claims against current repository evidence rather than relying solely on plans, earlier reviews, or assumptions.

## Trace sensitive and untrusted data

Follow relevant data through its lifecycle, including where applicable:

- input;
- validation;
- parsing or transformation;
- authorization;
- processing;
- logging;
- persistence;
- backups;
- telemetry;
- model or connector transmission;
- deletion.

Identify where data crosses trust boundaries or changes sensitivity, ownership, or privilege.

Never include actual secrets, credentials, tokens, or other sensitive values in the review artifact.

## Evaluate security controls

Inspect controls relevant to the reviewed boundary, including:

- authentication;
- authorization;
- tenant or user isolation;
- privilege changes;
- secret and credential handling;
- encryption assumptions;
- input validation;
- output escaping or encoding;
- failure behavior;
- sensitive-data exposure.

Do not assume a control exists or works correctly merely because the intended design requires it.

## Evaluate threats

For each concern, describe a plausible attacker or failure scenario.

Identify the conditions required for the scenario to occur.

Keep these distinct:

- confirmed vulnerabilities supported by current evidence;
- credible risks that require further validation;
- assumptions that could not yet be verified.

Do not report hypothetical possibilities as confirmed vulnerabilities.

## Validate supporting evidence

Inspect relevant:

- tests;
- configuration;
- deployment assumptions;
- dependency behavior;
- security-sensitive defaults.

When a security claim depends on a particular dependency or platform version, identify the installed version and verify the claim against authoritative documentation or other primary security sources.

State clearly when required evidence is unavailable.

## Recommend mitigations

For each confirmed or credible issue, recommend the smallest practical mitigation that addresses the actual security boundary.

Include appropriate verification, such as:

- regression tests;
- abuse-case tests;
- authorization tests;
- malformed or adversarial input tests;
- configuration validation;
- deployment checks.

Do not modify code, credentials, permissions, configuration, or production state unless the user explicitly authorizes that work.

## Write the durable review

Every review produces a new append-only Markdown artifact under:

```text
docs/security/
```

Use filenames shaped like:

```text
<NN>-<short-slug>-review.md
```

Before creating the file:

1. inspect existing review filenames in `docs/security/`;
2. find the highest valid numeric prefix;
3. increment it;
4. zero-pad consistently with existing files, or use two digits when no convention exists.

Create `docs/security/` only when the first security review is written.

Never overwrite or replace an earlier review.

Choose a concise slug describing the reviewed security boundary or change.

## Review structure

The review must identify:

- what change, boundary, threat, or data flow was reviewed;
- relevant source artifacts and repository evidence;
- security assumptions that materially affect the conclusions.

Order findings by severity.

For each finding include:

- **Affected asset and trust boundary** — what is at risk and where the relevant boundary lies.
- **Evidence** — concrete supporting evidence and its precise repository location.
- **Threat or failure scenario** — how the issue could realistically occur and its prerequisites.
- **Likelihood** — how plausible exploitation or failure is given the known conditions.
- **Impact** — the consequence if the scenario occurs.
- **Confidence** — how strongly the available evidence supports the finding.
- **Recommended mitigation** — the smallest practical change that addresses the issue.
- **Verification** — how to establish that the mitigation works and does not regress.

Also record:

## Scope Limitations

Areas that were intentionally outside the review or could not be inspected.

## Missing Evidence

Information required for stronger conclusions but unavailable during the review.

## Residual Risk

Security risk that remains after the recommended mitigations or cannot currently be eliminated.

If no material vulnerability is found, state that the review found no material vulnerability within the inspected scope and available evidence.

Do not claim that the system is secure.

Report the created review path to the user.