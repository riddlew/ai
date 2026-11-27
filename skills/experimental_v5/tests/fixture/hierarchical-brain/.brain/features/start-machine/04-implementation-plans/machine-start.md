---
id: PLAN-002
kind: implementation-plan
status: approved
parents: [CMP-002]
requirements: [SPEC-001#REQ-002, SPEC-001#REQ-003, SPEC-001#REQ-004]
depends_on: []
parent_hashes: [CMP-002@eb49583ccbf12aa8f30e0d5541c8b8be5a142044]
---
# Machine start execution: Implementation Plan

Design inspected at: {{BASELINE_SHA}}
Approval: approved by the user in the blueprint review on 2026-11-05.

## Intended changes and unchanged boundaries

Add a `start` operation to `MachineRegistry` in `machine_control.py`, mirroring `stop`. Unchanged: `MachineRegistry.stop`, the `Machine` fields, and `Session` (routing belongs to PLAN-001).

## Existing code and verified owners

- `machine_control.py`, `MachineRegistry`: owns machine state transitions (`stop`).
- `machine_control.py`, `Machine`: holds `state` and `enabled`.

## Binding design constraints and sources

- B1: State transitions stay in `MachineRegistry` (ADR 0001).
- B2: Public method `MachineRegistry.start(self, machine_id: str) -> dict` returns the protocol response object (approved in the blueprint review).
- B3: No new class, manager, or module.
- Illustrative: the order of the checks inside `start`, and any private helper.

## Proposed files, interfaces, and data/control flow

`start` looks up the machine and returns `{"ok": False, "error": "machine_not_found"}` when it is absent, `{"ok": False, "error": "not_eligible"}` unless `enabled` is true and `state == "stopped"`, and otherwise sets `state = "running"` and returns `{"ok": True, "state": "running"}`.

## Increments

- INC-1: Start an eligible machine and report an unknown machine (E1, E4).
- INC-2: Reject disabled or already running machines without change (E2, E3). Depends on INC-1, which creates `start`.

## Failure paths, compatibility, and risks

Failures never change state. No compatibility impact: StartMachine is new.

## Verification strategy

Registry-level unit tests for E1–E4 in `tests/test_machine_control.py`; the existing StopMachine tests must still pass.

## Assumptions and blockers

None.
