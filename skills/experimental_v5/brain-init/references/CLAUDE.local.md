# Brain v5 project policy

Brain workflow version: experimental_v5

## Authority and authorization
- User establishes consequential behavioral and architecture decisions. Investigate discoverable facts first; consult when consequential behavior, ownership, API, protocol, persistence, concurrency, security, compatibility or irreversible cost is unresolved.
- An explicit request to implement authorizes code changes within established scope; brainstorming, planning, explaining or reviewing alone does not authorize code edits.
- Follow designated authoritative source contracts, applicable ADRs, user decisions, requirements, and explicit amendments. Code describes implementation facts; it never silently overrides requirements. Keep one authoritative owner per decision.
- Routine reversible implementation details require no questions or approval. Plans, specifications and tasks are optional and have no approval gates.
- Default to inline execution. Dispatch subagents ONLY when explicitly requested. Carry any explicitly selected execution mode across skills without re-asking.
- Preserve user edits, branch/worktree permissions, no unauthorized commits or merges, and scoped writes.

## Brain context
- Locate the project Brain via explicit path, Project brain setting, or `.brain/00_index.md`. Project active version is determined by this installed policy, not historical v4 document status.
- Begin with the user request, active feature and minimal relevant index, authoritative decisions, amendments, code and tests. Expand automatically for unknown dependencies or conflicting facts. A soft context budget must never suppress governing evidence.
- `.brain/.notes/` is private: never traverse, search, index, read or modify it unless the user explicitly requests a specific read; no inferred write permission.
- Keep Git and authoritative source verification explicit. Do not treat a handoff or a stale index as proof of current code.
- Shared Brain may live outside a worktree. Respect actual write authorization; never route around denied workspace boundaries. Keep branch-only implementation facts in pending branch records until verified on main.

## Documents
- Reference `brain-init/references/feature-document-contract.md`. Optional brief → specification → components → plans → tasks, without mandatory stages. `execution.md` and `handoff.md` are optional, short retrieval/state aids; neither overrides requirements.
- Default owner: brainstorm owns decisions/briefs, write-spec owns specifications, design-implementation owns plans, implement/pair owns execution, update owns root knowledge/ADRs/source maps, compact is manual and preview-first.
- Brainstorm may directly update a narrow established decision in an existing spec/plan without a separate owner invocation; complex modifications use their owner or focused amendment. Preserve stable IDs and related meaning.
- No `status` / approval-state changes or parent-hash reapproval; ignore historical v4 metadata when reading. Explicit `amends` and `supersedes` determine narrowly scoped precedence; contradictory amendments are blockers, not latest-file-wins.
- No skill automatically invokes `brain-update`. The user invokes it explicitly when shared knowledge synchronization is useful.

## Implementation and communication
- Implement coherent changes with risk-proportionate focused tests and diff review; deeper checks for security, concurrency, migrations, protocols and compatibility. Test-first when useful, not obligatory.
- Diagnose failures using new evidence rather than repeating identical speculative fixes and test runs. Stop when requested behavior and proportionate verification are complete; avoid unrelated refactoring or documentation.
- Keep progress, final reports and knowledge concise. Record only durable decisions, material blockers, verification and resume state; no redundant restatements.
- Pair modes: AI-led edits on request; developer-led proposes code but never edits application files; Learning Mode mentors the user's coding without editing application files.
