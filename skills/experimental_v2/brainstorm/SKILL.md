---
name: brainstorm
description: Collaboratively resolve consequential product and architecture decisions, investigating facts independently and deferring routine implementation details.
---

# Brainstorm

Help the user define a sound direction without treating the assistant's preferred design as an approved decision.

Follow the project decision-authority policy in root `CLAUDE.md`. In this skill, the user owns consequential requirements and architecture decisions; the assistant investigates facts and recommends alternatives.

Do not implement the feature or make production-code changes during brainstorming.

## 1. Establish the decision space

Understand the objective, existing relevant behavior, and decisions the user has already made. Inspect available repository code, tests, documentation, context records, and ADRs when they can answer factual questions.

Maintain a lightweight dependency graph of relevant questions and decisions. Track each item as one of:

- **Established:** explicitly decided by the user or supported by an applicable established project decision.
- **Fact to investigate:** answerable from the repository, documentation, tooling, or an experiment.
- **Decision for the user:** a consequential choice about requirements, priorities, behavior, tradeoffs, or architecture.
- **Deferred detail:** a routine, reversible implementation choice that does not need agreement during brainstorming.

Record important assumptions as **unverified** until investigated or explicitly accepted. Do not convert the assistant's inferred preferences into requirements.

## 2. Decide which questions matter

A question warrants user consultation when its answer could materially change:

- required behavior, scope, user experience, or failure semantics;
- component responsibilities, ownership, or lifecycle;
- state management, concurrency, persistence, or public contracts;
- dependencies, deployment, or other difficult-to-reverse choices;
- substantial implementation complexity or future maintenance obligations.

In particular, **a proposal to introduce a manager, service, layer, or other component that takes over an existing responsibility is an architectural decision**, not a routine implementation detail. Explain and discuss it rather than assuming approval.

Do **not** manufacture questions about ordinary method boundaries, naming, local helpers, or speculative extension points. Such details can remain open for implementation unless they have a consequential effect.

Do not assume that the current architecture is necessarily optimal. Treat it as evidence and a starting point. Reconsider it when a concrete problem justifies doing so, but obtain the user's decision before adopting a material change.

## 3. Investigate facts without interviewing the user

Determine discoverable facts from available source files, tests, project configuration, documentation, and tools. If a factual investigation is blocked, say what is unknown and why.

Do not ask questions like "Which component owns the connection?" when the repository can answer them. You may need to ask whether the user *wants to change* that ownership; that is a different, subjective question.

Facts may rule out options, but they do not independently authorize subjective tradeoffs.

## 4. Ask consequential questions in dependency order

Identify decisions whose prerequisites are resolved. Prioritize the ones that unblock the most important work or pose the largest risk.

Ask a small, focused batch—normally one to three independent questions—rather than exhausting every theoretically available choice. Never ask a dependent question until its prerequisite has been resolved. Batch more questions only if the user asks for that style.

For each question:

1. Give it a number and concise title.
2. Explain why the decision matters **now** and what evidence is known.
3. Present realistic options, including preserving the current design when viable.
4. Recommend one option **provisionally**, based on actual requirements and tradeoffs.
5. Explain what complexity or risk each meaningful option introduces.
6. Wait for the user's choice before treating the decision as settled.

Example:

**Question 1 — Connection ownership**

The session currently owns the service connection. New communication could remain in `Session`, or ownership could move to a separate manager. The new manager would add another lifecycle boundary; I have not found a current requirement that needs it.

- **A. Extend `Session`** — fewer moving parts, existing ownership preserved.
- **B. Introduce a connection manager** — justified if connection lifetime or sharing must be independent of sessions.

**Recommended:** A, based on the current evidence. Do you want to retain session ownership?

Never phrase a recommendation, common design pattern, or inferred intention as an already approved decision.

## 5. Reevaluate after each answer

Update the decision graph. An answer may resolve or eliminate questions, reveal new dependencies, or contradict an assumption.

If the user's choice appears technically unsound, explain the concrete concern and alternatives; do not quietly substitute your preferred design. Resolve disagreements with the user before establishing the direction.

Stop asking questions when all **consequential decisions required for the next stage** are resolved. Do not prolong the discussion to settle routine implementation details or hypothetical future requirements.

## 6. Confirm the resulting direction

Summarize:

- the intended behavior and scope;
- decisions the user approved, with their essential rationale;
- relevant facts and existing responsibilities;
- explicit non-goals;
- remaining uncertainties, separating **blocking decisions** from **deferred implementation details**.

Ask the user to confirm the direction before promoting a proposal to an established decision. Do not begin implementation without authorization. When a direction was already confirmed in the discussion, preserve that approval instead of asking again.
