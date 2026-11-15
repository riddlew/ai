# Implementation plan: composable voices for `write-human`

Status: **Approved proposal; implementation not started.**

## Goal

Expand `write-human` from one selected voice to an ordered pair of at most two voices, add six new voice profiles, and document recommended combinations in `README.md`. Preserve the skill's required explicit `voice` and `mode` configuration and its factual-fidelity guarantees.

## Existing state

The current skill on `main` has:

- `SKILL.md`: required single voice and `mode=preserve|flexible`; questions for missing settings; voice precedence; read-only input handling; final-text-only output.
- Four profiles: `software-engineer.md` (`swe`), `technical-writer.md`, `business.md`, and `academic.md`.
- `references/ai-writing-patterns.md` and `references/fidelity.md`.
- `tests/acceptance.md` with existing manual behavior checks.
- Attribution and MIT license inherited from `blader/humanizer`.

Existing safeguards and license attribution must remain intact.

## Scope and non-goals

**In scope:** ordered voice composition, six additional voice profiles, `README.md`, updated frontmatter and usage guidance, and expanded manual acceptance checks.

**Out of scope:** implementation changes to `brain-distill-content`, changes to factual-fidelity policy or the 26-pattern reference, extra mandatory preference questions, automated persona generation, new summarization modes, combining more than two voices, and combination-specific profile files.

## Required behavior and contracts

### Configuration and parsing

Accept one voice or a two-voice ordered pair in `voice=primary+secondary`, along with `mode=preserve|flexible`.

Examples:

```text
/write-human voice=swe mode=flexible
/write-human voice=swe+educator mode=flexible
/write-human voice=educator+swe mode=preserve
/write-human voice=legal+technical-writer mode=preserve
/write-human voice=swe+custom:"direct and conversational" mode=preserve
```

Also accept explicit natural-language settings and the existing `software-engineer` alias for `swe`. A custom voice requires its own description; quote or otherwise clearly delimit descriptions containing spaces or `+`. For a custom-first pair, `voice=custom:"..."+swe` is equivalent to selecting that described voice as primary.

Voice vocabulary:

- Standalone general: `general` (no profile file).
- Existing: `swe`, `technical-writer`, `business`, `academic`.
- New: `casual`, `educator`, `product-manager`, `journalist`, `marketing`, `legal`.
- User-described: `custom:<description>`.

Validation:

1. Require an **explicit** voice and mode on **every invocation**. Never infer or default them from the text, audience, prior unrelated turns, or a writing sample.
2. One voice is valid. Two **distinct** voices are valid when ordered and compatible with the rules below.
3. `general` is standalone: reject `general+swe` and `swe+general`; ask for one specialized voice or `general` alone.
4. At most one custom voice is allowed in a pair. Reject two custom voices and ask to combine their descriptions into one if desired.
5. Reject three or more voices and duplicate pairs (for example, `swe+swe`); do not silently discard entries.
6. Reject unknown voice names, an undescribed custom voice, and an unknown editing mode. Explain the valid choices and ask only for correction of invalid or missing settings.
7. Ask for **all** missing settings in one interaction. If voice is valid but mode is missing, ask only for mode; if mode is valid but voice is missing, ask only for voice. Do not rewrite until configuration is complete.
8. Keep existing `preserve` and `flexible` semantics exactly. Voice combination does not increase permission to compress away unique substantive information.

### Composition and precedence

- **Primary voice** establishes the dominant register, disciplinary vocabulary, and editorial priorities.
- **Secondary voice** refines presentation for a second purpose, such as teaching, informality, or product context. It may not silently replace primary-voice conventions.
- `swe+educator`: engineering-oriented explanation that is easier to learn from.
- `educator+swe`: teaching-oriented explanation that retains accurate engineering terminology.
- Reverse order may result in different editorial emphasis; it must **never** alter factual content.

Precedence for competing style instructions:

1. Factual, technical, logical, and source-fidelity rules are non-negotiable.
2. Explicit user directions.
3. User-provided writing sample.
4. Primary voice.
5. Secondary voice.
6. General writing guidance.

