# Hierarchical Brain redesign — implementation plan

Status: **Core skills and reproducible H1–H11 fixtures implemented; static CI passing; fresh-agent execution pending** (branch `feature/hierarchical-brain`)

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

Initial structural checks are implemented in `brain-init/scripts/validate_feature_docs.py` and `tests/test_feature_document_contract.py`, and run in GitHub Actions. Fresh-agent behavior tests are still pending.

A document's `id` is stable within a feature, regardless of filename; requirement and example IDs are qualified by their specification. Approved children carry `parent_hashes` content fingerprints so changes to governing documents invalidate stale approvals rather than silently continuing. ADRs remain independent authorities under `.brain/adrs/`. `execution.md` records mutable progress, not intended design.

## Implementation phases

### P1 — Document model and templates
**Status: Authored; static checks passing**

- [x] Establish canonical paths and stable document identifiers.
- [x] Establish per-level schemas, authoring rules, and readiness/approval states.
- [x] Establish ownership, traceability, stale-descendant handling, and scope-proportional skipping.
- [x] Provide templates and an explicit example.
- [x] Add initial structural validator and contract-test source.
- [x] Run and review contract tests through GitHub Actions; fix observed failures.

**Gate:** A brief, specification, component, plan, task, and execution record can be authored consistently without duplicating authority.

### P2 — Core brain infrastructure and validation
**Status: Instructions authored; static validation passing, behavioral verification pending**

- [x] Update `brain-init` instructions to use the feature hierarchy for new projects; behavior tests pending.
- [x] Update `brain-update` instructions to index features and report broken links without rewriting producer-owned content; behavior tests pending.
- [x] Update `brain-init/references/CLAUDE.local.md` with document authority, write ownership, and approval rules.
- [x] Author and execute dependency/reference validator and unit tests in GitHub Actions.
- [x] Run validator tests and introduce structural checks into skill handoffs.
- [x] Preserve existing main-branch, worktree, and context-loading safeguards in skill instructions; [ ] test these behaviors in fresh agents.

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
- [x] Remove old `brain-write-tickets/SKILL.md` and update guides, supporting skills, and tests. No parallel ticket/task generator.
- [x] Preserve `brain-plan` planning tickets as investigation/decision records, not implementation tasks.

**Gate:** Approved component designs yield small, executable, verifiable tasks with real dependencies.

### P5 — Execution ownership and resumption
**Status: Initial skill refactor authored; validation pending**

- [x] `brain-implement`: consume actionable tasks and governing documents; preserve collaborative/guided/autonomous modes.
- [x] Move mutable progress and review evidence out of implementation plans into feature-level `execution.md`.
- [x] Retain review base, branch, worktree, checkpoints, verification, Rulings, Deferred, and design deviations in the new execution template; [ ] verify behavior in agent tests.
- [x] Require re-verification of completed work and source assumptions on resume without silently rewriting approved plans.
- [ ] Behavior-test the resumption process.
- [x] Preserve direct implementation without five documents in skill instructions; [ ] behavior-test proportionality.

**Gate:** A multi-session task run resumes from code and evidence, not checked boxes alone.

### P6 — Docs and reference cleanup
**Status: Revised bundled guides; further review pending**

- [x] Update bundled `README.md`, `USAGE.md`, `CLAUDE.local.md`, and `brain-update/references/templates.md` to describe the new hierarchy.
- [x] Update principal guides and example links to agree with the new skills; fresh-agent behavior verification remains pending.
- [x] Update skill-local templates, builder-review prompts, subagent handoffs, and explicit bundled-file paths.
- [x] Remove obsolete shared-plan storage descriptions in primary guides and key skill references.
- [x] Provide an illustrative end-to-end `StartMachine` worked example with ADR links, failure cases, and requirement-to-task traceability (`brain-init/references/start-machine-example.md`). It does not claim implemented TCP behavior.

**Gate:** Installed guides and skill contracts agree on paths and authority.

### P7 — Skill behavior tests and regression
**Status: Static CI passing; fresh-agent behavior tests still pending**

- [x] Add H1–H11 behavior scenario definitions (not yet executed).
- [ ] Execute RED/GREEN scenarios in fresh agents.
- [x] Validate IDs, dependencies, cycles, parent approval, requirement lineage, coverage, and direct-parent hash mismatches; structural stale-approval detection has regression tests.
- [x] Allow independent specifications without inferred unrelated parents; reject requirement-bearing descendants without parents and malformed non-sequence metadata.
- [x] Execute 47 static contract tests, fixture setup verification, and StartMachine structural validation in GitHub Actions (`Brain static contracts`, passing at `1c5c55d`).
- [x] Add `tests/build_hierarchical_fixture.py` and `tests/prepare_hierarchical_scenario.py` so H1–H11 have isolated, reproducible Git repositories, prompts, invalid references, independent approval scopes, a real localized bug, and worktree scenarios.
- [ ] Dispatch fresh agents for H1–H11 with RED/GREEN comparisons and grade observed behavior against scenario criteria.
- [ ] Check trivial-change bypass, worktree/branch safety, execution resume, and no unapproved architectural decisions.
- [ ] Exercise `StartMachine` end to end: idea → brief → specs → components → plans → tasks → verified implementation.
- [x] Run existing `experimental_v4` static contract tests through GitHub Actions.
- [ ] Run fresh-agent regression scenarios.
- [ ] Distinguish tests actually run from planned/unverified tests.

**Gate:** Evidence demonstrates the redesigned workflow and important existing guarantees.

## Implementation order and change boundaries

Work in order P1 → P2 → P3 → P4 → P5 → P6 → P7, but write focused tests alongside each phase. Do not let lower-level documents override approved upstream requirements or ADRs. Escalate consequential user decisions; routine reversible implementation choices remain with the agent. When changing an approved parent, flag affected descendants for revalidation and reapproval as appropriate.

## Definition of done

Five document types have explicit contracts, the new `brain-decompose` exists, `brain-write-tickets` is replaced by `brain-write-tasks`, technical plans and mutable execution records have separate owners, structural and behavioral validation pass, the complete `StartMachine` scenario works, and small work can still bypass unnecessary stages. No legacy feature-layout support is required.

## Current verification and integration limitations

The branch contains the five-stage document hierarchy, `brain-decompose`, the renamed `brain-write-tasks`, updated producers and review prompts, and separate `execution.md` ownership. A worked StartMachine example documents illustrative ADR and failure-path mappings; no real server code has been implemented. GitHub Actions executes Python static contract tests and the StartMachine structural fixture. Static CI passed at `1c5c55d` (47 Python contract tests, fixture construction for H1–H11, and StartMachine structural validation). The validator now lives in `brain-init/scripts/`, making it available when the individual skill directories are installed; all producer skills have instructions for preserving approved-parent fingerprints. The fixture builder and scenario preparer are executed in GitHub Actions, but **no fresh AI agents have been dispatched** for scenarios H1–H11 in this session. The GitHub connector does not expose an agent runner. They remain necessary to validate that agents actually respect approvals, worktree safety, document ownership, progressive decomposition, resume behavior, and proportionality. A passing structural fixture does **not** demonstrate that StartMachine was implemented. `tests/AGENT_TESTING.md` contains the fixture preparation command and grading instructions for a future interactive agent test run.
