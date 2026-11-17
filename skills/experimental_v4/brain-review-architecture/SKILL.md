---
name: brain-review-architecture
description: Discover architectural friction across a codebase, or assess a selected feature, subsystem, design, or boundary, reporting evidence-backed improvements without implementing them. Use when the user asks whether an area's design is sound, where the architecture is making changes expensive, or to evaluate an ownership or boundary decision.
---

# Architecture Review

Investigate architecture as **evidence-backed proposals**, not permission to redesign or implement. Choose **Discovery** if the user has not selected an area; otherwise use **Focused review**. Do not automatically perform both.

## Workflow

1. Establish current branch/HEAD, dirty changes, applicable decisions and the review scope. Inspect code, dependencies, callers, tests, configuration and ADRs sufficiently to trace responsibility/lifecycle and important boundaries.
2. Read the **relevant previous** architecture reports, including legacy flat reviews. State a compact **coverage summary** and note what was not inspected. Distinguish findings **still supported**, **resolved**, **no longer applicable**, and **unverified**. Do not reissue stale findings uncritically.
3. **Discovery:** identify evidence-based candidate issues, smallest plausible corrections, tradeoffs and open choices, without designing a migration. Let the user select a candidate before a detailed focused review.
4. **Focused:** inspect the selected boundary, constraints and viable options. Check current ownership and downstream effects; clearly separate approved structure from proposed changes. Ask for consequential decisions before implementation.
5. Report findings, code evidence, prior-review continuity, constraints and limitations. **For a standalone architecture review, save a report by default when a writable Brain exists**, at `.brain/reviews/architecture/<NN>-<short-slug>/review.md`; when invoked solely as a specialist, don't save unless requested. Use `${CLAUDE_SKILL_DIR}/../brain-review-code/references/report-storage.md` and `brain-tool doc new --kind review --report-type architecture`.

**Read when needed:** `${CLAUDE_SKILL_DIR}/references/architecture-review-details.md` for broad discovery sampling, full finding/report format, prior review reconciliation and deep design analysis. A review never itself approves the proposed architecture.

**Recommended next step:** End the final user-facing reply with one concise, evidence-based next action, naming the appropriate skill or command when useful. If blocked, identify the missing information, prerequisite, or approval instead of advancing; if complete, say no further action is needed. A recommendation is not authorization to execute another step. Keep it outside copy-ready deliverables.
