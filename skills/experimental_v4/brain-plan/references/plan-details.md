# Detailed workflow — brain-plan

**Open only for conditional branches described by SKILL.md.** The original full procedure is preserved below; current primary skill and policy govern where both discuss the same rule.


# Plan Feature

**Mechanical planning files:** When multi-session planning is justified, use `sh "${CLAUDE_SKILL_DIR}/../brain-init/scripts/brain-tool" doc new --kind planning-index` and `--kind planning-ticket` to create exactly the needed files and ticket numbering. You still decide questions, dependencies, evidence, and approval. See `${CLAUDE_SKILL_DIR}/../brain-init/references/deterministic-tooling.md` for the command contract, preview/authorization safeguards, and runtime fallbacks.


**Project context (current rule):** Follow `CLAUDE.local.md` §Project brain loading; read core decisions, applicable feature plans, related technical documents and authoritative sources. Search by behavior and source paths, follow links and broaden when uncertain. The old mandatory context-map/full-root instruction is superseded.

Track planning state for substantial or uncertain efforts across sessions. This skill owns planning scope, planning tickets and their dependencies, and cross-session continuation. It delegates interactive decisions to `brain-brainstorm` and executable implementation decomposition to `brain-write-tasks` after approved functional and technical design. Planning tickets remain bounded investigations or decisions, not implementation tasks. Follow `CLAUDE.local.md` for decision authority.

## Boundaries

- **Plan, do not implement.** Bounded investigations, prerequisite tasks, and minimal prototypes are permitted planning work. None of them, nor completed planning, authorizes implementing the final objective.
- **Planning state is not implementation state.** Do not create feature implementation plans, executable tasks, or implementation checklists here. `brain-design-implementation` owns feature-level `04-implementation-plans/`, `brain-write-tasks` owns `05-tasks/`, and `brain-implement` separately owns `execution.md`. The planning directory remains the record of planning decisions.

## Start

1. Establish the **final objective** and known exclusions.
2. Inspect project context as needed to separate known facts from open decisions.
3. Before creating planning tickets, survey the major in-scope uncertainties breadth-first: consequential user decisions, facts to investigate, prototype questions, and prerequisites. Capture questions that can be stated precisely as tickets and less-defined areas under Open Areas. Do not deeply resolve each question during this initial survey.
4. Decide whether the effort warrants multi-session planning. If it can be resolved in one session, do not create a planning directory; use `brain-brainstorm` or `brain-write-spec` instead, without interrupting a straightforward authorized task to ask.

Otherwise create `.brain/planning/<feature-stub>/` with a concise, stable stub:

```text
.brain/planning/<feature-stub>/
├── INDEX.md
└── <NNN>-<ticket-slug>.md
```

## INDEX.md

```markdown
# <Planning effort>

## Objective

The final outcome.

## Notes and Constraints

Confirmed preferences, approved architectural decisions, relevant facts,
and explicitly marked assumptions or caveats.

## Resolved Tickets

Short linked summaries of resolved planning tickets.

## Open Areas

In-scope areas not yet precise enough to become tickets.

## Out of Scope

Work explicitly outside the objective.
```

Keep `INDEX.md` concise; detailed evidence, alternatives, and resolutions belong in tickets. Never label an unverified assumption as an approved constraint. Anything beyond the objective belongs in **Out of Scope**, not **Open Areas**.

## Planning tickets

Create a ticket when a **real, consequential** question or prerequisite can be stated precisely, even if blocked. Do not create tickets for speculative capabilities or routine implementation details.

Each ticket represents one decision, investigation, prototype question, or prerequisite; fits in one large agent session; and records its evidence, options or work, and eventual resolution. Use numbered filenames such as `001-permission-model.md`, `002-expiry-semantics.md`, `003-share-dialog-prototype.md`.

Required frontmatter:

```yaml
---
ticket-tag: consult
status: unresolved
depends-on: []
---
```

**Tags:**

- `research` — investigate project-local or external facts needed for later decisions.
- `prototype` — build the smallest artifact needed to assess a concrete behavior or appearance.
- `consult` — resolve a bounded consequential decision with the user; the default when judgment is required.
- `task` — prerequisite work that makes a later decision possible, never implementation of the objective.

**Status:** `unresolved`, `resolved`, or `excluded`.

**Dependencies:** list prerequisite ticket identifiers in `depends-on`. A ticket is actionable only when it is `unresolved` and all its dependencies are `resolved`. Blocked tickets stay in the plan; never fabricate answers to unblock them.

## Resolve tickets

Default to **one non-research ticket per session** to keep decisions focused. Resolve more in a session only when the user explicitly asks and dependencies permit. Independent research tickets may run in parallel when appropriate; do not use parallel work to settle dependent user decisions or prototype approvals.

- **Research:** investigate with repository files, tests, documentation, tools, and external evidence. Record findings, confidence, and planning implications. Research can eliminate options but cannot decide the user's priorities or approve a boundary.
- **Consult:** invoke `brain-brainstorm` with only this ticket's decision space: the question and why it matters, applicable constraints and decisions, resolved dependencies and evidence, and an explicit boundary excluding other tickets. If a new consequential choice surfaces, resolve it within this ticket when it belongs to the same decision, or record a dependent `consult` ticket. The ticket is resolved only when the user explicitly approves the outcome.
- **Prototype:** produce only the minimum artifact needed to answer the question, present it for evaluation, and record the feedback and decision. It stays unresolved until evaluation is complete.
- **Task:** perform only the prerequisite work and record its result and implications.

After resolving a ticket:

1. Record the outcome in the ticket (for `consult`: the approved decision, alternatives, and rationale).
2. Mark it `resolved`.
3. Add a short linked summary under **Resolved Tickets** in `INDEX.md`.
4. Reevaluate downstream dependencies and open areas.

Then invoke `brain-update` with a one-line summary of what changed.

## Continue an existing plan

Treat the planning directory as authoritative; do not reconstruct decisions from memory.

1. Read `INDEX.md`.
2. Take the user's selected ticket, or else the lowest-numbered actionable ticket.
3. Read that ticket and only the context its dependencies require.
4. Resolve it by tag, using the one-non-research-ticket default unless the user authorizes more.
5. Update the ticket, `INDEX.md`, dependencies, and open areas.
6. Create, change, exclude, or remove tickets only when new evidence or user decisions justify it.

## Evolve the plan

Move an open area into tickets once it can be stated as a meaningful ticket, and remove its open-area note. When a decision makes future work unnecessary, exclude or remove that work.

For a ticket outside the objective: mark it `excluded`, record it under **Out of Scope**, update dependent tickets, and do not count it as an approved resolution.

## Hand off to the hierarchical feature workflow

Review unresolved tickets and Open Areas before handoff; resolve every consequential decision that blocks an unambiguous requirement. Record a feature brief through `brain-brainstorm` when appropriate, then invoke `brain-write-spec` for approved behavior, `brain-decompose-feature` for meaningful functional boundaries, `brain-design-implementation` for code-aware implementation plans, and `brain-write-tasks` for executable tasks when task decomposition adds value. A simple settled change may skip unnecessary levels. Planning tickets in `.brain/planning/` remain investigation/decision records, never executable tasks. Do not authorize implementation merely because planning concluded.
