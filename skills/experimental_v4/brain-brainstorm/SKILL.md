---
name: brain-brainstorm
description: Resolve consequential product and architecture decisions with the user through dependency-ordered questions and evidence-based recommendations, investigating discoverable facts independently. Use when a requested feature or change has unclear behavior, scope, or design direction that should be settled before writing a specification or code.
---

# Brainstorm

**Project brain:** Follow `CLAUDE.local.md` §Project brain loading: read **all** root `.md` files once per session (again after compaction), plus the active branch's pending file when present. Inspect linked detail and verify task-critical facts against current source. Do not send the whole brain to subagents. If no brain exists, proceed and mention `/brain-init` once.

Help the user settle a sound direction. Investigate facts yourself, recommend, and let the user decide consequential choices (`CLAUDE.local.md`). Do not implement or change production code while brainstorming.

## 1. Map the decision space

Establish the objective, the relevant existing behavior, and decisions the user has already made. Use code, tests, documentation, the `.brain` root files, and ADRs in `.brain/adrs/` to answer factual questions.

Track every question in a decision table:

| ID | Decision | Status | Depends on | Resolution |
|---|---|---|---|---|
| D1 | Who owns the outbound connection | Investigate | — | — |
| D2 | Behavior when the connection drops mid-send | User decision | D1 | — |

Statuses:

- **Established** — decided by the user or an applicable project record. Resolution states the choice, its essential rationale, and its source.
- **Investigate** — a fact answerable from the repository, documentation, tooling, or an experiment.
- **User decision** — a consequential choice about requirements, behavior, tradeoffs, or architecture.
- **Deferred** — an internal detail no user of the software can observe, left to implementation.

Mark assumptions as unverified until investigated or accepted. Do not convert your own preferences into requirements.

## 2. Decide which questions matter

A question is a **User decision** when its answer could materially change:

- anything a user of the software can observe: names, arguments, defaults, output, messages, exit codes, ordering, limits, and edge cases;
- required behavior, scope, user experience, or failure semantics;
- component responsibilities, ownership, or lifecycle;
- state management, concurrency, persistence, or public contracts;
- dependencies, deployment, or other hard-to-reverse choices;
- substantial implementation complexity or maintenance obligations.

A proposal to introduce a manager, service, layer, or other component that takes over an existing responsibility is an architectural decision, not a routine detail.

Normally mark internal method boundaries, code names, and local helpers as **Deferred**. **Exception:** when the user deliberately specifies a design pattern, component responsibility, interface, method signature, or code structure, investigate its fit and record the confirmed preference as **Established** rather than discarding it as an implementation detail. A user may also ask to jointly design these details; do not insist they are deferred. Don't raise speculative extension points. Scope comes from the user: ask about a scope edge rather than stating a non-goal they didn't give.

### Cover material behavior

For every **new or materially changed observable behavior**, consider invocation and defaults, success results, applicable failures and unchanged state, boundaries (including empty, duplicates, and limits), and regressions in shared code. Record unresolved consequential choices in the decision table; group cases governed by the same decision instead of asking one question per edge case.

Use current code and tests (`file:line`) to establish existing behavior. Preserve behavior outside the authorized change unless the user chooses otherwise; do not ask the user to reapprove established or unaffected behavior. Flag any adjacent behavior that the proposed change would materially alter. The code establishes what is, not what should be.

### User-directed implementation design

Give the user room to describe **how they want the code to work**: ownership, patterns to use or avoid, existing classes to extend, data flow, and important signatures or method outlines. Ask for these preferences when they materially affect the proposed architecture, but never require the user to specify details they do not care about. Start with the user's preferred design; assess it against actual code, requirements, correctness, and maintenance cost, and explain concrete concerns instead of silently replacing it. Distinguish **binding approved preferences** from tentative ideas and illustrative examples. More detailed code design may be explored later through `/brain-blueprint`.

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

### Visual companion

When the next **User decision** you will ask is about something the user will look at, offer a browser tab before you present its options. That means a screen or page layout, or a visual design, where the options would look different from each other. Requirements, behavior, scope, tradeoffs, ownership, and text or data formats a code block can show stay in text.

- Make the offer a message of its own, with nothing else in it: "This might be easier if I show you. Want me to open a browser tab with some mockups?" Other ready questions wait a turn.
- Offer it only if `node --version` works.
- Start nothing and write nothing before the user accepts. If they decline, stay in text and don't offer again unless they raise it.
- If they accept, read `${CLAUDE_SKILL_DIR}/references/visual-companion.md` and follow it.
- Record what they choose in the decision table, like any other answer.
- Stop the server when the browser is no longer needed, and at the latest when you confirm the direction (§7).

## 6. Update after each answer

Update the table: an answer may resolve or eliminate decisions, add new ones, or contradict an assumption. If the user's choice appears technically unsound, explain the concrete concern and alternatives; do not substitute your preferred design.

Publish the decision table **at most once per response**, and only when something changed since the last published table. Show the rows that changed.

When every row is **Established** or **Deferred**, ask: "Is there anything else about how this should behave, or should I write up the direction?" Keep asking until the user says to write it up. If the user tells you to stop earlier, stop: each unanswered question stays an open decision, never a default. Don't settle **Deferred** details or hypothetical future requirements.

## 7. Confirm the direction

Present the final summary in this format, which `brain-write-spec` consumes:

```markdown
## Direction: <feature>

**Behavior and scope:** <intended behavior and what is in scope>
**Non-goals:** <exclusions the user stated, or "None stated">

### Changes

- <behavior>: <current behavior with `file:line`, or "new"> → <new behavior>. Why: <the user's reason, or the requirement it serves>

**Unchanged (confirm only if affected):** <materially affected existing behaviors that the direction explicitly preserves, or "None">
**Assumptions (confirm):** <everything in this direction the user didn't answer, or "None">

### Decisions

| ID | Decision | Status | Depends on | Resolution |
|---|---|---|---|---|
<every row>

**Relevant facts:** <existing responsibilities and constraints, with locations>
**Blocking open decisions:** <User decision rows that block the next stage, or "None">
**Approved design preferences:** <explicitly confirmed patterns, owners, interfaces, structures, or "None">
**Tentative implementation ideas:** <ideas discussed but not approved, or "None">
**Deferred to implementation:** <Deferred rows only, or "None"; anything observable the user didn't answer goes under Assumptions>
```

Ask the user to confirm the direction, including each **Unchanged** and **Assumptions** line, before treating it as established. If it was already confirmed in the discussion, do not ask again. Do not begin implementation without authorization.

Once the user confirms the direction, it is established. Preserve confirmed technical preferences in the summary for `brain-write-spec`, and suggest `/brain-blueprint` for a collaborative code-level design after the spec. A tentative signature or pattern is not approved merely because Claude proposed it. Then invoke `brain-update` with a one-line summary of what changed.
