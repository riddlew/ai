---
name: security-review
description: Review security, trust, authorization, secret, and sensitive-data boundaries, then write a durable review artifact. Use for authentication or authorization changes, untrusted input, logging and persistence, connector or model transmission, credential handling, or threat-focused review.
---

# Security Review

Trace credible threats and sensitive-data flows across the actual system boundary. Do not infer safety from missing evidence or broaden the review beyond the stated scope without explaining why the boundary is incomplete.

Use `$ARGUMENTS` as the change set, threat, data flow, or review scope when provided.

## Result Artifact

Before reviewing, locate the nearest project `.claude/` directory from the working directory up to the repository root. Do not use the personal `~/.claude/` directory.

- If no project `.claude/` directory exists, ask the user where to save the result before continuing. Do not create `.claude/`, choose another location, or skip the artifact without their answer.
- Resolve the work-item directory as `.claude/results/<ISSUE-ID>/` from an explicit ticket or issue ID. Without one, use a matching existing work item or create `.claude/results/<NNN>-<short-slug>/` with the next unused three-digit sequence.
- Read available investigation, combined plan, implementation, diagnosis, and earlier review artifacts as context. If reviewing `02-plan.md`, trace the proposed data and trust boundaries before implementation. Recheck all claims against current code, configuration, and authoritative security evidence.
- Write a new append-only result at `reviews/<NN>-security-review.md`, using the next unused two-digit review sequence. Do not overwrite an earlier review.
- Put the work-item key, stage, status, updated date, reviewed revision or boundary, and input artifact paths in YAML frontmatter. Put findings, scope limitations, and residual risk in the body. Never persist secrets or sensitive values in the artifact.
- Report the artifact path to the user.

## Workflow

1. Establish assets, actors, trust boundaries, entry points, authorization rules, and the review boundary.
2. Trace untrusted and sensitive data from input through validation, processing, logging, persistence, backups, telemetry, model or connector transmission, and deletion.
3. Inspect authentication, authorization, tenant separation, privilege changes, secret handling, encryption assumptions, escaping, and failure behavior where relevant.
4. For each concern, state a plausible attacker or failure scenario and the prerequisite conditions. Separate confirmed vulnerabilities from risks requiring validation.
5. Check relevant tests, configuration, deployment assumptions, and dependency behavior. Verify version-sensitive security claims against installed versions and authoritative sources.
6. Recommend the smallest practical mitigation that addresses the boundary, including regression or abuse-case validation.
7. Do not expose secrets in output or modify code, credentials, permissions, or production state unless the user explicitly authorizes it.

## Output

Write the review artifact with findings ordered by severity. For each finding include:

- affected asset and trust boundary;
- evidence and precise location;
- threat or failure scenario;
- likelihood, impact, and confidence;
- recommended mitigation and verification.

Also state scope limitations, missing evidence, and residual risk. If no material vulnerability is found, say so without claiming the system is secure.
