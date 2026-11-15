# Write Human

Rewrite existing prose to sound natural, clear, and appropriate for its audience without introducing new facts or changing what the source means. Based on [blader/humanizer](https://github.com/blader/humanizer); see [ATTRIBUTION.md](ATTRIBUTION.md) and [LICENSE](LICENSE).

This skill **rewrites**; it does not produce new content or summarize away unique information. If the task is to distill technical material into the shortest faithful version, use `brain-distill-content` instead.

## Quick start

Every invocation requires **two explicit settings**: `voice` and `mode`. Neither has a default.

```text
/write-human voice=general mode=preserve
/write-human voice=swe mode=flexible
/write-human voice=swe+educator mode=preserve
/write-human voice=educator+swe mode=flexible
/write-human voice=legal+technical-writer mode=preserve
/write-human voice=custom:"clear and slightly playful" mode=preserve
/write-human voice=swe+custom:"direct and conversational" mode=flexible
```

Supply text or a path with the command, or identify the source in the same conversation. If voice, mode, source, or a custom description is missing, the skill asks rather than assuming. `software-engineer` is an alias for `swe`. Source file paths are **read-only** unless you explicitly request an in-place edit.

## Voices

Choose one, or use `primary+secondary` for two distinct voices. `general` must be used alone.

| Voice | Best for |
| --- | --- |
| `general` | No specialized profile; audience-appropriate prose |
| `swe` | Engineering discussions, RFCs, reviews, and technical design |
| `technical-writer` | Guides, reference documentation, and instructions |
| `business` | Stakeholder updates, correspondence, and proposals |
| `academic` | Scholarly and research-oriented writing |
| `casual` | Everyday messages and informal conversation |
| `educator` | Clear teaching and conceptual explanations |
| `product-manager` | Requirements, product behavior, and product decisions |
| `journalist` | Attributed factual reporting and explainers |
| `marketing` | Supported product and promotional messaging |
| `legal` | Precise contracts, policies, and compliance prose |
| `custom:<description>` | User-defined voice, including a specific style or field |

Custom voices need a description. When a custom description includes spaces or `+`, quote or clearly delimit it: `voice=custom:"direct + thoughtful"+swe`.

## Editing modes

| Mode | What it changes | What it keeps |
| --- | --- | --- |
| `preserve` | Wording, rhythm, clarity, and local flow | Detail, headings, lists, organization, technical context, nuance |
| `flexible` | May substantially shorten, combine, or reorder prose and sections | Every distinct substantive claim, condition, requirement, exception, limitation, relevant example, and citation |

Flexible mode is **not summarization**. Neither mode permits new facts, technical claims, unsupported examples, invented quotations, or changed certainty. Both preserve code, commands, identifiers, links, metrics, conditions, guarantees, and ambiguity.

## How combinations work

`voice=primary+secondary` selects at most two voices:

- **Primary** determines the dominant register, vocabulary, and professional perspective.
- **Secondary** adjusts expression for a complementary purpose, without overriding the primary.
- **Order matters.** `swe+educator` reads like an engineer explaining a topic; `educator+swe` reads like an instructor who keeps engineering terminology accurate.
- Explicit user directions and a supplied writing sample override voice choices for **style**. Source fidelity overrides everything.

`general` does not combine with other voices; `general+swe` and `swe+general` are invalid. Duplicate voices, combinations of more than two, two custom voices, unknown names, and missing custom descriptions are invalid. The skill asks for correction instead of silently changing the choice.

## Useful voice combinations

These are examples, **not a whitelist**. Any other valid ordered pair may be used. Reversing the order changes which style is dominant.

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

### Compare `swe+educator` and `educator+swe`

Both must preserve the same technical facts. The first emphasizes engineering vocabulary and practical precision, using the educator voice to improve conceptual flow. The second emphasizes an instructional sequence and reader comprehension, using the SWE voice to keep technical details exact. Neither can add analogies, examples, or background information unsupported by the source.

## Questions, safety, and output

The skill asks for any missing required settings together. During rewriting, it normally preserves ambiguous wording; it asks a narrow question only if a consequential ambiguity cannot be carried through safely.

It detects formulaic AI writing patterns without banning words or punctuation, then performs a factual and technical fidelity check. It returns **only the final rewritten content** (or a minimal confirmation of an explicitly authorized file edit), without intermediate drafts or a list of pattern findings.

See [SKILL.md](SKILL.md) for authoritative behavior, [references/fidelity.md](references/fidelity.md) for preservation requirements, and [tests/acceptance.md](tests/acceptance.md) for manual checks.
