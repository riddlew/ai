# Implementation plan template

Follow the shared feature-document contract. `brain-design-implementation` owns the plan; `brain-implement` keeps execution evidence **outside** it in the feature's `execution.md`. Do not mix design approval and mutable execution status.

```markdown
---
id: PLAN-001
kind: implementation-plan
status: draft
parents: [CMP-001]
requirements: [SPEC-001#REQ-001]
depends_on: []
parent_hashes: []
---
# <Component / functional area> — Implementation Plan

Design inspected at: <full HEAD SHA>
Approval: pending

## Intended change and unchanged boundaries
- Change:
- Keep unchanged:

## Existing code and verified owners
| Existing file / component | Verified current behavior | Intended change | Why |
|---|---|---|---|

## Binding design constraints
- <approved requirement or design choice; cite decision, ADR, or user approval>

## Proposed structure, interfaces and call flow
<Important interfaces, state transitions, error paths, and interactions. Label examples Binding or Illustrative.>

## Method outlines (optional)
<Only when important or user-requested.>

## Behavioral increments and verification
1. <coherent behavior> — <SPEC-001#REQ-001 / SPEC-001#E1> — <verification boundary>

## Dependencies and assumptions
- <real prerequisite, unknown, or None>

## Open consequential decisions
- <question and affected scope, or None>
```

Fill `parent_hashes` with current fingerprints of approved parent components (or whichever earlier levels actually govern the plan), using the shared contract's helper. Do not approve the plan with empty parent hashes when `parents` is nonempty.

After explicit user approval set `status: approved` and record `Approval: user confirmed <date/context>`. If binding details change, set `needs-revision` until reaffirmed. Plan files contain **no** `Review base`, execution checklist, worktree, verification result, or mutable task progress.
