---
name: brain-next
description: Recommend the next useful step from actual context and blockers; no approvals or mandatory document sequence.
disable-model-invocation: true
---

# Brain next

Read only relevant current feature/decision/implementation context and Git evidence. Recommend ONE actionable next command, or say no action is needed. Requirements unclear → brainstorm; clear work → implement directly; recommend optional spec, design, decomposition or tasks only when they materially help. Never require an approval status, parent hashes, or an implementation plan just to implement.

A user may request a narrow existing-document reconciliation; if established and safely scoped, the relevant Brain skill may make the edit directly. For substantial or conflicting changes, recommend the appropriate owner and explicit amendment. Never automatically invoke `brain-update`, `brain-implement` or other skills, write code or commit.

Briefly give the rationale, no administrative checklist. Default inline.
