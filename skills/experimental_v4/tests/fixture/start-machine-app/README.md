# Machine control

In-memory machine control service. Clients send JSON-like request objects to a `Session`, which validates them and dispatches supported operations to the `MachineRegistry`.

- `machine_control.Session.handle` routes requests and validates their shape.
- `machine_control.MachineRegistry` owns machine state transitions.
- `machine_control.Machine` holds `state` (`"stopped"` or `"running"`) and `enabled`.

Supported request: `{"type": "StopMachine", "machine_id": "a"}`. The message protocol is described in `docs/machine-protocol.md`.

Run the tests with `python -m unittest discover -s tests -v`.