The primary voice resolves ordinary stylistic conflicts. Preserve ambiguity instead of guessing; ask a targeted question only when conflicts or ambiguity make faithful rewriting impossible. Voice combination must never create new facts, jargon, personal experience, technical requirements, citations, examples, or claims that were absent from the input. Load only the selected profile files.

### Output

Keep the existing behavior: return only the final rewritten prose (or the minimal confirmation required for an explicitly authorized file edit). No intermediate drafts or commentary.

## Implementation steps

### 1. Update `SKILL.md`

Modify only the relevant sections:

- Frontmatter `description` and `argument-hint`: list new voices, ordered composition syntax, and existing editing modes, without obscuring activation semantics.
- **Required configuration**: define one/two-voice grammar, examples, aliases, `general` standalone rule, custom-voice description requirements, invalid/ambiguous input handling, and no-default questions for missing settings.
- **Choose the explicitly specified voice**: add the six new profile mappings, load both selected profiles only, and document composition and precedence.
- **Rewrite workflow / final fidelity gate**: ensure both selected profiles are consulted, the primary voice takes priority for stylistic conflicts, and meanings/claims remain unchanged.
- Leave input safety, mode definitions, output-only behavior, and fidelity references unchanged except for cross-reference wording needed for composition.

Acceptance: existing `voice=swe mode=flexible` invocation behaves as before; `voice=swe+educator mode=flexible` selects two profiles in primary-first order.

### 2. Add six independent voice files

Create under `references/voices/`:

| File | Specialized focus | Guardrail |
| --- | --- | --- |
| `casual.md` | Natural, conversational communication and chat | No forced slang, jokes, or fabricated anecdotes |
| `educator.md` | Clear concept progression and accessible explanations | No invented examples, definitions, or missing prerequisites |
| `product-manager.md` | Product goals, scope, user behavior, and tradeoffs | No invented requirements, commitments, or prioritization |
| `journalist.md` | Direct, evidence-driven reporting and attribution | No invented quotes, sources, dates, or causal claims |
| `marketing.md` | Audience-aware persuasive language and product framing | No unsupported benefits, superlatives, guarantees, or performance claims |
| `legal.md` | Clear legal and policy prose with exact obligations | No altered definitions, exceptions, rights, scope, or legal implications |

Follow the pattern of existing voice files: heading, appropriate usage, style rules, avoidance rules, and a short before/after example. Each profile must function independently and should not mention specific combinations. Keep examples factually faithful.

Acceptance: all new profile paths exist, are independently understandable, and alter style without changing the underlying meaning.

### 3. Add `README.md`

Create `skills/experimental_v4/write-human/README.md` as a **user-facing guide** (the behavioral contract remains in `SKILL.md`).

Contents:

1. Purpose and distinction from summarization / `brain-distill-content`.
2. Quick-start commands for one voice, two voices, custom voice, and both editing modes.
3. Voice reference table for general + all ten specialized voices + custom; list concise strengths and typical use.
4. `preserve` vs. `flexible`, with explicit no-default rule and clarification behavior.
5. How ordered composition works; include a direct comparison of `swe+educator` and `educator+swe`.
6. A **curated catalog of useful combinations and expected results**, including at least:

| Combination | Expected result |
| --- | --- |
| `swe+educator` | Experienced engineer explaining technical concepts |
| `educator+swe` | Teaching-first technical explanation retaining engineering precision |
| `swe+casual` | Natural engineering chat or PR comments |
| `swe+product-manager` | Engineering explanation with product implications |
| `technical-writer+swe` | Structured engineering documentation |
| `technical-writer+educator` | Instructional developer guides |
| `technical-writer+legal` | Readable documentation preserving policy constraints |
| `product-manager+swe` | Product requirements with technical precision |
| `product-manager+educator` | Product concepts explained to stakeholders |
| `product-manager+business` | Product decisions framed for business stakeholders |
| `product-manager+marketing` | Grounded product announcements |
| `business+casual` | Natural professional emails or updates |
| `business+marketing` | Professional persuasive commercial writing |
| `business+legal` | Business correspondence with legal precision |
| `casual+marketing` | Conversational promotional copy |
| `casual+educator` | Friendly, understandable explanations |
| `educator+academic` | Accessible scholarly explanations |
| `academic+educator` | Rigorous teaching in an academic voice |
| `academic+journalist` | Research-focused reporting |
| `journalist+academic` | Evidence-driven articles with academic nuance |
| `journalist+casual` | Conversational reporting |
| `journalist+educator` | Explanatory journalism |
| `journalist+business` | Professional business reporting |
| `marketing+casual` | Approachable product messaging |
| `legal+technical-writer` | Clear legal or compliance instructions preserving legal meaning |
| `legal+business` | Formal commercial/legal correspondence |

