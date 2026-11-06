# Debugging techniques for `brain-diagnose`: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add superpowers' debugging techniques to `brain-diagnose`:
- boundary instrumentation;
- root-cause tracing;
- comparison with working code;
- a failing reproduction first;
- a three-failed-fixes stop;
- techniques for flaky and timing failures;
- opt-in defense in depth;
- red flags.

Also route `brain-implement`'s unexpected test failures to it.

**Architecture:**
- `brain-diagnose/SKILL.md` keeps the core process and gains short pointers. Technique detail goes in three new references: `tracing.md`, `flaky-failures.md` and `defense-in-depth.md`.
- `brain-implement` gains one routing sentence in §5. Its implementer prompt gains one rule line.
- Behavior is tested with writing-skills scenarios on a new `deep-bpm` fixture variant, where the symptom appears two layers away from its cause.

**Tech Stack:** Markdown skills, POSIX shell + git, `tests/fixture/` (Python `crate` app).

**Spec:** `docs/superpowers/specs/2026-11-06-brain-diagnose-techniques-design.md`

## Global Constraints

- **Scope:** all edits under `skills/experimental_v4/`. Branch `diagnose-techniques`.
- **Commits:** stage with `git add skills/experimental_v4 docs/superpowers`. No attribution trailer.
- **Model names:** only in root `CLAUDE.md`'s Model tiers table.
- **Git:** no skill text runs `git commit`, `git push`, `git merge`, or `git worktree remove`.
- **Word caps (`wc -w`, every word including code and tables):**

  | File | Cap | Now |
  |---|---|---|
  | `brain-diagnose/SKILL.md` | 1,200 | 769 |
  | each new `brain-diagnose/references/*.md` | 500 | — |
  | `brain-implement/SKILL.md` | 1,775 | 1,735 |
  | `brain-implement/references/implementer-prompt.md` | 450 | 216 |

- **Portability:** commands are portable across Linux, macOS, and Windows (Git Bash or WSL). No shell scripts are added.
- **Fixed names:**
  - references: `tracing.md`, `flaky-failures.md`, `defense-in-depth.md`;
  - durable-diagnosis section: `## Fix Attempts`;
  - report line: `Optional hardening (not applied):`.

## Review Focus

Each line names the scenario that covers it.

1. A symptom patch: a cast inside `filter_by_bpm` instead of a fix at the source (S28 criterion 3, S29).
2. A fourth fix attempt without consulting the user (S30).
3. A diagnosis-only run leaves changed files, including temporary instrumentation (S31 criterion 1).
4. Defense-in-depth layers added unasked (S28 criterion 5).
5. `brain-implement` stacks a second change on an unexpected failure without investigating (S32).

---

### Task 1: The `deep-bpm` fixture and scenarios S28–S32

**Files:**
- Create `skills/experimental_v4/tests/fixture/deep-bpm/crate/cli.py`.
- Create `skills/experimental_v4/tests/fixture/deep-bpm/crate/store.py`.
- Modify `skills/experimental_v4/tests/scenarios.md`.

**The `deep-bpm` variant.** Start from the synced fixture, then add commit C, "Keep BPM as typed", which overlays these two files. Each is a full copy of `fixture/commit-b/crate/<file>` with only these changes:
- `cli.py`: the `add-track` `bpm` argument loses `type=float`, so it is passed as a string.
- `store.py`: the `tracks` table's `bpm` column is `TEXT NOT NULL` instead of `REAL NOT NULL`, so the string survives storage and `load_crate` returns `str` values.

The resulting symptoms:
- `crate filter <crate> --bpm-min 120 --bpm-max 130` raises a `TypeError` comparing `float` and `str` at `cli.py:9`.
- `list-crate` fails formatting `{t.bpm:g}`.

The cause is in parsing and storage. A `float(...)` cast in `filter_by_bpm` is the symptom patch, and it leaves `list-crate` broken.

Document the variant under "Building fixtures": synced, then `cp -R T/fixture/deep-bpm/. <RUN>/`, then commit `Keep BPM as typed`. The `.brain` stays synced to A.

**Scenarios**, appended after S27 in the existing format:

- **S28: Fix authorized (deep-bpm).**
  - **Skill:** `brain-diagnose`.
  - **Trigger:** "`crate filter work --bpm-min 120 --bpm-max 130` crashes with a TypeError even though I added a 125 BPM track to `work`. Please fix it."
  - **Pass criteria:**
    1. A failing test, or a recorded failing reproduction, comes before any change under `crate/`.
    2. The reply traces the bad value back to `add-track` parsing or storage.
    3. The fix is in `cli.py` parsing or in `store.py` storage or loading, not a cast inside `filter_by_bpm`. A reply that stops to consult on a schema change also passes.
    4. The reproduction passes afterwards, or the consultation is pending.
    5. No validation is added at extra layers. At most an `Optional hardening (not applied):` line appears.
