# Builder reviews for specs, tickets, and impl plans: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every spec, ticket set, and new impl plan in `skills/experimental_v4` gets an author self-check and then a fresh standard-tier builder review. The impl plan's `Review Focus` items reach the final review.

**Architecture:**
- **One shared reference** (`brain-review-code/references/builder-review.md`) holds the author's rules and the reviewer prompt. Those rules cover dispatch, sorting questions into three piles, one message to the user, and re-review.
- **Each producing skill** adds its own self-check and points to that reference. The producing skills are `brain-write-spec`, `brain-write-tickets` and `brain-implement`, with `brain-implement`'s detail in a new `references/impl-plan-review.md`.
- **`brain-review-code`** gains Review Focus rows in its coverage table.
- **Testing:** each behavior is tested with writing-skills scenarios on the `crate` fixture. Each runs RED against the current skills, then GREEN after the change.

**Tech Stack:** Markdown skills, POSIX shell plus git, and the fixtures in `tests/fixture/`.

**Spec:** `docs/superpowers/specs/2026-11-05-brain-plan-review-design.md`

## Global Constraints

- **Edit scope:** all edits are under `skills/experimental_v4/`. Work happens in the `spec-review` worktree branch.
- **Commits:** stage with `git add skills/experimental_v4 docs/superpowers`. Commit messages carry no attribution trailer.
- **Model names:** they appear only in root `CLAUDE.md`'s Model tiers table. Skills and references say "standard tier".
- **Git:** no skill text runs `git commit`, `git push`, `git merge`, or `git worktree remove`.
- **Size limits (`wc -w`):**
  - `brain-implement/SKILL.md` ≤ 1,750 (now 1,670);
  - `brain-write-spec/SKILL.md` and `brain-write-tickets/SKILL.md` ≤ 1,200 each (now 916 and 877);
  - `brain-review-code/SKILL.md` ≤ 1,300 (now 1,247);
  - `brain-review-code/references/builder-review.md` ≤ 450;
  - `brain-implement/references/impl-plan-review.md` ≤ 350.
- **Commands:** portable across Linux, macOS, and Windows (Git Bash or WSL). No GNU-only or BSD-only flags.
- **Fixed names:**
  - Review Focus IDs are `RF1`, `RF2`, ….
  - Numbered requirements without a spec are `R1`, `R2`, ….
  - Report lines:
    - `Builder review: fresh standard-tier reviewer — <n> questions (<a> answered, <r> routine, <u> to user)`
    - `Builder review: self-read (no fresh reviewer) — weaker than an independent review`

## Review Focus

Each line names the scenario that covers it.

1. An Example silently settles an open choice (S24, criterion 2).
2. A review produces more than one message of questions (S24 criterion 3, S25 criterion 1, S26 criterion 3).
3. Ticket files are written before the set is approved (S25, criterion 2).
4. A plain resume reruns the impl plan review (S16 and S17, new criterion 3).
5. Review questions reopen settled decisions (S24, criterion 5).

---

### Task 1: Scenarios S24–S27, the spec 02 fixture, and S16/S17 criterion 3

**Files:**
- Create `skills/experimental_v4/tests/fixture/spec-02/02-key-filter.md`.
- Modify `skills/experimental_v4/tests/scenarios.md`.

**Fixture spec 02** (exact content):

```markdown
# Key Filter

## Problem

DJs mix harmonically and need the tracks in a crate that share a key.

## Desired Outcome

`crate filter <crate> --key <key>` lists the matching tracks in crate order.

## Behavior and Invariants

- Keys use Camelot notation: a number 1–12 followed by `A` or `B` (for example `8A`).
- Key matching is exact and case-insensitive (`8a` matches `8A`).
- Output keeps crate order.
- An invalid key exits with status 2 and prints `invalid key: <key>`.
- If the crate does not exist, the command exits with status 1 and prints `no such crate: <crate>`.
- `--key` may be combined with `--bpm-min` and `--bpm-max`; a track must satisfy all given filters.

## Examples

- **E1:** Given tracks A (8A), B (9A), and C (8A), when filtering `--key 8A`, then A and C are listed, in that order.
- **E2:** Given the same tracks, when filtering `--key 8a`, then A and C are listed.
- **E3 (failure):** When filtering `--key 13C`, then the command exits with status 2 and prints `invalid key: 13C`.

## Technical Decisions

- Add a nullable `key` column to `tracks`; `add-track` gains an optional `--key`.

## Verification Strategy

Unit tests of the filter function for E1 and E2; a CLI test for E3.
```

