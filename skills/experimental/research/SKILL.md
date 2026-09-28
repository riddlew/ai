---
name: research
description: Investigate a focused question using authoritative primary sources and save the findings as a traceable Markdown research note under docs/research/.
---

# Research

Use this skill to investigate a user-provided question that requires factual research.

Run the research in a **background agent** so the parent session can continue other work.

Store the finished result under:

```text
docs/research/<research-name-stub>/
```

Derive `<research-name-stub>` from the topic using a concise, filesystem-safe name.

Produce exactly one Markdown research document for each research effort.

## Source standard

Prefer the primary source that owns or defines the fact being investigated.

Use sources such as:

- official documentation;
- specifications and standards;
- source code;
- first-party APIs;
- other first-party technical material.

Do not rely on a secondary summary when the underlying primary source is available.

Trace substantive factual claims back to the authoritative source that supports them.

## Research process

Give the background agent:

- the research question;
- relevant context from the current conversation;
- any user-provided constraints or source material;
- the required output directory.

The agent should:

1. Identify the authoritative sources relevant to the question.
2. Investigate the question against those sources.
3. Verify factual claims directly against the supporting primary material.
4. Record the findings in one Markdown file.
5. Cite each substantive factual claim closely enough that its supporting source can be located and checked.
6. Record any unresolved uncertainty explicitly.

Do not invent missing facts or fill gaps with plausible assumptions.

## Uncertainty

If evidence for a point is ambiguous, incomplete, conflicting, or cannot be verified confidently:

1. stop drawing conclusions about that point;
2. identify exactly what is uncertain;
3. explain why the available evidence is insufficient;
4. consult the user before relying on an assumption or interpretation.

Do not silently choose between conflicting sources or infer an answer that the sources do not establish.

Research that can be completed independently may continue while clarification is needed on an unrelated point.

## Research document

The document must contain:

- the research findings;
- source references sufficient to trace substantive factual claims to their authoritative primary sources;
- unresolved uncertainties, when any remain.

Choose whatever Markdown structure and citation format best fit the research.

A typical result may look like:

```markdown
# <Research topic>

## Findings

<Findings with inline or nearby source references.>

## Unresolved Questions

<Only include when relevant.>

## Sources

<Primary sources used during the research.>
```

The exact filename is flexible, but there must be only one research Markdown file inside:

```text
docs/research/<research-name-stub>/
```

Keep the document focused on evidence relevant to the research question rather than producing a general survey of the topic.
