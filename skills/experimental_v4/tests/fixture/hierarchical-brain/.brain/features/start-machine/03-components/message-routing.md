---
id: CMP-001
kind: component
status: approved
parents: [SPEC-001]
requirements: [SPEC-001#REQ-001, SPEC-001#REQ-004, SPEC-001#REQ-005]
depends_on: []
parent_hashes: [SPEC-001@df485fbf629bab9ef550c3826a69635d00444499]
---
# Message routing and validation

## Responsibility and outcome

Recognizes StartMachine requests, rejects malformed ones, and forwards valid ones to machine start execution, returning its result unchanged. StopMachine routing is unchanged.

## Governing requirements and examples

SPEC-001#REQ-001, SPEC-001#REQ-004 (the `invalid_message` part), and SPEC-001#REQ-005; examples E5 and E6, and the end-to-end path of E1 and E4.

## In-scope behavior and boundaries

Message type recognition, `machine_id` shape validation, and dispatch. Does not decide eligibility or change machine state.

## Interactions with other components

Calls the start operation of CMP-002 for valid requests.

## Unresolved decisions

None.

## Component acceptance / verification

Session-level tests for E5 and E6; E1 and E4 observed through `Session.handle`.
