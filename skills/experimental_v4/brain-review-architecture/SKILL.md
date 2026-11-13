---
name: brain-review-architecture
description: Discover architectural friction across a codebase, or assess a selected feature, subsystem, design, or boundary, reporting evidence-backed improvements without implementing them. Use when the user asks whether an area's design is sound, where the architecture is making changes expensive, or to evaluate an ownership or boundary decision.
---

# Architecture Review

**Project brain:** Follow `CLAUDE.local.md` §Project brain loading: read **all** root `.md` files once per session (again after compaction), plus the active branch's pending file when present. Inspect linked detail and verify task-critical facts against current source. Do not send the whole brain to subagents. If no brain exists, proceed and mention `/brain-init` once.

Find or assess architectural improvements using concrete evidence. Follow `CLAUDE.local.md`: a recommendation or selected review topic is not approval to redesign. Do not modify production code.

Choose the mode by **whether the user has selected an area**, not by whether they already know what is wrong:

- **Discovery:** the user wants a search for improvement opportunities and has not selected a feature, file set, subsystem, or boundary. A broad concern ("the architecture is getting hard to maintain") gives direction without defining a focused scope.
- **Focused review:** the user selects a feature, file set, class, subsystem, design, boundary, decision, or previously discovered candidate, with or without a suspected problem.

If the request names specific code, use focused review. Do not run both modes automatically; after discovery, let the user select a candidate for focused review.

## Shared evidence rules

Establish the user's goal, known use cases, relevant owners and interfaces, constraints, and non-goals. Read `.brain/glossary.md`, `.brain/03_architecture.md`, and relevant ADRs in `.brain/adrs/`; treat an existing ADR as intentional unless current evidence supports reconsidering it.

Inspect code, tests, callers, dependencies, configuration, and change history only to the depth required. Separate verified facts, established choices, hypotheses, and unresolved decisions. Do not infer domain contexts from the number of modules or services.

Favor present problems over theoretical elegance: duplicated ownership, broken invariants, needless coordination, expensive change propagation, hard-to-test behavior, or real lock-in. A large class, a conditional, or a missing design pattern is not automatically a defect.

Test each candidate first against the **smallest improvement within existing responsibilities**. Consider a larger boundary or abstraction only when it remedies a concrete limitation at justified cost. Future use cases may inform reversibility analysis but are not requirements.

## Coverage and previous reviews

For a standalone review, first identify the current branch and `HEAD` SHA, relevant uncommitted changes, and the bounded review scope. Inspect the relevant code independently; do not let earlier reports substitute for current evidence.

Inventory relevant saved architecture reviews under `.brain/reviews/architecture/`, including legacy flat reports. Read the most recent matching review and any earlier review needed to understand outstanding findings. Check each prior finding against the current implementation and classify it as **still supported**, **resolved**, **no longer applicable**, or **unverified**. Keep newly discovered issues separate from issues newly introduced by code changes; on unchanged code, a new finding is a discovery, not a regression. If no usable prior report exists, state that this review establishes the baseline.

For the selected scope, record a compact **coverage summary** of the boundaries, responsibilities, lifecycle or contracts inspected, the evidence examined, and any unexamined areas. Do not imply that inspected areas are defect-free. In the conclusion, reconcile prior findings with current findings and identify any coverage gaps; do not infer the cause of a previous omission without evidence. Include the coverage summary and prior-finding dispositions in the conversation report, not just the saved file.

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

Deliver the review in the conversation. **For a standalone architecture review, also save a durable report by default when a writable project brain exists**, so later reviews have a baseline. When invoked solely as a specialist inside another review, return findings to the invoking workflow without saving unless requested. If the user explicitly requests a conversation-only review, do not save.

Follow `${CLAUDE_SKILL_DIR}/../brain-review-code/references/report-storage.md`: save new reports at `.brain/reviews/architecture/<NN>-<short-slug>/review.md`. Include the scope and source revision, cited evidence, coverage summary and limitations, findings, reconciliation with previous reports (or "first baseline"), the three concluding sections, and unresolved questions. Preserve older reports even if their findings are later resolved. A later approval leads to an ADR, not a rewrite of the old review.

When saving, create the report early and update its substantive sections as the review progresses; distinguish tentative observations from verified findings. The report is the only review-owned file you write unless supporting artifacts were explicitly requested. Then invoke `brain-update` with a one-line summary of the new review; do not record unapproved recommendations as decisions.

Report the conclusion and any file path created, or disclose if no report was saved.
