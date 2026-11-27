---
name: brain-review-code
description: Optional scoped review of code correctness, requirements, and repository fit.
---

# Code review

Default inline; use subagents only on explicit request. Establish actual target merge base plus in-scope staged, unstaged and untracked contents. Review source, callers, tests, applicable behavior requirements/ADRs/amendments and current decisions; no formal approved-plan prerequisite. Assess correctness, requirement fit and repository fit proportionate to risk. Report verified actionable findings, locations, severity, test evidence and limitations. Do not invent a requirement when none is documented.

Reviews are optional for routine implementation, not required approval checkpoints. Save a report only when useful/explicitly requested. Never edit code in read-only review or automatically invoke `brain-update`. See `references/code-review-details.md` and `references/findings.md` for detailed review.
