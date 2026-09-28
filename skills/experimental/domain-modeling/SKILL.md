---
name: domain-modeling
description: Refine project domain vocabulary, context boundaries, and durable architectural decisions during active design work.
---

# Domain Modeling

Use this skill when design work is changing the project's domain language, context boundaries, context relationships, or durable architectural decisions.

Do not invoke it merely to read or apply terminology that is already established.

## Establish the documentation state

Before changing domain documentation, inspect the repository for its existing domain-model structure.

There are three states:

### Mapped repository

If root `CONTEXT-MAP.md` exists, treat it as a multi-context repository.

Use the map to discover:

- which contexts exist;
- where each context's `CONTEXT.md` lives;
- enough boundary information to identify the context relevant to the current discussion.

Infer the relevant context from the subject being discussed and existing context definitions.

Ask the user only when more than one context remains genuinely plausible.

### Unmapped repository with a glossary

If there is no `CONTEXT-MAP.md` but root `CONTEXT.md` exists, treat the repository as a single domain context.

Use that file as the vocabulary record.

### Repository without domain documentation

If neither file exists, begin with no persisted domain model.

Do not create documentation merely because this skill was invoked.

Once the discussion establishes the first domain concept worth preserving, create root `CONTEXT.md` and treat the repository as single-context unless later design work establishes distinct contexts.

## Develop a domain concept

Work through domain concepts in this order.

### 1. Identify the concept

Determine what real domain idea the discussion is trying to represent.

Separate distinct concepts that are accidentally being discussed as one thing.

Do not add general programming or infrastructure terminology merely because it appears in the implementation.

### 2. Establish its boundaries

Clarify what makes the concept itself rather than merely choosing a name for it.

Determine, where relevant:

- what belongs to the concept;
- what does not;
- what distinguishes it from neighboring concepts;
- which properties must remain true for it to retain its meaning;
- which context owns the meaning.

Use concrete cases to expose unclear boundaries.

### 3. Reconcile vocabulary

Compare the concept with established terminology.

Immediately surface conflicts with the existing glossary.

If several names refer to the same concept, establish one canonical term.

If one name is being used for several different concepts, separate those meanings rather than preserving the ambiguity.

Record discouraged alternatives when they are likely to reappear or cause confusion.

### 4. Validate the model

Test the proposed concept and relationships against concrete scenarios.

Prefer cases that challenge the boundary rather than merely demonstrate the normal path, such as:

- an object that almost qualifies for the concept;
- a case where two terms appear interchangeable;
- a relationship that changes under an unusual condition;
- behavior that crosses a context boundary;
- an existing system case that appears inconsistent with the proposed meaning.

When the discussion describes existing system behavior and relevant code is available, inspect that code.

Surface contradictions between implementation behavior and the proposed domain model.

Do not silently redefine the domain model to match the implementation. Treat the disagreement as something to resolve.

### 5. Persist accepted terminology

As soon as the concept is sufficiently resolved, update its `CONTEXT.md`.

Do not accumulate resolved terminology in conversation and batch the glossary changes later.

Only persist terminology that has actually been established.

## Write CONTEXT.md

`CONTEXT.md` is the durable vocabulary reference for one domain context.

Its purpose is to let a reader understand the concepts people in that domain mean when they use project terminology.

Each file must identify:

- the context;
- what subject matter that context is responsible for;
- its established domain concepts;
- discouraged names where distinguishing them prevents ambiguity.

A useful entry answers:

> What does this term mean in this domain?

Definitions should therefore focus on identity and meaning.

Keep them concise.

Do not use the glossary as a place to explain software construction, design rationale, temporary analysis, or requirement prose. If information exists primarily to explain how the system is built or why a technical choice was made, it belongs elsewhere.

Only include terminology whose meaning is specific to the project's business or problem domain.

Organize concepts according to the domain itself. Related concept families may share a section when that makes the vocabulary easier to understand; otherwise keep the glossary flat.

Example:

```markdown
# Fulfillment

This context describes the domain involved in preparing and dispatching confirmed customer orders.

## Shipment

A collection of goods assigned to one delivery movement.

Avoid: `Delivery Batch`

## Package

A physical handling unit belonging to a Shipment.
```

## Manage multiple contexts

