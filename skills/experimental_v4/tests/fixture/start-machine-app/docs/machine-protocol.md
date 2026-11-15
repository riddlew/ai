# Machine message protocol

Status: approved. This document is the authoritative contract for requests handled by `Session.handle` and the responses it returns.

## Requests

- A request is an object with a string `type` and a non-empty string `machine_id`.
- Supported types: `StopMachine`.
- Adding a message type or an error code requires an approved specification.

## Responses

- Success: `{"ok": true, "state": "<machine state after the operation>"}`.
- Failure: `{"ok": false, "error": "<code>"}`. A failed request never changes machine state.

## Error codes

| Code | Meaning |
|---|---|
| `invalid_message` | The request is not an object, or `machine_id` is missing, empty, or not a string. |
| `unknown_type` | The `type` is not a supported message type. |
| `machine_not_found` | No machine has the given `machine_id`. |
| `not_running` | `StopMachine` targeted a machine that is not running. |
