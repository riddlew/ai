"""Small, dependency-free reference application for Brain skill testing.

There is deliberately no StartMachine behavior in the initial application.
The Session owns protocol routing; MachineRegistry owns machine state changes.
This exercises a functional boundary but is not a production TCP server.
"""
from dataclasses import dataclass


@dataclass
class Machine:
    state: str = "stopped"
    enabled: bool = True


class MachineRegistry:
    def __init__(self, machines: dict[str, Machine]):
        self.machines = machines

    def stop(self, machine_id: str) -> dict:
        machine = self.machines.get(machine_id)
        if machine is None:
            return {"ok": False, "error": "machine_not_found"}
        if machine.state != "running":
            return {"ok": False, "error": "not_running"}
        machine.state = "stopped"
        return {"ok": True, "state": machine.state}


class Session:
    """Existing message dispatcher; do not move connection/session ownership."""

    def __init__(self, registry: MachineRegistry):
        self.registry = registry

    def handle(self, message: object) -> dict:
        if not isinstance(message, dict):
            return {"ok": False, "error": "invalid_message"}
        if message.get("type") != "StopMachine":
            return {"ok": False, "error": "unknown_type"}
        machine_id = message.get("machine_id")
        if not isinstance(machine_id, str) or not machine_id:
            return {"ok": False, "error": "invalid_message"}
        return self.registry.stop(machine_id)
