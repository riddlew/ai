---
name: brain-init
description: Use when setting up or locating a project brain, or installing its collaboration policy and workflow guides.
---

# Brain Init

Sets up a project's `.brain/`, or connects the project to an existing one. Installs the shared `CLAUDE.local.md` policy and the bundled workflow guides (`USAGE.md` and `README.md`) without replacing project-specific instructions. `brain-update` maintains the brain afterward. For what goes where, read §4 (root files) and §5 (ADRs) of `${CLAUDE_SKILL_DIR}/../brain-update/SKILL.md`; read the file, don't invoke that skill. The templates are in `${CLAUDE_SKILL_DIR}/../brain-update/references/templates.md`. Follow `CLAUDE.local.md` for decision authority.

**Always:**

- Write only inside `.brain/`, plus the repository's `CLAUDE.local.md` and Git `info/exclude` (§0–1), and the approved moves in §2 step 3, including deleting originals and fixing links to them anywhere. Learn facts by reading code and git history. Never run the project's code, tests, or build; a fact that needs an experiment goes in `spikes.md`.
- Never edit documents other skills own (`specs/`, `tickets/`, `impl_plans/`, `planning/`, `diagnoses/`, `reviews/`) beyond moving them in §2 step 3 and fixing links to moved files.
- Never stage, commit, or push.
- Never dispatch subagents unless the user asks.
- Ask the user one question per message.

## 0. Install or reconcile the collaboration policy

The distributable source of the shared policy is **`${CLAUDE_SKILL_DIR}/references/CLAUDE.local.md`**. Use that file, not a policy reconstructed from memory or one already present in the project. The destination is `CLAUDE.local.md` at the checkout root (`git rev-parse --show-toplevel`), including when the skill is installed globally. Do not edit `CLAUDE.md`.

Perform this step **once per invocation that has a valid existing brain or is allowed to create one**, before reporting success or running the first-run investigation. Skip it if the supplied brain location is invalid, the saved location is broken, or branch/worktree safety checks forbid initialization. Run it even when `/brain-init` discovers that a valid brain already exists.

1. Read the bundled policy. If the destination doesn't exist, copy its contents **verbatim** to a new `CLAUDE.local.md`. If it exists, read it fully and **merge the missing policy instructions into it**, rather than overwriting or appending the entire bundled file.
2. Preserve existing project-specific instructions, comments, headings, and customizations. Reuse corresponding sections when present; add missing sections where needed, preserving the policy's rules and model-tier table. Avoid duplicate rules, duplicate headings, and a second document title. If an existing instruction materially conflicts with the bundled policy, **do not silently choose, override, or append contradictory rules**: explain the conflict, ask which should govern, and defer changing the file until resolved. Treat differences in wording alone as non-conflicts.
3. Make the merge **idempotent**: running `/brain-init` again should not add copies of instructions that are already present. If the existing file already expresses the complete policy, leave it unchanged. After editing, inspect the result for missing policy requirements, contradictions, and accidental deletion of existing content. If you cannot confidently merge without loss, leave the existing file unchanged and ask the user.
4. Keep this personal file out of Git when possible. If it is untracked and `git check-ignore -q CLAUDE.local.md` fails, add exactly one `CLAUDE.local.md` entry to `info/exclude` under `git rev-parse --git-common-dir`. If it is already tracked, **do not stage or commit it** and report that the change will be visible in Git; `info/exclude` cannot hide tracked files.

After this step, continue with §1 or §2, and report whether the policy was installed, merged, or already complete. A valid brain's saved `Project brain:` line is handled separately in §1; never remove it during the policy merge.

## 0a. Install the bundled workflow guides

The distributable sources are `${CLAUDE_SKILL_DIR}/references/USAGE.md` and `${CLAUDE_SKILL_DIR}/references/README.md`. Install them as `USAGE.md` and `README.md` **at the root of the selected brain**, not at the repository root and not beside the installed skills. Always use the bundled copies; never copy the project's own `README.md` in their place. A brain stored outside the checkout gets the guides in that external brain.

