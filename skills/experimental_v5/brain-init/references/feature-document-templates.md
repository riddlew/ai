# Feature document templates

Use the smallest relevant template. Follow `${CLAUDE_SKILL_DIR}/../brain-init/references/compact-writing.md`: use concise, self-contained statements, stable cross-references, exact evidence and non-redundant headings. A one-line fact is preferable to a paragraph when meaning is unchanged. Before approving a child, populate `parent_hashes` with the current Git-blob content fingerprints of every direct parent. `parent_hashes: []` is only final for a root brief (or a document with no parents); see the contract. Use the helper described there. Do not add inline YAML comments to list values. Keep YAML metadata consistent with `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-contract.md`; IDs in this file are **illustrative**, not reservations.

## 01 — Brief (`01-brief/brief.md`)

```markdown
---
id: BRF-001
kind: brief
status: draft
parents: []
requirements: []
depends_on: []
parent_hashes: []
---
# <Feature>: Brief

## Problem and motivation
## Desired outcome
## Scope and non-goals
## Known constraints and approved decisions
## Success criteria
## Open decisions
```

## 02 — Specification (`02-specifications/<slug>.md`)

```markdown
---
id: SPEC-001
kind: specification
status: draft
parents: [BRF-001]
requirements: []
depends_on: []
parent_hashes: []
---
# <Feature area>: Specification

## Purpose and scope
## Requirements and invariants
- REQ-001: <normative behavior>
- REQ-002: <normative failure or boundary behavior>

## Concrete examples
- E1: Given <state>, when <action>, then <exact result>.
- E2: Given <failure input>, when <action>, then <exact result>.

## Contracts and affected systems
## Verification strategy
## Open decisions and exclusions
```

The specification *declares* its own requirements in the body; the `requirements` metadata lists externally governing requirements only when appropriate, otherwise `[]`.

## 03 — Component (`03-components/<slug>.md`)

```markdown
---
id: CMP-001
kind: component
status: draft
parents: [SPEC-001]
requirements: [SPEC-001#REQ-001]
depends_on: []
parent_hashes: []
---
# <Functional responsibility>

## Responsibility and outcome
## Governing requirements and examples
## In-scope behavior and boundaries
## Interactions with other components
## Unresolved decisions
## Component acceptance / verification
```

A component is a **behavioral boundary**, not necessarily a class, module, service, or framework component.

## 04 — Implementation plan (`04-implementation-plans/<slug>.md`)

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
# <Component>: Implementation Plan

Design inspected at: <full HEAD SHA>
Approval: pending

## Intended changes and unchanged boundaries
## Existing code and verified owners
## Binding design constraints and sources
## Proposed files, interfaces, and data/control flow
## Failure paths, compatibility, and risks
## Verification strategy
## Assumptions and blockers
```

Keep binding vs illustrative implementation choices distinct. Do not store mutable execution progress here.

## 05 — Task (`05-tasks/TASK-001-<slug>.md`)

```markdown
---
id: TASK-001
kind: task
status: draft
parents: [PLAN-001]
requirements: [SPEC-001#REQ-001]
depends_on: []
parent_hashes: []
---
# <Concrete task>

## Action and implementation context
## Expected behavior / result
## Applicable design constraints
## Acceptance criteria and examples
## Verification
```

Small task does **not** mean a separate file per method or test assertion. Prefer a coherent independently verifiable increment.

## Execution (`execution.md`)

```markdown
# <Feature>: Execution

Review base: <commit before any feature code edits>
Branch: <branch name>
Workspace: <path / main checkout>
Collaboration mode: collaborative
Execution mode: inline

## Task status
- TASK-001: pending | in progress | verified awaiting review | approved done

## Current focus
## Blockers and open decisions
## Design deviations
## Verification evidence (command, outcome, revision)
## Rulings and deferred issues
- **<date> · <actor> · <increment>:** Decision: <exact ruling>; effect: <scope or exception>; basis: <approved source/evidence>.
## Review focus and checkpoint history
- <increment> · <date> · <status>: <verified command/outcome/revision; approval if observed>.
```

Execution status does not alter a task's approved definition. Revalidate the repository on every resumed session.
