# Brain v5 feature document contract

## Optional document hierarchy

`.brain/features/<feature>/01-brief/`, `02-specifications/`, `03-components/`, `04-implementation-plans/`, and `05-tasks/` are OPTIONAL. Direct implementation from an explicit request or brainstorming is valid. No empty placeholders, required stage transitions or document approval gates.

New feature files use YAML frontmatter with `id`, `kind`, `parents: []`, `requirements: []` and `depends_on: []`. `status` and `parent_hashes` are legacy optional metadata: do not generate or require them; ignore historical approval values/fingerprints. A plan or task may be independent with no governing parents when no higher-level documents exist. Stable IDs: BRF, SPEC, CMP, PLAN, TASK and local REQ-###, E#. Preserve IDs on edits.

A document's `parents` are explicit applicable higher-level documents; `requirements` are qualified `SPEC-001#REQ-001` refs; `depends_on` represents real same-kind prerequisites. Validate IDs, links, requirement refs, dependencies and cycles. Optional coverage checks report actual missing coverage only for a stage that exists and claims it; they do not invent mandatory documents.

## Decision authority and amendments

Each decision has one authoritative home: behavior in spec or minimal brainstorm decision record, design in plan, cross-feature architecture in ADR/user decisions. Source documents named authoritative govern their exact technical contracts. A handoff or execution record is only a reference and status aid.

When implementation is underway, material requirement/design changes may use a new focused spec/plan with `amends: [SPEC-001]` and `supersedes: [SPEC-001#REQ-003]` (or a stable design anchor). Scope must be explicit. The original governs unaffected decisions. Newest timestamp does not imply authority. Cycles, unknown targets, duplicate or conflicting supersession claims are validation errors requiring reconciliation. Minor edits and local choices do not require amendments. When no original spec/plan exists, create a concise focused decision record only if useful.

## Ownership

- Brief/brainstorm decisions: brain-brainstorm
- Specifications: brain-write-spec
- Components: brain-decompose-feature
- Implementation plans: brain-design-implementation
- Tasks: brain-write-tasks
- Execution/handoff: brain-implement or brain-pair-program; brain-brainstorm may create a concise handoff when necessary
- Shared project knowledge, source maps and ADRs: brain-update
- Manual editorial previews: brain-compact

Brainstorm may make a narrowly scoped edit to an existing spec/plan when the user has settled that decision and affected references are known. Never overwrite unrelated material or bypass a consequential unresolved decision. No automatic `brain-update` and no producer approval cascade.

`execution.md` is optional for short work; where present, record current focus, completed/remaining behavior, blockers, active amendments and verified tests. `handoff.md` is an optional minimal cross-session pointer, not a competing authority. Keep metadata, requirements and design concise and link rather than copy.

## Validation and compatibility

`python skills/experimental_v5/brain-init/scripts/validate_feature_docs.py .brain/features --check-coverage`
`sh skills/experimental_v5/brain-init/scripts/brain-tool validate --brain .brain`

The validator accepts historical v4 `status` and `parent_hashes` as inert legacy fields, without requiring reapproval. Project v5 selection is explicit in the installed `CLAUDE.local.md`. Preserve v4 files and archive metadata without bulk migration.
