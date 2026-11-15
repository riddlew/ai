"""Deterministic fixture setup checks; not fresh-agent behavioral tests."""
import importlib.util
import subprocess
import sys
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
        self.assertTrue((self.destination / ".brain" / builder.ADR_PATH).is_file())
        self.assertFalse((self.destination / ".brain" / "features").exists())
        self.assertFalse((self.destination / "CLAUDE.local.md").exists())

    def test_baseline_revision_is_reproducible(self):
        other = Path(self.tmp.name) / "other"
        builder.build(self.destination, "none")
        builder.build(other, "tasks")
        self.assertEqual(builder.git(self.destination, "rev-parse", "HEAD"),
                         builder.git(other, "rev-parse", "HEAD"))

    def test_preapproved_stage_validates_as_complete_chain(self):
        for stage, count in (("brief", 1), ("spec", 2), ("components", 3),
                             ("plans", 4), ("tasks", 5)):
            with self.subTest(stage=stage):
                path = Path(self.tmp.name) / stage
                builder.build(path, stage)
                feature = path / ".brain" / "features" / "start-machine"
                self.assertEqual(count, sum((feature / x).is_dir() for x in builder.LAYERS))
                verified = subprocess.run(
                    [sys.executable, str(VALIDATOR), str(path / ".brain" / "features"),
                     "--check-coverage"], capture_output=True, text=True,
                )
                self.assertEqual(0, verified.returncode, verified.stdout + verified.stderr)
                self.assertEqual("", builder.git(path, "status", "--porcelain"))
                index = (path / ".brain" / "00_index.md").read_text()
                self.assertIn("features/start-machine/01-brief/brief.md", index)

    def test_plans_record_the_inspected_baseline(self):
        builder.build(self.destination, "plans")
        head = builder.git(self.destination, "rev-parse", "HEAD")
        for plan in (self.destination / ".brain/features/start-machine/04-implementation-plans").glob("*.md"):
            self.assertIn(f"Design inspected at: {head}", plan.read_text())

    def test_builder_refuses_overwrite(self):
        builder.build(self.destination)
        with self.assertRaises(FileExistsError):
            builder.build(self.destination, "tasks")

    def test_no_start_machine_implementation_in_baseline(self):
        builder.build(self.destination, "tasks")
        process = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
            cwd=self.destination, capture_output=True, text=True,
        )
        self.assertEqual(0, process.returncode, process.stdout + process.stderr)
        source = (self.destination / "machine_control.py").read_text()
        self.assertIn('message.get("type") != "StopMachine"', source)
        self.assertNotIn("def start", source)

    def test_fixture_source_does_not_describe_itself_as_a_test(self):
        for path in (builder.APP / "README.md", builder.APP / "machine_control.py"):
            text = path.read_text().lower()
            for word in ("fixture", "agent", "skill", "throwaway"):
                self.assertNotIn(word, text, f"{path.name} mentions {word!r}")


if __name__ == "__main__":
    unittest.main()
