# Optional functional decomposition (v5)

Use when separate functional responsibilities materially improve an otherwise complicated feature. Never force an intermediate level. Read currently established requirements, examples, owners, callers, tests and architectural contracts. Preserve existing responsibilities unless the user selects a meaningful change.

A component record states responsibility, relevant requirement references, excluded behavior, public interactions, acceptance examples and meaningful dependencies. Do not invent services/classes solely because a component document exists. Save only as useful under `03-components/` with stable CMP IDs and optional parent links; an independent component need not have a spec.

Check real requirement ownership and overlap where a specification exists. Do not request document approval, compute fingerprints or invoke `brain-update`. Consult the user only for unresolved consequential decisions.
