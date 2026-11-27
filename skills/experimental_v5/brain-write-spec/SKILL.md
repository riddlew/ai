---
name: brain-write-spec
description: Write optional testable behavioral specifications from settled decisions and source evidence, without approval gates.
---

# Write specification

Use only when a specification will materially help. Inspect active decisions, authoritative contracts, relevant source and existing feature documents. Define observable scope, `REQ-###` requirements, concrete `E#` examples (normal, edge, failure, unchanged behavior), exclusions and proportionate verification; do not invent requirements. Write a concise specification in `.brain/features/<feature>/02-specifications/` using `brain-tool doc new --kind specification` if new, or modify an existing specification without renumbering requirements.

No `status: draft/approved/needs-revision`, user approval, parent fingerprint or descendant reapproval cycle. For material changes after implementation begins, prefer a focused new specification amendment explicitly identifying `amends` and `supersedes`, leaving unaffected original decisions in force. Do not create documentation merely because a stage exists. Record unresolved consequential choices instead of silently deciding.

Never invoke `brain-update` automatically. See `../brain-init/references/feature-document-contract.md`; consult `references/spec-details.md` only for complex examples or legacy-document conversion. Default inline; concise final summary.
