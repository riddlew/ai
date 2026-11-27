# Optional implementation plan details (v5)

A plan is useful for multi-component, risky or multi-session changes, but **never required** before `brain-implement`. Inspect actual implementation, callers, tests, Git SHA, established behavior, applicable ADRs and source contracts.

Plan the smallest viable change: existing owners first, relevant methods/interfaces, data/control flow, failure paths, compatibility, concurrency/persistence/security where relevant, negative constraints and focused verification. Distinguish *binding user-established structure* from illustrative helpers/pseudocode. Avoid speculative abstractions or architecture. Ask the user only about unresolved consequential design choices.

Write a concise `04-implementation-plans/` document when useful, without approval/status metadata or fingerprints. When a material change is chosen after implementation starts, prefer a narrowly scoped new plan with `amends` and `supersedes` pointing to a concrete original decision anchor. Unaffected decisions remain binding; no timestamp-based override.

Do not edit code, force tasks/decomposition, or automatically invoke `brain-update`. See v5 feature document contract and `blueprint-template.md`.
