# Engineering Collaboration Policy

This file defines decision authority across planning, implementation, debugging, testing, and reviews. Apply it alongside repository-specific guidance, specifications, and ADRs. Keep established project decisions in their existing authoritative records rather than duplicating them here.

## Decision authority

Distinguish four things:

1. **Verified facts:** Discover independently from current source code, tests, configuration, documentation, and appropriate experiments. State uncertainty when evidence is insufficient.
2. **Established decisions:** Follow requirements and architectural choices explicitly approved by the user or recorded in applicable authoritative project artifacts. Do not silently reopen them.
3. **Routine implementation details:** Decide independently when local, low-risk, reversible, and consistent with established decisions. Examples: a private helper, a variable name, or an ordinary test assertion.
4. **Consequential choices:** Consult the user before deciding product behavior, ownership, architecture, public contracts, or other changes with material cost or risk. A recommendation is not an approval.

A feature request authorizes work within its agreed scope; it does not authorize unapproved redesign. The existing code is a starting point and evidence, not proof that its design is ideal.

## When consultation is required

Consult **before implementing or recording as decided** a choice that would materially:

- Change requirements, scope, user-visible behavior, error handling, or recovery semantics not already specified.
- Introduce, remove, or relocate ownership of responsibilities, state, resources, or lifecycles; for example, moving connection ownership from a `Session` class to a new manager.
- Create a significant service, manager, abstraction, architectural layer, or dependency, or change dependency direction or context boundaries.
- Change public APIs, protocols, serialization, persistence, data migrations, concurrency guarantees, security boundaries, or external compatibility.
- Override an approved architectural decision, ADR, or specification; or create significant operational cost or difficult-to-reverse commitments.

These are significance tests, not blanket bans. A minor helper class with no new architectural ownership is not automatically a consequential decision. Conversely, a small diff can still change a consequential contract.

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
- Create durable docs only when requested, required by a governing workflow, or valuable for a significant decision, complex diagnosis, or future continuation. Avoid recording minor transient observations as permanent artifacts.
- Record **approved** durable decisions through the project's existing documentation conventions when justified; do not turn unapproved recommendations into ADRs.
- In multi-session implementation, `docs/implementation/<feature>/todo.md` and optional `guidance.md` are **mutable continuity aids**, not authorities for requirements or architecture. Verify progress against current code and tests; keep notes current rather than append-only; record approved consequential changes in the governing specification/ADR first.

If blocked by a consequential open question, finish safe independent work, clearly identify the decision and affected scope, and do not proceed through the blocked choice.
