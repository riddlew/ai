# Review Finding Format

Shared by `review-code`, `review-security`, `review-architecture`, and `review-merge-request`. A skill may add fields or define its categories; it does not remove or redefine the fields below.

## Severity

Rate the actual impact under credible conditions, independently of confidence.

- **Critical** — catastrophic or broadly exploitable security or data-loss failure under credible conditions.
- **High** — significant correctness, security, reliability, or requirement failure.
- **Medium** — material but bounded defect or maintainability consequence.
- **Low** — minor but actionable issue.

Do not raise severity for a worst case that the actual callers, permissions, or deployment make unreachable.

## Confidence

- **High** — the failure path or mismatch was traced in current code or reproduced.
- **Medium** — strongly supported, but at least one material premise is unverified.
- **Low** — plausible, but key evidence is missing.

When confidence is not High, name the missing evidence.

## Fields

```markdown
### [Severity] Short, concrete title

- **Location:** `path/to/file.ext:line`
- **Category:** <defined by the reporting skill>
- **Evidence and failure scenario:** What the code does, under which conditions it fails or diverges, and how this was established.
- **Impact:** The concrete consequence.
- **Confidence:** High | Medium | Low — missing evidence if not High.
- **Smallest correction:** The least disruptive fix. Mark consequential alternatives (ownership, contracts, persistence, architecture) as **requires approval**.
```

Report only substantiated, actionable findings, ordered by severity. Omit aesthetic preferences and speculative refactors.
