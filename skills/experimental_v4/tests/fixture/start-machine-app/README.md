# StartMachine agent-test application

This small Python application is a **throwaway test fixture**, not the implementation of the planned StartMachine feature. It is intentionally in-memory, so it does not exercise real TCP framing, socket handling or wire bytes.

- `machine_control.Session.handle` owns routing and request validation.
- `machine_control.MachineRegistry.stop` owns the existing machine-state transition.
- `Machine` holds `state` and `enabled`; `enabled` is not consulted by the existing StopMachine operation.
- Existing supported message: `{"type":"StopMachine","machine_id":"a"}`, returning an explicit success or error object.
- `StartMachine` is **not implemented**. An initial `StartMachine` request returns `{"ok":false,"error":"unknown_type"}`.

The test agent must follow the governing approved documents and verified code facts. A prompt without settled StartMachine requirements must **not** infer a wire format, authorization rules, eligibility rules, or error semantics merely from this example. For H2–H6, supply the actual approved feature documents and note that they are illustrative, not authoritative for an external TCP implementation.

Baseline verification: `python -m unittest discover -s tests -v`.

Fixture builder: `python skills/experimental_v4/tests/build_hierarchical_fixture.py <new-destination> --stage tasks`, from the source repository root. The builder creates a fresh Git repository with the project policy, a minimal ignored `.brain/`, and optionally the approved document layers from the structural fixture. Never run agents in the source fixture directory.
