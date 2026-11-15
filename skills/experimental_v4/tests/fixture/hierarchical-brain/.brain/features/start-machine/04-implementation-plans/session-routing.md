---
id: PLAN-001
kind: implementation-plan
status: approved
parents: [CMP-001]
requirements: [SPEC-001#REQ-001, SPEC-001#REQ-004, SPEC-001#REQ-005]
depends_on: [PLAN-002]
parent_hashes: [CMP-001@cb3f3305859e5a56d4edb3cce10003350e7ec24c]
---
# Message routing and validation: Implementation Plan

Design inspected at: {{BASELINE_SHA}}
Approval: approved by the user in the blueprint review on 2026-11-05.

## Intended changes and unchanged boundaries

Extend `Session.handle` in `machine_control.py` to accept `StartMachine` and dispatch valid requests to `MachineRegistry.start` (PLAN-002). Unchanged: StopMachine handling and responses, `unknown_type` for other types, and `Session` ownership of routing.

## Existing code and verified owners

- `machine_control.py`, `Session.handle`: validates the request object, its `type`, and `machine_id`, then calls the registry.

## Binding design constraints and sources

- B1: Routing and validation stay in `Session.handle` (ADR 0001; `09_user_decisions.md`).
- B2: StartMachine uses the same `machine_id` validation as StopMachine and fails with `invalid_message` (`docs/machine-protocol.md`).
- B3: `Session` returns the registry result unchanged.
- Illustrative: whether dispatch uses `if`/`elif` or a small mapping.

## Proposed files, interfaces, and data/control flow

`Session.handle` keeps its object check, accepts `type` in `{"StopMachine", "StartMachine"}`, validates `machine_id`, and calls `self.registry.stop` or `self.registry.start`.

## Increments

- INC-3: Route valid StartMachine requests to `MachineRegistry.start` and reject malformed ones (E5; E1 and E4 end to end; E6 unchanged). Depends on PLAN-002 INC-1.

## Failure paths, compatibility, and risks

Unknown types still return `unknown_type`. StopMachine responses must not change.

## Verification strategy

Session-level tests in `tests/test_machine_control.py` for E1, E4, E5, and E6.

## Assumptions and blockers

None.
