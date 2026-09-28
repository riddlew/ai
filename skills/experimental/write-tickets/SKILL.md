---
name: write-tickets
description: Convert an established plan, specification, or discussion into small implementation tickets with explicit dependencies and acceptance criteria. Use when the user requests implementation tickets or another skill delegates an established plan for ticket generation.
---

# Write Tickets

Create an implementation ticket set from decisions that have already been established.

The goal is to produce the smallest practical increments that deliver complete, verifiable behavior while making dependencies between increments explicit.

## Build the delivery model

Start from the current conversation and any source material the user identifies.

If a referenced file or document contains the requirements, read the relevant material completely before decomposing the work.

Inspect the repository when your current understanding is insufficient to determine how the requested behavior fits the existing system.

While doing so:

- use domain vocabulary from root `CONTEXT-MAP.md` and the relevant context's `CONTEXT.md`, otherwise root `CONTEXT.md`
- follow relevant ADRs in root `docs/adr/` and the relevant context's `docs/adr/`
- identify existing testing patterns and system boundaries
- notice structural changes that would make the requested work substantially easier or safer

Do not ask the user for facts that can be determined from the project itself.

## Identify capabilities

Describe the requested result as a set of independently observable capabilities.

For each capability, determine the minimum change that can make it work completely.

A ticket should normally cross whatever technical boundaries are required to deliver that behavior. Database, backend, frontend, configuration, and tests belong in the same ticket when they exist only to support the same increment.

A useful ticket should:

- produce a complete observable result
- be independently demonstrable or verifiable
- include the validation necessary to establish that it works
- be small enough for an agent to implement with a fresh context window

Avoid dividing work solely by implementation layer.

If preparatory restructuring is necessary before a capability can be implemented cleanly, represent that work separately and make the affected capability depend on it.

## Construct the dependency graph

Determine which tickets genuinely require other tickets to be completed first.

Do not create dependencies merely because one ticket happens to be numbered earlier.

A ticket with no prerequisite work is immediately actionable.

Prefer independent branches when multiple capabilities can be developed separately.

Number tickets so that prerequisites precede the tickets that depend on them.

## Handle cross-cutting changes safely

Some changes affect too much shared code to form an independently valid behavioral increment.

For these cases, design a staged migration that preserves a usable system between steps.

Typically this means:

- introducing a compatible new form without immediately removing the old one
- migrating affected consumers in manageable groups
- removing compatibility support only after nothing depends on the old form

Choose migration groups according to natural project boundaries and the size of the affected area.

Represent each independently manageable migration stage as its own ticket and encode the required dependencies between them.

If intermediate migration groups cannot be independently validated, include whatever final integration and verification work is necessary to establish the complete working state.

## Review before writing files

Present the proposed ticket set to the user before creating anything.

For each ticket show:

- **Title**
- **Depends on**
- **Outcome**

`Outcome` should state what becomes working or verifiable when the ticket is complete.

Ask the user to review whether:

- the tickets are appropriately sized
- the declared dependencies are genuine prerequisites
- any work should be combined or broken apart differently

Revise the model until the user approves it.

## Materialize the approved tickets

After approval, create one Markdown file per ticket under:

`docs/tickets/<feature-slug>/issues/<NN>-<slug>.md`

Start numbering at `01`.

Each file must represent exactly one ticket.

Use this format:

```markdown
# <NN>: <Ticket title>

## Outcome

Describe the complete behavior or result this ticket must deliver.

## Dependencies

List the ticket numbers and titles that must already be complete.

If there are no prerequisites:

None.

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
```

Acceptance criteria should describe observable behavior or verifiable outcomes rather than implementation steps.

Keep ticket descriptions durable. Do not include source-file paths or code excerpts that are likely to become outdated during implementation.

A small prototype artifact may be preserved when it expresses an already-established design decision more precisely than prose, such as a schema shape, state model, reducer structure, or type definition. Include only the decision-relevant portion and note that it came from a prototype.

The finished ticket set should make it clear both what can be worked on now and what becomes available after each prerequisite is completed.
