# Blueprint template

Create or update the **Implementation Design** section of the one per-feature file under `.brain/impl_plans/`. This is a proposal and continuity aid, not an authority over specifications, ADRs, or durable user decisions. Include only relevant sections; preserve any existing execution sections verbatim except for changes separately requested by the user.

For a new file:

```markdown
# <Feature> — Implementation Plan

Specification: `.brain/specs/<NN>-<feature>.md` (if applicable)
Tickets: `.brain/tickets/<feature>/` (if applicable)
Blueprint status: draft
Design inspected at: <full HEAD SHA>
Blueprint approval: not yet approved

## Implementation Design

### Intended change and unchanged boundaries
- Change: <observable feature and affected owners>
- Keep unchanged: <explicit constraints and relevant existing behavior>

### Binding design constraints
- <approved ownership, pattern, interface, contract, or other constraint>.
  Source: <spec/ADR/decision or explicit user approval>.

### Proposed structure
| Existing file / component | Current owner / behavior | Proposed edit | Why |
|---|---|---|---|
| `src/...` | ... | ... | ... |

### Interfaces and call flow
<Important signatures, call sequence, state changes, and failure paths.>
<Mark code examples 'Binding' only when the user approved their exact structure;
otherwise mark 'Illustrative' and describe the actual invariant.>

### Method outlines (optional)
- `<signature>` — inputs/outputs and responsibility
  - Intended steps and key invariants (comments or pseudocode as requested)
  - Failure behavior, caller expectations, and interaction with existing owners
  - Binding or Illustrative (state which; omit this section when it adds no value)

### Behavioral increments and verification
1. <Small coherent behavior> — <Examples / criteria> — <targeted verification>
2. ...

### Assumptions and blockers
- <Unverified fact or unresolved consequential decision; or None>

```

Once the user approves, update the header:

```markdown
Blueprint status: approved
Blueprint approval: user confirmed <YYYY-MM-DD> (<conversation or linked decision>)
```

`brain-implement` subsequently adds `Review base:`, `Branch:`, `Collaboration mode:`, `Workspace:`, `Execution mode:` and mutable `## Work Items`, `## Verification`, etc. **Do not create a second implementation plan or duplicate this design under another filename.**

**Quality rules**
- Source paths and signatures must be grounded in inspected code, not guessed.
- Separate approved design constraints from illustrative suggestions and unresolved proposals.
- Leave unnecessary method details to implementation; honor exact signatures or detailed pseudocode only where the user deliberately wants them.
- Each increment should be demonstrably correct on its own; avoid a purely "models → services → UI" sequence unless the intermediate state has independent verification value.
- The spec governs requirements; the blueprint cannot approve new behavior or override an ADR.
