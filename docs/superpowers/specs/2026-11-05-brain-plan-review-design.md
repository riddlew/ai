# Design: builder reviews for specs, tickets, and impl plans (experimental_v4, project 2 of 5)

## Intent

Every artifact someone builds from should be read by a fresh reviewer before anyone builds from it. In `skills/experimental_v4`, those artifacts are:
- the spec (`brain-write-spec`);
- the ticket set (`brain-write-tickets`);
- the impl plan (`brain-implement`).

The reviewer reads as a builder who can't ask questions, so it surfaces gaps the author can't see. Before that, the author runs a self-check that catches the mechanical gaps cheaply:
- a requirement with no Example or ticket;
- a name that drifts between documents;
- a failure case nothing tests.

This is superpowers' "builder check" and plan self-review, adapted to the brain skills.

## Current state (v4, after project 1)

- **`brain-write-spec`** writes the spec, invokes `brain-update`, and reports. There is no self-check and no reviewer.
- **`brain-write-tickets`** shows the proposed set to the user for approval, then writes the files. Nothing checks that every spec Example lands in a ticket, that names are consistent, or which failure cases nothing covers.
- **`brain-implement`** creates the impl plan when tracked work begins (§2), but doesn't review it.
  - Per-task reviews (subagent-driven mode) and the proportional final review already exist from project 1.
  - The final review isn't told which failure cases the plan leaves untested.
- **`brain-brainstorm`** ends in a summary, not a document.
- **`brain-plan-feature`** tracks planning questions and hands off to `brain-write-tickets` when tickets are wanted.

## Goals

1. **The review workflow (user-approved):**

   | Skill | Review |
   |---|---|
   | `brain-brainstorm` | None |
   | `brain-plan-feature` | None of its own. When tickets are wanted, it hands off to `brain-write-tickets`, which reviews them. |
   | `brain-write-spec` | Write the spec → self-check → fresh reviewer. |
   | `brain-write-tickets` | Draft the set → self-check → fresh reviewer → user approves → write the files. |
   | `brain-implement` | Impl plan created → self-check → fresh reviewer → first change. Per-task reviews (subagent-driven) and the final review stay as built in project 1. |

2. **Every spec, every ticket set, and every new impl plan gets the fresh reviewer.** None of these reviews is proportional or optional.
3. **The fresh reviewers run on the standard tier** (Sonnet today). Root `CLAUDE.md`'s Model tiers table gains this role. Per-task reviews stay on the standard tier and the final review stays on the strongest tier (Opus), unchanged from project 1.
4. **Failure cases that no Example covers reach the final review.** The impl plan gets a `Review Focus` section listing the failure cases the governing requirements imply but no Example or acceptance criterion covers. The final review checks each one deliberately. That review is the full-review subagent, or the skill's own diff inspection for small changes.

## Non-goals

- No review in `brain-brainstorm`, and none of `brain-plan-feature`'s planning tickets.
- No change to the project-1 per-task loop, the final review's proportionality, or its tiers.
- No second review round for fixes or for answers to the review's own questions. A structural revision gets one more review (see "Re-review").

## Anti-goals

These would make the change a failure even if it technically works:

- **The review becomes a new requirements interview, or reopens settled decisions.** `brain-write-spec` already forbids this, and the reviewer's questions don't override it.
- **A review finding decides an open choice.** Anything that needs the user goes to the user or becomes an Open Decision. It is never settled to make the artifact look complete.
- **Several rounds of questions to the user.** Each review produces at most one message to the user.
- **The reviewer edits files.** It is read-only. The author applies changes.

## The pieces

### Self-check (the author, in the main session)

Each self-check is a short checklist the author runs after drafting, before the fresh review. It fixes what it can and carries the rest forward.

