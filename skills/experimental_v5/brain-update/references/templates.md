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
| `USAGE.md` | Brain Skills workflow examples and selection guide | reference |
| `README.md` | Brain Skills catalog and installation reference | reference |
| `features/<slug>/01-brief/brief.md` | Desired outcome and success criteria | optional / no approval state |
| `features/<slug>/02-specifications/<name>.md` | Normative behavior and examples | optional / no approval state |
| `features/<slug>/03-components/<name>.md` | Functional decomposition and coverage | optional / no approval state |
| `adrs/0001-<slug>.md` | <one line> | accepted / superseded |
| `features/<slug>/04-implementation-plans/<name>.md` | Codebase-aware technical design | optional / no approval state |
| `features/<slug>/05-tasks/<name>.md` | Executable implementation task | optional / no approval state |
| `features/<slug>/execution.md` | Observed progress and verification | in progress / blocked / done |
| `planning/<feature>/` | <one line> | active / done |
| `diagnoses/01-<slug>.md` | <one line> | recorded |
| `reviews/architecture/01-<slug>/review.md` | <one line> | recorded |
| `docs/adr/0002-<slug>.md` | Left in place at the user's request | accepted |
| `pending/<branch>.md` | Changes waiting for `<branch>` to merge | pending |
| `sources/<source-slug>.md` | Source map, exact references, and coverage for an authoritative document | indexed / partial / stale |
| `knowledge/<domain>/<topic>.md` | Detailed technical knowledge with source references | current / partial / stale |
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

- **Add:** <what the branch adds>. Source: `features/<slug>/02-specifications/<name>.md`.
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

## `sources/<source-slug>.md` (authoritative source map)

Use one source map per designated authoritative document. Do not claim the full document was indexed unless all relevant sections were actually inspected.

```markdown
# <Document title> — Source Map

Authoritative source: `docs/<path-to-original.pdf>`
Authority established by: <user instruction or applicable approved project record>
Version / revision: <version or "unknown">
Content fingerprint: <SHA-256 or "not available">
Checked: <YYYY-MM-DD>
Coverage: indexed / partial / unverified / stale

## Scope
<Which systems, protocols, and versions the source governs.>

## Section map
| Source section / page / table | Technical topic | Brain knowledge | Coverage |
|---|---|---|---|
| §3.1, pp. 14–16, Table 2 | Frame header | `knowledge/protocols/tcp-framing.md` | indexed |
| §3.2, p. 17 | Error handling | `knowledge/protocols/errors.md` | partial |

## Missing or uncertain coverage
<Unreviewed sections, unreadable diagrams, ambiguous source locations.>

## Source changes
<Meaningful changes since the previous verified version and affected knowledge paths.>
```

Use exact references found in the original; the values above are illustrative.

## `knowledge/<domain>/<topic>.md` (source-derived technical knowledge)

Keep documents topic-specific. Include only applicable sections; use precise references for each important contract, especially message formats and state-machine transitions.

```markdown
# <Technical topic>

## Provenance
- Governing source: `docs/<path-to-original.pdf>` (version <...>)
- Source map: `sources/<source-slug>.md`
- Relevant sections: <actual section IDs, pages, tables, figures>
- Checked: <YYYY-MM-DD>; coverage: current / partial / stale

## How it works
<Useful technical model: responsibilities, flow, and interactions.>

## Explicit source requirements
- <Behavior, field layout, ranges, failure semantics, or timing rules.>
  Source: <exact section/page/table/requirement ID>.

## Contracts and pitfalls
<Important invariants, edge cases, version limits, and common mistakes.>

## Current implementation (if verified)
- <Code path and observed behavior, or "not yet implemented".>

## Uncertainty and verification
<Missing evidence, disagreements with code, checks needed against the original.>
```

The original source remains authoritative. Do not copy entire documents, invent details for uninspected sections, or record source requirements as user-established decisions.

## Compact entry rule

Use `brain-init/references/compact-writing.md` for project root facts, decisions, source summaries, indexes and ADRs. Prefer concise clauses, stable paths and a table for repeated fields; retain user rationale and source/verification scope, do not silently replace normative requirements with summaries.

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
| <Feature> | planned / in progress / done | `features/<slug>/02-specifications/<name>.md`, `features/<slug>/execution.md` |
```

## ADR

```markdown
# <Established Decision>

## Context
The actual constraints and situation.

## Decision
What was selected, and its scope.

## Rationale
Why this option was chosen over the meaningful alternatives. Label the user's stated reasons separately from inferred implications.
```

Add Consequences, Alternatives, Status, or References only when useful.
