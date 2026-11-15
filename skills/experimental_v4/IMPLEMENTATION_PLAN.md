# Hierarchical Brain redesign — implementation plan

Status: **Core hierarchy and producer refactor authored; static integration checks added; runtime verification pending** (branch `feature/hierarchical-brain`)

## Objective

Turn the existing `brain-*` skills into a document-first, progressively refinable engineering workflow:

**Brief → Specifications → Components → Implementation Plans → Tasks → Verified Execution**

The five named stages are document types, not mandatory ceremonies. Small, settled changes may go directly to implementation. The existing decision authority, test-first discipline, approved architectural constraints, review checkpoints, branch/worktree safety, and proportional workflow selection remain in force.

This redesign is a clean break for feature documentation. **Do not implement legacy-layout discovery, migration, or compatibility.** Keep project-wide `.brain/` knowledge, ADRs, reviews, exploratory planning, and source maps.

## Canonical feature layout

```text
.brain/
├── 00_index.md, 01_about.md, ..., state.md, glossary.md
├── adrs/, planning/, reviews/, sources/, knowledge/, pending/
└── features/<feature-slug>/
    ├── 01-brief/brief.md
    ├── 02-specifications/<spec-slug>.md
    ├── 03-components/<component-slug>.md
    ├── 04-implementation-plans/<plan-slug>.md
    ├── 05-tasks/<task-slug>.md
    └── execution.md
```

Detailed contracts and templates live in:
- `brain-init/references/feature-document-contract.md`
- `brain-init/references/feature-document-templates.md`

Initial structural checks are implemented in `scripts/validate_feature_docs.py` and `tests/test_feature_document_contract.py`. They have **not yet been executed** in an agent sandbox.

A document's `id` is stable within a feature, regardless of filename; requirement and example IDs are qualified by their specification. A child references the relevant parents and requirements. ADRs remain independent authorities under `.brain/adrs/`. `execution.md` records mutable progress, not intended design.

## Implementation phases

### P1 — Document model and templates
**Status: Authored; verification pending**

- [x] Establish canonical paths and stable document identifiers.
- [x] Establish per-level schemas, authoring rules, and readiness/approval states.
- [x] Establish ownership, traceability, stale-descendant handling, and scope-proportional skipping.
- [x] Provide templates and an explicit example.
- [x] Add initial structural validator and contract-test source.
- [ ] Run and review the contract tests; correct any failures.

**Gate:** A brief, specification, component, plan, task, and execution record can be authored consistently without duplicating authority.

### P2 — Core brain infrastructure and validation
**Status: Initial skill changes authored; validation pending**

- [ ] Update `brain-init` to use the feature hierarchy for new projects.
- [ ] Update `brain-update` to index features and verify links without editing producer-owned content.
- [ ] Update `brain-init/references/CLAUDE.local.md` with document authority, write ownership, and approval rules.
- [x] Author initial dependency/reference validator and unit tests (execution not yet verified).
- [ ] Run validator tests and integrate structural checks into skill handoffs.
- [ ] Preserve existing main-branch, worktree, and context-loading safeguards. Load feature details on demand.

**Gate:** New-brain setup, indexing, structural checks, and branch-aware updates work with the canonical feature layout.

### P3 — Progressive functional decomposition
**Status: Producer instructions authored; validation pending**

- [x] `brain-brainstorm`: capture an approved `01-brief/brief.md` without changing its decision process.
- [x] `brain-write-spec`: write behavior-first `02-specifications/` documents with stable requirement/example IDs.
- [x] **New `brain-decompose` skill:** group specifications into coherent functional components under `03-components/`; demonstrate complete requirement coverage and meaningful boundaries.
- [x] `brain-plan`: retain its role for investigations, unresolved decisions, and multi-session planning, with updated handoffs.

**Gate:** One approved brief yields specifications and traceable components; open decisions remain open.

### P4 — Implementation plans and task generation
**Status: Initial skill changes authored; validation pending**

