---
name: brain-init
description: Use when the user asks to set up a project brain, or to save where an existing project brain lives.
---

# Brain Init

Sets up a project's `.brain/`, or connects the project to an existing one. `brain-update` maintains the brain afterward. For what goes where, read §3 (root files) and §4 (ADRs) of `${CLAUDE_SKILL_DIR}/../brain-update/SKILL.md`; read the file, don't invoke that skill. The templates are in `${CLAUDE_SKILL_DIR}/../brain-update/references/templates.md`. Follow root `CLAUDE.md` for decision authority.

**Always:**

- Write only inside `.brain/`, plus `info/exclude`, `CLAUDE.local.md` when saving a location (§1), and the approved moves in §2 step 3, including deleting originals and fixing links to them anywhere. Learn facts by reading code and git history. Never run the project's code, tests, or build; a fact that needs an experiment goes in `spikes.md`.
- Never edit documents other skills own (`specs/`, `tickets/`, `impl_plans/`, `planning/`, `diagnoses/`, `reviews/`) beyond moving them in §2 step 3 and fixing links to moved files.
- Never stage, commit, or push.
- Never dispatch subagents unless the user asks.
- Ask the user one question per message.

## 1. Start

A brain is a folder that has `00_index.md`: the folder a `Project brain:` line or the user names, or a `.brain/` folder in the repository.

**The user gave a path.** If that folder, or the `.brain/` inside it, has `00_index.md`, save its location as below, tell the user `/brain-update` syncs it, and stop. If a different brain also exists at the worktree root or in the main checkout, say that skills will now use the saved one. Otherwise, say it isn't a project brain, and stop; to keep a new brain outside the repository, run `/brain-init` without a path, move the folder, then run `/brain-init <new path>`. To save, work from the checkout root (`git rev-parse --show-toplevel`):

1. In `CLAUDE.local.md` there, put the line `Project brain: <absolute path of the .brain folder>`. Replace an existing `Project brain:` line and keep the rest of the file. If git tracks `CLAUDE.local.md` (`git ls-files --error-unmatch CLAUDE.local.md` succeeds), don't write it; give the user the line instead.
2. Unless `git check-ignore -q CLAUDE.local.md` succeeds, append `CLAUDE.local.md` to `info/exclude` under `git rev-parse --git-common-dir`.
3. Tell the user where you saved it. Claude Code loads `CLAUDE.local.md` from the working directory and every folder above it, so a line saved in the main checkout covers the worktrees inside it, such as `.claude/worktrees/`; a line saved in a linked worktree covers only that worktree.

**No path.** Look where a `Project brain:` line in your loaded instructions points, then at `.brain/` in the current worktree root, then, inside a linked git worktree, at `.brain/` in the main checkout: the parent directory of `git rev-parse --path-format=absolute --git-common-dir`. If any of them is a brain, tell the user a brain already exists, say where, and stop. If a `Project brain:` line points to a folder that isn't a brain, say so, name the file that holds the line, and stop: `/brain-init <path>` points it at the brain, or the user can remove the line and run `/brain-init` again to create one. Otherwise, do the first run (§2).

**Where the first run creates it.** From a linked git worktree, an untracked brain goes in the main checkout, so every worktree shares it. If the user chooses to track it, or you are not in a linked worktree, it goes at the current worktree root.

**Isolated worktree sessions.** Claude Code isolates a session in a worktree only when the session was started with `claude --worktree` or entered the worktree you are working in with `EnterWorktree`; a linked worktree alone is not isolation. An isolated session can't edit the main checkout. If this session is isolated, or an edit to the main checkout is refused, and the brain would be created there, say so before investigating, and stop. Don't write it anywhere else or through shell commands. Tell the user to run `/brain-init` from a session in the main checkout.

A `.brain/` folder without `00_index.md` (for example, one holding a spec another skill saved) is not a brain; keep its files and index them during the first run.

## 2. First run

Take these steps in order.

1. **Investigate.** Read the README and docs, manifests and dependencies, entry points, module layout, tests, configuration, and recent `git log`. Never ask the user what the repository answers: language, frameworks, commands, settings, schema.
2. **Ask about git tracking. This is your first question.** Ask whether `.brain` should be tracked in git, saying the default is **not tracked**: local to this machine. Recommend the default unless told otherwise. If the answer is no or no preference, append `.brain/` to `info/exclude` under `git rev-parse --git-common-dir`. If yes, leave `.brain` visible to git. Either way, you never commit.
3. **Propose moving the documents `.brain` replaces.** List each one found, with its destination from the table below, and wait for approval. If `.brain` is untracked and any of them are tracked, say that moving them takes them out of git for everyone else, and offer to leave those in place, indexed by their current path. Once the user approves, move them. Do not copy, and do not ask again. Use `git mv` when `.brain` is tracked, or plain `mv` when it is not; git then shows the old paths as deleted, and you don't commit. Update links to moved files everywhere, including the README.

   | From | To |
   |---|---|
   | `docs/specs/*` | `.brain/specs/` |
   | `docs/adr/*` (root and context-local) | `.brain/adrs/`, renumbered if numbers collide |
   | `docs/tickets/<f>/issues/*` | `.brain/tickets/<f>/` |
   | `docs/implementation/<f>/todo.md` | `.brain/impl_plans/<f>.md` |
   | `docs/implementation/<f>/guidance.md` | its content into the relevant root files, then delete |
   | `docs/planning/*` | `.brain/planning/` |
   | `docs/diagnoses/*` | `.brain/diagnoses/` |
   | `docs/reviews/architecture/*`, `docs/security/*` | `.brain/reviews/architecture/`, `.brain/reviews/security/` |
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
5. **Write the brain.** Create the applicable root files (`brain-update` §3) from the templates. Leave out a root file that doesn't apply, and list it in `00_index.md` as "not applicable: <reason>"; never write a placeholder file. Record decisions the user already made in `09_user_decisions.md`, with an ADR only when one qualifies (`brain-update` §4). Planned integrations whose behavior is unverified (file formats, SDKs, OS APIs) go in `spikes.md`. Set `Last synced` to the full 40-character `HEAD` sha.
6. **Report** what you created and moved, then list the open questions and unverified assumptions.