Two invariants have no Example: the missing crate, and the combined filters. S25 and S26 depend on that.

**Fixture variants:**
- `synced+02`: the synced fixture, plus this file copied to `.brain/specs/02-key-filter.md`.
- No impl plan exists for spec 02.

**Scenario changes:**

- **S16 and S17:** add criterion 3: "No builder reviewer is dispatched (plain resume)."
- **S24: Spec builder review.**
  - **Setup:** synced. Skill `brain-write-spec`.
  - **Context:** "Brainstorm summary, confirmed by the user:
    - `crate filter <crate> --key <key>` lists the tracks with that key, in crate order.
    - Keys are Camelot notation (1–12 plus A or B), matched exactly and case-insensitively.
    - An invalid key exits with status 2 and prints `invalid key: <key>`.
    - Add a nullable `key` column to `tracks`, and an optional `--key` to `add-track`."

    The summary is silent on whether `--key` combines with `--bpm-min`/`--bpm-max`. That is the planted gap.
  - **Trigger:** "/brain-write-spec write the key filter spec from the brainstorm summary."
  - **Follow-up**, only if the agent asked about combining: `The user replies: "Combine them: a track must satisfy all given filters."`
  - **Pass criteria:**
    1. A builder reviewer is dispatched with an explicit standard-tier model, or the reply carries the `self-read` report line.
    2. No Example or rule decides whether `--key` combines with the BPM bounds. The question reaches the user, or appears under Open Decisions.
    3. At most one message of questions goes to the user.
    4. `.brain/specs/02-*.md` exists. After the follow-up, it has an Example for the combined filters, and `brain-update` has been invoked.
    5. It doesn't ask about Camelot notation, case-insensitivity, the exit status, or the column. Those are settled.
- **S25: Ticket set review.**
  - **Setup:** synced+02. Skill `brain-write-tickets`.
  - **Trigger:** "/brain-write-tickets break spec 02 into tickets."
  - **Follow-up:** `The user replies: "Approved."`
  - **Pass criteria:**
    1. Before any ticket file is written, one message has all of:
       - the proposed set;
       - a coverage table with a row for each of E1, E2 and E3 and each invariant;
       - the missing-crate case and the combined-filter case, either listed as uncovered or added as acceptance criteria;
       - the builder review result: a reviewer dispatched with an explicit standard-tier model, or the `self-read` line.
    2. No file exists under `.brain/tickets/` before the follow-up.
    3. After the follow-up, the ticket files exist, and every Example ID appears in some ticket's acceptance criteria.
- **S26: Impl plan review and Review Focus.**
  - **Setup:** synced+02. Skill `brain-implement`.
  - **Trigger:** "/brain-implement implement spec 02."
  - **Pass criteria:**
    1. `.brain/impl_plans/02-key-filter.md` exists with a `## Review Focus` section. One `RF` line covers the missing-crate case and names an owning work item or `blocked`.
    2. A builder reviewer is dispatched with an explicit standard-tier model before any code change, or the `self-read` line is reported.
    3. One message carries the startup questions and any review questions.
    4. Nothing under `crate/` or `tests/` has changed.
- **S27: Review Focus rows in `brain-review-code`.**
  - **Setup:** synced, with no WIP file (as in S15). Skill `brain-review-code`, run inline.
  - **Context:** "The impl plan's Review Focus: RF1 — a filter whose bounds are equal (120–120) lists the 120 BPM track."
  - **Trigger:** "/brain-review-code review the BPM filter work since the impl plan's review base, against spec 01, including the Review Focus items."
  - **Pass criteria:**
    1. The coverage table has an `RF1` row marked `unmet`, citing the exclusive upper bound.
    2. The summary line's met/total counts include the RF row.

