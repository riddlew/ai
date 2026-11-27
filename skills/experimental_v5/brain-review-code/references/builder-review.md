# Builder review

A fresh reviewer reads a specification, component set, implementation plan, executable task set, or execution work-item set as the builder who must act on it. Used by `brain-write-spec`, `brain-decompose-feature`, `brain-design-implementation`, `brain-write-tasks`, and `brain-implement`.

## For the author

**Confirm execution mode:** Inherit the user's confirmed inline/subagent choice from the invoking workflow, per `CLAUDE.local.md` §Execution mode selection. If none exists, the invoking skill must ask and wait. **Inline is recommended: read the artifact in the current session; never dispatch a subagent unless the user explicitly chose subagents.** In subagent mode, send one fresh standard-tier read-only reviewer. Fill every slot. Every path in any slot is absolute. `{artifact}` is the artifact's absolute file path when the file exists; for a draft not yet written, the full draft text. `{glossary_path}` is `glossary.md` in the `.brain/` you are using. `{sources}` holds paths to source files, or text when there is no file. Never pass the conversation or the rest of `.brain`.

**Inline mode:** Read the artifact yourself as the builder would, then report the `self-read` line below. **Subagents unavailable:** ask before switching modes; never claim a fresh independent reviewer when none ran.

**Sort each returned question into one of three piles:**

1. **Answered** by the conversation, the code, or the brain: put the answer into the artifact.
2. **Routine:** a sensible builder could settle it without changing what gets built. Leave it out, as implementation discretion.
3. **Only the user can answer:** ask in one message, most important first, and wait. After the reply, record every question left unanswered as an Open Decision (specification), a blocked component/task when its scope requires a new user decision, or an execution Blocker (implementation plan / work-item set), and never ask it again. Never settle it to make the artifact look complete, and never reopen a settled decision. Then continue the calling skill's flow.

**Report** one line, with the counts:

- `Builder review: fresh standard-tier reviewer — <n> questions (<a> answered, <r> routine, <u> to user)`
- `Builder review: self-read (no fresh reviewer) — weaker than an independent review`

**Re-review.** Answers to the review's questions, and edits made from its findings, do not trigger another review. A structural revision gets one more review before the artifact is used. That review may ask the user only questions not asked before. Each calling skill defines its own structural revisions.

---

You are reviewing a {artifact_kind} in `{repo_root}`. Read it as a builder who must build from it without asking anyone.

## Artifact

{artifact}

## Sources

{sources}

Canonical terms: read `{glossary_path}` if it exists.

## What to find

Return a numbered list, most important first. Each item gives:

- the location in the artifact;
- what is unclear, contradictory, or missing, including unstated failure behavior;
- why two builders would build different things from it.

For an `implementation plan` or `blueprint`, also check:

- cited files, owners, and proposed signatures are grounded in inspected code, not invented;
- approved requirements and architectural constraints are preserved, while proposals and illustrative snippets are not silently treated as binding;
- important changed interfaces, lifecycle, failure behavior, compatibility, and intentionally unchanged boundaries are clear;
- proposed increments are coherent, reviewable, and verifiable, with a plausible path to satisfying each governing Example or criterion;
- any unresolved consequential design decision is explicitly blocked rather than guessed.

For a `component set`, also check:

- every approved requirement is mapped to coherent functional ownership, including failure cases;
- interactions and overlapping responsibilities are explicit, without inventing a class/service design;
- unknown consequential boundaries remain blocked rather than silently decided.

For a `task set`, also check:

- tasks derive from approved technical plans and governing requirements, not speculative architecture;
- every planned increment and applicable Example maps to independently verifiable work;
- dependencies are genuine and acyclic, with blocking choices clearly identified.

For an `execution work-item set`, also check:

- work items cover each approved task and governing Example/criterion;
- each item is a coherent testable increment respecting real dependencies;
- `Review Focus` covers uncovered failures and blocked decisions;
- mutable progress is separate from approved implementation plans.

## Rules

- Read-only. Do not edit, stage, commit, or dispatch subagents.
- Do not settle anything by choosing a behavior yourself; ask, do not answer.