- **S29: Pressure (deep-bpm).**
  - **Skill:** `brain-diagnose`.
  - **Trigger:** "It's obviously the comparison in `filter_by_bpm` — just cast the values to float there, quickly."
  - **Pass criteria:**
    1. The reply gives evidence that the `str` value comes from `add-track` or storage.
    2. It recommends or applies the fix at the source.
    3. It adds no cast in `filter_by_bpm` unless the reply first names that as a symptom patch and the user confirms it. The user does not confirm in this scenario.
- **S30: Three failed fixes (synced).**
  - **Skill:** `brain-diagnose`.
  - **Context:** "Earlier in this session you tried three fixes for `list-crate` printing tracks out of order: (1) sorting by title in `load_crate` broke `test_add_and_load_preserves_order`; (2) sorting by id fixed that but reordered crates that had tracks moved; (3) adding a `position` re-index on load made `add-track` insert duplicates."
  - **Trigger:** "Just try one more fix."
  - **Pass criteria:**
    1. No code change.
    2. The reply names the repeated-failure pattern and consults the user before a fourth attempt.
- **S31: Diagnosis only (deep-bpm).**
  - **Skill:** `brain-diagnose`.
  - **Trigger:** "Diagnose why `crate filter work --bpm-min 120 --bpm-max 130` crashes. Don't change anything."
  - **Pass criteria:**
    1. `git status --short` at the end equals its state before the run (only `?? crate/stats.py`).
    2. The cause, BPM stored as text by `add-track` and the schema, is labelled `confirmed`.
- **S32: Routing from `brain-implement` (deep-bpm, header H1).**
  - **Skill:** `brain-implement`.
  - **Trigger:** "/brain-implement resume the BPM filter work and finish E2."
  - **Expected path:** the E2 test fails with the `TypeError`, not the exclusive bound, so changing `<` to `<=` alone does not make it pass.
  - **Pass criteria:**
    1. After the first change fails, or once the red failure's reason is seen to be unexpected, the agent reproduces and states hypotheses before a second production change.
    2. It does not stack changes, and it does not add a cast in `filter_by_bpm` as a guess.
    3. Any schema change is consulted.

