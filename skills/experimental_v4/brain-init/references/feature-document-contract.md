# Feature document contract

This file is the **single reference** for the hierarchy produced by the Brain skills. Each stage narrows an intention without granting itself authority to change requirements or architecture.

## Structure and purpose

Within `.brain/features/<feature-slug>/`:

| Level | Directory | Owns / answers |
|---|---|---|
| 1 — Brief | `01-brief/` | Why, desired outcome, scope, success |
| 2 — Specifications | `02-specifications/` | What behavior and contracts must hold |
| 3 — Components | `03-components/` | Which functional pieces collectively satisfy the specifications |
| 4 — Implementation Plans | `04-implementation-plans/` | How to realize each component in the inspected codebase |
| 5 — Tasks | `05-tasks/` | Which concrete, verifiable actions carry out the plans |
| Execution (outside levels) | `execution.md` | Actual progress, evidence, review, blockers, and deviations |

Other project brain material retains its purpose: root knowledge documents and `state.md`; durable architectural decisions under `adrs/`; cross-session unresolved planning in `planning/`; reviews, source maps, branch pending changes, and domain knowledge. They are **not additional composition levels**.

## Frontmatter (minimal YAML subset)

Every level document begins with metadata:

```yaml
---
id: CMP-002
kind: component
status: approved
parents:
  - SPEC-001
requirements:
  - SPEC-001#REQ-003
  - SPEC-001#REQ-004
depends_on: []
parent_hashes: [SPEC-001@<40-char Git blob hash>]
---
```

- `id`: stable, unique **within this feature**, with prefix `BRF`, `SPEC`, `CMP`, `PLAN`, or `TASK` and three decimal digits (`SPEC-001`). Never reuse an ID. Use the feature path to distinguish IDs from other features.
- `kind`: `brief`, `specification`, `component`, `implementation-plan`, `task`, matching the containing numbered directory.
- `status`: `draft`, `approved`, or `needs-revision`. A document can be approved only by the user when its required approval gate applies; a mere draft or a passing lint check is not approval.
- `parents`: IDs of upstream documents that provide authority. A brief has `[]`. Direct/short workflows may skip intermediate levels; a parent must be at a **strictly higher** (earlier) level. No cross-feature parents; reference shared ADRs by path in the body.
  A specification with independently established requirements may have `parents: []` even if a separate brief exists within the same feature; earlier unrelated documents do not create an implicit parent. A component, plan, or task claiming requirements must identify at least one explicit governing parent, including when intermediate levels are intentionally skipped.
- `requirements`: qualified requirements like `SPEC-001#REQ-003`. An `E1` example is addressed as `SPEC-001#E1`. Keep applicable references in downstream docs, and state explicitly when no behavior requirement applies.
- `depends_on`: IDs of prerequisite documents **of the same kind/level** (most useful for tasks); no self-dependencies or cycles. Use only genuine execution/production prerequisites, not mere preferred order.
- An `approved` child cannot depend on a parent whose status is `draft` or `needs-revision`. A component, plan, or task may only attribute requirements defined by its governing parents. Stable requirement IDs declared inside a specification must be unique.
- `parent_hashes`: Git-blob SHA-1 fingerprints of each direct parent document, written as `PARENT-ID@<40 hex chars>`, with `[]` for root briefs. Approved documents MUST capture every direct parent, and the structural validator rejects a changed parent even if its status was not updated. The producer generates these from the actual files after their parent is approved. Run `python ${CLAUDE_SKILL_DIR}/../brain-init/scripts/validate_feature_docs.py --show-parent-hashes <child-file>` to print the exact value before approval. Recompute only after checking the changed parent and explicitly renewing affected approvals; never update hashes to suppress a conflict.
- Lists are YAML block sequences or `[]`. No custom YAML tags, anchors, aliases, or hidden metadata magic. IDs and reference values are bare strings.

For a brief, use `parents: []`, `requirements: []`, `depends_on: []`, and `parent_hashes: []`. For a spec with a brief, use `parents: [BRF-001]` (or an equivalent block sequence); it declares requirements in its body. Components can have multiple specification parents. Plans can have multiple component parents when needed. Tasks can use one or multiple approved plan parents.