Run this step whenever §1 finds a **valid, writable brain** and after §2 step 5 creates a new one. Obey the same isolated-worktree and write-safety restrictions as other brain operations; if the selected brain isn't writable, report that and stop rather than writing to another location.

1. Confirm both bundled source files exist and can be read. If either is unavailable, report which one is missing; do not fabricate or substitute documentation.
2. For each destination, **copy** the bundled content if the file is absent. If its content is identical, leave it untouched. If a different file already exists, preserve it and report the difference; ask before replacing or reconciling it. Never silently overwrite a user-edited guide. Do not remove or move the bundled source.
3. Ensure `00_index.md` lists both guides under **Documents**, with purpose and status `reference`. This is the only exception allowing `brain-init` to modify an existing brain index after initial creation: add or correct **only these two inventory rows**; preserve the index header lines, all other rows, and `Last synced:`. Don't treat the guides as implementation knowledge or a new sync event.
4. Report each guide as installed, already current, or different and preserved. If either guide couldn't be copied, do not report the documentation installation as complete.

These are **workflow reference documents, not project-knowledge root files**. They are excluded from the mandatory full-root context read: skills must still load every project-knowledge root document, but consult only the relevant guide sections when choosing or explaining workflows. The policy in §0 references `.brain/USAGE.md` and `.brain/README.md` for the normal in-repository layout; when `Project brain:` points elsewhere, resolve both guide paths inside that selected brain.

## 1. Start

A brain is a folder that has `00_index.md`: the folder a `Project brain:` line or the user names, or a `.brain/` folder in the repository.

**The user gave a path.** If that folder, or the `.brain/` inside it, has `00_index.md`, apply §0, save its location as below, install the guides (§0a) in that selected brain, tell the user `/brain-update` syncs it, and stop. If a different brain also exists at the worktree root or in the main checkout, say that skills will now use the saved one. Otherwise, say it isn't a project brain, and stop; to keep a new brain outside the repository, run `/brain-init` without a path, move the folder, then run `/brain-init <new path>`. To save, work from the checkout root (`git rev-parse --show-toplevel`):

1. In the `CLAUDE.local.md` prepared in §0, put the line `Project brain: <absolute path of the .brain folder>`. Replace an existing `Project brain:` line and keep all other content. A tracked file can be edited but must not be staged or committed; report that status.
2. If the file is untracked, ensure the Git exclusion from §0 is still in place (without adding duplicate entries).
3. Tell the user where you saved it. Claude Code loads `CLAUDE.local.md` from the working directory and every folder above it, so a line saved in the main checkout covers the worktrees inside it, such as `.claude/worktrees/`; a line saved in a linked worktree covers only that worktree.

**No path.** Look where a `Project brain:` line in your loaded instructions points, then at `.brain/` in the current worktree root, then, inside a linked git worktree, at `.brain/` in the main checkout: the parent directory of `git rev-parse --path-format=absolute --git-common-dir`. If any of them is a brain, apply §0, install the guides (§0a) there, tell the user a brain already exists, say where, and stop. If a `Project brain:` line points to a folder that isn't a brain, say so, name the file that holds the line, and stop: `/brain-init <path>` points it at the brain, or the user can remove the line and run `/brain-init` again to create one. Otherwise, check the branch before the first run: the brain describes the main branch, which is `git symbolic-ref --short refs/remotes/origin/HEAD` without the `origin/` prefix. If that fails, it is a local `main` or `master` branch; if neither exists, ask the user which branch it is. If `git branch --show-current` is another branch, or `HEAD` is detached, say so, tell the user to run `/brain-init` from a checkout of the main branch, and stop. Otherwise, apply §0 and do the first run (§2).

**Where the first run creates it.** From a linked git worktree, an untracked brain goes in the main checkout, so every worktree shares it. If the user chooses to track it, or you are not in a linked worktree, it goes at the current worktree root.

