---
name: brain-design-implementation
description: Write optional code-specific technical plans for complex work; no document approval or implementation prerequisite.
---

# Implementation design

Create a technical plan when scope, risk or cross-session coordination justifies it; `brain-implement` does not require one. Inspect actual current code, owners, callers, tests, relevant specs, amendments and ADRs; record inspected revision when useful. Distinguish binding user-established decisions from illustrative helper details. Describe the smallest viable ownership, data/control flow, interfaces, errors, preserved behavior and verification.

Ask only unresolved consequential architecture or behavior questions. Write a concise plan under `04-implementation-plans/` using `brain-tool doc new --kind plan` for new files or edit an existing plan. Never require document approval, parent hashes, or status transitions. For significant design changes after implementation begins, prefer a focused amendment identifying precise prior decisions superseded.

Do not edit application code or invoke `brain-update` automatically. See the v5 feature contract. Load `references/blueprint-details.md` only when complex design requires it; default inline.
