---
name: brain-explain-changes
description: Walk through code changes or a component interactively in plain language, using real application paths to build understanding. Not a code review or implementation.
argument-hint: "[commit/range, file, symbol, or topic]"
disable-model-invocation: true
---

# Explain Changes

Teach **how changed code works**, not whether it should be redesigned. Read-only, interactive, grounded in the actual execution path. Use `$ARGUMENTS` as the requested revision/file/symbol/topic.

1. Resolve the requested commit/range/file/symbol/topic; if none, inspect staged, unstaged, and untracked changes, otherwise the latest commit. Show scope; don't silently tour the whole repository.
2. Read actual diff, implementation, callers, entry points, configuration and relevant tests. Use Brain/approved design when helpful, verifying behavior against current source.
3. Start with purpose and a short mental model; trace one **real execution path** from entry point through calls, state, output and failure/cleanup, using real `path:line` evidence. Say if a new component is not **actually wired into production code**. Distinguish **what changed from what already existed**.
4. Explain unfamiliar terms and tricky logic only as needed, in plain English using short, direct sentences and concrete examples. Distinguish implementation facts from inferred reasons.
5. Explain **one coherent part per response**, then pause for the user to direct the next. Do not quiz the user unless requested.

**Read-only:** Never edit code, docs, or Brain; don't run them unless the user asks (tests included). Do not claim an execution path was executed or verified unless it actually was. **Not a review:** Never grade, suggest refactors or invoke review skills unprompted. Do not invoke `brain-update`.

**Read when needed:** `${CLAUDE_SKILL_DIR}/references/explain-details.md` for comparison modes, teaching patterns and edge cases. This is an explanation, not a defect review.
