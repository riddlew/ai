# Design: pending brain changes for branches (experimental_v4)

## Intent

The brain is the central source of truth for how the app works and why. One brain is shared by every branch and worktree, but the code differs between them. Today `brain-update` writes whatever branch it runs on into the root files. After syncing from a feature branch, the brain describes code that `main` and the other worktrees don't have.

The fix: the brain's code descriptions describe the main branch. Work on other branches is recorded as **pending changes**: what the brain will say once that branch merges. When the user says a branch has merged, `brain-update` applies its pending changes after checking them against the merged code.

## Current state

- `.brain/00_index.md` has `Last synced: <sha>` and `Git: ignored|tracked`. `brain-update` diffs `<sha>..HEAD` on whatever branch is checked out.
- If `<sha>` isn't an ancestor of `HEAD`, `brain-update` says the brain was synced from another branch and labels other-branch content "on branch `wt`, not merged" (S12).
- The README lists this as a known limit.

## Goals

1. **The code descriptions describe the main branch.** These are `02`–`08`, the features part of `01_about.md`, and `state.md`'s done items. `Last synced` is always a commit on the main branch.
2. **The main branch is recorded.** `00_index.md` gets the header line `Main branch: <name>`.
   - `brain-init` detects it: `git symbolic-ref --short refs/remotes/origin/HEAD` without the `origin/` prefix, else a local `main` or `master`, else it asks the user. It records it and reports it. `brain-update` re-detects the same way when the recorded branch no longer exists.
   - `brain-update` adds the line the same way to an older brain that lacks it.
3. **Updating on another branch records pending changes.**
   - When the current branch isn't the main branch, `brain-update` writes no code facts into the root files. Instead it brings `.brain/pending/<branch>.md` up to date with the branch's whole change since its merge base with the main branch (`git merge-base <main> HEAD`).
   - Each entry names a root file, says Add, Change or Remove, gives the text, and links the spec or impl plan when one exists.
   - Entries that the branch's code no longer supports are removed.
4. **Intent is shared at once.** On any branch, `brain-update` still writes these straight into the root files:
   - user decisions (`09`, ADRs);
   - glossary terms;
   - open questions and answers;
   - spikes.
5. **State shows branch work.**
   - `state.md` lists each pending branch's work as in progress, labelled with the branch and linking its pending file.
   - `00_index.md` lists each pending file.
6. **Reminder first.** Every `brain-update` run, on any branch and however invoked, starts its reply by listing the pending files. Each row has the branch, the number of entries, and the date it was last updated. A branch git no longer has is marked "branch not found". Then it continues. When there are none, it lists nothing.
7. **Merges are applied when the user says so.** The user tells `brain-update` that a branch has merged, for example `/brain-update cue-points merged`. On the main branch, `brain-update` then works through that branch's pending file:
   - It checks each entry against the current code and applies the confirmed ones to the root files.
   - It reports entries the code doesn't confirm, doesn't apply them, and asks whether to keep them pending (the branch may have more to merge) or drop them.
   - It deletes the pending file once no entry is left, marks the `state.md` items done, and continues with the normal sync.

   This works for merge commits, squash merges and rebases alike, because it relies on the user's word and the code, not on git ancestry.
   - If the user says a branch merged while on another branch, `brain-update` says merges are applied from the main branch, and doesn't apply them.
   - If none of the branch's changes are in the main branch's code, it says so and keeps the file.
8. **Abandoned branches.** A pending file is deleted only when the user says that branch merged or was abandoned. "Branch not found" is reported, never acted on by itself.
9. **Legacy brains synced from a branch.** If `Last synced` isn't an ancestor of the main branch's `HEAD`, `brain-update` on the main branch:
   - re-verifies every root file against the main branch;
   - moves descriptions of code that exists only on another branch into that branch's pending file, finding the branch with `git branch --contains <sha>`; if it can't tell, it asks;
   - sets `Last synced` to `HEAD`.
10. **Setup runs on the main branch.**
    - `brain-init` with no brain, run on a branch other than the main branch, says the brain describes the main branch, tells the user to run `/brain-init` from a checkout of it, and stops.
    - Saving a path with `/brain-init <path>` works on any branch.
11. **Other skills see their own branch's pending changes.** On a branch other than the main branch, a skill reading the brain also reads `pending/<branch>.md` when it exists. This is added to the shared preamble only if a baseline test shows agents don't already do it via the `state.md` link.

## Non-goals

- Automatically detecting merges from git history.
- Per-branch copies of the brain, or tracking `.brain` in git per branch.
- Changing how specs, tickets or impl plans are stored. They already live in the shared brain and describe in-flight work.

## Anti-goals

- Pending entries applied without checking them against the merged code.
- A pending file deleted without the user's word.
- Code from a feature branch written into the root files as fact.
- Decisions made on a branch held back until merge.

## The pieces

- **`brain-update/SKILL.md`:**
  - §1 adds the main-branch check and the reminder.
  - New §2, "Branches": recording pending changes, applying merges, abandoned branches, legacy brains.
  - The update steps (now §3) are adjusted:
    - step 2's other-branch rule is replaced by goal 9;
    - step 6 sets `Last synced` only on the main branch.
- **`brain-update/references/templates.md`:** the `Main branch:` header line, and a `pending/<branch>.md` template. A `/` in a branch name becomes `--` in the file name.
- **`brain-init/SKILL.md`:** it records `Main branch:` (goal 2) and stops off the main branch (goal 10).
- **The shared preamble in 11 skills:** changed only if needed (goal 11).
- **README:** the known-limit paragraph is replaced by a short "Branches" description.

## Constraints

- Commands are portable across Linux, macOS, and Windows (Git Bash or WSL).
- No skill commits, pushes, or merges.
- No model names in skills.
- The isolation rules for worktree sessions are unchanged. Pending files are inside the brain, so the same refusals apply.
- `brain-update` has no word cap. Its additions stay under about 400 words.

## Testing

Writing-skills scenarios on the `crate` fixture, with RED runs before the change:
- recording on a branch;
- the reminder on `main`;
- applying a merge, including one planted entry the code contradicts;
- a pending file whose branch is gone;
- `brain-init` off `main`;
- other skills reading their branch's pending file;
- the revised S12.

Regression covers S1, S2, S4, S5, S11, S46 and S47.

## Left to the builder

- The exact wording of the reminder list.
- How entries are worded inside a pending file, within the template.
