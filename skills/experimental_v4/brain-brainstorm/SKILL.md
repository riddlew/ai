---
name: brain-brainstorm
description: Resolve consequential product and architecture decisions with the user through dependency-ordered questions and evidence-based recommendations, investigating discoverable facts independently. Use when a requested feature or change has unclear behavior, scope, or design direction that should be settled before writing a specification or code.
---

# Brainstorm

Help the user settle a sound direction. Investigate facts yourself, recommend, and let the user decide consequential choices (root `CLAUDE.md`). Do not implement or change production code while brainstorming.

## 1. Map the decision space

Establish the objective, the relevant existing behavior, and decisions the user has already made. Use code, tests, documentation, `CONTEXT.md`, and ADRs to answer factual questions.

Track every question in a decision table:

| ID | Decision | Status | Depends on | Resolution |
|---|---|---|---|---|
| D1 | Who owns the outbound connection | Investigate | — | — |
| D2 | Behavior when the connection drops mid-send | User decision | D1 | — |

Statuses:

- **Established** — decided by the user or an applicable project record. Resolution states the choice, its essential rationale, and its source.
- **Investigate** — a fact answerable from the repository, documentation, tooling, or an experiment.
- **User decision** — a consequential choice about requirements, behavior, tradeoffs, or architecture.
- **Deferred** — a routine, reversible implementation detail left to implementation.

Mark assumptions as unverified until investigated or accepted. Do not convert your own preferences into requirements.

## 2. Decide which questions matter

A question is a **User decision** when its answer could materially change:

- required behavior, scope, user experience, or failure semantics;
- component responsibilities, ownership, or lifecycle;
- state management, concurrency, persistence, or public contracts;
- dependencies, deployment, or other hard-to-reverse choices;
- substantial implementation complexity or maintenance obligations.

A proposal to introduce a manager, service, layer, or other component that takes over an existing responsibility is an architectural decision, not a routine detail.

Mark ordinary method boundaries, naming, local helpers, and speculative extension points as **Deferred** rather than asking about them.

## 3. Investigate facts yourself

Resolve **Investigate** rows from source, tests, configuration, documentation, and tools. Do not ask the user what the repository can answer ("Which component owns the connection?"); you may ask whether they want to *change* it. Facts can eliminate options but do not settle subjective tradeoffs. If an investigation is blocked, say what is unknown and why.

## 4. Generate options

For each **User decision** whose dependencies are resolved:

1. Load the lens for each area the decision touches, from `${CLAUDE_SKILL_DIR}/lenses/`:
   - `architecture.md` — ownership, lifecycle, dependency direction, reversibility
   - `data.md` — schema, migration, consistency, idempotency
   - `contracts.md` — API versioning, error contracts, compatibility
   - `failure.md` — retries, partial failure, concurrency

   Load none when no lens fits.
2. State the forces: the requirements and constraints any option must satisfy, and the evidence the lens directs you to gather.
3. Evaluate **preserving the current design** against those forces. Include it as an option when viable; otherwise state explicitly which requirement it cannot satisfy.
4. Add only genuinely different alternatives. Drop variants of the same idea and options that fail a stated force.

## 5. Ask in dependency order

Ask one to three independent questions whose prerequisites are resolved, starting with the decisions that carry the most risk or unblock the most work. Never ask a dependent question before its prerequisite. Batch more only if the user asks.

For each question:

1. Number and title it to match its decision-table ID.
2. Explain why it matters now and what evidence is known.
3. Present the options, with the complexity or risk each introduces.
4. Give a provisional recommendation grounded in the requirements and forces.
5. Wait for the user's choice before marking it **Established**.

Example:

**D1 — Connection ownership**

The session currently owns the service connection (`src/session.py:42`). New communication could stay in `Session`, or ownership could move to a separate manager. A manager adds another lifecycle boundary; I found no current requirement for connection lifetime to differ from session lifetime.

- **A. Extend `Session`** — fewer moving parts; existing ownership preserved.
- **B. Introduce a connection manager** — justified only if connections must outlive or be shared across sessions.

**Recommended:** A, based on current evidence. Do you want to keep session ownership?

Never phrase a recommendation, common pattern, or inferred intention as an approved decision.

## 6. Update after each answer

Update the table: an answer may resolve or eliminate decisions, add new ones, or contradict an assumption. If the user's choice appears technically unsound, explain the concrete concern and alternatives; do not substitute your preferred design.

Publish the decision table **at most once per response**, and only when something changed since the last published table. Show the rows that changed.

Stop asking when every consequential decision needed for the next stage is **Established**. Do not prolong the discussion to settle **Deferred** details or hypothetical future requirements.

## 7. Confirm the direction

Present the final summary in this format, which `brain-write-spec` consumes:

```markdown
## Direction: <feature>

**Behavior and scope:** <intended behavior and what is in scope>
**Non-goals:** <explicit exclusions>

### Decisions

| ID | Decision | Status | Depends on | Resolution |
|---|---|---|---|---|
<every row>

**Relevant facts:** <existing responsibilities and constraints, with locations>
**Blocking open decisions:** <User decision rows that block the next stage, or "None">
**Deferred to implementation:** <Deferred rows, or "None">
```

Ask the user to confirm the direction before treating it as established. If it was already confirmed in the discussion, do not ask again. Do not begin implementation without authorization.
