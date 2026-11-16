"""Cross-runtime smoke and parity contracts for dependency-free Brain tooling."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "brain-init/scripts/brain-tool"
VALIDATOR = ROOT / "brain-init/scripts/validate_feature_docs.py"
FIXTURE = ROOT / "tests/fixture/hierarchical-brain/.brain"


def invoke(runtime, *args, cwd=None, ok=True):
    env = {**os.environ, "BRAIN_RUNTIME": runtime}
    r = subprocess.run(["sh", str(TOOL), *map(str, args)], cwd=cwd,
                       env=env, text=True, capture_output=True)
    if ok and r.returncode:
        raise AssertionError(f"{runtime} {args}: {r.stderr}\n{r.stdout}")
    return r


def snapshot(root):
    return {str(p.relative_to(root)): p.read_bytes()
            for p in root.rglob("*") if p.is_file() and ".git" not in p.parts}


@unittest.skipUnless(shutil.which("node") and shutil.which("python3"),
                     "Python and Node required for full parity tests")
class DeterministicCliContract(unittest.TestCase):
    def test_init_doc_record_context_and_git_parity(self):
        outcomes = []
        for runtime in ("python", "node", "sh"):
            with tempfile.TemporaryDirectory() as temp:
                repo = Path(temp)
                subprocess.run(["git", "init", "-q", str(repo)], check=True)
                subprocess.run(["git", "-C", str(repo), "-c", "user.name=CI",
                                "-c", "user.email=ci@example.com", "commit",
                                "--allow-empty", "-qm", "base"], check=True)
                brain = repo / ".brain"
                opts = ("--brain", brain, "--repo", repo)
                common = ("--apply", "--authorized-root", repo)
                invoke(runtime, "init", *opts, "--tracking", "tracked",
                       "--at", "2026-01-01", "--revision", "a"*40, *common)
                first = snapshot(repo)
                invoke(runtime, "init", *opts, "--tracking", "tracked", *common)
                self.assertEqual(first, snapshot(repo), "init must be idempotent")
                invoke(runtime, "doc", "--brain", brain, "--feature", "demo",
                       "--kind", "brief", *common)
                invoke(runtime, "doc", "--brain", brain, "--feature", "demo",
                       "--kind", "specification", "--slug", "start",
                       "--parent", "BRF-001", *common)
                desc = (brain / "features/demo/02-specifications/start.md").read_text()
                self.assertIn("id: SPEC-001", desc)
                self.assertIn("parents: [BRF-001]", desc)
                self.assertIn("status: draft", desc)
                self.assertNotIn("REQ-001:", desc, "template examples are not requirements")
                self.assertIn("AFFECTED SPEC-001", invoke(
                    runtime, "validate", "--brain", brain,
                    "--affected", "BRF-001").stdout)
                self.assertIn("VALID feature documents", invoke(
                    runtime, "validate", "--brain", brain).stdout)
                self.assertNotEqual(invoke(runtime, "doc", "--brain", brain,
                    "--feature", "demo", "--kind", "specification",
                    "--slug", "start", "--parent", "BRF-001", *common,
                    ok=False).returncode, 0)
                invoke(runtime, "doc", "--brain", brain, "--feature", "demo",
                       "--kind", "execution", *common)
                invoke(runtime, "doc", "--brain", brain, "--feature", "demo",
                       "--kind", "planning-index", *common)
                invoke(runtime, "doc", "--brain", brain, "--feature", "demo",
                       "--kind", "planning-ticket", "--slug", "risk-review", *common)
                invoke(runtime, "doc", "--brain", brain, "--feature", "demo",
                       "--kind", "diagnosis", "--slug", "lost-update", *common)
                invoke(runtime, "doc", "--brain", brain, "--feature", "demo",
                       "--kind", "review", "--slug", "data-flow",
                       "--report-type", "architecture", *common)
                invoke(runtime, "git", "--repo", repo, "--brain", brain,
                       "--pending", "--branch", "feature/demo",
                       "--at", "2026-01-01", *common)
                self.assertIn("Branch: feature/demo",
                    (brain / "pending/feature--demo.md").read_text())
                record = brain / "features/demo/execution.md"
                invoke(runtime, "record", "--brain", brain, "--feature", "demo",
                       "--event", "test", "--detail", "passed", *common)
                before = record.read_bytes()
                invoke(runtime, "record", "--brain", brain, "--feature", "demo",
                       "--event", "test", "--detail", "passed", *common)
                self.assertEqual(before, record.read_bytes())
                manifest = invoke(runtime, "context", "--brain", brain,
                                  "--feature", "demo").stdout
                self.assertIn("DOC features/demo/02-specifications/start.md", manifest)
                self.assertIn("DOC 00_index.md", manifest)
                listing = invoke(runtime, "git", "--repo", repo).stdout
                self.assertIn("BRANCH", listing)
                self.assertIn("HEAD", listing)
                outcomes.append(snapshot(repo))
        self.assertEqual(outcomes[0], outcomes[1], "Node files differ from Python")
        self.assertEqual(outcomes[0], outcomes[2], "shell files differ from Python")

    def test_fixture_validation_and_parent_hashes(self):
        expected = subprocess.run(["python3", str(VALIDATOR),
                         str(FIXTURE / "features"), "--check-coverage"],
                         text=True, capture_output=True)
        self.assertEqual(expected.returncode, 0, expected.stderr + expected.stdout)
        doc = FIXTURE / "features/start-machine/05-tasks/TASK-001-registry-start.md"
        expected_hashes = subprocess.run(["python3", str(VALIDATOR),
                         "--show-parent-hashes", str(doc)],
                         text=True, capture_output=True)
        self.assertEqual(expected_hashes.returncode, 0, expected_hashes.stderr)
        for runtime in ("python", "node", "sh"):
            result = invoke(runtime, "validate", "--brain", FIXTURE,
                            "--check-coverage")
            self.assertIn("VALID feature documents", result.stdout)
            got = invoke(runtime, "validate", "--brain", FIXTURE,
                         "--show-parent-hashes", doc)
            self.assertEqual(expected_hashes.stdout.strip(), got.stdout.strip())

    def test_validation_rejects_structural_defects_in_every_runtime(self):
        changes = {
            "duplicate id": lambda root: shutil.copy2(
                root / "features/start-machine/05-tasks/TASK-001-registry-start.md",
                root / "features/start-machine/05-tasks/copy.md"),
            "stale parent": lambda root: (
                root / "features/start-machine/04-implementation-plans/machine-start.md"
            ).write_text((root / "features/start-machine/04-implementation-plans/machine-start.md"
                          ).read_text() + "\\nChanged design.\\n"),
            "unsupported list": lambda root: (
                root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
            ).write_text((root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
                          ).read_text().replace("parents: [PLAN-002]",
                                                "parents: PLAN-002")),
            "unknown parent": lambda root: (
                root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
            ).write_text((root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
                          ).read_text().replace("parents: [PLAN-002]",
                                                "parents: [PLAN-999]")),
            "unknown requirement": lambda root: (
                root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
            ).write_text((root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
                          ).read_text().replace("SPEC-001#REQ-002",
                                                "SPEC-999#REQ-001")),
        }
        for name, change in changes.items():
            with self.subTest(defect=name), tempfile.TemporaryDirectory() as temp:
                target = Path(temp) / ".brain"
                shutil.copytree(FIXTURE, target)
                change(target)
                expected = subprocess.run(
                    ["python3", str(VALIDATOR), str(target / "features")],
                    text=True, capture_output=True)
                self.assertNotEqual(expected.returncode, 0, name)
                for runtime in ("python", "node", "sh"):
                    got = invoke(runtime, "validate", "--brain", target, ok=False)
                    self.assertNotEqual(got.returncode, 0,
                                        f"{runtime} accepted {name}: {got.stdout}")


    def test_denied_write_and_preview(self):
        for runtime in ("python", "node", "sh"):
            with tempfile.TemporaryDirectory() as temp:
                repo = Path(temp)
                brain = repo / ".brain"
                invoke(runtime, "doc", "--brain", brain, "--feature", "demo",
                       "--kind", "brief")
                self.assertFalse(brain.exists(), "dry-run should not create files")
                result = invoke(runtime, "doc", "--brain", brain, "--feature", "demo",
                       "--kind", "brief", "--apply",
                       "--authorized-root", repo / "outside", ok=False)
                self.assertNotEqual(0, result.returncode)
                self.assertFalse(brain.exists(), "unauthorized write must not create files")


if __name__ == "__main__":
    unittest.main()
