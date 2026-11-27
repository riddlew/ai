---
name: brain-explain-changes
description: Interactively teach how unfamiliar code or a change set works, why its design choices matter, and how its pieces fit together. Flexible scope from symbols to a final branch diff; read-only, not a code review.
argument-hint: "[branch, commit/range, file, symbol, or topic]"
---

# Explain Changes

Help the user **understand actual code**: what it does, how it works, why important choices were made, and how its parts connect. Adapt to their question, from a single method to a branch or subsystem. **Do not force a scenario-specific script.** Teaching, not grading or implementing, is the goal.

**Execution mode:** Follow `CLAUDE.local.md` §Execution mode selection. If no inline/subagents choice is confirmed for this work, ask and wait; never delegate by default.

1. **Set a useful scope.** Use `$ARGUMENTS` and conversation context to identify what the user wants explained. A branch, diff, file, symbol, interaction or feature are all valid. If no target is clear, inspect **staged, unstaged, and untracked** changes, otherwise the **latest commit**; ask if the target remains ambiguous. Don't silently tour the repository. For a branch walkthrough, inspect the **final cumulative diff** against the intended target's merge base, not a series of commits; see the reference for comparison safeguards.
2. **Ground the explanation.** Read actual diffs when relevant, source, entry points, callers, dependencies, configuration and tests. Consult approved specifications, implementation plans, ADRs and decisions for **recorded design rationale** when useful, but verify the implemented behavior from code. Distinguish **what changed from what already existed** and sourced intent from **inferred reasons**. Don't invent motivation or execution evidence.
3. **Start with a mental model.** In **plain English**, explain the purpose and where the selected code fits. For multiple files, orient by responsibility and relationships rather than filename order. Trace a **real execution path** through relevant calls, state, outputs and failure behavior *when applicable*, citing `path:line` where available; if a new component is not **actually wired into production code**, say so. Explain how selected files connect to existing code and each other.
4. **Teach the important parts.** **Explain unfamiliar terms**, framework behavior, non-obvious logic, important design choices and tradeoffs, using concrete inputs and edge cases when helpful. Explain what/why/how without assuming every line needs commentary. Use **short, direct sentences** and adapt depth, examples and grouping to the user's questions. For broad changes, maintain a conversational map of explained versus remaining areas; no new ledger.
5. **Proceed interactively.** Explain **one coherent part per response**, **then pause** for questions, deeper exploration or the next part. Let the user drive the route and depth. **Do not quiz the user unless requested.** Do not require fixed steps, a forced tour of every function or premature design critique.

**Read-only:** Never edit code, docs, execution state or Brain; don't run them unless the user asks (tests included). Do not claim an execution path or tests were run unless actually observed. **Not a review:** Never grade, suggest refactors or invoke review skills unprompted. If used during a `brain-implement` or `brain-pair-program` approval checkpoint, **do not approve, close or advance that checkpoint**; the user returns to the original workflow to decide.

**Read when needed:** `${CLAUDE_SKILL_DIR}/references/explain-details.md` for branch comparison, cross-file teaching, review-checkpoint handoff and other situational guidance. These are examples, not mandatory modes.

**Recommended next step:** End the final user-facing reply with one concise, evidence-based next action, naming the appropriate skill or command when useful. If blocked, identify the missing information, prerequisite, or approval instead of advancing; if complete, say no further action is needed. A recommendation is not authorization to execute another step. Keep it outside copy-ready deliverables.