**Isolated worktree sessions.** Claude Code isolates a session in a worktree only when the session was started with `claude --worktree` or entered the worktree you are working in with `EnterWorktree`; a linked worktree alone is not isolation. An isolated session can't edit the main checkout. If this session is isolated, or an edit to the main checkout is refused, and the brain would be created there, say so before investigating, and stop. Don't write it anywhere else or through shell commands. Tell the user to run `/brain-init` from a session in the main checkout.

A `.brain/` folder without `00_index.md` (for example, one holding a spec another skill saved) is not a brain; keep its files and index them during the first run.

## 2. First run

Take these steps in order.

1. **Investigate.** Read the README and docs, manifests and dependencies, entry points, module layout, tests, configuration, and recent `git log`. Never ask the user what the repository answers: language, frameworks, commands, settings, schema.
2. **Ask about git tracking. This is the first first-run question unless §0 required resolving a policy conflict.** Ask whether `.brain` should be tracked in git, saying the default is **not tracked**: local to this machine. Recommend the default unless told otherwise. If the answer is no or no preference, ensure `.brain/` appears once in `info/exclude` under `git rev-parse --git-common-dir`. If yes, leave `.brain` visible to git. Either way, you never commit.
3. **Propose moving the documents `.brain` replaces.** List each one found, with its destination from the table below, and wait for approval. If `.brain` is untracked and any of them are tracked, say that moving them takes them out of git for everyone else, and offer to leave those in place, indexed by their current path. Once the user approves, move them. Do not copy, and do not ask again. Use a plain filesystem move, **not `git mv`**, which stages changes and violates the no-stage rule. With tracked documents, Git will show deletions and untracked destinations until the user stages them. Do not overwrite existing destinations; resolve name collisions before moving. Update links to moved files everywhere, including the repository README (not the bundled `.brain/README.md` guide). Check `git diff --cached` before and after to ensure this skill did not stage anything.

   | From | To |
   |---|---|
   | `docs/specs/*` | `.brain/specs/` |
   | `docs/adr/*` (root and context-local) | `.brain/adrs/`, renumbered if numbers collide |
   | `docs/tickets/<f>/issues/*` | `.brain/tickets/<f>/` |
   | `docs/implementation/<f>/todo.md` | `.brain/impl_plans/<f>.md` |
   | `docs/implementation/<f>/guidance.md` | its content into the relevant root files, then delete |
   | `docs/planning/*` | `.brain/planning/` |
   | `docs/diagnoses/*` | `.brain/diagnoses/` |
   | `docs/reviews/architecture/*`, `docs/security/*` | `.brain/reviews/architecture/<NN>-<slug>/review.md`, `.brain/reviews/security/<NN>-<slug>/review.md` (one folder per report; preserve any supporting files in the same folder) |
   | `CONTEXT.md` | entries in `glossary.md`, then delete |
   | `CONTEXT-MAP.md` | domain-boundaries section of `03_architecture.md`, then delete |

4. **Interview the user. This step is required.** Never fill it from defaults, recommendations, or guesses. Ask one question per message about what the code cannot show:
   - purpose;
   - users;
   - goals, non-goals, and priorities;
   - planned features;
   - domain terms the code doesn't define;
   - decisions already made.

   Keep asking until every applicable root file can be written without guessing. When the user doesn't know, record the question in `open_questions.md` and move on. Never ask process questions this skill answers: the file layout, where something is recorded, or how `.brain` is ignored.
5. **Write the brain.** Create the applicable root files (`brain-update` §4) from the templates. Leave out a root file that doesn't apply, and list it in `00_index.md` as "not applicable: <reason>"; never write a placeholder file. Record decisions the user already made in `09_user_decisions.md`, with an ADR only when one qualifies (`brain-update` §5). Planned integrations whose behavior is unverified (file formats, SDKs, OS APIs) go in `spikes.md`. Set `Last synced` to the full 40-character `HEAD` sha, and `Main branch:` to the main branch.
5a. **Install the workflow guides (§0a).** Copy the bundled `USAGE.md` and `README.md` into the brain and register them in `00_index.md`. The guides are not part of the root project-knowledge read.
6. **Report** what you created and moved, then list the open questions and unverified assumptions.
