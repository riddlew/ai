---
name: brain-review-architecture
description: Discover architectural friction across a codebase, or assess a selected feature, subsystem, design, or boundary, reporting evidence-backed improvements without implementing them. Use when the user asks whether an area's design is sound, where the architecture is making changes expensive, or to evaluate an ownership or boundary decision.
---

# Architecture Review

Find or assess architectural improvements using concrete evidence. Follow root `CLAUDE.md`: a recommendation or selected review topic is not approval to redesign. Do not modify production code.

Choose the mode by **whether the user has selected an area**, not by whether they already know what is wrong:

- **Discovery:** the user wants a search for improvement opportunities and has not selected a feature, file set, subsystem, or boundary. A broad concern ("the architecture is getting hard to maintain") gives direction without defining a focused scope.
- **Focused review:** the user selects a feature, file set, class, subsystem, design, boundary, decision, or previously discovered candidate, with or without a suspected problem.

If the request names specific code, use focused review. Do not run both modes automatically; after discovery, let the user select a candidate for focused review.

## Shared evidence rules

Establish the user's goal, known use cases, relevant owners and interfaces, constraints, and non-goals. Read applicable `CONTEXT-MAP.md`, the relevant `CONTEXT.md` (or root `CONTEXT.md`), and relevant ADRs; treat an existing ADR as intentional unless current evidence supports reconsidering it.

Inspect code, tests, callers, dependencies, configuration, and change history only to the depth required. Separate verified facts, established choices, hypotheses, and unresolved decisions. Do not infer domain contexts from the number of modules or services.

Favor present problems over theoretical elegance: duplicated ownership, broken invariants, needless coordination, expensive change propagation, hard-to-test behavior, or real lock-in. A large class, a conditional, or a missing design pattern is not automatically a defect.

Test each candidate first against the **smallest improvement within existing responsibilities**. Consider a larger boundary or abstraction only when it remedies a concrete limitation at justified cost. Future use cases may inform reversibility analysis but are not requirements.

## Mode A — Discovery

1. Center the search on the user's concern or change-cost pattern. Build a minimal picture of major modules, dependency direction, responsibility owners, and test interfaces.
2. Look for evidence of friction: repeated cross-module edits, ambiguous state ownership, duplicated coordination, pass-through chains, unwanted dependency cycles, tests requiring unrelated setup.
3. Form a hypothesis only when evidence explains **what is costly now**, its likely architectural cause, and a plausible improvement.
4. For each hypothesis, compare a simple local correction with any warranted structural alternative: ownership clarity, change radius, coupling, test observability, migration cost, new complexity.
5. Reject stylistic or speculative hypotheses. If no substantive friction appears, say so.

Report each candidate with: **hypothesis, verified evidence, affected boundaries and ADRs, smallest plausible correction, alternative (if warranted), costs, uncertainty, and questions for focused review**.

Do not rank candidates unless the user gave a criterion. Do not design full interfaces, file layouts, or migration plans, and do not turn candidates into tickets or ADRs. Ask which candidate, if any, deserves focused review.

## Mode B — Focused review

1. Establish the scope and intended behavior. Inspect enough callers and collaborators to understand the real boundary; do not expand into a general audit without a concrete reason.
2. Inspect responsibilities, state and lifecycle, contracts, dependency direction, tests, and evidence of maintenance friction. Evaluate whether the design is already appropriate, not only how it could change.
3. Identify supported improvements: unclear ownership, invalid states, duplicated policy, contract or persistence lock-in, needless indirection, meaningful test friction. Distinguish demonstrated problems from possibilities that need more evidence.
4. Compare **preserving the current design** and the smallest in-place correction first; add larger alternatives only where needed, with impact and migration cost.
5. Evaluate one realistic future extension only when it helps assess expensive lock-in.
6. Separate routine corrections from changes requiring the user's architectural decision.

Format findings per `${CLAUDE_SKILL_DIR}/../brain-review-code/references/findings.md`, with:

- **Location:** the area or boundary, with file references.
- **Category:** Ownership | Lifecycle | Coupling | Contracts | Invariants | Indirection | Test friction
- **Impact:** the current consequence or concrete expected benefit, plus the consequence if the pattern spreads, when relevant.
- An added field, **Tradeoffs:** what the correction costs or risks.

If the area is sound, say so explicitly rather than proposing change for its own sake. Finish with:

- **Decisions Safe to Preserve** — existing choices supported by evidence, including "no change needed".
- **Decisions Requiring Approval** — consequential alternatives, your provisional recommendation, and a specific question; "None" if applicable.
- **Validation Before Adoption** — tests or experiments needed before a pattern is propagated.

Do not implement, adopt, or document a proposed architecture as settled until the user chooses. Record an approved durable decision through `brain-update`.

## Output

Deliver the review in the conversation. Write a durable report only when the user requests one or a workflow needs it for continuation (for example, a `brain-plan-feature` research ticket).

A durable report goes in `docs/reviews/architecture/<NN>-<short-slug>-review.md`: increment the highest existing number, matching its padding (two digits by default). Never overwrite an earlier review. Include the scope, cited evidence, findings, the three concluding sections, and unresolved questions. A later approval leads to an ADR, not to a rewrite of the old review.

Report the conclusion and any file path created.
