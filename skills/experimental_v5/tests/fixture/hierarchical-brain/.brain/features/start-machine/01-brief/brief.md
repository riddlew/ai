---
id: BRF-001
kind: brief
status: approved
parents: []
requirements: []
depends_on: []
parent_hashes: []
---
# StartMachine: Brief

## Problem and motivation

Clients can stop a machine through `Session`, but cannot start one: a `StartMachine` request currently returns `unknown_type`.

## Desired outcome

A client sends `StartMachine` through the existing `Session` dispatcher, an eligible machine starts, and the client receives an explicit success or failure response.

## Scope and non-goals

- In scope: handling `StartMachine` requests in `Session` and starting machines through `MachineRegistry`.
- Non-goals: transport framing, authentication and authorization, and any change to `StopMachine`.

## Known constraints and approved decisions

- `Session` keeps routing and connection ownership; `MachineRegistry` keeps machine state transitions (`.brain/adrs/0001-session-routing-registry-state.md`).
- `StartMachine` uses the same request shape as `StopMachine`: `{"type": "StartMachine", "machine_id": "<id>"}`.
- Responses and existing error codes follow `docs/machine-protocol.md`. A successful start returns the machine's new state.

## Success criteria

- An eligible stopped machine starts, and the client receives a success response.
- Malformed requests and unknown machines fail with the existing protocol error codes and change nothing.

## Open decisions

- Which machines are eligible to start: whether `enabled` matters, and what happens when the machine is already running.
- The error code returned when a machine is not eligible to start.

Approval: direction confirmed by the user at the end of the StartMachine brainstorming session.
