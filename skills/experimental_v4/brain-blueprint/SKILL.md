---
name: brain-blueprint
description: Collaboratively design and approve concrete code-level implementation plans for approved feature components before implementation.
disable-model-invocation: true
---

# Blueprint — Implementation Plans

**Mechanical plan creation:** Use `sh "${CLAUDE_SKILL_DIR}/../brain-init/scripts/brain-tool" doc new --kind plan` for newly approved-scope design work (the generated document remains `draft`); populate its actual technical design and inspected SHA. Use `validate --show-parent-hashes` to calculate fingerprints without silently changing approved documents. See `${CLAUDE_SKILL_DIR}/../brain-init/references/deterministic-tooling.md` for the command contract, preview/authorization safeguards, and runtime fallbacks.


**Project brain:** Follow `CLAUDE.local.md` project-brain loading, branch context, decision authority, and source verification rules. Read the shared feature-document contract and templates from `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-contract.md` and `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-templates.md`.

Define **how** approved functional components will be implemented in the inspected codebase. Preserve approved requirements, architecture, and explicit design preferences. This skill owns only `.brain/features/<feature-slug>/04-implementation-plans/`. `brain-implement` owns mutable `execution.md`; do not record task completion or execution status here. For small settled changes, a separate blueprint is optional.

## 1. Establish the boundary

1. Read approved component documents, their governing specifications and examples, the brief when present, applicable ADRs, confirmed user decisions, and existing implementation plans. For a simpler workflow without components, use the directly governing approved specification or request.
2. Classify binding requirements, approved architectural and technical decisions, illustrative ideas, and unresolved consequential questions. A suggested method signature is not automatically binding.
3. Inspect current source: owners, callers, interfaces, data flow, lifecycle, integration points, tests, and conventions. Check branch and git status, including relevant uncommitted work.
4. Record `Design inspected at: <full HEAD SHA>` and relevant dirty-worktree assumptions. This is **not** `Review base`; `brain-implement` records that separately before editing production code.
5. Ask for user code-design preferences only when they remain open and matter. Investigate repository facts yourself.

## 2. Define smallest viable design

Use `${CLAUDE_SKILL_DIR}/references/blueprint-template.md` and feature document schema. Prefer one implementation plan per meaningful component, but permit one plan to cover several small related components or multiple plans for a genuinely large component. Never create files just to satisfy a one-to-one rule.

Describe:

- Intended change and explicitly unchanged behavior/ownership.
- Existing files and verified responsibilities; proposed changes and rationale.
- Important interfaces, signatures, control/data flow, state and failure paths.
- Compatibility, migration, verification strategy, and test boundaries where applicable.
- Binding design constraints and their approvals/sources versus illustrative or proposed details.
- Small coherent testable increments and governing qualified requirement/example IDs.
- Genuine dependencies, assumptions, and blockers.

Favor extending existing owners over unapproved services, new layers, premature abstraction, or speculative generality. Do not decide product semantics here. If existing architecture cannot satisfy the spec, explain the conflict and obtain approval before establishing a new binding design.

## 3. Review with the user

Present the affected files/owners, call flow, key signatures, unchanged boundaries, testable increments, and real tradeoffs. Invite design corrections. Review the complete plan against code and governing requirements, following the builder review in `${CLAUDE_SKILL_DIR}/../brain-review-code/references/builder-review.md` (`artifact_kind: blueprint`, `sources: component/specification and inspected paths`). If no independent reviewer exists, label it as a weaker self-review.

Before approval, populate the plan's `parent_hashes` with current fingerprints for its directly governing components/specifications using `${CLAUDE_SKILL_DIR}/../brain-init/scripts/validate_feature_docs.py --show-parent-hashes <plan-file>`. Reconcile any changed parent semantics before recording approval.

Ask explicitly for approval of the revised **binding technical design**. Without approval keep `status: draft` or `needs-revision`; do not implement. A specification approval or feature request is not blueprint approval. On approval set `status: approved`, record when/where approval occurred, and distinguish illustrative implementation suggestions from binding constraints.

## 4. Persist and hand off

Store the design at `.brain/features/<feature-slug>/04-implementation-plans/<plan-slug>.md`, using stable `PLAN-<NNN>` IDs, valid `parents` pointing to component IDs (or an earlier governing level if skipped), qualified `requirements`, and genuine same-level `depends_on`. Reuse a plan for the same technical responsibility; do not create duplicates.

Do not write `execution.md`, rewrite component/spec files, or reset task status. If an approved binding design is revised, mark affected plans `needs-revision` until reapproved, and flag descendant tasks for revalidation by their owner. Routine illustrative refinements can be recorded in the execution deviation log.

Invoke `brain-update` after writing or materially revising plans; it may index and report but not rewrite producer-owned documents. Report plan paths and IDs, approval state, blockers, and next authorized step. Recommend `brain-write-tasks` for a substantial plan; direct `brain-implement` may be appropriate for a small, settled change.
