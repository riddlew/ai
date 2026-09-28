---
name: handoff
description: Create a compact continuation artifact for a fresh agent, preserving only the context needed to resume the current work.
disable-model-invocation: true
---

# Handoff

Use this skill only when explicitly invoked.

Create a compact handoff document that allows a fresh agent to continue the current work without needing the full conversation history.

If the user describes what the next session will focus on, use that purpose to decide what context deserves emphasis.

## Select what to preserve

Summarize only information needed for effective continuation.

Prioritize:

- the current state of the work;
- decisions made during the conversation that are not already persisted elsewhere;
- active constraints and assumptions;
- unresolved questions;
- immediate next work;
- project locations or artifacts the next agent must inspect.

Do not preserve conversational history merely because it occurred.

When a next-session focus is provided, favor information that directly supports that work and omit unrelated context.

## Reference durable artifacts

Before reproducing substantial project information, determine whether it already exists in a durable artifact.

Examples include:

- specifications;
- plans;
- ADRs;
- implementation tickets or issues;
- research documents;
- reviews;
- diagnoses;
- commits;
- diffs;
- other project documentation.

When the relevant information already exists there, reference the artifact by filesystem path or URL instead of copying its contents.

Include only enough explanation to tell the next agent why the artifact matters.

Do not duplicate detailed content that the next agent can recover directly from the referenced artifact.

## Remove sensitive information

Do not place unnecessary sensitive information in the handoff.

Remove or redact:

- credentials;
- passwords;
- API keys;
- access tokens;
- private secrets;
- personally identifiable information;
- other sensitive values not required to continue the work.

When a sensitive item is operationally relevant, describe what the next agent needs to know without reproducing the value itself.

## Suggest useful skills

Include a section titled:

```markdown
## Suggested Skills
```

Name the skills the next agent should invoke for the expected continuation work.

Include only skills that are relevant to the remaining work.

When useful, briefly state what each skill should be used for.

## Write the handoff

Produce one Markdown document.

A useful structure is:

```markdown
# Handoff

## Next Session Focus

<Include when the user supplied one.>

## Current State

<What has been completed and where the work currently stands.>

## Relevant Context

<Only non-duplicated context needed to continue.>

## Existing Artifacts

- `<path-or-url>` — why the next agent should read it

## Unresolved Questions

<Decisions or uncertainties still open.>

## Next Work

<The most relevant continuation steps or investigation areas.>

## Suggested Skills

- `<skill-name>` — intended use
```

Adapt the structure when a different layout makes the continuation clearer.

## Save outside the workspace

Save the handoff in the operating system's temporary directory, not inside the project workspace.

Determine the temporary directory from the current operating system or runtime environment rather than assuming a fixed platform-specific path.

Choose a concise filename derived from the work, for example:

```text
handoff-<short-slug>.md
```

Verify that the final path is outside the project workspace.

Report the saved handoff file location to the user.