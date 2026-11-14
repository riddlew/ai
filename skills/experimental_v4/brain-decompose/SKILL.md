---
name: brain-decompose
description: Decompose approved specifications into coherent functional components with complete, traceable requirement coverage before code-level design.
disable-model-invocation: true
---

# Decompose into functional components

**Project brain:** Follow `CLAUDE.local.md` for project-brain loading, branch context, source verification, and decision authority. Read the feature-document contract and templates in the sibling `brain-init/references/` directory.

Translate approved specifications into **coherent functional responsibilities**, not code. Specifications govern required behavior; applicable ADRs and approved user decisions govern architectural decisions. Own only `.brain/features/<feature-slug>/03-components/`. Do not edit specifications, plans, tasks, production code, or the execution record.

## 1. Establish the scope

1. Read the governing approved specifications, all `REQ-` and `E` identifiers, any brief, applicable planning results, ADRs, decisions, and glossary entries.
2. Distinguish binding requirements, verified codebase facts, consequential open decisions, and routine implementation discretion.
3. Inspect relevant code when it helps identify existing ownership. Existing code is evidence about current behavior, not authority to change the required behavior.
4. If a small feature has no useful functional subdivision, recommend direct blueprinting or implementation instead. Do not generate filler documents.

## 2. Identify components

1. Account for every approved in-scope requirement, success behavior, failure path, and invariant.
2. Group related behaviors into cohesive **functional components**, each with an observable responsibility and verifiable result. A component need not correspond to a class, module, service, or software layer.
3. Preserve established ownership and approved architecture. Do not invent preparatory refactoring, abstractions, or changes to interfaces or persistence.
4. Describe interactions, shared contracts, and genuine dependencies. Avoid splitting by backend/frontend/database/test layers unless there is independent functional meaning.
5. When decomposition would require a consequential new ownership boundary, contract, or behavior, present evidence and options and ask the user rather than silently approving a redesign. Leave only affected scope blocked.

## 3. Write component documents

Write `.brain/features/<feature-slug>/03-components/<slug>.md`, using the shared `feature-document-templates.md`. Assign stable IDs `CMP-001`, `CMP-002`, ... within the feature. Required frontmatter:

```yaml
---
id: CMP-001
kind: component
status: draft
parents: [SPEC-001]
requirements: [SPEC-001#REQ-001]
depends_on: []
---
```

Use actual governing specification IDs in `parents`, and qualified requirement IDs in `requirements`. List only real same-level dependencies. Each document includes:

- Functional responsibility and observable result.
- Governing requirements and examples.
- Scope, boundaries, interactions, and exclusions.
- Open decisions and blockers.
- Acceptance or verification expectations.

Do not duplicate entire specifications or prescribe method names, file changes, or code designs. Reuse existing component documents and IDs on revision; avoid duplicate ownership.

## 4. Validate and review

Construct a requirement coverage table for **every approved in-scope requirement**. Multiple components may reference a requirement only with clear division of responsibility. Check invariants and failure behavior semantically, not only by counting references. Validate metadata, references and cycles using `scripts/validate_feature_docs.py` when available; structural coverage is not proof of semantic correctness.

Present the proposed component set, scope boundaries, coverage table, and consequential open decisions. Ask for approval. Do not label an unapproved design as `approved`; keep blocked scope `draft`. If a governing specification changes materially, review affected components and mark changed approvals `needs-revision` until reaffirmed. Independent approved scope can proceed.

## 5. Persist and hand off

Write only component documents, then invoke `brain-update` to update indexes without modifying producer-owned files. Report IDs, paths, coverage, approval status and blockers. Recommend `brain-blueprint` for codebase-aware technical design. Do not create implementation tasks or edit production code.
