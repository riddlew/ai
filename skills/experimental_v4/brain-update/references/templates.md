# Brain Templates

Adapt the content to the project. Keep the header lines of `00_index.md` exact; other skills and later runs parse them.

## `00_index.md`

```markdown
# Project Brain Index

Last synced: <40-character commit sha> (<YYYY-MM-DD>)
Git: ignored

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
| `impl_plans/<feature>.md` | <one line> | open / in progress / done |
| `planning/<feature>/` | <one line> | active / done |
| `diagnoses/01-<slug>.md` | <one line> | recorded |
| `reviews/architecture/01-<slug>.md` | <one line> | recorded |
| `docs/adr/0002-<slug>.md` | Left in place at the user's request | accepted |
```

`Git:` is `ignored` or `tracked`.

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
