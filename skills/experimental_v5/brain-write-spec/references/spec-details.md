# Optional specification details (v5)

Use when a durable behavioral contract helps implementation, verification or session continuity; direct `brain-implement` is valid without it. Read established user decisions, authoritative technical sources, relevant current behavior, callers and tests. Separate required observable results from existing implementation facts and optional technical choices.

Define compact, stable `REQ-001`, `REQ-002`, etc., and concrete `E1`, `E2` examples for normal, edge, failure, compatibility and unchanged behavior. Each example identifies given state/input, action and expected observable output. Specify exclusions and meaningful verification, not unnecessary code architecture. Preserve stable IDs in edits.

Write new `02-specifications/` files through `brain-tool doc new --kind specification` when useful. No approval-state metadata or parent hashes. For established changes to an existing feature before implementation, update only affected sections. For a material mid-implementation change, prefer a focused amendment with `amends` and `supersedes` pointing to the exact original requirement anchor. Do not require reapproval of unrelated documents.

Never automatically invoke `brain-update`. Ask the user only for unresolved consequential behavioral decisions, not for administrative approval of the document.
