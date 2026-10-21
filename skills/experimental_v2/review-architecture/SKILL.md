---
name: review-architecture
description: Discover architectural improvement opportunities across a broad codebase or evaluate a specific feature, file, subsystem, design, or boundary for evidence-backed improvements without implementing unapproved decisions.
---

# Architecture Review

This skill combines architectural discovery (formerly `improve-architecture`) and focused architectural review. Follow root `CLAUDE.md` for decision authority. **A recommendation or selected review topic is not approval to redesign the system.** Do not modify production code.

Choose the mode based on **whether the user has selected an area to examine**, not whether they already know what is wrong:

- **Discovery:** The user wants the agent to search across the codebase for worthwhile architectural improvement opportunities and has not selected a specific feature, file set, subsystem, or boundary. A broad concern (for example, "the architecture is getting difficult to maintain") can provide direction without defining a focused review scope.
- **Focused review:** The user selects a specific feature, set of files, class, subsystem, design, boundary, architectural decision, or previously discovered candidate. They may simply want to know whether the selected area can be improved; they do **not** need to identify a problem or propose a solution first.

If a request names specific code to review, default to **focused review**, even if it is exploratory. Do not redirect to discovery merely because the user has not identified a defect. Do not run both modes automatically. If discovery reveals useful candidates, present them and let the user select one for deeper review.

## Shared evidence rules

Establish the user's goal, known use cases, relevant owners and interfaces, constraints, and intentional non-goals. Read applicable root `CONTEXT-MAP.md`, the relevant context's `CONTEXT.md` (or root `CONTEXT.md`), and relevant root/context ADRs. Treat an existing ADR as intentional unless current evidence supports reconsideration.

Inspect relevant code, tests, callers, dependencies, configuration, and change history only to the depth required. Separate verified facts, established choices, hypotheses, and unresolved decisions. Do not infer domain contexts from the number of modules or services.

Favor present problems over theoretical elegance: duplicated ownership, broken invariants, needless coordination, expensive change propagation, hard-to-test behavior, or real lock-in. A large class, a conditional, or a missing design pattern is not automatically defective.

Test a candidate first against the **smallest improvement within existing responsibilities**. Consider a larger boundary or abstraction only when it remedies a concrete limitation and its cost is justified. Future use cases may inform reversibility analysis but are not requirements to implement today.

## Mode A — Discovery

When the user has not selected a specific area:

1. Center the search on any broad concern or change-cost pattern the user describes. Build a minimal picture of major modules, dependency direction, responsibility owners, and meaningful test interfaces. If the user already selected specific code or a feature, use focused review instead.
2. Identify evidence of friction: repeated cross-module edits, ambiguous state ownership, duplicated coordination, pass-through chains, unwanted dependency cycles, or tests requiring unrelated setup.
3. Form a hypothesis only when evidence explains **what is costly now**, the likely architectural cause, and a plausible improvement.
4. For each credible hypothesis, compare a simple local correction with any warranted structural alternative. Discuss ownership clarity, change radius, coupling, test observability, migration costs, and new complexity.
5. Reject stylistic or speculative hypotheses. If no substantive friction appears, report that rather than inventing work.

Present a concise discovery report covering, for each candidate: **hypothesis, verified evidence, affected boundaries and ADRs, smallest plausible correction, alternative (if warranted), costs, uncertainty, and questions for focused review**.

Do not rank candidates unless the user gave a criterion (for example, maintenance cost or defect risk). Do not design full interfaces, file layouts, or migration plans yet. Do not turn candidates into tickets or ADRs. Ask which candidate, if any, deserves focused review.

A discovery report can be delivered in the conversation. Write a temporary report file only when requested, when the investigation is too substantial to carry forward otherwise, or when a durable handoff is needed. Do not generate permanent architecture-review documents for an uneventful scan.

## Mode B — Focused review

When the user selects a feature, file set, class, subsystem, design, decision, or other specific area to evaluate—even without a suspected problem:

1. Establish the requested scope and intended behavior from the user and repository. Inspect enough callers and collaborators to understand the actual architectural boundary; do not expand into a general audit without a concrete reason. Identify applicable approved decisions and non-goals.
2. Inspect current responsibilities, state and lifecycle, contracts, dependency direction, tests, and available evidence of maintenance friction. Evaluate whether the design is already appropriate, not just how it might be changed.
3. Identify supported opportunities for improvement, such as unclear ownership, invalid state, duplicated policy, contract/persistence lock-in, needless indirection, or meaningful test friction. Distinguish demonstrated problems from possible improvements that need further evidence. Do not fabricate issues for completeness.
4. Compare **preserving the current design** and the smallest in-place correction first. Add larger alternatives only where needed; state impact and migration cost.
5. Evaluate one realistic future extension only when it helps assess expensive lock-in. Do not design for speculative scale.
6. Identify which findings can be acted on as routine corrections and which require the user's explicit architectural decision.

For each supported finding report: **area, evidence, current consequence or concrete expected benefit, potential consequence if spread (when relevant), smallest justified correction, tradeoffs, urgency, confidence**. If the selected area is already sound, say so explicitly rather than proposing changes for their own sake. Finish with:

- **Decisions Safe to Preserve** — existing choices supported by evidence, including the conclusion that no change is needed.
- **Decisions Requiring Approval** — consequential alternatives, your provisional recommendation, and a specific user question; say "None" if applicable.
- **Validation Before Adoption** — tests or experiments needed before a pattern is propagated.

Do not implement, adopt, or document a proposed architecture as settled until the user chooses. If an approved decision should be recorded as a durable architectural choice, invoke `domain-modeling`; the review finding itself does not authorize an ADR.

## Review artifact policy

Write a durable **append-only** report when the focused review concerns an important boundary, a costly-to-reverse change, a pattern likely to spread, a consequential dispute, or when the user requests a record. Do **not** force a permanent artifact for quick opinions, narrow low-risk reviews, or an investigation with no durable value.

When warranted, create `docs/reviews/architecture/<NN>-<short-slug>-review.md`; inspect existing numbers and follow their zero-padding (two digits by default). Never overwrite an earlier review. Include the reviewed scope, cited code/ADR evidence, supported findings, the three concluding sections, and any unresolved questions. A later approval may lead to a new ADR; do not rewrite an old review to make it appear approved retroactively.

Report the resulting conclusion and any file path actually created. If there is no durable report, say so only if relevant to the user request.