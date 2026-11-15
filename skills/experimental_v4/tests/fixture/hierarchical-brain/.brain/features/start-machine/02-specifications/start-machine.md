---
id: SPEC-001
kind: specification
status: approved
parents: [BRF-001]
requirements: []
depends_on: []
parent_hashes: [BRF-001@885995121a1e0d956251b9ce061ddadefd5f2bb7]
---
# StartMachine: Specification

## Problem and desired outcome

Clients can stop machines but not start them. `StartMachine` starts an eligible machine through the existing `Session` dispatcher and reports the result in the protocol's response shape.

## Requirements and invariants

- REQ-001: `Session.handle` accepts `{"type": "StartMachine", "machine_id": <non-empty string>}` and routes it to the machine start operation owned by `MachineRegistry`.
- REQ-002: A machine is eligible to start only when `enabled` is true and `state` is `"stopped"`. Starting an eligible machine sets `state` to `"running"` and returns `{"ok": true, "state": "running"}`.
- REQ-003: A StartMachine request for an ineligible machine returns `{"ok": false, "error": "not_eligible"}` and leaves the machine unchanged.
- REQ-004: A StartMachine request whose `machine_id` is missing, empty, or not a string returns `{"ok": false, "error": "invalid_message"}`; an unknown `machine_id` returns `{"ok": false, "error": "machine_not_found"}`. Neither changes any machine.
- REQ-005: Existing `StopMachine` behavior and responses are unchanged.

## Examples

- E1: Given machine `a` with `enabled=True, state="stopped"`, when `{"type": "StartMachine", "machine_id": "a"}` is handled, then the response is `{"ok": true, "state": "running"}` and `a.state` is `"running"`.
- E2: Given machine `a` with `enabled=False, state="stopped"`, when StartMachine for `a` is handled, then the response is `{"ok": false, "error": "not_eligible"}` and `a.state` stays `"stopped"`.
- E3: Given machine `a` with `enabled=True, state="running"`, when StartMachine for `a` is handled, then the response is `{"ok": false, "error": "not_eligible"}` and `a.state` stays `"running"`.
- E4: Given no machine `missing`, when StartMachine for `missing` is handled, then the response is `{"ok": false, "error": "machine_not_found"}`.
- E5: Given machine `a` stopped and enabled, when `{"type": "StartMachine", "machine_id": ""}`, `{"type": "StartMachine"}`, or `{"type": "StartMachine", "machine_id": 42}` is handled, then each response is `{"ok": false, "error": "invalid_message"}` and `a.state` stays `"stopped"`.
- E6: The existing StopMachine tests pass unchanged.

## Technical Decisions

- `Session.handle` remains the dispatcher and `MachineRegistry` the owner of state transitions (ADR 0001; `09_user_decisions.md`).
- Response shapes and existing error codes follow `docs/machine-protocol.md`.
- The eligibility rule and the `not_eligible` code resolve the brief's open decisions (user decision recorded in `09_user_decisions.md`, 2026-11-03).

## Verification Strategy

Unit tests in `tests/` using the existing boundaries: `MachineRegistry` tests verify E1–E4; `Session.handle` tests verify E1, E4, E5, and E6 end to end.

## Open Decisions

None. Authorization is a non-goal of BRF-001.

## Exclusions

Transport framing, authorization, and changes to `StopMachine`.
