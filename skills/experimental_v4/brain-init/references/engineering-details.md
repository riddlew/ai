# Decision and review details (read when needed)

## When consultation is required

Consult **before implementing or recording as decided** a choice that would materially:

- Change requirements, scope, user-visible behavior, error handling, or recovery semantics not already specified.
- Introduce, remove, or relocate ownership of responsibilities, state, resources, or lifecycles; for example, moving connection ownership from a `Session` class to a new manager.
- Create a significant service, manager, abstraction, architectural layer, or dependency, or change dependency direction or context boundaries.
- Change public APIs, protocols, serialization, persistence, data migrations, concurrency guarantees, security boundaries, or external compatibility.
- Override an approved architectural decision, ADR, or specification; or create significant operational cost or difficult-to-reverse commitments.

These are significance tests, not blanket bans. A minor helper class with no new architectural ownership is not automatically a consequential decision. Conversely, a small diff can still change a consequential contract. Consultation is for a **genuinely unresolved** consequential choice: first apply approved requirements and established decisions. Routine engineering details do not become approval questions merely because they involve state, architecture, or errors.

**Do not ask the user for facts that can be discovered.** Do not ask again for a choice the user already approved. Do not manufacture design questions, requirements, future extension points, or approvals merely to follow a process.

## How to consult

When a consequential decision arises:

1. Explain the concrete requirement, observed facts, and why the decision is necessary now.
2. Start with the simplest approach consistent with existing ownership and approved requirements.
3. Give only meaningful alternatives, explaining correctness, complexity, coupling, migration, testing, and maintenance tradeoffs.
4. State a provisional recommendation and its evidence. Identify assumptions and uncertainties explicitly.
5. Ask a focused question and **wait for the user's decision** before taking the consequential action.

If the current architecture genuinely cannot support a requirement safely or correctly, explain why and propose a change; do not quietly force a poor fit. If a user-approved direction presents a concrete safety or correctness problem, surface it instead of silently substituting another design.


## Implementation and review discipline

- Prefer the smallest coherent solution satisfying **current** requirements. Do not optimize for speculative flexibility or abstract design ideals.
- Inspect the relevant existing owners, callers, tests, and decision records before changing architecture.
- Implement incrementally, verify observable behavior, and keep changes within scope. Do not introduce a new architecture merely to make a test convenient.
- Treat reviews and research as evidence and proposals, not as authority to expand scope or change approved decisions.
- Keep process proportional: routine changes may be implemented and verified directly; substantial features may need specs; long-running work may need planning and tickets.
- `.brain/` is the project's single document store. `brain-init` creates it; after that, `brain-update` owns its root project-knowledge files, `adrs/`, `sources/`, and `knowledge/`; other skills write only their own documents into its subfolders, then invoke `brain-update`. In `.brain/features/<slug>/04-implementation-plans/`, `brain-design-implementation` owns design documents; `brain-implement` separately owns that feature's `execution.md` and may not rewrite approved designs.
- Deliver review and diagnosis results in the conversation. Save review reports only when requested or required by the workflow, **except** that standalone `brain-review-architecture` saves a baseline by default when a writable brain exists. Do not save a review invoked only as a specialist unless requested.
- Record **approved** durable decisions through the project's existing documentation conventions when justified; do not turn unapproved recommendations into ADRs.
- Implementation blueprints are **execution guidance**, not independent authority over the governing spec, ADRs, or approved user decisions. A blueprint explicitly approved by the user controls agreed implementation structure; clearly labeled illustrative signatures and pseudocode may be refined. `brain-implement` defaults to **collaborative** mode: for substantial or design-sensitive work, obtain blueprint approval before coding; after each verified, coherent increment, show the diff and pause for the user's review. Guided and autonomous modes are opt-in; none waives approval of unresolved consequential choices. Collaboration mode (review checkpoints) is distinct from execution mode (inline or subagent-driven); collaborative execution defaults to inline. For trivial, well-defined fixes, a separate blueprint is optional.
- Implementation plans in `.brain/features/<slug>/04-implementation-plans/` are approved design guidance, distinct from execution evidence; descriptive `.brain` root files (`01`–`08`, `state.md`) are continuity aids that summarize other sources. Verify them against current code and tests; they never override specifications, ADRs, or recorded decisions. `.brain/09_user_decisions.md` is itself an authority on intent, alongside specifications and ADRs, and `.brain/glossary.md` is the authority on terminology. Documents explicitly designated authoritative for a protocol, API, or external contract remain authoritative over summaries derived from them in `.brain/knowledge/`. Current code determines what is implemented, not what the source requires; do not silently reconcile these disagreements. Record approved consequential changes in the governing specification, ADR, or `09_user_decisions.md` first. If authoritative records disagree, first check whether a later approved decision explicitly supersedes an earlier one. Otherwise surface the conflict and consult rather than inventing precedence.

If blocked by a consequential open question, finish safe independent work, clearly identify the decision and affected scope, and do not proceed through the blocked choice.
