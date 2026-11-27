---
id: TASK-001
kind: task
status: approved
parents: [PLAN-002]
requirements: [SPEC-001#REQ-002, SPEC-001#REQ-003, SPEC-001#REQ-004]
depends_on: []
parent_hashes: [PLAN-002@8998a75d7b5114ab54bf875c1bf67e23307395cc]
---
# Add MachineRegistry.start

## Action and implementation context

Add `MachineRegistry.start(self, machine_id: str) -> dict` in `machine_control.py` (PLAN-002 INC-1 and INC-2).

## Expected behavior / result

An eligible machine (enabled and stopped) starts; a disabled or running machine returns `not_eligible`; an unknown machine returns `machine_not_found`. Failures change nothing.

## Applicable design constraints

PLAN-002 B1–B3. Do not change `Session` or `stop`.

## Acceptance criteria and examples

SPEC-001 E1–E4, asserted at the registry level, including unchanged state for E2 and E3.

## Verification

`python -m unittest discover -s tests -v` passes, including the existing StopMachine tests.
