---
name: plan-feature
description: Manage large or uncertain feature-planning efforts as persistent, dependency-aware planning tickets under docs/planning/.
---

# Plan Feature

Use this skill when a planning effort is too large or uncertain to resolve in one session.

Store persistent planning state under:

```text
docs/planning/<feature-stub>/
├── INDEX.md
└── <ticket-files>.md
```

This skill owns:

- planning state
- scope
- planning-ticket decomposition
- ticket dependencies
- cross-session continuation
- downstream planning updates
- handoff to implementation-ticket generation

It does not own the detailed interactive decision process for `consult` tickets. Delegate those to `brainstorm`.

Plan by default. Do not implement the final objective unless the planning material explicitly authorizes execution.

## Start

Planning may begin from:

- a new idea supplied by the user;
- relevant context from the current conversation;
- a linked planning or specification file.

First establish the **final objective**. Use it to determine what is in scope.

Then determine whether the entire effort can reasonably be resolved in one large session.

If it can:

- do not create a planning directory;
- stop and ask the user how they want to proceed.

Otherwise create:

```text
docs/planning/<feature-stub>/
```

Use a concise, stable feature stub.

## INDEX.md

`INDEX.md` is the canonical high-level state of the planning effort.

Use this structure:

```markdown
# <Planning effort>

## Objective

The final destination or outcome.

## Notes and Constraints

Persistent preferences, assumptions, constraints, and cross-cutting context.

## Resolved Tickets

Short summaries with links to resolved planning tickets.

## Open Areas

In-scope areas that are not yet precise enough to become tickets.

## Out of Scope

Work explicitly outside the final objective.
```

Keep `INDEX.md` concise.

Detailed questions, investigations, prototypes, reasoning, and resolutions belong in ticket files.

Do not duplicate detailed ticket resolutions in `INDEX.md`.

Anything beyond the final objective belongs in **Out of Scope**, not **Open Areas**.

## Planning tickets

Create a ticket as soon as a question or prerequisite can be stated precisely, even when it is currently blocked.

Each ticket must:

- represent exactly one decision, investigation, prototype question, or prerequisite task;
- be small enough for one large agent session;
- declare its type, status, and dependencies;
- contain its detailed work and eventual resolution.

Use numbered filenames such as:

```text
001-storage-model.md
002-error-behavior.md
003-ui-prototype.md
```

Each ticket must contain YAML frontmatter:

```yaml
---
ticket-tag: consult
status: unresolved
depends-on: []
---
```

### Ticket tags

`ticket-tag` must be exactly one of:

- `research` — investigate external or project-local facts required before another decision can be made.
- `prototype` — create the smallest artifact needed to evaluate concrete behavior or appearance with the user.
- `consult` — resolve a bounded decision interactively with the user. Use this by default when no other type is more appropriate.
- `task` — perform prerequisite work required before a later decision can be made. It must not simply implement the final objective.

### Status

Use:

- `unresolved`
- `resolved`
- `excluded`

### Dependencies

List prerequisite ticket filenames or identifiers in `depends-on`.

A ticket is actionable only when:

1. its status is `unresolved`; and
2. every ticket in `depends-on` is `resolved`.

Blocked tickets remain part of the plan.

Dependencies must represent genuine prerequisites rather than arbitrary ordering.

## Resolve tickets

Resolve at most one non-research ticket per session.

Independent `research` tickets may be investigated in parallel when they do not depend on one another.

Do not use parallel work to resolve multiple human decisions, prototypes requiring separate user evaluation, or prerequisite tasks in the same session.

### Research

For a `research` ticket:

- investigate the required external or project-local facts;
- use available files, repository content, documentation, tools, or environment rather than asking the user for discoverable facts;
- record the findings and their planning implications in the ticket.

Independent research tickets may run in parallel.

### Consult

For a `consult` ticket, invoke the `brainstorm` skill.

Provide it only the decision space relevant to the selected ticket, including:

- the ticket question;
- applicable constraints;
- relevant resolved dependencies;
- necessary planning context.

The `brainstorm` skill owns the interactive decision-resolution process.

Do not allow the delegated brainstorm to expand into unrelated planning tickets or attempt to resolve the entire feature.

After the user confirms the resulting decision:

1. record the detailed resolution in the planning ticket;
2. mark the ticket `resolved`;
3. update `INDEX.md`;
4. reevaluate downstream planning.

Never invent the user's preferences, priorities, requirements, or tradeoff decisions.

### Prototype

For a `prototype` ticket:

- create only the minimum artifact needed to evaluate the ticket's question;
- present it to the user for evaluation when human judgment is required;
- record the resulting decision in the ticket.

A prototype ticket remains unresolved until its required evaluation is complete.

Prototype artifacts are planning aids and do not authorize production implementation.

### Task

For a `task` ticket:

- perform only prerequisite work needed to make a later planning decision possible;
- record the result and any implications for dependent tickets.

A `task` must not merely implement part of the final objective.

## Continue an existing plan

Treat the planning directory as persistent state across sessions.

Do not reconstruct earlier decisions from memory when planning files already exist.

When continuing:

1. Read `INDEX.md`.
2. If the user selected a ticket, use that ticket.
3. Otherwise choose the first actionable ticket by ticket number.
4. Read that ticket.
5. Load related ticket files only when needed for dependencies or context.
6. Resolve the selected ticket according to its `ticket-tag`.
7. Record the detailed result in the ticket.
8. Set its status to `resolved`.
9. Add a short linked summary under `INDEX.md` → `Resolved Tickets`.
10. Reevaluate downstream planning.
11. Create, update, remove, or reclassify tickets as required by the result.

Do not duplicate the detailed resolution in `INDEX.md`.

## Evolve the plan

Keep uncertain future work in `INDEX.md` → `Open Areas` only while it cannot yet be expressed as a precise ticket.

When an open area becomes precise:

1. create the necessary ticket or tickets;
2. establish their dependencies;
3. remove the corresponding material from `Open Areas`.

A resolution may reveal that planned work is unnecessary, differently scoped, or better represented by other tickets. Update the planning graph accordingly.

If an existing ticket is later determined to be outside the final objective:

- set its status to `excluded`;
- do not treat it as a resolved planning decision;
- record the exclusion under `INDEX.md` → `Out of Scope`;
- update dependent tickets as necessary.

## Execution boundary

This skill is planning-first.

Do not implement the final objective merely because the design is sufficiently detailed.

Production implementation is allowed only when the planning material explicitly opts into execution.

The following remain valid planning activities without such authorization:

- investigation required by a `research` ticket;
- prerequisite work required by a planning `task`;
- minimal artifacts required by a `prototype`.

None of these implicitly authorize implementation of the final objective.

## Implementation handoff

Planning tickets and implementation tickets are separate.

Continue planning unless the user asks to turn the established plan into implementation tickets.

When the user requests implementation tickets:

1. Check whether any unresolved planning decision materially affects implementation.
2. If material decisions remain unresolved, continue planning rather than inventing them.
3. Otherwise invoke the `write-tickets` skill using the completed planning material as its source.
4. Let `write-tickets` own implementation decomposition, dependency analysis, acceptance criteria, user review, and creation of `docs/tickets/...`.

Do not duplicate implementation-ticket generation in this skill.

The planning directory remains the authoritative record of planning decisions after implementation tickets are created.