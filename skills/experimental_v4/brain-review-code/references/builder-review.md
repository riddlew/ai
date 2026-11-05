# Builder review

A fresh reviewer reads an artifact (spec, ticket set, or impl plan) as the person who must build from it. Used by `brain-write-spec`, `brain-write-tickets`, and `brain-implement`.

## For the author

**Dispatch.** Send one fresh subagent on the standard tier, read-only. Fill every slot. Every path in any slot is absolute. `{artifact}` is the artifact's absolute file path when the file exists; for a draft not yet written, the full draft text. `{glossary_path}` is `glossary.md` in the `.brain/` you are using. `{sources}` holds paths to source files, or text when there is no file. Never pass the conversation or the rest of `.brain`.

**No subagent tool.** Read the artifact yourself as the builder would, then report the `self-read` line below.

**Sort each returned question into one of three piles:**

1. **Answered** by the conversation, the code, or the brain: put the answer into the artifact.
2. **Routine:** a sensible builder could settle it without changing what gets built. Leave it out, as implementation discretion.
3. **Only the user can answer:** ask in one message, most important first, and wait. After the reply, record every question left unanswered as an Open Decision (spec), a blocked ticket (ticket set), or a Blocker (impl plan), and never ask it again. Never settle it to make the artifact look complete, and never reopen a settled decision. Then continue the calling skill's flow.

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

For an `impl plan`, also check:

- the work items cover every governing Example and criterion, in an order that respects dependencies;
- each item is one coherent, testable increment;
- `Review Focus` is complete.

## Rules

- Read-only. Do not edit, stage, commit, or dispatch subagents.
- Do not settle anything by choosing a behavior yourself; ask, do not answer.
