## What this skill does

The goal is to keep track of important information, the state of a codebase, decisions made, and to act like a central brain for AI so that it can obtain critical information across sessions without having to re-read large amounts of code and documentation. These files are updated throughout sessions to keep track, add, and remove information.

The brain consists of the following files:
```text
.brain
├── /adrs                Generated ADRs
├── /impl_plans          Generated implementation plans from users or specifications
├── /specs               Generated specifications of planned features
├── /tickets             Generated tickets from `write-tickets`
├── 00_index.md          Running index of all docs and their statuses
├── 01_about.md          What the app is, core concepts, how it works
├── 02_features.md       Capabilities grouped by module / feature
├── 03_architecture.md   Stack, framework, runtime, platform support, application design
├── 04_data_model.md     Entities, schema, relationships, derived data
├── 05_settings.md       User-configurable surface
├── 06_ux_interface.md   Visual language, layouts, interactions
├── 07_integrations.md   External tools, file formats, OS APIs
├── 08_error_logging.md  Operational concerns, observability
├── 09_user_decisions.md Open ended questions that were resolved by the user
├── glossary.md          Canonical terms for the project (see below)
├── open_questions.md    Open questions that have not been answered yet. Things assumed to work that need verification. Once these are answered, the information should be documented in the relevant files in `.brain`
├── state.md             Checklist of features that are planned or implemented
```

### glossary.md is required

When the app sits in a specialized domain (DJ, audio, broadcast, legal,
medical, finance, scientific instrumentation, etc.) terminology drifts
fast across docs. The same concept ends up with three names. Two
different concepts collide on one name. Both bugs are silent and
expensive to fix later.

Maintain `glossary.md` from day one. Every domain term, every internal
concept name, every UI-facing label that has a technical counterpart
(e.g. "Track Elements" surface label vs. "Segments" DB term) goes
here, with a one-line canonical definition. All other docs use the
canonical term.


### state.md is required

Maintain `state.md` to help agents stay on task and track their progress.


### The specified files are just a starting point

`00_index.md` through `09_user_decisions.md` are just a starting point.
There may be occasions where an additional file would make sense.

For example, if an application involves specific custom communication
protocols via TCP, you might create an additional `XX_protocols.md`, where
`XX` is the next number sequence. In this example, this file would outline
the planned communication protocols.


### spikes.md tracks unverified assumptions

Architecture docs tend to assume third-party tools, libraries, and OS
APIs behave as documented. Often they don't, especially for
reverse-engineered formats, proprietary SDKs, and platform-specific
audio/driver work. Track these explicitly:

```
- VST3 hosting in <chosen framework> at low latency — unverified
- Direct write to Rekordbox 7.x SQLite — unverified, fragile to updates
- faiss memory footprint with N-dim embeddings at 250k tracks — unverified
- ASIO driver enumeration via <library> on Windows 11 24H2 — unverified
```

Each spike resolves into either a confirmed assumption (move to
architecture doc), a confirmed problem (becomes a decision in
DECISIONS.md), or a deferred risk (stays in spikes.md with a note).


### Splitting and naming

When a doc passes roughly 3–5k words, split it (e.g.
`02_feature_modules.md` → `02a_feature_library_manager.md`,
`02b_feature_set_planner.md`) and leave a stub in the original
pointing to the children. Numeric prefixes keep ordering stable in
file listings.


## Running for the first time

When this skill runs, it should check that `.brain` exists. If it
does not, it can assume this is the first time it is running for
a project.

The first time it runs in a project, it should thoroughly investigate
and learn about the project / codebase. It should also grill the user
repetitively until it has a clear understanding about the project.

Once it has reached a thorough understanding, it should create
`.brain` and its files. Any open questions or assumptions that need
verification should be output to the user and documented in
`.brain/open_questions.md`.


## Running in a new session

When any of the skills in this folder (`brainstorm`, `implement`, etc)
are called in a new session or a session where `.brain` has not been
read in context, it should immediately read it to gain an understanding
about the project.


## Running during/after a session

Other skills may call this skill to update `.brain` during or after
a session. Updating this folder should always be delegated to this
skill for consistency and to ensure all proper steps are taken when
updating it.

This skill should check for changes, git commits, etc and update
all `.brain` files accordingly.


## Current skills

The current skills need to be modified to work with `.brain`.
Specifications and implementation plans should be written to
`.brain/specs` and `.brain/impl_plans`. ADRs are written to
`.brain/adrs`. Other files such as `CONTEXT.md` should be
replaced by using `.brain`. Any files that will not be
replaced by `.brain` should be raised as an issue so
I can figure out where that content will go. The goal is
to have all files and folders go to `.brain` as a central
source.