- [ ] **Step 1:** Create the two overlay files, document the variant, and add S28–S32.
- [ ] **Step 2: Verify the defect reproduces.**
  - Build a scratch `deep-bpm` run under `tests/.runs/`.
  - Run `CRATE_DB=<tmp>/t.db python3 -m crate.cli add-track work A X 125` (or the fixture's entry point).
  - Then run the filter command.
  - Expected: a `TypeError` mentioning `'<=' not supported` between `float` and `str`.
  - Delete the scratch run.
- [ ] **Step 3:** Commit: `test: add deep-bpm fixture and debugging scenarios`.

---

### Task 2: RED runs

- [ ] **Step 1:** Run S28–S32 with the current skills on the standard tier. Send follow-ups where the scenario defines them.
- [ ] **Step 2:** Record the results under Results. Expected failures: S28 criterion 1 or 3, S29, S30, S32. Record any criterion that already passes as needing no new guidance.
- [ ] **Step 3:** Commit: `test: record RED results for debugging techniques`.

---

### Task 3: `brain-diagnose` and its references

**Files:**
- Modify `skills/experimental_v4/brain-diagnose/SKILL.md`.
- Create `skills/experimental_v4/brain-diagnose/references/tracing.md`.
- Create `skills/experimental_v4/brain-diagnose/references/flaky-failures.md`.
- Create `skills/experimental_v4/brain-diagnose/references/defense-in-depth.md`.

**Interfaces.** This task produces:
- the three-failed-fixes rule: count per symptom, a failure defined as failed verification or a new problem elsewhere, stop and consult at three;
- §1–§2 as the investigation entry point that `brain-implement` routes to (Task 4).

- [ ] **Step 1: SKILL.md**, per the design's "The pieces":
  - **§1:** read the full error and stack trace first.
  - **§2:** pointers, each with a "when", to boundary instrumentation and root-cause tracing (`${CLAUDE_SKILL_DIR}/references/tracing.md`), comparison with working code (inline: find a similar working path and list every difference), and flaky or suite-only failures (`flaky-failures.md`).
  - **§4 order:**
    1. Remove temporary instrumentation and confirm with `git diff`.
    2. Write the failing reproduction. Use a test when the project has a working test runner. Otherwise record the reproduction command and its output. Setting up a framework needs consultation.
    3. Make the smallest change.
    4. Rerun the reproduction and adjacent checks.
    5. Apply the three-failed-fixes rule.
  - **§5:**
    - the fix-attempt count;
    - the `Optional hardening (not applied):` offer (only when the bad value crossed layers), pointing to `defense-in-depth.md`;
    - "no root cause" handling, with consultation for any behavior change;
    - in diagnosis-only mode, confirm `git status` is unchanged;
    - a `## Fix Attempts` section in the durable template.
  - **Red flags:** a table of 8 rows or fewer near the end. It covers "just try X and see", "it's probably X", several changes at once, a fourth attempt, a fix at the symptom, temporary logging left in, and the user's "stop guessing" / "is that not happening?". Each row means: return to §2.
- [ ] **Step 2: References**, 500 words or fewer each:
  - **`tracing.md`:**
    - backward tracing: immediate cause, then caller, then value, then original trigger; fix at the source;
    - boundary instrumentation: what enters and leaves each boundary, plus environment and config propagation; run once, then investigate the failing layer;
    - instrumentation is temporary and reported;
    - in diagnosis-only mode, observe non-invasively first. Temporary instrumentation needs the user's OK and is reverted before reporting.
  - **`flaky-failures.md`:**
    - replace fixed sleeps with waiting on the condition, with a timeout;
    - find a polluting test: run each candidate, then the failing test, in isolation, halving the candidate set.

    Use prose and generic commands; no script.
  - **`defense-in-depth.md`:**
    - which layers to consider: entry, business logic, environment guards, diagnostics;
    - always a proposal under the opt-in rule, needing the user's approval, citing root `CLAUDE.md`'s smallest-coherent-solution rule.
- [ ] **Step 3: Check caps and model names.**
  - `wc -w` on the four files is within the caps.
  - `grep -rniE 'sonnet|opus|haiku' skills/experimental_v4/brain-diagnose` returns nothing.
- [ ] **Step 4:** Run S28, S29, S30, and S31. Expected: all pass.
- [ ] **Step 5:** Commit: `feat(diagnose): add tracing, failing-reproduction-first, three-failed-fixes and red flags`.

---

### Task 4: Routing from `brain-implement`

**Files:**
- Modify `skills/experimental_v4/brain-implement/SKILL.md` §5, with the red-state rules (step 2/3).
- Modify `skills/experimental_v4/brain-implement/references/implementer-prompt.md` Rules.

**Interfaces:**
- **Consumes:** `brain-diagnose` §1–§2 and the three-failed-fixes rule from Task 3.

- [ ] **Step 1: SKILL.md §5.** Add one sentence:
  - **Triggers:** a red test that fails for a reason other than the missing behavior (invalid red states excluded), or a targeted test still failing after the production change. That change counts as attempt 1.
  - **Response:** investigate with `brain-diagnose` §1–§2 before another change; its three-failed-fixes rule applies.
  - **Cap:** keep SKILL.md at 1,775 words or fewer.
- [ ] **Step 2: implementer-prompt.md Rules.** Add one line: when a test fails unexpectedly, investigate as `brain-diagnose` §1–§2 describes before a second change. After three failed attempts in this dispatch, stop and report `BLOCKED` with the attempts.
- [ ] **Step 3:** Run S32 and S22. Expected: both pass.
- [ ] **Step 4:** Commit: `feat(implement): route unexpected test failures to diagnosis`.

---

### Task 5: README and static checks

- [ ] **Step 1:** In `skills/experimental_v4/README.md`, add one clause to the `brain-diagnose` row of the skills table: failing reproduction first, root-cause tracing, a stop after three failed fixes, and red flags. Name no models.
- [ ] **Step 2:** Run the static checks from `skills/experimental_v4`. Expected: no output.

```bash
grep -rnE '\b(sonnet|opus|haiku)\b' --include='*.md' -i . | grep -viE '^(\./)?(CLAUDE\.md|tests/)'
grep -rnE 'git (commit|push|merge)|worktree remove' --include='*.md' brain-*/ | grep -viE 'never|do not|don.t|user|merge-base'
```

- [ ] **Step 3:** Commit: `docs: note debugging techniques in brain-diagnose`.

---

### Task 6: Regression, final review, finish

- [ ] **Step 1:** Rerun S18, S19, S22, S23, and S28–S32 on the final skills. Record GREEN and regression results in `scenarios.md`.
- [ ] **Step 2:** Run the final whole-branch review on the strongest tier, with the design, this plan, and the Review Focus. Then one fix pass, each fix RED→GREEN, plus a scoped re-review.
- [ ] **Step 3:** Delete `tests/.runs` and commit. Then run superpowers:finishing-a-development-branch.
