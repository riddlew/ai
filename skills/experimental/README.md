# Skills

Skills marked **manual** set `disable-model-invocation: true` and run only when you invoke them explicitly (for example `/implement`). `tdd` is not user-invocable; `implement` invokes it.

| Skill | What it does | Use it when | Output |
|---|---|---|---|
| `brainstorm` | Resolves open decisions, assumptions, and tradeoffs through a dependency-aware discussion. Asks all currently answerable questions together, investigates discoverable facts itself, and leaves subjective choices to you. | You have an idea or decision that is not sufficiently defined yet. | A confirmed direction in the conversation. |
| `diagnose` | Investigates bugs and failures using reproduction, evidence, competing hypotheses, and discriminating experiments. Applies a bounded fix only when you authorize one. | Something is broken, intermittent, regressed, or failing and you need the cause rather than speculative fixes. | `docs/diagnoses/<NN>-<slug>.md` |
| `domain-modeling` | Maintains domain vocabulary, context boundaries, context maps, and ADRs for decisions with durable rationale. | A design discussion changes the meaning of domain concepts, bounded contexts, or significant architectural decisions. | `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/<NNNN>-<slug>.md` (root or `<context>/docs/adr/`) |
| `handoff` (manual) | Produces a compact continuation document that references existing artifacts instead of copying them, and suggests skills for the next session. | You are stopping work and want a fresh session to continue without carrying the full conversation. | `handoff-<slug>.md` in the OS temp directory |
| `implement` (manual) | Creates a branch and records its base, implements the work using `tdd`, runs lint and targeted tests during development and the full suite once at the end, commits, then runs `review-code` against the recorded base and commits in-scope fixes. | A specification or ticket is settled and you are ready to modify production code. | A branch with committed work |
| `improve-architecture` | Explores the repository for evidence-backed architectural friction and presents unranked hypotheses. Hands the one you select to `review-architecture`. | You know the architecture could be improved but have not yet identified the specific decision to examine. | A temporary discovery report |
| `plan-feature` | Manages a multi-session planning effort as dependency-aware planning tickets (`research`, `prototype`, `consult`, `task`). Resolves one non-research ticket per session, delegates `consult` tickets to `brainstorm`, and hands off to `write-tickets` on request. | A feature or initiative has too many decisions to resolve reliably in one session. | `docs/planning/<feature>/INDEX.md` and numbered ticket files |
| `research` | Investigates a focused question in a background agent using authoritative primary sources, with traceable citations and explicit uncertainty. | A decision depends on external or project-local facts that need verification. | `docs/research/<topic>/<file>.md` |
| `review-architecture` | Performs a focused review of a specific architectural decision, boundary, implementation, or pattern, including its consequences if adopted broadly. | You know exactly which architectural area needs scrutiny, especially before it spreads or becomes expensive to change. | `docs/reviews/architecture/<NN>-<slug>-review.md` |
| `review-code` | Reviews `git diff <base>...HEAD` as two independent assessments: repository fit (rules and maintainability) and requirement fit (against the spec). Uses a base ref you provide or one recorded by `implement`; otherwise asks. | Code has been written and you want a focused implementation review before accepting it. | Report in the conversation |
| `review-security` | Traces threats, trust boundaries, authorization, secrets, and sensitive-data flows and records findings with likelihood, impact, and mitigations. | A change affects authentication, authorization, untrusted input, credentials, sensitive data, connectors, persistence, or other security boundaries. | `docs/security/<NN>-<slug>-review.md` |
| `tdd` (not user-invocable) | Drives implementation through red/green increments at test boundaries you approve, preferring integration-style tests without mocking project-owned code. | Invoked by `implement` at each TDD boundary. | Tests and code |
| `write-documentation` | Creates or updates concise repository documentation from verified repository evidence. | README or project documentation is missing, stale, or needs to reflect the current developer workflow. | Root `README.md` or the project's established doc |
| `write-spec` (manual) | Synthesizes existing decisions and project evidence into a feature specification. Does not interview you or reopen decisions. | The problem is sufficiently understood and you need a stable requirements and design contract before creating tickets. | `docs/specs/<NN>-<slug>.md` |
| `write-tickets` | Decomposes an established plan or specification into small vertical tickets with genuine dependencies and acceptance criteria. Presents the ticket set for your approval before writing files. | Design decisions are settled and you want executable work broken into independently verifiable increments. | `docs/tickets/<feature>/issues/<NN>-<slug>.md` |

## Example Flows

### Implementing a new feature

For a substantial feature, a typical flow might be:

1. **brainstorm** if the initial idea is still vague. For example, “Users should be able to share notes” may need decisions about permissions, link lifetime, revocation, and anonymous access.

2. **plan-feature** if resolving the feature will take multiple sessions. It creates the planning directory, resolves one non-research ticket per session, and uses brainstorm for `consult` tickets. Its `research` tickets are investigated and recorded inside the planning ticket.

