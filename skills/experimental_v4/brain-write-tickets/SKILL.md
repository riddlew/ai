---
name: brain-write-tickets
description: Decompose an approved specification, plan, or discussion into small, independently verifiable implementation tickets with genuine dependencies, after the user approves the proposed set. Use when the user asks for tickets, or approved work spans multiple sessions or independently deliverable increments.
---

# Write Tickets

**Project brain:** If `.brain/00_index.md` exists (at this worktree's root, or in the main checkout when working in a linked git worktree) and you have not read its root files in this session (or they were lost to context compaction), read every root `.md` file in that `.brain/` now. Read subfolders only when a root file links to them or the task needs them. Do not load `.brain` into subagents wholesale; pass only what their task needs. Write any `.brain/` document into that same `.brain/`. If no brain exists, proceed without one and mention once that `/brain-update` can create it.

Convert established requirements into the **smallest practical set of independently verifiable delivery increments**. Follow root `CLAUDE.md`: tickets describe authorized outcomes and cannot settle unresolved behavior or approve a redesign.

Use this skill only when the user requests tickets or a long-running workflow delegates ticket generation. If one ticket would merely restate the specification, recommend implementing from the specification directly.

## 1. Gather the evidence

Read the relevant conversation, approved planning material, specifications (including their Examples), and referenced sources fully enough to preserve their intent. Read `.brain/glossary.md`, `.brain/03_architecture.md`, relevant ADRs in `.brain/adrs/`, existing tests, verification patterns, and public boundaries.

Keep separate:

- **Approved requirements and decisions** — binding inputs.
- **Repository facts** — how the system works today.
- **Recommendations** — possible approaches, not constraints.
- **Open choices** — decisions requiring the user.

## 2. Identify independently observable capabilities

Each ticket should:

- deliver one coherent, observable, independently verifiable behavior;
- cross database, backend, UI, configuration, and test layers as needed to complete it;
- fit in a fresh agent context;
- verify consistently with the specification and project testing patterns;
- add nothing unrequested.

Do not split by implementation layer or manufacture a large set for a small feature.

## 3. Preserve approved architecture

Use existing owners, code paths, and decisions as the starting hypothesis. Decomposition cannot approve a structural change by turning it into a preparatory ticket; an "Extract X" ticket ahead of work that could extend the existing owner needs a demonstrated reason and the user's approval.

Consult the user before adding tickets that would:

- move or divide lifecycle, state, or domain ownership;
- introduce a new manager, service, layer, or significant dependency;
- change established interfaces, persistence formats, or observable behavior;
- require an unapproved migration or broad restructuring;
- choose unresolved product semantics, scope, or architecture.

Present the constraint, the minimal approach within existing architecture, any larger option, tradeoffs, and a recommendation; wait for the decision.

## 4. Construct genuine dependencies

Add a dependency only when a ticket cannot deliver its outcome until another is complete. Do not serialize independent capabilities.

Stage an **approved** cross-cutting migration so intermediate states stay valid: introduce a compatible mechanism, migrate consumers in verifiable groups, then remove compatibility support. Do not propose compatibility layers or generalized interfaces without concrete migration requirements.

Number tickets in dependency-consistent order; numbering itself is not a dependency.

## 5. Check, review, and obtain approval

Do these in order, before creating files. Consult on §3 architecture questions before drafting, outside the one approval message.

1. **Draft the set.** Draft each proposed ticket with:
   - **Title** — the behavioral increment.
   - **Depends on** — genuine prerequisites, or none.
   - **Outcome** — what becomes observable or verifiable.
   - **Examples covered** — specification example IDs, when a specification exists.
   - **Architectural implications** — consequential changes needing approval, or "existing boundaries preserved".
2. **Self-check.** Fix the drafts until:
   - a coverage table maps each spec Example and each invariant to the ticket(s) that cover it, with none left without a ticket. Without a spec, number the approved requirements from the plan or discussion `R1`, `R2`, … and map those;
   - every acceptance criterion references Examples or states an observable result;
   - names and terms are consistent across tickets, and with the spec and `.brain/glossary.md`;
   - dependencies are genuine and acyclic.

   Then list the failure cases that no Example or criterion covers. Each becomes an acceptance criterion when approved requirements determine its outcome. Otherwise it is a question for the user. The list is not saved after approval.
3. **Builder review.** Follow `${CLAUDE_SKILL_DIR}/../brain-review-code/references/builder-review.md`, with `ticket set` as `{artifact_kind}`. `{sources}` is the spec, or the approved plan or discussion text when there is no spec. `{artifact}` is the draft text, since no files exist yet.
4. **One approval message.** It must contain all of:
   - the set;
   - the coverage table;
   - the uncovered failure cases and what happened to each;
   - the `Builder review:` line;
   - any questions only the user can answer. Each one left unanswered becomes a blocked ticket or a blocked note on the affected ticket.

Revise until the user approves. A revision that adds, splits, or merges tickets gets one more builder review before approval; answers to review questions do not. If the user already supplied and approved the exact decomposition, the self-check and review still run. The one message then becomes a report with the same contents, minus the approval request. Write files without a fresh approval unless the review changed the set structurally (added, split, or merged tickets) or raised questions only the user can answer; in those cases ask for approval in that message. Approval of the set does not approve an architectural decision that was neither disclosed nor established.

## 6. Write approved tickets

Create one file per ticket at `.brain/tickets/<feature-slug>/<NN>-<slug>.md`, numbering from `01`. When continuing an existing set, follow its numbering and do not overwrite unrelated files.

```markdown
# <NN>: <Ticket Title>

## Outcome

<One complete capability or verifiable result.>

## Dependencies

<Prerequisite ticket numbers and titles, or None.>

## Acceptance Criteria

- [ ] Satisfies specification examples E1–E3 (`.brain/specs/<NN>-<slug>.md`, Examples).
- [ ] <Observable result not covered by a specification example.>

## Governing Decisions

<References to the approved specification, planning result, or ADR.
Include only essential boundaries not recoverable from those sources.>
```

**Acceptance criteria reference specification Examples by ID** instead of restating them. Add a criterion only for behavior the Examples do not cover. Without a specification, write each criterion as an observable result derived from established requirements. Describe results, not coding steps.

Omit Governing Decisions when the sources are unmistakable from context. Do not embed volatile source paths or implementation snippets unless an approved prototype fragment preserves a design contract. If a consequential decision is unresolved, do not write a ticket that assumes an answer; record the block and consult.

Tickets are stable definitions; `brain-implement` tracks execution progress separately once work starts.

Write only the ticket files into `.brain/`; leave the index, `state.md`, and other root files to `brain-update`. Then invoke `brain-update` with a one-line summary of what changed.

Report the created ticket paths, actionable tickets, and remaining dependencies or blockers. Do not begin implementation unless separately authorized.
