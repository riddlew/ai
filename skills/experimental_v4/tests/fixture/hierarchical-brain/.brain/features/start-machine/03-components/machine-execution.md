---
id: CMP-002
kind: component
status: approved
parents: [SPEC-001]
requirements: [SPEC-001#REQ-002, SPEC-001#REQ-003, SPEC-001#REQ-004]
depends_on: []
parent_hashes: [SPEC-001@df485fbf629bab9ef550c3826a69635d00444499]
---
# Machine start execution

## Responsibility and outcome

The machine state owner starts an eligible machine and reports a protocol-shaped result; ineligible and unknown machines are rejected without any change.

## Governing requirements and examples

SPEC-001#REQ-002, SPEC-001#REQ-003, and SPEC-001#REQ-004 (the `machine_not_found` part); examples E1–E4.

## In-scope behavior and boundaries

The eligibility rule (enabled and stopped), the stopped-to-running transition, and the `not_eligible` and `machine_not_found` results. No message parsing.

## Interactions with other components

Invoked by CMP-001.

## Unresolved decisions

None.

## Component acceptance / verification

Registry-level tests for E1–E4.
