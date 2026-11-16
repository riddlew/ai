---
name: brain-write-tasks
description: Decompose approved technical implementation plans into small, verifiable executable tasks with grounded dependencies, requirement coverage, and user-approved task boundaries.
disable-model-invocation: true
---

# Write Tasks

**Mechanical task creation:** Use `sh "${CLAUDE_SKILL_DIR}/../brain-init/scripts/brain-tool" doc new --kind task` to allocate stable IDs, names and initial draft frontmatter. Supply actual governing plan parents and write task actions, examples, and dependencies yourself; script success never grants approval. See `${CLAUDE_SKILL_DIR}/../brain-init/references/deterministic-tooling.md` for the command contract, preview/authorization safeguards, and runtime fallbacks.


**Project brain:** Follow `CLAUDE.local.md` for project brain, decision authority, and source verification. Read `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-contract.md` and `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-templates.md`.

Preserve rigorous coverage, genuine dependency checks, user approval, and builder review while generating **concrete implementation actions** from approved plans, rather than delivery tickets from specifications. Own only `.brain/features/<feature-slug>/05-tasks/`. Do not edit approved implementation plans, upstream documents, execution history, or production code. For one trivial action, direct implementation may be more proportionate.

## 1. Gather governing evidence

Read the approved implementation plans, their component/spec parents, requirement and example IDs, applicable ADRs and decisions, and codebase facts relevant to the plans. Check existing `05-tasks/` documents to preserve IDs. Distinguish binding requirements and technical designs from illustrative snippets, current repository facts, and consequential open decisions. Do not generate tasks that assume a blocked design is approved.

## 2. Produce practical, executable increments

Each task should:

- Implement one coherent bounded technical change contributing to a meaningful verifiable outcome.
- Name intended code change(s), relevant paths/owners where verified, applicable constraints, and expected result.
- Map back to approved plan IDs, qualified requirements, and relevant example IDs.
- Fit in a fresh agent context without inventing missing decisions.
- Define independent meaningful verification (targeted tests, contract checks, or explicit alternative evidence).
- Cross architectural layers when necessary for a coherent outcome; do not automatically split by file/class/layer or individual code statement.
- Have only **genuine** prerequisites; unrelated tasks may run independently.

Do not turn a task into a new architecture decision or introduce changes beyond approved scope. Prefer small behavioral increments within existing ownership and code paths. Architecture or public-contract redesign requires separate approval in governing documents **before** generating affected tasks.

## 3. Draft and review the task set

Create draft task definitions with ID, title, plan parent IDs, requirements, dependencies, precise action, expected behavior, acceptance criteria, and verification. Construct a **coverage table** mapping each approved plan increment, applicable requirement, and example to one or more tasks. Report missing failure cases; add accepted criteria when a requirement resolves them, otherwise record the unresolved user choice.

Self-check: stable unique IDs, valid plan parents, accurate requirement/example refs, no duplicate ownership or scope creep, genuine acyclic dependencies, and no claimed approvals of unresolved design. Run the shared structural validator when available. Run the builder review from `${CLAUDE_SKILL_DIR}/../brain-review-code/references/builder-review.md` with `artifact_kind: task set` and approved plans/specifications as sources. If no reviewer is available, label a weaker self-review.

Present the task set, dependency ordering, coverage table, uncovered failure cases, review result, and genuine questions in one approval message. If the user already approved exactly that decomposition, review and write without a redundant approval unless the review changes it materially.

## 4. Persist approved tasks

Write individual files to `.brain/features/<feature-slug>/05-tasks/TASK-<NNN>-<slug>.md` using the shared task template.

```yaml
---
id: TASK-001
kind: task
status: approved
parents: [PLAN-001]
requirements: [SPEC-001#REQ-001]
depends_on: []
parent_hashes: []
---
```

Each document should include `Action and implementation context`, `Expected behavior / result`, `Applicable design constraints`, `Acceptance criteria and examples`, and `Verification`. Use code paths only when grounded in inspected source; reference the plan rather than duplicate it. Approval of a task set does not authorize code edits without the separately applicable `brain-implement` authorization.

Populate each task's `parent_hashes` with actual approved plan fingerprints using `${CLAUDE_SKILL_DIR}/../brain-init/scripts/validate_feature_docs.py --show-parent-hashes <task-file>` before final approval. Never simply refresh stale hashes to bypass a changed binding plan.

An upstream binding design change may invalidate affected tasks. Mark them `needs-revision` until reconciled and reapproved; preserve IDs and unaffected tasks.

## 5. Handoff

Invoke `brain-update` after creating or materially revising tasks. Report paths, IDs, dependencies, approval status and blockers. Recommend `brain-implement` for authorized execution. Progress, review results, and verification history belong exclusively to `execution.md`.
