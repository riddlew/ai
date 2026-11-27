# Optional plan example (v5)

```markdown
---
id: PLAN-001
kind: implementation-plan
parents: []
requirements: []
depends_on: []
---
# Feature: Implementation plan

Design inspected at: <verified Git revision>

## Objective and unchanged boundaries
## Existing owners and source evidence
## Proposed code changes and interface/data flow
## Established binding design constraints
## Illustrative implementation details
## Failure cases, compatibility and security risks
## Proportionate verification
## Unresolved consequential decisions
```

For an amendment, add `amends: [PLAN-001]`, `supersedes: [PLAN-001#stable-anchor]`, explain the changed decision and identify affected code/tests. Do not add approval states, fingerprint metadata or execution history to the plan. Keep mutable progress in optional `execution.md`.
