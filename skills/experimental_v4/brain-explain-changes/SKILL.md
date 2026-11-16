---
name: brain-explain-changes
description: Walk through code changes or a component interactively in plain language, using real application paths to build understanding. Not a code review or implementation.
argument-hint: "[commit/range, file, symbol, or topic]"
disable-model-invocation: true
---

# Explain Changes

Teach **how changed code works**, not whether it should be redesigned. Read-only, interactive, grounded in the actual execution path.

1. Resolve the requested commit/range/file/symbol/topic; if none, inspect dirty changes, otherwise the latest commit. Show scope; don't silently tour the whole repository.
2. Read actual diff, implementation, callers, entry points, configuration and relevant tests. Use Brain/approved design when helpful, verifying behavior against current source.
3. Start with purpose and a short mental model; trace one real request/event from entry point through calls, state, output and failure/cleanup, using real `path:line` evidence. Say if a new component is not actually wired in.
4. Explain unfamiliar terms and tricky logic only as needed, in short plain-language chunks with concrete examples. Distinguish implementation facts from inferred reasons.
5. Explain **one coherent segment per response**, then pause for the user to direct the next. Never quiz, review, grade code, run tests without request, edit documents or invoke `brain-update`.

**Read when needed:** `${CLAUDE_SKILL_DIR}/references/explain-details.md` for comparison modes, teaching patterns and edge cases. This is an explanation, not a defect review.