Introduce or maintain `CONTEXT-MAP.md` when the repository has multiple domain contexts.

Its purpose is navigation and boundary comprehension: a reader should be able to determine where a concept belongs and how responsibilities meet across contexts.

For each known context, record enough information to answer:

- What domain responsibility does this context own?
- Where is its vocabulary documented?
- Where does its responsibility meet another context?

Record cross-context relationships when they materially help explain ownership, handoff, dependency, or shared concepts.

Do not duplicate each context's glossary in the map.

When design work establishes a new context or materially changes a context boundary or relationship, update the map as part of that change.

Example:

```markdown
# Context Map

## Catalog

Vocabulary: `catalog/CONTEXT.md`

Owns the meaning and organization of products offered for sale.

## Ordering

Vocabulary: `ordering/CONTEXT.md`

Owns customer intent to purchase and the lifecycle of submitted orders.

## Boundary Notes

Ordering references products defined by Catalog but owns the commercial snapshot recorded on an Order.
```

## Record durable decisions

Use an ADR when preserving the reasoning will materially help future maintainers avoid re-litigating, accidentally undoing, or misinterpreting an important architectural choice.

Before creating one, ask whether the rationale has durable value.

A decision is worth recording when all of these are true:

- future maintainers could reasonably choose differently if they saw only the finished code or structure;
- more than one credible approach was available when the choice was made;
- reversing the choice later would require meaningful migration, coordination, compatibility work, or architectural disruption.

If those conditions are not present, leave the decision out of ADRs.

Routine configuration choices, ordinary implementation details, obvious conventions, and choices that can be changed locally without meaningful consequences do not need decision records.

Decisions that commonly justify durable rationale include situations such as:

- assigning responsibility to one domain context rather than another;
- choosing a communication contract that multiple components must depend on;
- establishing persistence or consistency semantics that shape future design;
- introducing a platform dependency that becomes difficult to remove;
- accepting a significant operational or safety constraint;
- preserving compatibility with an external system at architectural cost;
- choosing one extensibility model while deliberately giving up another.

These are examples, not automatic ADR triggers. Apply the durable-rationale test.

## Place ADRs by ownership

Store each ADR with the architectural scope that owns the decision.

Use root:

```text
docs/adr/
```

when the decision constrains the system as a whole or cannot naturally belong to one domain context.

For decisions owned by one context, place the ADR under that context's:

```text
<context>/docs/adr/
```

Create an ADR directory only when that scope first needs a decision record.

Do not duplicate the same ADR at multiple levels. If a local decision has system-wide consequences, choose the scope whose maintainers need to own the decision.

## Create an ADR

Before writing a new ADR, inspect the chosen `docs/adr/` directory.

ADR filenames use:

```text
NNNN-short-slug.md
```

Determine the number from the directory itself:

1. inspect existing ADR filenames;
2. parse their numeric prefixes;
3. find the highest valid number;
4. assign the next number;
5. use four digits.

If there are no existing ADRs, start at `0001`.

Choose a short slug describing the decision rather than its implementation task.

An ADR must contain enough information for a future maintainer to recover:

- what was decided;
- what situation made the decision necessary;
- why the chosen direction was preferred.

For example:

```markdown
# Separate Ordering and Fulfillment Contexts

## Context

Ordering and physical fulfillment evolve under different business rules, but both initially appeared in the same application boundary.

## Decision

Treat Ordering and Fulfillment as separate domain contexts.

## Rationale

Their ownership, terminology, lifecycle rules, and rate of change differ enough that sharing one model would create ambiguous responsibilities.
```

Add status, alternatives, consequences, or other sections only when they preserve useful decision knowledge.

## Keep records synchronized with design

During an active design discussion:

- persist a resolved term immediately;
- update context boundaries when the model changes;
- update `CONTEXT-MAP.md` when a multi-context relationship or ownership boundary is established or materially changed;
- create an ADR when a newly settled decision meets the durable-rationale policy.

Keep the artifacts separate by purpose:

- `CONTEXT.md` defines domain meaning;
- `CONTEXT-MAP.md` explains domain ownership and boundaries across contexts;
- ADRs preserve the rationale behind consequential architectural choices.

Do not use one artifact as a substitute for another.