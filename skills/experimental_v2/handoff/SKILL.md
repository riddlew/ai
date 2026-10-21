---
name: handoff
description: Create a compact continuation artifact for a fresh agent, preserving verified state, approved decisions, unresolved choices, and the next authorized work.
disable-model-invocation: true
---

# Handoff

Use this skill only when explicitly invoked or when the user expressly requests a durable cross-session continuation note. Do not generate a handoff after every task.

Create a concise Markdown handoff that lets a fresh agent resume the current work without reading the entire conversation. A handoff **transfers context, not decision-making or implementation authority**. Follow root `CLAUDE.md` when classifying established and open decisions. Do not make new product or architectural decisions, perform implementation, or reinterpret proposals as approvals while preparing it.

If the user specifies the next session's focus, organize the handoff around that focus.

## Establish the current state

Consult the current conversation and, when available, the relevant repository state and durable artifacts. Verify status claims that could have changed, rather than treating an earlier plan or agent message as proof of completion.

Capture only what the next agent needs:

- The current objective and completed work.
- The exact point where work stopped, preferably by referencing the feature `todo.md` when available.
- Explicitly **approved** product and architectural decisions not already recoverable from a durable artifact.
- Known constraints and relevant facts.
- Unresolved decisions, competing proposals, and assumptions that still need validation.
- The next authorized work and any action blocked on user consultation.
- Paths, URLs, commands, or repository references essential to resuming.

Where relevant, record the verified branch, commit, working-tree state, and tests or checks run (including failures or checks not run). Do not imply that code is committed, tests pass, or a file exists unless the evidence supports it.

## Preserve decision status

Keep these distinct:

- **Approved:** The user explicitly chose the direction, or the decision is already authoritative in project documentation.
- **Proposed:** The assistant recommended it, but the user has not approved it.
- **Open:** The user still needs to decide among consequential alternatives.
- **Unverified:** A factual claim or assumption has not been established from evidence.

A recommendation, brainstorm result, review finding, tentative agreement, or unaccepted design is not automatically an approved decision. Never turn one into a requirement by how you phrase the handoff.

If a consequential choice remains open, state the concrete question, relevant alternatives, evidence, and whether work must pause for the answer. Do not choose on behalf of the user.

## Prefer the feature's living implementation records

When the work is being implemented from a spec or ticket set, check for the feature workspace under `docs/implementation/` and read:

- `todo.md` for current progress, blockers, verification, next task, and original Git review base;
- `guidance.md` if it exists for verified discoveries and references to established decisions.

Verify important status claims against repository evidence where accessible. **Do not create a second status tracker in the handoff**, repeat the todo checklist, or copy the guidance file. Reference their paths with a one-sentence explanation of the immediate continuation need. If an existing record is demonstrably stale and editing it is within scope, correct that record first rather than preserving conflicting status in the temporary handoff.

The living files may eliminate the need for a separate handoff entirely; nevertheless, when the user explicitly invoked this skill, create the requested compact temporary handoff, focused on context **not already present** in the feature records (for example, a specific next-session focus or transient environment limitation).

## Reference durable artifacts

Before repeating detailed context, locate relevant existing sources, such as specifications, planning tickets, ADRs, context documents, reviews, diagnoses, research notes, commits, and diffs.

Reference them by a **verified** path, URL, or commit identifier. Briefly explain why each matters and whether it records a decision, evidence, or a proposal. Prefer references over copied content, but include concise critical context if the source will not be accessible in the next session.

Do not duplicate large files or create new repository documentation just for this handoff.

## Protect sensitive information

Do not include secrets, credentials, access tokens, private keys, personal data, or unrelated sensitive values. Describe relevant configuration or access requirements without reproducing secrets.

## Suggest continuation skills

Include a `## Suggested Skills` section naming only installed or otherwise known relevant skills. Explain their intended use briefly. Naming a skill does not authorize its execution or bypass its consultation rules.

## Write the handoff

Create one Markdown document. Adapt the structure to the actual work; omit empty sections other than Suggested Skills.

```markdown
# Handoff

## Next Session Focus

<Only when supplied or clearly established.>

## Current State

<Verified progress and point of continuation.>

## Approved Decisions and Constraints

<Only essential decisions not adequately recorded elsewhere.>

## Existing Artifacts

- `docs/implementation/<feature>/todo.md` — verified progress and next work, if present
- `docs/implementation/<feature>/guidance.md` — current implementation discoveries, if present
- `<other-verified-path-or-reference>` — purpose and status

## Unresolved Decisions and Uncertainty

<Separate questions requiring user approval from factual gaps.>

## Next Work

<Concrete next steps; identify which actions are already authorized.>

## Suggested Skills

- `<skill-name>` — relevant use
```

## Save outside the workspace

Save the file in the operating system's temporary directory, discovered from the active runtime rather than hard-coded. Use a concise name such as `handoff-<short-slug>.md` and avoid overwriting an unrelated existing handoff.

Verify that the saved file exists and is outside the project workspace. Report its actual path. Mention that the temporary location may not persist indefinitely; do not claim the next session will automatically have access to it.
