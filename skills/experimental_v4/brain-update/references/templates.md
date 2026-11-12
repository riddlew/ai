# Brain Templates

Adapt the content to the project. Keep the header lines of `00_index.md` exact; other skills and later runs parse them.

## `00_index.md`

```markdown
# Project Brain Index

Last synced: <40-character commit sha> (<YYYY-MM-DD>)
Git: ignored
Main branch: main

## Root files

| File | Purpose | Status |
|---|---|---|
| `01_about.md` | What the project is and who uses it | current |
| `06_ux_interface.md` | — | not applicable: <reason> |

## Documents

| Path | Purpose | Status |
|---|---|---|
| `specs/01-<slug>.md` | <one line> | draft / approved / implemented / superseded |
| `adrs/0001-<slug>.md` | <one line> | accepted / superseded |
| `tickets/<feature>/` | <one line> | open / in progress / done |
| `impl_plans/<feature>.md` | Implementation design and progress | design draft / design approved / in progress / done |
| `planning/<feature>/` | <one line> | active / done |
| `diagnoses/01-<slug>.md` | <one line> | recorded |
| `reviews/architecture/01-<slug>.md` | <one line> | recorded |
| `docs/adr/0002-<slug>.md` | Left in place at the user's request | accepted |
| `pending/<branch>.md` | Changes waiting for `<branch>` to merge | pending |
```

`Git:` is `ignored` or `tracked`. `Main branch:` names the branch the root files describe.

## `pending/<branch>.md`

A `/` in the branch name becomes `--` in the file name (`feature/cue-points` → `pending/feature--cue-points.md`).

```markdown
# Pending brain changes: <branch>

Branch: <branch>
Base: <40-character merge-base sha>
Updated: <40-character branch HEAD sha> (<YYYY-MM-DD>)

Apply these to the root files when the branch merges, after checking each against the merged code.

## 02_features.md

- **Add:** <what the branch adds>. Source: `specs/NN-<slug>.md`.
- **Change:** <old description> → <new description>.

## 04_data_model.md

- **Remove:** <what the branch removes>.
```

## Technical knowledge document (optional)

Use when a subsystem or API needs durable detail beyond the root overview. Include only applicable sections; avoid function-by-function code duplication.

```markdown
# <Subsystem or API>

## Sources
- `src/path/to/owner`
- `src/path/to/caller-or-test`

## How it works
<Behavior, ownership, flow, and important interactions.>

## Contracts and invariants
<Inputs, outputs, guarantees, edge cases, compatibility limits.>

## Known pitfalls
<Unexpected behavior and constraints worth preserving.>

## Verification
<What was checked, on which branch/revision; what remains uncertain.>
```

## `09_user_decisions.md` entry

```markdown
- **<YYYY-MM-DD> — <Decision, stated as chosen>.** <Rationale the user gave, or "No rationale given.">
  Source: <conversation | specs/NN-<slug>.md | adrs/NNNN-<slug>.md>
```

## `glossary.md`

```markdown
| Term | Definition | Code / DB | Avoid |
|---|---|---|---|
| **Crate** | A named, ordered collection of tracks. | `Crate` class; `playlists` table | "Playlist" in user-facing text |
```

When the project has several domains, use one section and table per domain.

## `open_questions.md` entry

```markdown
- **<Question?>** <Why it matters.> Blocks: <what, or "nothing yet">. Raised <YYYY-MM-DD>.
```

## `spikes.md` entry

```markdown
- <Assumption> — unverified — <why it matters>.
- <Assumption> — deferred — <risk note>.
```

## `state.md`

```markdown
| Feature | Status | Links |
|---|---|---|
| <Feature> | planned / in progress / done | `specs/NN-<slug>.md`, `impl_plans/<feature>.md` |
```

## ADR

```markdown
# <Approved Decision>

## Context
The actual constraints and situation.

## Decision
What was selected, and its scope.

## Rationale
Why this option was chosen over the meaningful alternatives. Label the user's stated reasons separately from inferred implications.
```

Add Consequences, Alternatives, Status, or References only when useful.
