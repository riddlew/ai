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
                ignored = subprocess.run(["git", "-C", str(repo),
                                          "check-ignore", "-q",
                                          "CLAUDE.local.md"], check=False)
                self.assertEqual(ignored.returncode, 0,
                                 "untracked personal policy must be excluded even when Brain is tracked")
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
                       "--kind", "planning-ticket", "--slug", "permission-check", *common)
                self.assertTrue((brain / "planning/demo/001-risk-review.md").is_file())
                self.assertTrue((brain / "planning/demo/002-permission-check.md").is_file())
                invoke(runtime, "doc", "--brain", brain, "--feature", "demo",
                       "--kind", "diagnosis", "--slug", "lost-update", *common)
                invoke(runtime, "doc", "--brain", brain, "--feature", "demo",
                       "--kind", "diagnosis", "--slug", "retry-storm", *common)
                self.assertTrue((brain / "diagnoses/01-lost-update.md").is_file())
                self.assertTrue((brain / "diagnoses/02-retry-storm.md").is_file())
                invoke(runtime, "doc", "--brain", brain, "--feature", "demo",
                       "--kind", "review", "--slug", "data-flow",
                       "--report-type", "architecture", *common)
                invoke(runtime, "doc", "--brain", brain, "--feature", "demo",
                       "--kind", "review", "--slug", "error-handling",
                       "--report-type", "architecture", *common)
                self.assertTrue((brain / "reviews/architecture/01-data-flow/review.md").is_file())
                self.assertTrue((brain / "reviews/architecture/02-error-handling/review.md").is_file())
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

    def test_init_preserves_customized_guide(self):
        for runtime in ("python", "node", "sh"):
            with self.subTest(runtime=runtime), tempfile.TemporaryDirectory() as temp:
                repo = Path(temp)
                subprocess.run(["git", "init", "-q", str(repo)], check=True)
                brain = repo / ".brain"
                brain.mkdir()
                guide = brain / "README.md"
                guide.write_text("# Custom project guide\n")
                run = invoke(runtime, "init", "--repo", repo, "--brain", brain,
                    "--tracking", "tracked", "--revision", "a"*40,
                    "--at", "2026-01-01", "--apply", "--authorized-root",
                    repo, ok=False)
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertEqual(guide.read_text(), "# Custom project guide\n")
                self.assertTrue((brain / "USAGE.md").is_file())
                self.assertIn("REVIEW", run.stdout)

    def test_options_are_rejected_when_unknown(self):
        for runtime in ("python", "node", "sh"):
            with self.subTest(runtime=runtime):
                result = invoke(runtime, "doc", "--brain", ".brain",
                    "--feature", "demo", "--kind", "brief",
                    "--unrecognized-flag", "x", ok=False)
                self.assertNotEqual(result.returncode, 0)


    def test_ignored_brain_and_local_policy_exclusions(self):
        for runtime in ("python", "node", "sh"):
            with self.subTest(runtime=runtime), tempfile.TemporaryDirectory() as temp:
                repo = Path(temp)
                subprocess.run(["git", "init", "-q", str(repo)], check=True)
                invoke(runtime, "init", "--repo", repo,
                       "--brain", repo / ".brain", "--tracking", "ignored",
                       "--revision", "a"*40, "--at", "2026-01-01",
                       "--apply", "--authorized-root", repo)
                for relative in (".brain/", "CLAUDE.local.md"):
                    outcome = subprocess.run(["git", "-C", str(repo),
                                              "check-ignore", "-q", relative],
                                             check=False)
                    self.assertEqual(outcome.returncode, 0, relative)
                exclude = Path(subprocess.check_output(
                    ["git", "-C", str(repo), "rev-parse",
                     "--path-format=absolute", "--git-common-dir"],
                    text=True).strip()) / "info/exclude"
                initial = exclude.read_text()
                invoke(runtime, "init", "--repo", repo,
                       "--brain", repo / ".brain", "--tracking", "ignored",
                       "--apply", "--authorized-root", repo)
                self.assertEqual(initial, exclude.read_text(),
                                 "Git exclusions must not be duplicated")


    def test_init_saves_location_without_rewriting_custom_policy(self):
        for runtime in ("python", "node", "sh"):
            with self.subTest(runtime=runtime), tempfile.TemporaryDirectory() as temp:
                repo = Path(temp)
                subprocess.run(["git", "init", "-q", str(repo)], check=True)
                brain = repo / ".brain"
                policy = repo / "CLAUDE.local.md"
                policy.write_text("# Local project instructions\nKeep this custom rule.\n")
                args = ("init", "--brain", brain, "--repo", repo,
                        "--tracking", "tracked", "--at", "2026-01-01",
                        "--revision", "a"*40, "--save-location",
                        "--apply", "--authorized-root", repo)
                invoke(runtime, *args)
                current = policy.read_text()
                expected = "Project brain: " + str(brain)
                self.assertEqual(current.count(expected), 1)
                self.assertIn("Keep this custom rule.", current)
                invoke(runtime, *args)
                self.assertEqual(current, policy.read_text())
                other = repo / ".brain-other"
                rejected = invoke(runtime, "init", "--brain", other,
                    "--repo", repo, "--tracking", "tracked",
                    "--at", "2026-01-01", "--revision", "a"*40,
                    "--save-location", "--apply", "--authorized-root", repo,
                    ok=False)
                self.assertNotEqual(rejected.returncode, 0)
                self.assertFalse(other.exists(),
                                 "conflict should fail before any document installation")


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

    def test_block_style_yaml_lists_work_in_all_runtimes(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / ".brain"
            shutil.copytree(FIXTURE, target)
            doc = target / "features/start-machine/05-tasks/TASK-001-registry-start.md"
            original = doc.read_text()
            doc.write_text(original.replace("parents: [PLAN-002]",
                                            "parents:\n  - PLAN-002"))
            for runtime in ("python", "node", "sh"):
                result = invoke(runtime, "validate", "--brain", target,
                                "--check-coverage")
                self.assertIn("VALID feature documents", result.stdout)


    def test_validation_rejects_structural_defects_in_every_runtime(self):
        changes = {
            "duplicate id": lambda root: shutil.copy2(
                root / "features/start-machine/05-tasks/TASK-001-registry-start.md",
                root / "features/start-machine/05-tasks/copy.md"),
            "stale parent": lambda root: (
                root / "features/start-machine/04-implementation-plans/machine-start.md"
            ).write_text((root / "features/start-machine/04-implementation-plans/machine-start.md"
                          ).read_text() + "\nChanged design.\n"),
            "unsupported list": lambda root: (
                root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
            ).write_text((root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
                          ).read_text().replace("parents: [PLAN-002]",
                                                "parents: PLAN-002")),
            "duplicate metadata": lambda root: (
                root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
            ).write_text((root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
                          ).read_text().replace("status: approved",
                                                "status: approved\nstatus: approved")),
            "missing required list": lambda root: (
                root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
            ).write_text((root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
                          ).read_text().replace("depends_on: []\n", "")),
            "duplicate parent reference": lambda root: (
                root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
            ).write_text((root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
                          ).read_text().replace("parents: [PLAN-002]",
                                                "parents: [PLAN-002, PLAN-002]")),
            "unexpected parent hash": lambda root: (
                root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
            ).write_text((root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
                          ).read_text().replace("parent_hashes: [PLAN-002@",
                                                "parent_hashes: [PLAN-999@" + "0"*40 + ", PLAN-002@")),
            "wrong kind for folder": lambda root: (
                root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
            ).write_text((root / "features/start-machine/05-tasks/TASK-001-registry-start.md"
                          ).read_text().replace("kind: task", "kind: specification")),
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


    def test_context_selection_fingerprints_and_estimates(self):
        rel = "features/start-machine/02-specifications/start-machine.md"
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / ".brain"
            shutil.copytree(FIXTURE, target)
            (target / "00_index.md").write_text("# Project Brain Index\n")
            expected = (target / rel).read_text()
            manifests = []
            for runtime in ("python", "node", "sh"):
                data = invoke(runtime, "context", "--brain", target, "--feature",
                              "start-machine", "--hashes", "--estimate").stdout
                self.assertIn("ESTIMATE bytes=", data)
                self.assertIn("DOC " + rel, data)
                manifests.append(data)
                selected = invoke(runtime, "context", "--brain", target,
                                  "--select", rel).stdout
                self.assertEqual(selected, expected)
                bad = invoke(runtime, "context", "--brain", target,
                             "--select", "../README.md", ok=False)
                self.assertNotEqual(bad.returncode, 0)
            self.assertEqual(manifests[0], manifests[1])
            self.assertEqual(manifests[0], manifests[2])


    def test_symlink_escape_is_rejected_in_every_runtime(self):
        for runtime in ("python", "node", "sh"):
            with self.subTest(runtime=runtime), tempfile.TemporaryDirectory() as temp:
                repo = Path(temp) / "repo"
                outside = Path(temp) / "outside"
                repo.mkdir()
                outside.mkdir()
                brain = repo / ".brain"
                brain.mkdir()
                (brain / "00_index.md").write_text("# Index\n")
                (outside / "demo").mkdir()
                (brain / "features").symlink_to(outside, target_is_directory=True)
                write = invoke(runtime, "doc", "--brain", brain,
                    "--feature", "demo", "--kind", "brief", "--apply",
                    "--authorized-root", repo, ok=False)
                self.assertNotEqual(write.returncode, 0)
                self.assertFalse((outside / "demo/01-brief").exists())
                (brain / "features").unlink()
                slot = brain / "features/demo"
                slot.mkdir(parents=True)
                external = outside / "execution.md"
                external.write_text("## Checkpoints\n")
                (slot / "execution.md").symlink_to(external)
                edit = invoke(runtime, "record", "--brain", brain,
                    "--feature", "demo", "--event", "verified",
                    "--detail", "some result", "--apply",
                    "--authorized-root", repo, ok=False)
                self.assertNotEqual(edit.returncode, 0)
                self.assertEqual(external.read_text(), "## Checkpoints\n")
                read = invoke(runtime, "context", "--brain", brain,
                    "--select", "features/demo/execution.md", ok=False)
                self.assertNotEqual(read.returncode, 0)


    def test_launcher_auto_falls_back_to_node_then_shell(self):
        with tempfile.TemporaryDirectory() as temp:
            tools_dir = Path(temp)
            for command in ("sh", "dirname"):
                (tools_dir / command).symlink_to(shutil.which(command))
            env = {**os.environ, "PATH": str(tools_dir), "BRAIN_RUNTIME": "auto"}
            shell = subprocess.run(["/bin/sh", str(TOOL), "--help"],
                                   env=env, text=True, capture_output=True)
            self.assertEqual(shell.returncode, 0, shell.stderr)
            self.assertIn("brain-tool", shell.stdout)
            node = tools_dir / "node"
            node.write_text("#!/bin/sh\necho NODE-FALLBACK\n")
            node.chmod(0o755)
            fallback = subprocess.run(["/bin/sh", str(TOOL), "--help"],
                                      env=env, text=True, capture_output=True)
            self.assertEqual(fallback.returncode, 0, fallback.stderr)
            self.assertIn("NODE-FALLBACK", fallback.stdout)


    def test_init_preflights_external_git_common_dir(self):
        for runtime in ("python", "node", "sh"):
            with self.subTest(runtime=runtime), tempfile.TemporaryDirectory() as temp:
                source = Path(temp) / "main"
                linked = Path(temp) / "linked"
                subprocess.run(["git", "init", "-q", str(source)], check=True)
                subprocess.run(["git", "-C", str(source), "-c", "user.name=CI",
                                "-c", "user.email=ci@example.com", "commit",
                                "--allow-empty", "-qm", "base"], check=True)
                subprocess.run(["git", "-C", str(source), "worktree",
                                "add", "-q", "-b", "test-worktree", str(linked)], check=True)
                result = invoke(runtime, "init", "--repo", linked,
                    "--brain", linked / ".brain", "--tracking", "ignored",
                    "--apply", "--authorized-root", linked, ok=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((linked / ".brain").exists(),
                                 "unauthorized Git exclude must not leave a partial Brain")
                self.assertFalse((linked / "CLAUDE.local.md").exists(),
                                 "preflight must run before installing a policy")


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
