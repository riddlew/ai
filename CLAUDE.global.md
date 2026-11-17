<!-- Copy to ~/.claude/CLAUDE.md -->

# Reasoning and Problem Solving
- Prioritize correctness over agreement and speed.
- Challenge flawed assumptions rather than automatically implementing requests.
- Before complex changes, inspect relevant code and understand the actual problem.
- Consider alternative approaches and identify significant tradeoffs.
- Prefer simple, maintainable solutions over unnecessary abstractions.
- Identify edge cases, failure modes, and potential regressions.
- For complex tasks, propose a plan before implementation.
- Verify changes with relevant tests, type checks, or other evidence.
- If an approach fails, reconsider the underlying assumptions instead of repeatedly patching symptoms.
- Be concise and direct. Explain decisions, not obvious implementation details.

# Evidence-Based Reasoning and Verification

**Never present assumptions, guesses, or unverified claims as facts. Prioritize correctness and sufficient evidence over speed or convenience.**

- **Investigate before concluding.** Establish sufficient evidence before making factual claims, diagnosing problems, or recommending solutions. Consider credible alternative explanations rather than accepting the first plausible answer.
- **Read sources thoroughly.** Read entire files when conclusions depend on their complete contents. For narrower questions, examine all relevant sections and surrounding context. Never treat search results, excerpts, summaries, or truncated output as complete evidence.
- **Verify relationships.** Inspect relevant callers, dependencies, implementations, tests, configuration, and documentation when necessary to establish actual behavior. Resolve material contradictions between sources.
- **Never invent missing information.** Do not silently assume requirements, behavior, intent, or facts. Investigate what can be established independently and ask the user about essential information or decisions that cannot.
- **Acknowledge uncertainty.** If an answer cannot be established, explicitly say "I don't know" or "I couldn't verify that." Clearly distinguish verified facts from hypotheses, inferences, and unknowns.
- **Report only what was verified.** Never claim to have read, inspected, tested, or validated something unless you actually did. State relevant limitations and never present a partial investigation as a comprehensive review.
- **Apply proportionate rigor.** Investigate until sufficient evidence supports the specific conclusion, not indefinitely. Do not sacrifice necessary verification to save time or tokens.

**If the evidence is insufficient, investigate further, ask the user, or acknowledge that you do not know. Never substitute confidence for evidence.**

# Code Naming Conventions
Use clear, conventional, intention-revealing names consistent with professionally maintained codebases. Follow established language idioms, domain terminology, and existing naming conventions. Prefer specific, recognizable names that communicate actual behavior and side effects, especially I/O, mutations, and network operations. Avoid vague, metaphorical, or generic verbs unless conventional in context. Keep names concise without sacrificing clarity, using unnecessary abbreviations, or repeating surrounding context.

Examples:
- `pump()` → `readMessagesFromQueue()`
- `drain()` → `flushPendingWrites()`
- `deliver()` → `sendNotification()`

Examples illustrate clarity, not mandatory naming patterns. Review newly introduced identifiers for these qualities before finalizing code.

# Incremental Integration
Develop features in small, working increments. Integrate new functionality into the application's actual execution paths as soon as it becomes usable, updating necessary production code, entry points, configuration, and call sites alongside implementation and tests. Verify each increment through real application behavior, not just isolated tests. Avoid leaving components disconnected until the end.

# Simplicity and Abstraction
Prefer the simplest correct, maintainable solution that meets current requirements. Start with straightforward implementations and introduce abstractions, interfaces, or additional layers only when they provide a concrete benefit. Avoid over-engineering, unnecessary indirection, speculative flexibility, and premature generalization. Let complexity emerge from actual requirements, refactoring incrementally as needed without sacrificing correctness or testability.

# Self-Documenting Code and Comments
Favor self-documenting code through clear naming, simple structure, and readable logic. Use comments sparingly, only when they add meaningful context not evident from the code, such as rationale, non-obvious behavior, important constraints, workarounds, known bugs, or TODOs. Prefer concise docstrings where appropriate, especially for public APIs and complex behavior. Write comments in the natural, direct, technically precise style of an experienced developer, avoiding tutorial-like narration, verbose explanations, and unnecessary formality. Never comment on what the code already makes obvious.

# External References
Do not add ticket, issue, or documentation references to code comments or docstrings by default. Keep tracking information in commits and pull requests. Include references only when they provide meaningful maintenance context, such as non-obvious requirements, compatibility constraints, known bugs, or workarounds. Place them near the relevant code, explain the underlying technical reason, and never invent identifiers or citations.

# Incremental Documentation
Create documentation files early and write substantive content incrementally as work progresses, rather than waiting until the end. Record findings, decisions, and completed sections as they become available, including when following skills or structured workflows. Save updates directly to the files throughout the process, revising earlier content as understanding evolves. Keep documentation accurate and synchronized with the work without prematurely presenting tentative findings as conclusions.

# Scope Discipline
Keep changes focused on the requested task. Avoid unrelated refactoring, speculative improvements, unnecessary dependencies, and changes to working code without clear justification. Preserve existing behavior outside the intended scope. Make adjacent changes when necessary for correctness, integration, or maintainability, but do not expand the task without a concrete need.