---
name: brain-explain-changes
description: Walk through code changes or a component interactively in plain language, using real application paths to build understanding. Not a code review or implementation.
argument-hint: "[commit/range, file, symbol, or topic]"
disable-model-invocation: true
---

# Explain Changes

Help the user understand code they may not have written. **Teach how it works, not whether it should be changed.** Be conversational, accurate, and deliberately easy to follow.

**Project brain:** Follow `CLAUDE.local.md` §Project brain loading: read all project-knowledge root `.md` files once per session (again after compaction), plus the active branch's pending file when present. Open linked detail only when relevant; verify task-critical claims in current code. If no brain exists, proceed without requiring `/brain-init`.

**Scope:** Use `$ARGUMENTS` as the requested commit, range, file, function, or topic. If absent, inspect staged, unstaged, and untracked changes; if the working tree is clean, inspect the latest commit. Identify the exact revision or paths being explained. If multiple unrelated changes are present, give a brief overview and let the user choose where to start. If there are no changes or a usable target, ask what to explain. Do not silently substitute a full repository tour.

## Workflow

1. **Find the actual changes.** Read the relevant diff (when available), changed code, nearby callers, entry points, configuration, and tests. Use `.brain` context or approved design documents when helpful, but check current behavior in source. Distinguish what changed from what already existed.
2. **Build a short mental model.** Explain in plain English what the change adds or fixes, where it fits, and the 2–4 most important parts. Start with the purpose, not class names or implementation detail.
3. **Trace a real execution path.** Follow one concrete input, request, or event from where the application starts using the change through its main calls, state changes, result, and relevant failure/cleanup behavior. Show how the new component is actually wired into production code; do not stop at isolated tests or the new file. If it is not wired in, say so without turning the walkthrough into a review.
4. **Unpack only the tricky parts.** Explain unfamiliar syntax, important decisions, and non-obvious conditions as they arise. Explain why a design choice exists only when supported by code, tests, comments, or decisions; label inference as inference. Use one short code snippet or concrete example only when it improves comprehension.
5. **Connect tests to behavior.** Point out the most useful tests and what real behavior they demonstrate, when relevant. Don't recite the entire test suite.
6. **Proceed interactively.** Explain one coherent part per response, then pause. Offer to continue to the next part or dig into the current one, and follow the user's questions and preferred depth. On the first response, provide the overview and *one* starting point, not a complete lecture. Do not quiz the user unless requested.

## Plain-language standard

- Use short, direct sentences and familiar words. Write like a patient, experienced developer explaining the code to a teammate, **not** like a textbook, tutorial generator, or architecture report.
- Explain unfamiliar terms in one simple sentence on first use; don't avoid precise names when they help the user locate code.
- Explain **what happens, why it matters, and where to see it**. Use concrete examples ("when the app receives a message...") rather than abstract summaries ("the system orchestrates message lifecycle management").
- Prefer small chunks and ordinary paragraphs to long bullet lists, walls of text, line-by-line narration, or unnecessary analogies. Match the user's requested depth; start simple and add detail when asked.
- Link explanations to real `path:line` locations where available, otherwise cite file and symbol. Do not invent call flows, claims, or reasons.

## Boundaries

- **Read-only:** Do not edit code, tests, project-brain files, or documentation; don't create reports, update the brain, or commit. Avoid commands that modify the working tree. Reading tests is enough; don't run them unless the user asks.
- **Not a review:** Don't hunt for defects, grade code quality, suggest refactors, or invoke other review skills. If you notice a serious issue relevant to the explanation, mention it briefly and neutrally, then return to teaching. If the user asks for a review, direct them to the relevant review skill.
- Do not claim an execution path, behavior, or test result is verified by running the program unless it actually was. Be explicit about what you read and what remains uncertain.
