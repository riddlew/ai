# Fidelity rules

Use for **every** rewrite. These rules override any example or heuristic in the pattern catalog.

## Do not add facts

Do not introduce facts, technical claims, examples, citations, invented first-person experience, missing background, or causal explanations not in the input, even if plausible or personally known. Treat claims as reported by the source, not independently verified. Do not imply that code, sources, tests, or documents have been checked unless the provided source itself says they have.

## Preserve logic, certainty, and scope

Compare the source and draft for changes in:

- Obligation and confidence: must, should, may, might, optional, required, guaranteed, best-effort.
- Conditions and exceptions: if, unless, only, and/or, negation, fallback, precedence, exclusions.
- Who and what: ownership, actor, component, user group, supported environment, version, scope.
- Time: before/after, ordering, concurrency, deadlines, timeouts, asynchronous/synchronous, retries.
- Failure behavior: status, error handling, partial failures, consistency and recovery guarantees.
- State of knowledge: implemented vs proposed, observed vs hypothesized, claimed vs verified.
- Evidence: names, numbers, units, percentages, exact values, dates, citations, quotations, links.
- Interfaces: API names, types, function names, CLI flags, paths, environment variables, configuration keys, data formats, schemas, code and commands.
- Unique examples, edge cases, caveats, limitations, assumptions, rationale, warnings and contradictions.

Never strengthen uncertain claims or weaken requirements to make prose smoother. Do not silently resolve inconsistencies.

## Preserve non-prose exactly

Keep code fences, inline code, code samples, commands, literals, citations, anchors, URLs, Markdown link targets, machine-readable metadata, and verbatim quotations intact. For file edits, do not rewrite technical artifacts as if they were narrative prose.

## Editing intensity boundaries

- **Preserve:** Retain the original's meaningful details, structure, headings, lists, and examples; make local changes for clarity.
- **Flexible:** You may reorganize and aggressively cut duplicated wording or examples that communicate no additional point. Preserve every distinct material claim and its associated conditions and references.
- In neither mode is silence permission to produce a summary or discard unique technical context.

## Check before returning

Ask: What new fact became true? What source fact disappeared? Did modality, timing, scope, status, negation, ownership, or certainty change? Did a citation or exact technical token change? Did the edit respect the selected mode? Correct all discrepancies.

When an ambiguity cannot be rewritten faithfully, ask a narrow question. Otherwise preserve the ambiguity and proceed.