- [ ] **Step 1:** Create the fixture file and add S24–S27, plus S16/S17 criterion 3, to `scenarios.md`. Document the `synced+02` variant under Building fixtures.
- [ ] **Step 2:** Commit: `test: add scenarios for builder reviews`.

---

### Task 2: RED runs (current skills)

- [ ] **Step 1:** Build the fixtures and run S24, S25, S26 and S27 with the skills as they are now.
- [ ] **Step 2:** Record the results under Results. Expected failures:
  - S24 criterion 1 (no reviewer);
  - S25 criterion 1 (no coverage table or review);
  - S26 criteria 1 and 2;
  - S27 criterion 1.

  Whatever passes is recorded as needing no new guidance.
- [ ] **Step 3:** Commit: `test: record RED results for builder reviews`.

---

### Task 3: Shared builder-review reference, model tier row, and `brain-write-spec`

**Files:**
- Create `brain-review-code/references/builder-review.md`.
- Modify `CLAUDE.md`, Model tiers: in the standard-tier row for the task implementer, task reviewer and scoped re-review, add "spec, ticket-set, and impl plan builder reviews".
- Modify `brain-write-spec/SKILL.md`.

**Interfaces:**
- **Produces:** the shared reference.
  - **Part 1, "For the author"** (above a `---` line):
    - Dispatch on the standard tier, read-only.
    - Fill every slot; path slots are absolute.
    - With no subagent tool, the author reads the artifact as the builder and reports the `self-read` line.
    - Sort the reviewer's questions into the design's three piles.
    - Questions only the user can answer go in one message, most important first.
    - Answers to review questions don't trigger a re-review. A structural revision gets one more review.
  - **Part 2, the prompt.** Slots: `{artifact_kind}` (spec | ticket set | impl plan), `{artifact}`, `{sources}`, `{glossary_path}`, `{repo_root}`.
    - The reviewer reads as a builder who can't ask anyone. It returns a numbered list, most important first. Each item gives a location, what is unclear, contradictory or missing, and why two builders would diverge.
    - For `impl plan`, it also checks that items cover every governing Example and criterion in dependency order, that each item is one testable increment, and that Review Focus is complete.
    - It is read-only: no edits, no subagents.
- **Consumed by:** Tasks 4 and 6, at the path "`brain-review-code/references/builder-review.md` beside this skill's folder".

- [ ] **Step 1:** Write `builder-review.md` (≤ 450 words) and add the CLAUDE.md row text.
- [ ] **Step 2: `brain-write-spec`.** Add a new section after §4 ("Write the file"), titled `## 5. Check and review`.
  - **Self-check:** the design's five spec items. Write a missing Example when approved requirements determine its outcome; otherwise record an Open Decision.
  - **Builder review:** follow the shared reference, with the `spec` kind and no extra sources.
  - **Pile 3:** ask once, wait, apply the answers, and record anything unanswered under Open Decisions.
  - **Ordering:** the existing "Then invoke `brain-update`" and report lines now come after this section. The report includes the `Builder review:` line.
- [ ] **Step 3:** Check `wc -w` (≤ 1,200 and ≤ 450), and grep the edited files for model names. Expected: none.
- [ ] **Step 4:** Run S24. Expected: pass.
- [ ] **Step 5:** Commit: `feat(write-spec): self-check and builder review every spec`.

---

### Task 4: `brain-write-tickets`

**Files:** Modify `brain-write-tickets/SKILL.md`.

**Interfaces:**
- **Consumes:** the shared reference (Task 3).
- **Produces:** the approval message's coverage table, which has one row per spec Example and invariant, or per `R<n>` requirement when there is no spec.

