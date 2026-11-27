"""Validate hierarchical scenario setup without claiming agent behavior was tested."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tests" / "prepare_hierarchical_scenario.py"
spec = importlib.util.spec_from_file_location("brain_scenarios", SCRIPT)
scenarios = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = scenarios  # dataclasses resolve their module
spec.loader.exec_module(scenarios)
CHECKER = ROOT / "brain-init" / "scripts" / "validate_feature_docs.py"
FEATURE = ".brain/features/start-machine"


def validate(features: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(CHECKER), str(features), "--check-coverage"],
                          capture_output=True, text=True)


class HierarchicalScenarioContract(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def prepare(self, name, **kwargs):
        return scenarios.prepare(self.root / name.lower(), name, **kwargs)

    def test_each_scenario_creates_separate_runnable_fixture(self):
        for name in sorted(scenarios.SCENARIOS):
            with self.subTest(name=name):
                prepared = self.prepare(name)
                self.assertTrue((prepared.cwd / "machine_control.py").is_file())
                self.assertTrue((prepared.repo / ".brain" / "00_index.md").is_file())
                self.assertTrue((prepared.repo / ".git").exists())
                self.assertTrue(prepared.trigger)
                self.assertNotIn("{validator}", prepared.trigger)
                self.assertNotIn("results", str(prepared.cwd).lower())

    def test_triggers_do_not_state_the_rules_under_test(self):
        leaks = ("needs-revision", "parent_hashes", "canonical", "five-level", "five-document",
                 "do not migrate", "authoritative", "fingerprint", "invent")
        for name, (_, _, context, trigger) in scenarios.SCENARIOS.items():
            with self.subTest(name=name):
                for word in leaks:
                    self.assertNotIn(word, (context + trigger).lower())

    def test_policy_is_installed_untracked_only_when_given(self):
        policy = self.root / "policy.md"
        policy.write_text("# Policy\n")
        prepared = self.prepare("H3", policy=policy)
        self.assertEqual("# Policy\n", (prepared.repo / "CLAUDE.local.md").read_text())
        self.assertEqual("", scenarios.builder.git(prepared.repo, "status", "--porcelain"))
        self.assertFalse((self.prepare("H4").repo / "CLAUDE.local.md").exists())

    def test_h2_has_approved_brief_contract_adr_and_open_decisions(self):
        prepared = self.prepare("H2")
        brief = (prepared.repo / FEATURE / "01-brief" / "brief.md").read_text()
        self.assertIn("status: approved", brief)
        self.assertIn("## Open decisions", brief)
        self.assertTrue((prepared.repo / "docs" / "machine-protocol.md").is_file())
        self.assertTrue((prepared.repo / ".brain" / scenarios.builder.ADR_PATH).is_file())
        self.assertFalse((prepared.repo / FEATURE / "02-specifications").exists())
        decisions = (prepared.repo / ".brain" / "09_user_decisions.md").read_text()
        self.assertNotIn("not_eligible", decisions)

    def test_h6b_has_checkpoint_awaiting_review_and_later_user_edit(self):
        prepared = self.prepare("H6B")
        record = (prepared.repo / FEATURE / "execution.md").read_text()
        self.assertIn("TASK-001: verified awaiting review", record)
        head = scenarios.builder.git(prepared.repo, "rev-parse", "HEAD")
        self.assertIn(f"Review base: {head}", record)
        for path in ("machine_control.py", "tests/test_machine_control.py"):
            blob = scenarios.builder.git(prepared.repo, "hash-object", path)
            self.assertNotIn(blob, record, f"{path} should differ from the reviewed checkpoint")
        self.assertIn("def start", (prepared.repo / "machine_control.py").read_text())
        run = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                             cwd=prepared.repo, capture_output=True, text=True)
        self.assertEqual(0, run.returncode, run.stderr)
        self.assertIn("Ran 10 tests", run.stderr)

    @unittest.skip("Legacy v4 instruction contract superseded; see test_v5_workflow.py")

    def test_h7_has_independent_approved_scope(self):
        prepared = self.prepare("H7")
        features = prepared.repo / ".brain/features"
        self.assertTrue((features / "start-machine/02-specifications/audit.md").is_file())
        result = validate(features)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        spec1 = features / "start-machine/02-specifications/start-machine.md"
        spec1.write_text(spec1.read_text() + "\nUser changes eligibility.\n")
        result = validate(features)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("stale parent hash for SPEC-001", result.stdout)
        self.assertNotIn("stale parent hash for SPEC-002", result.stdout)

    def test_h8_has_targeted_committed_bug(self):
        prepared = self.prepare("H8")
        self.assertIn('machine.state = "idle"', (prepared.repo / "machine_control.py").read_text())
        self.assertEqual("", scenarios.builder.git(prepared.repo, "status", "--porcelain"))
        self.assertFalse((prepared.repo / ".brain" / "features").exists())
        run = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                             cwd=prepared.repo, capture_output=True, text=True)
        self.assertNotEqual(0, run.returncode)

    @unittest.skip("Legacy v4 instruction contract superseded; see test_v5_workflow.py")

    def test_h9_reports_each_structural_defect_and_corrected_fixture_passes(self):
        prepared = self.prepare("H9")
        result = validate(prepared.repo / ".brain/features")
        self.assertEqual(1, result.returncode)
        for message in ("duplicate id TASK-001", "unknown parent PLAN-009",
                        "dependency PLAN-002 must be at the same level",
                        "unknown requirement SPEC-001#REQ-009", "dependency cycle"):
            self.assertIn(message, result.stdout)
        corrected = scenarios.builder.build(self.root / "corrected", "tasks")
        self.assertEqual(0, validate(corrected / ".brain/features").returncode)

    def test_h10_restricted_worktree_states_its_write_scope(self):
        for name in ("H10A", "H10B"):
            with self.subTest(name=name):
                prepared = self.prepare(name)
                self.assertEqual(prepared.repo / ".claude/worktrees/h10", prepared.cwd)
                self.assertIsNone(prepared.worktree, "scope must not depend on environment enforcement")
                self.assertEqual(prepared.cwd, prepared.launch)
                self.assertEqual([], prepared.add_dirs)
                self.assertIn(f"authorized writes inside {prepared.cwd} and nowhere else", prepared.context)
                self.assertIn(f"main checkout at {prepared.repo} is outside this session's authorized "
                              "write scope", prepared.context)
                self.assertFalse((prepared.cwd / ".brain").exists())
                self.assertTrue((prepared.repo / FEATURE / "execution.md").is_file())
                self.assertEqual("agent-h10", scenarios.builder.git(
                    prepared.cwd, "branch", "--show-current"))
                status = scenarios.builder.git(prepared.cwd, "status", "--porcelain")
                self.assertIn("M README.md", status)
                self.assertIn("?? notes/", status)
                self.assertEqual("", scenarios.builder.git(prepared.repo, "status", "--porcelain"))

    @unittest.skip("Legacy v4 instruction contract superseded; see test_v5_workflow.py")

    def test_h7_needs_revision_blocks_only_the_revised_chain(self):
        prepared = self.prepare("H7")
        features = prepared.repo / ".brain/features"
        spec1 = features / "start-machine/02-specifications/start-machine.md"
        spec1.write_text(spec1.read_text().replace("status: approved", "status: needs-revision", 1)
                         .replace("state stays `\"running\"`", "state stays `\"running\"` (revised)"))
        result = validate(features)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("approved document has unapproved parent SPEC-001", result.stdout)
        for unaffected in ("audit.md", "audit-reporting.md", "audit-log.md", "TASK-003", "SPEC-002"):
            self.assertNotIn(unaffected, result.stdout)

    def test_h10e_ordinary_worktree_session_can_write_the_shared_brain(self):
        prepared = self.prepare("H10E")
        self.assertIsNone(prepared.worktree)
        self.assertEqual(prepared.repo / ".claude/worktrees/h10", prepared.cwd)
        self.assertEqual(prepared.cwd, prepared.launch)
        self.assertEqual([prepared.repo / ".brain"], prepared.add_dirs)
        self.assertTrue((prepared.repo / FEATURE / "execution.md").is_file())
        self.assertFalse((prepared.cwd / ".brain").exists())

    def test_h10_external_brain_wins_over_stale_main_checkout_copy(self):
        for name in ("H10C", "H10D"):
            with self.subTest(name=name):
                prepared = self.prepare(name)
                (outside,) = prepared.add_dirs
                self.assertFalse(outside.is_relative_to(prepared.repo))
                self.assertIn(f"Project brain: {outside}",
                              (prepared.repo / "CLAUDE.local.md").read_text())
                self.assertTrue((outside / "features/start-machine/execution.md").is_file())
                self.assertEqual(0, validate(outside / "features").returncode)
                self.assertTrue((prepared.repo / ".brain/00_index.md").is_file())
                self.assertFalse((prepared.repo / FEATURE / "05-tasks").exists())

    def test_h11_keeps_legacy_documents_beside_shared_knowledge(self):
        prepared = self.prepare("H11")
        brain = prepared.repo / ".brain"
        self.assertIn("MachineManager", (brain / "specs/01-start-machine.md").read_text())
        self.assertTrue((brain / "tickets" / "01-machine-manager.md").is_file())
        self.assertTrue((brain / scenarios.builder.ADR_PATH).is_file())
        self.assertFalse((brain / "features").exists())


if __name__ == "__main__":
    unittest.main()
