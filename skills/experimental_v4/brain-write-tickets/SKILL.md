---
name: brain-write-tickets
description: Decompose an approved specification, plan, or discussion into small, independently verifiable implementation tickets with genuine dependencies, after the user approves the proposed set. Use when the user asks for tickets, or approved work spans multiple sessions or independently deliverable increments.
---

# Write Tickets

Convert established requirements into the **smallest practical set of independently verifiable delivery increments**. Follow root `CLAUDE.md`: tickets describe authorized outcomes and cannot settle unresolved behavior or approve a redesign.

Use this skill only when the user requests tickets or a long-running workflow delegates ticket generation. If one ticket would merely restate the specification, recommend implementing from the specification directly.

## 1. Gather the evidence

Read the relevant conversation, approved planning material, specifications (including their Examples), and referenced sources fully enough to preserve their intent. Read applicable `CONTEXT-MAP.md` / `CONTEXT.md`, relevant ADRs, existing tests, verification patterns, and public boundaries.

Keep separate:

- **Approved requirements and decisions** — binding inputs.
- **Repository facts** — how the system works today.
- **Recommendations** — possible approaches, not constraints.
- **Open choices** — decisions requiring the user.

## 2. Identify independently observable capabilities

Each ticket should:

- deliver one coherent, observable, independently verifiable behavior;
- cross database, backend, UI, configuration, and test layers as needed to complete it;
- fit in a fresh agent context;
- verify consistently with the specification and project testing patterns;
- add nothing unrequested.

Do not split by implementation layer or manufacture a large set for a small feature.

## 3. Preserve approved architecture

Use existing owners, code paths, and decisions as the starting hypothesis. Decomposition cannot approve a structural change by turning it into a preparatory ticket; an "Extract X" ticket ahead of work that could extend the existing owner needs a demonstrated reason and the user's approval.

Consult the user before adding tickets that would:

- move or divide lifecycle, state, or domain ownership;
- introduce a new manager, service, layer, or significant dependency;
- change established interfaces, persistence formats, or observable behavior;
- require an unapproved migration or broad restructuring;
- choose unresolved product semantics, scope, or architecture.

Present the constraint, the minimal approach within existing architecture, any larger option, tradeoffs, and a recommendation; wait for the decision.

## 4. Construct genuine dependencies

Add a dependency only when a ticket cannot deliver its outcome until another is complete. Do not serialize independent capabilities.

Stage an **approved** cross-cutting migration so intermediate states stay valid: introduce a compatible mechanism, migrate consumers in verifiable groups, then remove compatibility support. Do not propose compatibility layers or generalized interfaces without concrete migration requirements.

Number tickets in dependency-consistent order; numbering itself is not a dependency.

## 5. Obtain approval for the set

Before creating files, present each proposed ticket with:

- **Title** — the behavioral increment.
- **Depends on** — genuine prerequisites, or none.
- **Outcome** — what becomes observable or verifiable.
- **Examples covered** — specification example IDs, when a specification exists.
- **Architectural implications** — consequential changes needing approval, or "existing boundaries preserved".

Revise until the user approves. If the user already supplied and approved the exact decomposition, do not ask again. Approval of the set does not approve an architectural decision that was neither disclosed nor established.

## 6. Write approved tickets

Create one file per ticket at `docs/tickets/<feature-slug>/issues/<NN>-<slug>.md`, numbering from `01`. When continuing an existing set, follow its numbering and do not overwrite unrelated files.

```markdown
# <NN>: <Ticket Title>

## Outcome

<One complete capability or verifiable result.>

## Dependencies

<Prerequisite ticket numbers and titles, or None.>

## Acceptance Criteria

- [ ] Satisfies specification examples E1–E3 (`docs/specs/<NN>-<slug>.md`, Examples).
- [ ] <Observable result not covered by a specification example.>

## Governing Decisions

<References to the approved specification, planning result, or ADR.
Include only essential boundaries not recoverable from those sources.>
```

**Acceptance criteria reference specification Examples by ID** instead of restating them. Add a criterion only for behavior the Examples do not cover. Without a specification, write each criterion as an observable result derived from established requirements. Describe results, not coding steps.

Omit Governing Decisions when the sources are unmistakable from context. Do not embed volatile source paths or implementation snippets unless an approved prototype fragment preserves a design contract. If a consequential decision is unresolved, do not write a ticket that assumes an answer; record the block and consult.

Tickets are stable definitions; `brain-implement` tracks execution progress separately once work starts.

Report the created ticket paths, actionable tickets, and remaining dependencies or blockers. Do not begin implementation unless separately authorized.
