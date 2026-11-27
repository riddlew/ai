# Detailed workflow — brain-explain-changes

These are **situational safeguards**, not separate modes or a required sequence. The primary skill follows the user's intent and preferred depth. Always follow `CLAUDE.local.md` for context loading, the explicit inline/subagent choice, and the private `.brain/.notes/` boundary.

## Explain code without assuming a predefined target

- The user may ask about a function, class, file's purpose, several files interacting, an unfamiliar subsystem, current changes, a commit or a branch. Resolve from their words, `$ARGUMENTS`, recent context and Git state; ask only when material ambiguity remains. Don't redirect a clear question into a full tour.
- No target given: inspect staged, unstaged and relevant untracked changes; if none, inspect the latest commit as a useful default. If several unrelated changes exist, offer a short map and let the user choose. Don't silently claim the latest commit represents an entire feature branch.
- Read relevant actual code **beyond** the diff as needed to establish callers, instantiation/wiring, interfaces, configuration, data flow and tests. applicable specifications and plans clarify requirements and recorded choices; current code determines current behavior. The fact a plan intended a design does not prove the code implements it.
- Start with the purpose and a short mental model. For a focused question, give the answer directly. For broader material, identify natural components, connections and a useful starting point. Follow a concrete execution path where meaningful; not every utility, declaration, migration or test has an application entry point. State when a component is not wired into production.

## Full-branch and other cumulative change sets

For requests such as "walk me through all changes on this branch":

1. Establish the **intended target branch** from an explicit target, PR metadata, repository conventions or verified Git configuration. Do not assume the current branch's upstream is the target. When materially ambiguous, ask which target to compare.
2. Determine the **merge base** of the target and source branch, then inspect the **final cumulative diff** from that base to the requested branch tip. **Do not narrate each commit** or use commit-message summaries as implementation evidence. Show the chosen target, merge-base reference and diff scope in plain language; if unavailable, explain the limitation.
3. Cover **added, modified, renamed and deleted files**, including relevant tests, migrations, configuration and wiring. Group by responsibility or end-to-end behavior; start with the goal and component relationships rather than an alphabetical file dump. Account for changed paths in a compact **change map** so important groups aren't lost. Explain details progressively, not all at once.
4. Identify **uncommitted staged, unstaged and untracked** work separately. Clarify whether the user wants it included if it might change the walkthrough; never silently mix working-tree changes into the committed branch diff. If a PR/base diff has moved or the merge-base comparison is misleading, state the reference and caveat rather than asserting an exact final PR outcome.
5. Keep a **conversation-level** sense of which groups were explained and what remains. Resume questions and jumps without repeating the tour or creating a checklist/progress file. In a long session, recover scope from verified Git state and available conversation context; don't invent remembered coverage.

The comparison rule also applies to broad requests about a change set, but **don't require a Git diff** to explain an unchanged component or concept. Use actual files, relationships and tests for any scope.

## Explain what, how and why

- **Purpose:** What job does this class, method or change perform, and why does the wider feature need it? Explain ownership and how it connects to existing code, especially for an unfamiliar new file.
- **Behavior:** Trace representative inputs, calls, relevant state transitions and outputs; discuss failures, edge cases, threading, transactions or lifecycle **when they actually matter**. If the path cannot be verified, identify the uncertainty.
- **Reasoning:** Explain important choices such as dependency injection, abstraction boundaries, SQL/JPA behavior, concurrency or error mapping. Check established design, ADRs, comments and tests for the **recorded rationale**. When rationale is not documented, say "A likely reason is..." and distinguish it from what can be proved. Do not attribute speculative intentions to the author.
- **Understanding:** Define unfamiliar syntax/framework concepts succinctly and expand with a small code excerpt or realistic example if useful. Explain tradeoffs when they illuminate the approach; don't quietly turn the teaching session into a refactoring review.
- **Adaptation:** Prefer logically coherent chunks over a line-by-line lecture. Respond to specific questions immediately, allow digressions, then continue from the place the user chooses. Never quiz or require the user to demonstrate comprehension unless they request it.

Give concrete source references (`path:line` when known). Distinguish the existing behavior from new behavior and explain the test's observable coverage without claiming tests were executed. If serious concerns become apparent, mention them neutrally when relevant; a requested assessment belongs to `brain-review-code`.

## During implementation review

A user may invoke `/brain-explain-changes` during implementation or pairing. Explain the **actual current diff** and related code, with relevant established design and `execution.md` as read-only context. Answer as many questions as necessary; **do not mark the increment approved**, edit `execution.md`, initiate the next increment, modify code or trigger a review. Direct approval/revision decisions back to the paused implementing skill. A request to understand code is **not** authorization to approve or change it.

## Boundaries

- Strictly **read-only**: no code, test, doc, Brain, report or execution-record writes. Don't invoke `brain-update`; don't run tests unless the user explicitly asks and the command is safe within the authorized scope.
- **Not a code review:** don't hunt for defects, grade code, suggest a rewrite unprompted or trigger reviewer skills automatically. If asked for correctness or requirement-fit review, hand off to `brain-review-code` without claiming a review already occurred.
- **Evidence honesty:** tests read are not tests run; plans are intent, not proof of implementation; source walkthroughs are not runtime executions. Don't invent branch baselines, original motives or unseen sessions.