- [x] `brain-blueprint`: produce codebase-grounded `04-implementation-plans/` documents for components; preserve binding/illustrative design distinctions and explicit approvals.
- [x] **Rename and evolve `brain-write-tickets` → `brain-write-tasks`**. Reuse its dependency/coverage/builder-review discipline, but generate executable `05-tasks/` documents from approved plans.
- [x] Remove the old `brain-write-tickets/SKILL.md` and update core planning handoffs; [ ] finish references in guides, supporting skills, and tests; **do not** maintain parallel ticket/task generation.
- [ ] Preserve `brain-plan` planning tickets as a separate kind of investigation/decision record, not implementation tasks.

**Gate:** Approved component designs yield small, executable, verifiable tasks with real dependencies.

### P5 — Execution ownership and resumption
**Status: Initial skill refactor authored; validation pending**

- [x] `brain-implement`: consume actionable tasks and governing documents; preserve collaborative/guided/autonomous modes.
- [x] Move mutable progress and review evidence out of implementation plans into feature-level `execution.md`.
- [x] Retain review base, branch, worktree, checkpoints, verification, Rulings, Deferred, and design deviations in the new execution template; [ ] verify behavior in agent tests.
- [x] Require re-verification of completed work and source assumptions on resume; [ ] behavior-test the process. do not silently rewrite approved plans.
- [ ] Preserve direct implementation without five documents for small settled changes.

**Gate:** A multi-session task run resumes from code and evidence, not checked boxes alone.

### P6 — Docs and reference cleanup
**Status: Revised bundled guides; further review pending**

- [x] Update bundled `README.md`, `USAGE.md`, `CLAUDE.local.md`, and `brain-update/references/templates.md` to describe the new hierarchy.
- [ ] Verify guide examples and prose are fully consistent with the new skills.
- [ ] Update skill-local templates, review prompts, and links to changed paths.
- [ ] Remove outdated descriptions of old spec/ticket/impl-plan storage.
- [ ] Provide an end-to-end `StartMachine` example, including ADR links and failure cases.

**Gate:** Installed guides and skill contracts agree on paths and authority.

### P7 — Skill behavior tests and regression
**Status: Static tests and scenario definitions authored; tests not yet run**

- [x] Add H1–H11 behavior scenario definitions (not yet executed).
- [ ] Execute RED/GREEN scenarios in fresh agents.
- [x] Add initial static checks for IDs, dependencies, cycles, parent approval, requirement lineage, and stage coverage; cross-feature and stale-approval behavior still needs validation.
- [ ] Execute and extend static checks where necessary.
- [ ] Check trivial-change bypass, worktree/branch safety, execution resume, and no unapproved architectural decisions.
- [ ] Exercise `StartMachine` end to end: idea → brief → specs → components → plans → tasks → verified implementation.
- [ ] Run the existing relevant `experimental_v4` static tests and fresh-agent regression scenarios.
- [ ] Distinguish tests actually run from planned/unverified tests.

**Gate:** Evidence demonstrates the redesigned workflow and important existing guarantees.

## Implementation order and change boundaries

Work in order P1 → P2 → P3 → P4 → P5 → P6 → P7, but write focused tests alongside each phase. Do not let lower-level documents override approved upstream requirements or ADRs. Escalate consequential user decisions; routine reversible implementation choices remain with the agent. When changing an approved parent, flag affected descendants for revalidation and reapproval as appropriate.

## Definition of done

Five document types have explicit contracts, the new `brain-decompose` exists, `brain-write-tickets` is replaced by `brain-write-tasks`, technical plans and mutable execution records have separate owners, structural and behavioral validation pass, the complete `StartMachine` scenario works, and small work can still bypass unnecessary stages. No legacy feature-layout support is required.

## Current verification and integration limitations

The branch now contains the new `brain-decompose` skill, the renamed `brain-write-tasks` skill (with old `brain-write-tickets/SKILL.md` deleted), updated core producers, and the initial separation of plans from `execution.md`. These are authored instructions, **not yet verified in fresh-agent scenarios**. Existing usage guides, review helpers, and many tests may still refer to the removed layout and skill name; treat that cleanup as open. The validator, unit tests, and fresh-agent behavior scenarios have not yet been executed against a runnable checkout through the GitHub integration. `tests/test_skill_reference_contract.py` now checks referenced bundled files, retired ticket writer naming, and canonical producer targets. A previously malformed `brain-update` indexing step and obsolete shared-plan documentation have been corrected. Test execution and semantic validation remain necessary. Do not claim regression success before running actual checks in a checkout.