Document filenames are human-readable and may change; **IDs and explicit references are authoritative**. Task filenames may include ID for readability, e.g. `TASK-001-add-message-discriminator.md`.

## Behavioral identifiers and traceability

Specifications define `REQ-001`, `REQ-002`, etc., and numbered concrete examples `E1`, `E2`, etc. A requirement is scoped by its specification (`SPEC-001#REQ-001`), not global to the brain. Every downstream document includes the applicable requirement refs in metadata and names the relevant examples or verification evidence in its body. Do not duplicate entire specifications in components or tasks.

**Coverage gate:** At a completed stage, every in-scope approved requirement must be attributed to a descendant at that stage (unless an explicit, approved scope exclusion or deliberate bypass is recorded). Multiple descendants may satisfy one requirement, but overlapping ownership must be intentional and clear. An incomplete stage is `draft`, not approved. Do not mark a stage complete solely because every ID appears somewhere; validate meaning as well as references.

A review should be able to trace a verified task back through its plan, component, specification, and brief where those levels exist.

## Status, authority, and updates

- Brief/specification: user-approved intent and expected behavior are normative. Applicable ADRs and `09_user_decisions.md` remain authoritative for their approved decisions. Recorded current source/code facts describe what exists, not what ought to exist.
- Component: functional decomposition and ownership of requirement *coverage*, not permission to introduce an architectural service or new behavior.
- Implementation Plan: agreed technical design. Binding choices require approval; example signatures marked `Illustrative` remain flexible.
- Task: execution contract derived from approved plans; it cannot quietly change their meaning.
- Execution record: **facts and evidence** about work, not a competing normative specification.
- On a material approved parent change, mark affected approved descendants `needs-revision` until reviewed; unrelated branches of the feature may proceed. Never silently approve a revised binding design.
- If authoritative records conflict without a superseding approved decision, record the conflict and consult rather than inventing precedence.
- Evidence-based completeness: implementation checks actual tests, relevant source, diffs, and review outcomes; a checked box is not proof.

## Producer ownership

| Path | Owner |
|---|---|
| `01-brief/` | `brain-brainstorm` (or user-authored material accepted as a brief) |
| `02-specifications/` | `brain-write-spec` |
| `03-components/` | `brain-decompose` |
| `04-implementation-plans/` | `brain-blueprint` |
| `05-tasks/` | `brain-write-tasks` |
| `execution.md` | `brain-implement` |
| Root brain knowledge, `adrs/`, `sources/`, `knowledge/` | `brain-update` (initialized by `brain-init`) |

`brain-update` may index and report problems with producer-owned files, not silently edit them. `brain-plan` owns its separate `planning/` records and calls the appropriate producer when the objective is ready.

## Proportionality

Do not generate filler documents or insist on passing through all five folders. For a small, settled change, direct implementation is valid. For a modest feature, spec → implementation plan → task can be valid. If a level is omitted, links point to the actual governing documents rather than fabricated placeholders. Avoid decomposition into individual lines of code; tasks should be coherent, independently verifiable actions.

## Structural validation (initial implementation)

Run from the repository root with Python 3.10+:

```bash
python skills/experimental_v4/brain-init/scripts/validate_feature_docs.py .brain/features --check-coverage
python -m unittest discover -s skills/experimental_v4/tests -p 'test_feature_document_contract.py'
```

The validator checks required metadata, document kinds, stable IDs, parent level ordering, same-level dependencies, cycles, qualified requirement references and approved child-to-parent fingerprints. A feature folder may be absent before the first feature is documented; do not require empty placeholder directories. With `--check-coverage`, every **fully approved populated** downstream stage must cover all requirements declared by approved specifications through approved documents; stages containing draft/needs-revision documents are incomplete and do not claim full coverage. Skipped stages are permitted. These are structural checks only; human/agent review remains necessary for semantic coverage and correctness. The tests are authored; runtime execution in a checked-out repository remains pending.
