# Worked example: StartMachine through the five document levels

This is a **planning and traceability example**, not a verified software implementation. The fixture at `skills/experimental_v4/tests/fixture/hierarchical-brain/.brain/features/start-machine/` is synthetic. It can validate document references and coverage, but does not prove an actual TCP server accepts `StartMachine`.

## Starting intent and governing decision

The user requests a TCP server operation that starts an eligible stopped machine and returns a protocol-compliant result. An illustrative approved ADR at `.brain/adrs/001-session-owns-connection.md` says the existing session object retains connection ownership; no new connection manager may be introduced without approval.

The ADR is referenced in document prose, **not** placed in `parents:`: parents belong exclusively to the five-level hierarchy. If the ADR does not exist or is unapproved, do not claim it as established. Record the open design question instead.

## 1. Brief — `01-brief/brief.md`

```yaml
---
id: BRF-001
kind: brief
status: approved
parents: []
requirements: []
depends_on: []
parent_hashes: []
---
```

**Desired outcome:** An authorized TCP client can request that an eligible machine start.

**Scope:** The request path, eligibility checks, machine-start invocation and response.

**Non-goals:** Replacing connection ownership, introducing a new manager or changing unrelated protocol messages.

**Success:** Eligible machines start; ineligible machines do not change state; clients receive a protocol-conformant result.

## 2. Specification — `02-specifications/start-machine.md`

```yaml
---
id: SPEC-001
kind: specification
status: approved
parents: [BRF-001]
requirements: []
depends_on: []
parent_hashes: [BRF-001@<actual-git-blob-hash>]
---
```

Approved normative behavior:

- `REQ-001`: A valid StartMachine message reaches the existing machine-start execution path.
- `REQ-002`: Ineligible targets are rejected without changing machine state.
- `REQ-003`: Every processed request returns a protocol-conformant success or failure response.

Concrete examples:

- `E1`: Given an eligible stopped machine, when a valid request arrives, the machine starts and a success result is returned.
- `E2`: Given an ineligible target, when a request arrives, machine state is unchanged and failure is returned.

A real specification must define the *exact* message fields, eligibility rules, errors and wire responses **from approved contracts or authoritative sources**. Those values are deliberately omitted here because this example has no actual target protocol. Do not turn this example's unspecified wire encoding into a production decision.

## 3. Components — `03-components/`

| Component | Functional ownership | Requirements | Examples |
|---|---|---|---|
| `CMP-001` — Message routing | Existing dispatcher accepts StartMachine and routes/returns the response | `SPEC-001#REQ-001`, `SPEC-001#REQ-003` | `SPEC-001#E1`, `SPEC-001#E2` |
| `CMP-002` — Machine execution | Existing machine owner checks eligibility and starts only eligible targets | `SPEC-001#REQ-001`, `SPEC-001#REQ-002` | `SPEC-001#E1`, `SPEC-001#E2` |

Both components participate in `REQ-001`, but dispatch and state-transition ownership remain distinct. This is **functional decomposition**: it does not mandate two new classes or services.

Each approved component has `parents: [SPEC-001]` and `parent_hashes: [SPEC-001@<actual-git-blob-hash>]`. Any new consequential responsibility boundary must be approved before it is treated as binding.

## 4. Implementation plans — `04-implementation-plans/`

- `PLAN-001` — routing: `parents: [CMP-001]`. Inspect the real dispatcher and its callers, then identify the smallest modification that preserves the approved transport behavior.
- `PLAN-002` — execution: `parents: [CMP-002]`. Inspect the current machine-start owner, concurrency constraints and test boundaries; verify the rejection path leaves state unchanged.

An implementation plan contains its own `Design inspected at:` SHA, approved binding design constraints, known owners, intended changes and verification strategy. A SHA or file path is **not invented** when no codebase has been inspected. The sample fixture uses an explicitly illustrative inspection value and must not be adopted unchanged.

`brain-blueprint` records explicit user approval of binding design; it never writes the mutable execution checklist into the plan.

## 5. Tasks — `05-tasks/`

| Task | Parent plan | Action and verification | Dependencies |
|---|---|---|---|
| `TASK-001` — execute machine | `PLAN-002` | Implement eligibility check and machine start; targeted success/failure tests | None |
| `TASK-002` — route message | `PLAN-001` | Bind request routing to the existing owner and validate success/failure responses | `TASK-001` if the routing verification genuinely requires its result |

The dependency is an illustrative technical precondition, not an automatic consequence of numbering. Tasks preserve qualified requirement IDs, example coverage, independent acceptance criteria and approved parent fingerprints. They must not introduce extra protocol semantics.

## 6. Execution — `execution.md`

The execution record is outside the five levels. `brain-implement` records:

- Verified original Git review base, current branch and workspace.
- Each task's actual progress, blockers, tests and observed results.
- Collaborative user-review checkpoints and deviations from binding design.
- Resumption verification against actual code, Git status and tests.

A checked task is not proof of implementation. The illustrative feature fixture records every task as pending and does not claim production changes.

## Traceability and reapproval

The requirement-to-task chains are:

```text
BRF-001
  └── SPEC-001
       ├── REQ-001 → CMP-001 → PLAN-001 → TASK-002
       │           → CMP-002 → PLAN-002 → TASK-001
       ├── REQ-002 → CMP-002 → PLAN-002 → TASK-001
       └── REQ-003 → CMP-001 → PLAN-001 → TASK-002
```

All approved child files record **content fingerprints** of their direct parents, not arbitrary text placeholders. Obtain the actual values with:

```bash
python "${CLAUDE_SKILL_DIR}/../brain-init/scripts/validate_feature_docs.py" --show-parent-hashes ".brain/features/start-machine/03-components/message-routing.md"
python "${CLAUDE_SKILL_DIR}/../brain-init/scripts/validate_feature_docs.py" .brain/features --check-coverage
```

If the user changes the approved eligibility requirement, the specification is revised first; dependent components, plans and tasks are reviewed and, where necessary, marked `needs-revision`. Do not merely refresh hashes to bypass that review. Unaffected authorized work can continue.

**Limits of this example:** All messages, protocols and component boundaries here are illustrative until checked against an actual project. Structural validation demonstrates document consistency only. Fresh-agent behavioral tests and actual implementation verification remain separate requirements.
