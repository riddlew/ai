---
name: domain-modeling
description: Refine project-specific domain language, context boundaries, and durable approved architectural decisions without turning proposals into authority.
---

# Domain Modeling

Maintain the project's domain vocabulary, context boundaries, and durable architecture decisions when active design work genuinely changes them. Follow root `CLAUDE.md` for decision authority. This skill records **established meaning and approved decisions**; it does not independently approve new architecture or modify production code.

Do not invoke merely to read existing terminology, document a routine helper class, or generate diagrams for implementation modules.

## 1. Locate authoritative context

Inspect existing documentation before proposing changes:

- If root `CONTEXT-MAP.md` exists, use it to find established contexts and the relevant context's `CONTEXT.md`.
- Otherwise, if root `CONTEXT.md` exists, treat the repository as one documented domain context.
- If neither exists, do not manufacture a model. Create root `CONTEXT.md` only when a project-specific concept has actually been established and preserving it has a practical benefit.

Find the relevant context from **domain responsibility and meaning**, not merely source directories. Ask the user only when choosing the owner would resolve an important ambiguity. Multiple modules, classes, services, or teams do not automatically imply multiple domain contexts.

Consult relevant root `docs/adr/` and context-local `docs/adr/`, existing specs/reviews, current code, and tests as needed. Distinguish documented intent from observed behavior and proposals.

## 2. Develop meaningful concepts

For each actual domain concept:

1. Clarify what it means, what belongs and does not belong, and what distinguishes it from neighboring concepts.
2. Identify meaningful invariants and relationships. Use real boundary cases, including near-misses or cross-context interactions, when needed to test a proposed definition.
3. Reconcile established names, aliases, and ambiguous terms. Preserve familiar vocabulary when its meaning is sound.
4. Inspect implementation evidence where relevant. Surface contradictions without silently redefining the domain to match code or rewriting code to match a proposal.
5. Confirm any consequential new definition, canonical term, ownership choice, or boundary with the user **unless it was already approved** in the originating discussion or artifact.

Routine wording that faithfully records an established concept needs no new approval. Never promote an agent recommendation, candidate architecture, or unverified inference to a settled domain decision.

## 3. Maintain `CONTEXT.md`

Use one `CONTEXT.md` per established domain context. It should answer: **What does this term mean in this domain?**

Record the context's subject matter, concise definitions of established concepts, and discouraged alternatives only when they prevent likely confusion. Prefer meaning and identity over implementation details, design rationale, class names, temporary requirements, and speculative generalization.

Example:

```markdown
# Fulfillment

Owns the domain meaning of preparing and dispatching confirmed orders.

## Shipment

Goods assigned to one delivery movement.

Avoid: `Delivery Batch`

## Package

A physical handling unit within a Shipment.
```

Do not create or expand glossaries just to mirror a codebase's classes or services. Update accepted terminology when it matters to current work, rather than generating incidental documentation churn.

## 4. Maintain `CONTEXT-MAP.md`

Create a root map when **multiple approved domain contexts** exist and readers need to understand their boundaries. For each context, record its responsibility, the path to its `CONTEXT.md`, and material handoffs or shared meanings with other contexts. Do not duplicate the glossaries.

A context is a boundary of domain meaning or responsibility, not necessarily a deployment unit, service, package, or team. Introducing, splitting, merging, removing, or changing context ownership requires a consequential domain decision under `CLAUDE.md`.

Example:

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

## 5. Record significant approved decisions as ADRs

An architectural decision record is appropriate only when:

1. The user has approved the choice, or it is otherwise an established authoritative project decision.
2. Credible alternatives existed, and a future maintainer could reasonably decide differently from inspecting the resulting code alone.
3. Reversal would involve meaningful coordination, compatibility, migration, or structural disruption.

Do **not** write ADRs for every design choice, ordinary configuration, easily reversed refactor, or speculative flexibility. For example, connection ownership may warrant an ADR if its reversal would affect multiple contracts or lifecycle guarantees; introducing one small helper normally does not.

Place system-wide ADRs in root `docs/adr/`; place context-owned ADRs in `<context>/docs/adr/`. Do not duplicate them at multiple levels. Inspect the selected directory and assign `NNNN-short-slug.md` using the next available number (`0001` if empty).

Record at least:

```markdown
# <Approved Decision>

## Context
The actual constraints and situation.

## Decision
What was selected and its scope.

## Rationale
Why this option was chosen over meaningful alternatives.
```

Add consequences, alternatives, status, and references only when useful. Separate user-stated rationale from evidence-based implications; do not invent agreement or reasoning. Preserve superseded ADRs as history and link to a new, approved superseding ADR rather than retroactively rewriting earlier choices.

## 6. Persist without changing design authority

After a choice is established, update only the relevant glossary, map, or ADR. Check consistency and preserve unrelated records. A recommendation in `review-architecture`, a prototype, or a brainstorm proposal does not qualify as approval by itself; use the user's actual choice.

Report which files changed and any decision left open. If the work only applies existing domain language and makes no durable change, no new artifact is required.