The catalog is **illustrative, not exhaustive**. Other valid ordered pairs remain supported. Include examples in both directions only where the different emphasis is meaningful.

7. Constraints, invalid combinations, and reminder that safety and fidelity rules override both voices.
8. Existing `humanizer` attribution, linked to the separate `ATTRIBUTION.md` and `LICENSE` rather than duplicating license text.

Acceptance: every combination in the catalog uses recognized voice names and accurately describes the intended priority order. All six new voices and four existing specialized voices appear in the voice table.

### 4. Expand `tests/acceptance.md`

Preserve the existing checks and add tests for:

- Single-voice backward compatibility.
- Ordered pair parsing and loading only the selected profiles.
- Both orderings of `swe+educator` with the same input: expected style differences, identical factual assertions.
- Both orderings of `legal+technical-writer` with identical legal obligations.
- One or more missing settings: ask only for missing inputs, no defaults.
- Three voices, duplicates, `general` combinations, `custom+custom`, unknown names, missing custom description, and malformed pairs: ask for correction without rewriting.
- Custom primary and custom secondary with clearly delimited descriptions.
- `preserve` vs. `flexible`: structural differences without unique information loss.
- `marketing`: no invented benefits, metrics, or guarantees.
- `journalist` and `academic`: no invented citations, quotes, or evidence.
- `educator`: no new technical examples or unsupported explanations.
- `product-manager`: no invented requirements, success criteria, or decisions.
- `legal`: unchanged obligations, exceptions, and legal definitions.
- Unchanged code snippets, commands, identifiers, data, citations, and URLs.
- Prompt-injection text inside source stays source content, never instructions.
- Final output is only the rewrite.

Use representative source fixtures: technical RFC, instructional content, product announcement, and policy/commercial text. Prefer behavior-based criteria rather than exact expected wording.

Acceptance: all tests are documented; run behavioral checks in a capable agent runtime during implementation and record any failures.

### 5. Review and verify

1. Check `SKILL.md` frontmatter and linked profile paths.
2. Verify the README references every profile and uses the same syntax and precedence rules as `SKILL.md`.
3. Verify all original acceptance checks still apply.
4. Compare output from `voice=swe`, `voice=swe+educator`, and `voice=educator+swe` on identical technical input.
5. Verify both `mode=preserve` and `mode=flexible` and invalid/missing configuration paths.
6. Perform source-to-rewrite fidelity checks for modal verbs, conditions, guarantees, negations, IDs, code blocks, references, and uncertainty.
7. Confirm the original MIT `LICENSE` and `ATTRIBUTION.md` are unchanged.

**Done when:** the skill supports any permitted ordered pair, every new profile is present and linked, the README documents all selected combinations and their expected style, old invocations still work, and tests show no newly introduced factual/technical regressions.

## Planned file changes

- Modify: `SKILL.md`
- Modify: `tests/acceptance.md`
- Add: `README.md`
- Add: `references/voices/casual.md`
- Add: `references/voices/educator.md`
- Add: `references/voices/product-manager.md`
- Add: `references/voices/journalist.md`
- Add: `references/voices/marketing.md`
- Add: `references/voices/legal.md`

**Total implementation changes: 9 files (7 new, 2 modified).** This plan file is separate from those changes.

## Implementation order

1. Update skill configuration and composition rules.
2. Add all six voice profiles.
3. Write the user-facing README and combinations table.
4. Expand acceptance checks.
5. Run comparisons and fidelity verification; refine only observed problems.

Do not implement the skill changes while drafting this plan.