- [ ] **Step 1:** Rename §5 to `Check, review, and obtain approval`. Its flow:
  1. Draft the set.
  2. Run the self-check (the design's ticket items). Each uncovered failure case becomes an acceptance criterion if its outcome is determined; otherwise it is a question for the user.
  3. Run the builder review: shared reference, `ticket set` kind. The sources are the spec, or the approved plan or discussion text. The drafts go in `{artifact}`.
  4. Send one message containing the set fields (unchanged), the coverage table, the uncovered list, the `Builder review:` line, and the pile-3 questions.

  A user revision that adds, splits, or merges tickets gets one more review before approval. Files are still written only after approval (§6).
- [ ] **Step 2:** Check `wc -w` (≤ 1,200).
- [ ] **Step 3:** Run S25. Expected: pass.
- [ ] **Step 4:** Commit: `feat(write-tickets): coverage self-check and builder review before approval`.

---

### Task 5: Review Focus rows in `brain-review-code`

**Files:** Modify `brain-review-code/SKILL.md`, Requirement fit (around line 86, the coverage table).

- [ ] **Step 1:** Add one row per Review Focus item (`RF<n>`) when provided, marked met, unmet, or unverifiable, with evidence.
  - An unmet item is a finding graded by its effect.
  - The summary line's counts include RF rows.
- [ ] **Step 2:** Check `wc -w` (≤ 1,300).
- [ ] **Step 3:** Run S27 and S15. Expected: both pass.
- [ ] **Step 4:** Commit: `feat(review-code): cover Review Focus items in the coverage table`.

---

### Task 6: Impl plan review in `brain-implement`

**Files:**
- Create `brain-implement/references/impl-plan-review.md`.
- Modify `brain-implement/SKILL.md`, §2 and §7 step 3.
- Modify `brain-implement/references/todo-template.md`.

**Interfaces:**
- **Consumes:**
  - the shared reference (Task 3);
  - the `RF<n>` rows (Task 5).
- **Produces:** a `## Review Focus` section in the template, with example lines:
  - `- RF1: <failure case> — tested in <work item>`
  - `- RF2: <failure case> — blocked: <decision needed>` (also listed under Blockers and Open Decisions)

- [ ] **Step 1: `impl-plan-review.md`** (≤ 350 words).
  - **Self-check:** the design's impl plan items, including the RF rules. Never invent a blocked case's behavior.
  - **Builder review:** shared reference, `impl plan` kind. The sources are the spec and tickets, or the governing request.
  - **Questions:** pile-3 questions merge with the pending startup questions into one message.
  - **Triggers:**
    - review on creation, and on adding, splitting, or merging work items from new or changed Examples, tickets, or requirements;
    - never on a plain resume, status updates, fix-pass items, `Ruling:` entries, or Deferred entries.
- [ ] **Step 2: SKILL.md.**
  - **§2:** after the impl plan is created, or after a structural revision, follow `${CLAUDE_SKILL_DIR}/references/impl-plan-review.md` before the first change.
  - **§7 step 3:** pass the impl plan's Review Focus list to the full reviewer. Own diff inspection reports one row per RF item.
  - Keep SKILL.md at or under 1,750 words.
- [ ] **Step 3: Template.** Add the `## Review Focus` section after Deferred, plus one Rules bullet.
- [ ] **Step 4:** Run S26, S16, and S17. Expected: all pass.
- [ ] **Step 5:** Commit: `feat(implement): review new impl plans and carry Review Focus to the final review`.

---

### Task 7: README and static checks

**Files:** Modify `README.md`.
- Add the design's review workflow table under Example workflows, or in a new short "Reviews" section after "Verification".
- In the skills table, add one clause each to the rows for `brain-write-spec`, `brain-write-tickets` and `brain-implement`.

- [ ] **Step 1:** Make the edits. Name no models.
- [ ] **Step 2: Static checks.** Run from `skills/experimental_v4`. Expected: no output.

```bash
grep -rnE '\b(sonnet|opus|haiku)\b' --include='*.md' -i . | grep -viE '^(\./)?(CLAUDE\.md|tests/)'
grep -rnE 'git (commit|push|merge)|worktree remove' --include='*.md' brain-*/ | grep -viE 'never|do not|don.t|user|merge-base'
```

- [ ] **Step 3:** Commit: `docs: document builder reviews`.

---

### Task 8: Regression, final review, finish

- [ ] **Step 1:** Rerun S9, S15, S16–S19, S23, and S24–S27 on the final skills. Record the results.
- [ ] **Step 2:** Run the final whole-branch review on the strongest tier, with the design, this plan, and the Review Focus list. Then do one fix pass, RED to GREEN, for each Critical or Important finding.
- [ ] **Step 3:** Delete `tests/.runs`, commit, then run superpowers:finishing-a-development-branch.
