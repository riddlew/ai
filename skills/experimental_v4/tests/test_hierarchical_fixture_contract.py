"""Deterministic fixture setup checks; not fresh-agent behavioral tests."""
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tests" / "build_hierarchical_fixture.py"
spec = importlib.util.spec_from_file_location("brain_fixture_builder", SCRIPT)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

VALIDATOR = ROOT / "brain-init" / "scripts" / "validate_feature_docs.py"


class HierarchicalFixtureContract(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.destination = Path(self.tmp.name) / "fixture"

    def test_no_docs_stage_has_clean_git_and_valid_brain(self):
        builder.build(self.destination, "none")
        self.assertEqual("", builder.git(self.destination, "status", "--porcelain"))
        self.assertTrue((self.destination / ".brain" / "00_index.md").is_file())
        self.assertFalse((self.destination / ".brain" / "features").exists())
        self.assertTrue((self.destination / "CLAUDE.local.md").is_file())

    def test_preapproved_stage_validates_as_complete_chain(self):
        for stage, count in (("brief", 1), ("spec", 2), ("components", 3),
                             ("plans", 4), ("tasks", 5)):
            with self.subTest(stage=stage):
                path = Path(self.tmp.name) / stage
                builder.build(path, stage)
                feature = path / ".brain" / "features" / "start-machine"
                self.assertEqual(count, sum((feature / x).is_dir() for x in builder.LAYERS))
                verified = subprocess.run(
                    ["python", str(VALIDATOR), str(path / ".brain" / "features"),
                     "--check-coverage"], capture_output=True, text=True,
                )
                self.assertEqual(0, verified.returncode, verified.stdout + verified.stderr)
                self.assertEqual("", builder.git(path, "status", "--porcelain"))

    def test_builder_refuses_overwrite(self):
        builder.build(self.destination)
        with self.assertRaises(FileExistsError):
            builder.build(self.destination, "tasks")

    def test_no_start_machine_implementation_in_baseline(self):
        builder.build(self.destination, "tasks")
        process = subprocess.run(
            ["python", "-m", "unittest", "discover", "-s", "tests"],
            cwd=self.destination, capture_output=True, text=True,
        )
        self.assertEqual(0, process.returncode, process.stdout + process.stderr)
        self.assertIn('message.get("type") != "StopMachine"',
                      (self.destination / "machine_control.py").read_text())


if __name__ == "__main__":
    unittest.main()
