---
name: domain-modeling
description: Maintain project domain vocabulary (CONTEXT.md), context boundaries (CONTEXT-MAP.md), and ADRs for approved, hard-to-reverse decisions. Use when design work establishes or changes the meaning of a domain term, a context boundary, or an approved architectural decision that should be recorded.
---

# Domain Modeling

Maintain domain vocabulary, context boundaries, and durable architecture decisions when design work genuinely changes them. This skill records **established meaning and approved decisions**; it does not approve new architecture (root `CLAUDE.md`) or modify production code.

Do not invoke it merely to read existing terminology, document a routine helper, or diagram implementation modules.

## 1. Locate authoritative context

- If root `CONTEXT-MAP.md` exists, use it to find the relevant context's `CONTEXT.md`.
- Otherwise, if root `CONTEXT.md` exists, treat the repository as one documented context.
- If neither exists, do not manufacture a model. Create root `CONTEXT.md` only when a project-specific concept has been established and preserving it has a practical benefit.

Find the relevant context by **domain responsibility and meaning**, not source directories. Multiple modules, services, or teams do not imply multiple contexts. Ask the user only when choosing the owner resolves an important ambiguity.

Consult relevant root and context-local `docs/adr/`, existing specifications and reviews, code, and tests. Distinguish documented intent from observed behavior and proposals.

## 2. Develop meaningful concepts

For each domain concept:

1. Clarify what it means, what belongs and does not belong, and how it differs from neighboring concepts.
2. Identify invariants and relationships; test a proposed definition against real boundary cases and near-misses.
3. Reconcile established names, aliases, and ambiguous terms; keep familiar vocabulary when its meaning is sound.
4. Check implementation evidence and surface contradictions, without silently redefining the domain to match code or changing code to match a proposal.
5. Confirm any consequential new definition, canonical term, ownership choice, or boundary with the user unless it was already approved.

Routine wording that faithfully records an established concept needs no new approval.

## 3. Maintain `CONTEXT.md`

One `CONTEXT.md` per established context, answering: **What does this term mean in this domain?** Record the context's subject, concise definitions, and discouraged alternatives only when they prevent likely confusion. Prefer meaning and identity over class names, design rationale, temporary requirements, and speculative generalization.

```markdown
# Fulfillment

Owns the domain meaning of preparing and dispatching confirmed orders.

## Shipment

Goods assigned to one delivery movement.

Avoid: `Delivery Batch`

## Package

A physical handling unit within a Shipment.
```

Do not mirror the codebase's classes or services as a glossary, and update terminology only when it matters to current work.

## 4. Maintain `CONTEXT-MAP.md`

Create a root map when **multiple approved contexts** exist and readers need their boundaries. For each context record its responsibility, the path to its `CONTEXT.md`, and material handoffs or shared meanings. Do not duplicate the glossaries.

A context is a boundary of domain meaning or responsibility, not necessarily a deployment unit, package, or team. Introducing, splitting, merging, removing, or reassigning a context is a consequential decision.

```markdown
# Context Map

## Catalog
Vocabulary: `catalog/CONTEXT.md`
Owns product definitions.

## Ordering
Vocabulary: `ordering/CONTEXT.md`
Owns purchase intent and submitted-order lifecycle.

## Boundary Notes
Ordering uses Catalog product identities but owns the order's commercial snapshot.
```

## 5. Record approved decisions as ADRs

Write an ADR only when all hold:

1. The user approved the choice, or it is already an authoritative project decision.
2. Credible alternatives existed, and a future maintainer could reasonably decide differently from the code alone.
3. Reversal would require meaningful coordination, compatibility work, migration, or structural disruption.

Do not write ADRs for ordinary design choices, configuration, easily reversed refactors, or speculative flexibility. For example, choosing which context owns order pricing may warrant an ADR; adding a small helper does not.

Place system-wide ADRs in root `docs/adr/` and context-owned ADRs in `<context>/docs/adr/`, never both. Use `NNNN-short-slug.md` with the next available number (`0001` if empty).

```markdown
# <Approved Decision>

## Context
The actual constraints and situation.

## Decision
What was selected and its scope.

## Rationale
Why this option was chosen over meaningful alternatives.
```

Add consequences, alternatives, status, and references only when useful. Separate user-stated rationale from evidence-based implications; do not invent agreement or reasoning. Preserve superseded ADRs and link a new, approved superseding ADR instead of rewriting history.

## 6. Persist and report

Update only the relevant glossary, map, or ADR, and preserve unrelated records. A recommendation from `brain-review-architecture`, a prototype, or a brainstorm proposal is not approval; use the user's actual choice.

Report which files changed and any decision left open. If the work only applies existing language, no artifact is needed.
