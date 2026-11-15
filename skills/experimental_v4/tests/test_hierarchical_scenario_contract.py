"""Validate H1–H11 setup without claiming agent behavior was tested."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tests" / "prepare_hierarchical_scenario.py"
spec = importlib.util.spec_from_file_location("brain_scenarios", SCRIPT)
scenarios = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scenarios)


class HierarchicalScenarioContract(unittest.TestCase):
    def test_each_scenario_creates_separate_runnable_fixture(self):
        for name in sorted(scenarios.SCENARIOS):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                destination = Path(tmp) / "agent-fixture"
                actual, trigger = scenarios.prepare(destination, name)
                self.assertTrue((actual / "machine_control.py").is_file())
                self.assertTrue((actual / "CLAUDE.local.md").is_file())
                self.assertTrue(trigger)
                self.assertTrue((destination / ".brain" / "00_index.md").is_file())
                self.assertTrue((destination / ".git").exists())
                self.assertNotIn("results", str(actual).lower())

    def test_h9_is_intentionally_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "bad"
            scenarios.prepare(destination, "H9")
            bad_task = destination / ".brain/features/start-machine/05-tasks/TASK-002-route-message.md"
            self.assertIn("PLAN-999", bad_task.read_text())

    def test_h10_is_linked_worktree_with_ignored_brain_in_main(self):
        with tempfile.TemporaryDirectory() as tmp:
            main = Path(tmp) / "main"
            worktree, _ = scenarios.prepare(main, "H10")
            self.assertNotEqual(main, worktree)
            self.assertFalse((worktree / ".brain").exists())
            self.assertTrue((main / ".brain" / "00_index.md").is_file())

    def test_h11_keeps_legacy_notes_separate(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "legacy"
            scenarios.prepare(dest, "H11")
            self.assertTrue((dest / ".brain" / "tickets" / "legacy.md").is_file())
            self.assertFalse((dest / ".brain" / "features").exists())


if __name__ == "__main__":
    unittest.main()