- **Spec:**
  - every required behavior and invariant has at least one Example, including the failure paths that apply (§2's list: invalid input, missing or denied access, conflicts, partial failure, limits). Following §2, write the missing Example when approved requirements determine its outcome; record an Open Decision only when the outcome depends on a choice nobody has made.
  - no Example settles an open choice;
  - terms match `.brain/glossary.md`;
  - Example IDs are unique;
  - the Verification Strategy names a test boundary for every Example.
- **Ticket set:**
  - a coverage table that maps each spec Example and invariant to the ticket(s) that cover it, with none left without a ticket. Without a spec, number the approved requirements from the plan or discussion (`R1`, `R2`, …) and map those.
  - every acceptance criterion references Examples or states an observable result;
  - names and terms are consistent across tickets and with the spec and glossary;
  - dependencies are genuine and acyclic;
  - a list of failure cases that no Example or criterion covers. Each one becomes an acceptance criterion when approved requirements determine its outcome. Otherwise it is a question for the user. The list is shown in the approval message and not saved. The impl plan's self-check derives its own list from the approved artifacts.
- **Impl plan:**
  - every governing Example, acceptance criterion, or numbered requirement maps to a work item;
  - names match the spec and tickets;
  - `Review Focus` lists the failure cases that the governing requirements imply but that no Example or criterion covers. Each line either names the work item whose tests pin it, per §5's rule to test failure paths the Examples don't cover, or, when no approved requirement determines the outcome, is marked `blocked` and moved to Blockers and Open Decisions. Implementers never invent the behavior.

### Fresh builder review (a subagent)

- **Dispatch:** a fresh subagent on the standard tier, read-only. Its inputs:
  - the artifact;
  - the sources it is built from:
    - nothing extra for a spec;
    - the spec for a ticket set, or the approved plan or discussion text when there is no spec;
    - the spec and tickets for an impl plan, or the governing request recorded in the plan when there are neither;
  - `.brain/glossary.md`;
  - access to the repository.

  It does not get the conversation or the rest of `.brain`.
- **Its task:** read as a builder who must build from this without asking anyone, and return:
  - the questions it would have to ask;
  - places where two builders would build different things;
  - contradictions;
  - failure behavior left unstated.

  For an impl plan, "build from" means executing the work items. The reviewer checks three things:
  - the items cover every governing Example and criterion, in an order that respects dependencies;
  - each item is one coherent, testable increment;
  - `Review Focus` is complete.
- **One shared prompt template** serves all three artifacts, with a slot for which artifact is being reviewed.
- **Without a subagent tool,** the author reads the artifact as that builder, and the report says: `Builder review: self-read (no fresh reviewer) — weaker than an independent review`.

### Sorting the reviewer's questions (the author)

Each question goes into one of three piles:

1. **Answered already** by the conversation, the code, or the brain. Put the answer into the artifact.
2. **Routine detail.** A sensible builder could settle it without changing what gets built. Leave it out of the artifact as implementation discretion. In the impl plan, note it only if continuity needs it.
3. **Only the user can answer it.** Ask in one message, most important first, and wait for the reply.
   - For a spec, ask after the file is written and before `brain-update`. Apply the answers to the spec, then invoke `brain-update` and report. These questions are bounded to the gaps a builder hit, so they don't count as a new requirements interview, and they never reopen a settled choice.
   - For a ticket set, the questions go in the same message that asks for set approval.
   - For an impl plan, they come before the first change and follow root `CLAUDE.md`'s consultation rules. When the startup questions (§1 step 6) are also pending, everything goes in one message.
   - Anything the user leaves unanswered becomes an Open Decision in a spec, a blocked ticket in a ticket set, or a Blocker in an impl plan.

### Re-review

- Answers to the review's own questions, and edits that come from the review's findings, don't trigger another review.
- A structural revision gets one more fresh review before the artifact is used:
  - a spec that gains or loses behaviors;
  - a ticket set where tickets are added, split, or merged;
  - an impl plan where work items are added, split, or merged from new or changed Examples, tickets, or requirements.
- These changes are not structural and never trigger a review:
  - a plain resume;
  - status updates;
  - fix-pass items;
  - `Ruling:` or Deferred entries.

### The final review and Review Focus

- `brain-implement` §7 step 3 passes the impl plan's `Review Focus` list to the full-review subagent.
- `brain-review-code`'s coverage table adds one row per Review Focus item, marked met, unmet, or unverifiable, with evidence.
- An unmet item is a finding graded by its effect. Critical, High, and Medium findings enter the one fix pass, as for any other finding.
- When the final check is the skill's own diff inspection, it reports the same rows.

### Where each skill changes

- **`brain-write-spec`:** after the file is written (§4), and before `brain-update` and the report:
  - run the self-check, then the fresh review, then sort the questions;
  - the report says what the review found and changed.
- **`brain-write-tickets`:**
  - §5 becomes: draft the set → self-check → fresh review → present everything in one message. That message holds the set, the coverage table, the uncovered failure cases, and any questions only the user can answer.
  - Files are written only after approval (§6, unchanged).
- **`brain-implement`:**
  - When §2 creates the impl plan, or on a structural revision (see Re-review), run the self-check and the fresh review before the first change.
  - `references/todo-template.md` gains a `## Review Focus` section.
  - §7 step 3 hands the Review Focus list to the full reviewer. Own-diff inspection also checks each item.
- **`brain-review-code`:** the coverage table takes Review Focus rows when they are provided.
- **Root `CLAUDE.md`:** the standard-tier row in Model tiers gains "spec, ticket-set, and impl plan builder reviews".
- **`README.md`:** the review workflow table (Goal 1) and the skills table.

## Constraints

- **Edit scope:** edits only under `skills/experimental_v4/`. Work happens in the `spec-review` worktree branch.
- **Commits:** no attribution trailers.
- **Model names:** they appear only in root `CLAUDE.md`'s Model tiers table. Skills say "standard tier".
- **Git:** skill text never runs `git commit`, `git push`, `git merge`, or `git worktree remove`.
- **Size:**
  - `brain-implement/SKILL.md` stays at or under 1,750 words (it is 1,670 now). The impl plan review's detail goes in a reference.
  - `brain-write-spec` and `brain-write-tickets` stay at or under 1,200 words each (they are about 900 now).
- **Commands:** portable across Linux, macOS, and Windows (Git Bash or WSL).
- **Subagents:** skills dispatch them only where this design says to (the user asked for fresh reviewers). Every dispatch names its tier.

## Testing

Use writing-skills scenarios in `tests/scenarios.md`, RED with the current skills and GREEN after the change, on the `crate` fixture. Project 1 showed scenario agents can dispatch subagents.

- **Spec:** the trigger leaves a planted gap, for example "filter by key" with no rule for tracks that have no key.
  - Pass: the self-check or the fresh review catches it; it becomes a question to the user or an Open Decision, never a silent choice; exactly one message goes to the user.
- **Tickets:** a spec has an Example that the natural decomposition misses.
  - Pass: the coverage table shows the gap before approval, the review result is in the approval message, and no files are written before approval.
- **Impl plan:** a spec has a failure path with no Example.
  - Pass: the impl plan's `Review Focus` lists it, with either an owning work item or `blocked`. The final review's coverage table has a row for it.
- **Regression:** rerun S9, S16–S19, and S23.

## Left to the builder

- Prompt wording.
- Where the shared reviewer template lives. It must be one file, with no copies. Skills locate it by an absolute path, as `subagent-driven.md` already does for `findings.md`.
- How drafts reach the reviewer before files exist: a scratch file outside `.brain/`, or the prompt.
- Exact report lines and checklist wording.
