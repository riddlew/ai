---
name: write-tickets
description: Turn an approved plan, specification, or discussion into small verifiable implementation tickets with genuine dependencies and explicit user approval of the proposed decomposition.
---

# Write Tickets

Convert established requirements into the **smallest practical set of independently verifiable delivery increments**. Tickets describe authorized outcomes and constraints; they do not give the assistant permission to settle unresolved product behavior or redesign the architecture.

Use this skill **only when** the user requests tickets, or when a long-running workflow delegates ticket generation for independently deliverable work. Do not treat every specification as requiring tickets; direct implementation is preferable when the feature fits one coherent session. Follow root `CLAUDE.md` for decision authority.

## 1. Establish the evidence and decision boundary

Read the relevant conversation, approved planning material, specifications, and other referenced sources fully enough to preserve their intent. Inspect the repository where needed to determine how the work fits its current architecture.

Read applicable domain records and architectural decisions:

- root `CONTEXT-MAP.md` and relevant context `CONTEXT.md`, otherwise root `CONTEXT.md`;
- relevant ADRs under root `docs/adr/` and the owning context's `docs/adr/`;
- relevant existing tests, verification patterns, and public boundaries.

Keep separate:

- **Approved requirements and decisions:** binding inputs to ticket writing.
- **Repository facts:** evidence about how the system works today.
- **Recommendations:** possible implementation approaches, not approved constraints.
- **Open choices:** decisions that require the user's judgment.

Do not ask the user for discoverable repository facts. Do not infer approval from a suggested implementation, planning discussion, architecture review, or working code.

## 2. Identify independently observable capabilities

Describe the agreed result as complete capabilities. Each ticket should normally:

- deliver one coherent, observable, independently verifiable behavior;
- cross database, backend, UI, configuration, and test layers where needed to complete that behavior;
- be small enough for a fresh agent context;
- include verification consistent with the approved specification and current project testing patterns;
- avoid functionality that was not requested or approved.

Do not split tickets merely by implementation layer. Do not manufacture a large ticket set for a small feature. If one ticket merely restates the specification and creates no coordination value, recommend implementing from the specification directly instead of creating tickets.

## 3. Preserve approved architecture during decomposition

Use existing responsibility owners, code paths, and architectural decisions as the starting hypothesis. Ticket planning may identify a real impediment to that approach, but **cannot approve a structural change by decomposing it into a preparatory ticket**.

For example, do not automatically create `Extract ConnectionManager` before a ticket that extends communication in `Session`. First establish the concrete problem that cannot reasonably be solved within `Session`. Then explain the alternatives and seek approval if moving ownership is consequential.

**Consult the user before adding tickets that would:**

- move or divide meaningful lifecycle, state, or domain ownership;
- introduce a new manager, service, layer, or significant dependency;
- change established interfaces, persistence formats, or externally observable behavior;
- require an unapproved migration or broad restructuring;
- choose unresolved product semantics, scope, or architecture.

Present the observed constraint, the minimal approach within existing architecture, any larger option, tradeoffs, and a recommendation. Wait for the user's decision. Routine ticket sizing and local implementation details do not require separate approval.

## 4. Construct genuine dependencies

Add a dependency only when a ticket cannot reasonably deliver its outcome until another has been completed. Do not make independent capabilities serial merely because one ticket has a lower number.

If an **approved** cross-cutting migration is required, stage it so intermediate states remain valid when practical:

1. introduce a compatible mechanism when necessary;
2. migrate consumers in coherent, verifiable groups;
3. remove compatibility support after all dependents are migrated.

Create migration tickets only for work that is actually needed and authorized. Do not propose compatibility layers or generalized interfaces without concrete migration requirements.

Number tickets in dependency-consistent order, without treating numbering itself as a dependency.

## 5. Obtain approval for the ticket set

Before creating files, present the proposed set with:

- **Title** — the coherent behavioral increment.
- **Depends on** — genuine prerequisite tickets, or none.
- **Outcome** — what becomes observable or verifiable after the ticket.
- **Architectural implications** — any consequential changes needing explicit approval, or a statement that existing boundaries are preserved.

Ask the user to review the decomposition, dependencies, and proposed scope. Revise until they approve it. If the user already supplied and approved the exact decomposition, do not request redundant confirmation. **Approval of the ticket set does not automatically approve an architectural decision that was neither disclosed nor established.**

Do not request a separate user decision for every routine test case or implementation detail.

## Implementation progress is separate from ticket definition

Tickets define approved outcomes, dependencies, and acceptance criteria. They are **not** a session log and do not need to track every intermediate coding step.

When `implement` begins work on a ticket set, it creates or resumes **one feature-level** `docs/implementation/<spec-file-stem>/todo.md` if there is a governing spec, or `docs/implementation/<ticket-feature-slug>/todo.md` otherwise. That file records **current execution status**, references tickets by path, and identifies the next unblocked item. It must not duplicate their complete acceptance criteria. `guidance.md` in the same directory is optional and stores useful current implementation discoveries, not new requirements or unapproved architecture.

**Do not create or update `todo.md` or `guidance.md` while merely writing tickets.** This avoids a task tracker that claims implementation has started before it has. Preserve the ticket files as stable definitions; execution progress belongs to `todo.md` once work starts. If a newly approved design decision changes ticket scope, update the authoritative specification/tickets as needed rather than silently changing only implementation notes.

## 6. Write approved tickets

After approval, create exactly one Markdown file per ticket under:

```text
docs/tickets/<feature-slug>/issues/<NN>-<slug>.md
```

Start numbering at `01`. Check for existing files and avoid overwriting unrelated work; when continuing an existing ticket set, respect the project's established numbering and update behavior.

Use:

```markdown
# <NN>: <Ticket Title>

## Outcome

<One complete capability or verifiable result.>

## Dependencies

<Prerequisite ticket numbers/titles, or None.>

## Acceptance Criteria

- [ ] <Observable or objectively verifiable result>

## Governing Decisions

<Reference the applicable approved specification, planning result, or ADR.
Include only essential boundaries not readily recoverable from those sources.>
```

The Governing Decisions section may be omitted when sources and constraints are already unmistakable from the ticket set's context. Acceptance criteria should derive from established requirements and describe results rather than coding steps.

Keep implementation tickets durable. Prefer references to authoritative specifications and ADRs over copying their full content. Do not embed volatile source-file paths or implementation snippets unless an approved prototype fragment is needed to preserve a particular design contract.

If a consequential decision remains unresolved, don't write a ticket that silently assumes one answer. Record the block, consult the user, and resume once the decision is made.

Report the created ticket paths, actionable tickets, and remaining genuine dependencies or blockers. Do not begin implementation unless it is separately authorized.
