---
name: handoff
description: Create a compact continuation artifact for a fresh agent, preserving verified state, approved decisions, unresolved choices, and the next authorized work.
disable-model-invocation: true
---

# Handoff

Use only when explicitly invoked or when the user requests a cross-session continuation note. Create a concise Markdown handoff that lets a fresh agent resume without reading the whole conversation.

A handoff **transfers context, not authority**. While preparing it, do not make product or architectural decisions, implement anything, or reword proposals as approvals (root `CLAUDE.md`).

If the user specifies the next session's focus, organize the handoff around it.

## Establish the current state

Use the conversation and, where available, repository state and durable artifacts. Verify status claims that may have changed; an earlier plan or agent message is not proof of completion.

Capture only what the next agent needs:

- the objective and completed work;
- where work stopped, preferably by referencing the feature `todo.md`;
- **approved** decisions not already recoverable from a durable artifact;
- known constraints and relevant facts;
- unresolved decisions, competing proposals, and assumptions needing validation;
- the next authorized work and anything blocked on the user;
- essential paths, URLs, commands, and references.

Record the verified branch, commit, working-tree state, and checks run (including failures and checks not run) where relevant. Do not imply code is committed, tests pass, or a file exists without evidence.

## Preserve decision status

Label each decision:

- **Approved** — the user chose it, or project documentation makes it authoritative.
- **Proposed** — recommended by the assistant, not approved.
- **Open** — the user still needs to choose among consequential alternatives.
- **Unverified** — a factual claim not yet established from evidence.

For each open choice, state the question, alternatives, evidence, and whether work must pause for the answer.

## Reference existing records

When work is implemented from a specification or tickets, read `docs/implementation/<feature>/todo.md` and `guidance.md` if present, and verify important claims against the repository. Reference these files with one sentence on the immediate continuation need; do not copy them or create a second status tracker. If a record is demonstrably stale and editing it is in scope, correct the record first.

The living records may make a separate handoff unnecessary, but when the user invoked this skill, still create a compact handoff focused on context **not already** in those records (for example, a next-session focus or a transient environment limitation).

Reference other artifacts (specifications, planning tickets, ADRs, context documents, reviews, diagnoses, commits) by **verified** path, URL, or commit, noting whether each records a decision, evidence, or a proposal. Include concise critical context only if the source will not be accessible next session. Do not create repository documentation for the handoff.

Never include secrets, credentials, tokens, private keys, or personal data; describe access requirements instead.

## Write the handoff

Adapt the structure to the work; omit empty sections other than Suggested Skills.

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

Name only installed or known skills under Suggested Skills; naming one does not authorize running it.

## Save outside the workspace

Save to the operating system's temporary directory, discovered from the runtime rather than hard-coded, as `handoff-<short-slug>.md`, without overwriting an unrelated handoff. Verify the file exists outside the project workspace and report its path. Note that the temporary location may not persist and the next session will not have it automatically.
