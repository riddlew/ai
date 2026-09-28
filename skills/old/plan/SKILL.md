---
name: plan
description: Interactively turn investigation findings and user input into an approved design and executable implementation plan. Use after investigation and before implementation to resolve uncertainty, compare approaches, select a vertical slice, and create bounded tasks without guessing user intent.
argument-hint: "[issue-id or work-item] [optional: alternatives|decision|vertical-slice|pattern-review] [context]"
---

# Plan

Turn an evidence-backed investigation into an approved design and the executable contract that the implementation skill will follow. Resolve material uncertainty through collaborative questions; do not guess what the user wants or modify source code.

Use `$ARGUMENTS` as the work item plus additional design or planning context, priorities, constraints, and requested boundaries.

## Result Artifact

Before planning, locate the nearest project `.claude/` directory from the working directory up to the repository root. Do not use the personal `~/.claude/` directory.

- If no project `.claude/` directory exists, ask the user where to save the result before continuing. Do not create `.claude/`, choose another location, or skip the artifact without their answer.
- Resolve the work-item directory as `.claude/results/<ISSUE-ID>/` from an explicit ticket or issue ID. Without one, use the matching existing work-item directory; if none exists, ask which work item to plan.
- Read `01-investigation.md` as the primary input. Recheck important claims and assumptions against current repository state. If required investigation evidence is missing or stale, stop and request investigation rather than planning around it.
- Write or update `02-plan.md`. Keep status **draft** while questions or design decisions remain, change it to **design-approved** after explicit approval of the design, and mark it **ready** only after explicit approval of the task plan.
- Put the work-item key, stage, status, updated date, repository revision or working-tree state, and input artifact paths in YAML frontmatter. Put the ordered tasks, dependencies, evidence, assumptions, and unresolved issues in the body.
- Report the artifact path and readiness status to the user.

## Clarification Gate

Do not select a design or draft the task sequence until the user's intent is precise enough to avoid material assumptions.

1. Read the investigation, current repository evidence, and `$ARGUMENTS` before asking questions.
2. State briefly what the investigation establishes and what still needs clarification for design or task planning.
3. Research questions that the repository, configuration, or authoritative documentation can answer. Ask the user only for intent, priority, acceptable tradeoffs, or information unavailable from evidence.
4. Ask one focused question per message. Prefer concrete multiple-choice options when they clarify a real decision, lead with a recommendation and its reason, and allow the user to supply a different answer.
5. Probe vague or consequential answers with another single question. Cover every issue that could change scope, task boundaries, ordering, compatibility, migration, rollout, validation, documentation, or the completion condition.
6. Never convert silence, ambiguity, or an unanswered question into a default. Record it under **Open Questions** and keep the plan **draft**.
7. After each answer, record the resolved decision and its source in the draft artifact. If an answer conflicts with an already approved design section, expose the conflict and request approval to reopen that decision.
8. Continue until no material planning uncertainty remains. Routine implementation details supported by repository conventions are evidence, not user decisions; cite that evidence in the plan.

The questioning should be proportional to the task, but the no-guessing rule and both approval gates always apply.

## Design Phase

1. Confirm the investigation supplies acceptance criteria, constraints, relevant code evidence, and material unknowns.
2. Identify decisions that are costly to reverse or affect public contracts, stored data, security boundaries, concurrency, dependencies, or downstream consumers.
3. Compare two or three realistic approaches when meaningful. Evaluate them against correctness, complexity, maintainability, compatibility, migration cost, operational risk, repository fit, and verification cost.
4. Recommend one option when evidence makes it materially better. Label it as proposed until approved.
5. Select the smallest end-to-end vertical slice that tests the riskiest architectural assumption. Avoid speculative infrastructure and premature abstraction.
6. Review the first instance of any public interface, persistence format, ownership model, inheritance hierarchy, shared-state mechanism, or reusable abstraction before it spreads.
7. Define the implementation boundary: allowed components and behavior changes, invariants, compatibility requirements, validation expectations, non-goals, and stop conditions.
8. Present the proposed design in manageable sections and ask for explicit approval. Revise affected sections when requested.
9. After explicit approval, record approved, deferred, and open decisions and change `02-plan.md` to **design-approved**. Do not begin task decomposition before this gate.

## Task Planning Phase

1. Ask further one-at-a-time questions when task boundaries, priorities, sequencing, rollout, validation, documentation, or completion conditions remain unclear.
2. Extract the approved outcome, vertical slice, constraints, invariants, non-goals, validation requirements, stop conditions, and resolved user decisions.
3. Decompose the slice into the smallest coherent tasks that can be implemented and reviewed independently.
4. For each task specify:
   - outcome and observable behavior;
   - affected files, symbols, or components when repository evidence supports them;
   - allowed behavior changes and preserved invariants;
   - tests or reproducible baseline required before implementation;
   - implementation dependencies and ordering constraints;
   - risks and likely scope-conflict triggers;
   - exact or discoverable validation commands;
   - concrete completion condition.
5. Order tasks by dependency and architectural risk. Preserve the approved vertical slice before generalized infrastructure.
6. Keep repository facts separate from user decisions. Do not leave planning assumptions hidden; resolve them or list them as blocking open questions. Assign confidence to uncertain file or symbol mappings.
7. Define when implementation must stop and return to investigation or planning. A change to the approved design reopens the design approval gate.
8. Present the complete task plan and ask for explicit approval. If the user requests changes, revise the artifact and re-present the affected sections.
9. Only after explicit approval, record the plan approval in the artifact and change status to **ready**.

If task planning exposes a new expensive-to-reverse decision, incompatible requirement, or necessary scope expansion, return `02-plan.md` to **draft**, record the conflict, and reopen the applicable questions and design approval.

## Optional Review Gate

The user may run `code-review`, `architecture-review`, or `security-review` against `02-plan.md` before implementation. When revising the plan after review:

- read the applicable review artifacts;
- address or explicitly defer each material finding;
- preserve approved design decisions unless the user explicitly reopens them;
- record the review artifacts as inputs;
- present the revision and restore **ready** only after explicit user approval and when no blocking finding remains. If a finding changes the approved design, return to **draft** and repeat both applicable approval gates.

## Output

Write one artifact containing the approved design followed by an ordered implementation plan with a stable identifier for each task. Include:

- design alternatives, recommendation, tradeoffs, and approval;
- selected vertical slice and implementation boundary;
- dependency order;
- shared invariants;
- validation sequence;
- unresolved issues and deferred work;
- implementation stop conditions;
- resolved decisions and any blocking open questions;
- plan approval and readiness status.

Do not implement tasks, invent user preferences, infer either approval, or mark the work item verified.
