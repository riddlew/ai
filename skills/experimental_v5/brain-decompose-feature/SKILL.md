---
name: brain-decompose-feature
description: Optionally separate complex feature responsibilities and requirement coverage without approvals.
---

# Decompose feature

Use only when distinct functional responsibilities make decomposition valuable; never mandate a component stage. Read relevant current requirements/decisions, code ownership and constraints. Capture coherent bounded responsibilities with stable CMP IDs and accurate applicable references, without inventing technical services or behavior. Scaffold new files via `brain-tool doc new --kind component` if useful; no parent required when no higher-stage document exists.

Check real coverage and conflicting responsibilities, preserving stable IDs. No approval states, parent hashes, descendant reapproval or automatic `brain-update`. Ask only unresolved consequential user choices. Default inline.
