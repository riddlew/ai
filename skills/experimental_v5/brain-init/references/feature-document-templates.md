# Brain v5 optional feature templates

Use only the artifacts helpful to the requested task. IDs and example requirements below are illustrative. No approval states or parent fingerprints. Preserve existing IDs.

## 01 — Brief
```markdown
---
id: BRF-001
kind: brief
parents: []
requirements: []
depends_on: []
---
# <Feature>: Brief
## Objective and exclusions
## Settled decisions and non-obvious constraints
## Remaining questions
```

## 02 — Specification
```markdown
---
id: SPEC-001
kind: specification
parents: []
requirements: []
depends_on: []
---
# <Feature>: Specification
## Scope
## Requirements
- REQ-001: <observable behavior>
## Examples
- E1: Given <state>, when <action>, then <result>
## Constraints and verification
```

## 03 — Component
```markdown
---
id: CMP-001
kind: component
parents: []
requirements: []
depends_on: []
---
# <Feature>: Component
## Responsibility
## Interfaces and relevant requirements
```

## 04 — Implementation plan
```markdown
---
id: PLAN-001
kind: implementation-plan
parents: []
requirements: []
depends_on: []
---
# <Feature>: Implementation plan
Design inspected at: <Git revision, if inspected>
## Ownership and concrete design
## Failures, compatibility and verification
## Binding constraints versus illustrative choices
```

## 05 — Task
```markdown
---
id: TASK-001
kind: task
parents: []
requirements: []
depends_on: []
---
# <Feature>: Task
## Action and expected behavior
## Verification
```

## Optional focused amendment
```markdown
---
id: PLAN-002
kind: implementation-plan
parents: []
requirements: []
depends_on: []
amends: [PLAN-001]
supersedes: [PLAN-001#cancellation-strategy]
---
# Cancellation change
## Reason and new decision
## Exact old decision being replaced
## Affected implementation and tests
```
