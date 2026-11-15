---
id: TASK-002
kind: task
status: approved
parents: [PLAN-001]
requirements: [SPEC-001#REQ-001, SPEC-001#REQ-004, SPEC-001#REQ-005]
depends_on: [TASK-001]
parent_hashes: [PLAN-001@5a215d347ecf892f4533d174897429c444a271bd]
---
# Route StartMachine through Session

## Action and implementation context

Extend `Session.handle` in `machine_control.py` to accept `StartMachine` and call `MachineRegistry.start` (PLAN-001 INC-3).

## Expected behavior / result

Valid StartMachine requests reach `MachineRegistry.start` and return its result; malformed ones return `invalid_message`; StopMachine and unknown types behave as before.

## Applicable design constraints

PLAN-001 B1–B3.

## Acceptance criteria and examples

SPEC-001 E5 and E6, plus E1 and E4 through `Session.handle`.

## Verification

`python -m unittest discover -s tests -v` passes.