3. **domain-modeling** whenever planning establishes or changes concepts such as Share, Recipient, or ownership boundaries.

4. **research** for questions like “What guarantees does SQLite provide for concurrent readers during this operation?” when the answer should come from primary sources and stand as its own traceable note.

5. **review-architecture** for a risky structural decision, such as whether sharing should live inside the Notes context or be a separate capability with its own ownership model. Do this before writing the spec, because write-spec records decisions without reopening them. Decisions you approve from the review are recorded through domain-modeling.

6. **write-spec** once feature behavior and constraints are settled. Run it where the decisions are available (the current conversation, or the planning directory and other artifacts you point it to).

7. **write-tickets** to turn the specification into implementation increments. When using plan-feature, you can instead ask plan-feature for implementation tickets and it invokes write-tickets from the planning material. Either way, you approve the ticket set before files are written.

8. **implement** for each ticket. It uses tdd (you approve the test boundaries), runs linting and tests, commits, and runs review-code against the base it recorded and the governing spec or ticket.

9. **review-security** when the feature introduces meaningful trust, authorization, secret, or sensitive-data boundaries.

10. **write-documentation** if the feature changes setup, configuration, commands, or contributor-facing project behavior.

Use **handoff** whenever you need to stop mid-process and continue in a fresh session.

### Debugging a failure

Example: “Notes edited in two tabs occasionally lose the first tab's changes.”

1. **diagnose**, saying whether you want diagnosis only or also authorize a fix. It establishes a reproduction or baseline, tests competing hypotheses (for example, last-write-wins in the save endpoint versus a stale client cache), and writes `docs/diagnoses/<NN>-<slug>.md`.

2. If you authorized a fix and the cause is local, diagnose makes the smallest fix, adds a regression test, and reruns the reproduction. Commit it, then run **review-code** with the commit before the fix as the base.

3. If the cause requires redesign, broader scope, or a contract change, diagnose stops. Continue with **brainstorm** to decide the approach (for example, optimistic locking versus merging), then **write-spec** using the diagnosis as evidence, and **implement**.

4. Add **review-security** when the failure involved a trust boundary, such as one user's edit landing on another user's note.

### Improving existing architecture

Example: “Changes to note permissions keep requiring edits in five modules.”

1. **improve-architecture**, optionally pointed at the area that hurts. It presents unranked, evidence-backed hypotheses in a temporary report.

2. Pick one. It hands off to **review-architecture**, which writes `docs/reviews/architecture/<NN>-<slug>-review.md` with findings and decisions requiring approval.

3. Approve the decisions you accept. review-architecture invokes **domain-modeling** to record them as ADRs and update `CONTEXT.md` or `CONTEXT-MAP.md` if ownership moves.

4. **write-spec** for the restructuring, then **write-tickets**, which splits cross-cutting changes into staged migration tickets that keep the system working between steps.

5. **implement** each ticket.

### Deciding from external facts

Example: “Can we keep SQLite if sync introduces concurrent writers?”

1. **research** runs in the background and writes `docs/research/<topic>/<file>.md` with primary-source citations and explicit open questions.

2. **brainstorm** the decision with the research note as evidence. It surfaces the remaining tradeoffs and leaves the choice to you.

3. **domain-modeling** records the decision as an ADR if reversing it later would be costly.

### Security review of existing code

Example: “Audit how share links are authorized before we expose them publicly.”

1. **review-security** on the share-link boundary. It traces tokens and note data from input to persistence and logging, and writes `docs/security/<NN>-<slug>-review.md` with findings, mitigations, and verification.

2. For small, contained mitigations, **implement** with the review as the requirements. Its tdd step can turn the review's verification items into abuse-case and authorization tests.

3. For mitigations that change behavior or contracts, **brainstorm** the tradeoffs first, then **write-spec** and **write-tickets**.

4. To confirm a suspected exploit before fixing it, run **diagnose** on that finding.

### Small, well-defined change

Example: “Add a `--json` flag to the export command.”

1. **implement** directly with the requirement stated in the conversation. It records a base, uses tdd, validates, commits, and runs review-code.

2. review-code looks for an applicable spec. If none exists, say so and it skips the requirement-fit assessment.

3. **write-documentation** if the flag should appear in the README.

### Continuing across sessions

Example: a plan-feature effort that is halfway through its planning tickets.

1. **handoff** at the end of a session, optionally stating the next focus. It writes `handoff-<slug>.md` to the OS temp directory, points to durable artifacts such as `docs/planning/<feature>/INDEX.md` instead of copying them, and lists suggested skills.

2. In the new session, give the agent the handoff file and run **plan-feature**. It reads `INDEX.md` and resumes with the next actionable ticket.

Because planning, specs, tickets, diagnoses, reviews, and ADRs are all written to `docs/`, a handoff only needs to carry the context that is not already recorded there.
