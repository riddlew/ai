---
name: brain-review-code
description: Review a bounded Git change set for correctness, requirement fit, and repository fit, reporting only evidence-backed findings. Use when the user asks for a code review of a branch, commit range, or working-tree change, or when implementation of a substantial or consequential change is complete.
---

# Code Review

Review a **bounded change set** for **Correctness**, **Requirement fit**, and **Repository fit**. Report verified findings, not speculative style objections; do not silently redesign approved requirements.

## Workflow

**Execution mode:** Follow `CLAUDE.local.md` §Execution mode selection before review work. If no explicit or confirmed mode applies, ask inline (recommended) or subagents and wait. Large change sets never authorize delegation automatically. Inline runs all three assessments in the main session.

1. Resolve **the actual comparison** (target base, source HEAD, merge base and working-tree scope). Never substitute the branch's own `@{upstream}` for the intended target. Include staged, unstaged and relevant untracked **contents** whenever in scope; preserve user edits.
2. Read applicable approved specifications/Examples under `.brain/features/<feature-slug>/02-specifications/`, task acceptance criteria under `05-tasks/` when present, architecture/ADRs and repository guidance. If no authoritative requirement basis is available, explain why Requirement fit is limited; never invent it.
3. Complete all three assessments. Check correctness and requirement coverage thoroughly; **scope Repository fit proportionally** to changed code, affected boundaries and concrete maintenance costs, expanding only where evidence warrants deeper architectural inspection. Trace plausible defects through code/tests; try to disprove each. Evaluate observable behavior and current costs, not aesthetic preferences. Preserve one status row for each in-scope Example, acceptance criterion and Review Focus (`RF<n>`): met, unmet or unverifiable.
4. Consolidate findings by file/line, impact, evidence, severity and actionable correction. Distinguish verified bugs from questions and limitations; no unsupported blanket pass/fail verdict. Report comparison base, scope, assessment mode and tests actually examined.
5. Deliver findings in the conversation. Save a durable report only when requested or required: `.brain/reviews/code/<NN>-<short-slug>/review.md`. Use `${CLAUDE_SKILL_DIR}/references/report-storage.md` and `brain-tool doc new --kind review --report-type code`, then `brain-update` when the report changes.

**Read when needed:** `${CLAUDE_SKILL_DIR}/references/code-review-details.md` for delegated/inline assessment separation, full evidence packets, coverage report format or complex review. `${CLAUDE_SKILL_DIR}/references/findings.md` for severity and validation; `${CLAUDE_SKILL_DIR}/references/builder-review.md` for source-specific fit.

Do not change reviewed code or introduce a consequential redesign as a review finding without consulting the user.

**Recommended next step:** End the final user-facing reply with one concise, evidence-based next action, naming the appropriate skill or command when useful. If blocked, identify the missing information, prerequisite, or approval instead of advancing; if complete, say no further action is needed. A recommendation is not authorization to execute another step. Keep it outside copy-ready deliverables.
