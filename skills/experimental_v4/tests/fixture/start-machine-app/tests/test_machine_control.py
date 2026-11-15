"""Only existing StopMachine behavior is tested at the fixture baseline."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from machine_control import Machine, MachineRegistry, Session


class ExistingBehavior(unittest.TestCase):
    def setUp(self):
        self.machine = Machine(state="running")
        self.registry = MachineRegistry({"a": self.machine})
        self.session = Session(self.registry)

    def test_stop_running_machine(self):
        self.assertEqual({"ok": True, "state": "stopped"},
                         self.session.handle({"type": "StopMachine", "machine_id": "a"}))
        self.assertEqual("stopped", self.machine.state)

    def test_stop_does_not_change_ineligible_machine(self):
        self.machine.state = "stopped"
        self.assertEqual({"ok": False, "error": "not_running"},
                         self.session.handle({"type": "StopMachine", "machine_id": "a"}))
        self.assertEqual("stopped", self.machine.state)

    def test_stop_unknown_machine(self):
        self.assertEqual({"ok": False, "error": "machine_not_found"},
                         self.session.handle({"type": "StopMachine", "machine_id": "missing"}))

    def test_unknown_message_does_not_change_machine(self):
        self.assertEqual({"ok": False, "error": "unknown_type"},
                         self.session.handle({"type": "StartMachine", "machine_id": "a"}))
        self.assertEqual("running", self.machine.state)

    def test_malformed_message(self):
        for message in (None, "StopMachine", {}, {"type": "StopMachine", "machine_id": 42}):
            with self.subTest(message=message):
                result = self.session.handle(message)
                self.assertEqual(False, result["ok"])
        self.assertEqual("running", self.machine.state)


if __name__ == "__main__":
    unittest.main()
